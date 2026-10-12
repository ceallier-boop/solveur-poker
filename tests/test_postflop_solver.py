import itertools
import numpy as np
import pytest
from spinsacademy.cards import W
from spinsacademy.postflop import fast, kernels as K
from spinsacademy.postflop.hu_solver import HUPostflop
from spinsacademy.solver.postflop import fit_offsets


@pytest.fixture(scope='module')
def pool():
    return fast.board_pool(120, 16, 4, 3)


def test_showdown_kernel_matches_brute_force():
    rng = np.random.default_rng(1)
    board = rng.choice(52, 5, replace=False).astype(np.int64)
    ranks = K.combo_ranks(board, K.CC); opp = rng.random(1326) * (rng.random(1326) < 0.3); opp[ranks < 0] = 0
    win, tie, tot = K.showdown(ranks, opp, K.CC)
    for c in rng.choice(np.where(ranks >= 0)[0], 25):
        a, b = K.CC[c]
        ok = [d for d in range(1326) if ranks[d] >= 0 and not ({a, b} & set(K.CC[d]))]
        assert abs(sum(opp[d] for d in ok if ranks[d] < ranks[c]) - win[c]) < 1e-9
        assert abs(sum(opp[d] for d in ok if ranks[d] == ranks[c]) - tie[c]) < 1e-9
        assert abs(sum(opp[d] for d in ok) - tot[c]) < 1e-9


def test_numba_iteration_equals_python(pool):
    g1, g2 = HUPostflop(3.0, 7.0), HUPostflop(3.0, 7.0); w = np.ones(169); ranks, order, valid, bucket = pool
    r = w[K.CLASS_OF]; i = 5
    g1.t = 1; out = g1._walk(g1.root, [r * valid[i], r * valid[i]], dict(ranks=ranks[i], valid=valid[i], bucket=list(bucket[i])), False, True)
    arr = g2._arrays(); g2.t = 1
    fast.iterate(*arr, g2.P, g2.Rf, g2.Sf, 1.0, ranks[i], order[i], valid[i], bucket[i], r, r, True, False, g2.V, g2.reach, K.CC)
    assert np.abs(out[0] - g2.V[0, 0]).max() < 1e-9 and np.abs(out[1] - g2.V[0, 1]).max() < 1e-9
    assert max(np.abs(g1.R[n.id] - g2.Rf[n.id, :, :len(n.actions)]).max() for n in g1.dec) < 1e-9


def test_postflop_is_zero_sum_and_position_matters(pool):
    w = np.ones(169)
    g = HUPostflop(2.0, 9.0).fast_solve(w, w, pool, iters=600)
    G0, G1 = g.fast_evaluate(w, w, pool)
    g0, g1 = np.average(G0, weights=W), np.average(G1, weights=W)
    assert abs(g0 + g1 - 2.0) < 0.02                 # le pot initial est réparti entre les deux joueurs
    assert g1 > g0 + 0.1                             # à ranges égales, le joueur en position gagne plus


def test_fit_offsets_reproduces_marginals():
    rng = np.random.default_rng(2); P = 4.0
    w0 = rng.random(169); w1 = rng.random(169)
    d0t = rng.normal(0, 0.2, 169); d1t = rng.normal(0, 0.2, 169)
    from spinsacademy.cards import DISJOINT as D
    from spinsacademy.allin import E
    G = P * E + d0t[:, None] - d1t[None, :]
    G0 = (D * G) @ w1 / (D @ w1); G1 = (D * (P - G)).T @ w0 / (D.T @ w0)
    d0, d1 = fit_offsets(P, w0, w1, G0, G1)
    Gh = P * E + d0[:, None] - d1[None, :]
    assert np.abs((D * Gh) @ w1 / (D @ w1) - G0).max() < 1e-6 and np.abs((D * (P - Gh)).T @ w0 / (D.T @ w0) - G1).max() < 1e-6


def test_pipeline_three_handed_runs_and_stays_consistent():
    """chaîne complète à 3 joueurs (petits réglages) : pas d'erreur, ranges postflop prises en compte, exploitabilité faible"""
    from spinsacademy.solver.pipeline import solve
    from spinsacademy.postflop.hu_solver import PostflopConfig
    s, model, hist = solve([8, 8, 8], outer=1, pre_iters=300, post_iters=200, boards=60, workers=2,
                           pf_cfg=PostflopConfig(rollouts=2), log=None)
    assert model.offsets and len(hist) == 1
    assert max(s.exploitability()) < 0.01
