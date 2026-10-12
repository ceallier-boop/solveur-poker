"""Calculs de base du solveur postflop (numba) : évaluation des mains, force des combos, abattage contre une range.

Convention : carte = rang * 4 + couleur (rang 0..12 = 2..A) ; combo = couple (a, b) avec a < b, 1 326 combos.
L'évaluateur reprend celui du noyau postflop validé (legacy/conversation/postflop_package : distributions exactes
des mains à 5 et 7 cartes, accord avec un évaluateur indépendant).
"""
import numpy as np
from numba import njit

from ..cards import INDEX

CC = np.array([(a, b) for a in range(52) for b in range(a + 1, 52)], dtype=np.int64)
RANKS = '23456789TJQKA'


def _class_of(a, b):
    r1, r2 = a // 4, b // 4; hi, lo = max(r1, r2), min(r1, r2)
    if hi == lo: return INDEX[RANKS[hi] * 2]
    return INDEX[RANKS[hi] + RANKS[lo] + ('s' if a % 4 == b % 4 else 'o')]


CLASS_OF = np.array([_class_of(a, b) for a, b in CC], dtype=np.int64)


@njit(cache=True)
def _straight_high(mask):
    for hi in range(12, 3, -1):
        if ((mask >> (hi - 4)) & 31) == 31: return hi
    if (mask & (1 << 12)) and (mask & 15) == 15: return 3
    return -1


@njit(cache=True)
def evaln(c, n):
    """valeur d'une main de n cartes (5 à 7) : (catégorie << 20) | départages"""
    rc = np.zeros(13, np.int64); sc = np.zeros(4, np.int64); smask = np.zeros(4, np.int64); mask = 0
    for k in range(n):
        r = c[k] >> 2; s = c[k] & 3
        rc[r] += 1; sc[s] += 1; smask[s] |= (1 << r); mask |= (1 << r)
    for s in range(4):
        if sc[s] >= 5:
            fm = smask[s]; sh = _straight_high(fm)
            if sh >= 0: return (8 << 20) | sh
            score = 0; cnt = 0
            for r in range(12, -1, -1):
                if (fm >> r) & 1 and cnt < 5: score = (score << 4) | r; cnt += 1
            return (5 << 20) | score
    quad = -1; trip = -1; p1 = -1; p2 = -1
    for r in range(12, -1, -1):
        m = rc[r]
        if m == 4: quad = r
        elif m == 3:
            if trip < 0: trip = r
            elif p1 < 0: p1 = r
        elif m == 2:
            if p1 < 0: p1 = r
            elif p2 < 0: p2 = r
    if quad >= 0:
        k = -1
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != quad: k = r; break
        return (7 << 20) | (quad << 4) | k
    if trip >= 0 and p1 >= 0: return (6 << 20) | (trip << 4) | p1
    sh = _straight_high(mask)
    if sh >= 0: return (4 << 20) | sh
    if trip >= 0:
        score = trip; cnt = 0
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != trip and cnt < 2: score = (score << 4) | r; cnt += 1
        return (3 << 20) | score
    if p1 >= 0 and p2 >= 0:
        score = (p1 << 4) | p2
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != p1 and r != p2: score = (score << 4) | r; break
        return (2 << 20) | score
    if p1 >= 0:
        score = p1; cnt = 0
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != p1 and cnt < 3: score = (score << 4) | r; cnt += 1
        return (1 << 20) | score
    score = 0; cnt = 0
    for r in range(12, -1, -1):
        if rc[r] > 0 and cnt < 5: score = (score << 4) | r; cnt += 1
    return score


@njit(cache=True)
def combo_ranks(board, CC):
    """valeur de chaque combo sur un board de 5 cartes ; -1 si le combo touche le board"""
    bm = np.int64(0)
    for k in range(5): bm |= np.int64(1) << board[k]
    out = np.full(1326, -1, np.int64); cards = np.zeros(7, np.int64)
    for k in range(5): cards[2 + k] = board[k]
    for c in range(1326):
        a = CC[c, 0]; b = CC[c, 1]
        if (bm >> a) & 1 or (bm >> b) & 1: continue
        cards[0] = a; cards[1] = b; out[c] = evaln(cards, 7)
    return out


@njit(cache=True)
def _percentile(ranks):
    """rang relatif (0..1) de chaque combo valide parmi les combos valides du board (égalités au milieu)"""
    n = 0
    for c in range(1326):
        if ranks[c] >= 0: n += 1
    order = np.argsort(ranks)
    out = np.full(1326, -1.0)
    i = 0; start = 1326 - n
    while i < n:
        j = i; v = ranks[order[start + i]]
        while j + 1 < n and ranks[order[start + j + 1]] == v: j += 1
        p = (i + j) / 2.0 / max(n - 1, 1)
        for k in range(i, j + 1): out[order[start + k]] = p
        i = j + 1
    return out


@njit(cache=True)
def strength(board, k, full_board, rollouts, CC, seed, squared=False):
    """force de chaque combo sur les k premières cartes du board : rang relatif moyen à la river sur `rollouts` suites
    tirées au hasard (k = 5 : rang exact). Approxime l'équité contre une main aléatoire.
    squared=True : moyenne du carré du rang relatif (EHS²), qui distingue les mains à fort potentiel (tirages)
    des mains moyennes de même force moyenne."""
    if k == 5: return _percentile(combo_ranks(full_board, CC))
    np.random.seed(seed)
    used = np.zeros(52, np.bool_)
    for i in range(k): used[board[i]] = True
    acc = np.zeros(1326); b5 = np.zeros(5, np.int64)
    for i in range(k): b5[i] = board[i]
    for r in range(rollouts):
        m = k; u2 = used.copy()
        while m < 5:
            x = np.random.randint(52)
            if not u2[x]: u2[x] = True; b5[m] = x; m += 1
        pr = _percentile(combo_ranks(b5, CC))
        acc += pr * pr if squared else pr
    out = acc / rollouts
    for c in range(1326):
        if used[CC[c, 0]] or used[CC[c, 1]]: out[c] = -1.0
    return out


@njit(cache=True)
def showdown(ranks, opp, CC):
    """pour chaque combo : masse adverse battue, à égalité, et masse adverse compatible (bloqueurs exacts)"""
    order = np.argsort(ranks)
    card = np.zeros(52); below = 0.0
    win = np.zeros(1326); tie = np.zeros(1326); tot = np.zeros(1326)
    total = 0.0; allc = np.zeros(52)
    for c in range(1326):
        if ranks[c] >= 0 and opp[c] > 0:
            total += opp[c]; allc[CC[c, 0]] += opp[c]; allc[CC[c, 1]] += opp[c]
    i = 0
    while i < 1326:
        c0 = order[i]
        if ranks[c0] < 0: i += 1; continue
        j = i
        while j + 1 < 1326 and ranks[order[j + 1]] == ranks[c0]: j += 1
        gs = 0.0; gcard = np.zeros(52)                       # masse adverse du groupe d'égalité
        for k in range(i, j + 1):
            c = order[k]
            if opp[c] > 0: gs += opp[c]; gcard[CC[c, 0]] += opp[c]; gcard[CC[c, 1]] += opp[c]
        for k in range(i, j + 1):
            c = order[k]; a = CC[c, 0]; b = CC[c, 1]
            win[c] = below - card[a] - card[b]
            tie[c] = gs - gcard[a] - gcard[b] + opp[c]
            tot[c] = total - allc[a] - allc[b] + opp[c]
        for k in range(i, j + 1):
            c = order[k]
            if opp[c] > 0: below += opp[c]; card[CC[c, 0]] += opp[c]; card[CC[c, 1]] += opp[c]
        i = j + 1
    return win, tie, tot


@njit(cache=True)
def compatible(opp, valid, CC):
    """masse adverse compatible (sans carte commune) avec chaque combo valide"""
    total = 0.0; allc = np.zeros(52)
    for c in range(1326):
        if valid[c] and opp[c] > 0: total += opp[c]; allc[CC[c, 0]] += opp[c]; allc[CC[c, 1]] += opp[c]
    out = np.zeros(1326)
    for c in range(1326):
        if valid[c]: out[c] = total - allc[CC[c, 0]] - allc[CC[c, 1]] + (opp[c] if opp[c] > 0 else 0.0)
    return out
