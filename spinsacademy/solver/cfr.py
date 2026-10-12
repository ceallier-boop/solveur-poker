"""Solveur préflop par CFR+ vectorisé sur les 169 classes de mains, chip EV, 2 ou 3 joueurs.

Pondération des mains adverses, du point de vue du joueur p qui tient la classe i :
  - heads-up : D[i, j] (couples de combos disjoints : effet de bloqueurs exact au niveau des classes) ;
  - 3 joueurs : D[i, j] * D[i, k] / n_i (bloqueurs entre p et chaque adversaire ; les deux adversaires sont
    supposés indépendants entre eux, approximation du second ordre).
Valeurs terminales : répartition du pot par couches (pots annexes), équité à 2 mains E ou à 3 mains T ;
les fins de tour « flop » sont évaluées par un modèle postflop (voir postflop.py).
EV publiées : relatives au fold du joueur au nœud (convention HRC), en BB.
"""
import os
import numpy as np
from ..cards import DISJOINT as D, W as NCOMB
from ..allin import E
from .tree import Tree, TreeConfig

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
_T = None


def equity3():
    """T[i, j, k] : part du pot de la classe i contre j et k (all-in à 3), et TD = T * D_ij * D_ik / n_i"""
    global _T
    if _T is None:
        T = np.load(os.path.join(DATA, 'equity3_169.npy')).astype(np.float32)
        TD = T * (D[:, :, None] * D[:, None, :] / NCOMB[:, None, None]).astype(np.float32)
        _T = (T, TD.reshape(169 * 169, 169))
    return _T


def layers(contrib, active):
    """[(montant, joueurs éligibles)] : pot principal puis pots annexes ; les jetons des joueurs couchés sont de l'argent mort"""
    out = []; prev = 0.0
    for lvl in sorted(set(contrib)):
        amt = (lvl - prev) * sum(1 for c in contrib if c >= lvl - 1e-12)
        elig = tuple(p for p in active if contrib[p] >= lvl - 1e-12)
        if amt > 0:
            if not elig:            # couche payée seulement par des joueurs couchés : revient au plus gros joueur actif
                elig = (max(active, key=lambda p: contrib[p]),)
            out.append((amt, elig))
        prev = lvl
    return out


class Solver:
    def __init__(self, stacks, cfg=None, postflop=None):
        self.tree = Tree(stacks, cfg or TreeConfig()); self.n = self.tree.n
        from .postflop import Showdown
        self.postflop = postflop or Showdown()
        self.DE = D * E
        self.nodes = self.tree.nodes
        self.dec = self.tree.decisions()
        self.R = {nd.id: np.zeros((169, len(nd.actions))) for nd in self.dec}
        self.S = {nd.id: np.zeros((169, len(nd.actions))) for nd in self.dec}
        self.t = 0
        if self.n == 3: equity3()

    # ------------------------------------------------------------------ pondérations
    def _opp(self, p):
        return [q for q in range(self.n) if q != p]

    def mass(self, p, reach):
        """poids des mains adverses compatibles avec chaque classe de p (non normalisé)"""
        if self.n == 2:
            return D @ reach[self._opp(p)[0]]
        q, s = self._opp(p)
        return (D @ reach[q]) * (D @ reach[s]) / NCOMB

    def showdown_value(self, nd, p, reach, contrib=None, active=None):
        """somme sur les mains adverses (pondérées par leur atteinte) du gain net de p ; contrib/active modifiables par le modèle postflop"""
        contrib = nd.contrib if contrib is None else contrib
        active = [q for q in range(self.n) if not nd.folded[q]] if active is None else active
        const = -contrib[p]; terms_e = {}; t3 = 0.0
        for amt, elig in layers(contrib, active):
            if p not in elig: continue
            if len(elig) == 1: const += amt
            elif len(elig) == 2:
                q = elig[0] if elig[1] == p else elig[1]; terms_e[q] = terms_e.get(q, 0.0) + amt
            else: t3 += amt
        if self.n == 2:
            q = self._opp(p)[0]; rq = reach[q]
            v = const * (D @ rq)
            if q in terms_e: v = v + terms_e[q] * (self.DE @ rq)
            return v
        q, s = self._opp(p); rq, rs = reach[q], reach[s]
        Dq, Ds = D @ rq, D @ rs
        v = const * Dq * Ds / NCOMB
        if q in terms_e: v = v + terms_e[q] * (self.DE @ rq) * Ds / NCOMB
        if s in terms_e: v = v + terms_e[s] * (self.DE @ rs) * Dq / NCOMB
        if t3:
            Y = (equity3()[1] @ rs.astype(np.float32)).reshape(169, 169).astype(np.float64)
            v = v + t3 * (Y @ rq)
        return v

    def terminal_value(self, nd, p, reach):
        if nd.terminal == 'flop': return self.postflop.value(self, nd, p, reach)
        return self.showdown_value(nd, p, reach)

    # ------------------------------------------------------------------ CFR+
    def _sigma(self, nid, avg=False):
        R = self.S[nid] if avg else self.R[nid]
        pos = np.maximum(R, 0); s = pos.sum(1, keepdims=True)
        return np.where(s > 0, pos / np.where(s > 0, s, 1), 1.0 / R.shape[1])

    def _pass(self, avg=False, br=None):
        """parcours complet : renvoie V[nid] (n, 169) ; br = joueur en meilleure réponse (max sur ses actions)"""
        V = {}; reach = {self.tree.root.id: np.ones((self.n, 169))}; sig = {}
        order = self.nodes                       # créés en préordre : un parent précède ses enfants
        for nd in order:
            if nd.kind != 'decision': continue
            sg = self._sigma(nd.id, avg); sig[nd.id] = sg; r = reach[nd.id]
            for k, ch in enumerate(nd.children):
                r2 = r.copy(); r2[nd.player] = r[nd.player] * sg[:, k]; reach[ch.id] = r2
        for nd in reversed(order):
            r = reach[nd.id]
            if nd.kind == 'terminal':
                V[nd.id] = np.stack([self.terminal_value(nd, p, r) for p in range(self.n)]); continue
            a = nd.player; sg = sig[nd.id]; ch = np.stack([V[c.id] for c in nd.children], axis=2)   # (n, 169, A)
            v = ch.sum(axis=2)
            v[a] = ch[a].max(axis=1) if br == a else (ch[a] * sg).sum(axis=1)
            V[nd.id] = v
            if not avg and br is None:
                self.R[nd.id] = np.maximum(self.R[nd.id] + ch[a] - v[a][:, None], 0)
                self.S[nd.id] += self.t * r[a][:, None] * sg
        return V, reach

    def solve(self, iters=1000, log_every=0):
        for _ in range(iters):
            self.t += 1; self._pass()
            if log_every and self.t % log_every == 0: print(self.t, self.exploitability(), flush=True)
        return self

    # ------------------------------------------------------------------ résultats
    def exploitability(self):
        """gain moyen (BB par main) de chaque joueur en meilleure réponse contre la stratégie moyenne des autres"""
        V, reach = self._pass(avg=True); root = self.tree.root.id; out = []
        for p in range(self.n):
            Vb, _ = self._pass(avg=True, br=p)
            m = self.mass(p, reach[root])
            gain = (Vb[root][p] - V[root][p]) / m
            out.append(float((NCOMB * gain).sum() / NCOMB.sum()))
        return out

    def strategy(self):
        """{clé de nœud : dict(player, actions, freq (169, A), ev (169, A) relatives au fold, reach (169))}"""
        V, reach = self._pass(avg=True); out = {}
        for nd in self.dec:
            a = nd.player; m = self.mass(a, reach[nd.id])
            with np.errstate(invalid='ignore', divide='ignore'):
                ev = np.stack([V[c.id][a] / m for c in nd.children], axis=1) + nd.contrib[a]
            out[nd.key] = dict(player=self.tree.names[a], actions=list(nd.actions), freq=self._sigma(nd.id, avg=True), ev=ev, reach=reach[nd.id][a])
        return out
