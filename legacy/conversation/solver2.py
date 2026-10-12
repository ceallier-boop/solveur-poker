"""Solveur HU préflop v2 : fold / limp / raise(o) / shove, avec réponses du BB.
Arbre :
 SB : fold | limp | raise o | shove
  vs limp  : BB check (flop, pot 2) | BB shove  -> SB fold/call
  vs raise : BB fold | call | 3-bet shove       -> SB fold/call
  vs shove : BB fold | call
Post-flop : équité réalisée = clip(E + beta), enjeu par joueur T = mise + alpha*(S - mise).
"""
import sys, time
import numpy as np
from pushfold import build_classes, equity_matrix
from pushfold_raise import rm, notation, pct


def solve2(E, w, S, o=2.0, alpha=0.35, beta=0.03, allow_limp=True, iters=8000):
    n = 169
    p = w / w.sum()
    A = S * (2 * E - 1)
    Er = np.clip(E + beta, 0, 1)
    C = (o + alpha * (S - o)) * (2 * Er - 1)
    Cl = (1 + alpha * (S - 1)) * (2 * Er - 1)
    mask = np.array([1.0, 1.0 if allow_limp else 0.0, 1.0, 1.0])

    def rootrm(reg):
        pos = np.maximum(reg, 0) * mask
        s = pos.sum(axis=1, keepdims=True)
        base = mask / mask.sum()
        return np.where(s > 0, pos / np.where(s > 0, s, 1), base)

    reg_root = np.zeros((n, 4)); reg_bvr = np.zeros((n, 3)); reg_bvs = np.zeros((n, 2))
    reg_s3 = np.zeros((n, 2)); reg_bl = np.zeros((n, 2)); reg_sl = np.zeros((n, 2))
    av = dict(root=np.zeros((n, 4)), bvr=np.zeros((n, 3)), bvs=np.zeros((n, 2)),
              bl=np.zeros((n, 2)), s3=np.zeros((n, 2)), sl=np.zeros((n, 2)))
    w3 = np.zeros(n); wl = np.zeros(n)

    def utilities(bR, bS, bL, s3, sL):
        U_S = (1 - bS[:, 1])[None, :] + bS[:, 1][None, :] * A
        third = (1 - s3[:, 1])[:, None] * (-o) + s3[:, 1][:, None] * A
        U_R = bR[:, 0][None, :] + bR[:, 1][None, :] * C + bR[:, 2][None, :] * third
        lshove = (1 - sL[:, 1])[:, None] * (-1.0) + sL[:, 1][:, None] * A
        U_L = bL[:, 0][None, :] * Cl + bL[:, 1][None, :] * lshove
        return U_S, U_R, U_L

    def step_cfv(reg, cfv, strat):
        v = (strat * cfv).sum(axis=1, keepdims=True)
        return np.maximum(reg + cfv - v, 0)

    for t in range(1, iters + 1):
        sr = rootrm(reg_root); bR = rm(reg_bvr); bS = rm(reg_bvs)
        bL = rm(reg_bl); s3 = rm(reg_s3); sL = rm(reg_sl)
        U_S, U_R, U_L = utilities(bR, bS, bL, s3, sL)
        cfv = np.stack([np.full(n, -0.5), U_L @ p, U_R @ p, U_S @ p], axis=1)
        reg_root = step_cfv(reg_root, cfv, sr)
        r3 = p * bR[:, 2]
        reg_s3 = step_cfv(reg_s3, np.stack([np.full(n, -o * r3.sum()), A @ r3], axis=1), s3)
        rl = p * bL[:, 1]
        reg_sl = step_cfv(reg_sl, np.stack([np.full(n, -rl.sum()), A @ rl], axis=1), sL)
        reachR = p * sr[:, 2]
        cR = np.stack([np.full(n, -reachR.sum()), -(reachR @ C),
                       o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A], axis=1)
        reg_bvr = step_cfv(reg_bvr, cR, bR)
        reachS = p * sr[:, 3]
        reg_bvs = step_cfv(reg_bvs, np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], axis=1), bS)
        reachL = p * sr[:, 1]
        cL = np.stack([-(reachL @ Cl),
                       (reachL * (1 - sL[:, 1])).sum() - (reachL * sL[:, 1]) @ A], axis=1)
        reg_bl = step_cfv(reg_bl, cL, bL)
        av["root"] += t * sr; av["bvr"] += t * bR; av["bvs"] += t * bS; av["bl"] += t * bL
        av["s3"] += (t * sr[:, 2])[:, None] * s3; w3 += t * sr[:, 2]
        av["sl"] += (t * sr[:, 1])[:, None] * sL; wl += t * sr[:, 1]

    nz = lambda a: a / a.sum(axis=1, keepdims=True)
    sr, bR, bS, bL = nz(av["root"]), nz(av["bvr"]), nz(av["bvs"]), nz(av["bl"])
    s3 = np.where(w3[:, None] > 0, av["s3"] / np.where(w3 > 0, w3, 1)[:, None], 0.5)
    sL = np.where(wl[:, None] > 0, av["sl"] / np.where(wl > 0, wl, 1)[:, None], 0.5)

    # exploitabilite
    U_S, U_R, U_L = utilities(bR, bS, bL, s3, sL)
    r3 = p * bR[:, 2]; rl = p * bL[:, 1]
    U_R_br = (bR[:, 0] @ p) + C @ (p * bR[:, 1]) + np.maximum(-o * r3.sum(), A @ r3)
    U_L_br = Cl @ (p * bL[:, 0]) + np.maximum(-rl.sum(), A @ rl)
    cand = np.stack([np.full(n, -0.5), U_L_br, U_R_br, U_S @ p], axis=1) + np.where(mask > 0, 0, -1e9)
    br_sb = float(p @ cand.max(axis=1))
    reachF = (p * sr[:, 0]).sum(); reachL = p * sr[:, 1]; reachR = p * sr[:, 2]; reachS = p * sr[:, 3]
    cR = np.stack([np.full(n, -reachR.sum()), -(reachR @ C),
                   o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A], axis=1)
    cS = np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], axis=1)
    cL = np.stack([-(reachL @ Cl), (reachL * (1 - sL[:, 1])).sum() - (reachL * sL[:, 1]) @ A], axis=1)
    br_bb = float(p @ (0.5 * reachF + cR.max(axis=1) + cS.max(axis=1) + cL.max(axis=1)))
    return dict(sr=sr, bR=bR, bS=bS, bL=bL, s3=s3, sL=sL, expl=br_sb + br_bb)


if __name__ == "__main__":
    combos, nc, names = build_classes()
    t0 = time.time()
    E = equity_matrix(combos, nc, 8000, 11)
    np.save("/home/claude/E2.npy", E)
    print(f"Equité {time.time()-t0:.0f}s", flush=True)
    w = nc.astype(float)

    print("\n== 1) Effet du limp (o=2, alpha=.35, beta=.03) ==")
    print("Stack | sans limp: raise/shove | avec limp: limp/raise/shove | BB check vs limp / shove | expl")
    for S in [10, 15, 20, 25]:
        a = solve2(E, w, S, allow_limp=False, iters=6000)
        b = solve2(E, w, S, allow_limp=True, iters=6000)
        print(f"{S:>4} | {pct(a['sr'][:,2],w):3.0f}% / {pct(a['sr'][:,3],w):3.0f}% | "
              f"{pct(b['sr'][:,1],w):3.0f}% / {pct(b['sr'][:,2],w):3.0f}% / {pct(b['sr'][:,3],w):3.0f}% | "
              f"{pct(b['bL'][:,0],w):3.0f}% / {pct(b['bL'][:,1],w):3.0f}% | {b['expl']:.4f}", flush=True)

    print("\n== 2) Sensibilité (avec limp) : SB raise% | BB call% / 3bet% vs raise ==")
    for S in [15, 20]:
        print(f"-- Stack {S} BB --  alpha beta  o | limp raise shove | BB call 3bet")
        for o in [2.0, 2.5]:
            for alpha in [0.2, 0.35, 0.5]:
                for beta in [0.0, 0.03, 0.06]:
                    r = solve2(E, w, S, o=o, alpha=alpha, beta=beta, iters=5000)
                    print(f"   {alpha:.2f} {beta:.2f} {o:.1f} | {pct(r['sr'][:,1],w):3.0f}% {pct(r['sr'][:,2],w):3.0f}% "
                          f"{pct(r['sr'][:,3],w):3.0f}% | {pct(r['bR'][:,1],w):3.0f}% {pct(r['bR'][:,2],w):3.0f}%", flush=True)
