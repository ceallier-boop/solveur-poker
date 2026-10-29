"""défis (programme de travail, étape 5, 29/10/2026)"""
import datetime
import pytest
from fastapi.testclient import TestClient
from spinsacademy import challenges

A, B = {'X-Player-Id': 'chal-a-0000'}, {'X-Player-Id': 'chal-b-0000'}
D = datetime.date(2026, 10, 29)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_rules():
    s = lambda c, t=0: dict(correct=c, size=5, timeouts=t)
    assert challenges.won('daily', s(4)) and not challenges.won('daily', s(3))
    assert challenges.won('perfect', s(5)) and not challenges.won('perfect', s(4))
    assert challenges.won('pressure', s(3)) and not challenges.won('pressure', s(5, 1))
    days = {D.replace(day=k) for k in range(10, 17)}
    assert challenges.full_week(days, D) == 7 and challenges.full_week({D}, D) == 1
    assert challenges.daily_seed(D) == 20261029


def _play(c, H, body, pick=0):
    s = c.post('/sessions', json=body, headers=H).json(); hands = []
    for i in range(s['size']):
        q = c.get(f"/quiz/next?session_id={s['session_id']}").json()['question']; hands.append((q['spot_id'], q['hand']))
        c.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][pick]['id']})
    return hands


def test_challenges_api(client):
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    assert [x['kind'] for x in r['daily']] == ['daily', 'perfect'] and [x['kind'] for x in r['weekly']] == ['pressure', 'range']
    assert all(x['status'] == 'todo' for x in r['daily'] + r['weekly']) and r['history'] == [] and r['daily'][1]['theme_fr']
    assert _play(client, A, {'mode': 'gto', 'challenge': 'daily'}) == _play(client, B, {'mode': 'gto', 'challenge': 'daily'})   # mêmes mains pour tous
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    d = r['daily'][0]
    assert d['status'] in ('won', 'tried') and d['result_fr'] and d['action'] is None                   # une seule tentative compte
    assert (d['status'] == 'won') == bool(r['history'])
    _play(client, A, {'mode': 'gto', 'challenge': 'pressure'})
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['weekly'][0]['status'] != 'todo'
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'reader'}, headers=A).status_code == 422
    assert [x['kind'] for x in client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['weekly']] == ['pressure', 'range', 'reader']
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}).status_code == 400             # joueur identifié
