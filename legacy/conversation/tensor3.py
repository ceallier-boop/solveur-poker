"""Tenseur d'équité à 3 mains : T[i,j,k] = part du pot de la main i contre j et k (all-in 3 joueurs)."""
import sys, time
import numpy as np
from numba import njit
from pushfold import build_classes, eval7


@njit(cache=True)
def sample_triples(combos, ncombos, A, B, C, K, seed):
    np.random.seed(seed)
    n = A.shape[0]
    out = np.zeros((n, 3))
    cards = np.zeros(7, np.int64)
    used = np.zeros(52, np.bool_)
    sc = np.zeros(3, np.int64)
    bd = np.zeros(5, np.int64)
    h = np.zeros((3, 2), np.int64)
    cl = np.zeros(3, np.int64)
    for t in range(n):
        cl[0] = A[t]; cl[1] = B[t]; cl[2] = C[t]
        done = 0
        attempts = 0
        impossible = False
        while done < K:
            attempts += 1
            if attempts > 3000 and done == 0:
                impossible = True
                break
            used[:] = False
            ok = True
            for p in range(3):
                a = np.random.randint(ncombos[cl[p]])
                c0 = combos[cl[p], a, 0]; c1 = combos[cl[p], a, 1]
                if used[c0] or used[c1]:
                    ok = False
                    break
                used[c0] = True; used[c1] = True
                h[p, 0] = c0; h[p, 1] = c1
            if not ok:
                continue
            m = 0
            while m < 5:
                x = np.random.randint(52)
                if not used[x]:
                    used[x] = True; bd[m] = x; m += 1
            best = -1
            for p in range(3):
                cards[0] = h[p, 0]; cards[1] = h[p, 1]
                for q in range(5):
                    cards[2 + q] = bd[q]
                sc[p] = eval7(cards)
                if sc[p] > best:
                    best = sc[p]
            nw = 0
            for p in range(3):
                if sc[p] == best:
                    nw += 1
            for p in range(3):
                if sc[p] == best:
                    out[t, p] += 1.0 / nw
            done += 1
        if impossible:
            for p in range(3):
                out[t, p] = 1.0 / 3.0
        else:
            for p in range(3):
                out[t, p] /= K
    return out


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    combos, nc, names = build_classes()
    idx = np.array([(a, b, c) for a in range(169) for b in range(a, 169) for c in range(b, 169)], dtype=np.int64)
    A, B, C = idx[:, 0].copy(), idx[:, 1].copy(), idx[:, 2].copy()
    print(f"{len(A)} triplets non ordonnés, {K} tirages chacun", flush=True)
    t0 = time.time()
    e = sample_triples(combos, nc, A[:2000], B[:2000], C[:2000], K, 1)  # chauffe + mesure
    dt = time.time() - t0
    print(f"mesure: {dt:.1f}s pour 2000 triplets -> estimation totale {dt*len(A)/2000/60:.1f} min", flush=True)
    t0 = time.time()
    e = sample_triples(combos, nc, A, B, C, K, 12345)
    print(f"Monte Carlo fini en {time.time()-t0:.0f}s", flush=True)
    # symetrisation des classes identiques
    e0, e1, e2 = e[:, 0].copy(), e[:, 1].copy(), e[:, 2].copy()
    ab = A == B; bc = B == C; ac = A == C
    m = ab & ~bc; e0[m] = e1[m] = (e[m, 0] + e[m, 1]) / 2
    m = bc & ~ab; e1[m] = e2[m] = (e[m, 1] + e[m, 2]) / 2
    m = ab & bc; e0[m] = e1[m] = e2[m] = e[m].mean(axis=1)
    es = [e0, e1, e2]
    cls = [A, B, C]
    T = np.zeros((169, 169, 169), dtype=np.float32)
    import itertools
    for perm in itertools.permutations(range(3)):
        T[cls[perm[0]], cls[perm[1]], cls[perm[2]]] = es[perm[0]]
    np.save("/home/claude/T3.npy", T)
    # controles
    idx2 = {n: i for i, n in enumerate(names)}
    aa, kk, qq = idx2["AA"], idx2["KK"], idx2["QQ"]
    print(f"AA vs KK,QQ: {T[aa,kk,qq]:.3f} (attendu ~0.78) ; somme des 3 parts (AA,KK,QQ): "
          f"{T[aa,kk,qq]+T[kk,aa,qq]+T[qq,aa,kk]:.3f} (attendu 1.000)")
    print("72o vs AA,KK:", round(float(T[idx2['72o'], aa, kk]), 3))
