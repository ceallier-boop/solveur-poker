"""Résolution complète : préflop (CFR+) et sous-jeux postflop heads-up, alternés jusqu'à stabilité des ranges.

  1. préflop résolu avec le modèle postflop courant (au départ : showdown) ;
  2. pour chaque fin de tour « flop » : sous-jeux postflop heads-up (un par paire de joueurs actifs) résolus avec les ranges qui y arrivent,
     corrections de réalisation ajustées (postflop.fit_offsets) ;
  3. retour en 1 avec ces corrections, amorties (moyenne avec le tour précédent, poids `damping`, ou moyenne de tous les
     tours : 'linear') ; on s'arrête après `outer` tours, ou plus tôt dès que la variation de stratégie d'un tour passe sous
     `tol` points, ou que la dérive passe sous `tol_mbb`.
Deux mesures de stabilité par tour :
  - shift_pts : variation des fréquences (points), pondérée par combos et atteinte. Les mains mixtes, presque indifférentes,
    peuvent changer de fréquence d'un tour à l'autre sans effet sur l'EV : cette mesure surestime l'instabilité ;
  - drift_mbb : exploitabilité de la stratégie du tour précédent dans le modèle du nouveau tour (mBB par main, pire joueur) :
    ce que coûterait de garder l'ancienne stratégie. C'est la mesure qui compte pour la correction.
Les sous-jeux sont indépendants et résolus en parallèle.
"""
import hashlib, json, os, tempfile, time
import multiprocessing as mp
import numpy as np
from ..cards import DISJOINT as D, W
from ..postflop import fast
from ..postflop.hu_solver import HUPostflop, PostflopConfig
from .cfr import Solver
from . import correction
from .postflop import Realization, fit_offsets
from .tree import TreeConfig

_POOL = None


def pool_files(n, buckets, rollouts, seed, metric='ehs', textured=False, flop_buckets=0):
    """réservoir de boards calculé une seule fois par jeu de réglages et rangé sur disque (un fichier par tableau) : les
    processus le relisent (une seconde), au lieu de le recalculer chacun à chaque configuration"""
    key = hashlib.md5(json.dumps([n, buckets, rollouts, seed, metric, textured, flop_buckets]).encode()).hexdigest()[:12]
    d = os.path.join(tempfile.gettempdir(), f'spinsacademy_pool_{key}')
    names = ('ranks', 'order', 'valid', 'bucket')
    if not all(os.path.isfile(os.path.join(d, f + '.npy')) for f in names):
        arrays = fast.board_pool(n, buckets, rollouts, seed, metric, textured, flop_buckets)
        tmp = d + f'.tmp{os.getpid()}'; os.makedirs(tmp, exist_ok=True)
        for f, a in zip(names, arrays): np.save(os.path.join(tmp, f + '.npy'), a)
        try:
            os.replace(tmp, d)
        except OSError:                                      # un autre processus l'a écrit entre-temps
            pass
    return [os.path.join(d, f + '.npy') for f in names]


def _init_pool(files):
    global _POOL
    _POOL = tuple(np.load(f) for f in files)                # copie en mémoire (80 Mo) : un tableau en lecture seule ferait recompiler numba


def _subgame(job):
    """un sous-jeu postflop ; state : regrets du même sous-jeu au tour précédent (reprise), ou None. La stratégie moyenne
    repart de zéro : elle ne doit refléter que les ranges de ce tour"""
    pot, stack, w0, w1, iters, cfg, seed, aggressor, state, corr, eff = job
    g = HUPostflop(pot, stack, cfg, aggressor=aggressor); g._arrays()
    if state is not None:
        g.Rf[:] = state
    g.fast_solve(w0, w1, _POOL, iters=iters, seed=seed)
    G0, G1 = g.fast_evaluate(w0, w1, _POOL)
    if corr:                                                 # G17 : écart exact - abstrait appris (solver.correction)
        G0, G1 = correction.get(corr).apply(pot, stack, aggressor, G0, G1, eff)
    return G0, G1, g.root_frequencies(w0, _POOL), g.Rf.astype(np.float32)


def strategy_shift(a, b):
    """écart moyen de fréquences (points) entre deux stratégies préflop, pondéré par combos et atteinte"""
    tot = 0.0; wt = 0.0
    for k, x in a.items():
        if k not in b: continue
        w = W * x['reach']; tot += float((w * 0.5 * np.abs(x['freq'] - b[k]['freq']).sum(1)).sum()); wt += float(w.sum())
    return 100 * tot / max(wt, 1e-12)


def solve(stacks, cfg=None, outer=3, pre_iters=1500, post_iters=3000, pf_cfg=None, boards=1000, workers=4, seed=1, damping=0.5, log=print, tol=None, tol_mbb=None,
          warm=False, post_warm=1000, rare_mass=0.0, rare_iters=500, correction=None):
    """warm : à partir du 2e tour, chaque sous-jeu postflop repart des regrets du même sous-jeu au tour précédent (la stratégie
    moyenne, elle, repart de zéro : elle ne doit refléter que les ranges de ce tour), avec post_warm itérations au lieu de
    post_iters. Le préflop, lui, est toujours résolu depuis zéro (2 à 40 s) : repris, ses nœuds peu joués (le BB qui part à
    tapis sur une relance, par exemple) n'apprenaient plus rien et gardaient des fréquences sans valeur. rare_mass : un sous-jeu dont la masse (probabilité que ses deux
    ranges arrivent au flop) pèse moins de rare_mass de la masse de tous les sous-jeux reçoit au plus rare_iters itérations
    (rare_iters // 2 en reprise) : ces lignes comptent peu dans les EV préflop. correction : nom d'une table de
    solver.correction (G17), ajoutée aux gains postflop des pots relancés avant fit_offsets ; None : aucune."""
    pf_cfg = pf_cfg or PostflopConfig(); model = Realization(); history = []; states = {}
    ctx = mp.get_context('fork' if 'fork' in mp.get_all_start_methods() else 'spawn')   # Windows : pas de fork
    files = pool_files(boards, pf_cfg.buckets, pf_cfg.rollouts, seed, pf_cfg.metric, pf_cfg.textured, pf_cfg.flop_buckets)
    with ctx.Pool(workers, initializer=_init_pool, initargs=(files,)) as pool:
        s = Solver(stacks, cfg or TreeConfig(), postflop=model).solve(pre_iters); prev = s.strategy()
        for k in range(outer):
            t0 = time.time(); _, reach = s._pass(avg=True); subs = Realization.subgames(s)
            mass = [float(reach[nd.id][o] @ D @ reach[nd.id][i]) for nd, o, i, *_ in subs]; tot = max(sum(mass), 1e-300)
            live = [j for j, (nd, o, i, *_) in enumerate(subs) if reach[nd.id][o].sum() > 0 and reach[nd.id][i].sum() > 0]
            subs = [subs[j] for j in live]; mass = [mass[j] for j in live]   # range vide (action jamais jouée) : correction précédente gardée
            jobs = []
            for j, (nd, o, i, pot, stack, ag) in enumerate(subs):
                key = (nd.id, o, i); st = states.get(key) if warm else None
                it = post_iters if st is None else post_warm
                if mass[j] < rare_mass * tot: it = min(it, rare_iters if st is None else rare_iters // 2)
                jobs.append((pot, stack, reach[nd.id][o], reach[nd.id][i], it, pf_cfg, seed + 17 * j + 1009 * k * warm, ag, st, correction,
                             min(stacks[o], stacks[i])))
            results = pool.map(_subgame, jobs)
            roots = {}
            for (nd, o, i, pot, stack, _), (G0, G1, rf, st) in zip(subs, results):
                d0, d1 = fit_offsets(pot, reach[nd.id][o], reach[nd.id][i], G0, G1)
                model.store(nd, o, i, d0, d1, damping); roots[(nd.key, o, i)] = rf
                if warm: states[(nd.id, o, i)] = st
            model.commit(damping)                                # amortissement : évite les oscillations entre tours
            old_S = s.S
            s = Solver(stacks, cfg or TreeConfig(), postflop=model).solve(pre_iters)
            cur = s.strategy(); shift = strategy_shift(cur, prev); prev = cur
            new_S, s.S = s.S, old_S; drift = 1000 * max(s.exploitability()); s.S = new_S     # même arbre : mêmes identifiants de nœuds
            history.append(dict(round=k + 1, subgames=len(subs), rare=sum(m < rare_mass * tot for m in mass), shift_pts=shift, drift_mbb=drift, seconds=time.time() - t0))
            if log: log(f'  tour {k + 1} : {len(subs)} sous-jeux postflop, variation de stratégie {shift:.2f} points, dérive {drift:.2f} mBB ({time.time() - t0:.0f} s)')
            if (tol is not None and shift <= tol) or (tol_mbb is not None and drift <= tol_mbb): break
    return s, model, history
