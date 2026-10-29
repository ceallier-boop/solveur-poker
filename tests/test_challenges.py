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
    assert challenges.won('pressure', s(4)) and not challenges.won('pressure', s(3)) and not challenges.won('pressure', s(5, 1))   # test joueurs 9 : 4/5
    days = {D.replace(day=k) for k in range(10, 17)}
    assert challenges.full_week(days, D) == 7 and challenges.full_week({D}, D) == 1
    gap = {D.replace(day=k) for k in (20, 21, 22, 24, 25, 26)}           # un jour manqué pardonné, comme la série de jours
    assert challenges.full_week(gap, D.replace(day=26)) == 6 == challenges.td.streak(gap, D.replace(day=26))
    assert challenges.full_week(gap | {D.replace(day=27)}, D.replace(day=27)) == 7
    assert challenges.full_week({datetime.date(2026, 9, 30), D.replace(day=1)}, D.replace(day=1)) == 1   # le mois seulement
    assert challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=85)) and not challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=82))   # « trop serrée »
    assert challenges.daily_seed(D) == 20261029


def _play(c, H, body, pick=0, stop=None):
    s = c.post('/sessions', json=body, headers=H).json(); hands = []
    for i in range(s['size'] if stop is None else stop):
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
    assert d['status'] in ('won', 'tried') and d['result_fr'] and d['action'] is None and d['next_fr'] == 'Nouveau défi demain.'
    assert r['history'][0]['kind'] == 'daily' and r['history'][0]['won'] == (d['status'] == 'won')      # tentatives visibles aussi
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}, headers=A).status_code == 409       # une seule tentative
    assert client.post('/sessions', json={'mode': 'exploit', 'challenge': 'daily'}, headers=A).status_code == 409   # tous modes confondus
    _play(client, A, {'mode': 'gto', 'challenge': 'pressure'})
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['weekly'][0]['status'] != 'todo'
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'reader'}, headers=A).status_code == 422
    assert [x['kind'] for x in client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['weekly']] == ['pressure', 'range', 'reader']
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}).status_code == 400             # joueur identifié


def test_daily_abandoned_counts(client):
    """test joueurs 9 : une tentative abandonnée compte (le bouton ne revient pas, le serveur refuse la suivante)"""
    _play(client, A, {'mode': 'gto', 'challenge': 'daily'}, pick=0, stop=2)
    d = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['daily'][0]
    assert d['status'] == 'tried' and d['action'] is None and '3 sans réponse' in d['result_fr']
    assert client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['daily'][0]['action'] is None
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}, headers=A).status_code == 409


def test_perfect_on_session_theme(client):
    """test joueurs 9 : la série parfaite porte sur le thème de la séance du jour"""
    t = client.get('/users/me/today?mode=gto&tz=60', headers=A).json()
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    assert r['daily'][1]['theme_fr'] == t['theme_fr']
    s = client.post('/sessions', json={'mode': 'gto', 'challenge': 'perfect', 'tz': 60}, headers=A).json()
    from spinsacademy import quiz
    f = t['steps'][1]['filters']
    for i in range(s['size']):
        q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        sp = quiz.load(s['dataset_version'])[1][q['spot_id']]
        assert f.get('min_stack', 0) <= sp['effective_stack_bb'] <= f.get('max_stack', 99)
        client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']})


def test_reader_profiles():
    """test joueurs 9 : au moins 2 « Quelle pastille ? » dans le défi « Lecteur de vilain »"""
    from spinsacademy import field, quiz
    items = quiz.pool(quiz.DEFAULT_FIELD, {'family': 'read'})
    for seed in range(40):
        out = field.draw(items, 5, seed, min_profil=challenges.READER_PROFILES)
        types = [next(sp for sp in items if sp['spot_id'] == s)['field']['type'] for s, _ in out]
        assert types.count('profil') >= challenges.READER_PROFILES
