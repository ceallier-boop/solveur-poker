"""Recette des questions d'équités (CE3, 10/11 ; docs/api/QUIZ_EQUITES.md), indépendante du module : les valeurs attendues sont lues
directement dans spinsacademy/data/equites.json (sans spinsacademy.equities ni equity_quiz), et la table elle-même est recontrôlée sur
des valeurs calculables à la main (couleur au flop, chances de toucher une paire, équités connues contre une main au hasard).
  - tranches : la bonne tranche contient la valeur exacte, à 1,5 point au moins de chaque frontière ; tranche voisine = imprécision ;
  - « forces et faiblesses » : une affirmation est vraie si et seulement si la main porte l'étiquette dans la table, nettement
    (20 % du seuil, 1 point au moins) ; jamais de règle pensée pour deux rangs différents sur une paire, ni dans les forces et faiblesses ;
  - aucun mélange avec les séries GTO ou exploitantes ; bloc « equity » séparé de /users/me/stats ;
  - aucun nom d'expert, aucun « BB perdus », ni « outs » ni « range » dans un énoncé du niveau 1."""
import json, math, os, re
import pytest
from fastapi.testclient import TestClient

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, 'spinsacademy', 'data', 'equites.json'), encoding='utf-8') as f: T = json.load(f)
IDX = {h: i for i, h in enumerate(T['hands'])}
HIT_KEYS = {'suite': ('suite', 'quinte_flush'), 'couleur': ('couleur', 'quinte_flush')}
PAIR_UNCLEAR = {'cartes_hautes', 'depareillee', 'top_paire_souvent', 'top_paire_rarement', 'paire_faible'}
NAMES_RE = re.compile(r'lucho|lucky|pasg8|\bPA\b|coach', re.I)


def raw_value(kind, topic, hand):
    """valeur exacte en dix-millièmes, lue dans la table brute"""
    if kind == 'hit':                                                # docs/api/QUIZ_EQUITES.md : « suite » et « couleur » comptent la quinte flush
        row = dict(zip(T['keys'], T['flop'][IDX[hand]]))
        return sum(row[k] for k in HIT_KEYS.get(topic, (topic,)))
    if topic in ('random', 'hasard', 'au_hasard'): return T['equity_random'][IDX[hand]]
    return next(r for r in T['ranges'] if r['id'] == topic)['equity'][IDX[hand]]


def bounds(label):
    """« moins de 10 % » → (0, 1000) ; « de 10 à 15 % » → (1000, 1500) ; « 25 % ou plus » → (2500, 10001), en dix-millièmes"""
    n = [round(100 * float(x.replace(',', '.'))) for x in re.findall(r'\d+(?:,\d+)?', label)]
    if label.startswith('moins'): return 0, n[0]
    if 'ou plus' in label: return n[0], 10001
    return n[0], n[1]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def series(client, h, kind, seed, size=5):
    s = client.post('/sessions', json={'mode': 'equity', 'size': size, 'seed': seed, 'filters': {'kind': kind}}, headers=h)
    assert s.status_code == 201, s.text
    sid = s.json()['session_id']; out = []
    for i in range(size):
        q = client.get('/quiz/next', params={'session_id': sid}, headers=h).json()['question']
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][0]['id']}, headers=h).json()
        out.append((q, a))
    return sid, out


def level2(client, h):
    assert client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'bases'}, headers=h).status_code in (200, 201)


# ------------------------------------------------------------------ la table, recontrôlée sur des valeurs calculables à la main
def test_table_matches_values_computable_by_hand():
    C = math.comb
    for h in T['hands']:
        row = dict(zip(T['keys'], T['flop'][IDX[h]]))
        flush = row['couleur'] + row['quinte_flush']                                                                # « au moins couleur » compte aussi full et carré
        if len(h) == 3 and h[2] == 's': assert abs(flush - 1e4 * C(11, 3) / C(50, 3)) <= 1, (h, flush)              # trois cartes de sa couleur : 165 / 19 600
        else: assert flush == 0, (h, flush)                                                                          # dépareillée ou paire : impossible au flop
        if len(h) == 2: assert row['au_moins_brelan'] >= round(1e4 * (1 - C(48, 3) / C(50, 3))) - 1, h               # au moins un des deux restants : 11,8 %
        else: assert row['au_moins_paire'] >= round(1e4 * (1 - C(44, 3) / C(50, 3))) - 1, h                          # une des six cartes : 32,4 %
    for h, eq in (('AA', 8520), ('KK', 8240), ('QQ', 7990), ('AKs', 6700), ('AKo', 6530)):                          # équités publiées contre une main au hasard
        assert abs(T['equity_random'][IDX[h]] - eq) <= 25, (h, T['equity_random'][IDX[h]])


def test_table_gives_no_two_rank_rule_to_a_pocket_pair():
    """défaut du 10/11 corrigé par Moteur GTO : aucune paire de poche ne porte une étiquette pensée pour deux rangs différents"""
    bad = {h: [l for l, _ in T['labels'][IDX[h]] if l in PAIR_UNCLEAR] for h in T['hands'] if len(h) == 2}
    assert not any(bad.values()), {h: ls for h, ls in bad.items() if ls}


# ------------------------------------------------------------------ tranches
@pytest.mark.parametrize('kind', ['hit', 'equity'])
def test_band_contains_the_exact_value_with_a_margin(client, kind):
    seen = 0
    for lv in (1, 2):
        h = {'X-Player-Id': f'eq-band-{kind}-{lv}-00'}
        if lv == 2: level2(client, h)
        for seed in range(12):
            _, qa = series(client, h, kind, seed)
            for q, a in qa:
                e = a['equity']; topic = q['topic']; v = raw_value(kind, topic, q['hand'])
                assert e['value_bp'] == v, (q['spot_id'], q['hand'], e['value_bp'], v)
                ids = [o['id'] for o in q['options']]; k = ids.index(e['correct_option']); lo, hi = bounds(q['options'][k]['label_fr'])
                assert lo <= v < hi, (q['spot_id'], q['hand'], v, q['options'][k]['label_fr'])
                assert (lo == 0 or v - lo >= 150) and (hi == 10001 or hi - v >= 150), ('marge < 1,5 point', q['spot_id'], q['hand'], v, lo, hi)
                assert len(ids) == (4 if lv == 1 else len(ids)) and (lv == 1 or len(ids) in (5, 6)), (lv, len(ids))
                got = a['verdict']; d = abs(ids.index(q['options'][0]['id']) - k)            # on a répondu la première option
                assert got == ('correct' if d == 0 else 'imprécision' if d == 1 else 'erreur'), (got, d)
                assert a['regret_mbb'] == 0 and a.get('loss_fr') is None
                seen += 1
    assert seen == 2 * 12 * 5


# ------------------------------------------------------------------ forces et faiblesses
def test_statements_follow_the_table_and_are_clear(client):
    defs = {d['id']: d for d in T['labels_def']}; seen = 0
    for lv in (1, 2):
        h = {'X-Player-Id': f'eq-labels-{lv}-0000'}
        if lv == 2: level2(client, h)
        for seed in range(15):
            _, qa = series(client, h, 'labels', seed)
            for q, a in qa:
                hand = q['hand']; on = dict(T['labels'][IDX[hand]])
                sts = a['equity']['statements']; assert len(sts) == 4
                for s in sts:
                    lid = s['label_id']
                    assert s['true'] == (lid in on), (hand, lid, s['true'], on)
                    if len(hand) == 2: assert lid not in PAIR_UNCLEAR, ('règle à deux rangs posée sur une paire', hand, lid)
                    d = defs[lid]
                    if s['true'] and isinstance(d.get('seuil'), (int, float)) and d.get('sens') in ('>=', '<') and lid in on and str(d.get('unite', '')).startswith('dix-millièmes'):
                        m = max(100, round(0.2 * d['seuil'])); val = on[lid]
                        assert abs(val - d['seuil']) >= m, ('affirmation trop proche du seuil', hand, lid, val, d['seuil'])
                truth = [s['true'] for s in sts]; ok = a['equity']['correct_option']
                assert truth.count(True) == 1 or truth.count(False) == 1, (hand, truth)
                seen += 1
    assert seen == 2 * 15 * 5


def test_strengths_never_use_two_rank_rules_on_a_pair(client):
    h = {'X-Player-Id': 'eq-pairs-strengths-01'}; level2(client, h); pairs = 0
    for seed in range(30):
        _, qa = series(client, h, 'hit', seed)
        for q, a in qa:
            if len(q['hand']) != 2: continue
            pairs += 1; txt = ' '.join(a.get('strengths_fr', []) + a.get('weaknesses_fr', []))
            assert not re.search(r'top paire|cartes hautes|dépareillée|paire faible', txt, re.I), (q['hand'], txt)
    assert pairs >= 5, f'trop peu de paires tirées ({pairs}) pour conclure'


# ------------------------------------------------------------------ séparation des modes et des statistiques
def test_no_equity_question_in_gto_or_exploit_series_and_separate_stats(client):
    h = {'X-Player-Id': 'eq-mix-check-000001'}
    for mode in ('gto', 'exploit'):
        for seed in range(8):
            s = client.post('/sessions', json={'mode': mode, 'seed': seed}, headers=h).json()
            for i in range(s['size']):
                q = client.get('/quiz/next', params={'session_id': s['session_id']}, headers=h).json()['question']
                assert not str(q['spot_id']).startswith('eq:') and q.get('mode') != 'equity', (mode, q['spot_id'])
    before = client.get('/users/me/stats', headers=h).json()
    series(client, h, 'hit', 1); series(client, h, 'labels', 2)
    after = client.get('/users/me/stats', headers=h).json()
    assert after['questions'] == before['questions'], 'les équités ne comptent pas dans le score GTO / exploitant'
    assert after['equity']['questions'] == 10 and after['equity']['sessions'] == 2 and {k['kind'] for k in after['equity']['by_kind']} == {'hit', 'labels'}


def test_texts_no_expert_no_bb_lost_and_level1_words(client):
    h = {'X-Player-Id': 'eq-texts-check-0001'}; texts = []
    for kind in ('hit', 'equity', 'labels'):
        for seed in range(6):
            sid, qa = series(client, h, kind, seed)
            for q, a in qa:
                assert not re.search(r'\bouts?\b|\brange\b', q['prompt_fr'], re.I), ('niveau 1', q['prompt_fr'])
                texts.append(json.dumps([q, a], ensure_ascii=False))
            texts.append(json.dumps(client.get(f'/sessions/{sid}/summary', headers=h).json(), ensure_ascii=False))
    blob = '\n'.join(texts)
    assert not NAMES_RE.search(blob), NAMES_RE.search(blob).group(0)
    assert not re.search(r'BB perdu', blob, re.I)
