"""Sous-jeux postflop heads-up résolus exactement sur un board fixé : contrôle de l'abstraction du solveur.

Le solveur de production (hu_solver) partage une même stratégie entre tous les boards, par groupe de force de la main.
Ici, sur un board donné (turn : 4 cartes, river : 5 cartes), chaque combo a sa propre stratégie à chaque nœud et la
carte de river est un nœud de hasard énuméré (48 cartes, chaque couple de mains en voit 44). CFR+ complet, sans
échantillonnage ni groupes : c'est la valeur exacte du sous-jeu, avec le même arbre de mises que la production.
On compare ensuite, board par board :
  - la valeur exacte de chaque combo à l'équilibre ;
  - la valeur obtenue quand les deux joueurs appliquent la stratégie abstraite (groupes de force) ;
  - l'exploitabilité de la stratégie abstraite sur ce board (meilleure réponse combo par combo).
Valeurs comptées comme dans hu_solver : gain net à partir du début du sous-jeu, G_OOP + G_IP = pot.
"""
import numpy as np
from numba import njit
from .kernels import CC, CLASS_OF, combo_ranks, strength, _percentile
from .fast import _showdown2, _compat
from .hu_solver import HUPostflop

ACT, FOLD, SHOW, CHANCE = 0, 1, 2, 3


@njit(cache=True)
def _sigma(src, kind, nch, out):
    """normalisation par nœud et combo (appariement des regrets ou stratégie moyenne)"""
    for n in range(kind.shape[0]):
        if kind[n] != ACT: continue
        k = nch[n]
        for c in range(1326):
            s = 0.0
            for a in range(k):
                if src[n, c, a] > 0: s += src[n, c, a]
            for a in range(k):
                out[n, c, a] = (src[n, c, a] if src[n, c, a] > 0 else 0.0) / s if s > 0 else 1.0 / k


@njit(cache=True)
def _pass(kind, player, c0, c1, winner, nch, child, ctx, P, ranks, order, valid, sig, r0, r1, br, update, R, Sg, t, V, reach, CC):
    """un parcours complet. br = -1 : les deux joueurs suivent sig ; br = p : p joue sa meilleure réponse.
    update : regrets et stratégie moyenne CFR+ (mises à jour simultanées)."""
    N = kind.shape[0]
    for c in range(1326):
        reach[0, 0, c] = r0[c] * valid[ctx[0], c]; reach[0, 1, c] = r1[c] * valid[ctx[0], c]
    for n in range(N):
        if kind[n] == ACT:
            a = player[n]
            for j in range(nch[n]):
                ch = child[n, j]
                for c in range(1326):
                    reach[ch, 1 - a, c] = reach[n, 1 - a, c]; reach[ch, a, c] = reach[n, a, c] * sig[n, c, j]
        elif kind[n] == CHANCE:
            for j in range(nch[n]):
                ch = child[n, j]; v = ctx[ch]
                for c in range(1326):
                    reach[ch, 0, c] = reach[n, 0, c] * valid[v, c]; reach[ch, 1, c] = reach[n, 1, c] * valid[v, c]
    win = np.zeros(1326); tie = np.zeros(1326); tot = np.zeros(1326)
    for n in range(N - 1, -1, -1):
        v = ctx[n]
        if kind[n] == FOLD:
            for p in range(2):
                _compat(reach[n, 1 - p], valid[v], CC, tot)
                net = (P + (c1[n] if p == 0 else c0[n])) if winner[n] == p else -(c0[n] if p == 0 else c1[n])
                for c in range(1326): V[n, p, c] = net * tot[c]
        elif kind[n] == SHOW:
            cc = c0[n]
            for p in range(2):
                _showdown2(ranks[v], order[v], reach[n, 1 - p], CC, win, tie, tot)
                for c in range(1326): V[n, p, c] = (P + cc) * win[c] + 0.5 * P * tie[c] - cc * (tot[c] - win[c] - tie[c])
        elif kind[n] == CHANCE:
            w = 1.0 / (nch[n] - 4)                         # 48 rivers énumérées, 44 compatibles avec deux mains données
            for p in range(2):
                for c in range(1326):
                    s = 0.0
                    for j in range(nch[n]): s += V[child[n, j], p, c]
                    V[n, p, c] = s * w
        else:
            a = player[n]; k = nch[n]
            for c in range(1326):
                vo = 0.0
                for j in range(k): vo += V[child[n, j], 1 - a, c]
                V[n, 1 - a, c] = vo
                if a == br:
                    m = V[child[n, 0], a, c]
                    for j in range(1, k):
                        if V[child[n, j], a, c] > m: m = V[child[n, j], a, c]
                    V[n, a, c] = m
                else:
                    va = 0.0
                    for j in range(k): va += sig[n, c, j] * V[child[n, j], a, c]
                    V[n, a, c] = va
            if update:
                for c in range(1326):
                    if not valid[v, c]: continue
                    for j in range(k):
                        x = R[n, c, j] + V[child[n, j], a, c] - V[n, a, c]
                        R[n, c, j] = x if x > 0 else 0.0
                        Sg[n, c, j] += t * reach[n, a, c] * sig[n, c, j]


class ExactHU:
    """sous-jeu heads-up sur un board fixé (4 ou 5 cartes), même arbre de mises que HUPostflop"""

    def __init__(self, pot, stack, board, cfg=None, tree=None):
        board = [int(x) for x in board]; assert len(board) in (4, 5)
        self.board = board; self.street = len(board) - 3
        self.tree = tree or HUPostflop(pot, stack, cfg, start_street=self.street)
        self.P = self.tree.P
        # contextes : 0 = board de départ ; pour une turn, 1..48 = board complété par chaque river
        rivers = [] if len(board) == 5 else [x for x in range(52) if x not in board]
        boards = [board] + [board + [r] for r in rivers]
        self.boards = boards; nctx = len(boards)
        self.ranks = np.full((nctx, 1326), -1, np.int64); self.order = np.zeros((nctx, 1326), np.int64)
        self.valid = np.zeros((nctx, 1326))
        for i, b in enumerate(boards):
            if len(b) == 5:
                self.ranks[i] = combo_ranks(np.array(b, np.int64), CC); self.order[i] = np.argsort(self.ranks[i])
            used = np.zeros(52, bool); used[b] = True
            self.valid[i] = ~(used[CC[:, 0]] | used[CC[:, 1]])
        self._expand(rivers)
        N = len(self.kind); Wd = int(self.nch[self.kind == ACT].max()) if (self.kind == ACT).any() else 1
        self.R = np.zeros((N, 1326, Wd)); self.Sg = np.zeros((N, 1326, Wd)); self.sig = np.zeros((N, 1326, Wd))
        self.V = np.zeros((N, 2, 1326)); self.reach = np.zeros((N, 2, 1326)); self.t = 0

    def _expand(self, rivers):
        """arbre déplié en ordre préfixe : un nœud de hasard avant chaque passage à la river"""
        kind, player, c0, c1, winner, children, ctx, orig = [], [], [], [], [], [], [], []

        def add(k, n, cx):
            i = len(kind); kind.append(k); ctx.append(cx); children.append([]); orig.append(n.id if n is not None else -1)
            player.append(n.player if n is not None else -1); winner.append(n.winner if n is not None else -1)
            c0.append(n.c[0] if n is not None else 0.0); c1.append(n.c[1] if n is not None else 0.0)
            return i

        def walk(n, cx):
            if cx == 0 and rivers and (n.street >= 2):          # première rencontre de la river : hasard
                i = add(CHANCE, None, 0)
                for r in range(len(rivers)): children[i].append(walk(n, r + 1))
                return i
            i = add({'act': ACT, 'fold': FOLD, 'show': SHOW}[n.kind], n, cx)
            for ch in n.children: children[i].append(walk(ch, cx))
            return i

        walk(self.tree.root, 0)
        N = len(kind); Wd = max(len(c) for c in children)
        self.kind = np.array(kind, np.int64); self.player = np.array(player, np.int64); self.winner = np.array(winner, np.int64)
        self.c0 = np.array(c0); self.c1 = np.array(c1); self.ctx = np.array(ctx, np.int64); self.orig = np.array(orig, np.int64)
        self.nch = np.array([len(c) for c in children], np.int64); self.child = np.zeros((N, Wd), np.int64)
        for i, cs in enumerate(children): self.child[i, :len(cs)] = cs
        assert all(ch > i for i, cs in enumerate(children) for ch in cs)

    def _run(self, r0, r1, br=-1, update=False):
        _pass(self.kind, self.player, self.c0, self.c1, self.winner, self.nch, self.child, self.ctx, self.P, self.ranks, self.order,
              self.valid, self.sig, r0, r1, br, update, self.R, self.Sg, float(self.t), self.V, self.reach, CC)

    def solve(self, r0, r1, iters=1000):
        """r0, r1 : poids par combo (1 326) d'OOP et d'IP"""
        for _ in range(iters):
            self.t += 1; _sigma(self.R, self.kind, self.nch, self.sig); self._run(r0, r1, update=True)
        _sigma(self.Sg, self.kind, self.nch, self.sig)
        return self

    def set_abstract(self, sigma_buckets, buckets):
        """stratégie abstraite : sigma_buckets (nœud original, groupe, action) ; buckets[(contexte, rue)] -> groupe de chaque combo"""
        for n in np.where(self.kind == ACT)[0]:
            o = self.orig[n]; st = self.tree.nodes[o].street
            k = self.nch[n]; self.sig[n, :, :k] = sigma_buckets[o][buckets[(self.ctx[n], st)]][:, :k]

    def values(self, r0, r1, br=-1):
        """valeur de chaque combo à la racine pour les deux joueurs (avec self.sig), et masses compatibles"""
        self._run(r0, r1, br=br)
        return self.V[0, 0].copy(), self.V[0, 1].copy()

    def compat(self, r0, r1):
        m0 = np.zeros(1326); m1 = np.zeros(1326); v = self.valid[0]
        _compat(r1 * v, v.astype(np.bool_), CC, m0); _compat(r0 * v, v.astype(np.bool_), CC, m1)
        return m0, m1

    def exploitability(self, r0, r1):
        """(gain moyen des deux meilleures réponses - pot) / 2, par couple de mains, en fraction du pot"""
        v0, _ = self.values(r0, r1, br=0); _, v1 = self.values(r0, r1, br=1)
        m0, _ = self.compat(r0, r1); M = float((r0 * self.valid[0] * m0).sum())
        u = float((r0 * v0).sum() + (r1 * v1).sum())
        return (u / M - self.P) / 2 / self.P


def abstract_buckets(ex, B, rollouts, seed, metric='ehs'):
    """groupes de force de chaque combo sur chaque contexte du sous-jeu, calculés comme dans fast.board_pool"""
    out = {}
    for i, b in enumerate(ex.boards):
        b5 = np.array(b + [0] * (5 - len(b)), np.int64); k = len(b)
        if k == 5: s = _percentile(combo_ranks(b5, CC))
        else: s = strength(b5, k, b5, rollouts, CC, seed + k, metric == 'ehs2')
        if metric == 'ehs2' and k < 5:
            v = s >= 0; q = np.quantile(s[v], np.linspace(0, 1, B + 1)[1:-1]); g = np.where(v, np.searchsorted(q, s), 0)
        else:
            g = np.clip((s * B).astype(np.int64), 0, B - 1)
        g = np.where(s >= 0, g, 0)
        out[(i, k - 3)] = g
    return out


def average_sigma(hp):
    """stratégie moyenne du solveur abstrait (version numba) : (nœud, groupe, action)"""
    S = np.maximum(hp.Sf, 0); s = S.sum(2, keepdims=True)
    nch = np.array([max(len(n.children), 1) for n in hp.nodes])
    uni = np.zeros_like(S)
    for i, k in enumerate(nch): uni[i, :, :k] = 1.0 / k
    return np.where(s > 0, S / np.where(s > 0, s, 1), uni)
