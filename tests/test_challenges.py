"""défis (programme de travail, étape 5, 29/10/2026 ; corrections du test joueurs 9)"""
import datetime, os, sqlite3
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
    assert challenges.won('pressure', s(4)) and not challenges.won('pressure', s(3)) and not challenges.won('pressure', s(5, 1))   # 4 sur 5
    days = {D.replace(day=k) for k in range(10, 17)}
    assert challenges.full_week(days, D) == 7 and challenges.full_week({D}, D) == 1
    assert challenges.full_week(days - {D.replace(day=13)}, D) == 3        # sans jour manqué, contrairement à la série de jours
    assert not challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=82)) and challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=90))
    assert challenges.daily_seed(D) == 20261029


def _play(c, H, body, pick=0, stop=None):
    s = c.post('/sessions', json=body, headers=H).json(); hands = []
    for i in range(s['size'] if stop is None else stop):
        q = c.get(f"/quiz/next?session_id={s['session_id']}").json()['question']; hands.append((q['spot_id'], q['hand']))
        c.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][pick]['id']})
    return hands if stop is None else s['session_id']


def test_challenges_api(client):
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    assert [x['kind'] for x in r['daily']] == ['daily', 'perfect'] and [x['kind'] for x in r['weekly']] == ['pressure', 'range']
    assert all(x['status'] == 'todo' for x in r['daily'] + r['weekly']) and r['history'] == []
    t = client.get('/users/me/today?mode=gto&tz=60', headers=A).json()
    assert r['daily'][1]['theme_fr'] == t['theme_fr']                                               # série parfaite : thème de la séance
    assert _play(client, A, {'mode': 'gto', 'challenge': 'daily'}) == _play(client, B, {'mode': 'gto', 'challenge': 'daily'})   # mêmes mains pour tous
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    d = r['daily'][0]
    assert d['status'] in ('won', 'tried') and d['result_fr'] and d['action'] is None and d['next_fr'] == 'Nouveau défi demain.'
    assert r['history'] and r['history'][0]['kind'] == 'daily' and r['history'][0]['won'] == (d['status'] == 'won')   # tentatives aussi
    for mode in ('gto', 'exploit'):                                                                 # une seule tentative, tous modes confondus
        assert client.post('/sessions', json={'mode': mode, 'challenge': 'daily'}, headers=A).status_code == 409
    assert client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['daily'][0]['status'] == d['status']
    _play(client, A, {'mode': 'gto', 'challenge': 'pressure'})
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['weekly'][0]['status'] != 'todo'
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'reader'}, headers=A).status_code == 422
    assert [x['kind'] for x in client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['weekly']] == ['pressure', 'range', 'reader']
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}).status_code == 400             # joueur identifié


def test_daily_abandoned_is_resumed_not_restarted(client):
    sid = _play(client, A, {'mode': 'gto', 'challenge': 'daily'}, stop=2)
    d = client.get('/users/me/challenges?mode=gto&tz=0', headers=A).json()['daily'][0]
    assert d['status'] == 'started' and d['action'] == dict(type='resume', session_id=sid, chrono=15, challenge='daily') and d['result_fr'] == '2/5 mains jouées'
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}, headers=A).status_code == 409


def test_perfect_uses_session_theme_and_reader_has_pastilles(client):
    from spinsacademy import quiz
    t = client.get('/users/me/today?mode=gto&tz=0', headers=A).json()
    lo, hi = t['steps'][1]['filters'].get('min_stack', 0), t['steps'][1]['filters'].get('max_stack', 99)
    s = client.post('/sessions', json={'mode': 'gto', 'challenge': 'perfect'}, headers=A).json()
    for i in range(s['size']):
        q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        sp = quiz.load(s['dataset_version'])[1][q['spot_id']]
        assert lo <= sp['effective_stack_bb'] <= hi                                                 # dans le niveau du joueur
        client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']})
    s = client.post('/sessions', json={'mode': 'exploit', 'challenge': 'reader', 'seed': 3}, headers=A).json()
    con = sqlite3.connect(os.environ['SPINSACADEMY_DB'])
    spots = [r[0] for r in con.execute('SELECT spot_id FROM questions WHERE session_id = ?', (s['session_id'],))]; con.close()
    _, sp = quiz.load(s['dataset_version'])
    assert len(spots) == 5 and sum(sp[x]['field']['type'] == 'profil' for x in spots) >= challenges.READER_PASTILLES
