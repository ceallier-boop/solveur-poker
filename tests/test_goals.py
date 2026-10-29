"""objectifs de la semaine (programme de travail, étape 3, 29/10/2026)"""
import datetime, sqlite3
import pytest
from fastapi.testclient import TestClient
from spinsacademy import goals

H = {'X-Player-Id': 'g' * 20}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = tmp_path / 'test.sqlite'; monkeypatch.setenv('SPINSACADEMY_DB', str(db))
    from spinsacademy.api import app
    c = TestClient(app); c.db = str(db); return c


def test_week_and_proposals():
    assert goals.week_start(datetime.date(2026, 10, 29)) == datetime.date(2026, 10, 26)            # jeudi -> lundi
    assert goals.propose({}, None, []) == dict(days=5, ranges=3, precision=goals.DEFAULT_BB)
    assert goals.propose({}, None, [], new=True) == dict(days=3, ranges=1, precision=goals.DEFAULT_BB)        # test joueurs 9 : nouveau joueur
    assert goals.propose({}, None, [], days_cap=2)['days'] == 2                                                # jamais plus que les jours restants
    thu = datetime.date(2026, 10, 29)
    assert goals.days_cap(dict(days=0), thu) == 4 and goals.days_cap(dict(days=2), thu) == 6 and goals.days_cap(dict(days=0), datetime.date(2026, 11, 1)) == 1
    assert goals.days_cap(dict(days=1, day_set={thu}), thu) == 4                                               # aujourd'hui déjà compté
    missed = dict(days=2, ranges=0, precision=None, decisions=10)
    assert goals.propose(dict(days=5, ranges=3, precision=12), missed, []) == dict(days=4, ranges=2, precision=goals.DEFAULT_BB)   # reconduits plus faciles
    kept = dict(days=6, ranges=4, precision=9.0, decisions=80)
    assert goals.propose(dict(days=5, ranges=3, precision=12), kept, [10.0, 12.0]) == dict(days=5, ranges=3, precision=10.0)  # moyenne - 10 %


def test_precision_needs_enough_decisions():
    assert not goals.done('precision', 20, dict(precision=10.0, decisions=12))
    assert goals.done('precision', 20, dict(precision=10.0, decisions=40))
    v = goals.view(dict(days=5, precision=20, ranges=3), dict(days=2, precision=10.0, decisions=12, ranges=3))
    assert [x['done'] for x in v] == [False, False, True] and 'au moins 30 décisions' in v[1]['text_fr']


def _series(c, plan):
    s = c.post('/sessions', json={'mode': 'gto', 'plan': plan}, headers=H).json()
    for i in range(s['size']):
        q = c.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        c.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']})
    return s['session_id']


def test_goals_api(client):
    g = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()
    assert [x['kind'] for x in g['items']] == ['days', 'precision', 'ranges'] and g['last_week'] is None
    day = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
    assert [x['target'] for x in g['items']] == [min(3, 7 - day.weekday()), goals.DEFAULT_BB, 1]          # nouveau joueur : cibles basses
    assert g['items'][0]['max'] == 7 - day.weekday()
    _series(client, 'theme')
    g = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()
    assert g['items'][0]['value'] == 1 and g['items'][1]['value'] is not None
    g = client.put('/users/me/goals', json={'mode': 'gto', 'kind': 'days', 'target': 3, 'tz': 60}, headers=H).json()
    assert g['items'][0]['target'] == 3 and client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['items'][0]['target'] == 3
    assert client.put('/users/me/goals', json={'mode': 'gto', 'kind': 'days', 'target': 9}, headers=H).status_code == 422
    if day.weekday() > 0:                                                                                    # plus de séances que de jours restants
        assert client.put('/users/me/goals', json={'mode': 'gto', 'kind': 'days', 'target': 7, 'tz': 60}, headers=H).status_code == 422
    # une série de la semaine dernière : le bilan s'affiche
    sid = _series(client, 'theme'); last = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat(timespec='seconds')
    con = sqlite3.connect(client.db); con.execute('UPDATE sessions SET created_at = ? WHERE id = ?', (last, sid))
    con.execute('UPDATE attempts SET answered_at = ? WHERE session_id = ?', (last, sid)); con.commit(); con.close()
    assert client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['last_week'] is None              # pas d'objectifs cette semaine-là
    con = sqlite3.connect(client.db)
    week = (datetime.date.fromisoformat(client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['week']) - datetime.timedelta(days=7)).isoformat()
    con.execute("INSERT INTO goals(player_id, mode, week, kind, target, updated_at) VALUES (?, 'gto', ?, 'days', 5, '2026-01-01')", (H['X-Player-Id'], week)); con.commit(); con.close()
    lw = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['last_week']
    assert lw and lw['days'] == 1 and lw['total'] == 3 and lw['decisions'] == 5
    assert client.get('/users/me/export', headers=H).json()['goals']
    assert client.delete('/users/me', headers=H).status_code == 204
