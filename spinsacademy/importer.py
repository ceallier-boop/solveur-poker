"""Import des exports HRC vers un dataset de spots préflop versionné.

Un spot = un nœud de décision : état du jeu normalisé, actions légales, et, pour chacune des 169 classes de main,
la fréquence HRC, l'EV HRC, l'EV exacte quand elle est calculable, et le poids d'atteinte. Une question de quiz
est un couple (spot, main) tiré plus tard parmi les mains qui atteignent le nœud.

Règles :
  - seuls les exports de l'arbre préflop de référence sont importés ; quand plusieurs exports ont les mêmes
    stacks, le plus récent est retenu (ordre BASE_PREFERENCE) ;
  - EV de référence pour la correction : l'EV exacte quand chaque action autre que fold en a une (décision tout
    ou rien), sinon l'EV HRC ;
  - une main n'est proposée en question que si elle atteint le nœud (reach >= MIN_REACH) et si la stratégie HRC
    est cohérente avec l'EV de référence : EV(meilleure action) - somme(fréquence x EV) <= MAX_SELF_REGRET_MBB ;
  - un spot invalide (fréquences non normalisées, action illégale, mains manquantes) bloque la publication ;
  - une version publiée est immuable : on ne réécrit jamais un dossier existant.

Usage : python -m spinsacademy.importer --version 2026.10.12-1 [--out data/datasets/gto_preflop]
"""
import argparse, datetime, hashlib, json, os
import numpy as np
from . import allin
from .cards import NAMES, W
from .hrc import ROOT, exports, is_allin, labels, load, positions, preflop_hash, tree_hash

IMPORTER_VERSION = '1.1.0'
REF_PREFLOP = 'daa9aaa0'          # arbre préflop retenu (limp du BTN autorisé), voir data/hrc/README.md
MIN_REACH = 0.05                  # poids d'atteinte minimal pour qu'une main soit proposée en question
MAX_SELF_REGRET_MBB = 60.0        # incohérence maximale entre la stratégie HRC et l'EV de référence pour proposer la main
BLINDS = {3: [0.0, 0.5, 1.0], 2: [0.5, 1.0]}


class InvalidSpot(Exception):
    pass


def _sha256(path):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(path)):
        for f in sorted(files):
            p = os.path.join(root, f); h.update(os.path.relpath(p, path).encode()); h.update(open(p, 'rb').read())
    return h.hexdigest()


def _state(st, seq):
    """mises engagées, joueurs couchés et historique normalisé après la séquence"""
    n = len(st); names = positions(st); commit = list(BLINDS[n]); folded = [False] * n; hist = []
    for a in seq:
        p = a['player']; amt = a['amount'] / 10000
        if a['type'] == 'F':
            folded[p] = True; hist.append(dict(position=names[p], action='fold'))
        elif a['type'] == 'X':
            hist.append(dict(position=names[p], action='check'))
        elif a['type'] == 'C':
            commit[p] += amt
            last = next((h for h in reversed(hist) if h['action'] in ('raise', 'allin')), None)
            kind = 'limp' if last is None else ('call_allin' if last['action'] == 'allin' or commit[p] >= st[p] - 1e-9 else 'call')
            hist.append(dict(position=names[p], action=kind, to_bb=round(commit[p], 4)))
        elif a['type'] == 'R':
            commit[p] = amt
            hist.append(dict(position=names[p], action='allin' if is_allin(amt, st, seq[:len(hist)], p) else 'raise', to_bb=round(amt, 4)))
        else:
            raise InvalidSpot(f"type d'action inconnu : {a['type']}")
        if commit[p] > st[p] + 1e-9: raise InvalidSpot(f"{names[p]} engage {commit[p]:g} BB pour un stack de {st[p]:g}")
    return commit, folded, hist


def _actions(node, st, commit):
    p = node['player']; to_call = max(commit) - commit[p]; out = []
    seq = node['sequence']
    raises = [k for k, a in enumerate(seq) if a['type'] == 'R']
    facing_allin = bool(raises) and is_allin(seq[raises[-1]]['amount'] / 10000, st, seq[:raises[-1]], seq[raises[-1]]['player'])
    for a, lab in zip(node['actions'], labels(node, st)):
        amt = a['amount'] / 10000
        if a['type'] == 'F':
            if to_call <= 1e-9:
                out.append(None); continue                # fold gratuit de l'arbre HRC : retiré (vérifié à fréquence nulle)
            out.append(dict(id='F', type='fold'))
        elif a['type'] == 'X':
            if to_call > 1e-9: raise InvalidSpot('check proposé face à une mise')
            out.append(dict(id='X', type='check'))
        elif a['type'] == 'C':
            if abs(amt - min(to_call, st[p] - commit[p])) > 1e-6: raise InvalidSpot(f'montant du call incohérent ({amt:g} contre {to_call:g})')
            total = commit[p] + amt
            out.append(dict(id='C', type='call_allin' if facing_allin or total >= st[p] - 1e-9 else ('limp' if not raises else 'call'), to_bb=round(total, 4)))
        elif a['type'] == 'R':
            if amt > st[p] + 1e-9: raise InvalidSpot(f'relance à {amt:g} BB au-delà du stack ({st[p]:g})')
            if amt <= max(commit) + 1e-9: raise InvalidSpot(f'relance à {amt:g} BB inférieure à la mise en cours')
            out.append(dict(id=lab, type='allin' if lab == 'A' else 'raise', to_bb=round(amt, 4)))
    kept = [x for x in out if x is not None]
    if len({x['id'] for x in kept}) != len(kept): raise InvalidSpot('actions en double')
    return out, to_call


def _vec(node, ai, field='played'):
    return np.array([node['hands'][h][field][ai] for h in NAMES], float)


def _exact(st, nodes, key, labs):
    """EV exactes par action (None quand l'action n'a pas de calcul exact)"""
    n = len(st); ev = [None] * len(labs)
    if key in allin.CALL_NODES[n] and 'C' in labs:
        (skey, slab), (a, b), dead, blind = allin.CALL_NODES[n][key]
        sn = nodes.get(skey)
        if sn is not None and slab in labels(sn, st):
            q = _vec(sn, labels(sn, st).index(slab)) * _vec_weight(sn)
            if q.sum() > 0: ev[labs.index('C')] = allin.call_ev(q, min(st[a], st[b]), dead, blind)
    if key in allin.SHOVE_NODES[n] and 'A' in labs:
        ckey, (a, b), dead, mine, his = allin.SHOVE_NODES[n][key]
        cn = nodes.get(ckey)
        if cn is not None and 'C' in labels(cn, st):
            ev[labs.index('A')] = allin.shove_ev(_vec_weight(cn), _vec(cn, labels(cn, st).index('C')), min(st[a], st[b]), dead, mine, his)
    if 'F' in labs: ev[labs.index('F')] = np.zeros(169)
    return ev


def _vec_weight(node):
    return np.array([node['hands'][h]['weight'] for h in NAMES], float)


def build_spot(export_dir, st, nodes, key, settings, source_sha):
    node = nodes[key]; names = positions(st); labs = labels(node, st)
    if len(labs) < 2: return None
    if len(node['hands']) != 169 or set(node['hands']) != set(NAMES): raise InvalidSpot('169 classes attendues')
    commit, folded, hist = _state(st, node['sequence'])
    if folded[node['player']]: raise InvalidSpot('le joueur qui agit a déjà foldé')
    acts, to_call = _actions(node, st, commit)
    freq = np.array([node['hands'][h]['played'] for h in NAMES], float)
    if np.abs(freq.sum(1) - 1).max() > 2e-3: raise InvalidSpot('fréquences non normalisées')
    ev_hrc = np.array([node['hands'][h]['evs'] for h in NAMES], float)
    reach = _vec_weight(node)
    exact = _exact(st, nodes, key, labs)
    keep = [j for j, a in enumerate(acts) if a is not None]
    if len(keep) < len(acts):
        if freq[:, [j for j in range(len(acts)) if acts[j] is None]].max() > 1e-3: raise InvalidSpot('fold gratuit joué par HRC')
        acts = [acts[j] for j in keep]; labs = [labs[j] for j in keep]; exact = [exact[j] for j in keep]
        freq = freq[:, keep]; freq = freq / freq.sum(1, keepdims=True); ev_hrc = ev_hrc[:, keep]
    full_exact = all(e is not None for e in exact)
    ev_ref_source = 'exact' if full_exact else 'hrc'
    hero = node['player']
    hands = {}
    for i, h in enumerate(NAMES):
        ex = [None if e is None or np.isnan(e[i]) else round(float(e[i]), 5) for e in exact]
        if full_exact and any(x is None for x in ex): raise InvalidSpot(f'EV exacte manquante pour {h}')
        ref = np.array(ex if full_exact else ev_hrc[i], float)
        self_regret = round(1000 * float(ref.max() - (freq[i] * ref).sum()), 1); r = round(float(reach[i]), 4)
        hands[h] = dict(reach=r, freq=[round(float(x), 4) for x in freq[i]],
                        ev_hrc=[round(float(x), 5) for x in ev_hrc[i]], ev_exact=ex,
                        hrc_self_regret_mbb=self_regret,
                        quiz_eligible=bool(r >= MIN_REACH and self_regret <= MAX_SELF_REGRET_MBB))   # décidé sur les valeurs publiées
    table = '3-handed' if len(st) == 3 else 'heads-up'
    sid = hashlib.sha256(json.dumps([REF_PREFLOP, table, st, key]).encode()).hexdigest()[:12]
    mass = W * reach
    return dict(
        spot_id=f"{'3w' if len(st) == 3 else 'hu'}-{'-'.join(f'{x:g}' for x in st)}-{key}-{sid[:6]}",
        table=table, players=names, stacks_bb=st, blinds_bb=dict(sb=0.5, bb=1.0), ante_bb=0.0, model='chip_ev',
        hero=names[hero], node_key=key, history=hist,
        pot_bb=round(sum(commit), 4), to_call_bb=round(to_call, 4), hero_committed_bb=round(commit[hero], 4),
        effective_stack_bb=round(min(st[q] for q in range(len(st)) if not folded[q]), 4),
        actions=acts, ev_reference=ev_ref_source, ev_exact_approximate=bool(len(st) == 3 and allin.APPROXIMATE_3WAY and any(e is not None for e, l in zip(exact, labs) if l != 'F')),
        reach_share=round(float(mass.sum() / W.sum()), 4),
        eligible_hands=sum(1 for x in hands.values() if x['quiz_eligible']),
        hands=hands,
        provenance=dict(export=os.path.relpath(export_dir, ROOT), export_sha256=source_sha, hrc_tree=tree_hash(settings), hrc_preflop_tree=preflop_hash(settings),
                        postflop_mode=settings['treeconfig']['postflop']['id'].split('.')[-1], importer=IMPORTER_VERSION,
                        equity_matrix=os.path.basename(allin.EQUITY_FILE)))


def build_dataset(raw=None):
    spots, rejected, used, skipped = [], [], [], []
    seen = set()
    for d in (exports(raw) if raw else exports()):
        s, st, nodes = load(d)
        if preflop_hash(s) != REF_PREFLOP: skipped.append((d, 'arbre préflop différent')); continue
        if tuple(st) in seen: skipped.append((d, 'stacks déjà couverts par un export plus récent')); continue
        seen.add(tuple(st)); sha = _sha256(d); used.append(d)
        for key in sorted(nodes, key=lambda k: (k.count('_'), k)):
            try:
                sp = build_spot(d, st, nodes, key, s, sha)
                if sp: spots.append(sp)
            except InvalidSpot as e:
                rejected.append((d, key, str(e)))
    return spots, rejected, used, skipped


def publish(version, out, raw=None):
    target = os.path.join(out, version)
    if os.path.exists(target): raise SystemExit(f'{target} existe déjà : une version publiée est immuable, choisir un nouveau numéro')
    spots, rejected, used, skipped = build_dataset(raw)
    if rejected: raise SystemExit('Publication bloquée, spots invalides :\n' + '\n'.join(f'  {os.path.relpath(d, ROOT)} {k} : {m}' for d, k, m in rejected))
    os.makedirs(target)
    with open(os.path.join(target, 'spots.jsonl'), 'w') as f:
        for sp in spots: f.write(json.dumps(sp, ensure_ascii=False, separators=(',', ':')) + '\n')
    digest = hashlib.sha256(open(os.path.join(target, 'spots.jsonl'), 'rb').read()).hexdigest()
    manifest = dict(dataset='gto_preflop', version=version, created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                    importer=IMPORTER_VERSION, reference_preflop_tree=REF_PREFLOP, model='chip_ev', spots=len(spots), spots_sha256=digest,
                    ev_reference_rule="EV exacte si chaque action autre que fold en a une, sinon EV HRC", min_reach_for_questions=MIN_REACH, max_self_regret_mbb=MAX_SELF_REGRET_MBB,
                    questions_eligible=sum(sp['eligible_hands'] for sp in spots),
                    sources=[os.path.relpath(d, ROOT) for d in used], skipped=[dict(export=os.path.relpath(d, ROOT), reason=r) for d, r in skipped],
                    status='staging')
    json.dump(manifest, open(os.path.join(target, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    return manifest


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True); ap.add_argument('--out', default=os.path.join(ROOT, 'data', 'datasets', 'gto_preflop'))
    m = publish(**vars(ap.parse_args()))
    print(f"{m['spots']} spots publiés en staging : {m['version']} ({len(m['sources'])} exports, {len(m['skipped'])} écartés)")
