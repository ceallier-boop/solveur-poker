import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz

ME = {'X-Player-Id': 'appareil-test-0001'}
ADMIN = {'X-Admin-Token': 'jeton-de-test'}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'r.sqlite'))
    monkeypatch.setenv('SPINSACADEMY_ADMIN_TOKEN', ADMIN['X-Admin-Token'])
    from spinsacademy.api import app
    return TestClient(app)


def answered(client, mode='gto', seed=1):
    """session d'une question, répondue ; renvoie (session_id, spot_id)"""
    sid = client.post('/sessions', json={'mode': mode, 'seed': seed, 'size': 1}, headers=ME).json()['session_id']
    q = client.get('/quiz/next', params={'session_id': sid}).json()
    client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': q['question']['options'][0]['id']})
    return sid, q['question']['spot_id']


def test_report_flow_and_duplicates(client):
    sid = client.post('/sessions', json={'seed': 1, 'size': 2}, headers=ME).json()['session_id']
    client.get('/quiz/next', params={'session_id': sid})
    assert client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'unclear'}).status_code == 409   # pas encore répondue
    q = client.get('/quiz/next', params={'session_id': sid}).json()
    client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': q['question']['options'][0]['id']})
    r = client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'wrong_answer', 'comment': '  le call me semble meilleur '}, headers=ME)
    assert r.status_code == 201 and r.json()['status'] == 'open'
    assert client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'other'}).status_code == 409
    assert client.post('/reports', json={'session_id': sid, 'question_index': 1, 'reason': 'bidon'}).status_code == 422
    assert client.post('/reports', json={'session_id': 'inconnue', 'question_index': 0, 'reason': 'other'}).status_code == 404
    rows = client.get('/admin/reports', headers=ADMIN).json()
    assert len(rows) == 1 and rows[0]['comment'] == 'le call me semble meilleur' and rows[0]['player_id'] == ME['X-Player-Id']
    assert rows[0]['reason_fr'] and rows[0]['prompt_fr'] and rows[0]['reports_on_spot'] == 1


def test_admin_requires_token(client, monkeypatch):
    for path in ('/admin/reports', '/admin/disabled', '/admin/log'):
        assert client.get(path).status_code == 403
        assert client.get(path, headers={'X-Admin-Token': 'mauvais'}).status_code == 403
    monkeypatch.delenv('SPINSACADEMY_ADMIN_TOKEN')
    assert client.get('/admin/reports', headers=ADMIN).status_code == 403                   # sans jeton configuré, l'administration est fermée


def test_disable_spot_excludes_it_from_draws_then_enable(client):
    sid, spot = answered(client)
    rid = client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'wrong_answer'}).json()['report_id']
    res = client.post(f'/admin/reports/{rid}/resolve', json={'status': 'accepted', 'resolution': 'EV HRC bruitée', 'disable_spot': True, 'actor': 'expert'}, headers=ADMIN)
    assert res.status_code == 200 and res.json()['disabled_spot'] == spot
    assert client.post(f'/admin/reports/{rid}/resolve', json={'status': 'rejected', 'resolution': 'bis'}, headers=ADMIN).status_code == 409
    assert client.get('/admin/reports', headers=ADMIN).json() == []
    assert [d['spot_id'] for d in client.get('/admin/disabled', headers=ADMIN).json()] == [spot]
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    for seed in range(30):                                                                    # le tirage de l'API ne propose plus ce spot
        series = quiz.draw_series(quiz.DEFAULT_VERSION, None, 20, seed, frozenset([spot]))
        assert spot not in {s for s, _ in series}
    s2 = client.post('/sessions', json={'seed': 1, 'size': 1}, headers=ME).json()['session_id']
    assert client.get('/quiz/next', params={'session_id': s2}).json()['question']['spot_id'] != spot
    assert client.delete(f'/admin/disabled/{spot}', params={'reason': 'corrigé', 'actor': 'expert'}, headers=ADMIN).status_code == 200
    assert client.delete(f'/admin/disabled/{spot}', params={'reason': 'bis'}, headers=ADMIN).status_code == 404
    s3 = client.post('/sessions', json={'seed': 1, 'size': 1}, headers=ME).json()['session_id']
    assert client.get('/quiz/next', params={'session_id': s3}).json()['question']['spot_id'] == spot   # même graine : le spot revient
    log = client.get('/admin/log', headers=ADMIN).json()
    assert [e['action'] for e in log] == ['resolve_report', 'enable_spot'] and log[0]['actor'] == 'expert' and log[0]['details']['disabled_spot'] == spot


def test_disabled_gto_spot_excludes_derived_exploit_spots():
    _, spots = quiz.load(quiz.DEFAULT_EXPLOIT)
    base = next(sp['base_spot_id'] for sp in spots.values() if sp.get('adaptations', 0) > 0)
    for seed in range(10):
        series = quiz.draw_series(quiz.DEFAULT_EXPLOIT, None, 10, seed, frozenset([base]))
        assert all(spots[s]['base_spot_id'] != base for s, _ in series)


def test_rejected_report_keeps_spot(client):
    sid, spot = answered(client, mode='exploit')
    rid = client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'illegal_action'}).json()['report_id']
    client.post(f'/admin/reports/{rid}/resolve', json={'status': 'rejected', 'resolution': 'action légale'}, headers=ADMIN)
    assert client.get('/admin/disabled', headers=ADMIN).json() == []
    assert client.get('/admin/reports', params={'status': 'rejected'}, headers=ADMIN).json()[0]['resolution'] == 'action légale'
