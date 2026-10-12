"""Push/fold à 3 joueurs en chip EV (Expresso : le gagnant prend tout, donc ICM = chip EV).
BTN / SB / BB, stacks égaux S (en BB), SB 0,5 et BB 1, pas d'ante.
Arbre : BTN push/fold ; si fold -> SB push/fold -> BB call/fold ;
        si push -> SB call/fold -> BB call/fold (BB face à 1 ou 2 all-in).
Hypothèses : mains indépendantes (pas de card removal entre joueurs dans la pondération des ranges).
"""
import sys, time
import numpy as np
from pushfold import build_classes
from pushfold_raise import rm, notation, pct


def solve_3h(E, T, w, S, iters=3000):
    n = 169
    p = w / w.sum()
    T2 = T.reshape(-1, n)                      # (169*169, 169), float32
    Pf = p.astype(np.float32)

    def tv(vec):                                # T @ vec -> (169,169)
        return (T2 @ vec.astype(np.float32)).reshape(n, n).astype(np.float64)

    E1 = E * (2 * S + 1) - S                    # net x vs y, un seul all-in, blind BB morte
    E2 = E * (2 * S + 0.5) - S                  # idem, 0.5 mort
    Sn = S * (2 * E - 1)                        # all-in heads-up sans argent mort

    def cfvs(pB, aS, cS, d1, d2, d3):
        q0 = p @ (1 - pB); rB = p * pB; rBs = rB.sum()
        W3 = tv(p * d3)
        M3 = E1 * (p @ (1 - d3)) + 3 * S * W3 - S * (p @ d3)
        F2 = (1 - d2)[None, :] * 1.5 + d2[None, :] * E2
        btn_push = (p @ (1 - cS)) * (F2 @ p) + M3 @ (p * cS)
        G1 = ((1 - d1)[None, :] + d1[None, :] * Sn) @ p
        s1 = (np.full(n, -0.5 * q0), q0 * G1)
        sc = (np.full(n, -0.5 * rBs), M3 @ rB)
        b1 = (np.full(n, -q0 * (p @ aS)), q0 * (Sn @ (p * aS)))
        pf = p @ (1 - cS)
        b2 = (np.full(n, -rBs * pf), pf * (E2 @ rB))
        rC = p * cS
        b3 = (np.full(n, -rBs * rC.sum()), 3 * S * (tv(rC) @ rB) - S * rBs * rC.sum())
        const_bb = 0.5 * q0 * (p @ (1 - aS))
        return btn_push, s1, sc, b1, b2, b3, const_bb

    names = ["btn", "s1", "sc", "b1", "b2", "b3"]
    reg = {k: np.zeros((n, 2)) for k in names}
    avg = {k: np.zeros((n, 2)) for k in names}
    for t in range(1, iters + 1):
        st = {k: rm(reg[k]) for k in names}
        btn_push, s1, sc, b1, b2, b3, _ = cfvs(*(st[k][:, 1] for k in names))
        cf = {"btn": (np.zeros(n), btn_push), "s1": s1, "sc": sc, "b1": b1, "b2": b2, "b3": b3}
        for k in names:
            c = np.stack(cf[k], axis=1)
            v = (st[k] * c).sum(axis=1, keepdims=True)
            reg[k] = np.maximum(reg[k] + c - v, 0)
            avg[k] += t * st[k]
    fin = {k: avg[k] / avg[k].sum(axis=1, keepdims=True) for k in names}

    # --- écart à l'équilibre (somme des gains de meilleure réponse) + contrôle somme nulle
    btn_push, s1, sc, b1, b2, b3, const_bb = cfvs(*(fin[k][:, 1] for k in names))
    pB, aS, cS, d1, d2, d3 = (fin[k][:, 1] for k in names)
    u_btn = p @ (pB * btn_push); br_btn = p @ np.maximum(0, btn_push)
    u_sb = p @ ((1 - aS) * s1[0] + aS * s1[1] + (1 - cS) * sc[0] + cS * sc[1])
    br_sb = p @ (np.maximum(s1[0], s1[1]) + np.maximum(sc[0], sc[1]))
    u_bb = p @ ((1 - d1) * b1[0] + d1 * b1[1] + (1 - d2) * b2[0] + d2 * b2[1] + (1 - d3) * b3[0] + d3 * b3[1]) + const_bb
    br_bb = p @ (np.maximum(b1[0], b1[1]) + np.maximum(b2[0], b2[1]) + np.maximum(b3[0], b3[1])) + const_bb
    fin["expl"] = float(br_btn + br_sb + br_bb - (u_btn + u_sb + u_bb))
    fin["sumcheck"] = float(u_btn + u_sb + u_bb)
    fin["values"] = (float(u_btn), float(u_sb), float(u_bb))
    return fin


if __name__ == "__main__":
    combos, nc, names = build_classes()
    E = np.load("/home/claude/E2.npy")
    T = np.load("/home/claude/T3.npy")
    w = nc.astype(float)
    stacks = [int(a) for a in sys.argv[1:]] or [4, 6, 8, 10, 12, 15]
    out = ["# Push/fold à 3 joueurs (BTN / SB / BB) en chip EV — Expresso", "",
           "Hypothèses : stacks égaux, SB 0,5 / BB 1, pas d'ante, gagnant prend tout (ICM = chip EV), "
           "équités à 3 mains estimées par Monte Carlo, mains indépendantes (pas de card removal entre joueurs). "
           "Fréquences mixtes entre 5 % et 95 %.", ""]
    print("Stack | BTN push | SB open-shove (BTN fold) | SB call vs BTN | BB call vs SB | BB call vs BTN (SB fold) | BB call vs BTN+SB | écart | somme EV")
    for S in stacks:
        t0 = time.time()
        f = solve_3h(E, T, w, S)
        print(f"{S:>4} | {pct(f['btn'][:,1],w):4.0f}% | {pct(f['s1'][:,1],w):4.0f}% | {pct(f['sc'][:,1],w):4.0f}% | "
              f"{pct(f['b1'][:,1],w):4.0f}% | {pct(f['b2'][:,1],w):4.0f}% | {pct(f['b3'][:,1],w):4.0f}% | "
              f"{f['expl']:.4f} | {f['sumcheck']:+.5f} ({time.time()-t0:.0f}s)", flush=True)
        out += [f"## Stack {S} BB", "",
                f"**BTN — push ({pct(f['btn'][:,1],w):.0f} %)** : {notation(f['btn'][:,1])}", "",
                f"**SB — open-shove après fold du BTN ({pct(f['s1'][:,1],w):.0f} %)** : {notation(f['s1'][:,1])}", "",
                f"**SB — call du push BTN ({pct(f['sc'][:,1],w):.0f} %)** : {notation(f['sc'][:,1])}", "",
                f"**BB — call du push SB (BTN fold) ({pct(f['b1'][:,1],w):.0f} %)** : {notation(f['b1'][:,1])}", "",
                f"**BB — call du push BTN (SB fold) ({pct(f['b2'][:,1],w):.0f} %)** : {notation(f['b2'][:,1])}", "",
                f"**BB — call face à BTN push + SB call ({pct(f['b3'][:,1],w):.0f} %)** : {notation(f['b3'][:,1])}", ""]
        np.savez(f"/home/claude/strat3h_{S}.npz", **{k: f[k] for k in ["btn", "s1", "sc", "b1", "b2", "b3"]})
    open("/home/claude/ranges_3handed.md", "w").write("\n".join(out))
