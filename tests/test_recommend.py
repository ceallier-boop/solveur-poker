"""recommandations de l'accueil (programme de travail, étape 2, 29/10/2026)"""
import datetime
import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz, ranges, recommend

H = {'X-Player-Id': 'r' * 20}
NOW = datetime.datetime(2026, 10, 29, 18, tzinfo=datetime.timezone.utc)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_priorities_and_two_at_most():
    late = [dict(due=True, due_at=(NOW - datetime.timedelta(days=3)).isoformat())]
    stats = dict(recurring_errors=[dict(label='GTO · Face à un tapis · BB · Moins de 10 BB', errors=5, questions=8, tight=4, loose=1,
                                        filters=dict(mode='gto', family='vs_allin', hero='BB', min_stack=0, max_stack=9.5))], by={})
    recs = recommend.build(stats, late, None, [], {}, NOW)
    assert [r['kind'] for r in recs] == ['review', 'theme'] and len(recs) == 2
    assert recs[1]['text_fr'].startswith('Face à un tapis · BB · Moins de 10 BB : 5 erreurs sur 8, le plus souvent en mettant moins de jetons')
    assert recs[1]['action'] == dict(type='series', filters=dict(family='vs_allin', hero='BB', min_stack=0, max_stack=9.5))
    # le thème déjà dans la séance n'est pas recommandé une deuxième fois
    assert [r['kind'] for r in recommend.build(stats, [], None, [], dict(family='vs_allin', hero='BB', min_stack=0, max_stack=9.5), NOW)] == ['discover']


def test_range_and_chrono_recommendations():
    v = quiz.DEFAULT_VERSION; t = ranges.pick(v, seed=1)
    last = dict(spot_id=t['spot_id'], hands=[], accuracy_pct=50.0, dataset_version=v)
    r = recommend.range_redo(last)
    assert r['kind'] == 'range' and 'trop serrée' in r['text_fr'] and r['action'] == dict(type='range', spot_id=t['spot_id'])
    rows = [dict(timed_out=1, answered_at=(NOW - datetime.timedelta(days=1)).isoformat())] * 3
    assert recommend.timeouts(rows, NOW)['action']['chrono'] == 15
    assert recommend.timeouts(rows[:1], NOW) is None


def test_api_recommendations_range_by_spot_and_conseil_key(client):
    r = client.get('/users/me/recommendations?mode=gto&tz=60', headers=H).json()
    assert [x['kind'] for x in r['items']] == ['discover']                 # nouveau joueur : une découverte, pas le thème de la séance
    t = ranges.pick(quiz.DEFAULT_VERSION, seed=3)
    assert client.get('/ranges/next', params=dict(spot=t['spot_id'])).json()['spot_id'] == t['spot_id']
    s = client.post('/sessions', json={'mode': 'gto'}, headers=H).json()
    q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
    assert q['node_key'] == quiz.load(quiz.DEFAULT_VERSION)[1][q['spot_id']]['node_key']
