"""Rythme N1 (09/11/2026) : séance du jour de 10 minutes, en plus de celle de 15"""
import pytest
from fastapi.testclient import TestClient

H = {'X-Player-Id': 's' * 20}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _kinds(t): return [s['kind'] for s in t['steps']]


def test_short_session_has_no_range_and_one_theme_series(client):
    long = client.get('/users/me/today?tz=0', headers=H).json(); short = client.get('/users/me/today?tz=0&minutes=10', headers=H).json()
    assert long['minutes'] == 15 and _kinds(long) == ['review', 'theme', 'range'] and long['steps'][1]['total'] == 2
    assert short['minutes'] == 10 and _kinds(short) == ['review', 'theme'] and short['steps'][1]['total'] == 1
    assert short['theme_fr'] == long['theme_fr']                              # même thème du jour : la séance courte ne change pas le plan


def test_short_session_is_done_after_one_theme_series_while_the_long_one_goes_on(client):
    s = client.get('/users/me/today?tz=0', headers=H).json()['steps'][1]
    ss = client.post('/sessions', json={'mode': 'gto', 'plan': 'theme', 'filters': {k: v for k, v in s['filters'].items()}, 'tz': 0}, headers=H).json()
    for i in range(ss['size']):
        q = client.get(f"/quiz/next?session_id={ss['session_id']}", headers=H).json()['question']
        client.post('/attempts', json={'session_id': ss['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']}, headers=H)
    short = client.get('/users/me/today?tz=0&minutes=10', headers=H).json(); long = client.get('/users/me/today?tz=0', headers=H).json()
    assert short['steps'][1]['done'] and short['active_today']
    assert not long['steps'][1]['done'] and long['steps'][1]['count'] == 1       # la séance de 15 attend encore une série et la range
