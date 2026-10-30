"""mode Field : banque de questions du moteur exploitant v4.2 (tools/field), corrigée après l'audit des coachs de la v4.1"""
import json, os, re, sys
import pytest
from fastapi.testclient import TestClient
from spinsacademy import catalog, field, quiz
from spinsacademy.hrc import ROOT

H = {'X-Player-Id': 'f' * 32}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _spots():
    return quiz.load(quiz.DEFAULT_FIELD)[1]


def test_dataset_is_valid_and_hides_internal_profile():
    spots = _spots()
    assert len(spots) > 300 and not any(field.problems(s) for s in spots.values())
    types = {s['field']['type'] for s in spots.values()}
    assert types == set(field.TYPE_FR)
    for sp in list(spots.values())[:120]:
        h = next(iter(sp['hands'])); q = quiz.question(quiz.DEFAULT_FIELD, sp['spot_id'], h)
        blob = json.dumps(q, ensure_ascii=False)
        assert 'internal_profile' not in blob and sp['field']['internal_profile'] not in q['prompt_fr']
        assert 'correct' not in q['field'] and 'mBB' not in blob and q['mode'] == 'exploit'
        for o in sp['field']['options']:
            r = quiz.correct(quiz.DEFAULT_FIELD, sp['spot_id'], h, o['id'])
            assert 'mBB' not in r['explanation_fr'] + ' '.join(r['why_fr'])                      # montants en BB, jamais en mBB
            assert r['explanation_fr'].count('À retenir') == 1 and (r['verdict'] == 'correct') == (o['id'] == sp['field']['correct'])


def test_audit_corrections_v4_2():
    spots = list(_spots().values()); F = [s['field'] for s in spots]
    # 1. HU contre un rec inconnu : le limp n'est plus sous-évalué (8 questions « pousser » rejetées par Lucho et PA)
    unknown_hu = [s for s in spots if s['field']['type'] == 'inconnu' and s['table'] == 'heads-up' and s['hero'] == 'SB']
    assert sum(s['field']['correct'] in ('L', 'R') for s in unknown_hu) > 0.8 * len(unknown_hu)   # v4.5 : limp ou petite relance, pas le tapis
    for s in unknown_hu:
        ev = {o['id']: o['ev_mbb'] for o in s['field']['options']}
        if s['field']['correct'] == 'A' and 'L' in ev:
            assert ev['A'] - ev['L'] >= s['field']['noise_mbb'] - 1                                # un tapis ne gagne que nettement
    # 2. rec passif et reg sont deux pastilles
    prof = [f for f in F if f['type'] == 'profil']
    assert prof and all({'Rec passif', 'Reg'} <= {o['label_fr'] for o in f['options']} for f in prof)
    assert not any('proche de la théorie' in o['label_fr'] for f in prof for o in f['options'])
    # 3. pièges : vrai écart du vilain, décision non triviale
    for f in F:
        if f['type'] == 'piège':
            assert f['margin_mbb'] <= 10 * f['noise_mbb'] + 1
            if f['rule'] == 'R9' and f['stats']: assert abs(f['stats'][0]['observed_pct'] - f['stats'][0]['gto_pct']) >= 4.95
    # 4. pas de déviation sur une main que HRC joue déjà en mixte (>= 30 %)
    assert all(f['gto_freq_pct'] < 30 for f in F if f['type'] in ('adaptation', 'inconnu'))
    # 5. à 6 BB, payer moins contre un vilain qui pousse peu exige 80 occasions
    assert all(f['observations'] >= 80 for s, f in zip(spots, F) if f['type'] in ('adaptation', 'inconnu') and s['effective_stack_bb'] <= 6
               and s['field_family'] == 'vs_allin' and f['correct'] == 'F')
    # limp en BvB : borne basse, dit comme tel
    for s, f in zip(spots, F):
        if any(o['id'] == 'L' for o in f['options']) and f['type'] not in ('identification',):
            assert f['limp_estimate'] == (s['table'] == 'heads-up')


@pytest.mark.slow
def test_catalog_validates_field_dataset():
    r = catalog.validate(quiz.DEFAULT_FIELD)
    assert r['ok'], [c for c in r['checks'] if not c['ok']]


def test_field_series_api(client):
    r = client.post('/sessions', json={'mode': 'exploit', 'seed': 7}, headers=H)
    assert r.status_code == 201 and r.json()['dataset_version'].startswith('exploit_field/') and r.json()['adaptive'] is None
    sid = r.json()['session_id']; traps = reads = 0; hands = []
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        assert q['mode'] == 'exploit' and q['field']['type_fr'] and q['options']
        traps += q['field']['type'] in ('piège', 'échantillon'); reads += q['field']['type'] in field.READ
        if q['field']['type'] not in field.READ: hands.append(q['hand'])
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][-1]['id']}).json()
        assert a['verdict'] in ('correct', 'imprécision', 'erreur') and a['field']['rule'] and a['explanation_fr']
        if i == 0:
            rep = client.post('/reports', json={'session_id': sid, 'question_index': 0, 'reason': 'wrong_answer', 'comment': 'test'}, headers=H)
            assert rep.status_code == 201
    assert traps <= field.MAX_TRAPS and reads <= field.MAX_READ and len(set(hands)) == len(hands)
    s = client.get(f'/sessions/{sid}/summary').json(); assert s['complete'] and s['questions'] == 5
    st = client.get('/users/me/stats', headers=H).json()
    assert any(x['label'] == 'Exploitant' for x in st['by']['mode'])
    assert client.get('/users/me/reviews', params={'mode': 'exploit'}, headers=H).status_code == 200
    f = client.post('/sessions', json={'mode': 'exploit', 'seed': 2, 'filters': {'family': 'read'}}, headers=H)
    assert f.status_code == 201                                          # série « lecture du vilain » : pas de plafond de lecture
    q = client.get('/quiz/next', params={'session_id': f.json()['session_id']}).json()['question']
    assert q['field']['type'] in field.READ and q['field']['ask_fr']
    g = client.post('/sessions', json={'mode': 'exploit', 'seed': 2, 'filters': {'table': 'heads-up', 'hero': 'SB'}}, headers=H).json()
    q = client.get('/quiz/next', params={'session_id': g['session_id']}).json()['question']
    assert q['table'] == 'heads-up' and q['hero'] == 'SB'


@pytest.mark.skipif(not os.path.isdir(os.path.join(ROOT, 'data', 'hrc', 'raw', 'min_raise_hu')), reason='exports HRC bruts absents')
def test_engine_v4_2_checks():
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'field'))
    import exploit_engine as ee, profils_field as pf
    from hrcdata import NAMES
    r = ee.run_spot('hu', 8, 'SB pousse face au BB', ee.SPOTS[('hu', 'SB pousse face au BB')], profiles={'x': pf.factors(pf.DEFAULT, 8)})['x']
    i = NAMES.index('J2s')
    assert r['ev_limp'][i] > max(r['ev_raw'][i], 0)                       # J2s à 8 BB contre un rec inconnu : on limpe (audit)
    g = ee.limp_ev('hu', 8, '', '0C', 1.0)[0]
    assert abs(g[i] - ee.hero_ev_hrc('hu', 8, '', 'C')[i]) < 1e-12          # contre un BB GTO, l'estimation rend l'EV HRC


@pytest.mark.slow
def test_profiles_follow_field_shares():
    """v4.3 : le volume prime (banque x 10) ; le rec passif reste le profil le plus représenté, et le tirage des séries
    pondère chaque question par la part de son profil dans le field"""
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'field'))
    import profils_field as pf, quiz_generator as qg
    from collections import Counter
    spots = list(_spots().values()); F = [s['field'] for s in spots]; c = Counter(f['internal_profile'] for f in F)
    assert len(F) >= 0.95 * qg.N_TARGET and c.most_common(1)[0][0] == pf.DEFAULT
    drawn = Counter(); by_id = {s['spot_id']: s for s in spots}
    for seed in range(60):
        for sid, _ in field.draw(spots, 5, seed): drawn[by_id[sid]['field']['internal_profile']] += 1
    assert drawn.most_common(1)[0][0] == pf.DEFAULT and drawn[pf.DEFAULT] / sum(drawn.values()) >= 0.30   # v4.4 : tapis et réponses à parts égales
    fam = Counter(); ans = Counter()
    for seed in range(200):
        for sid, _ in field.draw(spots, 5, seed):
            sp = by_id[sid]; fam[sp['field_family']] += 1
            if sp['field_family'] == 'vs_limp': ans[sp['field']['correct']] += 1
    n = sum(fam.values())
    assert fam['vs_limp'] / n <= 0.32 and fam['vs_allin'] / n >= 0.30          # v4.4 (audit) : le limp ne prend plus la moitié des séries
    assert max(ans.values()) / sum(ans.values()) <= 0.65                        # on ne répond pas « tapis » sans réfléchir


def test_limp_situations_theory_and_postflop():
    spots = list(_spots().values())
    limp = [s for s in spots if s['field_family'] == 'vs_limp']
    assert len(limp) >= 60 and {s['table'] for s in limp} == {'heads-up', '3-handed'}
    ids = lambda s: {o['id'] for o in s['field']['options']}
    assert all('X' in ids(s) and ids(s) <= {'X', 'A', 'R'} and len(ids(s)) >= 2 for s in limp)    # check, tapis ou iso à 3 BB (v4.5)
    assert any('R' in ids(s) for s in limp) and any(s['effective_stack_bb'] >= 15 for s in limp)
    assert all([h for h in s['history'] if h['action'] != 'fold'][-1]['action'] == 'limp' and s['hero'] == 'BB' for s in limp)
    assert len(spots) >= 400
    banned = ('coach', 'Lucho', 'Lucky', 'marge de précision', 'bruit', 'borne basse', 'incertitude')
    for sp in spots[::3]:
        h = next(iter(sp['hands']))
        for o in sp['field']['options']:
            r = quiz.correct(quiz.DEFAULT_FIELD, sp['spot_id'], h, o['id'])
            text = r['explanation_fr'] + ' '.join(r['why_fr']) + json.dumps(r['next'] or {}, ensure_ascii=False)
            assert not any(b in text for b in banned), (sp['spot_id'], [b for b in banned if b in text])
            if sp['field']['type'] not in field.READ:
                assert any("d'équité" in l for l in r['why_fr'])                                # éléments théoriques chiffrés
            best_t = next(x['type'] for x in sp['field']['options'] if x['id'] == sp['field']['correct'])
            if best_t in field.FLOP_MOVES and sp['field']['type'] not in field.READ:                 # A' : seulement si le meilleur coup mène au flop
                n = r['next']; assert n and n['title_fr'] == 'Gérer le postflop' and n['plus_fr'] and n['minus_fr']
                assert 'SPR' in n['intro'] and n['forces'] and len(n['plan']) == 3
                hu_bb = sp['table'] == 'heads-up' and sp['hero'] == 'BB'
                vs_btn = any(h['position'] == 'BTN' and h['action'] in ('limp', 'raise') for h in sp['history'])   # le BTN parle après le BB
                assert ('premier' in n['position']) == (hu_bb or (sp['table'] == '3-handed' and (sp['hero'] == 'SB' or vs_btn)))   # heads-up : le SB est au bouton
            elif sp['field']['type'] not in field.READ:
                assert r['next'] is None                                                        # tapis ou relance : pas de plan pour un check


def test_audit_corrections_v4_4():
    """audit complet des coachs (22/10) : stats affichées justes, reads significatifs, type caché avant la réponse"""
    spots = list(_spots().values())
    for sp in spots:
        f = sp['field']; st = {s['stat']: s for s in f['stats']}
        if 'call_pct_bb_sb_fold' in st:                                   # le BB se compte sur les folds du SB
            assert st['call_pct_bb_sb_fold']['n'] == f['observations'] - st['call_pct']['k'] and st['call_pct_bb_sb_fold']['k'] <= st['call_pct_bb_sb_fold']['n']
        if 'call_after_limp_pct' in st: assert st['call_after_limp_pct']['n'] >= 10      # pas de stat de call sous 10 limps
    for sp in spots[::7]:
        q = quiz.question(quiz.DEFAULT_FIELD, sp['spot_id'], next(iter(sp['hands'])))
        assert q['field']['type'] in ('inconnu', 'observé', 'pastille', 'identification', 'profil')    # piège / adaptation : seulement à la correction
    tight = [s for s in spots if s['field']['type'] == 'adaptation' and s['field']['gto'] in ('A', 'C') and s['field']['correct'] in ('F', 'L', 'X')]
    assert len(tight) >= 100                                              # des adaptations « plus serré », pas seulement « plus large »
    lab = lambda f: next(o['label_fr'] for o in f['options'] if o['id'] == f['correct'])
    assert any(lab(s['field']) == 'Nit' for s in spots if s['field']['type'] == 'profil')          # le limp sépare le nit du rec passif


def test_extension_v4_5():
    """v4.5 : 4 à 25 BB, relance non all-in, nouvelles situations, tapis inégaux en heads-up, range de tapis du rec"""
    spots = list(_spots().values())
    assert max(s['effective_stack_bb'] for s in spots) == 25 and sum(s['effective_stack_bb'] >= 15 for s in spots) > 0.15 * len(spots)
    sits = {s['field']['situation'] for s in spots}
    assert {"BB face à l'open du BTN (SB fold)", 'SB face au tapis du BB après son limp'} <= sits
    assert any(s['field_family'] == 'vs_raise' for s in spots)
    raise_q = [s for s in spots if any(o['id'] == 'R' for o in s['field']['options'])]
    assert raise_q and all(next(o for o in s['actions'] if o['id'] == 'R')['to_bb'] in (2.3, 3.0, 3.5) for s in raise_q)
    hu = [s for s in spots if s['table'] == 'heads-up' and s['field']['type'] != 'profil']
    cov = [s for s in hu if len(set(s['stacks_bb'])) > 1]
    assert 0.25 * len(hu) <= len(cov) <= 0.55 * len(hu) and all(min(s['stacks_bb']) == s['effective_stack_bb'] for s in cov)
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'field'))
    import exploit_engine as ee, profils_field as pf
    from hrcdata import NAMES
    f = pf.factors(pf.DEFAULT, 12)                     # compromis Lucho / Lucky : il pousse peu, mais pas seulement le haut de sa range
    r = ee.run_spot('hu', 12, "BB face à l'all-in du SB", ee.SPOTS[('hu', "BB face à l'all-in du SB")], profiles={'rec': f, 'flat': dict(f, shape=False)})
    for h in ('KQo', 'KJo', 'A4o'): assert r['rec']['evs']['paie'][NAMES.index(h)] > max(0, r['flat']['evs']['paie'][NAMES.index(h)])   # redevenus des calls
    for h in ('QJo', 'T8o'): assert r['rec']['evs']['paie'][NAMES.index(h)] < 0                                                        # les mains faibles se couchent
