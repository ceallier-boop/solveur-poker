import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_full_series_of_five(client):
    r = client.post('/sessions', json={'seed': 3}); assert r.status_code == 201
    sid = r.json()['session_id']; assert r.json()['size'] == 5
    seen = []
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}).json()
        assert not q['done'] and q['question_index'] == i
        body = q['question']
        assert 'solution' not in str(body) and 'ev' not in {k for o in body['options'] for k in o}    # aucune solution envoyée
        seen.append(body['spot_id'])
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': body['options'][0]['id']}).json()
        assert a['verdict'] in ('correct', 'imprécision', 'erreur') and a['explanation_fr'] and not a['already_answered']
    assert len(set(seen)) == 5                                                                         # pas deux fois le même spot
    assert client.get('/quiz/next', params={'session_id': sid}).json()['done']
    s = client.get(f'/sessions/{sid}/summary').json()
    assert s['complete'] and s['questions'] == 5 and sum(s['verdicts'].values()) == 5 and 0 <= s['score_pct'] <= 100
    assert s['dataset_version'] == quiz.DEFAULT_VERSION


def test_answers_are_final_and_validated(client):
    sid = client.post('/sessions', json={'seed': 1}).json()['session_id']
    q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
    ids = [o['id'] for o in q['options']]
    assert client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': 'ZZ'}).status_code == 422
    first = client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': ids[0]}).json()
    again = client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': ids[0]}).json()
    assert again['already_answered'] and again['verdict'] == first['verdict']                          # reprise après coupure réseau
    if len(ids) > 1:
        assert client.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': ids[1]}).status_code == 409
    assert client.get('/quiz/next', params={'session_id': 'inconnue'}).status_code == 404


def test_filters_and_reproducibility(client):
    a = client.post('/sessions', json={'seed': 7, 'filters': {'table': 'heads-up', 'family': 'vs_allin'}}).json()['session_id']
    b = client.post('/sessions', json={'seed': 7, 'filters': {'table': 'heads-up', 'family': 'vs_allin'}}).json()['session_id']
    qa = client.get('/quiz/next', params={'session_id': a}).json()['question']; qb = client.get('/quiz/next', params={'session_id': b}).json()['question']
    assert qa['spot_id'] == qb['spot_id'] and qa['hand'] == qb['hand'] and qa['table'] == 'heads-up' and qa['family'] == 'vs_allin'
    assert client.post('/sessions', json={'filters': {'table': 'heads-up', 'hero': 'BTN'}}).status_code == 422   # filtre sans spot
    assert client.post('/sessions', json={'filters': {'table': 'six-max'}}).status_code == 422


def test_series_coverage_across_seeds():
    """répartition réellement servie sur 300 séries : toutes les familles et les deux tables apparaissent"""
    import collections
    fam = collections.Counter(); table = collections.Counter()
    _, spots = quiz.load()
    for seed in range(300):
        for sid, h in quiz.draw_series(seed=seed):
            fam[quiz.family(spots[sid])] += 1; table[spots[sid]['table']] += 1
    assert set(fam) == {'first_in', 'vs_limp', 'vs_raise', 'vs_allin'} and min(fam.values()) > 0.15 * sum(fam.values())
    assert set(table) == {'3-handed', 'heads-up'}


def test_web_interface_is_served(client):
    r = client.get('/'); assert r.status_code == 200 and 'SpinsAcademy' in r.text and '/static/app.js' in r.text
    for f in ('app.js', 'app.css', 'manifest.json', 'icon.svg'):
        assert client.get(f'/static/{f}').status_code == 200


def test_exploit_mode_series(client):
    r = client.post('/sessions', json={'mode': 'exploit', 'seed': 4}).json()
    assert r['mode'] == 'exploit' and r['dataset_version'].startswith('exploit_calls/')
    sid = r['session_id']; bases = set()
    for i in range(r['size']):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        assert q['mode'] == 'exploit' and q['villain']['observed_pct'] != q['villain']['gto_pct']
        assert [o['id'] for o in q['options']] == ['F', 'C'] and 'part à tapis avec' in q['prompt_fr']
        bases.add(q['spot_id'].rsplit('-x', 1)[0])
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': 'C'}).json()
        assert a['gto_label'] and 'hypothèse de simulation' in a['explanation_fr']
    assert len(bases) == r['size']                                     # jamais deux fois la même situation de base


def test_exploit_dataset_consistency():
    """facteur 1 implicite : l'EV « GTO » stockée = l'EV exacte du spot GTO ; une adaptation change bien l'action"""
    from spinsacademy import quiz
    _, ex = quiz.load(quiz.DEFAULT_EXPLOIT); _, gto = quiz.load(quiz.DEFAULT_VERSION)
    n = 0
    for sp in list(ex.values())[:40]:
        base = gto[sp['base_spot_id']]
        for h, v in sp['hands'].items():
            if 'ev_gto' not in v: continue
            assert abs(v['ev_gto'][1] - base['hands'][h]['ev_exact'][1]) < 1e-6
            if v['kind'] == 'adaptation':
                assert (v['ev_exact'][1] > 0) != (v['ev_gto'][1] > 0) and abs(v['ev_exact'][1]) * 1000 >= 20; n += 1
        f = sp['villain']['factor']
        assert (sp['villain']['observed_pct'] > sp['villain']['gto_pct']) == (f > 1)
    assert n > 0


def test_gains_are_shown_in_bb_with_floor():
    assert quiz.gain_bb(0.049) == '<0,05 BB' and quiz.gain_bb(0.05) == '0,05 BB' and quiz.gain_bb(1.234) == '1,23 BB'
    assert quiz.gain_bb(-0.01, signed=True) == '−<0,05 BB' and quiz.gain_bb(0.12, signed=True) == '+0,12 BB'
    seen_small = False
    for ref in (quiz.DEFAULT_VERSION, quiz.DEFAULT_EXPLOIT):
        for sp in list(quiz.pool(ref))[:60]:
            h = next(x for x, v in sp['hands'].items() if v['quiz_eligible'])
            for a in sp['actions']:
                r = quiz.correct(ref, sp['spot_id'], h, a['id'])
                assert 'mBB' not in r['explanation_fr']
                seen_small |= '<0,05 BB' in r['explanation_fr']
    assert seen_small


def test_correction_has_grid_and_why():
    _, spots = quiz.load()
    seen = {'exact': 0, 'hrc': 0}
    for sp in spots.values():
        h = next((x for x, v in sp['hands'].items() if v['quiz_eligible']), None)
        if not h: continue
        r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, sp['actions'][0]['id'])
        g = r['range']; assert len(g['actions']) == len(sp['actions']) and h in g['hands']
        assert all(sum(v) == 100 for v in g['hands'].values()) and abs(sum(g['share_pct']) - 100) <= 2
        assert r['why_fr'] and all(line in r['explanation_fr'] for line in r['why_fr'])
        if 'équité' in r['why_fr'][0]: seen['exact'] += 1
        else: seen['hrc'] += 1
    assert seen['exact'] > 20 and seen['hrc'] > 100


def test_draw_balances_positions_and_skips_no_lesson_hands():
    import collections
    _, spots = quiz.load(); pos = collections.Counter()
    for seed in range(60):
        for s, h in quiz.draw_series(quiz.DEFAULT_VERSION, None, 5, seed):
            pos[spots[s]['hero']] += 1
            assert quiz.lesson_gap(spots[s], h) is not None
    assert min(pos.values()) >= 0.25 * sum(pos.values())


def test_lexique_is_served_and_well_formed(client):
    import json, os
    lex = client.get('/static/lexique.json').json()
    cats = set(lex['categories'])
    assert lex['version'] and len(lex['terms']) >= 50
    for t in lex['terms']:
        assert t['term'] and t['def'] and t['match'] and t['cat'] in cats
    terms = {t['term'] for t in lex['terms']}
    assert len(terms) == len(lex['terms'])                                                 # pas de doublon
    for needed in ('GTO', 'Équité', 'Cote du pot', 'Range', 'Stratégie mixte', 'ICM'):
        assert any(x.startswith(needed) for x in terms), needed
