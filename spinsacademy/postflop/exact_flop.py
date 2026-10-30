"""Sous-jeu postflop heads-up résolu exactement à partir du flop, sur un flop fixé (action G9 du 30/10/2026).

Même arbre de mises que le solveur de production (HUPostflop) ; chaque combo a sa propre stratégie à chaque nœud, la turn
(49 cartes) et la river (48) sont des nœuds de hasard énumérés. CFR+ complet (alterné), sans groupes ni tirage : c'est la valeur
exacte du sous-jeu, qui sert d'arbitre entre le solveur de production (groupes de force partagés entre tous les flops)
et la référence.

Découpage en tranches : le jeu déplié ne tient pas en mémoire (13 à 100 Go selon le pot). On le découpe par carte de
turn : la tranche t est l'arbre complet vu avec la turn t déjà connue (rivers énumérées), et toutes les tranches ont la
même forme. Les nœuds du flop sont présents dans chaque tranche mais leur stratégie est commune : leurs valeurs sont la
moyenne des tranches (un couple de mains donné est compatible avec 45 turns), et leurs regrets sont mis à jour après le
passage de toutes les tranches. Les regrets et stratégies cumulées des nœuds de turn et de river sont en float32, la
stratégie courante est recalculée à la volée ; les tranches sont parcourues en parallèle.

Valeurs comptées comme dans hu_solver : gain net à partir du flop, G_OOP + G_IP = pot.
"""
import numba
import numpy as np
from numba import njit, prange
from .kernels import CC, CLASS_OF, combo_ranks, strength, _percentile
from .fast import _showdown2, _compat
from .hu_solver import HUPostflop

ACT, FOLD, SHOW, CHANCE = 0, 1, 2, 3


@njit(cache=True)
def _sig_node(n, c, k, street, slot, aidx, mode, R0, S0, R1, S1, Tab, orig, bk0, bk1, bk2, ctx, out):
    """stratégie d'un combo à un nœud : 0 regrets courants, 1 stratégie moyenne, 2 stratégie abstraite (groupes)"""
    if mode == 2:
        v = ctx[n]
        b = bk0[c] if street[n] == 0 else (bk1[c] if street[n] == 1 else bk2[v, c])
        for a in range(k): out[a] = Tab[orig[n], b, a]
        return
    s = 0.0
    for a in range(k):
        if street[n] == 0: x = R0[aidx[n], c, a] if mode == 0 else S0[aidx[n], c, a]
        else: x = R1[aidx[n], c, a] if mode == 0 else S1[aidx[n], c, a]
        out[a] = x if x > 0 else 0.0; s += out[a]
    for a in range(k): out[a] = out[a] / s if s > 0 else 1.0 / k


@njit(cache=True)
def _slice(kind, player, street, c0, c1, winner, nch, child, ctx, aidx, slot, P, ranks, order, valid, mode, br, upd, tw,
           R0, S0, R1, S1, Tab, orig, bk0, bk1, bk2, r0, r1, actl, nact, sig, V, reach, buf, win, tie, tot, CC):
    """une tranche (turn fixée) : passe avant (atteintes), passe arrière (valeurs) ; mises à jour CFR+ des nœuds de turn et de river.
    Indexage compact : V, reach et sig ne portent que les combos de la range de chaque joueur (combo actl[p, ii]) ; les
    abattages et les folds passent par un tableau des 1 326 combos (buf)."""
    N = kind.shape[0]; tmp = np.zeros(8)
    for p in range(2):
        for ii in range(nact[p]):
            c = actl[p, ii]; reach[0, p, ii] = (r0[c] if p == 0 else r1[c]) * valid[0, c]
    for n in range(N):
        if kind[n] == ACT:
            a = player[n]; o = 1 - a; k = nch[n]; sl = slot[n]
            for ii in range(nact[a]):
                _sig_node(n, actl[a, ii], k, street, sl, aidx, mode, R0, S0, R1, S1, Tab, orig, bk0, bk1, bk2, ctx, tmp)
                for j in range(k): sig[sl, ii, j] = tmp[j]
            for j in range(k):
                ch = child[n, j]
                for ii in range(nact[o]): reach[ch, o, ii] = reach[n, o, ii]
                for ii in range(nact[a]): reach[ch, a, ii] = reach[n, a, ii] * sig[sl, ii, j]
        elif kind[n] == CHANCE:
            for j in range(nch[n]):
                ch = child[n, j]; v = ctx[ch]
                for p in range(2):
                    for ii in range(nact[p]): reach[ch, p, ii] = reach[n, p, ii] * valid[v, actl[p, ii]]
    for n in range(N - 1, -1, -1):
        v = ctx[n]
        if kind[n] == FOLD or kind[n] == SHOW:
            for p in range(2):
                o = 1 - p
                for c in range(1326): buf[c] = 0.0
                for ii in range(nact[o]): buf[actl[o, ii]] = reach[n, o, ii]
                if kind[n] == FOLD:
                    _compat(buf, valid[v], CC, tot)
                    net = (P + (c1[n] if p == 0 else c0[n])) if winner[n] == p else -(c0[n] if p == 0 else c1[n])
                    for ii in range(nact[p]): V[n, p, ii] = net * tot[actl[p, ii]]
                else:
                    cc = c0[n]
                    _showdown2(ranks[v], order[v], buf, CC, win, tie, tot)
                    for ii in range(nact[p]):
                        c = actl[p, ii]; V[n, p, ii] = (P + cc) * win[c] + 0.5 * P * tie[c] - cc * (tot[c] - win[c] - tie[c])
        elif kind[n] == CHANCE:
            w = 1.0 / (nch[n] - 4)                         # 48 rivers, 44 compatibles avec deux mains données
            for p in range(2):
                for ii in range(nact[p]):
                    s = 0.0
                    for j in range(nch[n]): s += V[child[n, j], p, ii]
                    V[n, p, ii] = s * w
        else:
            a = player[n]; o = 1 - a; k = nch[n]; sl = slot[n]
            for ii in range(nact[o]):
                vo = 0.0
                for j in range(k): vo += V[child[n, j], o, ii]
                V[n, o, ii] = vo
            for ii in range(nact[a]):
                if a == br:
                    m = V[child[n, 0], a, ii]
                    for j in range(1, k):
                        if V[child[n, j], a, ii] > m: m = V[child[n, j], a, ii]
                    V[n, a, ii] = m
                else:
                    va = 0.0
                    for j in range(k): va += sig[sl, ii, j] * V[child[n, j], a, ii]
                    V[n, a, ii] = va
            if upd == a and street[n] >= 1:
                i = aidx[n]
                for ii in range(nact[a]):
                    c = actl[a, ii]
                    if valid[v, c] == 0: continue
                    for j in range(k):
                        x = R1[i, c, j] + V[child[n, j], a, ii] - V[n, a, ii]
                        R1[i, c, j] = x if x > 0 else 0.0
                        S1[i, c, j] += tw * reach[n, a, ii] * sig[sl, ii, j]


@njit(parallel=True, cache=True)
def _all_slices(kind, player, street, c0, c1, winner, nch, child, ctx, aidx, slot, P, ranks, order, valid, mode, br, upd, tw,
                R0, S0, R1, S1, Tab, orig, bk0, bk1, bk2, r0, r1, actl, nact, flop_nodes, acc, nslot, W, G, CC):
    """toutes les tranches, réparties en G groupes parallèles ; acc[t] reçoit les valeurs des nœuds du flop de la tranche t
    (dans les 1 326 combos). Les tampons d'un groupe servent à toutes ses tranches."""
    T = ranks.shape[0]; N = kind.shape[0]; M = actl.shape[1]
    for g in prange(G):
        sig = np.zeros((nslot, M, W)); V = np.zeros((N, 2, M)); reach = np.zeros((N, 2, M))
        buf = np.zeros(1326); win = np.zeros(1326); tie = np.zeros(1326); tot = np.zeros(1326)
        for t in range(g, T, G):
            _slice(kind, player, street, c0, c1, winner, nch, child, ctx, aidx, slot, P, ranks[t], order[t], valid[t], mode, br, upd, tw,
                   R0, S0, R1[t], S1[t], Tab, orig, bk0, bk1[t], bk2[t], r0, r1, actl, nact, sig, V, reach, buf, win, tie, tot, CC)
            for i in range(flop_nodes.shape[0]):
                for p in range(2):
                    for c in range(1326): acc[t, i, p, c] = 0.0
                    for ii in range(nact[p]): acc[t, i, p, actl[p, ii]] = V[flop_nodes[i], p, ii]


class ExactFlopHU:
    """sous-jeu heads-up à partir d'un flop fixé, même arbre de mises que HUPostflop (pot, tapis, réglages, agresseur)"""

    def __init__(self, pot, stack, flop, cfg=None, aggressor=-1):
        self.flop = [int(x) for x in flop]; assert len(self.flop) == 3
        self.tree = HUPostflop(pot, stack, cfg, aggressor=aggressor); self.P = self.tree.P
        self.turns = [x for x in range(52) if x not in self.flop]
        self._expand()
        T = len(self.turns); nctx = 49                                     # contexte 0 : flop + turn ; 1..48 : + river
        self.ranks = np.full((T, nctx, 1326), -1, np.int64); self.order = np.zeros((T, nctx, 1326), np.int64)
        self.valid = np.zeros((T, nctx, 1326)); self.rivers = []
        for ti, t in enumerate(self.turns):
            riv = [x for x in self.turns if x != t]; self.rivers.append(riv)
            for i, b in enumerate([self.flop + [t]] + [self.flop + [t, r] for r in riv]):
                used = np.zeros(52, bool); used[b] = True; self.valid[ti, i] = ~(used[CC[:, 0]] | used[CC[:, 1]])
                if len(b) == 5: self.ranks[ti, i] = combo_ranks(np.array(b, np.int64), CC); self.order[ti, i] = np.argsort(self.ranks[ti, i])
        used = np.zeros(52, bool); used[self.flop] = True; self.valid_flop = ~(used[CC[:, 0]] | used[CC[:, 1]])
        W = self.W
        self.R0 = np.zeros((self.na0, 1326, W)); self.S0 = np.zeros((self.na0, 1326, W))
        self.R1 = np.zeros((T, max(self.na1, 1), 1326, W), np.float32); self.S1 = np.zeros((T, max(self.na1, 1), 1326, W), np.float32)
        self._acc = np.zeros((T, len(self.flop_nodes), 2, 1326)); self.t = 0
        self.Tab = np.zeros((1, 1, W)); self.bk = (np.zeros(1326, np.int64), np.zeros((T, 1326), np.int64), np.zeros((T, nctx, 1326), np.int64))

    def _expand(self):
        """tranche dépliée en ordre préfixe : un nœud de hasard (48 rivers) avant la river, ou avant un abattage anticipé"""
        kind, player, street, c0, c1, winner, children, ctx, orig = [], [], [], [], [], [], [], [], []

        def add(k, n, cx, st):
            i = len(kind); kind.append(k); ctx.append(cx); children.append([]); orig.append(n.id if n is not None else -1)
            player.append(n.player if n is not None else -1); winner.append(n.winner if n is not None else -1)
            c0.append(n.c[0] if n is not None else 0.0); c1.append(n.c[1] if n is not None else 0.0); street.append(st)
            return i

        def walk(n, cx):
            if cx == 0 and (n.street >= 2 or n.kind == 'show'):          # river inconnue : hasard
                i = add(CHANCE, None, 0, 2)
                for r in range(48): children[i].append(walk(n, r + 1))
                return i
            i = add({'act': ACT, 'fold': FOLD, 'show': SHOW}[n.kind], n, cx, n.street)
            for ch in n.children: children[i].append(walk(ch, cx))
            return i

        walk(self.tree.root, 0)
        N = len(kind); Wc = max(len(c) for c in children)
        self.W = max([len(c) for i, c in enumerate(children) if kind[i] == ACT] + [1])         # largeur des stratégies (le hasard en a 48)
        self.kind = np.array(kind, np.int64); self.player = np.array(player, np.int64); self.winner = np.array(winner, np.int64)
        self.street = np.array(street, np.int64); self.c0 = np.array(c0); self.c1 = np.array(c1); self.ctx = np.array(ctx, np.int64)
        self.orig = np.array(orig, np.int64)
        self.nch = np.array([len(c) for c in children], np.int64); self.child = np.zeros((N, Wc), np.int64)
        for i, cs in enumerate(children): self.child[i, :len(cs)] = cs
        assert all(ch > i for i, cs in enumerate(children) for ch in cs)
        act = self.kind == ACT
        self.aidx = np.full(N, -1, np.int64); self.slot = np.full(N, -1, np.int64)
        f = np.where(act & (self.street == 0))[0]; o = np.where(act & (self.street >= 1))[0]
        self.aidx[f] = np.arange(len(f)); self.aidx[o] = np.arange(len(o)); self.slot[act] = np.arange(int(act.sum()))
        self.na0, self.na1, self.nslot = len(f), len(o), int(act.sum())
        # nœuds du flop (rue 0, hors hasard) et premiers nœuds hors du flop : leurs valeurs moyennées sur les turns
        flop_set = {i for i in range(N) if self.street[i] == 0 and kind[i] != CHANCE}; border = set()
        for i in flop_set:
            for ch in children[i]:
                if ch not in flop_set: border.add(ch)
        self.flop_nodes = np.array(sorted(flop_set | border | {0}), np.int64)   # racine toujours présente (abattage immédiat : hasard)
        self._pos = {int(n): i for i, n in enumerate(self.flop_nodes)}
        self._children = children

    # ---------------------------------------------------------------- parcours
    def _run(self, r0, r1, mode, br=-1, upd=-1):
        """upd : joueur dont les regrets sont mis à jour (CFR+ alterné), -1 aucun"""
        bk0, bk1, bk2 = self.bk
        _all_slices(self.kind, self.player, self.street, self.c0, self.c1, self.winner, self.nch, self.child, self.ctx, self.aidx, self.slot,
                    self.P, self.ranks, self.order, self.valid, mode, br, upd, float(self.t), self.R0, self.S0, self.R1, self.S1,
                    self.Tab, self.orig, bk0, bk1, bk2, r0, r1, *self._active(r0, r1), self.flop_nodes, self._acc, self.nslot, self.W, min(numba.get_num_threads(), len(self.turns)), CC)
        A = self._acc.sum(0) / 45.0                                # un couple de mains donné est compatible avec 45 turns
        Vf = {}                                                    # valeurs des nœuds du flop, recalculées avec la stratégie commune
        for i in range(len(self.flop_nodes) - 1, -1, -1):
            n = int(self.flop_nodes[i])
            if not (self.kind[n] == ACT and self.street[n] == 0): Vf[n] = A[i]; continue
            a = self.player[n]; k = self.nch[n]; chs = [int(x) for x in self.child[n, :k]]
            CV = np.stack([Vf[c] for c in chs], axis=2)            # (2, 1326, k)
            sg = self._sigma0(n, mode)
            v = CV.sum(axis=2); v[a] = CV[a].max(axis=1) if br == a else (CV[a] * sg).sum(axis=1)
            Vf[n] = v
            if upd == a:
                j = self.aidx[n]; ok = self.valid_flop[:, None]
                self.R0[j, :, :k] = np.where(ok, np.maximum(self.R0[j, :, :k] + CV[a] - v[a][:, None], 0), 0)
                self.S0[j, :, :k] += self.t * self._reach0[n][a][:, None] * sg
        return Vf[0]

    def _active(self, r0, r1):
        """combos de la range de chaque joueur sur ce flop : (2, n) et nombres"""
        lists = [np.where((r > 0) & self.valid_flop)[0] for r in (r0, r1)]
        actl = np.zeros((2, max(len(x) for x in lists)), np.int64); nact = np.array([len(x) for x in lists], np.int64)
        for p in range(2): actl[p, :nact[p]] = lists[p]
        return actl, nact

    def _sigma0(self, n, mode):
        k = self.nch[n]; j = self.aidx[n]
        if mode == 2:
            return self.Tab[self.orig[n]][self.bk[0]][:, :k]
        X = np.maximum(self.R0[j, :, :k] if mode == 0 else self.S0[j, :, :k], 0); s = X.sum(1, keepdims=True)
        return np.where(s > 0, X / np.where(s > 0, s, 1), 1.0 / k)

    def _flop_reach(self, r0, r1, mode):
        """atteintes des nœuds du flop (pour la stratégie moyenne des nœuds du flop)"""
        out = {0: np.stack([r0 * self.valid_flop, r1 * self.valid_flop])}
        for n in self.flop_nodes:
            n = int(n)
            if not (self.kind[n] == ACT and self.street[n] == 0): continue
            a = self.player[n]; sg = self._sigma0(n, mode)
            for j, ch in enumerate(self.child[n, :self.nch[n]]):
                r = out[n].copy(); r[a] = r[a] * sg[:, j]; out[int(ch)] = r
        return out

    def solve(self, r0, r1, iters=300, log_every=0, log=print):
        """r0, r1 : poids par combo (1 326) d'OOP et d'IP. CFR+ alterné, stratégie moyenne pondérée par l'itération"""
        r0 = np.asarray(r0, float); r1 = np.asarray(r1, float)
        for _ in range(iters):
            self.t += 1
            for p in (0, 1):                                        # CFR+ alterné : un joueur après l'autre
                self._reach0 = self._flop_reach(r0, r1, 0); self._run(r0, r1, 0, upd=p)
            if log_every and self.t % log_every == 0 and log: log(f'  {self.t} itérations : exploitabilité {100 * self.exploitability(r0, r1):.2f} % du pot')
        return self

    def set_abstract(self, tab, buckets):
        """stratégie abstraite du solveur de production : tab (nœud original, groupe, action) ; buckets = (flop (1326),
        turns (49, 1326), rivers (49, 49, 1326) dont la ligne 0 est inutilisée)"""
        W = self.W; T = np.zeros((tab.shape[0], tab.shape[1], W)); T[:, :, :tab.shape[2]] = tab[:, :, :W]
        self.Tab = T; self.bk = buckets

    def values(self, r0, r1, mode=1, br=-1):
        """valeurs à la racine (2, 1326) : mode 1 stratégie moyenne exacte, 2 stratégie abstraite"""
        r0 = np.asarray(r0, float); r1 = np.asarray(r1, float)
        return self._run(r0, r1, mode, br=br).copy()

    def compat(self, r0, r1):
        m0 = np.zeros(1326); m1 = np.zeros(1326); v = self.valid_flop
        _compat(r1 * v, v, CC, m0); _compat(r0 * v, v, CC, m1)
        return m0, m1

    def exploitability(self, r0, r1, mode=1):
        """(gain moyen des deux meilleures réponses - pot) / 2, par couple de mains, en fraction du pot"""
        v0 = self.values(r0, r1, mode, br=0)[0]; v1 = self.values(r0, r1, mode, br=1)[1]
        m0, _ = self.compat(r0, r1); M = float((r0 * self.valid_flop * m0).sum())
        return ((float((r0 * v0).sum() + (r1 * v1).sum())) / M - self.P) / 2 / self.P


def flop_buckets(ex, B, rollouts, seed, metric='ehs'):
    """groupes de force de chaque combo, comme fast.board_pool : flop, chaque turn, chaque river"""
    def grp(board, k):
        b5 = np.array(board + [0] * (5 - len(board)), np.int64)
        s = _percentile(combo_ranks(b5, CC)) if k == 5 else strength(b5, k, b5, rollouts, CC, seed + k, metric == 'ehs2' and k < 5)
        if metric == 'ehs2' and k < 5:
            v = s >= 0; q = np.quantile(s[v], np.linspace(0, 1, B + 1)[1:-1]); g = np.where(v, np.searchsorted(q, s), 0)
        else:
            g = np.clip((s * B).astype(np.int64), 0, B - 1)
        return np.where(s >= 0, g, 0)
    T = len(ex.turns); b0 = grp(ex.flop, 3); b1 = np.zeros((T, 1326), np.int64); b2 = np.zeros((T, 49, 1326), np.int64)
    for ti, t in enumerate(ex.turns):
        b1[ti] = grp(ex.flop + [t], 4)
        for ri, r in enumerate(ex.rivers[ti]): b2[ti, ri + 1] = grp(ex.flop + [t, r], 5)
    return b0, b1, b2


def class_values(ex, V, r0, r1):
    """G par classe (169) des deux joueurs sur ce flop : somme des valeurs / somme des masses compatibles (comme fast_evaluate)"""
    m0, m1 = ex.compat(r0, r1); out = []
    for p, m in ((0, m0), (1, m1)):
        num = np.bincount(CLASS_OF, weights=V[p], minlength=169); den = np.bincount(CLASS_OF, weights=m, minlength=169)
        out.append((num, den))
    return out
