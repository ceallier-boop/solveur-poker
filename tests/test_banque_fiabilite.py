"""P15 (décision du 05/11) : banque du solveur en test fermé de 8 à 16 BB ; filtre anti-bruit selon le champ reliability (G18)"""
import pytest
from spinsacademy import grading, quiz

V = 'gto_preflop/2026.11.07-s2'


def test_only_the_closed_test_range_is_served():
    pool = quiz.pool(V)
    assert pool and all(quiz.SOLVER_TEST_BB[0] <= sp['effective_stack_bb'] <= quiz.SOLVER_TEST_BB[1] for sp in pool)
    _, spots = quiz.load(V)
    assert any(not quiz.SOLVER_TEST_BB[0] <= sp['effective_stack_bb'] <= quiz.SOLVER_TEST_BB[1] for sp in spots.values())   # la banque couvre plus : seul le service est limité


def test_noise_floor_depends_on_the_reliability_of_the_decision():
    _, spots = quiz.load(V)
    tapis = next(sp for sp in spots.values() if sp['reliability'] == 'tapis'); flop = next(sp for sp in spots.values() if sp['reliability'] == 'flop')
    assert quiz.noise_floor(tapis) == grading.TOLERANCE_MBB and quiz.noise_floor(flop) == quiz.REF_NOISE_MBB
    assert all(quiz.error_gap(sp, h) >= quiz.noise_floor(sp) for sp in quiz.pool(V)[:200] for h in quiz.teachable(sp))


def test_reference_banks_keep_their_rules():
    _, ref = quiz.load(quiz.DEFAULT_VERSION)
    assert not any(quiz.from_solver(sp) for sp in ref.values())
    assert all(quiz.noise_floor(sp) in (0.0, quiz.REF_NOISE_MBB) for sp in ref.values())
    _, spots = quiz.load(V)
    old = next(sp for sp in spots.values() if sp['reliability'] == 'tapis')
    assert quiz.noise_floor(dict(old, reliability=None)) == quiz.REF_NOISE_MBB          # une banque sans le champ garde le seuil prudent
