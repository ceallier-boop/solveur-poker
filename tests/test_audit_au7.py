"""Audit AU7 (06/11/2026) : test de placement de 10 mains"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import levels, quiz

H = {'X-Player-Id': 'c' * 20}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _play(client, mode):
    """joue les 10 mains : 'best' = une réponse correcte quand il y en a une, 'worst' = une erreur quand il y en a une"""
    s = client.post('/sessions', json={'mode': 'gto', 'plan': 'placement'}, headers=H)
    assert s.status_code == 201, s.text
    s = s.json(); assert s['size'] == 10
    effs = []; ver = s['dataset_version']; _, spots = quiz.load(ver)
    for i in range(10):
        q = client.get(f"/quiz/next?session_id={s['session_id']}", headers=H).json()['question']
        effs.append(spots[q['spot_id']]['effective_stack_bb'])          # comme le serveur (levels) : tapis effectif, pas le plus petit de la table
        v = {o['id']: quiz.correct(ver, q['spot_id'], q['hand'], o['id'])['verdict'] for o in q['options']}
        want = 'correct' if mode == 'best' else 'erreur'
        pick = next((a for a, x in v.items() if x == want), q['options'][0]['id'])
        client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': pick}, headers=H)
    return s['session_id'], effs


def test_placement_series_covers_the_three_depths(client):
    client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'bases'}, headers=H)
    sid, effs = _play(client, 'best')
    n = [sum(1 for e in effs if levels.LEVELS[lv]['depth'][0] <= e < levels.LEVELS[lv]['depth'][1]) for lv in (1, 2, 3)]
    assert n == [4, 3, 3], effs


def test_good_player_is_proposed_level_3_and_weak_player_level_1(client):
    client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'bases'}, headers=H)
    sid, _ = _play(client, 'best'); r = client.get(f'/users/me/placement?session_id={sid}', headers=H).json()
    assert r['complete'] and r['proposed_level'] == 3 and r['current_level'] == 2 and 'Niveau proposé : 3' in r['text_fr']
    assert [b['questions'] for b in r['bands']] == [4, 3, 3]
    sid, _ = _play(client, 'worst'); r = client.get(f'/users/me/placement?session_id={sid}', headers=H).json()
    assert r['proposed_level'] == 1 and r['current_level'] == 2           # la proposition ne change rien tant que le joueur ne valide pas
    assert client.put('/users/me/level', json={'level': r['proposed_level']}, headers=H).json()['level'] == 1


def test_placement_is_not_counted_in_the_progress(client):
    client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'bases'}, headers=H)
    _play(client, 'worst')
    assert client.get('/users/me/stats', headers=H).json()['questions'] == 0


def test_placement_needs_a_player_and_the_gto_mode(client):
    assert client.post('/sessions', json={'mode': 'gto', 'plan': 'placement'}).status_code == 400
    assert client.post('/sessions', json={'mode': 'exploit', 'plan': 'placement'}, headers=H).status_code == 422
    assert client.get('/users/me/placement?session_id=inconnue', headers=H).status_code == 404


def test_placement_rule_thresholds():
    r = levels.placement_result([(4, 1), (4, 1), (4, 1), (4, 0), (12, 1), (12, 0), (12, 1), (20, 1), (20, 1), (20, 1)])
    assert r['proposed_level'] == 3 and r['complete']
    r = levels.placement_result([(4, 1), (4, 1), (4, 0), (4, 0), (12, 1), (12, 1), (12, 1), (20, 1), (20, 1), (20, 1)])
    assert r['proposed_level'] == 1                                         # 2 sur 4 à moins de 10 BB : on ne monte pas, même si la suite est réussie
    r = levels.placement_result([(4, 1), (4, 1), (4, 1), (4, 1), (12, 1), (12, 0), (12, 0), (20, 1), (20, 1), (20, 1)])
    assert r['proposed_level'] == 2
    assert not levels.placement_result([(4, 1)])['complete']
