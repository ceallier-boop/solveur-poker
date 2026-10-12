"""Solveur postflop heads-up : CFR+ à tirage du board, vectorisé sur les 1 326 combos, abstraction par groupes de force.

Jeu : pot P au flop, tapis effectif S derrière chaque joueur ; OOP parle en premier à chaque rue.
  - sans mise à payer : check, mise (bet_fraction du pot), tapis ;
  - face à une mise : fold, call, tapis (une relance, toujours à tapis) ;
  - une mise de plus de allin_fraction du tapis restant devient un tapis.
À chaque itération, un board complet (5 cartes) est tiré ; les combos qui le touchent sont exclus (tirage exact
de la distribution jointe mains + board). Information d'un joueur : nœud de l'arbre + groupe de force de sa main
sur le board visible (rang relatif moyen à la river, contre toutes les mains), `buckets` groupes par rue.
Gains comptés depuis le flop : G = gain net à partir du flop, avec G_OOP + G_IP = P (le pot initial est réparti).
"""
from dataclasses import dataclass
import numpy as np
from .kernels import CC, CLASS_OF, compatible, showdown, strength, combo_ranks
from . import fast


@dataclass
class PostflopConfig:
    bet_fraction: float = 0.66
    allin_fraction: float = 0.67
    buckets: int = 16
    rollouts: int = 6


class _N:
    __slots__ = ('id', 'kind', 'player', 'street', 'c', 'actions', 'children', 'winner')

    def __init__(self, id, kind, street, c, player=-1, winner=-1):
        self.id = id; self.kind = kind; self.street = street; self.c = c; self.player = player; self.winner = winner
        self.actions = []; self.children = []


class HUPostflop:
    def __init__(self, pot, stack, cfg=None):
        self.P = float(pot); self.S = float(stack); self.cfg = cfg or PostflopConfig(); self.nodes = []
        self.root = self._street(0, (0.0, 0.0))
        self.dec = [n for n in self.nodes if n.kind == 'act']
        B = self.cfg.buckets
        self.R = {n.id: np.zeros((B, len(n.actions))) for n in self.dec}
        self.Sg = {n.id: np.zeros((B, len(n.actions))) for n in self.dec}
        self.t = 0

    # ---------------------------------------------------------------- arbre
    def _new(self, kind, street, c, **kw):
        n = _N(len(self.nodes), kind, street, c, **kw); self.nodes.append(n); return n

    def _street(self, street, c):
        if street == 3 or min(self.S - c[0], self.S - c[1]) <= 1e-9: return self._new('show', street, c)
        return self._act(street, c, 0, facing=0.0, raised=False, checked=False)

    def _act(self, street, c, p, facing, raised, checked):
        n = self._new('act', street, c, player=p); left = self.S - c[p]; pot = self.P + c[0] + c[1]
        if facing <= 1e-9:
            opts = [('X', None)]
            bet = self.cfg.bet_fraction * pot
            if bet < self.cfg.allin_fraction * left: opts.append((f'B{self.cfg.bet_fraction:g}', bet))
            opts.append(('A', left))
        else:
            opts = [('F', None), ('C', None)]
            if not raised and left > facing + 1e-9: opts.append(('A', left))
        for lab, amt in opts:
            if lab == 'X':
                ch = self._street(street + 1, c) if checked else self._act(street, c, 1 - p, 0.0, raised, True)
            elif lab == 'F':
                ch = self._new('fold', street, c, winner=1 - p)
            elif lab == 'C':
                c2 = list(c); c2[p] += min(facing, left); ch = self._street(street + 1, tuple(c2))
            else:                                          # mise ou tapis ; face à une mise, c'est une relance
                c2 = list(c); c2[p] += amt; to_call = c2[p] - c2[1 - p]
                ch = self._act(street, tuple(c2), 1 - p, to_call, raised or facing > 0, False)
            n.actions.append(lab); n.children.append(ch)
        return n

    # ---------------------------------------------------------------- un parcours sur un board
    def _sigma(self, nid, avg):
        R = self.Sg[nid] if avg else self.R[nid]
        pos = np.maximum(R, 0); s = pos.sum(1, keepdims=True)
        return np.where(s > 0, pos / np.where(s > 0, s, 1), 1.0 / R.shape[1])

    def _walk(self, n, r, ctx, avg, update):
        if n.kind == 'fold':
            out = []
            for p in (0, 1):
                net = (self.P + n.c[1 - p]) if n.winner == p else -n.c[p]
                out.append(net * compatible(r[1 - p], ctx['valid'], CC))
            return out
        if n.kind == 'show':
            out = []
            for p in (0, 1):
                w, t, tot = showdown(ctx['ranks'], r[1 - p], CC); c = n.c[p]           # mises égales à l'abattage
                out.append((self.P + c) * w + 0.5 * self.P * t - c * (tot - w - t))
            return out
        a = n.player; b = ctx['bucket'][n.street]; valid = ctx['valid']
        sg = self._sigma(n.id, avg)[np.where(valid, b, 0)]
        vals = []
        for k, ch in enumerate(n.children):
            r2 = [r[0], r[1]]; r2[a] = r[a] * sg[:, k]
            vals.append(self._walk(ch, r2, ctx, avg, update))
        va = np.stack([v[a] for v in vals], axis=1); vo = sum(v[1 - a] for v in vals)
        node_va = (va * sg).sum(1)
        if update:
            inst = (va - node_va[:, None]) * valid[:, None]; bb = np.where(valid, b, 0); B = self.cfg.buckets
            reg = np.stack([np.bincount(bb, weights=inst[:, k], minlength=B) for k in range(len(n.children))], axis=1)
            self.R[n.id] = np.maximum(self.R[n.id] + reg, 0)
            acc = np.stack([np.bincount(bb, weights=r[a] * sg[:, k] * valid, minlength=B) for k in range(len(n.children))], axis=1)
            self.Sg[n.id] += self.t * acc
        out = [None, None]; out[a] = node_va; out[1 - a] = vo
        return out

    def _context(self, rng):
        board = rng.choice(52, 5, replace=False).astype(np.int64)
        ranks = combo_ranks(board, CC); valid = ranks >= 0
        B = self.cfg.buckets; seed = int(rng.integers(1 << 30)); bucket = []
        for k in (3, 4, 5):
            s = strength(board, k, board, self.cfg.rollouts, CC, seed + k)
            bucket.append(np.clip((s * B).astype(np.int64), 0, B - 1))
        return dict(board=board, ranks=ranks, valid=valid, bucket=bucket)

    # ---------------------------------------------------------------- version numba
    def _arrays(self):
        if hasattr(self, '_arr'): return self._arr
        N = len(self.nodes)
        kind = np.array([{'act': 0, 'fold': 1, 'show': 2}[n.kind] for n in self.nodes], np.int64)
        player = np.array([n.player for n in self.nodes], np.int64); street = np.array([min(n.street, 2) for n in self.nodes], np.int64)
        c0 = np.array([n.c[0] for n in self.nodes]); c1 = np.array([n.c[1] for n in self.nodes]); winner = np.array([n.winner for n in self.nodes], np.int64)
        nch = np.array([len(n.children) for n in self.nodes], np.int64); child = np.zeros((N, 3), np.int64)
        for n in self.nodes:
            for k, ch in enumerate(n.children): child[n.id, k] = ch.id
        assert all(n.id == i for i, n in enumerate(self.nodes)) and all(ch.id > n.id for n in self.nodes for ch in n.children)
        B = self.cfg.buckets
        self.Rf = np.zeros((N, B, 3)); self.Sf = np.zeros((N, B, 3))
        self.V = np.zeros((N, 2, 1326)); self.reach = np.zeros((N, 2, 1326))
        self._arr = (kind, player, street, c0, c1, winner, nch, child)
        return self._arr

    def fast_solve(self, w_oop, w_ip, pool, iters=4000, seed=0):
        arr = self._arrays(); ranks, order, valid, bucket = pool
        r0 = np.asarray(w_oop, float)[CLASS_OF]; r1 = np.asarray(w_ip, float)[CLASS_OF]
        rng = np.random.default_rng(seed); idx = rng.integers(len(ranks), size=iters)
        for i in idx:
            self.t += 1
            fast.iterate(*arr, self.P, self.Rf, self.Sf, float(self.t), ranks[i], order[i], valid[i], bucket[i], r0, r1, True, False, self.V, self.reach, CC)
        return self

    def fast_evaluate(self, w_oop, w_ip, pool, boards=None):
        """G par classe (169) des deux joueurs avec la stratégie moyenne, sur les boards du réservoir"""
        arr = self._arrays(); ranks, order, valid, bucket = pool
        r0 = np.asarray(w_oop, float)[CLASS_OF]; r1 = np.asarray(w_ip, float)[CLASS_OF]
        Vs = [np.zeros(1326), np.zeros(1326)]; Ms = [np.zeros(1326), np.zeros(1326)]; m = np.zeros(1326)
        for i in range(len(ranks) if boards is None else boards):
            fast.iterate(*arr, self.P, self.Rf, self.Sf, 1.0, ranks[i], order[i], valid[i], bucket[i], r0, r1, False, True, self.V, self.reach, CC)
            for p, opp in ((0, r1), (1, r0)):
                Vs[p] += self.V[0, p]; fast._compat(opp * valid[i], valid[i], CC, m); Ms[p] += m
        G = []
        for p in (0, 1):
            num = np.bincount(CLASS_OF, weights=Vs[p], minlength=169); den = np.bincount(CLASS_OF, weights=Ms[p], minlength=169)
            G.append(np.where(den > 0, num / np.where(den > 0, den, 1), np.nan))
        return G

    def root_frequencies(self, w_oop, pool, boards=500):
        """fréquences globales des actions d'OOP à la racine (stratégie moyenne)"""
        arr = self._arrays(); ranks, order, valid, bucket = pool; r0 = np.asarray(w_oop, float)[CLASS_OF]
        acc = np.zeros(len(self.root.actions)); tot = 0.0
        for i in range(boards):
            b = bucket[i, 0]; S = np.maximum(self.Sf[0], 0); s = S.sum(1, keepdims=True)
            sg = np.where(s > 0, S / np.where(s > 0, s, 1), 1.0 / len(self.root.actions))[:, :len(self.root.actions)]
            w = r0 * valid[i]; acc += (w[:, None] * sg[b]).sum(0); tot += w.sum()
        return dict(zip(self.root.actions, acc / tot))

    # ---------------------------------------------------------------- interface (version Python, référence des tests)
    def solve(self, w_oop, w_ip, iters=4000, seed=0):
        """w_oop, w_ip : poids par classe (169) des ranges qui atteignent le flop"""
        rng = np.random.default_rng(seed)
        r0 = np.asarray(w_oop, float)[CLASS_OF]; r1 = np.asarray(w_ip, float)[CLASS_OF]
        for _ in range(iters):
            self.t += 1; ctx = self._context(rng)
            self._walk(self.root, [r0 * ctx['valid'], r1 * ctx['valid']], ctx, avg=False, update=True)
        return self

    def evaluate(self, w_oop, w_ip, boards=2000, seed=99):
        """G par classe (169) pour chaque joueur, avec la stratégie moyenne ; et les fréquences globales à la racine"""
        rng = np.random.default_rng(seed)
        r0 = np.asarray(w_oop, float)[CLASS_OF]; r1 = np.asarray(w_ip, float)[CLASS_OF]
        V = [np.zeros(1326), np.zeros(1326)]; M = [np.zeros(1326), np.zeros(1326)]
        for _ in range(boards):
            ctx = self._context(rng); v = ctx['valid']
            out = self._walk(self.root, [r0 * v, r1 * v], ctx, avg=True, update=False)
            for p, opp in ((0, r1 * v), (1, r0 * v)):
                V[p] += out[p]; M[p] += compatible(opp, v, CC)
        G = []
        for p in (0, 1):
            num = np.bincount(CLASS_OF, weights=V[p], minlength=169); den = np.bincount(CLASS_OF, weights=M[p], minlength=169)
            G.append(np.where(den > 0, num / np.where(den > 0, den, 1), np.nan))
        return G
