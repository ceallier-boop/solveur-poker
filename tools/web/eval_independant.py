"""Évaluateur de mains indépendant (responsable des tests), en Python pur, sans aucun import de spinsacademy : sert de référence aux
recettes des questions d'équités avec tableau (outs, board_equity, flop_help ; docs/api/QUIZ_EQUITES.md, v2).

Cartes : chaînes de deux caractères, rang dans « 23456789TJQKA » puis couleur « s h d c » (« As », « 7d »).
  category(cartes)              : 0 carte haute … 8 quinte flush, sur 3 à 7 cartes
  rank7(cartes)                 : clé comparable de la meilleure main de 5 cartes (catégorie, puis départages)
  outs(main, tableau)           : cartes du turn qui améliorent la main selon la règle du 11/11 (Δ main > Δ tableau)
  improve_by_river(main, tableau) : nombre de couples (turn, river) sur 1 081 qui améliorent la main selon la même règle
  equity(main, tableau, poids)  : équité exacte en dix-millièmes, sur les 1 081 suites, contre une main au hasard (poids None) ou contre
                                  une range {classe: poids} (cartes vues retirées, égalité pour moitié)
"""
from itertools import combinations

R = '23456789TJQKA'
DECK = [r + s for r in R for s in 'shdc']


def _parse(c): return R.index(c[0]), c[1]


def _straight_high(ranks):
    """plus haute carte d'une suite parmi des rangs distincts (l'As compte aussi pour 1), ou -1"""
    s = set(ranks)
    if 12 in s: s = s | {-1}
    for top in range(12, 2, -1):
        if all(top - k in s for k in range(5)): return top
    return -1


def rank7(cards):
    rs = [_parse(c) for c in cards]
    by_suit = {}
    for r, s in rs: by_suit.setdefault(s, []).append(r)
    flush = next((sorted(v, reverse=True) for v in by_suit.values() if len(v) >= 5), None)
    if flush:
        sf = _straight_high(flush)
        if sf >= 0: return (8, sf)
    cnt = {}
    for r, _ in rs: cnt[r] = cnt.get(r, 0) + 1
    groups = sorted(((n, r) for r, n in cnt.items()), reverse=True)       # (nombre, rang) décroissants
    distinct = sorted(cnt, reverse=True)
    if groups[0][0] == 4:
        quad = groups[0][1]; return (7, quad, max(r for r in distinct if r != quad))
    trips = [r for n, r in groups if n == 3]; pairs = [r for n, r in groups if n == 2]
    if trips and (len(trips) > 1 or pairs):
        t = trips[0]; p = max([x for x in trips[1:]] + pairs); return (6, t, p)
    if flush: return (5,) + tuple(flush[:5])
    st = _straight_high(distinct)
    if st >= 0: return (4, st)
    if trips:
        t = trips[0]; k = [r for r in distinct if r != t][:2]; return (3, t) + tuple(k)
    if len(pairs) >= 2:
        a, b = pairs[0], pairs[1]; k = max(r for r in distinct if r not in (a, b)); return (2, a, b, k)
    if pairs:
        a = pairs[0]; return (1, a) + tuple([r for r in distinct if r != a][:3])
    return (0,) + tuple(distinct[:5])


def category(cards):
    """catégorie seule ; sur 3 ou 4 cartes, seules les catégories réalisables (pas de suite ni de couleur à moins de 5 cartes)"""
    if len(cards) >= 5: return rank7(cards)[0]
    cnt = {}
    for c in cards: cnt[c[0]] = cnt.get(c[0], 0) + 1
    v = sorted(cnt.values(), reverse=True)
    if v[0] == 4: return 7
    if v[0] == 3: return 3
    if v[0] == 2 and len(v) > 1 and v[1] == 2: return 2
    return 1 if v[0] == 2 else 0


def outs(hand, board):
    seen = set(hand) | set(board); base_m, base_t = category(hand + board), category(board)
    return [c for c in DECK if c not in seen and category(hand + board + [c]) - base_m > category(board + [c]) - base_t]


def improve_by_river(hand, board):
    seen = set(hand) | set(board); rest = [c for c in DECK if c not in seen]
    base_m, base_t = category(hand + board), category(board)
    return sum(1 for t, r in combinations(rest, 2) if category(hand + board + [t, r]) - base_m > category(board + [t, r]) - base_t)


def hand_class(c1, c2):
    (r1, s1), (r2, s2) = _parse(c1), _parse(c2)
    if r1 < r2: r1, r2, s1, s2 = r2, r1, s2, s1
    if r1 == r2: return R[r1] * 2
    return R[r1] + R[r2] + ('s' if s1 == s2 else 'o')


def equity(hand, board, weights=None):
    """équité exacte en dix-millièmes : moyenne, sur les 1 081 suites et les mains adverses compatibles (pondérées), de gain + ½ égalité"""
    seen = set(hand) | set(board); rest = [c for c in DECK if c not in seen]
    villains = [(a, b, 1.0 if weights is None else float(weights.get(hand_class(a, b), 0))) for a, b in combinations(rest, 2)]
    villains = [v for v in villains if v[2] > 0]
    win = tot = 0.0
    for t, r in combinations(rest, 2):
        full = board + [t, r]; me = rank7(hand + full)
        for a, b, w in villains:
            if a in (t, r) or b in (t, r): continue
            op = rank7([a, b] + full)
            win += w * (1.0 if me > op else 0.5 if me == op else 0.0); tot += w
    return round(1e4 * win / tot)
