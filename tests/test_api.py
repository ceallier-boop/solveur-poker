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
    """répartition réellement servie sur 300 séries : toutes les familles et les deux tables apparaissent, premières décisions en tête"""
    import collections
    fam = collections.Counter(); table = collections.Counter()
    _, spots = quiz.load()
    for seed in range(300):
        for sid, h in quiz.draw_series(seed=seed):
            fam[quiz.family(spots[sid])] += 1; table[spots[sid]['table']] += 1
    n = sum(fam.values())                       # v4.4 : tirage selon la fréquence réelle des situations
    assert set(fam) == {'first_in', 'vs_limp', 'vs_raise', 'vs_allin'} and min(fam.values()) > 0.08 * n
    assert fam['first_in'] / n >= 0.40 and fam['vs_allin'] > fam['vs_raise']
    assert set(table) == {'3-handed', 'heads-up'}


def test_web_interface_is_served(client):
    r = client.get('/'); assert r.status_code == 200 and 'SpinsAcademy' in r.text and '/static/app.js' in r.text
    for f in ('app.js', 'app.css', 'manifest.json', 'icon.svg'):
        assert client.get(f'/static/{f}').status_code == 200


def test_exploit_mode_series(client):
    """mode exploitant : questions du field (spinsacademy.field), jamais l'ancien mode des profils fictifs"""
    r = client.post('/sessions', json={'mode': 'exploit', 'seed': 4}).json()
    assert r['mode'] == 'exploit' and r['dataset_version'].startswith('exploit_field/')
    for i in range(r['size']):
        q = client.get('/quiz/next', params={'session_id': r['session_id']}).json()['question']
        assert q['mode'] == 'exploit' and q['field'] and q['villain'] is None and q['profile'] is None
        a = client.post('/attempts', json={'session_id': r['session_id'], 'question_index': i, 'action_id': q['options'][0]['id']}).json()
        assert a['field']['rule'] and 'Profil fictif' not in a['explanation_fr']
    assert client.get('/profiles').status_code == 404                     # route de l'ancien mode retirée


def test_gains_are_shown_in_bb_with_floor():
    assert quiz.gain_bb(0.019) == '<0,02 BB' and quiz.gain_bb(0.02) == '<0,02 BB' and quiz.gain_bb(0.021) == 'un peu plus de 0,02 BB' and quiz.gain_bb(0.0202) == 'un peu plus de 0,02 BB' and quiz.gain_bb(1.234) == '1,23 BB'
    assert quiz.gain_bb(-0.01, signed=True) == '−<0,02 BB' and quiz.gain_bb(0.12, signed=True) == '+0,12 BB'
    seen_small = False
    for ref in (quiz.DEFAULT_VERSION,):
        for sp in list(quiz.pool(ref))[:60]:
            h = next(x for x, v in sp['hands'].items() if v['quiz_eligible'])
            for a in sp['actions']:
                r = quiz.correct(ref, sp['spot_id'], h, a['id'])
                assert 'mBB' not in r['explanation_fr']
                seen_small |= '<0,02 BB' in r['explanation_fr'] or 'moins de 0,02 BB' in r['explanation_fr']
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
    _, spots = quiz.load(); pos = collections.Counter(); table = collections.Counter(); diff = collections.Counter()
    for seed in range(120):
        series = quiz.draw_series(quiz.DEFAULT_VERSION, None, 5, seed)
        assert len({h for _, h in series}) == len(series)                       # pas deux fois la même main dans une série
        for s, h in series:
            pos[spots[s]['hero']] += 1; table[spots[s]['table']] += 1; diff[quiz.difficulty(quiz.lesson_gap(spots[s], h))] += 1
            assert quiz.lesson_gap(spots[s], h) is not None
    n = sum(pos.values())
    assert 0.25 <= table['heads-up'] / n <= 0.45                                # cible validée : 35 % de heads-up
    assert diff['facile'] / n <= 0.15                                           # plafond validé : 15 % de questions faciles
    assert min(pos['SB'], pos['BB']) >= 0.25 * n and pos['BTN'] >= 0.15 * n     # le BTN ne joue pas en heads-up


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


def test_second_review_fixes():
    _, spots = quiz.load()
    sp = spots['3w-8-8-4-BTN-allin_SB-fold-eee730']                                            # BB couvert : 4 BB effectifs
    assert quiz.call_terms(sp) == (3.0, 8.5) and quiz.action_label(sp, sp['actions'][1]) == 'Payer le tapis (3 BB de plus)'
    aa = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], 'AA', 'C')['why_fr'][1]
    assert '85,' in aa                                                                             # (4,29 + 3) / 8,5
    assert quiz.gain_bb(0.062) == 'un peu plus de 0,06 BB' and quiz.gain_bb(0.058) == 'un peu moins de 0,06 BB' and quiz.gain_bb(0.07) == '0,07 BB'
    for s in list(spots.values())[::20]:                                                        # la meilleure action affichée figure dans la stratégie affichée
        for h, x in s['hands'].items():
            if x['quiz_eligible']: assert quiz.reference_action(s, h) in dict(grading.displayed_mix(s, h))


def test_several_good_decisions_when_ev_ties():
    _, spots = quiz.load(); seen = 0
    for s in quiz.candidates(spots):
        for h in quiz.teachable(s):
            ev = grading.reference_ev(s, h); top = max(ev); ids = [a['id'] for a in s['actions']]
            good = [ids[k] for k, e in enumerate(ev) if 1000 * (top - e) <= grading.TOLERANCE_MBB + 1e-9]
            if len(good) < 2: continue
            r = quiz.correct(quiz.DEFAULT_VERSION, s['spot_id'], h, good[-1])
            assert r['core_fr'].startswith('Plusieurs bonnes décisions') and set(r['good_actions']) == set(good)
            assert r['verdict'] == 'correct' and r['loss_fr'] is None
            labels = {a['id']: quiz.action_label(s, a) for a in s['actions']}
            other = [l for l in r['why_fr'] if l.startswith('Autre option')]
            assert not any(quiz._low(labels[g]) in l.split(':')[1].split(',')[0] for g in good for l in other)   # une action à égalité n'est pas « autre option »
            seen += 1
            if seen >= 20: return
    assert seen


def test_dataset_loaded_once_under_concurrency():
    """démarrage à froid (test à cinq joueurs du 23/10) : des requêtes simultanées partagent un seul chargement du dataset"""
    import threading
    quiz.load.cache_clear(); calls = []
    real = quiz._load.__wrapped__
    def counting(v): calls.append(v); return real(v)
    quiz._load = quiz.lru_cache(maxsize=8)(counting)
    try:
        out = []
        th = [threading.Thread(target=lambda: out.append(id(quiz.load(quiz.DEFAULT_FIELD)))) for _ in range(6)]
        [t.start() for t in th]; [t.join() for t in th]
        assert len(calls) == 1 and len(set(out)) == 1
    finally:
        quiz._load = quiz.lru_cache(maxsize=8)(real); quiz.load.cache_clear()
