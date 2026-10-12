"""Solveurs push/fold avec card removal (blockers) exact au niveau des classes de mains.
- HU : P(main adverse j | ma main i) proportionnelle au nombre de paires de combos disjointes D[i,j].
- 3 joueurs : poids conjoint J[x,y,z] = D[x,y] D[x,z] D[y,z] / (n_x n_y n_z)  (approximation produit des
  disjonctions deux à deux ; exacte sauf cas rares de triples impossibles).
"""
import numpy as np
from pushfold import build_classes
from pushfold_raise import rm

combos, nc, names = build_classes()
n = 169
ncf = nc.astype(float)


def pair_counts():
    masks = []
    for i in range(n):
        masks.append(np.array([(1 << int(combos[i, k, 0])) | (1 << int(combos[i, k, 1])) for k in range(nc[i])],
                              dtype=np.int64))
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = ((masks[i][:, None] & masks[j][None, :]) == 0).sum()
    return D


D = pair_counts()


def pct(v, pm):
    return 100 * float((v * pm).sum() / pm.sum())


# ------------------------------------------------------------------ HU
def solve_hu(E, S, iters=8000, cr=True):
    Dm = D if cr else np.outer(ncf, ncf)
    Pj = Dm / Dm.sum()
    pm = Pj.sum(1)
    Q = Pj / pm[:, None]
    M = S * (2 * E - 1)
    x = np.full(n, 0.5); y = np.full(n, 0.5)
    QM = Q * M
    QMt = Q * M.T

    def br_sb(y):
        return ((Q @ (1 - y) + QM @ y) > -0.5).astype(float)

    def br_bb(x):
        return ((QMt @ x) < (Q @ x)).astype(float)

    for t in range(1, iters + 1):
        x += (br_sb(y) - x) / (t + 1)
        y += (br_bb(x) - y) / (t + 1)

    def u(x, y):
        ev = Q @ (1 - y) + QM @ y
        return float(pm @ ((1 - x) * -0.5 + x * ev))
    expl = u(br_sb(y), y) - u(x, br_bb(x))
    return x, y, expl, pm


# ------------------------------------------------------------------ 3 joueurs
class ThreeHanded:
    def __init__(self, E, T, cr=True):
        self.E = E
        Dm = D if cr else np.outer(ncf, ncf)
        J = Dm[:, :, None] * Dm[:, None, :] * Dm[None, :, :] / (
            ncf[:, None, None] * ncf[None, :, None] * ncf[None, None, :])
        if cr:
            for i in range(n):
                if combos[i, 0, 0] >> 2 == combos[i, 0, 1] >> 2:   # paire : 3 paires identiques impossibles
                    J[i, i, i] = 0.0
        N = J.sum(axis=(1, 2))
        self.pm = N / N.sum()
        Cnd = (J / N[:, None, None]).astype(np.float32)
        del J
        self.Cnd2 = Cnd.reshape(-1, n)
        self.CT2 = (Cnd * T).astype(np.float32).reshape(-1, n)
        self.W1 = (self.Cnd2 @ np.ones(n, np.float32)).reshape(n, n).astype(np.float64)

    def mv(self, M2, v):
        return (M2 @ v.astype(np.float32)).reshape(n, n).astype(np.float64)

    def node_cfvs(self, S, pB, aS, cS, d1, d2, d3):
        E = self.E; W1 = self.W1
        E1 = E * (2 * S + 1) - S; E2 = E * (2 * S + 0.5) - S; Sn = S * (2 * E - 1)
        Cc_cS = self.mv(self.Cnd2, cS); Cc_d3 = self.mv(self.Cnd2, d3)
        CT_d3 = self.mv(self.CT2, d3); Cc_pB = self.mv(self.Cnd2, pB); CT_cS = self.mv(self.CT2, cS)
        X = W1 - Cc_cS
        Mmat = E1 * (W1 - Cc_d3) + 3 * S * CT_d3 - S * Cc_d3
        btn = 1.5 * (X @ (1 - d2)) + (X * E2) @ d2 + Mmat @ cS
        Wb = W1 - Cc_pB
        q0 = Wb.sum(1)
        s1 = (-0.5 * q0, Wb @ (1 - d1) + (Wb * Sn) @ d1)
        rBs = Cc_pB.sum(1)
        sc = (-0.5 * rBs, Mmat @ pB)
        b1 = (-(Wb @ aS), (Wb * Sn) @ aS)
        b2 = (-(X @ pB), (X * E2) @ pB)
        b3 = (-(Cc_cS @ pB), 3 * S * (CT_cS @ pB) - S * (Cc_cS @ pB))
        const_bb = 0.5 * (Wb @ (1 - aS))
        return btn, s1, sc, b1, b2, b3, const_bb

    def values(self, S, strat):
        pB, aS, cS, d1, d2, d3 = strat
        btn, s1, sc, b1, b2, b3, cbb = self.node_cfvs(S, *strat)
        pm = self.pm
        u_btn = pm @ (pB * btn); br_btn = pm @ np.maximum(0, btn)
        u_sb = pm @ ((1 - aS) * s1[0] + aS * s1[1] + (1 - cS) * sc[0] + cS * sc[1])
        br_sb = pm @ (np.maximum(s1[0], s1[1]) + np.maximum(sc[0], sc[1]))
        u_bb = pm @ ((1 - d1) * b1[0] + d1 * b1[1] + (1 - d2) * b2[0] + d2 * b2[1]
                     + (1 - d3) * b3[0] + d3 * b3[1] + cbb)
        br_bb = pm @ (np.maximum(b1[0], b1[1]) + np.maximum(b2[0], b2[1]) + np.maximum(b3[0], b3[1]) + cbb)
        return (u_btn, u_sb, u_bb), (br_btn, br_sb, br_bb)

    def solve(self, S, iters=3000):
        names_ = ["btn", "s1", "sc", "b1", "b2", "b3"]
        reg = {k: np.zeros((n, 2)) for k in names_}
        avg = {k: np.zeros((n, 2)) for k in names_}
        for t in range(1, iters + 1):
            st = {k: rm(reg[k]) for k in names_}
            btn, s1, sc, b1, b2, b3, _ = self.node_cfvs(S, *(st[k][:, 1] for k in names_))
            cf = {"btn": (np.zeros(n), btn), "s1": s1, "sc": sc, "b1": b1, "b2": b2, "b3": b3}
            for k in names_:
                c = np.stack(cf[k], axis=1)
                v = (st[k] * c).sum(axis=1, keepdims=True)
                reg[k] = np.maximum(reg[k] + c - v, 0)
                avg[k] += t * st[k]
        fin = {k: (avg[k] / avg[k].sum(axis=1, keepdims=True))[:, 1] for k in names_}
        u, br = self.values(S, [fin[k] for k in names_])
        fin["expl"] = float(sum(br) - sum(u)); fin["sum"] = float(sum(u))
        return fin
