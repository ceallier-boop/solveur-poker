import numpy as np
from spinsacademy.postflop.exact import ExactHU, abstract_buckets, average_sigma
from spinsacademy.postflop.hu_solver import HUPostflop, PostflopConfig
from spinsacademy.postflop.fast import board_pool

BOARD = [0, 13, 26, 40, 51]
ONES = np.ones(1326)


def test_river_converges_and_is_zero_sum():
    ex = ExactHU(2, 24, BOARD)
    ex.solve(ONES, ONES, 50); e50 = ex.exploitability(ONES, ONES)
    ex.solve(ONES, ONES, 450); e500 = ex.exploitability(ONES, ONES)
    assert e500 < e50 and e500 < 0.01
    v0, v1 = ex.values(ONES, ONES); m0, _ = ex.compat(ONES, ONES)
    assert abs((v0.sum() + v1.sum()) / (ex.valid[0] * m0).sum() - 2.0) < 1e-9          # G_OOP + G_IP = pot


def test_no_stack_is_pure_showdown():
    ex = ExactHU(2, 0, BOARD); ex.solve(ONES, ONES, 1)
    assert len(ex.kind) == 1
    v0, v1 = ex.values(ONES, ONES); m0, m1 = ex.compat(ONES, ONES)
    eq0 = np.where(m0 > 0, v0 / np.where(m0 > 0, m0, 1), 0)
    best = int(np.argmax(np.where(ex.valid[0] > 0, ex.ranks[0], -1)))
    assert abs(eq0[best] - 2.0) < 0.02                                                    # la meilleure main gagne (presque) tout le pot


def test_turn_has_one_chance_node_per_river_transition_and_abstract_is_exploitable():
    cfg = PostflopConfig(buckets=4, rollouts=2)
    hp = HUPostflop(2, 3, cfg, start_street=1)
    ex = ExactHU(2, 3, BOARD[:4], tree=hp)
    n_trans = sum(1 for n in hp.nodes for ch in n.children if n.street == 1 and ch.street >= 2)
    assert (ex.kind == 3).sum() == n_trans and set(ex.nch[ex.kind == 3]) == {48}
    pool = board_pool(20, 4, 2, 0); hp.fast_solve(ONES[:169], ONES[:169], pool, iters=50)
    ex.solve(ONES, ONES, 30); e_eq = ex.exploitability(ONES, ONES)
    ex.set_abstract(average_sigma(hp), abstract_buckets(ex, 4, 2, 0)); e_ab = ex.exploitability(ONES, ONES)
    assert e_ab > e_eq >= 0
