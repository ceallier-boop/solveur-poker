"""Erreur d'abstraction du solveur postflop, mesurée sans HRC : sous-jeu river ou turn résolu exactement board par board.

Ranges : celles d'un export HRC à l'entrée du postflop (produit des fréquences jouées le long de la ligne), par exemple
le pot limpé heads-up : le SB limpe (root:C, il est IP), le BB checke (SB-call:X, il est OOP).
1. Le solveur abstrait de production (groupes de force partagés entre boards) est entraîné sur le sous-jeu qui commence
   à la rue choisie, sur un réservoir de boards au hasard.
2. Sur K boards tirés au hasard, le sous-jeu est résolu exactement (spinsacademy.postflop.exact) ; on évalue aussi la
   stratégie abstraite sur ce board, et son exploitabilité.
3. Gains G par classe (comme fast_evaluate) : abstrait - exact, par famille de mains. C'est l'erreur que reçoit le
   modèle de réalisation du préflop.

Usage : python tools/solver/exact_check.py --street river --boards 200
        python tools/solver/exact_check.py --street turn --boards 40 --exact-iters 400
"""
import argparse, json, multiprocessing as mp, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy.cards import NAMES, W
from spinsacademy.hrc import load, labels
from spinsacademy.postflop.kernels import CC, CLASS_OF
from spinsacademy.postflop.hu_solver import HUPostflop, PostflopConfig
from spinsacademy.postflop.fast import board_pool
from spinsacademy.postflop.exact import ExactHU, abstract_buckets, average_sigma

R_ = '23456789TJQKA'
CATS = ['paires', 'As assortis', 'connecteurs assortis', 'autres assorties', 'broadways dépareillés', 'As dépareillés', 'dépareillées faibles']


def cat(h):
    if len(h) == 2: return 'paires'
    a, b, s = R_.index(h[0]), R_.index(h[1]), h[2] == 's'
    if s and a == 12: return 'As assortis'
    if s and a - b <= 2: return 'connecteurs assortis'
    if s: return 'autres assorties'
    if b >= 8: return 'broadways dépareillés'
    if a == 12: return 'As dépareillés'
    return 'dépareillées faibles'


def hrc_range(nodes, st, line):
    """produit, le long de la ligne, des fréquences jouées par le joueur ; line = 'nœud:action,nœud:action'"""
    w = None
    for item in line.split(','):
        key, act = item.split(':'); n = nodes[key]; hl = labels(n, st)
        f = np.array([n['hands'][h]['played'][hl.index(act)] for h in NAMES])
        if w is None: w = np.array([n['hands'][h]['weight'] for h in NAMES])
        w = w * f
    return w


G_ = {}


def _board(i):
    a = G_['args']; rng = np.random.default_rng(a.seed * 7919 + i)
    board = [int(x) for x in rng.choice(52, 5 if a.street == 'river' else 4, replace=False)]
    r0, r1 = G_['r0'], G_['r1']; t0 = time.time()
    ex = ExactHU(a.pot, a.stack, board, tree=G_['tree'])
    ex.solve(r0, r1, a.exact_iters); e_eq = ex.exploitability(r0, r1)
    eq = ex.values(r0, r1)                                 # solve() laisse la stratégie moyenne dans ex.sig
    ex.set_abstract(G_['sigma'], abstract_buckets(ex, a.buckets, a.rollouts, int(rng.integers(1 << 30)), a.metric, a.textured))
    ab = ex.values(r0, r1); e_ab = ex.exploitability(r0, r1)
    m = ex.compat(r0, r1)
    return dict(i=i, eq=eq, ab=ab, m=m, e_eq=e_eq, e_ab=e_ab, sec=time.time() - t0)


def by_class(vals, masses):
    num = np.bincount(CLASS_OF, weights=vals, minlength=169); den = np.bincount(CLASS_OF, weights=masses, minlength=169)
    return np.where(den > 0, num / np.where(den > 0, den, 1), np.nan)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--street', choices=('river', 'turn'), default='river')
    ap.add_argument('--hrc', default='data/hrc/raw/min_raise_hu/hand_15')
    ap.add_argument('--oop', default='SB-call:X', help='ligne du joueur OOP (BB en heads-up)')
    ap.add_argument('--ip', default='root:C', help='ligne du joueur IP (SB, bouton)')
    ap.add_argument('--pot', type=float, default=2.0); ap.add_argument('--stack', type=float, default=24.0)
    ap.add_argument('--boards', type=int, default=200); ap.add_argument('--exact-iters', type=int, default=1000)
    ap.add_argument('--abs-iters', type=int, default=3000); ap.add_argument('--pool', type=int, default=1000)
    ap.add_argument('--buckets', type=int, default=16); ap.add_argument('--rollouts', type=int, default=6)
    ap.add_argument('--metric', default='ehs'); ap.add_argument('--textured', action='store_true'); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--out', default=None)
    a = ap.parse_args()
    s, st, nodes = load(a.hrc)
    w0 = hrc_range(nodes, st, a.oop); w1 = hrc_range(nodes, st, a.ip)
    r0 = w0[CLASS_OF]; r1 = w1[CLASS_OF]
    start = 2 if a.street == 'river' else 1
    cfg = PostflopConfig(buckets=a.buckets, rollouts=a.rollouts, metric=a.metric, textured=a.textured)
    t0 = time.time()
    hp = HUPostflop(a.pot, a.stack, cfg, start_street=start)
    pool = board_pool(a.pool, a.buckets, a.rollouts, a.seed + 1, a.metric, a.textured)
    hp.fast_solve(w0, w1, pool, iters=a.abs_iters, seed=a.seed)
    print(f'abstrait : {len(hp.nodes)} nœuds, {a.abs_iters} itérations sur {a.pool} boards ({time.time() - t0:.0f} s)', flush=True)
    G_.update(args=a, r0=r0, r1=r1, tree=HUPostflop(a.pot, a.stack, cfg, start_street=start), sigma=average_sigma(hp))
    res = []
    with mp.get_context('fork').Pool(a.workers) as p:
        for k, r in enumerate(p.imap_unordered(_board, range(a.boards))):
            res.append(r)
            if (k + 1) % max(1, a.boards // 10) == 0:
                print(f'  {k + 1}/{a.boards} boards ; exploitabilité exacte {100 * np.mean([x["e_eq"] for x in res]):.2f} % pot, '
                      f'abstraite {100 * np.mean([x["e_ab"] for x in res]):.2f} % pot ({r["sec"]:.0f} s/board)', flush=True)
    out = dict(street=a.street, hrc=a.hrc, oop=a.oop, ip=a.ip, pot=a.pot, stack=a.stack, boards=a.boards, exact_iters=a.exact_iters,
               abs_iters=a.abs_iters, buckets=a.buckets, metric=a.metric, textured=a.textured,
               exploitability_exact_pct_pot=100 * float(np.mean([x['e_eq'] for x in res])),
               exploitability_abstract_pct_pot=100 * float(np.mean([x['e_ab'] for x in res])), players={})
    print(f'\n== {a.street}, pot {a.pot:g} BB, tapis {a.stack:g} BB, {a.boards} boards')
    print(f'exploitabilité moyenne : exacte {out["exploitability_exact_pct_pot"]:.2f} % du pot, '
          f'stratégie abstraite {out["exploitability_abstract_pct_pot"]:.2f} % du pot')
    for p, name, w in ((0, 'OOP (' + a.oop + ')', w0), (1, 'IP (' + a.ip + ')', w1)):
        M = sum(x['m'][p] for x in res)
        Ge = by_class(sum(x['eq'][p] for x in res), M); Ga = by_class(sum(x['ab'][p] for x in res), M)
        mass = W * w; ok = (mass > 0) & ~np.isnan(Ge)
        d = 1000 * (Ga - Ge)
        line = f'{name} : G abstrait - G exact (mBB) :'; fam = {}
        for c in CATS:
            msk = ok & np.array([cat(h) == c for h in NAMES])
            if msk.any(): fam[c] = float(np.average(d[msk], weights=mass[msk])); line += f' {c} {fam[c]:+.0f} ;'
        tot = float(np.average(d[ok], weights=mass[ok])); line += f' global {tot:+.0f}'
        print(line)
        worst = sorted((i for i in range(169) if ok[i]), key=lambda i: -abs(d[i]))[:8]
        print('   écarts les plus forts : ' + ', '.join(f'{NAMES[i]} {d[i]:+.0f}' for i in worst))
        out['players'][name] = dict(by_family_mbb=fam, global_mbb=tot,
                                    by_class_mbb={NAMES[i]: round(float(d[i]), 1) for i in range(169) if ok[i]},
                                    G_exact={NAMES[i]: round(float(Ge[i]), 4) for i in range(169) if ok[i]})
    if a.out: json.dump(out, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print('FIN', flush=True)


if __name__ == '__main__':
    main()
