"""Courbe de calage du solveur sur la référence v5, profondeur par profondeur (G19, 08/11/2026).

Pour chaque configuration à tapis égaux : nombre d'exports moyennés, nœuds comparés, TV, accord, perte du solveur (EV de la référence) et plancher
(regret de la référence elle-même), séparés selon le type de décision du champ `reliability` (tapis ou flop). Avec au moins deux répétitions : bruit de
la référence (TV et perte d'un export contre la moyenne des autres).

Usage : python tools/solver/calibration_curve.py data/solver/runs/sf3dc2e6_48fa0906 [--out fichier.json]
"""
import argparse, glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc  # noqa: E402
from spinsacademy.cards import NAMES  # noqa: E402
from spinsacademy.solver import calibration, dataset as ds  # noqa: E402
from spinsacademy.solver.tree import Tree, TreeConfig  # noqa: E402


def agg(rows):
    if not rows: return None
    w = np.array([r['share'] for r in rows]); a = lambda k: round(float(np.dot(w, [r[k] for r in rows]) / w.sum()), 1)
    return dict(nodes=len(rows), tv=a('tv'), agree=a('agree'), loss=a('loss'), floor=a('floor'))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run_dir'); ap.add_argument('--out'); a = ap.parse_args()
    out = []
    for p in sorted(glob.glob(os.path.join(a.run_dir, '*.json')), key=lambda p: (len(json.load(open(p))['stacks']), json.load(open(p))['stacks'][0])):
        res = json.load(open(p)); st = [float(x) for x in res['stacks']]
        if len(set(st)) != 1: continue
        ref = ds.reference_nodes(ds.REFERENCE_PREFLOP[res['tree']], st)
        if ref is None: continue
        rel = ds.reliability_of(Tree(tuple(st), TreeConfig(**res['tree_config'])))
        ours = {k: dict(actions=hrc.labels(n, st), freq=np.array([n['hands'][h]['played'] for h in NAMES])) for k, n in res['nodes'].items()}
        rows = calibration.compare(ours, st, ref['nodes'])
        tapis = [r for r in rows if rel[r['node']]['reliability'] == 'tapis']; flop = [r for r in rows if rel[r['node']]['reliability'] == 'flop']
        row = dict(config=os.path.basename(p)[:-5], exports=len(ref['exports']), outside=round(float(np.average([r['outside'] for r in rows], weights=[r['share'] for r in rows])), 1),
                   all=agg(rows), tapis=agg(tapis), flop=agg(flop))
        if len(ref['exports']) > 1:                                   # bruit de la référence : un export contre la moyenne des autres
            tvs, losses = [], []
            for i, e in enumerate(ref['exports']):
                others = [x for j, x in enumerate(ref['exports']) if j != i]
                loaded = [hrc.load(os.path.join(hrc.ROOT, x)) for x in others]
                mean = hrc.average([(loaded[0][0], l[1], l[2]) for l in loaded]) if len(loaded) > 1 else loaded[0][2]
                one = hrc.load(os.path.join(hrc.ROOT, e)); strat = {k: dict(actions=hrc.labels(n, st), freq=np.array([n['hands'][h]['played'] for h in NAMES])) for k, n in one[2].items()}
                s = calibration.summary(calibration.compare(strat, st, mean)); tvs.append(s['tv']); losses.append(s['loss_mbb'])
            row['noise'] = dict(tv=round(float(np.mean(tvs)), 1), loss=round(float(np.mean(losses)), 1))
        out.append(row)
        f = lambda d: '—' if d is None else f"TV {d['tv']:4.1f} accord {d['agree']:5.1f} perte {d['loss']:6.1f} (plancher {d['floor']:5.1f})"
        print(f"{row['config']:<12} {row['exports']} exp. {row['all']['nodes']:>2} nœuds ; tout : {f(row['all'])} ; tapis : {f(row['tapis'])} ; flop : {f(row['flop'])} ; hors {row['outside']}"
              + (f" ; bruit TV {row['noise']['tv']}, perte {row['noise']['loss']}" if 'noise' in row else ''), flush=True)
    if a.out: json.dump(out, open(a.out, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
