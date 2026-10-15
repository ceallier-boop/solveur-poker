"""Fusion des relectures expertes (grilles reponses_modele.csv remplies par chaque expert).

Usage : python tools/audit/expert_merge.py <dossier de l'échantillon> expert_A.csv expert_B.csv expert_C.csv [-o RAPPORT.md]
(les grilles d'un même expert remplies par lots peuvent être concaténées, ou passées avec le préfixe expert_A: devant chaque fichier)

Rapport :
  - accord entre experts sur chaque critère (part des questions où tous répondent pareil, kappa de Fleiss sur la référence) ;
  - décision par question : « à corriger » si la majorité conteste la référence ou juge la question bloquante,
    « à arbitrer » si un seul expert la conteste, « validée » sinon ;
  - taux de validation par strate (mode, format, situation, profondeur, source de l'EV, type de cas), pour savoir où
    l'application est fiable ;
  - liste des questions à corriger et à arbitrer, avec les commentaires.
Les réponses manquantes ou hors des valeurs prévues sont signalées, pas devinées.
"""
import argparse, collections, csv, json, os

VALUES = {'reference_ok': {'oui', 'non', 'incertain'}, 'verdicts_ok': {'oui', 'non'}, 'correction_ok': {'oui', 'non'},
          'regle_ok': {'oui', 'non', 'sans objet'}, 'gravite': {'bloquant', 'majeur', 'mineur', 'aucun'}}
STRATA = (('Mode', 'mode'), ('Format', 'format'), ('Situation', 'situation'), ('Position', 'position'), ('Source de l\'EV', 'source_ev'),
          ('Type de cas', 'type_de_cas'))


def norm(x): return (x or '').strip().lower()


def read(path):
    with open(path, encoding='utf-8-sig') as f:
        return {r['id']: {k: (v or '').strip() for k, v in r.items()} for r in csv.DictReader(f, delimiter=';')}


def fleiss(rows, cats):
    """kappa de Fleiss : rows = liste de Counter (réponses par catégorie), même nombre de juges par ligne"""
    rows = [r for r in rows if sum(r.values()) >= 2]
    if not rows: return None
    n = sum(rows[0].values()); N = len(rows)
    p = {c: sum(r[c] for r in rows) / (N * n) for c in cats}
    P = sum((sum(v * v for v in r.values()) - n) / (n * (n - 1)) for r in rows) / N; Pe = sum(v * v for v in p.values())
    return None if Pe >= 1 else (P - Pe) / (1 - Pe)


def decide(ans):
    ref = [norm(a['reference_ok']) for a in ans]; grav = [norm(a['gravite']) for a in ans]
    against = ref.count('non'); k = len(ans)
    if against * 2 > k or grav.count('bloquant') * 2 > k: return 'à corriger'
    if against or 'bloquant' in grav or grav.count('majeur') * 2 > k: return 'à arbitrer'
    return 'validée'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('sample'); ap.add_argument('files', nargs='+'); ap.add_argument('-o', default=None)
    a = ap.parse_args()
    qs = {q['id']: q for q in map(json.loads, open(os.path.join(a.sample, 'questions.jsonl')))}
    merged = collections.OrderedDict()
    for f in a.files:                                   # « expert_A:lot1.csv » : plusieurs fichiers pour un même expert
        name, path = f.split(':', 1) if ':' in f and not os.path.exists(f) else (os.path.splitext(os.path.basename(f))[0], f)
        merged.setdefault(name, {}).update(read(path))
    experts = list(merged.items())
    problems = []
    for name, rows in experts:
        for qid in qs:
            r = rows.get(qid)
            if r is None: problems.append(f'{name} : {qid} sans réponse'); continue
            for col, ok in VALUES.items():
                if norm(r.get(col)) not in ok: problems.append(f"{name} : {qid}, {col} = « {r.get(col, '')} » (attendu : {' / '.join(sorted(ok))})")
    full = [qid for qid in qs if all(qid in rows for _, rows in experts)]
    per = {qid: [rows[qid] for _, rows in experts] for qid in full}
    dec = {qid: decide(ans) for qid, ans in per.items()}
    out = [f"# Relecture experte : synthèse ({len(experts)} experts, {len(full)} questions sur {len(qs)} relues par tous)", '']
    out += ['## Accord entre experts', '', '| Critère | Tous d\'accord |', '|---|---|']
    for col in VALUES:
        same = sum(1 for ans in per.values() if len({norm(x[col]) for x in ans}) == 1)
        out.append(f"| {col} | {round(100 * same / len(per)) if per else 0} % |")
    kap = fleiss([collections.Counter(norm(x['reference_ok']) for x in ans) for ans in per.values()], VALUES['reference_ok'])
    out += ['', f"Kappa de Fleiss sur la référence : {'non calculable' if kap is None else f'{kap:.2f}'.replace('.', ',')} "
            "(au-delà de 0,6 : accord solide ; sous 0,4 : consignes à préciser avant d'exploiter les résultats).", '']
    c = collections.Counter(dec.values())
    out += ['## Décision par question', '', f"Validées {c['validée']}, à arbitrer {c['à arbitrer']}, à corriger {c['à corriger']}.", '']
    out += ['## Validation par strate', '', '| Strate | Valeur | Questions | Validées | À corriger |', '|---|---|---|---|---|']
    for title, key in STRATA:
        groups = collections.defaultdict(list)
        for qid in full: groups[qs[qid][key]].append(dec[qid])
        for val, ds in sorted(groups.items()):
            out.append(f"| {title} | {val} | {len(ds)} | {round(100 * ds.count('validée') / len(ds))} % | {ds.count('à corriger')} |")
    for label in ('à corriger', 'à arbitrer'):
        ids = [qid for qid in full if dec[qid] == label]
        out += ['', f"## Questions {label} ({len(ids)})", '']
        for qid in ids:
            q = qs[qid]
            out.append(f"### {qid} · {q['mode']} · {q['format']} · {q['position']} {q['situation']} · {q['tapis_effectif_bb']} BB · {q['main']} (référence : {q['reference']})")
            for (name, _), x in zip(experts, per[qid]):
                extra = ' ; '.join(t for t in (f"attendu : {x['action_attendue']}" if x.get('action_attendue') else '',
                                              f"verdict : {x['verdict_conteste']}" if x.get('verdict_conteste') else '') if t)
                out.append(f"- {name} : référence {x['reference_ok'] or '?'}, gravité {x['gravite'] or '?'}"
                           + (f" ({extra})" if extra else '') + (f" : {x['commentaire']}" if x.get('commentaire') else ''))
            out.append('')
    if problems: out += ['', f'## Réponses à reprendre ({len(problems)})', ''] + [f'- {p}' for p in problems[:200]]
    text = '\n'.join(out) + '\n'
    if a.o: open(a.o, 'w').write(text)
    print(text if not a.o else f"rapport : {a.o} ({c['validée']} validées, {c['à arbitrer']} à arbitrer, {c['à corriger']} à corriger)")


if __name__ == '__main__':
    main()
