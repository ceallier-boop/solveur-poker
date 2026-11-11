"""Questions d'équités avec tableau, sorte « outs » (v2) : vérification par un évaluateur indépendant (pur Python, sans le kernel
evaln), notation, énoncé, API et démo sans mélange."""
import itertools, random
import pytest
from fastapi.testclient import TestClient
from spinsacademy import equity_board as B, equity_quiz as E


# ------------------------------------------------------------------ évaluateur indépendant : catégorie de 3 à 7 cartes
def ref_category(cards):
    ranks = [c // 4 for c in cards]; suits = [c % 4 for c in cards]
    cnt = sorted((ranks.count(r) for r in set(ranks)), reverse=True)

    def straight(rs):
        s = set(rs) | ({-1} if 12 in rs else set())
        return any(all(x in s for x in range(lo, lo + 5)) for lo in range(-1, 9))
    flush_suits = [s for s in range(4) if suits.count(s) >= 5]
    if flush_suits and straight([r for r, s in zip(ranks, suits) if s == flush_suits[0]]): return 8
    if cnt[0] == 4: return 7
    if cnt[0] == 3 and len(cnt) > 1 and cnt[1] >= 2: return 6
    if flush_suits: return 5
    if straight(ranks): return 4
    if cnt[0] == 3: return 3
    if cnt[0] == 2 and len(cnt) > 1 and cnt[1] == 2: return 2
    if cnt[0] == 2: return 1
    return 0


def ref_improves(hand, board, extra):
    return ref_category(hand + board + extra) - ref_category(hand + board) > ref_category(board + extra) - ref_category(board)


def ref_outs(hand, board):
    return sorted(c for c in range(52) if c not in hand + board and ref_improves(hand, board, [c]))


def test_reference_evaluator_agrees_on_categories():
    rnd = random.Random(3)
    for _ in range(3000):
        n = rnd.choice((3, 4, 5, 6, 7)); cs = rnd.sample(range(52), n)
        assert B.category(cs) == ref_category(cs), [B.name(c) for c in cs]


def test_outs_exact_against_reference():
    rnd = random.Random(5)
    for _ in range(300):
        cs = rnd.sample(range(52), 5); hand, board = cs[:2], cs[2:]
        assert sorted(c for c, _ in B.outs(hand, board)) == ref_outs(hand, board)


@pytest.mark.parametrize('hand,board,n', [
    ('AsKs', 'Qs7s2d', 15),        # tirage couleur (9) + paires As/Rois (6)
    ('9s8s', 'Ts7d2c', 14),        # tirage quinte ouvert (8) + paires 9/8 (6)
    ('7h7d', 'Ks9c2s', 2),         # paire de poche sous le tableau : seulement le brelan (une carte qui paire le tableau ne compte pas)
    ('AhQd', 'Kc9s4h', 6),         # deux cartes plus hautes : 6
    ('JhTh', 'Qs9d2h', 14),        # quinte ouverte (8) + paires (6)
])
def test_known_counts(hand, board, n):
    h, b = B.cards_of(hand), B.cards_of(board)
    assert len(B.outs(h, b)) == n == len(ref_outs(h, b))


def test_river_count_against_reference():
    rnd = random.Random(9)
    for _ in range(4):
        cs = rnd.sample(range(52), 5); hand, board = cs[:2], cs[2:]
        live = [c for c in range(52) if c not in cs]
        ref = sum(1 for t, r in itertools.combinations(live, 2) if ref_improves(hand, board, [t, r]))
        assert B.river_count(hand, board) == ref


def _series(level, seeds=range(12)):
    for sd in seeds:
        yield from E.draw(level, 4, seed=sd, kind='outs')


def test_questions_valid_bands_and_margin():
    n = 0
    for lv in (1, 2):
        for sid, h in _series(lv):
            q = B.parse(sid); b = E._built(sid, h); hand = B.cards_of(h)
            N = len(ref_outs(hand, q['board']))
            assert B.MIN_OUTS <= N <= B.MAX_OUTS and ref_category(hand + q['board']) <= 1
            assert lv == 2 or q['topic'] in B.TOPICS_L1
            if q['topic'] == 'nombre':
                assert b['numbers'][b['correct']] == N and len(b['options']) == 4
            else:
                v = 100 * N / 47 if q['topic'] == 'turn' else None
                if v is not None: assert abs(b['value'] / 100 - v) < 0.006
                f = b['f']; x = b['value'] / 100; c = b['correct']
                lo = f[c - 1] if c else 0; hi = f[c] if c < len(f) else 100
                assert lo <= x < hi and all(abs(x - y) >= E.MARGIN for y in f)
                assert len(f) + 1 in ((4,) if lv == 1 else (5, 6))
            n += 1
    assert n >= 80


def test_correction_and_grading():
    sid = B.spot_id('nombre', 2, B.cards_of('Qs7s2d'), 2, 4, 1)
    b = E._built(sid, 'AsKs'); assert b['options'] == ['13 cartes', '15 cartes', '17 cartes', '19 cartes']
    v = [E.correct(sid, 'AsKs', f'b{i}')['verdict'] for i in range(4)]
    assert v == ['imprécision', 'correct', 'imprécision', 'erreur']
    r = E.correct(sid, 'AsKs', 'b1')
    assert r['regret_mbb'] == 0 and r['loss_fr'] is None and r['equity']['outs_count'] == 15 and r['equity']['rule_river_pct'] == 60
    assert 'couleur : 9 cartes' in r['explanation_fr'] and 'Règle des 2 et 4' in r['explanation_fr'] and 'passer devant' in r['explanation_fr']
    q = E.question(sid, 'AsKs')
    assert q['board'] == ['Q♠', '7♠', '2♦'] and q['board_cards'] == ['Qs', '7s', '2d'] and q['hand_display'] == 'A♠K♠' and q['street'] == 'flop'
    assert q['villain_hand'] is None and q['kind'] == 'outs' and q['category_fr'] == 'Équités'
    assert 'outs_count' not in str(q) and '15' not in str(q['prompt_fr'])
    assert not E.valid(sid, 'AsQs')                  # main en double avec le tableau
    assert not E.valid(B.spot_id('river', 1, B.cards_of('Qs7s2d'), 10, 4, 1), 'AsKs')     # niveau 1 : pas de question « river »


def test_default_series_has_no_board_question():
    for sd in range(20):
        assert all(not sid.startswith('eq:outs:') for sid, _ in E.draw(2, 5, seed=sd))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_api_outs_series(client):
    r = client.post('/sessions', json={'mode': 'equity', 'filters': {'kind': 'outs'}, 'size': 4, 'seed': 2}); assert r.status_code == 201
    sid = r.json()['session_id']
    for i in range(4):
        q = client.get('/quiz/next', params={'session_id': sid}).json()['question']
        assert q['kind'] == 'outs' and len(q['board']) == 3 and len(q['hand_cards']) == 2
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][0]['id']}).json()
        assert a['verdict'] in ('correct', 'imprécision', 'erreur') and a['regret_mbb'] == 0
    s = client.get(f'/sessions/{sid}/summary').json()
    assert s['complete'] and s['bb_per_100'] is None and s['by_theme'][0]['kind'] == 'outs'
