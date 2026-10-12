"""Noyau postflop autonome (aucune dépendance au modèle préflop) : ranges à 1 326 combinaisons, équités exactes, catégories, tirages, amélioration.

Convention : carte = rang * 4 + couleur ; rang 0..12 (2..A) ; couleur 0..3 (c, d, h, s).
Métriques distinctes (à ne pas confondre dans les corrections de quiz) :
  - équité            : part du pot théorique sur toutes les cartes à venir (gain + moitié des égalités)
  - devant maintenant : la main actuelle bat la range adverse sur le board actuel (sans cartes à venir)
  - amélioration      : probabilité de passer à une catégorie de main supérieure à la turn ou d'ici la river
  - tirages           : probabilité de compléter couleur ou quinte, par énumération exacte
"""
import numpy as np
from itertools import combinations
from numba import njit

RANKS = '23456789TJQKA'; SUITS = 'cdhs'
CC = np.array([(a, b) for a in range(52) for b in range(a + 1, 52)], dtype=np.int64)         # 1 326 combinaisons
MASK = ((np.int64(1) << CC[:, 0]) | (np.int64(1) << CC[:, 1])).astype(np.int64)


def card(s):
    if len(s) != 2 or s[0] not in RANKS or s[1] not in SUITS: raise ValueError(f"carte invalide : {s!r}")
    return RANKS.index(s[0]) * 4 + SUITS.index(s[1])


def card_str(c): return RANKS[c // 4] + SUITS[c % 4]


def class_index(c1, c2):
    """classe de main (grille 13 x 13, indice ligne*13 + colonne) : paires sur la diagonale, assorties au-dessus, dépareillées en dessous"""
    r1, r2 = c1 // 4, c2 // 4
    hi, lo = max(r1, r2), min(r1, r2)
    if hi == lo: return (12 - hi) * 13 + (12 - hi)
    if c1 % 4 == c2 % 4: return (12 - hi) * 13 + (12 - lo)
    return (12 - lo) * 13 + (12 - hi)


CLASS_OF = np.array([class_index(a, b) for a, b in CC], dtype=np.int64)
CLASS_NAMES = []
for _row in range(13):
    for _col in range(13):
        _hi = 12 - _row; _lo = 12 - _col
        if _row == _col: CLASS_NAMES.append(RANKS[_hi] * 2)
        elif _row < _col: CLASS_NAMES.append(RANKS[_hi] + RANKS[_lo] + 's')
        else: CLASS_NAMES.append(RANKS[12 - _col] + RANKS[12 - _row] + 'o')


@njit(cache=True)
def _straight_high(mask):
    for hi in range(12, 3, -1):
        if ((mask >> (hi - 4)) & 31) == 31: return hi
    if (mask & (1 << 12)) and (mask & 15) == 15: return 3
    return -1


@njit(cache=True)
def evaln(c, n):
    """valeur d'une main de n cartes (5 à 7) : (catégorie << 20) | départages ; catégories 0 carte haute ... 8 quinte flush"""
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


# ---------- validation des entrées
def _board(board):
    b = [card(c) if isinstance(c, str) else int(c) for c in board]
    if len(b) not in (3, 4, 5): raise ValueError("le board doit compter 3, 4 ou 5 cartes")
    if len(set(b)) != len(b): raise ValueError("cartes dupliquées sur le board")
    if any(c < 0 or c > 51 for c in b): raise ValueError("carte hors de 0..51")
    return b


def _range(w, bmask, name='range'):
    w = np.asarray(w, float)
    if w.shape != (1326,): raise ValueError(f"{name} : 1 326 poids attendus")
    if not np.all(np.isfinite(w)) or np.any(w < 0): raise ValueError(f"{name} : poids négatifs ou non finis")
    w = w.copy(); w[(MASK & bmask) != 0] = 0.0                 # combinaisons impossibles avec le board
    if w.sum() <= 0: raise ValueError(f"{name} : range vide après exclusion des cartes du board")
    return w


def range_from_class_freq(freq169):
    """poids par combinaison = fréquence de la classe de main (169 valeurs) ; toutes les combinaisons d'une classe ont le même poids"""
    f = np.asarray(freq169, float)
    if f.shape != (169,): raise ValueError("169 fréquences attendues")
    return f[CLASS_OF].copy()


def single_combo(c1, c2):
    a, b = sorted([card(c1), card(c2)])
    w = np.zeros(1326); w[int(np.where((CC[:, 0] == a) & (CC[:, 1] == b))[0][0])] = 1.0
    return w


# ---------- équité exacte
@njit(cache=True)
def _equity(board, runouts, wa, wb, CC, MASK):
    L = len(board); bm = np.int64(0)
    for k in range(L): bm |= (np.int64(1) << board[k])
    ia = np.where(wa > 0)[0]; ib = np.where(wb > 0)[0]
    need = np.zeros(1326, np.bool_)
    for x in ia: need[x] = True
    for x in ib: need[x] = True
    cards = np.zeros(7, np.int64)
    for k in range(L): cards[2 + k] = board[k]
    R = np.zeros(1326, np.int64)
    win = 0.0; tie = 0.0; tot = 0.0
    for u in range(runouts.shape[0]):
        rm = np.int64(0)
        for k in range(runouts.shape[1]):
            cards[2 + L + k] = runouts[u, k]; rm |= (np.int64(1) << runouts[u, k])
        for c in range(1326):
            if not need[c] or (MASK[c] & (bm | rm)) != 0: R[c] = -1
            else:
                cards[0] = CC[c, 0]; cards[1] = CC[c, 1]; R[c] = evaln(cards, 7)
        for x in ia:
            if R[x] < 0: continue
            for y in ib:
                if R[y] < 0 or (MASK[x] & MASK[y]) != 0: continue
                w = wa[x] * wb[y]; tot += w
                if R[x] > R[y]: win += w
                elif R[x] == R[y]: tie += w
    return win, tie, tot


def _runouts(b):
    rest = [c for c in range(52) if c not in b]
    k = 5 - len(b)
    if k == 0: return np.zeros((1, 0), dtype=np.int64)
    return np.array(list(combinations(rest, k)), dtype=np.int64)


def _equity_raw(b, wa, wb):
    bm = sum(1 << c for c in b)
    wa = _range(wa, bm, 'range A'); wb = _range(wb, bm, 'range B')
    win, tie, tot = _equity(np.array(b, dtype=np.int64), _runouts(b), wa, wb, CC, MASK)
    if tot <= 0: raise ValueError("aucun couple de mains compatible entre les deux ranges")
    return win, tie, tot


def equity_breakdown(board, wa, wb):
    """équité exacte de A contre B : tous les tirages restants énumérés, cartes bloquées et égalités comprises"""
    b = _board(board)
    win, tie, tot = _equity_raw(b, wa, wb)
    return dict(win=win / tot, tie=tie / tot, loss=1 - (win + tie) / tot, equity=(win + 0.5 * tie) / tot)


def range_equity(board, wa, wb):
    return equity_breakdown(board, wa, wb)['equity']


def hand_vs_range(hero, board, wb):
    """une main précise (deux cartes) contre une range : cas particulier d'une range réduite à une combinaison"""
    return range_equity(board, single_combo(*hero), wb)


# ---------- main actuelle contre la range adverse (sans cartes à venir)
@njit(cache=True)
def _made(board, CC, MASK, need):
    L = len(board); bm = np.int64(0)
    for k in range(L): bm |= (np.int64(1) << board[k])
    cards = np.zeros(7, np.int64)
    for k in range(L): cards[2 + k] = board[k]
    R = np.zeros(1326, np.int64)
    for c in range(1326):
        if not need[c] or (MASK[c] & bm) != 0: R[c] = -1
        else:
            cards[0] = CC[c, 0]; cards[1] = CC[c, 1]; R[c] = evaln(cards, L + 2)
    return R


@njit(cache=True)
def _compare(R, wa, wb, MASK):
    ahead = 0.0; tie = 0.0; tot = 0.0
    for x in np.where(wa > 0)[0]:
        if R[x] < 0: continue
        for y in np.where(wb > 0)[0]:
            if R[y] < 0 or (MASK[x] & MASK[y]) != 0: continue
            w = wa[x] * wb[y]; tot += w
            if R[x] > R[y]: ahead += w
            elif R[x] == R[y]: tie += w
    return ahead, tie, tot


def made_hand_comparison(board, wa, wb):
    """part de A devant, à égalité et derrière B sur le board actuel (aucune carte à venir) ; différent de l'équité"""
    b = _board(board); bm = sum(1 << c for c in b)
    wa = _range(wa, bm, 'range A'); wb = _range(wb, bm, 'range B')
    R = _made(np.array(b, dtype=np.int64), CC, MASK, (wa > 0) | (wb > 0))
    a, t, tot = _compare(R, wa, wb, MASK)
    return dict(ahead=a / tot, tied=t / tot, behind=1 - (a + t) / tot)


# ---------- catégories, amélioration, tirages
@njit(cache=True)
def _improve(board, CC, MASK, need, horizon):
    """pour chaque combinaison : probabilité de passer à une catégorie supérieure à la turn (horizon 1) ou d'ici la river (horizon 2)"""
    L = len(board); bm = np.int64(0)
    for k in range(L): bm |= (np.int64(1) << board[k])
    out = np.full(1326, -1.0)
    cards = np.zeros(7, np.int64)
    for k in range(L): cards[2 + k] = board[k]
    for c in range(1326):
        if not need[c] or (MASK[c] & bm) != 0: continue
        cards[0] = CC[c, 0]; cards[1] = CC[c, 1]
        base = evaln(cards, L + 2) >> 20
        rest = np.zeros(50, np.int64); m = 0
        for x in range(52):
            if (bm >> x) & 1 or x == CC[c, 0] or x == CC[c, 1]: continue
            rest[m] = x; m += 1
        up = 0; n = 0
        if horizon == 1:
            for t in range(m):
                cards[2 + L] = rest[t]; n += 1
                if (evaln(cards, L + 3) >> 20) > base: up += 1
        else:
            for t in range(m):
                for r in range(t + 1, m):
                    cards[2 + L] = rest[t]; cards[3 + L] = rest[r]; n += 1
                    if (evaln(cards, L + 4) >> 20) > base: up += 1
        out[c] = up / n
    return out


def improvement(board, w, horizon='river'):
    """probabilité moyenne (pondérée par la range) de monter d'au moins une catégorie ; horizon 'turn' ou 'river' (flop uniquement)"""
    b = _board(board)
    if len(b) != 3: raise ValueError("amélioration définie à partir du flop (3 cartes)")
    bm = sum(1 << c for c in b); w = _range(w, bm)
    p = _improve(np.array(b, dtype=np.int64), CC, MASK, w > 0, 1 if horizon == 'turn' else 2)
    ok = p >= 0
    return float((w[ok] * p[ok]).sum() / w[ok].sum())


@njit(cache=True)
def _draws(board, CC, MASK, need):
    """par combinaison : tirage couleur (4 cartes de la couleur, pas de couleur faite), nombre d'outs de quinte à la turn, probabilités de couleur et de quinte ou mieux d'ici la river"""
    bm = np.int64(0)
    for k in range(3): bm |= (np.int64(1) << board[k])
    fd = np.zeros(1326, np.int64); outs = np.zeros(1326, np.int64)
    pfl = np.full(1326, -1.0); pst = np.full(1326, -1.0)
    cards = np.zeros(7, np.int64)
    for k in range(3): cards[2 + k] = board[k]
    for c in range(1326):
        if not need[c] or (MASK[c] & bm) != 0: continue
        cards[0] = CC[c, 0]; cards[1] = CC[c, 1]
        base = evaln(cards, 5) >> 20
        for s in range(4):
            n = 0
            for k in range(5):
                if (cards[k] & 3) == s: n += 1
            if n == 4 and base < 5: fd[c] = 1
        rest = np.zeros(50, np.int64); m = 0
        for x in range(52):
            if (bm >> x) & 1 or x == CC[c, 0] or x == CC[c, 1]: continue
            rest[m] = x; m += 1
        o = 0
        for t in range(m):
            cards[5] = rest[t]
            if base < 4 and (evaln(cards, 6) >> 20) == 4: o += 1
        outs[c] = o
        nf = 0; ns = 0; n = 0
        for t in range(m):
            for r in range(t + 1, m):
                cards[5] = rest[t]; cards[6] = rest[r]; n += 1
                cat = evaln(cards, 7) >> 20
                if cat == 5 or cat == 8: nf += 1
                if cat >= 4: ns += 1
        pfl[c] = nf / n; pst[c] = ns / n
    return fd, outs, pfl, pst


def draws(board, w):
    """tirages de la range sur un flop : parts de la range avec tirage couleur et avec tirage de quinte (outs à la turn), probabilités moyennes de compléter"""
    b = _board(board)
    if len(b) != 3: raise ValueError("tirages définis sur le flop")
    bm = sum(1 << c for c in b); w = _range(w, bm)
    fd, outs, pfl, pst = _draws(np.array(b, dtype=np.int64), CC, MASK, w > 0)
    ok = pfl >= 0; tw = w[ok].sum()
    share = lambda m: float(w[ok & m].sum() / tw)
    return dict(tirage_couleur=share(fd == 1), tirage_quinte_ouvert=share(outs >= 8), tirage_quinte_interne=share((outs >= 4) & (outs < 8)),
                p_couleur_river=float((w[ok] * pfl[ok]).sum() / tw), p_quinte_ou_mieux_river=float((w[ok] * pst[ok]).sum() / tw))


def draws_of_combo(board, c1, c2):
    """détail pour une combinaison précise : outs de quinte à la turn et probabilités de compléter d'ici la river"""
    b = _board(board); w = single_combo(c1, c2); bm = sum(1 << c for c in b)
    fd, outs, pfl, pst = _draws(np.array(b, dtype=np.int64), CC, MASK, w > 0)
    i = int(np.where(w > 0)[0][0])
    return dict(tirage_couleur=bool(fd[i]), outs_quinte=int(outs[i]), p_couleur_river=float(pfl[i]), p_quinte_ou_mieux_river=float(pst[i]))


def flop_categories(board, w):
    """distribution pondérée des catégories sur le flop ; une paire est détaillée (overpair, top pair, paire médiane, paire basse, paire de poche, paire du board)"""
    b = _board(board)
    if len(b) != 3: raise ValueError("catégories définies sur le flop")
    bm = sum(1 << c for c in b); w = _range(w, bm); brs = sorted([c // 4 for c in b], reverse=True)
    names = ['carte haute', 'une paire', 'deux paires', 'brelan', 'quinte', 'couleur', 'full ou mieux', 'full ou mieux', 'full ou mieux']
    cnt = {}; tot = 0.0
    for ci in np.where(w > 0)[0]:
        h = CC[ci]; cards = np.array([h[0], h[1]] + b, dtype=np.int64)
        cat = int(evaln(cards, 5) >> 20)
        if cat == 1:
            hr = sorted([h[0] // 4, h[1] // 4], reverse=True)
            if hr[0] == hr[1]: name = 'overpair' if hr[0] > brs[0] else ('paire de poche sous le board' if hr[0] < brs[2] else 'paire de poche intermédiaire')
            else:
                pr = [r for r in hr if r in brs]
                name = 'paire du board seulement' if not pr else ('top pair' if pr[0] == brs[0] else ('paire médiane' if pr[0] == brs[1] else 'paire basse'))
        else:
            name = names[cat]
            if cat == 0 and any(sum(1 for c in cards if c % 4 == s) == 4 for s in range(4)): name = 'carte haute + tirage couleur'
        cnt[name] = cnt.get(name, 0.0) + w[ci]; tot += w[ci]
    return {k: v / tot for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])}


def street_metrics(board, wa, wb):
    """tableau de bord d'un flop pour deux ranges : chaque métrique est séparée, jamais confondue avec une autre"""
    eq = equity_breakdown(board, wa, wb); mh = made_hand_comparison(board, wa, wb)
    return dict(equity_A=eq['equity'], win_A=eq['win'], tie=eq['tie'], ahead_now_A=mh['ahead'], tied_now=mh['tied'], behind_now_A=mh['behind'],
                improve_turn_A=improvement(board, wa, 'turn'), improve_turn_B=improvement(board, wb, 'turn'),
                improve_river_A=improvement(board, wa, 'river'), improve_river_B=improvement(board, wb, 'river'),
                draws_A=draws(board, wa), draws_B=draws(board, wb))


# =====================================================================================================
# Métriques pédagogiques : avantage de range, avantage de mains fortes, avantage de « nuts », texture, changement flop -> turn
# =====================================================================================================
STRONG = ('overpair', 'top pair', 'deux paires', 'brelan', 'quinte', 'couleur', 'full ou mieux')           # « top pair ou mieux »
DEFAULT_THRESHOLDS = dict(range_adv_pts=5.0, parity_pts=2.0, strong_gap_pts=6.0, nut_gap_pts=8.0, turn_shift_pts=4.0, draw_share=0.20)      # calibrés sur la bibliothèque de 63 flops x 2 lignes


def flop_texture(board):
    """caractéristiques et étiquette de texture d'un flop (déterministe)"""
    b = _board(board)
    if len(b) != 3: raise ValueError("texture définie sur le flop")
    rk = sorted([c // 4 for c in b], reverse=True); su = [c % 4 for c in b]
    n_suits = len(set(su)); paired = len(set(rk)) < 3; trips = len(set(rk)) == 1
    span = rk[0] - rk[2]
    high = RANKS[rk[0]]
    pattern = {1: 'monotone', 2: 'bicolore', 3: 'arc-en-ciel'}[n_suits]
    if trips: structure = 'brelan'
    elif paired: structure = 'pairé'
    elif span <= 4 or (rk[0] == 12 and rk[1] <= 3 and rk[2] <= 3 and False): structure = 'connecté'
    elif span <= 6: structure = 'semi-connecté'
    else: structure = 'déconnecté'
    broadways = sum(1 for r in rk if r >= 8)
    group = 'A' if rk[0] == 12 else ('K-Q' if rk[0] >= 10 else ('J-T' if rk[0] >= 8 else '9 ou moins'))
    return dict(high=high, high_group=group, pattern=pattern, structure=structure, broadways=broadways, span=span, paired=paired,
                label=f"{high}-haut, {structure}, {pattern}")


def canonical_flops():
    """les 1 755 flops distincts à permutation des couleurs près : liste de (flop représentant, nombre de flops équivalents)"""
    from itertools import permutations
    perms = list(permutations(range(4)))
    classes = {}
    for a, b, c in combinations(range(52), 3):
        key = min(tuple(sorted((x // 4) * 4 + p[x % 4] for x in (a, b, c))) for p in perms)
        if key not in classes: classes[key] = [tuple(key), 0]
        classes[key][1] += 1
    return [([card_str(x) for x in rep], n) for rep, n in classes.values()]


def strong_share(board, w):
    cat = flop_categories(board, w)
    return sum(v for k, v in cat.items() if k in STRONG)


def nut_shares(board, wa, wb, top=0.10):
    """part de chaque range parmi les `top` meilleures combinaisons de l'ensemble des deux ranges (poids égaux), sur le flop actuel"""
    b = _board(board); bm = sum(1 << c for c in b)
    wa = _range(wa, bm, 'range A'); wb = _range(wb, bm, 'range B'); wa = wa / wa.sum(); wb = wb / wb.sum()
    R = _made(np.array(b, dtype=np.int64), CC, MASK, (wa > 0) | (wb > 0))
    u = 0.5 * (wa + wb); ok = u > 0
    order = np.argsort(-R[ok], kind='stable'); vals = R[ok][order]; wts = u[ok][order]
    cum = np.cumsum(wts) / wts.sum()
    thr = vals[np.searchsorted(cum, top)] if top < 1 else vals[-1]          # valeur de main à partir de laquelle on est dans le top
    sa = float(wa[(R >= thr) & (wa > 0)].sum()); sb = float(wb[(R >= thr) & (wb > 0)].sum())
    return sa, sb


def turn_shift(board, wa, wb):
    """équité de A sur chaque turn possible ; renvoie la liste (carte, équité, variation par rapport au flop) et le poids de chaque turn"""
    b = _board(board)
    if len(b) != 3: raise ValueError("flop attendu")
    eq0 = equity_breakdown(b, wa, wb)['equity']; rows = []
    for t in range(52):
        if t in b: continue
        try: win, tie, tot = _equity_raw(b + [t], wa, wb)
        except ValueError: continue
        e = (win + 0.5 * tie) / tot
        rows.append(dict(turn=card_str(t), equity=e, delta=e - eq0, weight=tot))
    return eq0, rows


def pedagogical_profile(board, wa, wb, thresholds=None, with_turns=True):
    """tout ce dont la sélection pédagogique a besoin pour un flop et deux ranges (A = premier joueur, B = second)"""
    th = dict(DEFAULT_THRESHOLDS); th.update(thresholds or {})
    b = _board(board); tex = flop_texture(b)
    eq = equity_breakdown(b, wa, wb)['equity']; mh = made_hand_comparison(b, wa, wb)
    sA = strong_share(b, wa); sB = strong_share(b, wb); nA, nB = nut_shares(b, wa, wb)
    dA = draws(b, wa); dB = draws(b, wb)
    out = dict(board=[card_str(c) for c in b], texture=tex, equity_A=eq, range_adv_pts=100 * (eq - 0.5), ahead_now_A=mh['ahead'],
               strong_A=sA, strong_B=sB, strong_gap_pts=100 * (sA - sB), nut_A=nA, nut_B=nB, nut_gap_pts=100 * (nA - nB),
               improve_turn_A=improvement(b, wa, 'turn'), improve_turn_B=improvement(b, wb, 'turn'),
               draw_share_A=dA['tirage_couleur'] + dA['tirage_quinte_ouvert'], draw_share_B=dB['tirage_couleur'] + dB['tirage_quinte_ouvert'])
    if with_turns:
        eq0, rows = turn_shift(b, wa, wb)
        big = sorted([r for r in rows if abs(100 * r['delta']) >= th['turn_shift_pts']], key=lambda r: -abs(r['delta']))
        out.update(turn_max_gain_pts=100 * max(r['delta'] for r in rows), turn_max_loss_pts=100 * min(r['delta'] for r in rows),
                   turn_instructive=[dict(turn=r['turn'], delta_pts=round(100 * r['delta'], 1)) for r in big[:6]], n_turns_shift=len(big))
    out['concepts'] = _concepts(out, th, with_turns)
    return out


def _concepts(out, th, with_turns=True):
    c = []
    if out['range_adv_pts'] >= th['range_adv_pts']: c.append('RANGE_ADVANTAGE_A')
    elif out['range_adv_pts'] <= -th['range_adv_pts']: c.append('RANGE_ADVANTAGE_B')
    elif abs(out['range_adv_pts']) <= th['parity_pts']: c.append('RANGE_PARITY')
    if out['strong_gap_pts'] >= th['strong_gap_pts']: c.append('STRONG_HANDS_ADVANTAGE_A')
    elif out['strong_gap_pts'] <= -th['strong_gap_pts']: c.append('STRONG_HANDS_ADVANTAGE_B')
    if out['nut_gap_pts'] >= th['nut_gap_pts']: c.append('NUT_ADVANTAGE_A')
    elif out['nut_gap_pts'] <= -th['nut_gap_pts']: c.append('NUT_ADVANTAGE_B')
    if max(out['draw_share_A'], out['draw_share_B']) >= th['draw_share']: c.append('DRAW_HEAVY')
    if with_turns and out.get('n_turns_shift', 0) >= 1: c.append('TURN_SHIFT')
    return c


def apply_thresholds(profiles, thresholds=None):
    """recalcule les concepts de profils déjà calculés avec d'autres seuils (le seuil de turn est fixé au calcul des profils)"""
    th = dict(DEFAULT_THRESHOLDS); th.update(thresholds or {})
    for p in profiles: p['concepts'] = _concepts(p, th, 'n_turns_shift' in p)
    return profiles


def select_flops(profiles, concept, k=5, key=None):
    """les k flops qui illustrent le mieux un concept (classement par l'intensité de la mesure associée)"""
    measure = key or {'RANGE_ADVANTAGE_A': lambda p: p['range_adv_pts'], 'RANGE_ADVANTAGE_B': lambda p: -p['range_adv_pts'], 'RANGE_PARITY': lambda p: -abs(p['range_adv_pts']),
                      'STRONG_HANDS_ADVANTAGE_A': lambda p: p['strong_gap_pts'], 'STRONG_HANDS_ADVANTAGE_B': lambda p: -p['strong_gap_pts'],
                      'NUT_ADVANTAGE_A': lambda p: p['nut_gap_pts'], 'NUT_ADVANTAGE_B': lambda p: -p['nut_gap_pts'],
                      'DRAW_HEAVY': lambda p: max(p['draw_share_A'], p['draw_share_B']), 'TURN_SHIFT': lambda p: max(abs(p.get('turn_max_gain_pts', 0)), abs(p.get('turn_max_loss_pts', 0)))}[concept]
    cand = [p for p in profiles if concept in p['concepts']]
    return sorted(cand, key=measure, reverse=True)[:k]
