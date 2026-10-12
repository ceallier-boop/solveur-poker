"""Push/fold à 3 joueurs, stacks inégaux (BTN, SB, BB), chip EV (gagnant prend tout).
Règles : un all-in appelé engage min(stack, mise) ; l'excédent non appelé est rendu ; les pots
annexes sont répartis par couches (équité à 3 mains pour la couche principale, heads-up pour
les couches suivantes). Pas de jeu post-flop entre gros stacks sur l'excédent.
"""
import sys, time
import numpy as np
from pushfold import build_classes
from pushfold_raise import rm, notation, pct


def three_way(commits):
    """Couches d'un showdown à 3 : renvoie P1 (pot 3 joueurs), Q[i][j] (pot heads-up i/j), K[i] (rendu - mise)."""
    P1 = 0.0
    Q = np.zeros((3, 3)); K = -np.array(commits, dtype=float)
    levels = sorted(set(commits)); prev = 0.0
    for lvl in levels:
        part = [i for i in range(3) if commits[i] >= lvl - 1e-12]
        amt = (lvl - prev) * len(part)
        if len(part) == 3: P1 += amt
        elif len(part) == 2:
            i, j = part; Q[i][j] += amt; Q[j][i] += amt
        else:
            K[part[0]] += amt
        prev = lvl
    return P1, Q, K


def solve_uneq(E, T, w, st, iters=3000):
    b, s, c = [float(x) for x in st]
    n = 169
    p = w / w.sum()
    T2 = T.reshape(-1, n)
    tv = lambda v: (T2 @ v.astype(np.float32)).reshape(n, n).astype(np.float64)
    Lbs, Lbc, Lsc = min(b, s), min(b, c), min(s, c)
    P1, Q, K = three_way([b, min(s, b), min(c, b)])
    NB = E * (2 * Lbc + 0.5) - Lbc      # BTN-BB heads-up, 0,5 mort (SB fold)
    NS = E * (2 * Lbs + 1.0) - Lbs      # BTN-SB heads-up, 1 mort (BB fold)
    ND = E * 2 * Lsc - Lsc              # SB-BB heads-up (BTN fold)

    def cfvs(pB, aS, cS, d1, d2, d3):
        q0 = p @ (1 - pB); rB = p * pB; rBs = rB.sum()
        d3p = p * d3; sd3 = d3p.sum(); nd3 = p @ (1 - d3)
        W3d = tv(d3p); Ed3 = E @ d3p
        pf = p @ (1 - cS)
        Mb = nd3 * NS + P1 * W3d + Q[0][1] * E * sd3 + (Q[0][2] * Ed3 + K[0] * sd3)[:, None]
        btn_push = pf * (1.5 * (p @ (1 - d2)) + NB @ (p * d2)) + Mb @ (p * cS)
        G1 = ((1 - d1)[None, :] + d1[None, :] * ND) @ p
        s1 = (np.full(n, -0.5 * q0), q0 * G1)
        Ms = nd3 * NS + P1 * W3d + Q[1][0] * E * sd3 + (Q[1][2] * Ed3 + K[1] * sd3)[:, None]
        sc = (np.full(n, -0.5 * rBs), Ms @ rB)
        b1 = (np.full(n, -q0 * (p @ aS)), q0 * (ND @ (p * aS)))
        b2 = (np.full(n, -rBs * pf), pf * (NB @ rB))
        rC = p * cS; rCs = rC.sum()
        b3 = (np.full(n, -rBs * rCs),
              P1 * (tv(rC) @ rB) + Q[2][0] * (E @ rB) * rCs + Q[2][1] * (E @ rC) * rBs + K[2] * rBs * rCs)
        const_bb = 0.5 * q0 * (p @ (1 - aS))
        return btn_push, s1, sc, b1, b2, b3, const_bb

    names = ["btn", "s1", "sc", "b1", "b2", "b3"]
    reg = {k: np.zeros((n, 2)) for k in names}
    avg = {k: np.zeros((n, 2)) for k in names}
    for t in range(1, iters + 1):
        stt = {k: rm(reg[k]) for k in names}
        btn_push, s1, sc, b1, b2, b3, _ = cfvs(*(stt[k][:, 1] for k in names))
        cf = {"btn": (np.zeros(n), btn_push), "s1": s1, "sc": sc, "b1": b1, "b2": b2, "b3": b3}
        for k in names:
            cc = np.stack(cf[k], axis=1)
            v = (stt[k] * cc).sum(axis=1, keepdims=True)
            reg[k] = np.maximum(reg[k] + cc - v, 0)
            avg[k] += t * stt[k]
    fin = {k: (avg[k] / avg[k].sum(axis=1, keepdims=True))[:, 1] for k in names}
    btn_push, s1, sc, b1, b2, b3, const_bb = cfvs(*(fin[k] for k in names))
    pB, aS, cS, d1, d2, d3 = (fin[k] for k in names)
    u_btn = p @ (pB * btn_push); br_btn = p @ np.maximum(0, btn_push)
    u_sb = p @ ((1 - aS) * s1[0] + aS * s1[1] + (1 - cS) * sc[0] + cS * sc[1])
    br_sb = p @ (np.maximum(s1[0], s1[1]) + np.maximum(sc[0], sc[1]))
    u_bb = p @ ((1 - d1) * b1[0] + d1 * b1[1] + (1 - d2) * b2[0] + d2 * b2[1] + (1 - d3) * b3[0] + d3 * b3[1]) + const_bb
    br_bb = p @ (np.maximum(b1[0], b1[1]) + np.maximum(b2[0], b2[1]) + np.maximum(b3[0], b3[1])) + const_bb
    fin["expl"] = float(br_btn + br_sb + br_bb - (u_btn + u_sb + u_bb))
    fin["values"] = (float(u_btn), float(u_sb), float(u_bb))
    return fin
