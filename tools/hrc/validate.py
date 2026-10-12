"""Validation des exports HRC : structure, arbre préflop, et contrôle des EV HRC sur les calls d'all-in.

Les calls d'all-in à deux joueurs (sans jeu postflop) ont une EV exacte connue à partir de la range de shove :
  EV(call) - EV(fold) = eq * (2 L + mort) - L + blind_payée,   L = stack effectif,
avec eq l'équité de la main contre la range de shove, effet de bloqueurs compris (combos disjoints).
L'écart entre cette valeur et l'EV exportée par HRC mesure le bruit Monte-Carlo de HRC sur ce nœud.

Usage : python tools/hrc/validate.py [--out docs/hrc/VALIDATION_HRC.md]
"""
import argparse, json, os
import numpy as np
from hrc_io import ROOT, NC, exports, labels, load, positions, preflop_hash, tree_hash

E = np.load(os.path.join(os.path.dirname(__file__), 'equity_169.npy'))   # équité classe contre classe (combos disjoints), Monte-Carlo 20 000 tirages


def _classes():
    ranks = '23456789TJQKA'; names = []; combos = []
    for row in range(13):
        for col in range(13):
            if row == col:
                r = 12 - row; names.append(ranks[r] * 2); combos.append([(r * 4 + a, r * 4 + b) for a in range(4) for b in range(a + 1, 4)])
            elif row < col:
                hi, lo = 12 - row, 12 - col; names.append(ranks[hi] + ranks[lo] + 's'); combos.append([(hi * 4 + s, lo * 4 + s) for s in range(4)])
            else:
                hi, lo = 12 - col, 12 - row; names.append(ranks[hi] + ranks[lo] + 'o'); combos.append([(hi * 4 + a, lo * 4 + b) for a in range(4) for b in range(4) if a != b])
    masks = [np.array([(1 << x) | (1 << y) for x, y in c], dtype=np.int64) for c in combos]
    D = np.array([[((mi[:, None] & mj[None, :]) == 0).sum() for mj in masks] for mi in masks], float)
    return names, D


NAMES, D = _classes()
W = np.array([NC(h) for h in NAMES], float)

# nœud du joueur qui paie -> (nœud et action du shove, joueurs impliqués, argent mort, blind déjà payée par celui qui paie)
ALLIN_CALLS = {
    2: [('SB-allin', ('root', 'A'), (0, 1), 0.0, 1.0)],
    3: [('BTN-fold_SB-allin', ('BTN-fold', 'A'), (1, 2), 0.0, 1.0),
        ('BTN-allin_SB-fold', ('root', 'A'), (0, 2), 0.5, 1.0)],
}


def check_allin_calls(st, nodes):
    out = []
    for key, (skey, slab), (a, b), dead, blind in ALLIN_CALLS[len(st)]:
        if key not in nodes or skey not in nodes: continue
        sn = nodes[skey]; sl = labels(sn, st)
        if slab not in sl: continue
        q = np.array([sn['hands'][h]['played'][sl.index(slab)] * sn['hands'][h]['weight'] for h in NAMES])
        if q.sum() <= 0: continue
        L = min(st[a], st[b])
        J = D * q[None, :]; eq = (J * E).sum(1) / J.sum(1)
        exact = eq * (2 * L + dead) - L + blind
        n = nodes[key]; nl = labels(n, st)
        if 'C' not in nl: continue
        jc = nl.index('C')
        hrc = np.array([n['hands'][h]['evs'][jc] for h in NAMES]); played = np.array([n['hands'][h]['played'][jc] for h in NAMES])
        w = W * np.array([n['hands'][h]['weight'] for h in NAMES])
        d = hrc - exact
        wrong = ((exact > 0.02) & (played < 0.5)) | ((exact < -0.02) & (played > 0.5))
        out.append(dict(node=key, mean_abs_mbb=1000 * float(np.average(np.abs(d), weights=w)), max_abs_mbb=1000 * float(np.abs(d).max()),
                        bias_mbb=1000 * float(np.average(d, weights=w)), wrong=[NAMES[i] for i in np.where(wrong)[0]],
                        shove_pct=100 * float((W * q).sum() / W.sum())))
    return out


def validate(d):
    s, st, nodes = load(d)
    issues = []
    for k, n in nodes.items():
        for h, v in n['hands'].items():
            if abs(sum(v['played']) - 1) > 2e-3: issues.append(f'{k}/{h} : fréquences non normalisées')
            if len(v['played']) != len(n['actions']) or len(v['evs']) != len(n['actions']): issues.append(f'{k}/{h} : longueur incohérente')
        if len(n['hands']) != 169: issues.append(f'{k} : {len(n["hands"])} classes au lieu de 169')
    if 'root' not in nodes: issues.append('nœud racine absent')
    depth = max(len(n['sequence']) for n in nodes.values())
    open_raises = sum(1 for n in nodes.values() for a in n['actions'] if a['type'] == 'R' and a.get('node') is None and a['amount'] / 10000 < st[n['player']] - 1e-9)
    return dict(path=os.path.relpath(d, ROOT), stacks=st, preflop=preflop_hash(s), tree=tree_hash(s), postflop=s['treeconfig']['postflop']['id'].split('.')[-1],
                eqmodel=s['eqmodel']['id'], nodes=len(nodes), depth=depth, open_raises=open_raises, issues=issues, allin=check_allin_calls(st, nodes))


def report(results):
    L = ['# Validation des exports HRC', '', 'Généré par `python tools/hrc/validate.py`. Ne pas modifier à la main.', '',
         '## Structure', '', '| Export | Stacks (BB) | Arbre préflop | Postflop | Nœuds | Profondeur | Raises sans nœud fils | Anomalies |', '|---|---|---|---|---|---|---|---|']
    for r in results:
        L.append(f"| `{r['path']}` | {' / '.join(f'{x:g}' for x in r['stacks'])} | `{r['preflop']}` | {r['postflop']} | {r['nodes']} | {r['depth']} | {r['open_raises']} | {len(r['issues']) or '—'} |")
    L += ['', '« Profondeur » : nombre maximal d\'actions avant un nœud exporté. « Raises sans nœud fils » : relances non all-in dont la suite n\'est pas exportée.', '',
          '## EV HRC contre EV exacte sur les calls d\'all-in', '',
          'Écart entre l\'EV du call exportée par HRC et l\'EV exacte (chip EV, bloqueurs compris) calculée à partir de la range de shove exportée. '
          'Une « décision fausse » est une main où HRC joue majoritairement l\'action dont l\'EV exacte est inférieure de plus de 20 mBB.', '',
          'Heads-up : le calcul est exact. À 3 joueurs, il ignore les cartes du joueur qui a foldé : le biais négatif de quelques dizaines de mBB '
          'vient en partie de cette approximation, et les « décisions fausses » proches du seuil sont à confirmer.', '',
          '| Export | Stacks | Nœud | Shove adverse | Écart moyen | Écart max | Biais | Décisions fausses |', '|---|---|---|---|---|---|---|---|']
    for r in results:
        for a in r['allin']:
            L.append(f"| `{r['path']}` | {' / '.join(f'{x:g}' for x in r['stacks'])} | {a['node']} | {a['shove_pct']:.0f} % | {a['mean_abs_mbb']:.0f} mBB | {a['max_abs_mbb']:.0f} mBB | {a['bias_mbb']:+.0f} mBB | {', '.join(a['wrong']) or '—'} |")
    bad = [(r['path'], i) for r in results for i in r['issues']]
    if bad:
        L += ['', '## Anomalies', ''] + [f'- `{p}` : {i}' for p, i in bad]
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'hrc', 'VALIDATION_HRC.md'))
    res = [validate(d) for d in exports()]
    open(ap.parse_args().out, 'w').write(report(res))
    print(len(res), 'exports validés ;', sum(len(r['issues']) for r in res), 'anomalie(s)')
