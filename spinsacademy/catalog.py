"""Cycle de vie des datasets (cahier des charges §2, §13.1 et §16) : contrôle, publication, retrait.

Un dataset est un dossier immuable data/datasets/<dataset>/<version> (manifest.json + spots.jsonl) produit hors ligne
par spinsacademy.importer (GTO) ou spinsacademy.exploit (exploitant) : c'est l'import, en « staging ».
Son statut vit dans la base de l'application (table datasets) :
  staging  -> validated (contrôles passés) | rejected (au moins un contrôle bloquant en échec)
  validated -> published : la version servie aux nouvelles séries ; l'ancienne version publiée devient « retired »
  published / retired / validated -> disabled : retrait immédiat (motif obligatoire)
  retired / disabled -> published : retour arrière, si le rapport de contrôle est toujours valable (fichiers inchangés)
Une seule version publiée par dataset. Un dataset exploitant ne peut être publié que si son dataset GTO source l'est.
Les séries déjà commencées gardent leur version pour la correction ; une version retirée (disabled) ne sert plus de
question. Chaque action est inscrite au journal d'administration (acteur, date, motif).
"""
import datetime, hashlib, json, os
import numpy as np
from . import quiz
from .cards import NAMES

KINDS = ('gto_preflop', 'exploit_calls')
STATUS_FR = {'staging': 'À contrôler', 'validated': 'Contrôlé', 'rejected': 'Refusé au contrôle', 'published': 'Publié',
             'retired': 'Remplacé', 'disabled': 'Retiré'}
SCHEMA = """
CREATE TABLE IF NOT EXISTS datasets(ref TEXT PRIMARY KEY, dataset TEXT NOT NULL, version TEXT NOT NULL, status TEXT NOT NULL,
  spots_sha256 TEXT, report TEXT, validated_at TEXT, published_at TEXT, updated_at TEXT, actor TEXT, reason TEXT);
"""


def _now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def full_ref(ref):
    """« 2026.10.12-2 » (ancienne forme, dataset GTO) ou « dataset/version » -> « dataset/version »"""
    return ref if '/' in ref else f'gto_preflop/{ref}'


def folders():
    """versions présentes sur disque : [(ref, manifest)]"""
    out = []
    for ds in KINDS:
        base = os.path.join(quiz.DATASETS, ds)
        if not os.path.isdir(base): continue
        for v in sorted(os.listdir(base)):
            m = os.path.join(base, v, 'manifest.json')
            if os.path.isfile(m): out.append((f'{ds}/{v}', json.load(open(m))))
    return out


def _sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ contrôles
def _check(cid, label, ok, details='', blocking=True, count=None):
    """level : ok, fail (bloquant) ou warn (avertissement, n'empêche pas la publication)"""
    return dict(id=cid, label_fr=label, ok=bool(ok), blocking=blocking, level='ok' if ok else ('fail' if blocking else 'warn'),
                details_fr=details, count=count)


def _spot_problems(sp, manifest, exploit):
    """liste des anomalies d'un spot (chaînes en français)"""
    p = []
    for k in ('spot_id', 'table', 'players', 'stacks_bb', 'hero', 'node_key', 'history', 'pot_bb', 'to_call_bb', 'actions', 'ev_reference', 'hands'):
        if k not in sp: p.append(f'champ {k} manquant')
    if p: return p
    if len(sp['players']) != len(sp['stacks_bb']): p.append('autant de tapis que de joueurs attendus')
    if sp['hero'] not in sp['players']: p.append('héros absent de la table')
    if any(h['position'] not in sp['players'] for h in sp['history']): p.append('historique : position inconnue')
    if any(h['position'] == sp['hero'] and h['action'] == 'fold' for h in sp['history']): p.append('le héros a déjà foldé')
    ids = [a['id'] for a in sp['actions']]
    if len(ids) < 2 or len(set(ids)) != len(ids): p.append('au moins deux actions distinctes attendues')
    if sp['to_call_bb'] > 0 and 'X' in ids: p.append('check proposé face à une mise')
    if sp['to_call_bb'] <= 0 and 'F' in ids: p.append('fold proposé sans mise à payer')
    for a in sp['actions']:
        if a.get('to_bb') is not None and a['to_bb'] > max(sp['stacks_bb']) + 1e-6: p.append(f'action {a["id"]} au-delà du plus gros tapis')
    if set(sp['hands']) != set(NAMES): p.append('169 classes de mains attendues'); return p
    if sp['ev_reference'] not in ('exact', 'hrc'): p.append('source d\'EV inconnue')
    min_reach = manifest.get('min_reach_for_questions', 0.0); max_regret = manifest.get('max_self_regret_mbb')
    n = len(ids); bad_norm = bad_ev = bad_rule = 0; eligible = 0
    for h, x in sp['hands'].items():
        f = x.get('freq')
        if x.get('reach', 0) > 0 and f is not None:
            if len(f) != n or min(f) < -1e-9 or abs(sum(f) - 1) > 2e-3: bad_norm += 1
        if not x.get('quiz_eligible'): continue
        eligible += 1
        ev = x.get('ev_exact') if sp['ev_reference'] == 'exact' else x.get('ev_hrc')
        if ev is None or len(ev) != n or any(e is None or not np.isfinite(e) for e in ev): bad_ev += 1
        if x['reach'] < min_reach - 1e-9 or (not exploit and max_regret is not None and x.get('hrc_self_regret_mbb', 0) > max_regret + 1e-9): bad_rule += 1
    if bad_norm: p.append(f'{bad_norm} mains aux fréquences non normalisées')
    if bad_ev: p.append(f'{bad_ev} mains proposables sans EV de référence complète')
    if bad_rule: p.append(f'{bad_rule} mains proposables hors des règles d\'éligibilité du manifeste')
    if eligible == 0: p.append('aucune main proposable')
    if sp.get('eligible_hands') != eligible: p.append('compte de mains proposables incohérent')
    if exploit and not sp.get('villain'): p.append('profil du vilain manquant')
    return p


def _rebuild(ref, manifest, spots):
    """test de référence : les spots publiés sont reproduits à l'identique depuis leurs sources ; (ok, bloquant, détail)"""
    ds = ref.split('/')[0]
    try:
        if ds == 'gto_preflop':
            from . import importer
            if manifest.get('importer') != importer.IMPORTER_VERSION:
                return None, f"importeur {manifest.get('importer')} ≠ version actuelle {importer.IMPORTER_VERSION} : reconstruction non comparable"
            missing = [s for s in manifest.get('sources', []) if not os.path.isdir(os.path.join(quiz.ROOT, s))]
            if missing: return None, f'{len(missing)} exports sources absents de ce poste : reconstruction non exécutée'
            rebuilt = {sp['spot_id']: sp for sp in importer.build_dataset()[0]}
        else:
            from . import exploit
            if manifest.get('builder') != exploit.BUILDER_VERSION:
                return None, f"générateur {manifest.get('builder')} ≠ version actuelle {exploit.BUILDER_VERSION} : reconstruction non comparable"
            rebuilt = {sp['spot_id']: sp for sp in exploit.build(manifest['source_gto_dataset'])[1]}
    except Exception as e:                                  # source illisible : on le dit, on ne bloque pas en silence
        return False, f'reconstruction impossible : {e}'
    norm = lambda o: json.loads(json.dumps(o))
    diff = [sid for sid, sp in spots.items() if sid not in rebuilt or norm(rebuilt[sid]) != norm(sp)]
    if diff: return False, f'{len(diff)} spots diffèrent de leur reconstruction (premier : {diff[0]})'
    return True, f'{len(spots)} spots reproduits à l\'identique depuis leurs sources'


def validate(ref, statuses=None):
    """rapport de contrôle lisible (§16) ; statuses : {ref: statut} pour les dépendances entre datasets"""
    ref = full_ref(ref); ds, version = ref.split('/', 1); d = quiz.ref_path(ref); checks = []
    mpath, spath = os.path.join(d, 'manifest.json'), os.path.join(d, 'spots.jsonl')
    if not (os.path.isfile(mpath) and os.path.isfile(spath)):
        checks.append(_check('files', 'Fichiers manifest.json et spots.jsonl présents', False, 'fichier manquant'))
        return _report(ref, checks, None)
    manifest = json.load(open(mpath)); sha = _sha(spath)
    checks.append(_check('manifest', 'Manifeste cohérent avec le dossier', manifest.get('dataset') == ds and manifest.get('version') == version,
                         f"dataset {manifest.get('dataset')}, version {manifest.get('version')}"))
    checks.append(_check('integrity', 'Fichier des spots identique à celui du manifeste (empreinte SHA-256)', sha == manifest.get('spots_sha256'),
                         'fichiers modifiés après génération' if sha != manifest.get('spots_sha256') else 'empreinte conforme'))
    try:
        rows = [json.loads(l) for l in open(spath) if l.strip()]
    except ValueError as e:
        checks.append(_check('parse', 'Lecture des spots', False, str(e))); return _report(ref, checks, sha)
    ids = [r.get('spot_id') for r in rows]; spots = {r.get('spot_id'): r for r in rows}
    checks.append(_check('count', 'Nombre de spots conforme au manifeste', len(rows) == manifest.get('spots'), f'{len(rows)} spots', count=len(rows)))
    dup = len(ids) - len(set(ids))
    checks.append(_check('duplicates', 'Aucun spot en double', dup == 0, f'{dup} doublons' if dup else 'aucun doublon'))
    exploit = ds == 'exploit_calls'; problems = {}
    for sp in rows:
        pr = _spot_problems(sp, manifest, exploit)
        if pr: problems[sp.get('spot_id')] = pr
    first = next(iter(problems.items()), None)
    checks.append(_check('spots', 'Chaque spot est complet, légal et noté sur des données valides', not problems,
                         f"{len(problems)} spots en anomalie ; premier : {first[0]} : {', '.join(first[1])}" if first else f'{len(rows)} spots conformes',
                         count=len(problems)))
    elig = sum(sp.get('eligible_hands', 0) for sp in rows)
    checks.append(_check('questions', 'Questions proposables conformes au manifeste', elig == manifest.get('questions_eligible'), f'{elig} questions', count=elig))
    if exploit:
        src = full_ref(manifest.get('source_gto_dataset', ''))
        try:
            _, gto = quiz.load(src); orphans = [s for s in rows if s.get('base_spot_id') not in gto]
            checks.append(_check('source', 'Chaque spot exploitant renvoie à un spot du dataset GTO source', not orphans, f'source {src} ; {len(orphans)} orphelins'))
        except (OSError, ValueError):
            checks.append(_check('source', 'Dataset GTO source présent', False, f'{src} introuvable'))
        st = (statuses or {}).get(src)
        checks.append(_check('source_status', 'Dataset GTO source publié', st == 'published', f'{src} : {STATUS_FR.get(st, "non enregistré")}', blocking=False))
    ok, detail = _rebuild(ref, manifest, spots)
    checks.append(_check('rebuild', 'Test de référence : reconstruction depuis les sources', ok is True, detail, blocking=ok is not None))
    return _report(ref, checks, sha)


def _report(ref, checks, sha):
    blocking = [c for c in checks if c['blocking'] and not c['ok']]
    warnings = [c for c in checks if not c['ok'] and not c['blocking']]
    return dict(ref=ref, at=_now(), spots_sha256=sha, ok=not blocking, checks=checks,
                summary_fr=('Contrôles réussis' if not blocking else f'{len(blocking)} contrôle(s) bloquant(s) en échec')
                + (f', {len(warnings)} avertissement(s)' if warnings else ''))


# ------------------------------------------------------------------ registre (base de l'application)
class LifecycleError(Exception):
    pass


def sync(con):
    """enregistre en « staging » les versions présentes sur disque et pas encore connues"""
    con.executescript(SCHEMA)
    known = {r[0] for r in con.execute('SELECT ref FROM datasets')}
    for ref, m in folders():
        if ref not in known:
            con.execute('INSERT INTO datasets(ref, dataset, version, status, updated_at) VALUES (?, ?, ?, ?, ?)', (ref, m['dataset'], m['version'], 'staging', _now()))


def statuses(con):
    return {r[0]: r[1] for r in con.execute('SELECT ref, status FROM datasets')}


def active(con, dataset):
    """version publiée d'un dataset (ref complète) ou None"""
    r = con.execute("SELECT ref FROM datasets WHERE dataset = ? AND status = 'published'", (dataset,)).fetchone()
    return r[0] if r else None


def status_of(con, ref):
    r = con.execute('SELECT status FROM datasets WHERE ref = ?', (full_ref(ref),)).fetchone()
    return r[0] if r else None


def _row(con, ref):
    sync(con)
    r = con.execute('SELECT * FROM datasets WHERE ref = ?', (ref,)).fetchone()
    if r is None: raise LifecycleError(f'dataset inconnu : {ref}')
    return r


def run_validation(con, ref, actor):
    ref = full_ref(ref); r = _row(con, ref)
    if r['status'] == 'published': raise LifecycleError('version publiée : la retirer avant de la recontrôler')
    rep = validate(ref, statuses(con))
    status = 'validated' if rep['ok'] else 'rejected'
    if r['status'] in ('retired', 'disabled') and rep['ok']: status = r['status']        # le contrôle ne remet rien en ligne
    con.execute('UPDATE datasets SET status = ?, report = ?, spots_sha256 = ?, validated_at = ?, updated_at = ?, actor = ? WHERE ref = ?',
                (status, json.dumps(rep, ensure_ascii=False), rep['spots_sha256'], rep['at'], _now(), actor, ref))
    return rep, status


def publish(con, ref, actor, reason):
    ref = full_ref(ref); r = _row(con, ref)
    if r['status'] not in ('validated', 'retired', 'disabled'): raise LifecycleError(f"statut « {STATUS_FR[r['status']]} » : contrôler la version avant de la publier")
    if not r['report'] or not json.loads(r['report'])['ok']: raise LifecycleError('aucun rapport de contrôle réussi pour cette version')
    path = os.path.join(quiz.ref_path(ref), 'spots.jsonl')
    if not os.path.isfile(path): raise LifecycleError('fichiers du dataset absents de ce serveur')
    if _sha(path) != r['spots_sha256']: raise LifecycleError('fichiers modifiés depuis le contrôle : recontrôler')
    if r['dataset'] == 'exploit_calls':
        m = json.load(open(os.path.join(quiz.ref_path(ref), 'manifest.json')))
        if status_of(con, m['source_gto_dataset']) != 'published': raise LifecycleError(f"le dataset GTO source {full_ref(m['source_gto_dataset'])} n'est pas publié")
    prev = active(con, r['dataset'])
    if prev and prev != ref:
        con.execute("UPDATE datasets SET status = 'retired', updated_at = ?, actor = ?, reason = ? WHERE ref = ?", (_now(), actor, f'remplacé par {ref}', prev))
    con.execute("UPDATE datasets SET status = 'published', published_at = ?, updated_at = ?, actor = ?, reason = ? WHERE ref = ?", (_now(), _now(), actor, reason, ref))
    return prev


def disable(con, ref, actor, reason):
    ref = full_ref(ref); r = _row(con, ref)
    if r['status'] == 'disabled': raise LifecycleError('déjà retiré')
    con.execute("UPDATE datasets SET status = 'disabled', updated_at = ?, actor = ?, reason = ? WHERE ref = ?", (_now(), actor, reason, ref))
    dependants = []
    if r['dataset'] == 'gto_preflop':                       # un exploitant publié dont la source est retirée est retiré aussi
        for x in con.execute("SELECT ref FROM datasets WHERE dataset = 'exploit_calls' AND status = 'published'").fetchall():
            m = json.load(open(os.path.join(quiz.ref_path(x[0]), 'manifest.json')))
            if full_ref(m['source_gto_dataset']) == ref:
                con.execute("UPDATE datasets SET status = 'disabled', updated_at = ?, actor = ?, reason = ? WHERE ref = ?",
                            (_now(), actor, f'source {ref} retirée : {reason}', x[0])); dependants.append(x[0])
    return dependants


def listing(con):
    sync(con); out = []
    manifests = dict(folders())
    for r in con.execute("SELECT * FROM datasets ORDER BY dataset = 'exploit_calls', version DESC"):
        m = manifests.get(r['ref'], {}); rep = json.loads(r['report']) if r['report'] else None
        out.append(dict(ref=r['ref'], dataset=r['dataset'], version=r['version'], status=r['status'], status_fr=STATUS_FR[r['status']],
                        on_disk=r['ref'] in manifests, created_at=m.get('created_at'), spots=m.get('spots'), questions=m.get('questions_eligible'),
                        source=m.get('source_gto_dataset'), validated_at=r['validated_at'], published_at=r['published_at'], updated_at=r['updated_at'],
                        actor=r['actor'], reason=r['reason'], report_summary=rep['summary_fr'] if rep else None, report_ok=rep['ok'] if rep else None))
    return out


def report(con, ref):
    r = _row(con, full_ref(ref))
    return json.loads(r['report']) if r['report'] else None


if __name__ == '__main__':                                  # contrôle hors application : python -m spinsacademy.catalog <dataset/version>
    import sys
    rep = validate(sys.argv[1])
    for c in rep['checks']:
        print(f"{'OK ' if c['ok'] else ('ÉCHEC' if c['blocking'] else 'AVERT')}  {c['label_fr']} : {c['details_fr']}")
    print(rep['summary_fr']); sys.exit(0 if rep['ok'] else 1)
