"""Classe de questions « Équités » (CE3) : exactitude des tranches, marge, notation, séparation des modes, API."""
import datetime, json
import pytest
from fastapi.testclient import TestClient
from spinsacademy import equities, equity_quiz as E, progress, quiz
from spinsacademy.cards import NAMES


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _many(levels=(1, 2), seeds=range(25), kinds=(None, 'hit', 'equity', 'labels')):
    for lv in levels:
        for sd in seeds:
            for k in kinds:
                yield lv, E.draw(lv, 5, seed=sd, kind=k)


def test_correct_band_contains_exact_value_with_margin():
    n = 0
    for lv, series in _many():
        for sid, h in series:
            b = E._built(sid, h)
            if b['kind'] == 'labels' or b['kind'] in E.BOARD_KINDS: continue      # sortes avec tableau : tests/test_equity_board.py
            v = b['value'] / 100; f = b['f']; c = b['correct']
            lo = f[c - 1] if c > 0 else 0; hi = f[c] if c < len(f) else 100
            assert lo <= v < hi or (hi == 100 and v == 100)                    # la bonne tranche contient la valeur exacte
            assert all(abs(v - x) >= E.MARGIN for x in f)                        # jamais à moins de 1,5 point d'une frontière
            assert all(0 < x < 100 for x in f) and f == sorted(f)
            assert len(f) + 1 in ((4,) if lv == 1 else (5, 6))
            assert b['value'] == E.topic_value(b['kind'], b['topic'], h)        # valeur lue dans la table, sans arrondi
            n += 1
    assert n > 200


def test_values_come_from_the_table():
    assert E.topic_value('hit', 'au_moins_paire', '98s') == equities.hit_chances('98s')['au_moins_paire']
    assert E.topic_value('hit', 'couleur', 'AKs') == equities.hit_chances('AKs')['couleur'] + equities.hit_chances('AKs')['quinte_flush']
    assert E.topic_value('equity', 'hasard', 'AA') == 8520
    assert E.topic_value('equity', 'hu8_sb_tapis', 'QTo') == equities.equity_vs_range('QTo', 'hu8_sb_tapis')
    assert E.topic_value('hit', 'au_moins_paire', 'QQ') is None                   # une paire de poche a déjà sa paire : sujet écarté
    assert E.topic_value('hit', 'couleur', 'AKo') is None                         # dépareillée : pas de couleur au flop


def test_grading_full_half_zero():
    sid = E.spot_id_bands('hit', 'au_moins_paire', 2, 5, 6, 2)                  # 72o : 32,43 % -> tranche « de 30 à 35 % » en 3e position
    b = E._built(sid, '72o'); assert b['options'][2] == 'de 30 à 35 %' and b['f'] == [25, 30, 35, 40, 45]
    assert not E.valid(sid, '98s')                                              # 98s : 34,56 %, à moins de 1,5 point de la frontière 35 %
    got = {a: E.correct(sid, '72o', a) for a in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5')}
    assert [got[a]['verdict'] for a in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5')] == ['erreur', 'imprécision', 'correct', 'imprécision', 'erreur', 'erreur']
    assert [got[a]['points'] for a in ('b1', 'b2', 'b4')] == [0.5, 1.0, 0.0]
    r = got['b2']
    assert r['regret_mbb'] == 0 and r['loss_fr'] is None                        # pas de BB perdus
    assert r['equity']['value_fr'] == '32,4 %' and '19\u202f600 flops' in r['method_fr']
    assert not r['strengths_fr'] and 'Dépareillée' in r['weaknesses_fr'][0]
    with pytest.raises(ValueError): E.correct(sid, '72o', 'b9')
    with pytest.raises(ValueError): E.question(sid, 'AA')                         # main incompatible avec l'identifiant


def test_labels_one_answer_and_clear():
    for lv, series in _many(seeds=range(40), kinds=('labels',)):
        for sid, h in series:
            b = E._built(sid, h); q = E.parse(sid)
            want = q['mode'] == 'vraie'
            assert b['clarity'].count(want) == 1 and None not in b['clarity']
            assert lv == 2 or (q['mode'] == 'vraie' and set(q['ids']) <= set(E.LEVEL1_LABELS))
            labs = {l['id'] for l in equities.labels(h)}
            for i, c in zip(q['ids'], b['clarity']): assert (i in labs) == c   # « nettement vrai » : la table le dit aussi
            r = E.correct(sid, h, f"o{b['correct']}"); assert r['verdict'] == 'correct' and r['points'] == 1
            other = next(f'o{i}' for i in range(4) if i != b['correct'])
            assert E.correct(sid, h, other)['verdict'] == 'erreur'


def test_clarity_agrees_with_table_for_every_hand():
    for h in NAMES:
        labs = {l['id'] for l in equities.labels(h)}
        for i in E.label_defs():
            c = E.clarity(i, h)
            if c is not None: assert (i in labs) == c, (h, i)
        assert (E.domination(h) >= 3000) == ('dominee' in labs)


def test_level1_plain_words():
    for lv, series in _many(levels=(1,), seeds=range(30)):
        for sid, h in series:
            q = E.question(sid, h); r = E.correct(sid, h, q['options'][0]['id'])
            text = q['prompt_fr'] + ' '.join(o['label_fr'] for o in q['options']) + r['explanation_fr']
            assert 'outs' not in text and 'range' not in q['prompt_fr'] and 'équité de' not in q['prompt_fr']
            assert q['category_fr'] == 'Équités' and q['mode'] == 'equity' and len(q['options']) in (4,)
            for name in ('Lucho', 'Lucky', 'PA '): assert name not in text       # aucun nom d'expert


def test_question_has_no_solution():
    sid, h = E.draw(2, 1, seed=3, kind='hit')[0]
    q = E.question(sid, h)
    assert 'value' not in json.dumps(q) and 'correct' not in json.dumps(q)
    assert q['hand_display'] and q['options'][0]['id'] == 'b0'


def test_gto_series_never_draw_equity(client):
    for seed in range(5):
        sid = client.post('/sessions', json={'seed': seed}).json()['session_id']
        for _ in range(5):
            q = client.get('/quiz/next', params={'session_id': sid}).json()
            assert q['question']['mode'] == 'gto' and not q['question']['spot_id'].startswith('eq:')
            client.post('/attempts', json={'session_id': sid, 'question_index': q['question_index'], 'action_id': q['question']['options'][0]['id']})
    assert quiz.mode_of(E.REF) == 'equity' and quiz.mode_of(quiz.DEFAULT_VERSION) == 'gto'
    r = client.post('/sessions', json={'mode': 'gto', 'filters': {'kind': 'hit'}, 'seed': 1}); assert r.status_code == 201   # kind ignoré hors équités
    assert client.get('/quiz/next', params={'session_id': r.json()['session_id']}).json()['question']['mode'] == 'gto'


def test_api_equity_series_and_stats(client):
    H = {'X-Player-Id': 'joueur-equite-1'}
    r = client.post('/sessions', json={'mode': 'equity', 'seed': 4}, headers=H); assert r.status_code == 201
    sid = r.json()['session_id']; assert r.json()['mode'] == 'equity' and r.json()['size'] == 5 and r.json()['dataset_version'] == E.REF
    kinds = set(); hands = []
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        assert q['category_fr'] == 'Équités' and q['kind'] in E.KINDS
        kinds.add(q['kind']); hands.append(q['hand'])
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][0]['id']}).json()
        assert a['verdict'] in ('correct', 'imprécision', 'erreur') and a['regret_mbb'] == 0 and a['equity']['options'] == [o['label_fr'] for o in q['options']]
    assert kinds == set(E.DEFAULT_KINDS) and len(set(hands)) == 5
    s = client.get(f'/sessions/{sid}/summary').json()
    assert s['complete'] and s['bb_per_100'] is None and s['ev_questions'] == 0 and s['category_fr'] == 'Équités'
    # une série GTO à côté : le BB/100 et le score GTO ne voient pas les équités
    g = client.post('/sessions', json={'seed': 2}, headers=H).json()['session_id']
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': g}).json()['question']
        client.post('/attempts', json={'session_id': g, 'question_index': i, 'action_id': q['options'][0]['id']})
    st = client.get('/users/me/stats', headers=H).json()
    assert st['questions'] == 5 and st['ev_questions'] == 5 and [m['filters']['mode'] for m in st['by']['mode']] == ['gto']
    assert st['equity']['questions'] == 5 and st['equity']['sessions'] == 1 and {k['kind'] for k in st['equity']['by_kind']} == set(E.DEFAULT_KINDS)
    # une seule sorte
    one = client.post('/sessions', json={'mode': 'equity', 'filters': {'kind': 'labels'}, 'size': 3}).json()['session_id']
    for i in range(3):
        assert client.get('/quiz/next', params={'session_id': one}).json()['question']['kind'] == 'labels'
        client.post('/attempts', json={'session_id': one, 'question_index': i, 'action_id': 'o0'})
    assert client.post('/sessions', json={'mode': 'equity', 'filters': {'table': 'heads-up'}}).status_code == 422
    assert client.post('/sessions', json={'mode': 'equity', 'challenge': 'daily'}, headers=H).status_code == 422
    assert client.post('/attempts', json={'session_id': one, 'question_index': 0, 'action_id': 'o1'}).status_code in (200, 409)


def test_no_spaced_review_for_equity(client):
    """décision du 10/11 : pas de révision espacée des équités pour l'instant (pas de coût en BB)"""
    H = {'X-Player-Id': 'joueur-equite-2'}
    assert client.post('/sessions', json={'mode': 'equity', 'review': True}, headers=H).status_code == 422
    assert client.get('/users/me/reviews', params={'mode': 'equity'}, headers=H).status_code == 422


def test_progress_keeps_equity_out_of_bb100():
    sid, h = E.draw(1, 1, seed=1, kind='equity')[0]
    rows = [dict(session_id='s', session_created_at='2026-11-10', dataset_version=E.REF, spot_id=sid, hand=h, verdict='erreur', points=0.0,
                 regret_mbb=0.0, answered_at='2026-11-10T10:00:00+00:00')]
    st = progress.compute(rows)
    assert st['questions'] == 0 and st['bb_per_100'] is None and st['equity']['questions'] == 1


ROUTES = [('/users/me/stats', {}), ('/users/me/level', {}), ('/users/me/preferences', {})] + [
    (r, {'mode': m}) for m in ('gto', 'exploit') for r in ('/users/me/today', '/users/me/recommendations', '/users/me/goals', '/users/me/wins',
                                                        '/users/me/challenges', '/users/me/worst-today', '/users/me/reviews', '/users/me/adaptation')]


def _snapshot(client, H):
    out = {}
    for r, params in ROUTES:
        x = client.get(r, params=params, headers=H)
        assert x.status_code < 500, (r, params, x.text)
        body = x.json()
        if r == '/users/me/stats': body.pop('equity', None)
        out[(r, params.get('mode'))] = (x.status_code, body)
    return out


def test_other_routes_ignore_equity(client):
    """une série d'équités ne fait planter aucune route du joueur, et ne change rien de ce que voient les modes GTO et exploitant"""
    H = {'X-Player-Id': 'joueur-equite-3'}
    assert client.post('/users/me/onboarding', json={'level': 2, 'experience': 'confirme', 'goal': 'ranges'}, headers=H).status_code == 200
    for mode in ('gto', 'exploit'):
        sid = client.post('/sessions', json={'mode': mode, 'seed': 3}, headers=H).json()['session_id']
        for i in range(5):
            q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
            client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][-1]['id']})
    before = _snapshot(client, H)
    sid = client.post('/sessions', json={'mode': 'equity', 'seed': 9}, headers=H).json()['session_id']
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        r = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][-1]['id']})
        assert r.status_code == 200
    after = _snapshot(client, H)
    for k in before: assert before[k] == after[k], k
    assert client.get('/users/me/stats', headers=H).json()['equity']['questions'] == 5
    assert client.get('/users/me/export', headers=H).status_code == 200


def test_level_two_player_gets_wider_bands(client):
    H = {'X-Player-Id': 'joueur-equite-4'}
    assert client.post('/users/me/onboarding', json={'level': 2, 'experience': 'confirme', 'goal': 'ranges'}, headers=H).status_code == 200
    r = client.post('/sessions', json={'mode': 'equity', 'filters': {'kind': 'hit'}, 'seed': 2}, headers=H).json(); assert r['level'] == 2
    q = client.get('/quiz/next', params={'session_id': r['session_id']}).json()['question']
    assert q['level'] == 2 and len(q['options']) in (5, 6)
