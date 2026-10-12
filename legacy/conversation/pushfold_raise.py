"""Solveur préflop heads-up avec open-raise (CFR+), sur 169 classes de mains.

Arbre (SB = bouton, BB) :
  SB : fold | raise à `o` BB | shove
    BB vs raise  : fold | call (jeu post-flop approximé) | 3-bet shove
      SB vs 3-bet : fold | call
    BB vs shove  : fold | call
Post-flop approximé par une équité réalisée : équité brute + bonus de position
(zero-sum) et un enjeu T = o + alpha * (S - o) joué par chaque joueur.
Winner-take-all en heads-up : ICM = chip EV.
"""
import sys, time
import numpy as np
from pushfold import build_classes, equity_matrix, RANKS


def rm(reg):
    pos = np.maximum(reg, 0.0)
    s = pos.sum(axis=1, keepdims=True)
    n = reg.shape[1]
    return np.where(s > 0, pos / np.where(s > 0, s, 1), 1.0 / n)


def solve_raise(E, w, S, o=2.0, alpha=0.35, beta=0.03, iters=10000):
    p = w / w.sum()
    A = S * (2 * E - 1)                       # gain SB, all-in
    T = o + alpha * (S - o)
    C = T * (2 * np.clip(E + beta, 0, 1) - 1)  # gain SB, flop vu (equite realisee)
    n = 169
    reg_root = np.zeros((n, 3)); reg_bvr = np.zeros((n, 3))
    reg_bvs = np.zeros((n, 2));  reg_s3 = np.zeros((n, 2))
    avg_root = np.zeros((n, 3)); avg_bvr = np.zeros((n, 3))
    avg_bvs = np.zeros((n, 2));  avg_s3 = np.zeros((n, 2)); wgt_s3 = np.zeros(n)
    wsum = 0.0

    def tree_values(sr, bR, bS, s3):
        U_S = (1 - bS[:, 1])[None, :] + bS[:, 1][None, :] * A
        third = (1 - s3[:, 1])[:, None] * (-o) + s3[:, 1][:, None] * A
        U_R = bR[:, 0][None, :] + bR[:, 1][None, :] * C + bR[:, 2][None, :] * third
        return U_S, U_R

    for t in range(1, iters + 1):
        sr, bR, bS, s3 = rm(reg_root), rm(reg_bvr), rm(reg_bvs), rm(reg_s3)
        U_S, U_R = tree_values(sr, bR, bS, s3)
        # --- SB racine
        cfv = np.stack([np.full(n, -0.5), U_R @ p, U_S @ p], axis=1)
        v = (sr * cfv).sum(axis=1, keepdims=True)
        reg_root = np.maximum(reg_root + cfv - v, 0)
        # --- SB face au 3-bet shove
        r3 = p * bR[:, 2]
        cfv3 = np.stack([np.full(n, -o * r3.sum()), A @ r3], axis=1)
        v3 = (s3 * cfv3).sum(axis=1, keepdims=True)
        reg_s3 = np.maximum(reg_s3 + cfv3 - v3, 0)
        # --- BB face au raise
        reachR = p * sr[:, 1]
        c0 = np.full(n, -reachR.sum())
        c1 = -(reachR @ C)
        c2 = o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A
        cfvR = np.stack([c0, c1, c2], axis=1)
        vR = (bR * cfvR).sum(axis=1, keepdims=True)
        reg_bvr = np.maximum(reg_bvr + cfvR - vR, 0)
        # --- BB face au shove
        reachS = p * sr[:, 2]
        cfvS = np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], axis=1)
        vS = (bS * cfvS).sum(axis=1, keepdims=True)
        reg_bvs = np.maximum(reg_bvs + cfvS - vS, 0)
        # --- moyennes (ponderation lineaire, SB-vs-3bet ponderee par sa reach)
        avg_root += t * sr; avg_bvr += t * bR; avg_bvs += t * bS
        avg_s3 += (t * sr[:, 1])[:, None] * s3; wgt_s3 += t * sr[:, 1]

    sr = avg_root / avg_root.sum(axis=1, keepdims=True)
    bR = avg_bvr / avg_bvr.sum(axis=1, keepdims=True)
    bS = avg_bvs / avg_bvs.sum(axis=1, keepdims=True)
    s3 = np.where(wgt_s3[:, None] > 0, avg_s3 / np.where(wgt_s3 > 0, wgt_s3, 1)[:, None], 0.5)

    # --- exploitabilite (meilleures reponses sequentielles)
    U_S, U_R = tree_values(sr, bR, bS, s3)
    v_sb = float(p @ (sr * np.stack([np.full(n, -0.5), U_R @ p, U_S @ p], axis=1)).sum(axis=1))
    # BR du SB
    third_best = np.maximum(-o, A) if False else None
    r3 = p * bR[:, 2]
    best3 = np.maximum(-o * r3.sum(), A @ r3)               # valeur SB, apres raise+3bet (partielle)
    # utilite SB (i) du raise sous BR du noeud 3bet : somme_j p_j [bf + bc*C + b3*max(...)]
    U_R_br = (bR[:, 0] @ p) + (C @ (p * bR[:, 1])) + best3
    U_S_br = U_S @ p
    br_sb = float(p @ np.maximum.reduce([np.full(n, -0.5), U_R_br, U_S_br]))
    # BR du BB
    reachR = p * sr[:, 1]; reachS = p * sr[:, 2]; reachF = (p * sr[:, 0]).sum()
    cR = np.stack([np.full(n, -reachR.sum()), -(reachR @ C),
                   o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A], axis=1)
    cS = np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], axis=1)
    br_bb = float(p @ (0.5 * reachF + cR.max(axis=1) + cS.max(axis=1)))
    expl = br_sb + br_bb
    return sr, bR, bS, s3, expl


# ---------------- notation des ranges ----------------
def class_meta():
    meta = []
    for row in range(13):
        for col in range(13):
            if row == col: meta.append(("p", 12 - row, 12 - row))
            elif row < col: meta.append(("s", 12 - row, 12 - col))
            else: meta.append(("o", 12 - col, 12 - row))
    return meta

META = class_meta()
R = RANKS


def runs(vals):
    vals = sorted(vals, reverse=True)
    out = []
    for v in vals:
        if out and out[-1][1] == v + 1: out[-1][1] = v
        else: out.append([v, v])
    return out


def notation(freq, lo=0.95, mixed_lo=0.05):
    pure = {i for i in range(169) if freq[i] >= lo}
    mixed = [(i, freq[i]) for i in range(169) if mixed_lo <= freq[i] < lo]
    parts = []
    pr = runs([META[i][1] for i in pure if META[i][0] == "p"])
    for top, bot in pr:
        if top == bot: parts.append(f"{R[top]}{R[top]}")
        elif top == 12: parts.append(f"{R[bot]}{R[bot]}+")
        else: parts.append(f"{R[top]}{R[top]}-{R[bot]}{R[bot]}")
    for kind in ("s", "o"):
        for hi in range(12, -1, -1):
            los = [META[i][2] for i in pure if META[i][0] == kind and META[i][1] == hi]
            for top, bot in runs(los):
                if top == bot: parts.append(f"{R[hi]}{R[top]}{kind}")
                elif top == hi - 1: parts.append(f"{R[hi]}{R[bot]}{kind}+")
                else: parts.append(f"{R[hi]}{R[top]}{kind}-{R[hi]}{R[bot]}{kind}")
    txt = ", ".join(parts) if parts else "—"
    if mixed:
        def nm(i):
            k, h, l = META[i]
            return f"{R[h]}{R[l]}" if k == "p" and False else (R[h]*2 if k == "p" else f"{R[h]}{R[l]}{k}")
        mixed.sort(key=lambda t: (META[t[0]][0] != "p", -META[t[0]][1], -META[t[0]][2]))
        txt += "  |  mixtes : " + ", ".join(f"{nm(i)} {int(round(f*100))}%" for i, f in mixed)
    return txt


def pct(v, w): return 100 * float((v * w).sum() / w.sum())


if __name__ == "__main__":
    combos, nc, names = build_classes()
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    t0 = time.time()
    E = equity_matrix(combos, nc, K, 7)
    print(f"Equité: {time.time()-t0:.0f}s ({K} tirages/matchup)", flush=True)
    w = nc.astype(float)
    stacks = [8, 10, 12, 15, 20, 25]
    lines = ["# Ranges préflop heads-up (SB/BB) — push/fold + open-raise", "",
             "Hypothèses : open-raise à 2 BB, BB peut fold / call / 3-bet shove, "
             "post-flop approximé (équité réalisée, bonus position 3 %, 35 % du stack restant engagé). "
             "Heads-up winner-take-all (ICM = chip EV). Fréquences mixtes entre 5 % et 95 %.", ""]
    print("\nStack | SB: raise / shove / fold | BB vs raise: call / 3bet / fold | BB call vs shove | SB call vs 3bet | expl.")
    for S in stacks:
        t1 = time.time()
        sr, bR, bS, s3, ex = solve_raise(E, w, S)
        print(f"{S:>4} | {pct(sr[:,1],w):4.0f}% / {pct(sr[:,2],w):4.0f}% / {pct(sr[:,0],w):4.0f}% | "
              f"{pct(bR[:,1],w):4.0f}% / {pct(bR[:,2],w):4.0f}% / {pct(bR[:,0],w):4.0f}% | "
              f"{pct(bS[:,1],w):4.0f}% | {pct(s3[:,1],w):4.0f}% | {ex:.4f} ({time.time()-t1:.0f}s)", flush=True)
        lines += [f"## Stack effectif {S} BB", "",
                  f"**SB — raise 2 BB ({pct(sr[:,1],w):.0f} %)** : {notation(sr[:,1])}", "",
                  f"**SB — shove ({pct(sr[:,2],w):.0f} %)** : {notation(sr[:,2])}", "",
                  f"**SB — fold ({pct(sr[:,0],w):.0f} %)** : {notation(sr[:,0])}", "",
                  f"**BB vs raise — call ({pct(bR[:,1],w):.0f} %)** : {notation(bR[:,1])}", "",
                  f"**BB vs raise — 3-bet shove ({pct(bR[:,2],w):.0f} %)** : {notation(bR[:,2])}", "",
                  f"**BB vs shove — call ({pct(bS[:,1],w):.0f} %)** : {notation(bS[:,1])}", "",
                  f"**SB vs 3-bet shove — call ({pct(s3[:,1],w):.0f} %)** : {notation(s3[:,1])}", ""]
        np.savez(f"/home/claude/strat_{S}.npz", sr=sr, bR=bR, bS=bS, s3=s3)
    open("/home/claude/ranges_headsup.md", "w").write("\n".join(lines))
