"""Compare le solveur maison à HRC (référence de contrôle interne uniquement : HRC n'entre jamais dans le calcul).

Pour chaque nœud exporté par HRC qui existe dans l'arbre maison :
  - TV : distance de variation totale moyenne entre les deux stratégies (0 = identiques, 100 % = disjointes) ;
  - accord : part des mains (pondérées par combos et atteinte HRC) où l'action dominante est la même ;
  - perte : regret de la stratégie maison mesuré avec les EV de HRC, moins le regret de HRC lui-même (bruit de référence) ;
  - hors HRC : part de la stratégie maison sur des actions absentes de l'arbre HRC (non évaluable).
Usage : python tools/solver/benchmark_hrc.py --stacks 10,10 [--iters 1500] [--postflop showdown]
"""
import argparse, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy.cards import NAMES, W
from spinsacademy.hrc import exports, labels, load, preflop_hash
from spinsacademy.solver import postflop as pf
from spinsacademy.solver.cfr import Solver

REF = 'daa9aaa0'
OUTER, POST_ITERS, BUCKETS, DAMP, UNOPENED, ROLLOUTS = 3, 3000, 16, 0.5, 0.0, 6


def find_export(stacks):
    for d in exports():
        s, st, nodes = load(d)
        if preflop_hash(s) == REF and [float(x) for x in st] == [float(x) for x in stacks]: return d, st, nodes
    return None


def compare(strategy, st, nodes):
    rows = []
    for key, n in nodes.items():
        if key not in strategy: continue
        hl = labels(n, st); ours = strategy[key]
        P = np.array([n['hands'][h]['played'] for h in NAMES]); EV = np.array([n['hands'][h]['evs'] for h in NAMES])
        w = W * np.array([n['hands'][h]['weight'] for h in NAMES])
        if w.sum() <= 0: continue
        M = np.zeros_like(P); outside = np.zeros(169)
        for j, a in enumerate(ours['actions']):
            if a in hl: M[:, hl.index(a)] += ours['freq'][:, j]
            else: outside += ours['freq'][:, j]
        Mn = M / np.maximum(M.sum(1, keepdims=True), 1e-12)
        tv = 0.5 * np.abs(Mn - P).sum(1)
        agree = Mn.argmax(1) == P.argmax(1)
        best = EV.max(1); loss = best - (Mn * EV).sum(1); floor = best - (P * EV).sum(1)
        avg = lambda x: float((w * x).sum() / w.sum())
        glob = lambda F: [round(100 * float((w * F[:, j]).sum() / w.sum()), 1) for j in range(F.shape[1])]
        rows.append(dict(node=key, actions=hl, hrc=glob(P), ours=glob(Mn), tv=100 * avg(tv), agree=100 * avg(agree),
                         loss=1000 * avg(loss), floor=1000 * avg(floor), outside=100 * avg(outside), share=float(w.sum() / W.sum())))
    return rows


def run(stacks, iters, model):
    found = find_export(stacks)
    if not found: raise SystemExit(f'aucun export HRC de référence pour {stacks}')
    d, st, nodes = found
    t0 = time.time()
    from spinsacademy.solver.tree import TreeConfig
    tcfg = TreeConfig(unopened_allin_max=UNOPENED)
    if model == 'showdown':
        s = Solver(st, tcfg, postflop=pf.Showdown()).solve(iters)
    else:
        from spinsacademy.solver.pipeline import solve
        from spinsacademy.postflop.hu_solver import PostflopConfig
        s, _, _ = solve(st, tcfg, pre_iters=iters, outer=OUTER, post_iters=POST_ITERS, pf_cfg=PostflopConfig(buckets=BUCKETS, rollouts=ROLLOUTS), damping=DAMP)
    dt = time.time() - t0
    rows = compare(s.strategy(), st, nodes)
    return dict(export=d, stacks=st, iters=iters, seconds=dt, expl=s.exploitability(), rows=rows, model=model)


def show(res):
    print(f"== {' / '.join(f'{x:g}' for x in res['stacks'])} BB ({os.path.relpath(res['export'])}) ; modèle {res['model']} ; {res['iters']} itérations en {res['seconds']:.0f} s ; "
          f"exploitabilité {', '.join(f'{1000 * e:.1f}' for e in res['expl'])} mBB/main")
    for r in sorted(res['rows'], key=lambda r: (r['node'].count('_'), r['node'])):
        print(f"  {r['node']:28s} {' '.join(r['actions']):18s} HRC {r['hrc']}  maison {r['ours']}  TV {r['tv']:4.1f} %  accord {r['agree']:5.1f} %  "
              f"perte {r['loss']:6.1f} (HRC {r['floor']:5.1f}) mBB  hors HRC {r['outside']:4.1f} %")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--stacks', required=True); ap.add_argument('--iters', type=int, default=1500)
    ap.add_argument('--postflop', default='showdown', choices=['showdown', 'realization'])
    ap.add_argument('--outer', type=int, default=3); ap.add_argument('--post-iters', type=int, default=3000)
    ap.add_argument('--buckets', type=int, default=16); ap.add_argument('--damping', type=float, default=0.5)
    ap.add_argument('--unopened-allin-max', type=float, default=0.0, help='règle de tapis HRC heads-up : 15')
    ap.add_argument('--rollouts', type=int, default=6, help='tirages pour la force des mains au flop et à la turn')
    a = ap.parse_args()
    OUTER, POST_ITERS, BUCKETS, DAMP, UNOPENED, ROLLOUTS = a.outer, a.post_iters, a.buckets, a.damping, a.unopened_allin_max, a.rollouts
    show(run([float(x) for x in a.stacks.split(',')], a.iters, a.postflop))
