"""Audit AU3 (06/11/2026) : la série rapide reste dans la profondeur du niveau du joueur"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import levels, quiz

H = {'X-Player-Id': 'a' * 20}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _quick_series(client, n=4):
    out = []
    for _ in range(n):
        s = client.post('/sessions', json={'mode': 'gto', 'filters': {}}, headers=H).json()
        for i in range(s['size']):
            q = client.get(f"/quiz/next?session_id={s['session_id']}", headers=H).json()['question']
            out.append(q['spot_id'])
            client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']}, headers=H)
    return out


@pytest.mark.parametrize('experience,level', [('debut', 1), ('confirme', 2)])
def test_quick_series_stays_in_the_level_depth(client, experience, level):
    assert client.post('/users/me/onboarding', json={'experience': experience, 'goal': 'bases'}, headers=H).json()['level'] == level
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    lo, hi = levels.LEVELS[level]['depth']
    out = [spots[s]['effective_stack_bb'] for s in _quick_series(client)]
    bad = sorted(x for x in out if not lo <= x < hi)
    assert out and not bad, (level, f'hors profondeur : {bad}')


def test_explicit_filters_are_left_alone(client):
    client.post('/users/me/onboarding', json={'experience': 'debut', 'goal': 'bases'}, headers=H)
    s = client.post('/sessions', json={'mode': 'gto', 'filters': {'min_stack': 12, 'max_stack': 25}}, headers=H)
    assert s.status_code == 201
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    q = client.get(f"/quiz/next?session_id={s.json()['session_id']}", headers=H).json()['question']
    assert spots[q['spot_id']]['effective_stack_bb'] >= 12
