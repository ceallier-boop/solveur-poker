import pytest
from fastapi.testclient import TestClient
from spinsacademy import adaptive, grading, quiz

ME = {'X-Player-Id': 'appareil-adapt-0001'}
THEME = ('vs_allin', 'BB', '10_16')
THEME_FILTERS = dict(family='vs_allin', hero='BB', min_stack=9.5, max_stack=16.5)


def rows_for(theme, verdicts):
    sps = [sp for sp in quiz.pool(quiz.DEFAULT_VERSION) if adaptive.theme_of(sp) == theme]
    return [dict(dataset_version=quiz.DEFAULT_VERSION, spot_id=sps[i % len(sps)]['spot_id'], verdict=v, answered_at=f'2026-10-13T00:00:{i:02d}')
            for i, v in enumerate(verdicts)]


@pytest.mark.slow
def test_thresholds_do_not_conclude_on_few_answers():
    avail = {adaptive.theme_of(sp) for sp in quiz.pool(quiz.DEFAULT_VERSION)}
    assert not adaptive.plan(rows_for(THEME, ['erreur', 'erreur']), avail, 5, 1)['active']                 # 2 réponses : pas de conclusion
    p = adaptive.plan(rows_for(THEME, ['erreur', 'erreur', 'correct']), avail, 5, 1)
    assert p['active'] and [w['theme'] for w in p['weak']] == [list(THEME)]
    assert not adaptive.plan(rows_for(THEME, ['erreur', 'erreur'] + ['correct'] * 6), avail, 5, 1)['active']   # 2 erreurs sur 8 : acquis en cours


def test_composition_weak_review_discovery():
    avail = {adaptive.theme_of(sp) for sp in quiz.pool(quiz.DEFAULT_VERSION)}
    other = next(t for t in sorted(avail) if t != THEME)
    rows = rows_for(THEME, ['erreur'] * 3) + rows_for(other, ['correct'] * 6)
    p = adaptive.plan(rows, avail, 5, 2); kinds = [s['kind'] for s in p['slots']]
    assert kinds.count('weak') == 3 and kinds.count('review') == 1 and kinds.count('discovery') == 1
    assert all(tuple(s['theme']) == THEME for s in p['slots'] if s['kind'] == 'weak')
    assert all(s['theme'] is None or tuple(s['theme']) not in (THEME, other) for s in p['slots'] if s['kind'] == 'discovery')
    drawn = quiz.draw_plan(quiz.DEFAULT_VERSION, p['slots'], adaptive.theme_of, 2)
    _, spots = quiz.load()
    assert len({s for s, *_ in drawn}) == 5 and all(ok and adaptive.theme_of(spots[s]) == tuple(slot['theme']) for s, h, slot, ok in drawn if slot['kind'] == 'weak')


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'a.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def worst(q):
    _, spots = quiz.load(); sp = spots[q['spot_id']]; ev = grading.reference_ev(sp, q['hand'])
    return min(sp['actions'], key=lambda a: ev[[x['id'] for x in sp['actions']].index(a['id'])])['id']


def play(c, body, pick=worst):
    sid = c.post('/sessions', json=body, headers=ME).json()['session_id']; got = []
    while True:
        q = c.get('/quiz/next', params={'session_id': sid}).json()
        if q['done']: return sid, got
        got.append(q); c.post('/attempts', json={'session_id': sid, 'question_index': q['question_index'], 'action_id': pick(q['question'])})


def test_api_targets_weak_theme_and_respects_preferences(client):
    s0 = client.post('/sessions', json={'seed': 1}, headers=ME).json()
    assert s0['adaptive']['active'] is False and 'Pas encore' in s0['adaptive']['reason_fr']
    play(client, {'seed': 5, 'filters': THEME_FILTERS})                                       # 5 erreurs sur ce thème (filtres : pas d'adaptation)
    a = client.get('/users/me/adaptation', headers=ME).json()
    assert a['active'] and a['weak'][0]['theme'] == list(THEME) and a['weak'][0]['errors'] >= 3
    _, qs = play(client, {'seed': 7}, pick=lambda q: q['options'][0]['id'])
    weak = [q for q in qs if q['purpose'] == 'weak']
    assert len(weak) == 3 and all(adaptive.label(THEME) in q['purpose_fr'] for q in weak)
    _, spots = quiz.load()
    assert all(adaptive.theme_of(spots[q['question']['spot_id']]) == THEME for q in weak)
    _, qs = play(client, {'seed': 7, 'adaptive': False}); assert all(q['purpose'] is None for q in qs)
    assert client.put('/users/me/preferences', json={'adaptive': False}, headers=ME).json()['adaptive'] is False
    _, qs = play(client, {'seed': 8}); assert all(q['purpose'] is None for q in qs)
    client.put('/users/me/preferences', json={'adaptive': True}, headers=ME)
    r = client.post('/users/me/adaptation/reset', headers=ME).json(); assert r['adaptation_reset_at']
    assert client.get('/users/me/adaptation', headers=ME).json()['active'] is False                 # repart de zéro
    assert client.get('/users/me/stats', headers=ME).json()['questions'] == 20                      # l'historique est conservé
    assert client.get('/users/me/export', headers=ME).json()['preferences']['adaptation_reset_at'] == r['adaptation_reset_at']
    client.delete('/users/me', headers=ME)
    assert client.get('/users/me/preferences', headers=ME).json() == {'adaptive': True, 'adaptation_reset_at': None}


def test_correction_is_unchanged_by_adaptation(client):
    play(client, {'seed': 5, 'filters': THEME_FILTERS})
    sid, qs = play(client, {'seed': 9}, pick=lambda q: q['options'][0]['id'])
    summ = client.get(f'/sessions/{sid}/summary').json()
    for q in qs:
        r = client.post('/attempts', json={'session_id': sid, 'question_index': q['question_index'], 'action_id': q['question']['options'][0]['id']}).json()
        assert r == dict(quiz.correct(quiz.DEFAULT_VERSION, q['question']['spot_id'], q['question']['hand'], q['question']['options'][0]['id']), already_answered=True)
    assert summ['complete']
