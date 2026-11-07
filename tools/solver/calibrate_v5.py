"""Calage d'un résultat du solveur sur les exports de référence v5 (G19, 07/11/2026) : nœud par nœud, avec le bruit de la référence.

Usage : python tools/solver/calibrate_v5.py data/solver/runs/sf3dc2e6_48fa0906 hu_12-12 [--families]
Pour chaque nœud : fréquences globales de la référence et du solveur, distance de variation totale, accord des actions dominantes, perte du
solveur mesurée avec les EV de la référence (et plancher : regret de la référence elle-même). Avec --export : les 5 répétitions séparées,
pour mesurer l'écart entre deux calculs de la référence.
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc  # noqa: E402
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.solver import calibration, dataset as ds  # noqa: E402


def ours_of(res):
    st = [float(x) for x in res['stacks']]
    return {k: dict(actions=hrc.labels(n, st), freq=np.array([n['hands'][h]['played'] for h in NAMES])) for k, n in res['nodes'].items()}, st


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('config'); ap.add_argument('--repeats', action='store_true'); ap.add_argument('--families', action='store_true')
    a = ap.parse_args()
    res = json.load(open(os.path.join(a.run_dir, a.config + '.json'))); ours, st = ours_of(res)
    ref = ds.reference_nodes(ds.REFERENCE_PREFLOP.get(res['tree'], res['tree']), res['stacks'])
    print(f"{a.config} : {len(ref['exports'])} exports de référence moyennés ({', '.join(os.path.basename(e) for e in ref['exports'])})")
    rows = calibration.compare(ours, st, ref['nodes']); s = calibration.summary(rows)
    print(f"résumé : {s['nodes']} nœuds, TV {s['tv']} %, accord {s['agree']} %, perte {s['loss_mbb']} mBB (plancher de la référence {s['floor_mbb']}), hors référence {s['outside']} %")
    for r in sorted(rows, key=lambda r: -r['share']):
        print(f"  {r['node']:<28} part {100 * r['share']:5.1f} % ; réf {r['hrc']} / solveur {r['ours']} ; TV {r['tv']:4.1f} % ; accord {r['agree']:5.1f} % ; perte {r['loss']:6.1f} (plancher {r['floor']:5.1f}) mBB")
    if a.families:
        from spinsacademy.solver.correction import FAMILY
        print('perte du solveur mesurée avec les EV de la référence, par famille de mains (mBB, pondérée par la masse atteinte) : solveur (plancher de la référence)')
        for key in ('root', 'SB-raise2', 'SB-call', 'SB-call_BB-raise3'):
            n = ref['nodes'][key]; hl = hrc.labels(n, st); o = ours[key]
            P = np.array([n['hands'][h]['played'] for h in NAMES]); EV = np.array([n['hands'][h]['evs'] for h in NAMES]); w = W * np.array([n['hands'][h]['weight'] for h in NAMES])
            M = np.zeros_like(P)
            for j, act in enumerate(o['actions']):
                if act in hl: M[:, hl.index(act)] += o['freq'][:, j]
            M = M / np.maximum(M.sum(1, keepdims=True), 1e-12); loss = 1000 * (EV.max(1) - (M * EV).sum(1)); floor = 1000 * (EV.max(1) - (P * EV).sum(1))
            line = []
            for f in sorted(set(FAMILY)):
                ix = [i for i in range(169) if FAMILY[i] == f and w[i] > 0]
                if ix and w[ix].sum() > 0.03 * w.sum(): line.append(f'{f} {np.average(loss[ix], weights=w[ix]):.0f} ({np.average(floor[ix], weights=w[ix]):.0f})')
            print(f'  {key:<20}: ' + ' ; '.join(line))
    if a.repeats and len(ref['exports']) > 1:
        print('solveur contre chaque répétition de la référence prise seule (TV, accord, perte) :')
        for e in ref['exports']:
            sx, stx, nodes = hrc.load(os.path.join(ds.hrc.ROOT, e))
            rr = calibration.summary(calibration.compare(ours, stx, nodes)); print(f"  {os.path.basename(e)} : TV {rr['tv']} %, accord {rr['agree']} %, perte {rr['loss_mbb']} mBB (plancher {rr['floor_mbb']})")


if __name__ == '__main__':
    main()
