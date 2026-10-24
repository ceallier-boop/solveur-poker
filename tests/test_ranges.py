"""chantiers 2 et 5 (24/10/2026) : exercice « Construis ta range », BB perdus pour 100 décisions"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import progress, quiz, ranges

H = {'X-Player-Id': 'r' * 32}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_range_task_and_grade():
    t = ranges.pick(quiz.DEFAULT_VERSION, {'table': 'heads-up', 'min_stack': 0, 'max_stack': 9.5}, seed=2)
    assert t and t['question_fr'].startswith('Avec quelles mains') and len(t['hands']) >= 20 and t['rule_fr'].startswith('À retenir')
    ref = [h for h, x in t['hands'].items() if x[0] >= 0.5]
    best, empty, full = ranges.grade(t, ref), ranges.grade(t, []), ranges.grade(t, list(t['hands']))
    assert best['accuracy_pct'] >= 99 and best['bb_per_100'] < 1                       # la référence ne perd presque rien
    assert empty['accuracy_pct'] < best['accuracy_pct'] and empty['bb_per_100'] > best['bb_per_100'] and empty['missing'] > 0
    assert full['extra'] > 0 and full['my_share_pct'] == 100
    assert set(best['cells'].values()) <= {'ok_in', 'ok_out', 'mixed'}
    assert all(w['cost_bb'] >= 0 and w['kind'] in ('extra', 'missing') for w in empty['worst'])
    assert abs(best['ref_share_pct'] - int(t['rule_fr'].split('environ ')[1].split(' %')[0])) <= 2    # même chiffre que « À retenir »


def test_range_api_stats_and_delete(client):
    t = client.get('/ranges/next?table=3-handed&family=vs_allin&seed=4').json()
    assert t['hands'] and isinstance(t['hands'], list) and 'rule_fr' not in t        # la référence reste sur le serveur
    g = client.post('/ranges/answer', json={'spot_id': t['spot_id'], 'hands': t['hands'][:10] + ['XXo']}, headers=H).json()
    assert 0 <= g['accuracy_pct'] <= 100 and g['reference'] and set(g['cells']) == set(t['hands'])
    st = client.get('/users/me/stats', headers=H).json()['ranges']
    assert st['count'] == 1 and st['accuracy_pct'] == g['accuracy_pct']
    assert client.get('/users/me/export', headers=H).json()['ranges']
    assert client.delete('/users/me', headers=H).status_code == 204 and client.get('/users/me/stats', headers=H).json()['ranges'] == {'count': 0}
    assert client.get('/ranges/next?family=read').status_code == 422


def test_bb_lost_per_100(client):
    s = client.post('/sessions', json={'mode': 'gto', 'seed': 3}, headers=H).json(); lost = 0
    for k in range(s['size']):
        q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        r = client.post('/attempts', json={'session_id': s['session_id'], 'question_index': k, 'action_id': q['options'][-1]['id']}).json()
        lost += r['regret_mbb']
    summ = client.get(f"/sessions/{s['session_id']}/summary").json()
    assert summ['ev_questions'] == s['size'] and abs(summ['bb_lost'] - lost / 1000) < 0.02
    st = client.get('/users/me/stats', headers=H).json()
    assert abs(st['bb_per_100'] - 100 * lost / 1000 / s['size']) < 0.02 and st['evolution'][-1]['bb_per_100'] == st['bb_per_100']
    assert all('bb_per_100' in row for rows in st['by'].values() for row in rows)
    b = progress._bucket(); assert progress.bb_per_100(b) is None
