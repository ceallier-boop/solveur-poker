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
    cap = g['items'][0]['max']                                                  # test joueurs 9 : jours restants dans la semaine
    assert [x['target'] for x in g['items']] == [min(goals.DEFAULT_NEW['days'], cap), goals.DEFAULT_BB, goals.DEFAULT_NEW['ranges']]   # nouveau joueur
    _series(client, 'theme')
    g = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()
    assert g['items'][0]['value'] == 1 and g['items'][1]['value'] is not None
    g = client.put('/users/me/goals', json={'mode': 'gto', 'kind': 'days', 'target': cap, 'tz': 60}, headers=H).json()
    assert g['items'][0]['target'] == cap and client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['items'][0]['target'] == cap
    assert client.put('/users/me/goals', json={'mode': 'gto', 'kind': 'days', 'target': cap + 1, 'tz': 60}, headers=H).status_code == 422   # plus que les jours restants
    # une série de la semaine dernière : le bilan s'affiche
    sid = _series(client, 'theme'); last = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat(timespec='seconds')
    con = sqlite3.connect(client.db); con.execute('UPDATE sessions SET created_at = ? WHERE id = ?', (last, sid))
    con.execute('UPDATE attempts SET answered_at = ? WHERE session_id = ?', (last, sid)); con.commit(); con.close()
    assert client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['last_week'] is None      # pas d'objectifs la semaine passée : pas de bilan
    con = sqlite3.connect(client.db); wk = con.execute('SELECT week FROM goals LIMIT 1').fetchone()[0]
    prev = (datetime.date.fromisoformat(wk) - datetime.timedelta(days=7)).isoformat()
    con.executemany('INSERT INTO goals(player_id, mode, week, kind, target, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                    [(H['X-Player-Id'], 'gto', prev, k, t, last) for k, t in (('days', 3), ('precision', 20), ('ranges', 1))]); con.commit(); con.close()
    lw = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()['last_week']
    assert lw and lw['days'] == 1 and lw['total'] == 3 and lw['decisions'] == 5
    assert client.get('/users/me/export', headers=H).json()['goals']
    assert client.delete('/users/me', headers=H).status_code == 204
