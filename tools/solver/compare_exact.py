"""Solveur contre un export « enumerated » (exact) : nœud par nœud, stratégie (TV, accord, perte) et EV relatives au fold (biais, écart quadratique).

Usage : python tools/solver/compare_exact.py data/solver/runs/sf3dc2e6_48fa0906 hu_6-6 data/hrc/raw/v5/hu_6-6_enum
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc  # noqa: E402
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.solver import calibration  # noqa: E402
from spinsacademy.solver.tree import Tree, TreeConfig  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('config'); ap.add_argument('export'); a = ap.parse_args()
    res = json.load(open(os.path.join(a.run_dir, a.config + '.json'))); st = [float(x) for x in res['stacks']]
    s, st_e, en = hrc.load(a.export); assert [float(x) for x in st_e] == st
    rel = ds.reliability_of(Tree(tuple(st), TreeConfig(**res['tree_config'])))
    ours = {k: dict(actions=hrc.labels(n, st), freq=np.array([n['hands'][h]['played'] for h in NAMES])) for k, n in res['nodes'].items()}
    rows = calibration.compare(ours, st, en); print(f"{a.config} contre {os.path.basename(a.export)} : nœuds exact {len(en)}, solveur {len(res['nodes'])}, comparés {len(rows)}")
    print('nœuds absents de l\'exact :', sorted(set(res['nodes']) - set(en)))
    for r in sorted(rows, key=lambda r: -r['share']):
        n = en[r['node']]; w = W * np.array([n['hands'][h]['weight'] for h in NAMES]); X = res['nodes'][r['node']]
        hl = hrc.labels(n, st); idx = [hl.index(x) for x in ours[r['node']]['actions'] if x in hl]
        E = np.array([n['hands'][h]['evs'] for h in NAMES]); Y = np.array([X['hands'][h]['evs'] for h in NAMES])
        fold = 0 if hl[0] == 'F' else None
        if fold is None or len(idx) != Y.shape[1]: ev = ''
        else:
            d = 1000 * ((Y - Y[:, [0]]) - (E[:, idx] - E[:, [idx[0]]])); ev = f"; EV/fold biais {np.round(np.average(d[:, 1:], axis=0, weights=w)).astype(int).tolist()} écart {np.round(np.sqrt(np.average(d[:, 1:] ** 2, axis=0, weights=w))).astype(int).tolist()}"
        print(f"  {r['node']:<30} {rel[r['node']]['reliability']:<5} part {100 * r['share']:5.1f} % ; exact {r['hrc']} / solveur {r['ours']} ; TV {r['tv']:4.1f} % ; accord {r['agree']:5.1f} % ; perte {r['loss']:6.1f} (plancher {r['floor']:5.1f}) {ev}")
    s2 = calibration.summary(rows); print('résumé', s2)
    for k in ('tapis', 'flop'):
        sub = [r for r in rows if rel[r['node']]['reliability'] == k]
        if sub: w = np.array([r['share'] for r in sub]); f = lambda key: round(float(np.dot(w, [r[key] for r in sub]) / w.sum()), 1); print(f"  décisions {k} : {len(sub)} nœuds, TV {f('tv')} %, accord {f('agree')} %, perte {f('loss')} (plancher {f('floor')})")


if __name__ == '__main__':
    main()
