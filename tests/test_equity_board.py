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
    assert q['board'] == ['Qs', '7s', '2d'] and q['board_display'] == ['Q♠', '7♠', '2♦'] and q['hand_display'] == 'A♠K♠' and q['street'] == 'flop'
    assert q['hero_cards'] == ['As', 'Ks'] and q['villain_cards'] is None and q['ranges'] == []
    assert {o['why_fr'] for o in r['equity']['outs']} == {'fait la couleur', 'fait une paire'} and q['kind'] == 'outs' and q['category_fr'] == 'Équités'
    assert 'outs_count' not in str(q) and '15' not in str(q['prompt_fr'])
    assert not E.valid(sid, 'AsQs')                  # main en double avec le tableau
    assert not E.valid(B.spot_id('river', 1, B.cards_of('Qs7s2d'), 10, 4, 1), 'AsKs')     # niveau 1 : pas de question « river »


def test_default_series_mix_board_kinds():
    """12/11 : l'écran du tableau est livré, outs et équité sur le flop entrent dans les séries sans filtre ; flop_help reste sur demande"""
    kinds = {E.parse(sid)['kind'] for sd in range(6) for sid, _ in E.draw(2, 5, seed=sd)}
    assert kinds == {'hit', 'equity', 'labels', 'outs', 'board_equity'}
    for lv in (1, 2):
        for sid, h in E.draw(lv, 5, seed=3): assert E.valid(sid, h)


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
        assert q['kind'] == 'outs' and len(q['board']) == 3 and len(q['hero_cards']) == 2
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['options'][0]['id']}).json()
        assert a['verdict'] in ('correct', 'imprécision', 'erreur') and a['regret_mbb'] == 0
    s = client.get(f'/sessions/{sid}/summary').json()
    assert s['complete'] and s['bb_per_100'] is None and s['by_theme'][0]['kind'] == 'outs'


# ------------------------------------------------------------------ sorte « board_equity » : équité sur un flop connu
def ref_rank(cards):
    """valeur complète d'une main de 7 cartes (pur Python, indépendant d'evaln) : meilleure combinaison de 5 cartes"""
    best = None
    for five in itertools.combinations(cards, 5):
        rs = sorted((c // 4 for c in five), reverse=True); ss = {c % 4 for c in five}
        cnt = sorted(((rs.count(r), r) for r in set(rs)), reverse=True)
        flush = len(ss) == 1; u = sorted(set(rs), reverse=True)
        st = u[0] if len(u) == 5 and u[0] - u[4] == 4 else 3 if u == [12, 3, 2, 1, 0] else None
        if st is not None and flush: v = (8, st)
        elif cnt[0][0] == 4: v = (7, cnt[0][1], cnt[1][1])
        elif cnt[0][0] == 3 and cnt[1][0] == 2: v = (6, cnt[0][1], cnt[1][1])
        elif flush: v = (5, *rs)
        elif st is not None: v = (4, st)
        elif cnt[0][0] == 3: v = (3, cnt[0][1], *[r for c, r in cnt[1:]])
        elif cnt[0][0] == 2 and cnt[1][0] == 2: v = (2, cnt[0][1], cnt[1][1], cnt[2][1])
        elif cnt[0][0] == 2: v = (1, cnt[0][1], *[r for c, r in cnt[1:]])
        else: v = (0, *rs)
        best = v if best is None or v > best else best
    return best


def ref_equity_vs(hand, villain, board):
    live = [c for c in range(52) if c not in hand + villain + board]
    win = 0.0; n = 0
    for t, r in itertools.combinations(live, 2):
        a, b = ref_rank(hand + board + [t, r]), ref_rank(villain + board + [t, r])
        win += 1.0 if a > b else 0.5 if a == b else 0.0; n += 1
    return win / n


def _combo_index(cs):
    from spinsacademy.postflop.kernels import CC
    a, b = sorted(cs)
    return next(i for i in range(1326) if sorted((int(CC[i, 0]), int(CC[i, 1]))) == [a, b])


@pytest.mark.parametrize('hand,villain,board', [('AsKs', 'QhQd', 'Kd7s2s'), ('9s8s', 'AhKd', 'Ts7d2c'), ('7h7d', '7c6c', 'Ks9c2s')])
def test_hero_equity_against_reference(hand, villain, board):
    import numpy as np
    from spinsacademy.postflop.kernels import CC
    h, v, b = B.cards_of(hand), B.cards_of(villain), B.cards_of(board)
    opp = np.zeros(1326); opp[_combo_index(v)] = 1.0
    win, tot = B.hero_equity(h[0], h[1], np.array(b, np.int64), opp, CC)
    assert abs(win / tot - ref_equity_vs(h, v, b)) < 1e-9


def test_range_equity_is_weighted_mean():
    """contre une range de trois mains pondérées : moyenne pondérée des équités main contre main (chaque main adverse a 990 suites)"""
    import numpy as np
    from spinsacademy.postflop.kernels import CC
    h, b = B.cards_of('JhTh'), B.cards_of('Qs9d2h')
    vill = {('AsAd'): 1.0, ('KcQc'): 0.5, ('8c8d'): 0.25}
    opp = np.zeros(1326)
    for v, w in vill.items(): opp[_combo_index(B.cards_of(v))] = w
    win, tot = B.hero_equity(h[0], h[1], np.array(b, np.int64), opp, CC)
    ref = sum(w * ref_equity_vs(h, B.cards_of(v), b) for v, w in vill.items()) / sum(vill.values())
    assert abs(win / tot - ref) < 1e-9


def test_board_equity_questions():
    n = 0
    for lv in (1, 2):
        for sd in range(4):
            for sid, h in E.draw(lv, 3, seed=sd, kind='board_equity'):
                q = B.eq_parse(sid); b = E._built(sid, h)
                assert lv == 2 or q['topic'] in B.EQ_TOPICS_L1
                f = b['f']; x = b['value'] / 100; c = b['correct']
                lo = f[c - 1] if c else 0; hi = f[c] if c < len(f) else 100
                assert lo <= x < hi and all(abs(x - y) >= E.MARGIN for y in f)
                qq = E.question(sid, h)
                assert len(qq['board']) == 3 and qq['hero_cards'] == [h[:2], h[2:]] and qq['kind'] == 'board_equity'
                assert (qq['ranges'] == []) == (q['topic'] == 'hasard')
                if qq['ranges']: assert qq['ranges'][0]['who'] == 'villain' and 0 < max(qq['ranges'][0]['hands'].values()) <= 1
                r = E.correct(sid, h, qq['options'][c]['id'])
                assert r['verdict'] == 'correct' and r['regret_mbb'] == 0 and [s['street'] for s in r['equity']['by_street']] == ['preflop', 'flop']
                assert 'qui gagnera l\'argent' in r['explanation_fr']
                n += 1
    assert n == 24


# ------------------------------------------------------------------ sorte « flop_help » : ce flop t'aide-t-il plus que la range adverse ?
def test_flop_help_questions():
    import numpy as np
    from spinsacademy import allin
    from spinsacademy.cards import NAMES
    seen = set()
    for lv in (1, 2):
        for sd in range(3):
            for sid, h in E.draw(lv, 3, seed=sd, kind='flop_help'):
                q = B.help_parse(sid); b = E._built(sid, h); hand = B.cards_of(h)
                n, hero, mine, opp = B.scenario(q['topic'])
                assert mine[NAMES.index(B.class_of(hand))] > 0                                  # la main est dans la range du héros
                pre = round(10000 * float(allin.equity_vs_range(np.array(opp))[NAMES.index(B.class_of(hand))]))
                assert b['pre'] == pre
                d = (b['value'] - pre) / 100
                assert (d >= 4.5 and b['correct'] == 0) or (d <= -4.5 and b['correct'] == 2) or (abs(d) <= 1.5 and b['correct'] == 1)
                assert len({c >> 2 for c in q['board']}) > 1
                qq = E.question(sid, h); assert qq['kind'] == 'flop_help' and qq['ranges'][0]['who'] == 'villain' and len(qq['options']) == 3
                r = E.correct(sid, h, f"b{b['correct']}"); assert r['verdict'] == 'correct' and r['equity']['delta_bp'] == b['value'] - pre
                other = f"b{2 - b['correct']}" if b['correct'] != 1 else 'b0'
                assert E.correct(sid, h, other)['verdict'] == ('erreur' if b['correct'] != 1 else 'imprécision')
                seen.add(b['correct'])
    assert seen == {0, 1, 2}


def test_flop_help_value_matches_board_equity_kernel():
    """au flop, la valeur est l'équité exacte de la main contre la range adverse, recalculée ici avec les poids de la banque"""
    import numpy as np
    from spinsacademy.postflop.kernels import CC, CLASS_OF
    sid, h = E.draw(2, 1, seed=4, kind='flop_help')[0]
    q = B.help_parse(sid); hand = B.cards_of(h); opp = np.array(B.scenario(q['topic'])[3])[np.asarray(CLASS_OF)]
    win, tot = B.hero_equity(hand[0], hand[1], np.array(q['board'], np.int64), opp, CC)
    assert E._built(sid, h)['value'] == round(10000 * win / tot)
