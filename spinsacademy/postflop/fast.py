"""Itérations CFR+ du solveur postflop heads-up entièrement en numba, sur un arbre aplati (ordre préfixe) et un
réservoir de boards précalculés (valeurs des combos à la river, groupes de force par rue)."""
import numpy as np
from numba import njit
from .kernels import CC, combo_ranks, strength


def board_pool(n, buckets, rollouts, seed):
    """n boards tirés au hasard : valeurs à la river (n, 1326), ordre de tri, validité, groupes de force (n, 3, 1326)"""
    rng = np.random.default_rng(seed)
    ranks = np.zeros((n, 1326), np.int64); order = np.zeros((n, 1326), np.int64)
    bucket = np.zeros((n, 3, 1326), np.int64); valid = np.zeros((n, 1326), np.bool_)
    for i in range(n):
        board = rng.choice(52, 5, replace=False).astype(np.int64)
        r = combo_ranks(board, CC); ranks[i] = r; order[i] = np.argsort(r); valid[i] = r >= 0
        s0 = int(rng.integers(1 << 30))
        for k, nc in enumerate((3, 4, 5)):
            s = strength(board, nc, board, rollouts, CC, s0 + nc)
            bucket[i, k] = np.clip((s * buckets).astype(np.int64), 0, buckets - 1)
    return ranks, order, valid, bucket


@njit(cache=True)
def _showdown2(ranks, order, opp, CC, win, tie, tot):
    card = np.zeros(52); below = 0.0; total = 0.0; allc = np.zeros(52); gcard = np.zeros(52)
    for c in range(1326):
        win[c] = 0.0; tie[c] = 0.0; tot[c] = 0.0
        if ranks[c] >= 0 and opp[c] > 0:
            total += opp[c]; allc[CC[c, 0]] += opp[c]; allc[CC[c, 1]] += opp[c]
    i = 0
    while i < 1326:
        c0 = order[i]
        if ranks[c0] < 0:
            i += 1; continue
        j = i
        while j + 1 < 1326 and ranks[order[j + 1]] == ranks[c0]: j += 1
        gs = 0.0
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
            if opp[c] > 0:
                below += opp[c]; card[CC[c, 0]] += opp[c]; card[CC[c, 1]] += opp[c]
                gcard[CC[c, 0]] -= opp[c]; gcard[CC[c, 1]] -= opp[c]
        i = j + 1


@njit(cache=True)
def _compat(opp, valid, CC, out):
    total = 0.0; allc = np.zeros(52)
    for c in range(1326):
        if valid[c] and opp[c] > 0: total += opp[c]; allc[CC[c, 0]] += opp[c]; allc[CC[c, 1]] += opp[c]
    for c in range(1326):
        out[c] = (total - allc[CC[c, 0]] - allc[CC[c, 1]] + (opp[c] if opp[c] > 0 else 0.0)) if valid[c] else 0.0


@njit(cache=True)
def iterate(kind, player, street, c0, c1, winner, nch, child, P, R, Sg, t, ranks, order, valid, bucket,
            r0, r1, update, use_avg, V, reach, CC):
    """un parcours complet sur un board ; V (nœuds, 2, 1326) reçoit les valeurs ; R et Sg mis à jour si update"""
    N = kind.shape[0]; B = R.shape[1]
    sig = np.zeros((N, B, 3))
    for n in range(N):
        if kind[n] != 0: continue
        k = nch[n]
        for b in range(B):
            s = 0.0
            for a in range(k):
                x = Sg[n, b, a] if use_avg else R[n, b, a]
                if x > 0: s += x
            for a in range(k):
                x = Sg[n, b, a] if use_avg else R[n, b, a]
                sig[n, b, a] = (x if x > 0 else 0.0) / s if s > 0 else 1.0 / k
    for c in range(1326):
        reach[0, 0, c] = r0[c] if valid[c] else 0.0; reach[0, 1, c] = r1[c] if valid[c] else 0.0
    for n in range(N):                                   # ordre préfixe : le parent avant les enfants
        if kind[n] != 0: continue
        a = player[n]; st = street[n]
        for k in range(nch[n]):
            ch = child[n, k]
            for c in range(1326):
                reach[ch, 1 - a, c] = reach[n, 1 - a, c]
                reach[ch, a, c] = reach[n, a, c] * sig[n, bucket[st, c], k]
    win = np.zeros(1326); tie = np.zeros(1326); tot = np.zeros(1326)
    for n in range(N - 1, -1, -1):
        if kind[n] == 1:                                 # fold
            for p in range(2):
                _compat(reach[n, 1 - p], valid, CC, tot)
                net = (P + (c1[n] if p == 0 else c0[n])) if winner[n] == p else -(c0[n] if p == 0 else c1[n])
                for c in range(1326): V[n, p, c] = net * tot[c]
        elif kind[n] == 2:                               # abattage (mises égales)
            cc = c0[n]
            for p in range(2):
                _showdown2(ranks, order, reach[n, 1 - p], CC, win, tie, tot)
                for c in range(1326): V[n, p, c] = (P + cc) * win[c] + 0.5 * P * tie[c] - cc * (tot[c] - win[c] - tie[c])
        else:
            a = player[n]; st = street[n]; k = nch[n]
            for c in range(1326):
                va = 0.0; vo = 0.0; b = bucket[st, c]
                for j in range(k):
                    ch = child[n, j]; va += sig[n, b, j] * V[ch, a, c]; vo += V[ch, 1 - a, c]
                V[n, a, c] = va; V[n, 1 - a, c] = vo
            if update:
                for c in range(1326):
                    if not valid[c]: continue
                    b = bucket[st, c]
                    for j in range(k):
                        ch = child[n, j]
                        R[n, b, j] += V[ch, a, c] - V[n, a, c]
                        Sg[n, b, j] += t * reach[n, a, c] * sig[n, b, j]
    if update:                                           # CFR+ : regrets plafonnés à 0 après l'itération
        for n in range(N):
            if kind[n] != 0: continue
            for b in range(B):
                for j in range(nch[n]):
                    if R[n, b, j] < 0: R[n, b, j] = 0.0
