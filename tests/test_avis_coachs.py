"""P13 : règle des désaccords entre coachs (décision du 05/11, docs/produit/DECISIONS_2026-11-05.md) côté serveur.
Les textes servis ne citent ni coach ni nom : « experts »."""
import json, re
import pytest
from spinsacademy import coachs, quiz
from tools.solver import build_avis_coachs
from tests.test_coachs import PILOT, CLOSED_TEST, spot_in, action_id


def test_avis_file_is_regenerated_identically():
    with open(coachs.PATH, encoding='utf-8') as f: assert json.load(f) == json.loads(json.dumps(build_avis_coachs.build(), sort_keys=True))
    assert len(coachs.json.load(open(coachs.PATH, encoding='utf-8'))['avis']) == 60


def test_no_coach_name_in_the_data():
    blob = open(coachs.PATH, encoding='utf-8').read().lower()
    assert not re.search(r'lucho|lucky|pasg8|\bpa\b', blob)


def _answer(version, situation, hand, label):
    sp = spot_in(version, situation); aid = action_id(sp, label)
    return sp, aid, quiz.correct(version, sp['spot_id'], hand, aid)


def test_split_case_accepts_both_strategies_and_gives_the_nuance():
    """S035 : AA au BTN à 3 joueurs, 12 BB. Deux experts relancent, un limpe : les deux sont acceptés, la relance est la plus recommandée"""
    sit = '3w-12-12-12-root-5ef802'
    for label, recommended in (('RAISE TO 2,3 BB', True), ('CALL 1 BB', False)):
        sp, aid, r = _answer(PILOT, sit, 'AA', label)
        assert r['verdict'] == 'correct' and r['points'] == 1.0
        assert r['avis']['split'] and r['avis']['recommended'] is recommended and r['avis']['experts'] == 3
        assert r['avis']['nuance_fr'] == ('2 experts sur 3' if recommended else '1 expert sur 3')
        assert 'ne sont pas d\'accord' in r['explanation_fr'] and 'Les deux stratégies sont possibles' in r['explanation_fr'] if recommended else '2 experts sur 3' in r['explanation_fr']
        assert not re.search(r'coach|lucho|lucky', json.dumps(r, ensure_ascii=False), re.I)


def test_unanimous_experts_against_the_solver_are_accepted_and_the_solver_view_is_said():
    """S001 : KQo face au 3,5x du SB à 25 BB, heads-up : les trois experts payent, le solveur relance (écart de 137 mBB)"""
    sp, aid, r = _answer(PILOT, 'hu-25-25-SB-raise3.5-b8a863', 'KQo', 'CALL 2,5 BB')
    assert r['verdict'] == 'correct' and r['regret_mbb'] == 0.0 and r['solver_regret_mbb'] > 20
    assert not r['avis']['split'] and 'Le solveur préfère' in r['explanation_fr'] and 'Tu perds' not in r['explanation_fr']


def test_unreviewed_hand_keeps_the_solver_verdict():
    sp = spot_in(PILOT, '3w-12-12-12-root-5ef802')
    other = next(h for h in quiz.teachable(sp) if coachs.lookup(sp, h) is None)
    for a in sp['actions']:
        r = quiz.correct(PILOT, sp['spot_id'], other, a['id'])
        assert r['avis'] is None and r['solver_regret_mbb'] == r['regret_mbb']


def test_summary_does_not_count_an_accepted_answer_as_a_loss():
    sp, aid, r = _answer(PILOT, 'hu-25-25-SB-raise3.5-b8a863', 'KQo', 'CALL 2,5 BB')
    s = quiz.summary(PILOT, [(sp['spot_id'], 'KQo', r)])
    assert s['bb_lost'] == 0 and s['errors'] == [] and s['points'] == 1.0


def test_label_resolution_is_none_for_unknown_words_and_ambiguous_options():
    sp = spot_in(CLOSED_TEST, '3w-25-25-25-root-0be5e9')
    assert coachs.action_id(sp, 'SHRUG 2 BB') is None
