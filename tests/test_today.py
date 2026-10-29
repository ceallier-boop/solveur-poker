"""séance du jour (programme de travail, étape 1, 29/10/2026)"""
import datetime
import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz, ranges, today

H = {'X-Player-Id': 'd' * 32}
D = datetime.date(2026, 10, 29)
back = lambda k: D - datetime.timedelta(days=k)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_streak_forgives_one_day_a_week():
    assert today.streak(set(), D) == 0
    assert today.streak({back(0), back(1), back(2)}, D) == 3
    assert today.streak({back(1), back(2)}, D) == 2                      # aujourd'hui pas encore joué : la série tient
    assert today.streak({back(0), back(2), back(3)}, D) == 3             # un jour manqué pardonné
    assert today.streak({back(0), back(2), back(4)}, D) == 2             # deux dans la même semaine : la série s'arrête


def test_local_day_follows_player_timezone():
    assert today.local_day('2026-10-29T23:30:00+00:00', 60) == datetime.date(2026, 10, 30)
    assert today.local_day('2026-10-29T23:30:00+00:00', 0) == datetime.date(2026, 10, 29)


def test_newcomer_starts_with_short_stacks():
    t = today.build([], [], 0, None, D, 0)
    assert t['steps'][1]['label_fr'] == 'Thème : ' + today.THEMES[0][0] and t['next'] == 1 and t['steps'][0]['done']
    assert not t['started'] and not t['done'] and t['streak'] == 0


def _series(client, filters, plan):
    s = client.post('/sessions', json={'mode': 'gto', 'filters': filters, 'plan': plan}, headers=H).json()
    for i in range(s['size']):
        q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']})


def test_today_flow(client):
    t = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    assert t['minutes'] == 15 and [s['kind'] for s in t['steps']] == ['review', 'theme', 'range'] and t['next'] == 1
    theme = t['steps'][1]
    assert ranges.pick(quiz.DEFAULT_VERSION, t['steps'][2]['filters'] or None, seed=0)       # une range existe pour l'étape 3
    _series(client, theme['filters'], 'theme')
    t = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    assert t['started'] and t['steps'][1]['count'] == 1 and not t['steps'][1]['done'] and t['streak'] == 1
    assert t['steps'][1]['label_fr'] == theme['label_fr']                                    # même thème toute la journée
    _series(client, theme['filters'], 'theme')
    r = client.get('/ranges/next', params=t['steps'][2]['filters']).json()
    client.post('/ranges/answer', json={'spot_id': r['spot_id'], 'hands': r['hands'][:5]}, headers=H)
    t = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    assert t['done'] and t['next'] is None and all(s['done'] for s in t['steps']) and t['bb7'] is not None
    assert client.post('/sessions', json={'mode': 'gto', 'plan': 'autre'}, headers=H).status_code == 422
    assert client.get('/users/me/today?mode=poker', headers=H).status_code == 422
