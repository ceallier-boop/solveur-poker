import datetime
import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz, review

H = {'X-Player-Id': 'a' * 32}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _spot_hand():
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    for sid, sp in spots.items():
        hs = sorted(quiz.teachable(sp))
        if hs: return sid, hs[0]


def test_schedule_1_3_7():
    sid, h = _spot_hand(); t0 = datetime.datetime(2026, 10, 1, tzinfo=datetime.timezone.utc)
    at = lambda d: (t0 + datetime.timedelta(days=d)).isoformat()
    row = lambda d, v: dict(spot_id=sid, hand=h, verdict=v, answered_at=at(d))
    it = review.items([row(0, 'erreur')], quiz.DEFAULT_VERSION, t0 + datetime.timedelta(hours=12))
    assert len(it) == 1 and not it[0]['due'] and it[0]['stage'] == 1
    assert review.items([row(0, 'erreur')], quiz.DEFAULT_VERSION, t0 + datetime.timedelta(days=1))[0]['due']
    rows = [row(0, 'erreur'), row(1, 'correct')]                       # réussite à J+1 : prochaine à 3 jours
    it = review.items(rows, quiz.DEFAULT_VERSION, t0 + datetime.timedelta(days=2))[0]
    assert it['stage'] == 2 and not it['due']
    rows += [row(4, 'correct'), row(11, 'correct')]                    # J+3 puis J+7 : acquise
    assert review.items(rows, quiz.DEFAULT_VERSION, t0 + datetime.timedelta(days=30)) == []
    rows = [row(0, 'erreur'), row(1, 'correct'), row(2, 'imprécision')] # nouvelle erreur : retour à l'étape 1
    assert review.items(rows, quiz.DEFAULT_VERSION, t0 + datetime.timedelta(days=2))[0]['stage'] == 1
    early = [row(0, 'erreur'), row(0.5, 'correct')]                    # réussite avant l'échéance : rien ne change
    assert review.items(early, quiz.DEFAULT_VERSION, t0 + datetime.timedelta(days=1))[0]['stage'] == 1


def test_review_session_api(client, monkeypatch):
    assert client.get('/users/me/reviews').status_code in (400, 401, 422)
    assert client.get('/users/me/reviews', headers=H).json()['due'] == 0
    sid = client.post('/sessions', json={'seed': 2, 'adaptive': False}, headers=H).json()['session_id']
    missed = []
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][i % len(q['options'])]['id']}).json()
        if a['verdict'] != 'correct': missed.append((q['spot_id'], q['hand']))
    later = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)
    real = review.summary
    monkeypatch.setattr(review, 'summary', lambda rows, v, now=None: real(rows, v, later))
    r = client.get('/users/me/reviews', headers=H).json()
    assert r['due'] == len(set(missed)) and r['rule_fr']
    s = client.post('/sessions', json={'review': True, 'seed': 4}, headers=H).json()
    assert s['size'] == 5
    first = client.get('/quiz/next', params={'session_id': s['session_id']}).json()
    assert missed                                                      # graine choisie pour avoir au moins une erreur
    if missed:
        assert first['purpose'] == 'spaced' and first['purpose_fr'].startswith('Révision de ton erreur du')
        assert (first['question']['spot_id'], first['question']['hand']) in missed
