"""Rapports d'un dataset publié : import, validation, couverture, comparaison avec la référence, notation.

Usage : python -m spinsacademy.report --version 2026.10.12-2 [--out docs/dataset]
Le rapport relit uniquement les fichiers publiés (manifest.json, spots.jsonl) : il contrôle ce qui sera servi, pas ce que l'importeur croit avoir écrit.
"""
import argparse, collections, hashlib, json, os, random
import numpy as np
from . import grading
from .cards import NAMES, W
from .hrc import ROOT

DATASETS = os.path.join(ROOT, 'data', 'datasets', 'gto_preflop')


def situation(sp):
    """famille de décision lisible"""
    prior = [h for h in sp['history'] if h['action'] != 'fold']
    if not prior: return 'premier à parler'
    last = prior[-1]['action']
    if any(h['action'] == 'allin' for h in prior): return "face à un tapis"
    if any(h['action'] == 'raise' for h in prior): return 'face à une relance'
    return 'face à un limp' if last == 'limp' else 'autre'


def load(version):
    d = os.path.join(DATASETS, version)
    manifest = json.load(open(os.path.join(d, 'manifest.json')))
    raw = open(os.path.join(d, 'spots.jsonl'), 'rb').read()
    spots = [json.loads(l) for l in raw.decode().splitlines()]
    return manifest, spots, hashlib.sha256(raw).hexdigest()


def checks(spots):
    """contrôles rejoués sur le fichier publié ; renvoie [(contrôle, nombre d'échecs)]"""
    fails = collections.Counter()
    for sp in spots:
        hero = sp['players'].index(sp['hero']); stack = sp['stacks_bb'][hero]
        ids = [a['id'] for a in sp['actions']]
        fails['actions en double'] += len(ids) != len(set(ids))
        fails['fold proposé sans mise à payer'] += sp['to_call_bb'] == 0 and 'F' in ids
        fails['check proposé face à une mise'] += sp['to_call_bb'] > 0 and 'X' in ids
        fails['mise au-delà du stack'] += sum(1 for a in sp['actions'] if a.get('to_bb', 0) > stack + 1e-6)
        fails['classes manquantes'] += len(sp['hands']) != 169 or set(sp['hands']) != set(NAMES)
        for h in sp['hands'].values():
            fails['fréquences non normalisées'] += abs(sum(h['freq']) - 1) > 2e-3
            fails['longueurs incohérentes'] += not (len(h['freq']) == len(h['ev_hrc']) == len(h['ev_exact']) == len(ids))
            fails['EV exacte manquante sur un spot « exact »'] += sp['ev_reference'] == 'exact' and any(x is None for x in h['ev_exact'])
    return list(fails.items())


def fmt(x, d=0): return f'{x:,.{d}f}'.replace(',', ' ').replace('.', ',')


def build(version):
    m, spots, digest = load(version)
    L = [f'# Rapport du dataset `gto_preflop` {version}', '',
         f"Généré par `python -m spinsacademy.report --version {version}` à partir des fichiers publiés. Statut : **{m['status']}**. Importeur {m['importer']}.", '']

    # 1. import
    L += ['## 1. Import', '', f"- Exports retenus : **{len(m['sources'])}** ; écartés : **{len(m['skipped'])}**.",
          f"- Spots publiés : **{m['spots']}** ; questions proposables (couples spot × main) : **{fmt(m['questions_eligible'])}**.",
          f"- Empreinte de `spots.jsonl` : `{digest[:16]}…` ({'conforme' if digest == m['spots_sha256'] else '**DIFFÉRENTE du manifeste**'}).", '',
          '| Export écarté | Raison |', '|---|---|'] + [f"| `{s['export']}` | {s['reason']} |" for s in m['skipped']] + ['']
    per = collections.defaultdict(list)
    for sp in spots: per[sp['provenance']['export']].append(sp)
    L += ['| Export retenu | Table | Stacks (BB) | Postflop de référence | Spots | Questions |', '|---|---|---|---|---|---|']
    for e in m['sources']:
        ss = per[e]; s0 = ss[0]
        L.append(f"| `{e}` | {s0['table']} | {' / '.join(f'{x:g}' for x in s0['stacks_bb'])} | {s0['provenance']['postflop_mode']} | {len(ss)} | {fmt(sum(s['eligible_hands'] for s in ss))} |")
    L += ['', "Règle de sélection : arbre préflop `" + m['reference_preflop_tree'] + "` uniquement ; pour une même configuration de stacks, l'export le plus récent. "
          "Les doublons écartés ont le même arbre préflop ; la comparaison 12 / 12 / 12 (`data/hrc/README.md`) montre des fréquences identiques à 1 ou 2 points près.", '']

    # 2. validation
    ck = checks(spots)
    L += ['## 2. Validation', '', '| Contrôle (rejoué sur le fichier publié) | Échecs |', '|---|---|'] + [f'| {c} | {n} |' for c, n in ck]
    L += ['', "La publication est refusée au moindre spot invalide. Deux tests injectent volontairement une anomalie (`tests/test_importer.py` : "
          "fréquences non normalisées, relance au-delà du stack) et vérifient que rien n'est publié.", '']

    # 3. couverture
    rows = collections.defaultdict(lambda: [0, 0, 0])
    elig_cls = collections.Counter(); fam = collections.Counter(); pos = collections.Counter()
    for sp in spots:
        k = (sp['table'], ' / '.join(f'{x:g}' for x in sp['stacks_bb']))
        cand = sum(1 for h in sp['hands'].values() if h['reach'] >= m['min_reach_for_questions'])
        rows[k][0] += 1; rows[k][1] += cand; rows[k][2] += sp['eligible_hands']
        fam[(sp['table'], situation(sp))] += sp['eligible_hands']; pos[(sp['table'], sp['hero'])] += sp['eligible_hands']
        for h, v in sp['hands'].items(): elig_cls[h] += v['quiz_eligible']
    L += ['## 3. Couverture', '', f"Une main est proposable si elle atteint le nœud (poids ≥ {m['min_reach_for_questions']}) et si la stratégie de référence est cohérente avec l'EV de référence "
          f"(écart ≤ {fmt(m['max_self_regret_mbb'])} mBB). « Atteintes » compte les mains au-dessus du seuil de poids ; « proposables » retire les incohérentes.", '',
          '| Table | Stacks (BB) | Spots | Mains atteintes | Proposables | Retirées pour incohérence |', '|---|---|---|---|---|---|']
    for (t, st), (n, c, e) in sorted(rows.items(), key=lambda kv: (kv[0][0], [float(x) for x in kv[0][1].split(' / ')])):
        L.append(f'| {t} | {st} | {n} | {fmt(c)} | {fmt(e)} | {fmt(100 * (c - e) / max(c, 1), 1)} % |')
    L += ['', '| Table | Position du héros | Questions | | Table | Famille de décision | Questions |', '|---|---|---|---|---|---|---|']
    pl = sorted(pos.items()); fl = sorted(fam.items())
    for i in range(max(len(pl), len(fl))):
        a = pl[i] if i < len(pl) else (('', ''), ''); b = fl[i] if i < len(fl) else (('', ''), '')
        L.append(f"| {a[0][0]} | {a[0][1]} | {fmt(a[1]) if a[1] != '' else ''} | | {b[0][0]} | {b[0][1]} | {fmt(b[1]) if b[1] != '' else ''} |")
    low = sorted(elig_cls.items(), key=lambda kv: kv[1])[:10]
    L += ['', f"Les 169 classes sont proposables dans au moins {min(elig_cls.values())} spots. Les moins représentées : " + ', '.join(f'{h} ({n})' for h, n in low) + '.', '',
          "La couverture du catalogue de quiz (répartition réellement servie à l'utilisateur) dépendra du générateur de séries : à mesurer sur ses tirages.", '']

    # 4. comparaison de référence
    ex = [sp for sp in spots if sp['ev_reference'] == 'exact']
    dev = []; flips = 0; tot = 0
    for sp in ex:
        for h in NAMES:
            H = sp['hands'][h]
            if H['reach'] < m['min_reach_for_questions']: continue
            w = W[NAMES.index(h)] * H['reach']; e = np.array(H['ev_exact'], float); r = np.array(H['ev_hrc'], float)
            dev.append((w, float(np.abs(e - r).max()), sp['stacks_bb']))
            tot += 1; flips += int(np.argmax(H['freq']) != np.argmax(e) and 1000 * (e.max() - e[np.argmax(H['freq'])]) > 20)
    sr = [(W[NAMES.index(h)] * v['reach'], v['hrc_self_regret_mbb']) for sp in spots for h, v in sp['hands'].items() if v['reach'] >= m['min_reach_for_questions']]
    wts = np.array([a for a, _ in sr]); vals = np.array([b for _, b in sr]); order = np.argsort(vals); cum = np.cumsum(wts[order]) / wts.sum()
    q = lambda p: vals[order][np.searchsorted(cum, p)]
    L += ['## 4. Comparaison avec la référence', '',
          f"**Spots à EV exacte ({len(ex)})** : décisions tout ou rien. Écart moyen entre l'EV de référence et l'EV exacte : **{fmt(1000 * sum(w * d for w, d, _ in dev) / sum(w for w, _, _ in dev))} mBB**. "
          f"Dans {flips} cas sur {fmt(tot)} ({fmt(100 * flips / max(tot, 1), 1)} %), l'action majoritaire de la référence perd plus de 20 mBB selon l'EV exacte. La correction suit l'EV exacte.", '',
          "**Cohérence interne de la référence** (EV de la meilleure action moins EV de la stratégie de référence, sur l'EV de référence, mains atteintes, pondérées par combos) : "
          f"médiane {fmt(q(0.5), 1)} mBB, 90ᵉ centile {fmt(q(0.9), 1)} mBB, 99ᵉ centile {fmt(q(0.99), 1)} mBB. Au-delà de {fmt(m['max_self_regret_mbb'])} mBB, la main n'est pas proposée.", '',
          'Détail par export et par nœud : `docs/reference/VALIDATION_REFERENCE.md`.', '',
          "Limite : à 3 joueurs, l'EV exacte ne retire pas les cartes du joueur qui a foldé (`ev_exact_approximate`). Contrôle indépendant de la matrice d'équité : `spinsacademy/data/equity_169.json`.", '']

    # 5. notation
    dist = collections.Counter(); ex_by = collections.defaultdict(list); promoted = 0
    rnd = random.Random(7)
    for sp in spots:
        for h in NAMES:
            if not sp['hands'][h]['quiz_eligible']: continue
            for a in sp['actions']:
                g = grading.grade(sp, h, a['id']); dist[g['verdict']] += 1
                if g['verdict'] == 'correct' and g['regret_mbb'] > grading.TOLERANCE_MBB: promoted += 1
                ex_by[g['verdict']].append((sp, h, a['id'], g))
    n = sum(dist.values())
    L += ['## 5. Notation', '', f"Barème : correct ≤ {fmt(grading.TOLERANCE_MBB)} mBB de regret, ou ≤ {fmt(3 * grading.TOLERANCE_MBB)} mBB pour une action jouée au moins {fmt(100 * grading.MIXED_MIN)} % du temps par la référence "
          f"(spots à EV de référence) ; imprécision ≤ {fmt(3 * grading.TOLERANCE_MBB)} mBB ; erreur au-delà. Regret = EV de la meilleure action − EV de l'action choisie, toutes deux relatives au fold, en mBB, sur l'EV de référence du spot.", '',
          '| Verdict | Points | Réponses possibles (spot × main × action) | Part |', '|---|---|---|---|']
    for v in ('correct', 'imprécision', 'erreur'):
        L.append(f'| {v} | {fmt(grading.POINTS[v], 1)} | {fmt(dist[v])} | {fmt(100 * dist[v] / n, 1)} % |')
    L += ['', f"Dont {fmt(promoted)} réponses correctes grâce à la tolérance de stratégie mixte (regret entre {fmt(grading.TOLERANCE_MBB)} et {fmt(3 * grading.TOLERANCE_MBB)} mBB).", '',
          '### Exemples', '', '| Verdict | Spot | Main | Action | Regret | Fréquence de référence | Meilleure action | Source EV |', '|---|---|---|---|---|---|---|---|']
    for v in ('correct', 'imprécision', 'erreur'):
        pool = ex_by[v]
        picks = rnd.sample(pool, min(4, len(pool)))
        if v == 'correct':
            mixed = [x for x in pool if x[3]['regret_mbb'] > grading.TOLERANCE_MBB]
            picks = picks[:2] + rnd.sample(mixed, min(2, len(mixed)))
        for sp, h, a, g in picks:
            L.append(f"| {v} | `{sp['spot_id']}` | {h} | {a} | {fmt(g['regret_mbb'], 1)} mBB | {fmt(100 * g['chosen_frequency'])} % | {g['best_action']} | {g['ev_source']} |")
    L += ['', "Ces exemples sont tirés au hasard (graine fixe) ; ils sont à faire relire par l'expert poker, en particulier les cas « correct » obtenus par la tolérance mixte et les « imprécision ».", '']
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--version', required=True); ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'dataset'))
    a = ap.parse_args()
    path = os.path.join(a.out, f'RAPPORT_{a.version}.md'); open(path, 'w').write(build(a.version)); print(path)
