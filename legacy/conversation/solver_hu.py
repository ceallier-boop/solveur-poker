"""Solveur HU préflop v3 : v2 + iso-raise du BB face au limp.
SB : fold | limp | raise o | shove
 vs limp  : BB check | iso-raise à ri | shove
   vs iso  : SB fold | call | 4-bet shove  -> BB fold/call
   vs shove: SB fold/call
 vs raise : BB fold | call | 3-bet shove    -> SB fold/call
 vs shove : BB fold | call
"""
import sys, time
import numpy as np
from pushfold import build_classes
from pushfold_raise import rm, notation, pct


def solve3(E, w, S, o=2.0, ri=3.0, alpha=0.35, beta=0.03, iters=8000, k=1.0, allow_raise=True, compute_expl=True, overrides=None):
    n = 169
    p = w / w.sum()
    A = S * (2 * E - 1)
    Er = np.clip(0.5 + k * (E - 0.5) + beta, 0, 1)
    C = (o + alpha * (S - o)) * (2 * Er - 1)
    Cl = (1 + alpha * (S - 1)) * (2 * Er - 1)
    Ci = (ri + alpha * (S - ri)) * (2 * Er - 1)
    if overrides is not None: C, Cl, Ci = overrides

    reg = dict(root=np.zeros((n, 4)), bvr=np.zeros((n, 3)), bvs=np.zeros((n, 2)),
               s3=np.zeros((n, 2)), bl=np.zeros((n, 3)), sl=np.zeros((n, 2)),
               si=np.zeros((n, 3)), c4=np.zeros((n, 2)))
    av = {kk: np.zeros_like(v) for kk, v in reg.items()}
    wt = dict(s3=np.zeros(n), sl=np.zeros(n), si=np.zeros(n), c4=np.zeros(n))

    def utilities(st):
        bR, bS, bL, s3, sL, sI, c4 = st["bvr"], st["bvs"], st["bl"], st["s3"], st["sl"], st["si"], st["c4"]
        U_S = (1 - bS[:, 1])[None, :] + bS[:, 1][None, :] * A
        third = (1 - s3[:, 1])[:, None] * (-o) + s3[:, 1][:, None] * A
        U_R = bR[:, 0][None, :] + bR[:, 1][None, :] * C + bR[:, 2][None, :] * third
        lshove = (1 - sL[:, 1])[:, None] * (-1.0) + sL[:, 1][:, None] * A
        four = (1 - c4[:, 1])[None, :] * ri + c4[:, 1][None, :] * A
        iso = (-sI[:, 0])[:, None] + sI[:, 1][:, None] * Ci + sI[:, 2][:, None] * four
        U_L = bL[:, 0][None, :] * Cl + bL[:, 1][None, :] * iso + bL[:, 2][None, :] * lshove
        return U_S, U_R, U_L

    def upd(key, cfv, strat):
        v = (strat * cfv).sum(axis=1, keepdims=True)
        reg[key] = np.maximum(reg[key] + cfv - v, 0)

    for t in range(1, iters + 1):
        st = {kk: rm(v) for kk, v in reg.items()}
        if not allow_raise:
            r_ = np.maximum(reg["root"], 0.0); r_[:, 2] = 0.0
            ssum = r_.sum(axis=1, keepdims=True)
            st["root"] = np.where(ssum > 0, r_ / np.where(ssum > 0, ssum, 1), np.array([1/3, 1/3, 0, 1/3]))
        sr = st["root"]; bR, bS, bL = st["bvr"], st["bvs"], st["bl"]
        s3, sL, sI, c4 = st["s3"], st["sl"], st["si"], st["c4"]
        U_S, U_R, U_L = utilities(st)
        upd("root", np.stack([np.full(n, -0.5), U_L @ p, U_R @ p, U_S @ p], 1), sr)
        if not allow_raise:
            reg["root"][:, 2] = 0.0
        r3 = p * bR[:, 2]
        upd("s3", np.stack([np.full(n, -o * r3.sum()), A @ r3], 1), s3)
        rs = p * bL[:, 2]
        upd("sl", np.stack([np.full(n, -rs.sum()), A @ rs], 1), sL)
        ri_w = p * bL[:, 1]
        upd("si", np.stack([np.full(n, -ri_w.sum()), Ci @ ri_w,
                            ri * (ri_w * (1 - c4[:, 1])).sum() + A @ (ri_w * c4[:, 1])], 1), sI)
        reachR = p * sr[:, 2]
        upd("bvr", np.stack([np.full(n, -reachR.sum()), -(reachR @ C),
                             o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A], 1), bR)
        reachS = p * sr[:, 3]
        upd("bvs", np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], 1), bS)
        reachL = p * sr[:, 1]
        q4 = reachL * sI[:, 2]
        iso_cfv = ((reachL * sI[:, 0]).sum() - (reachL * sI[:, 1]) @ Ci
                   - ri * (1 - c4[:, 1]) * q4.sum() - c4[:, 1] * (q4 @ A))
        upd("bl", np.stack([-(reachL @ Cl), iso_cfv,
                            (reachL * (1 - sL[:, 1])).sum() - (reachL * sL[:, 1]) @ A], 1), bL)
        reach4 = p * sr[:, 1] * sI[:, 2]
        upd("c4", np.stack([-ri * reach4.sum() * np.ones(n), -(reach4 @ A)], 1), c4)
        for kk in ("root", "bvr", "bvs", "bl"):
            av[kk] += t * st[kk]
        for kk, own in (("s3", sr[:, 2]), ("sl", sr[:, 1]), ("si", sr[:, 1]), ("c4", bL[:, 1])):
            av[kk] += (t * own)[:, None] * st[kk]; wt[kk] += t * own

    fin = {}
    for kk in ("root", "bvr", "bvs", "bl"):
        fin[kk] = av[kk] / av[kk].sum(axis=1, keepdims=True)
    for kk in ("s3", "sl", "si", "c4"):
        d = wt[kk][:, None]
        fin[kk] = np.where(d > 0, av[kk] / np.where(d > 0, d, 1), 1.0 / av[kk].shape[1])

    if not compute_expl:
        return fin
    # --- exploitabilite (meilleures reponses sequentielles)
    sr, bR, bS, bL = fin["root"], fin["bvr"], fin["bvs"], fin["bl"]
    s3, sL, sI, c4 = fin["s3"], fin["sl"], fin["si"], fin["c4"]
    U_S, _, _ = utilities(fin)
    r3 = p * bR[:, 2]
    U_R_br = (bR[:, 0] @ p) + C @ (p * bR[:, 1]) + np.maximum(-o * r3.sum(), A @ r3)
    rs = p * bL[:, 2]; riw = p * bL[:, 1]
    node_i = np.maximum.reduce([np.full(n, -riw.sum()), Ci @ riw,
                                ri * (riw * (1 - c4[:, 1])).sum() + A @ (riw * c4[:, 1])])
    U_L_br = Cl @ (p * bL[:, 0]) + node_i + np.maximum(-rs.sum(), A @ rs)
    br_sb = float(p @ np.maximum.reduce([np.full(n, -0.5), U_L_br, U_R_br, U_S @ p]))
    reachF = (p * sr[:, 0]).sum(); reachR = p * sr[:, 2]; reachS = p * sr[:, 3]; reachL = p * sr[:, 1]
    cR = np.stack([np.full(n, -reachR.sum()), -(reachR @ C),
                   o * (reachR * (1 - s3[:, 1])).sum() - (reachR * s3[:, 1]) @ A], 1)
    cS = np.stack([np.full(n, -reachS.sum()), -(reachS @ A)], 1)
    q4 = reachL * sI[:, 2]
    iso_br = ((reachL * sI[:, 0]).sum() - (reachL * sI[:, 1]) @ Ci
              + np.maximum(-ri * q4.sum(), -(q4 @ A)))
    cL = np.stack([-(reachL @ Cl), iso_br,
                   (reachL * (1 - sL[:, 1])).sum() - (reachL * sL[:, 1]) @ A], 1)
    br_bb = float(p @ (0.5 * reachF + cR.max(1) + cS.max(1) + cL.max(1)))
    fin["expl"] = br_sb + br_bb
    return fin


if __name__ == "__main__":
    combos, nc, names = build_classes()
    E = np.load("/home/claude/E2.npy")
    w = nc.astype(float)
    out = ["# Ranges préflop heads-up v3 (fold / limp / raise / shove, iso-raise du BB)", "",
           "Hypothèses : open 2 BB, iso-raise du BB à 3 BB, 3-bet/4-bet = shove, post-flop approximé "
           "(équité réalisée, bonus de position 3 %, 35 % du stack restant engagé). "
           "Heads-up winner-take-all (ICM = chip EV). Mixtes affichés entre 5 % et 95 %.", ""]
    print("Stack | SB limp/raise/shove/fold | BB vs limp: check/iso/shove | SB vs iso: call/4bet | BB vs raise: call/3bet | expl")
    for S in [10, 15, 20, 25]:
        t0 = time.time()
        f = solve3(E, w, S)
        sr, bL, sI, bR, bS, sL, s3 = f["root"], f["bl"], f["si"], f["bvr"], f["bvs"], f["sl"], f["s3"]
        print(f"{S:>4} | {pct(sr[:,1],w):3.0f}/{pct(sr[:,2],w):3.0f}/{pct(sr[:,3],w):3.0f}/{pct(sr[:,0],w):3.0f} | "
              f"{pct(bL[:,0],w):3.0f}/{pct(bL[:,1],w):3.0f}/{pct(bL[:,2],w):3.0f} | "
              f"{pct(sI[:,1],w):3.0f}/{pct(sI[:,2],w):3.0f} | {pct(bR[:,1],w):3.0f}/{pct(bR[:,2],w):3.0f} | "
              f"{f['expl']:.4f} ({time.time()-t0:.0f}s)", flush=True)
        out += [f"## Stack effectif {S} BB", "",
                f"**SB — limp ({pct(sr[:,1],w):.0f} %)** : {notation(sr[:,1])}", "",
                f"**SB — raise 2 BB ({pct(sr[:,2],w):.0f} %)** : {notation(sr[:,2])}", "",
                f"**SB — shove ({pct(sr[:,3],w):.0f} %)** : {notation(sr[:,3])}", "",
                f"**SB — fold ({pct(sr[:,0],w):.0f} %)** : {notation(sr[:,0])}", "",
                f"**BB vs limp — iso-raise 3 BB ({pct(bL[:,1],w):.0f} %)** : {notation(bL[:,1])}", "",
                f"**BB vs limp — shove ({pct(bL[:,2],w):.0f} %)** : {notation(bL[:,2])}", "",
                f"**SB limp vs iso — call ({pct(sI[:,1],w):.0f} %)** : {notation(sI[:,1])}", "",
                f"**SB limp vs iso — 4-bet shove ({pct(sI[:,2],w):.0f} %)** : {notation(sI[:,2])}", "",
                f"**SB limp vs shove — call ({pct(sL[:,1],w):.0f} %)** : {notation(sL[:,1])}", "",
                f"**BB vs raise — call ({pct(bR[:,1],w):.0f} %)** : {notation(bR[:,1])}", "",
                f"**BB vs raise — 3-bet shove ({pct(bR[:,2],w):.0f} %)** : {notation(bR[:,2])}", "",
                f"**BB vs shove — call ({pct(bS[:,1],w):.0f} %)** : {notation(bS[:,1])}", ""]
    open("/home/claude/ranges_v3.md", "w").write("\n".join(out))

    print("\nSensibilité à 20 BB (alpha, beta) : SB limp/raise/shove | BB iso vs limp | BB call/3bet vs raise")
    for alpha, beta in [(0.2, 0.03), (0.5, 0.03), (0.35, 0.0), (0.35, 0.06)]:
        f = solve3(E, w, 20, alpha=alpha, beta=beta, iters=4000)
        sr, bL, bR = f["root"], f["bl"], f["bvr"]
        print(f"  a={alpha:.2f} b={beta:.2f} | {pct(sr[:,1],w):3.0f}/{pct(sr[:,2],w):3.0f}/{pct(sr[:,3],w):3.0f} | "
              f"{pct(bL[:,1],w):3.0f} | {pct(bR[:,1],w):3.0f}/{pct(bR[:,2],w):3.0f} | expl {f['expl']:.4f}", flush=True)
