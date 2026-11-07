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
    assert r['history'] and r['history'][0]['won'] == (d['status'] == 'won')                            # l'historique garde aussi les tentatives perdues
    _play(client, A, {'mode': 'gto', 'challenge': 'pressure'})
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['weekly'][0]['status'] != 'todo'
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'reader'}, headers=A).status_code == 422
    assert [x['kind'] for x in client.get('/users/me/challenges?mode=exploit&tz=60', headers=A).json()['weekly']] == ['pressure', 'range', 'reader']
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}).status_code == 400             # joueur identifié


def test_daily_concurrent_launches(client):
    """deux lancements simultanés du défi du jour : un seul passe (le second reçoit 409)"""
    import threading
    client.get('/users/me/today?mode=gto&tz=60', headers=A)
    codes = []
    ts = [threading.Thread(target=lambda: codes.append(client.post('/sessions', json={'mode': 'gto', 'challenge': 'daily'}, headers=A).status_code)) for _ in range(6)]
    for t in ts: t.start()
    for t in ts: t.join()
    assert sorted(codes) == [201, 409, 409, 409, 409, 409]


def test_ad_zone_off_everything_open(client):
    """drapeau éteint (test fermé, défaut) : rien de verrouillé, pas de déblocage"""
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    assert r['ad_zone']['enabled'] is False and r['ad_zone']['open'] is True
    assert not any(c.get('locked') for c in r['daily'] + r['weekly'])
    assert {c['kind'] for c in r['daily'] + r['weekly'] if c.get('zone') == 'ad'} == {'perfect', 'range'}
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'perfect', 'tz': 60}, headers=A).status_code == 201
    assert client.post('/users/me/challenges/unlock', json={'tz': 60, 'source': 'watched'}, headers=A).status_code == 409


def test_ad_zone_on_locked_until_unlock(client, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_AD_CHALLENGES', '1')
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    z = r['ad_zone']; locked = [c for c in r['daily'] + r['weekly'] if c.get('locked')]
    assert z['enabled'] and not z['open'] and z['button_fr'] and z['fallback_fr']
    assert {c['kind'] for c in locked} == {'perfect', 'range'} and all(c['action'] is None for c in locked)
    assert not any(c.get('locked') for c in r['daily'] + r['weekly'] if c['kind'] in ('daily', 'pressure'))   # gratuits
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'perfect', 'tz': 60}, headers=A).status_code == 403
    assert client.post('/users/me/challenges/unlock', json={'tz': 60, 'source': 'blocked'}, headers=A).status_code == 422   # repli : la page n'ouvre pas
    assert client.post('/users/me/challenges/unlock', json={'tz': 60, 'source': 'no_fill'}, headers=A).json()['open'] is True
    r = client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()
    assert r['ad_zone']['open'] and not any(c.get('locked') for c in r['daily'] + r['weekly'])
    assert client.post('/sessions', json={'mode': 'gto', 'challenge': 'perfect', 'tz': 60}, headers=A).status_code == 201
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=B).json()['ad_zone']['open'] is False     # par joueur
    assert client.get('/users/me/export', headers=A).json()['ad_unlocks'][0]['source'] == 'no_fill'
    client.delete('/users/me', headers=A)
    assert client.get('/users/me/challenges?mode=gto&tz=60', headers=A).json()['ad_zone']['open'] is False     # effacé avec le reste


def test_ad_zone_range_counts_only_open_days():
    """Range au cordeau verrouillé : une range réussie un jour fermé (jeu libre) ne valide pas le défi"""
    good = dict(answered_at=datetime.datetime(D.year, D.month, D.day, 10, tzinfo=datetime.timezone.utc).isoformat(), bb_per_100=1.0, accuracy_pct=90)
    rng = lambda days: next(c for c in challenges.build([], [good], set(), D, 0, 'gto', D, ad_open_days=days)['weekly'] if c['kind'] == 'range')
    assert rng(None)['status'] == 'won'                       # zone éteinte : compté comme avant
    assert rng(set())['status'] == 'todo' and rng(set())['locked']
    assert rng({D})['status'] == 'won' and not rng({D}).get('locked')
