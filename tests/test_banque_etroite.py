"""Retest joueurs I9 (10/11/2026) : avec la banque du test fermé (solveur, 8 à 16 BB) la séance du débutant et le test de placement ne sont plus refusés"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import levels, quiz

H = {'X-Player-Id': 'd' * 20}
BANQUE = '2026.11.07-s2'


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy import api               # importé avant tout réglage : DEFAULT_OF se fige à l'import
    monkeypatch.setattr(api, 'serving_version', lambda con, mode: BANQUE)
    return TestClient(api.app)


def test_beginner_theme_series_is_shorter_not_refused(client):
    r = client.post('/sessions', json={'mode': 'gto', 'plan': 'theme', 'filters': {'family': 'first_in', 'min_stack': 0, 'max_stack': 9.5}}, headers=H)
    assert r.status_code == 201, r.text
    assert 3 <= r.json()['size'] <= 5


def test_placement_on_narrow_bank_gives_ten_hands_and_no_level_3(client):
    s = client.post('/sessions', json={'mode': 'gto', 'plan': 'placement'}, headers=H)
    assert s.status_code == 201, s.text
    s = s.json(); assert s['size'] == 10
    ver = s['dataset_version']; _, spots = quiz.load(ver)
    for i in range(10):
        q = client.get(f"/quiz/next?session_id={s['session_id']}", headers=H).json()['question']
        assert 8 <= spots[q['spot_id']]['effective_stack_bb'] <= 16
        best = next((o['id'] for o in q['options'] if quiz.correct(ver, q['spot_id'], q['hand'], o['id'])['verdict'] == 'correct'), q['options'][0]['id'])
        client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': best}, headers=H)
    res = client.get(f"/users/me/placement?session_id={s['session_id']}", headers=H).json()
    assert res['complete'] and res['proposed_level'] <= 2


def test_placement_result_unit_missing_band():
    r = levels.placement_result([(9, 1.0)] * 4 + [(12, 1.0)] * 6, [9] * 4 + [12] * 6)
    assert r['complete'] and r['proposed_level'] == 2
