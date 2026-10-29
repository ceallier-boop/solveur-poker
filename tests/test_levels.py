"""niveaux du parcours et premier lancement (programme de travail, étape 4, 29/10/2026)"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import levels, quiz

H = {'X-Player-Id': 'l' * 20}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_level_scope():
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    sp = next(s for s in spots.values() if quiz.family(s) == 'first_in' and s['effective_stack_bb'] < 9.5)
    assert levels.in_level(1, sp) and not levels.in_level(2, sp)
    assert levels.fits(1, dict(family='vs_allin', min_stack=0, max_stack=9.5)) and not levels.fits(1, dict(hero='SB'))
    assert levels.fits(4, dict(hero='SB'))


def test_status_and_almost():
    st = levels.status(1, [], [], set())
    assert [c['kind'] for c in st['criteria']] == ['decisions', 'bb', 'ranges'] and not st['ready']
    assert levels.status(4, [], [], set())['final']
    near = dict(level=1, final=False, ready=False, criteria=[dict(kind='decisions', ok=False, value=80, target=100), dict(kind='bb', ok=True), dict(kind='ranges', ok=True)])
    assert levels.almost(near) == 'Plus que 20 décisions pour passer au niveau 2.'
    near['criteria'][0]['value'] = 10
    assert levels.almost(near) is None


def _series(c, filters=None):
    s = c.post('/sessions', json={'mode': 'gto', 'filters': filters or {}}, headers=H).json()
    for i in range(s['size']):
        q = c.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        c.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']})


def test_onboarding_and_level_api(client):
    lv = client.get('/users/me/level', headers=H).json()
    assert not lv['onboarded'] and lv['level'] == 1 and set(lv['experiences']) == {'debut', 'confirme', 'gros_volume'}
    lv = client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'ranges'}, headers=H).json()
    assert lv['onboarded'] and lv['level'] == 2 and lv['name'] == 'Le jeu à 10-16 BB'
    t = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    assert t['level']['number'] == 2 and '10 à 16 BB' in t['theme_fr']                            # la séance suit le niveau
    assert client.put('/users/me/level', json={'level': 1}, headers=H).json()['level'] == 1
    assert client.put('/users/me/level', json={'level': 4}, headers=H).status_code == 422
    assert client.get('/users/me/today?mode=exploit&tz=60', headers=H).json()['level']['number'] == 4
    assert client.get('/users/me/export', headers=H).json()['level']['level'] == 1


def test_existing_player_is_not_onboarded_again(client):
    _series(client)
    lv = client.get('/users/me/level', headers=H).json()
    assert lv['onboarded'] and lv['level'] == 1
