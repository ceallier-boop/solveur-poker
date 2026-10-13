import pytest
from fastapi.testclient import TestClient
from spinsacademy import grading, quiz


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
    """facteur 1 : l'EV de référence stockée = l'EV exacte du call contre la range d'équilibre push/fold ; une adaptation change bien l'action"""
    import numpy as np
    from spinsacademy import quiz, allin, pushfold
    _, ex = quiz.load(quiz.DEFAULT_EXPLOIT); _, gto = quiz.load(quiz.DEFAULT_VERSION)
    n = 0
    for sp in list(ex.values())[:40]:
        base = gto[sp['base_spot_id']]; push, _ = pushfold.shover_range(base, sp['villain']['position'])
        st = dict(zip(sp['players'], sp['stacks_bb'])); L = min(st[sp['hero']], st[sp['villain']['position']])
        ref = allin.call_ev(push, L, sp['pot_bb'] - sp['hero_committed_bb'] - L, sp['hero_committed_bb'])
        assert sp['villain']['reference'] == 'nash_pushfold'
        for h, v in sp['hands'].items():
            if 'ev_gto' not in v: continue
            assert abs(v['ev_gto'][1] - ref[quiz.NAMES.index(h)]) < 1e-4
            if v['kind'] == 'adaptation':
                assert (v['ev_exact'][1] > 0) != (v['ev_gto'][1] > 0) and min(abs(v['ev_exact'][1]), abs(v['ev_gto'][1])) * 1000 >= 20; n += 1
        f = sp['villain']['factor']
        assert (sp['villain']['observed_pct'] > sp['villain']['gto_pct']) == (f > 1)
    assert n > 0


def test_gains_are_shown_in_bb_with_floor():
    assert quiz.gain_bb(0.019) == '<0,02 BB' and quiz.gain_bb(0.02) == '<0,02 BB' and quiz.gain_bb(0.021) == '0,021 BB' and quiz.gain_bb(0.0202) == 'un peu plus de 0,02 BB' and quiz.gain_bb(1.234) == '1,23 BB'
    assert quiz.gain_bb(-0.01, signed=True) == '−<0,02 BB' and quiz.gain_bb(0.12, signed=True) == '+0,12 BB'
    seen_small = False
    for ref in (quiz.DEFAULT_VERSION, quiz.DEFAULT_EXPLOIT):
        for sp in list(quiz.pool(ref))[:60]:
            h = next(x for x, v in sp['hands'].items() if v['quiz_eligible'])
            for a in sp['actions']:
                r = quiz.correct(ref, sp['spot_id'], h, a['id'])
                assert 'mBB' not in r['explanation_fr']
                seen_small |= '<0,02 BB' in r['explanation_fr']
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


def test_equity_gap_bands_and_next_steps():
    _, spots = quiz.load(); bands = set(); kinds = set()
    for sp in spots.values():
        for h, x in sp['hands'].items():
            if not x['quiz_eligible']: continue
            for a in sp['actions']:
                r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, a['id'])
                for line in r['why_fr']:
                    for b in ('Décision serrée', 'Écart moyen', 'Écart large'):
                        if line.startswith(b): bands.add((b, a['id'] == r['best_action']))
                n = r['next'] or dict(metrics=[]); kinds.add(bool(n['metrics']))
                for m in n['metrics']:
                    assert m['compare'] == ('equal' if round(100 * m['value']) == round(100 * m['average']) else 'above' if m['value'] > m['average'] else 'below')
                if {t['id']: t['type'] for t in sp['actions']}[r['best_action']] in ('allin', 'call_allin'): assert not n['metrics']
        if len(bands) == 6 and kinds == {True, False}: break
    assert len(bands) == 6 and kinds == {True, False}             # trois niveaux d'écart, réponse juste ou fausse


def test_flop_profiles_match_known_probabilities():
    assert abs(quiz.postflop_profile('77')['set_plus'] - 0.1176) < 1e-3                      # brelan au flop : 11,8 %
    assert abs(quiz.postflop_profile('AKs')['flush_draw_plus'] - 0.1179) < 1e-3              # tirage couleur ou couleur : 11,8 %
    assert 0.32 <= quiz.postflop_profile('K7o')['pair_plus'] <= 0.34                          # paire ou mieux avec une main non pairée


def test_review_fixes_on_texts():
    """relecture joueur : chiffres justes et textes cohérents avec la correction"""
    assert abs(quiz.overcard_prob('TT') - 0.695) < 1e-3 and quiz.overcard_prob('AA') == 0     # au moins une carte au-dessus de la paire
    assert abs(float(quiz._VSR()[quiz.NAMES.index('AA')]) - 0.852) < 1e-3                    # AA contre une main au hasard, cartes retirées
    _, spots = quiz.load(); seen = set()
    for sp in list(spots.values())[::25]:
        types = {a['id']: a['type'] for a in sp['actions']}
        for h, x in sp['hands'].items():
            if not x['quiz_eligible']: continue
            shown = dict(grading.displayed_mix(sp, h))
            rf = grading.reference_freq(sp, h)
            for a, f in zip(sp['actions'], rf):                        # une action affichée est toujours acceptée
                assert (a['id'] in shown) == (f >= grading.MIXED_MIN or f == max(rf) and not any(v >= grading.MIXED_MIN for v in rf))
                if a['id'] in shown: assert grading.grade(sp, h, a['id'])['verdict'] == 'correct'
            for chosen in types:
                r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, chosen); n = r['next']; t = types[r['best_action']]
                text = r['explanation_fr']
                assert 'aucune n\'est une erreur' not in text and ' fold ' not in history_lines(sp) and '((' not in text
                if t == 'fold': assert n is None; seen.add('fold'); continue                          # rien à dire après le flop
                if quiz.family(sp) == 'vs_allin':
                    assert n is None or (not n['metrics'] and quiz.to_act_after(sp)); seen.add('vs_allin'); continue
                assert ' : Tu' not in n['intro'] and ' : tu pousses :' not in n['intro']
                if t == 'allin': assert 'se couche' in n['intro'] and not n['metrics']; seen.add('allin')
                if chosen != r['best_action']: assert n['intro'].startswith("Avec l'action de référence"); seen.add('subject')
                for m in n['metrics']:
                    assert m['tone'] == ('neutral' if m['compare'] == 'equal' else 'good' if (m['compare'] == 'above') != m['lower_is_better'] else 'bad')
                if 'à peine mieux que le' in text: seen.add('barely')
    assert {'vs_allin', 'allin', 'subject', 'fold'} <= seen


def history_lines(sp):
    return ' '.join(quiz.history_text(sp)) + ' '


def test_profile_catalog_texts():
    from spinsacademy import profiles
    c = profiles.catalog(); assert c['version'] == '1.4.0'
    m = next(p for p in c['profiles'] if p['id'] == 'maniac')
    assert 'mains faibles' not in m['description_fr'] and 'moins forte' in m['description_fr']
    assert all('4 à 25 BB' not in (p['scope_fr'] or '') for p in c['profiles'])


def test_second_review_fixes():
    _, spots = quiz.load()
    sp = spots['3w-8-8-4-BTN-allin_SB-fold-eee730']                                            # BB couvert : 4 BB effectifs
    assert quiz.call_terms(sp) == (3.0, 8.5) and quiz.action_label(sp, sp['actions'][1]) == 'Payer le tapis (3 BB de plus)'
    aa = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], 'AA', 'C')['why_fr'][1]
    assert '85,' in aa                                                                             # (4,29 + 3) / 8,5
    assert quiz.gain_bb(0.062) == '0,062 BB' and quiz.gain_bb(0.058) == '0,058 BB' and quiz.gain_bb(0.07) == '0,07 BB'
    for s in list(spots.values())[::20]:                                                        # la meilleure action affichée figure dans la stratégie affichée
        for h, x in s['hands'].items():
            if x['quiz_eligible']: assert quiz.reference_action(s, h) in dict(grading.displayed_mix(s, h))
    _, ex = quiz.load(quiz.DEFAULT_EXPLOIT)
    assert all(quiz.adapts(s) for s in quiz.candidates(ex)) and len(quiz.candidates(ex)) < len(ex)
