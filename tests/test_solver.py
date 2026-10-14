import numpy as np
import pytest
from spinsacademy.cards import W
from spinsacademy.hrc import exports, labels, load, preflop_hash
from spinsacademy.solver.cfr import Solver, layers
from spinsacademy.solver.tree import Tree, TreeConfig
from conftest import needs_raw

pct = lambda f: 100 * float((W * f).sum() / W.sum())


@needs_raw
def test_tree_reproduces_hrc_action_sets():
    """sur tous les nœuds exportés par HRC (arbre de référence), mêmes actions, hors tapis toujours proposé et fold gratuit retiré"""
    checked = 0
    for d in exports():
        s, st, nodes = load(d)
        if preflop_hash(s) != 'daa9aaa0' or max(st) > 25: continue        # au-delà de 25 BB (base v3) : règles HRC de relance incomplète non modélisées
        bk = Tree(st).by_key()
        for k, n in nodes.items():
            assert k in bk, (d, k)
            hl = set(labels(n, st))
            if 'F' not in bk[k].actions: hl -= {'F'}
            assert not (set(bk[k].actions) ^ hl) - {'A'}, (d, k, labels(n, st), bk[k].actions)
            checked += 1
    assert checked > 300


def test_side_pots():
    assert layers((10, 4, 10), [0, 1, 2]) == [(12, (0, 1, 2)), (12, (0, 2))]
    got = layers((2.3, 0.5, 1.0), [0])
    assert [e for _, e in got] == [(0,)] * 3 and np.allclose([a for a, _ in got], [1.5, 1.0, 1.3])   # tout revient au seul joueur actif


def test_heads_up_push_fold_nash():
    s = Solver([10, 10], TreeConfig(open_sb=99, allow_limp=False)).solve(2000)
    st = s.strategy()
    assert abs(pct(st['root']['freq'][:, 1]) - 58.3) < 0.5 and abs(pct(st['SB-allin']['freq'][:, 1]) - 37.4) < 0.5
    assert max(s.exploitability()) < 1e-4


def test_three_handed_push_fold_converges():
    s = Solver([10, 10, 10], TreeConfig(open_sb=99, open_btn=99, allow_limp=False)).solve(600)
    st = s.strategy()
    assert abs(pct(st['root']['freq'][:, 1]) - 33) < 1.5 and abs(pct(st['BTN-fold']['freq'][:, 1]) - 58) < 1.5
    assert max(s.exploitability()) < 1e-3


def test_full_tree_heads_up_converges_and_is_zero_sum():
    s = Solver([15, 15]).solve(1500)
    assert max(s.exploitability()) < 2e-3                      # < 2 mBB par main
    V, reach = s._pass(avg=True); r = s.tree.root.id
    ev = [float((W * V[r][p] / s.mass(p, reach[r])).sum() / W.sum()) for p in range(2)]
    assert abs(ev[0] + ev[1]) < 1e-6                           # jeu à somme nulle (heads-up : pondération exacte)


@needs_raw
def test_default_tree_matches_hrc_actions_exactly():
    """avec les seuils de tapis HRC (réglage par défaut), l'arbre reproduit exactement les actions HRC, tapis compris"""
    checked = 0
    for d in exports():
        s, st, nodes = load(d)
        if preflop_hash(s) != 'daa9aaa0' or max(st) > 25: continue        # au-delà de 25 BB (base v3) : règles HRC de relance incomplète non modélisées
        bk = Tree(st).by_key()
        for k, n in nodes.items():
            hl = set(labels(n, st))
            if 'F' not in bk[k].actions: hl -= {'F'}
            assert set(bk[k].actions) == hl, (d, k, labels(n, st), bk[k].actions)
            checked += 1
    assert checked > 300
