"""Validation des exports de référence : structure, arbre préflop, et contrôle des EV de référence sur les calls d'all-in.

Les calls d'all-in à deux joueurs (sans jeu postflop) ont une EV exacte connue à partir de la range de shove :
  EV(call) - EV(fold) = eq * (2 L + mort) - L + blind_payée,   L = stack effectif,
avec eq l'équité de la main contre la range de shove, effet de bloqueurs compris (combos disjoints).
L'écart entre cette valeur et l'EV exportée par la référence mesure le bruit Monte-Carlo de la référence sur ce nœud.

Usage : python tools/hrc/validate.py [--out docs/reference/VALIDATION_REFERENCE.md]
"""
import argparse, json, os
import numpy as np
from hrc_io import ROOT, exports, labels, load, preflop_hash, tree_hash

from spinsacademy import allin
from spinsacademy.cards import NAMES, W


def check_allin_calls(st, nodes):
    out = []
    for key, ((skey, slab), (a, b), dead, blind) in allin.CALL_NODES[len(st)].items():
        if key not in nodes or skey not in nodes: continue
        sn = nodes[skey]; sl = labels(sn, st)
        if slab not in sl: continue
        q = np.array([sn['hands'][h]['played'][sl.index(slab)] * sn['hands'][h]['weight'] for h in NAMES])
        if q.sum() <= 0: continue
        exact = allin.call_ev(q, min(st[a], st[b]), dead, blind)
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
    L = ['# Validation des exports de référence', '', 'Généré par `python tools/hrc/validate.py`. Ne pas modifier à la main.', '',
         '## Structure', '', '| Export | Stacks (BB) | Arbre préflop | Postflop | Nœuds | Profondeur | Raises sans nœud fils | Anomalies |', '|---|---|---|---|---|---|---|---|']
    for r in results:
        L.append(f"| `{r['path']}` | {' / '.join(f'{x:g}' for x in r['stacks'])} | `{r['preflop']}` | {r['postflop']} | {r['nodes']} | {r['depth']} | {r['open_raises']} | {len(r['issues']) or '—'} |")
    L += ['', '« Profondeur » : nombre maximal d\'actions avant un nœud exporté. « Raises sans nœud fils » : relances non all-in dont la suite n\'est pas exportée.', '',
          '## EV de référence contre EV exacte sur les calls d\'all-in', '',
          'Écart entre l\'EV du call exportée par la référence et l\'EV exacte (chip EV, bloqueurs compris) calculée à partir de la range de shove exportée. '
          'Une « décision fausse » est une main où la référence joue majoritairement l\'action dont l\'EV exacte est inférieure de plus de 20 mBB.', '',
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
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'reference', 'VALIDATION_REFERENCE.md'))
    res = [validate(d) for d in exports()]
    open(ap.parse_args().out, 'w').write(report(res))
    print(len(res), 'exports validés ;', sum(len(r['issues']) for r in res), 'anomalie(s)')
