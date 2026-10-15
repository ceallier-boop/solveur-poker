import re
import pytest
from fastapi.testclient import TestClient
from spinsacademy import exploit, profiles, quiz


def test_catalog_covers_every_factor_once():
    c = profiles.catalog()
    avail = [p for p in c['profiles'] if p['available']]
    assert sorted(p['tendency']['odds_factor'] for p in avail if p['tendency']['stat'] == 'shove_pct') == sorted(exploit.FACTORS)
    assert sorted(p['tendency']['odds_factor'] for p in avail if p['tendency']['stat'] == 'call_pct') == sorted(exploit.CALL_FACTORS)
    for p in c['profiles']:
        assert p['id'] and p['name_fr'] and p['description_fr'] and p['scope_fr']
        if p['available']: assert p['difficulty'] in (1, 2, 3) and p['adaptation_fr'] and p['tendency']['rule_fr']
    assert {p['id'] for p in c['profiles'] if not p['available']} == {'shark'}       # profil du cahier non couvert, dit comme tel


def _adaptation():
    _, spots = quiz.load(quiz.DEFAULT_EXPLOIT)
    for sp in spots.values():
        for h, x in sp['hands'].items():
            if x.get('kind') == 'adaptation': yield sp, h


def test_question_and_correction_show_profile_and_the_four_parts():
    sp, h = next(_adaptation())
    q = quiz.question(quiz.DEFAULT_EXPLOIT, sp['spot_id'], h); pr = profiles.for_villain(sp['villain'])
    assert q['profile']['id'] == pr['id'] and 'adaptation_fr' not in q['profile']                 # pas de conseil avant la réponse
    assert f"« {pr['name_fr']} »" in q['prompt_fr']
    for sp, h in list(_adaptation())[:200]:
        r = quiz.correct(quiz.DEFAULT_EXPLOIT, sp['spot_id'], h, 'F'); ex = r['exploit']
        assert ex['changed'] == (r['gto_action'] != r['best_action']) and ex['changed']             # une adaptation change toujours l'action
        assert ex['confidence'] == ('élevée' if abs(1000 * sp['hands'][h]['ev_exact'][1]) >= exploit.CLEAR_MBB else 'moyenne')
        assert all(ex[k] for k in ('reference_fr', 'comparison_fr', 'tendency_fr', 'confidence_fr', 'note_fr'))
        assert 'hypothèse de simulation' in ex['note_fr'] and ex['profile']['catalog_version'] == profiles.catalog()['version']
        assert r['explanation_fr'].startswith('Contre ce type de profil') and ' BB' in ex['reference_fr']
        assert re.fullmatch(r'.+\.\n.+ (perd|perdrait|gagne) (moins de 0,02 BB|entre [\d,]+ et [\d,]+ BB|plus de 5 BB)\.', ex['reference_fr'], re.S)  # fourchette
        assert ex['comparison_fr'].startswith("À l'équilibre push/fold, ce serait")
    g = quiz.correct(quiz.DEFAULT_VERSION, *next(iter((s['spot_id'], h) for s in quiz.load()[1].values() for h, x in s['hands'].items() if x['quiz_eligible'])), 'F')
    assert g['exploit'] is None and g['core_fr'] and not any(w in g['core_fr'] for w in g['why_fr'])
    assert quiz.gain_range(0.01) == 'moins de 0,02 BB' and quiz.gain_range(-0.3) == 'entre 0,06 et 0,5 BB' and quiz.gain_range(0.04) == 'entre 0,02 et 0,06 BB' and quiz.gain_range(7) == 'plus de 5 BB'


def test_profile_filter_and_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'p.sqlite'))
    from spinsacademy.api import app
    c = TestClient(app)
    assert {p['id'] for p in c.get('/profiles').json()['profiles']} >= {'nit', 'maniac'}
    _, spots = quiz.load(quiz.DEFAULT_EXPLOIT)
    sid = c.post('/sessions', json={'mode': 'exploit', 'seed': 3, 'filters': {'profile': 'maniac'}}).json()['session_id']
    for i in range(5):
        q = c.get('/quiz/next', params={'session_id': sid}).json()['question']
        assert q['profile']['id'] == 'maniac' and spots[q['spot_id']]['villain']['factor'] == 2.0
        c.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': 'F'})
    assert c.post('/sessions', json={'mode': 'exploit', 'filters': {'profile': 'shark'}}).status_code == 422


def test_spot_without_profile_is_never_asked(monkeypatch):
    monkeypatch.setattr(profiles, 'for_villain', lambda v, version=None: None)
    with pytest.raises(ValueError): quiz.draw_series(quiz.DEFAULT_EXPLOIT, None, 5, 1)
    sp, h = next(_adaptation())
    with pytest.raises(ValueError): quiz.correct(quiz.DEFAULT_EXPLOIT, sp['spot_id'], h, 'F')


def test_identification_band_contains_every_profile_spot():
    _, spots = quiz.load(quiz.DEFAULT_EXPLOIT)
    for sp in spots.values():
        v = sp['villain']; pr = profiles.for_villain(v); lo, hi = profiles.band(pr, v['gto_pct'])
        assert (lo is None or v['observed_pct'] >= lo - 0.05) and (hi is None or v['observed_pct'] <= hi + 0.05)
        assert (lo is None) == (pr['id'] == 'nit') and (hi is None) == (pr['id'] in ('maniac', 'station'))
        if lo is not None and hi is not None: assert lo < hi
    q = quiz.question(quiz.DEFAULT_EXPLOIT, sp['spot_id'], next(h for h, x in sp['hands'].items() if x['quiz_eligible']))
    assert q['profile']['band_pct'] == list(profiles.band(pr, v['gto_pct']))


def test_recognition_sheet():
    c = profiles.catalog()
    for p in (x for x in c['profiles'] if x['available']):
        r = profiles.recognition(p, 45.7)
        assert r and len(r['signs_fr']) >= 2 and 'hasard' in r['caution_fr'] and str(r['occasions']) in r['sample_fr']
    by = {p['id']: p['tendency']['odds_factor'] for p in c['profiles'] if p['available']}
    assert profiles.occasions_needed(by['maniac'], 45.7) < profiles.occasions_needed(by['agressif'], 45.7)   # plus l'écart est grand, moins il faut d'occasions
    assert profiles.occasions_needed(1.0, 45.7) is None
    q = quiz.question(quiz.DEFAULT_EXPLOIT, *next((sp['spot_id'], sorted(quiz.teachable(sp))[0]) for sp in quiz.pool(quiz.DEFAULT_EXPLOIT) if quiz.teachable(sp)))
    assert q['profile']['recognize']['sample_fr']


def test_station_shoves_are_exact_and_explained():
    _, spots = quiz.load(quiz.DEFAULT_EXPLOIT)
    shoves = [sp for sp in spots.values() if sp.get('push_fold')]
    assert shoves and all(profiles.for_villain(sp['villain'])['id'] == 'station' and [a['id'] for a in sp['actions']] == ['F', 'A'] for sp in shoves)
    sp = next(s for s in shoves if s['table'] == 'heads-up' and s['effective_stack_bb'] == 10)
    from spinsacademy import pushfold
    push, call, value = pushfold.heads_up(10.0)
    import numpy as np
    from spinsacademy.cards import NAMES
    assert all(abs(sp['hands'][h]['ev_gto'][1] - round(float(value[i]), 5)) < 1e-9 for i, h in enumerate(NAMES))   # référence : équilibre push/fold
    weak = [h for h, x in sp['hands'].items() if x['ev_gto'][1] > 0 and x['ev_exact'][1] < 0]
    assert weak and all(sp['hands'][h]['fold_pct'] < sp['hands'][h]['fold_pct_gto'] for h in weak)         # il se couche moins souvent
    assert sp['hands']['AA']['ev_exact'][1] > sp['hands']['AA']['ev_gto'][1]                               # la valeur gagne plus
    h = next(h for h, x in sp['hands'].items() if x['kind'] == 'adaptation' and x['quiz_eligible'])
    q = quiz.question(quiz.DEFAULT_EXPLOIT, sp['spot_id'], h)
    assert 'paie un tapis avec' in q['prompt_fr'] and 'Tu joues en tapis ou fold.' in q['prompt_fr']
    r = quiz.correct(quiz.DEFAULT_EXPLOIT, sp['spot_id'], h, 'A' if r_best(sp, h) == 'F' else 'F')
    assert 'Il se couche' in r['explanation_fr'] and 'on part à tapis avec' in r['explanation_fr'] and r['verdict'] != 'correct'


def r_best(sp, h): return 'A' if sp['hands'][h]['ev_exact'][1] > 0 else 'F'
