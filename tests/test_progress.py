import sqlite3
import pytest
from fastapi.testclient import TestClient
from spinsacademy import progress

ME = {'X-Player-Id': 'appareil-test-0001'}
OTHER = {'X-Player-Id': 'appareil-test-0002'}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'p.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def play(client, headers, seed, pick=0, size=5):
    sid = client.post('/sessions', json={'seed': seed, 'size': size}, headers=headers).json()['session_id']
    while True:
        q = client.get('/quiz/next', params={'session_id': sid}).json()
        if q['done']: return sid
        opts = q['question']['options']
        client.post('/attempts', json={'session_id': sid, 'question_index': q['question_index'], 'action_id': opts[pick % len(opts)]['id']})


def test_stats_after_several_series(client):
    for seed in range(4): play(client, ME, seed, pick=seed)
    s = client.get('/users/me/stats', headers=ME).json()
    assert s['sessions'] == 4 and s['questions'] == 20 and sum(s['verdicts'].values()) == 20
    assert 0 <= s['score_pct'] <= 100 and len(s['evolution']) == 4
    for dim in ('family', 'hero', 'table', 'depth'):
        assert sum(x['questions'] for x in s['by'][dim]) == 20
        for x in s['by'][dim]: assert x['reliable'] == (x['questions'] >= progress.MIN_SAMPLE)
    if s['weakest']: assert s['weakest']['reliable'] and s['weakest']['filters']
    for e in s['recurring_errors']: assert e['errors'] >= 2 and e['examples']


def test_players_are_isolated_and_anonymous_sessions_not_counted(client):
    play(client, ME, 1); play(client, OTHER, 2); play(client, {}, 3)
    assert client.get('/users/me/stats', headers=ME).json()['questions'] == 5
    assert client.get('/users/me/stats', headers=OTHER).json()['questions'] == 5
    assert client.get('/users/me/stats').status_code == 400
    assert client.get('/users/me/stats', headers={'X-Player-Id': "x'; drop"}).status_code == 400


def test_no_conclusion_on_small_samples(client):
    play(client, ME, 5, size=3)
    s = client.get('/users/me/stats', headers=ME).json()
    assert s['weakest'] is None and not any(x['reliable'] for v in s['by'].values() for x in v)


def test_export_and_delete(client):
    play(client, ME, 1); play(client, OTHER, 2)
    e = client.get('/users/me/export', headers=ME).json()
    assert len(e['sessions']) == 1 and len(e['answers']) == 5
    assert client.delete('/users/me', headers=ME).status_code == 204
    assert client.get('/users/me/stats', headers=ME).json()['questions'] == 0
    assert client.get('/users/me/stats', headers=OTHER).json()['questions'] == 5           # les autres joueurs ne sont pas touchés


def test_migration_of_older_database(tmp_path, monkeypatch):
    db = tmp_path / 'old.sqlite'
    con = sqlite3.connect(db)
    con.execute('CREATE TABLE sessions(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, dataset_version TEXT NOT NULL, filters TEXT NOT NULL, seed INTEGER, size INTEGER NOT NULL)')
    con.execute("INSERT INTO sessions VALUES ('ancienne', '2026-10-12T00:00:00+00:00', '2026.10.12-2', '{}', 1, 5)"); con.commit(); con.close()
    monkeypatch.setenv('SPINSACADEMY_DB', str(db))
    from spinsacademy.api import app
    c = TestClient(app)
    play(c, ME, 1)
    assert c.get('/users/me/stats', headers=ME).json()['questions'] == 5


def test_stats_split_by_mode(client):
    play(client, ME, 1)
    sid = client.post('/sessions', json={'mode': 'exploit', 'seed': 2}, headers=ME).json()['session_id']
    for i in range(5):
        client.get('/quiz/next', params={'session_id': sid})
        client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': 'F'})
    s = client.get('/users/me/stats', headers=ME).json()
    modes = {x['filters']['mode']: x['questions'] for x in s['by']['mode']}
    assert modes == {'gto': 5, 'exploit': 5}
    for e in s['recurring_errors']: assert e['filters']['mode'] in ('gto', 'exploit')
