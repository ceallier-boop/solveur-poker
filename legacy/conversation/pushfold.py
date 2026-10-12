import numpy as np
from numba import njit
import time, sys

RANKS = "23456789TJQKA"

# ---------- classes de mains (grille 13x13, index = row*13+col) ----------
def build_classes():
    combos = np.zeros((169, 12, 2), dtype=np.int64)
    n = np.zeros(169, dtype=np.int64)
    names = []
    for row in range(13):
        for col in range(13):
            idx = row * 13 + col
            if row == col:
                r = 12 - row
                cl = [(r*4+a, r*4+b) for a in range(4) for b in range(a+1, 4)]
                names.append(RANKS[r]*2)
            elif row < col:  # suited
                hi, lo = 12 - row, 12 - col
                cl = [(hi*4+s, lo*4+s) for s in range(4)]
                names.append(RANKS[hi]+RANKS[lo]+"s")
            else:  # offsuit
                hi, lo = 12 - col, 12 - row
                cl = [(hi*4+a, lo*4+b) for a in range(4) for b in range(4) if a != b]
                names.append(RANKS[hi]+RANKS[lo]+"o")
            n[idx] = len(cl)
            for k, c in enumerate(cl):
                combos[idx, k] = c
    return combos, n, names

# ---------- evaluateur 7 cartes ----------
@njit(cache=True)
def straight_high(mask):
    for hi in range(12, 3, -1):
        if ((mask >> (hi-4)) & 31) == 31:
            return hi
    if (mask & (1 << 12)) and (mask & 15) == 15:
        return 3
    return -1

@njit(cache=True)
def eval7(c):
    rc = np.zeros(13, np.int64); sc = np.zeros(4, np.int64); smask = np.zeros(4, np.int64)
    mask = 0
    for k in range(7):
        r = c[k] >> 2; s = c[k] & 3
        rc[r] += 1; sc[s] += 1; smask[s] |= (1 << r); mask |= (1 << r)
    for s in range(4):
        if sc[s] >= 5:
            fm = smask[s]
            sh = straight_high(fm)
            if sh >= 0:
                return (8 << 20) | sh
            score = 0; cnt = 0
            for r in range(12, -1, -1):
                if (fm >> r) & 1 and cnt < 5:
                    score = (score << 4) | r; cnt += 1
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
            if rc[r] > 0 and r != quad:
                k = r; break
        return (7 << 20) | (quad << 4) | k
    if trip >= 0 and p1 >= 0:
        return (6 << 20) | (trip << 4) | p1
    sh = straight_high(mask)
    if sh >= 0:
        return (4 << 20) | sh
    if trip >= 0:
        score = trip; cnt = 0
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != trip and cnt < 2:
                score = (score << 4) | r; cnt += 1
        return (3 << 20) | score
    if p1 >= 0 and p2 >= 0:
        score = (p1 << 4) | p2
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != p1 and r != p2:
                score = (score << 4) | r; break
        return (2 << 20) | score
    if p1 >= 0:
        score = p1; cnt = 0
        for r in range(12, -1, -1):
            if rc[r] > 0 and r != p1 and cnt < 3:
                score = (score << 4) | r; cnt += 1
        return (1 << 20) | score
    score = 0; cnt = 0
    for r in range(12, -1, -1):
        if rc[r] > 0 and cnt < 5:
            score = (score << 4) | r; cnt += 1
    return score

# ---------- matrice d'equite Monte Carlo ----------
@njit(cache=True)
def equity_matrix(combos, ncombos, K, seed):
    np.random.seed(seed)
    E = np.full((169, 169), 0.5)
    cards = np.zeros(7, np.int64)
    used = np.zeros(52, np.bool_)
    for i in range(169):
        for j in range(i+1, 169):
            tot = 0.0
            done = 0
            while done < K:
                a = np.random.randint(ncombos[i]); b = np.random.randint(ncombos[j])
                a0, a1 = combos[i, a, 0], combos[i, a, 1]
                b0, b1 = combos[j, b, 0], combos[j, b, 1]
                if a0 == b0 or a0 == b1 or a1 == b0 or a1 == b1:
                    continue
                used[:] = False
                used[a0] = used[a1] = used[b0] = used[b1] = True
                bd = np.zeros(5, np.int64)
                m = 0
                while m < 5:
                    x = np.random.randint(52)
                    if not used[x]:
                        used[x] = True; bd[m] = x; m += 1
                cards[0] = a0; cards[1] = a1
                for t in range(5): cards[2+t] = bd[t]
                sa = eval7(cards)
                cards[0] = b0; cards[1] = b1
                sb = eval7(cards)
                if sa > sb: tot += 1.0
                elif sa == sb: tot += 0.5
                done += 1
            E[i, j] = tot / K
            E[j, i] = 1.0 - E[i, j]
    return E

# ---------- solveur push/fold HU (jeu fictif) ----------
def solve(E, w, S, iters=6000):
    p = w / w.sum()
    M = S * (2*E - 1)          # gain SB si all-in, ligne = main SB, colonne = main BB
    x = np.full(169, 0.5); y = np.full(169, 0.5)

    def ev_push(y):            # EV du shove pour chaque main du SB
        return (1 - y) @ p + (M * y) @ p  # vecteur sur i

    def br_sb(y):
        return (ev_push(y) > -0.5).astype(float)

    def br_bb(x):
        px = p * x
        # cout (pour SB) si BB call de la main j : sum_i px_i * M_ij ; vs fold : sum_i px_i * 1
        call_cost = px @ M
        fold_cost = px.sum()
        return (call_cost < fold_cost).astype(float)

    for t in range(1, iters+1):
        x += (br_sb(y) - x) / (t + 1)
        y += (br_bb(x) - y) / (t + 1)

    def u(x, y):
        return float(p @ ((1 - x) * -0.5 + x * ev_push(y)))
    expl = u(br_sb(y), y) - u(x, br_bb(x))
    return x, y, expl

def pct(v, w):
    return 100 * float((v * w).sum() / w.sum())

def grid(v, names):
    out = ["     " + " ".join(f"{RANKS[12-c]:>3}" for c in range(13))]
    for r in range(13):
        row = [f"{RANKS[12-r]:>3}  "]
        for c in range(13):
            f = int(round(v[r*13+c]*20))*5   # arrondi a 5 %
            row.append(f"{f:>3}" if 0 < f < 100 else ("  ■" if f >= 100 else "  ·"))
        out.append(" ".join(row))
    return "\n".join(out)

if __name__ == "__main__":
    combos, nc, names = build_classes()
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    t0 = time.time()
    E = equity_matrix(combos, nc, K, 42)
    print(f"Matrice d'équité {169}x{169} ({K} tirages/matchup) en {time.time()-t0:.1f}s")
    np.save("/home/claude/E.npy", E)
    # sanity checks
    idx = {n: i for i, n in enumerate(names)}
    print(f"AA vs KK: {E[idx['AA'], idx['KK']]:.3f} (attendu ~0.82)")
    print(f"AKs vs QQ: {E[idx['AKs'], idx['QQ']]:.3f} (attendu ~0.46)")
    print(f"72o vs AA: {E[idx['72o'], idx['AA']]:.3f} (attendu ~0.12)")
    w = nc.astype(float)
    print("\nStack | SB shove % | BB call % | exploitabilité (BB/main)")
    res = {}
    for S in [4, 6, 8, 10, 12, 15, 20]:
        x, y, ex = solve(E, w, S)
        res[S] = (x, y)
        print(f"{S:>4}BB | {pct(x,w):9.1f}% | {pct(y,w):8.1f}% | {ex:.4f}")
    S = 10
    x, y = res[S]
    print(f"\n=== {S} BB : SB shove (% par main, arrondi 5%) ===")
    print(grid(x, names))
    print(f"\n=== {S} BB : BB call ===")
    print(grid(y, names))
