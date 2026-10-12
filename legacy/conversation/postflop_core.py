"""Noyau postflop (prototype) : ranges pondérées à 1 326 combinaisons, équité exacte range contre range, catégories de mains, probabilités d'amélioration."""
import numpy as np
from numba import njit
from pushfold import build_classes, eval7, straight_high
from sim3h import class_table
from hrcdata import NAMES, W

combos_c, nc_c, _ = build_classes()
CLS = class_table(combos_c, nc_c)
CC = np.array([(a, b) for a in range(52) for b in range(a + 1, 52)], dtype=np.int64)      # 1326 combinaisons (carte = rang*4 + couleur)
MASK = ((np.int64(1) << CC[:, 0]) | (np.int64(1) << CC[:, 1])).astype(np.int64)
CLASS_OF = np.array([CLS[a, b] for a, b in CC], dtype=np.int64)
RK = '23456789TJQKA'; SU = 'cdhs'


def card(s): return RK.index(s[0]) * 4 + SU.index(s[1])
def card_s(c): return RK[c // 4] + SU[c % 4]


def range_from_classes(freq169):
    """poids par combinaison = fréquence de la classe (toutes les combinaisons d'une classe ont le même poids)"""
    return np.asarray(freq169, float)[CLASS_OF].copy()


def range_from_hrc_action(node, label):
    """range d'un joueur qui arrive à `node` (poids d'atteinte) et joue l'action `label`"""
    labs = node['labels']; j = labs.index(label)
    w = node['w'] if 'w' in node else np.ones(169)
    return range_from_classes(w * node['played'][:, j])


@njit(cache=True)
def evaln(c, n):
    rc = np.zeros(13, np.int64); sc = np.zeros(4, np.int64); smask = np.zeros(4, np.int64); mask = 0
    for k in range(n):
        r = c[k] >> 2; s = c[k] & 3
        rc[r] += 1; sc[s] += 1; smask[s] |= (1 << r); mask |= (1 << r)
    for s in range(4):
        if sc[s] >= 5:
            fm = smask[s]; sh = straight_high(fm)
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
    sh = straight_high(mask)
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
def _range_equity(board, wa, wb, CC, MASK):
    bm = np.int64(0)
    for k in range(3): bm |= (np.int64(1) << board[k])
    rem = np.zeros(49, np.int64); m = 0
    for c in range(52):
        if not ((bm >> c) & 1): rem[m] = c; m += 1
    ia = np.where(wa > 0)[0]; ib = np.where(wb > 0)[0]
    need = np.zeros(1326, np.bool_)
    for x in ia: need[x] = True
    for x in ib: need[x] = True
    cards = np.zeros(7, np.int64); cards[2] = board[0]; cards[3] = board[1]; cards[4] = board[2]
    R = np.zeros(1326, np.int64)
    eq = 0.0; tot = 0.0
    for t in range(49):
        for r in range(t + 1, 49):
            rm = (np.int64(1) << rem[t]) | (np.int64(1) << rem[r])
            cards[5] = rem[t]; cards[6] = rem[r]
            for c in range(1326):
                if not need[c] or (MASK[c] & (bm | rm)) != 0: R[c] = -1
                else:
                    cards[0] = CC[c, 0]; cards[1] = CC[c, 1]; R[c] = eval7(cards)
            for x in ia:
                if R[x] < 0: continue
                for y in ib:
                    if R[y] < 0 or (MASK[x] & MASK[y]) != 0: continue
                    w = wa[x] * wb[y]; tot += w
                    if R[x] > R[y]: eq += w
                    elif R[x] == R[y]: eq += 0.5 * w
    return eq / tot


def range_equity(board, wa, wb):
    """équité exacte de la range A contre la range B sur un flop (turn et river énumérés), blocages et égalités compris"""
    return _range_equity(np.array([card(c) for c in board], dtype=np.int64), np.asarray(wa, float), np.asarray(wb, float), CC, MASK)


CAT_NAMES = ['carte haute', 'une paire', 'deux paires', 'brelan', 'quinte', 'couleur', 'full ou mieux', 'full ou mieux', 'full ou mieux']


def flop_categories(board, w):
    """distribution pondérée des catégories de mains sur le flop (une paire détaillée : overpair, top, milieu, bas, paire du board)"""
    b = [card(c) for c in board]; bm = sum(1 << c for c in b); brs = sorted([c // 4 for c in b], reverse=True)
    cnt = {}; tot = 0.0
    for ci in np.where(w > 0)[0]:
        if MASK[ci] & bm: continue
        h = CC[ci]; cards = np.array([h[0], h[1]] + b, dtype=np.int64)
        cat = int(evaln(cards, 5) >> 20)
        if cat == 1:
            hr = sorted([h[0] // 4, h[1] // 4], reverse=True)
            if hr[0] == hr[1]: name = 'overpair' if hr[0] > brs[0] else ('paire de poche sous le board' if hr[0] < brs[2] else 'paire de poche intermédiaire')
            else:
                pr = [r for r in hr if r in brs]
                if not pr: name = 'paire du board seulement'
                else: name = 'top pair' if pr[0] == brs[0] else ('paire médiane' if pr[0] == brs[1] else 'paire basse')
        else:
            name = CAT_NAMES[cat]
            if cat == 0 and sum(1 for s in range(4) if sum(1 for c in cards if c % 4 == s) == 4):
                name = 'carte haute + tirage couleur'
        cnt[name] = cnt.get(name, 0.0) + w[ci]; tot += w[ci]
    return {k: v / tot for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])}


def improvement_to_turn(board, w):
    """probabilité qu'une main de la range monte d'une catégorie à la turn (47 turns possibles, pondérées par la range)"""
    b = [card(c) for c in board]; bm = sum(1 << c for c in b)
    up = 0.0; tot = 0.0
    for ci in np.where(w > 0)[0]:
        if MASK[ci] & bm: continue
        h = CC[ci]; base = int(evaln(np.array([h[0], h[1]] + b, dtype=np.int64), 5) >> 20); n_up = 0; n = 0
        for t in range(52):
            if (bm >> t) & 1 or t == h[0] or t == h[1]: continue
            n += 1
            if int(evaln(np.array([h[0], h[1]] + b + [t], dtype=np.int64), 6) >> 20) > base: n_up += 1
        up += w[ci] * n_up / n; tot += w[ci]
    return up / tot
