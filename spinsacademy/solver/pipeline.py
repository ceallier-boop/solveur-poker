"""Résolution complète : préflop (CFR+) et sous-jeux postflop heads-up, alternés jusqu'à stabilité des ranges.

  1. préflop résolu avec le modèle postflop courant (au départ : showdown) ;
  2. pour chaque fin de tour « flop » : sous-jeux postflop heads-up (un par paire de joueurs actifs) résolus avec les ranges qui y arrivent,
     corrections de réalisation ajustées (postflop.fit_offsets) ;
  3. retour en 1 avec ces corrections, amorties (moyenne avec le tour précédent, poids `damping`) ;
     on s'arrête après `outer` tours.
Les sous-jeux sont indépendants et résolus en parallèle.
"""
import multiprocessing as mp
import time
import numpy as np
from ..cards import W
from ..postflop import fast
from ..postflop.hu_solver import HUPostflop, PostflopConfig
from .cfr import Solver
from .postflop import Realization, fit_offsets
from .tree import TreeConfig

_POOL = None


def _init_pool(n, buckets, rollouts, seed, metric='ehs', textured=False):
    global _POOL
    _POOL = fast.board_pool(n, buckets, rollouts, seed, metric, textured)


def _subgame(job):
    pot, stack, w0, w1, iters, cfg, seed, aggressor = job
    g = HUPostflop(pot, stack, cfg, aggressor=aggressor).fast_solve(w0, w1, _POOL, iters=iters, seed=seed)
    G0, G1 = g.fast_evaluate(w0, w1, _POOL)
    return G0, G1, g.root_frequencies(w0, _POOL)


def strategy_shift(a, b):
    """écart moyen de fréquences (points) entre deux stratégies préflop, pondéré par combos et atteinte"""
    tot = 0.0; wt = 0.0
    for k, x in a.items():
        if k not in b: continue
        w = W * x['reach']; tot += float((w * 0.5 * np.abs(x['freq'] - b[k]['freq']).sum(1)).sum()); wt += float(w.sum())
    return 100 * tot / max(wt, 1e-12)


def solve(stacks, cfg=None, outer=3, pre_iters=1500, post_iters=3000, pf_cfg=None, boards=1000, workers=4, seed=1, damping=0.5, log=print):
    pf_cfg = pf_cfg or PostflopConfig(); model = Realization(); history = []
    ctx = mp.get_context('fork')
    with ctx.Pool(workers, initializer=_init_pool, initargs=(boards, pf_cfg.buckets, pf_cfg.rollouts, seed, pf_cfg.metric, pf_cfg.textured)) as pool:
        s = Solver(stacks, cfg or TreeConfig(), postflop=model).solve(pre_iters); prev = s.strategy()
        for k in range(outer):
            t0 = time.time(); _, reach = s._pass(avg=True); subs = Realization.subgames(s)
            jobs = [(pot, stack, reach[nd.id][o], reach[nd.id][i], post_iters, pf_cfg, seed + 17 * j, ag) for j, (nd, o, i, pot, stack, ag) in enumerate(subs)]
            results = pool.map(_subgame, jobs)
            roots = {}
            for (nd, o, i, pot, stack, _), (G0, G1, rf) in zip(subs, results):
                d0, d1 = fit_offsets(pot, reach[nd.id][o], reach[nd.id][i], G0, G1)
                model.store(nd, o, i, d0, d1, damping); roots[(nd.key, o, i)] = rf
            model.commit(damping)                                # amortissement : évite les oscillations entre tours
            s = Solver(stacks, cfg or TreeConfig(), postflop=model).solve(pre_iters)
            cur = s.strategy(); shift = strategy_shift(cur, prev); prev = cur
            history.append(dict(round=k + 1, subgames=len(subs), shift_pts=shift, seconds=time.time() - t0))
            if log: log(f'  tour {k + 1} : {len(subs)} sous-jeux postflop, variation de stratégie {shift:.2f} points ({time.time() - t0:.0f} s)')
    return s, model, history
