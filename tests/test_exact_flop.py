"""Sous-jeu postflop exact à partir du flop (spinsacademy.postflop.exact_flop, action G9)."""
import itertools
import numpy as np
from spinsacademy.postflop.exact_flop import ExactFlopHU
from spinsacademy.postflop.kernels import CC, evaln

FLOP = [0, 21, 46]                                                  # 2s 7d Qh (carte = rang * 4 + couleur)
idx = lambda a, b: next(k for k, (x, y) in enumerate(CC) if (x, y) == (a, b))


def test_showdown_value_is_the_enumerated_equity():
    """tapis nul : abattage immédiat ; la valeur doit être l'équité sur les 990 couples turn / river (découpage par turn, poids 1/45 et 1/44)"""
    ex = ExactFlopHU(10.0, 0.0, FLOP)
    r0 = np.zeros(1326); r1 = np.zeros(1326); i, j = idx(48, 49), idx(36, 41)
    r0[i] = 1; r1[j] = 1
    V = ex.values(r0, r1, mode=1)
    rest = [c for c in range(52) if c not in FLOP + [48, 49, 36, 41]]; w = t = n = 0
    for x, y in itertools.combinations(rest, 2):
        h0 = evaln(np.array(FLOP + [x, y, 48, 49], np.int64), 7); h1 = evaln(np.array(FLOP + [x, y, 36, 41], np.int64), 7)
        w += h0 > h1; t += h0 == h1; n += 1
    assert abs(V[0][i] / 10 - (w + 0.5 * t) / n) < 1e-12 and abs((V[0][i] + V[1][j]) / 10 - 1) < 1e-12


def test_small_game_is_zero_sum_and_converges():
    """petit pot à faible profondeur : la somme des gains vaut le pot et l'exploitabilité baisse"""
    rng = np.random.default_rng(3); r0 = np.zeros(1326); r1 = np.zeros(1326)
    r0[rng.choice(1326, 60, replace=False)] = 1; r1[rng.choice(1326, 60, replace=False)] = 1
    ex = ExactFlopHU(4.0, 2.0, FLOP, aggressor=1)
    ex.solve(r0, r1, iters=3); e3 = ex.exploitability(r0, r1)
    ex.solve(r0, r1, iters=27); e30 = ex.exploitability(r0, r1)
    V = ex.values(r0, r1); m0, _ = ex.compat(r0, r1); M = float((r0 * ex.valid_flop * m0).sum())
    assert abs(((r0 * V[0]).sum() + (r1 * V[1]).sum()) / M / 4.0 - 1) < 1e-9
    assert e30 < e3 and e30 < 0.02
