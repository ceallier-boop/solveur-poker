"""Modèles de valeur des fins de tour « flop » (au moins deux joueurs avec des jetons derrière).

Showdown : chaque joueur réalise exactement son équité préflop (aucune mise après le flop). Référence la plus simple.

Realization : pour chaque fin de tour à deux joueurs, le sous-jeu postflop heads-up est résolu (spinsacademy.postflop)
avec les ranges qui y arrivent. On en tire, pour chaque classe, une correction additive de réalisation :
    part du pot de p avec i contre j = P * E[i, j] + delta_p[i] - delta_q[j]
(somme nulle par construction), ajustée pour reproduire les gains postflop G de chaque classe contre la range adverse.
Fins de tour à trois joueurs actifs (pas de solveur postflop à 3) : chaque paire de joueurs est résolue en
sous-jeu heads-up avec le pot réel et les deux ranges ; la correction d'un joueur est la moyenne de ses deux duels, et
    part de p avec i contre j et k = P * T[i, j, k] + delta_p[i] - (delta_q[j] + delta_s[k]) / 2
(somme nulle par construction). C'est une approximation : elle capte la position et la jouabilité, pas les
interactions propres à trois joueurs (protection, sandwich).
"""
import numpy as np
from ..cards import DISJOINT as D, W as NCOMB
from ..allin import E

POSTFLOP_ORDER = {3: (1, 2, 0), 2: (1, 0)}     # 3 joueurs : SB, BB, BTN ; heads-up : BB puis SB (bouton)


class Showdown:
    name = 'showdown'

    def value(self, solver, nd, p, reach):
        return solver.showdown_value(nd, p, reach)


def fit_offsets(P, w0, w1, G0, G1, iters=200):
    """deltas (d0, d1) tels que le modèle P*E + d0[i] - d1[j] reproduise G0 (contre w1) et G1 (contre w0)"""
    m1 = D @ w1; m0 = D.T @ w0
    E0 = (D * E) @ w1 / np.maximum(m1, 1e-12)                   # équité moyenne de i contre la range 1
    E1 = (D * (1 - E)).T @ w0 / np.maximum(m0, 1e-12)           # équité moyenne de j contre la range 0
    d0 = np.zeros(169); d1 = np.zeros(169)
    for _ in range(iters):
        d0 = G0 - P * E0 + (D @ (w1 * d1)) / np.maximum(m1, 1e-12)
        d1 = G1 - P * E1 + (D.T @ (w0 * d0)) / np.maximum(m0, 1e-12)
        k = float((w1 * NCOMB * d1).sum() / max((w1 * NCOMB).sum(), 1e-12)); d0 -= k; d1 -= k   # jauge : delta moyen de la range 1 nul
    return d0, d1


class Realization:
    name = 'realization'

    def __init__(self):
        self.offsets = {}          # id du nœud terminal -> {joueur: delta (169)}
        self._pending = {}

    def value(self, solver, nd, p, reach):
        off = self.offsets.get(nd.id)
        if off is None or nd.folded[p]: return solver.showdown_value(nd, p, reach)     # joueur couché : il perd sa mise
        active = [q for q in range(solver.n) if not nd.folded[q]]
        if len(active) == 3: return self._value3(solver, nd, p, reach, off)
        q = active[0] if active[1] == p else active[1]
        P = float(sum(nd.contrib)); rq = reach[q]; dp, dq = off[p], off[q]
        v = P * ((D * E) @ rq) + dp * (D @ rq) - D @ (rq * dq) - nd.contrib[p] * (D @ rq)
        if solver.n == 2: return v
        s = [x for x in range(3) if x not in (p, q)][0]
        return v * (D @ reach[s]) / NCOMB

    def _value3(self, solver, nd, p, reach, off):
        from .cfr import equity3
        q, s = [x for x in range(3) if x != p]; rq, rs = reach[q], reach[s]
        P = float(sum(nd.contrib)); Dq, Ds = D @ rq, D @ rs
        Y = (equity3()[1] @ rs.astype(np.float32)).reshape(169, 169).astype(np.float64)
        return (P * (Y @ rq) + (off[p] - nd.contrib[p]) * Dq * Ds / NCOMB
                - 0.5 * ((D @ (rq * off[q])) * Ds + (D @ (rs * off[s])) * Dq) / NCOMB)

    @staticmethod
    def aggressor(solver, nd):
        """dernier relanceur préflop (indice du joueur), None si le pot est limpé"""
        for tok in reversed(nd.key.split('_')):
            name, _, act = tok.partition('-')
            if act.startswith('raise') or act == 'allin': return solver.tree.names.index(name)
        return None

    @staticmethod
    def subgames(solver):
        """duels postflop à résoudre : (nœud, OOP, IP, pot, tapis restant, agresseur du duel : 0 OOP, 1 IP, -1 aucun ou tiers) ;
        trois duels par fin de tour à trois"""
        out = []
        for nd in solver.tree.terminals():
            if nd.terminal != 'flop': continue
            active = [q for q in range(solver.n) if not nd.folded[q]]
            order = [q for q in POSTFLOP_ORDER[solver.n] if q in active]
            stack = min(solver.tree.st[q] - nd.contrib[q] for q in active)
            ag = Realization.aggressor(solver, nd)
            for a in range(len(order)):
                for b in range(a + 1, len(order)):
                    rel = 0 if ag == order[a] else 1 if ag == order[b] else -1
                    out.append((nd, order[a], order[b], float(sum(nd.contrib)), float(stack), rel))
        return out

    def store(self, nd, o, i, d0, d1, damping):
        """enregistre les corrections d'un duel ; pour une fin de tour à trois, moyenne des deux duels de chaque joueur"""
        acc = self._pending.setdefault(nd.id, {})
        acc.setdefault(o, []).append(d0); acc.setdefault(i, []).append(d1)

    def commit(self, damping):
        for nid, acc in self._pending.items():
            new = {p: np.mean(v, axis=0) for p, v in acc.items()}
            old = self.offsets.get(nid)
            if old is not None and damping > 0:
                new = {p: damping * old[p] + (1 - damping) * new[p] for p in new}
            self.offsets[nid] = new
        self._pending = {}
