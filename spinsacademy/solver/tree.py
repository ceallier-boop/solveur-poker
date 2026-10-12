"""Arbre préflop Expresso (2 ou 3 joueurs) avec limp, relances et tapis.

Règles (paramétrables par TreeConfig) :
  - ordre de parole : BTN, SB, BB à 3 joueurs ; SB, BB en heads-up ; blinds 0,5 / 1, sans ante ;
  - premier à entrer : fold, limp (SB : compléter), open (BTN 2,3 BB, SB 3,5 BB), tapis ;
  - face à des limps : iso-raise du BB à 3 BB contre le seul SB, sinon 3,5 BB + 1 BB par limper ; le SB isole à 3,5 BB + 1 BB par limper ;
  - face à une relance : fold, call, 3-bet (multiplicateur de la relance + 1x par caller), tapis ;
  - face à un 3-bet : fold, call ou tapis ; ensuite fold ou call ;
  - au plus un call « à froid » par niveau de relance, sauf pour le joueur qui clôt l'action ;
  - une mise de plus de allin_fraction du tapis effectif devient un tapis ; le tapis est toujours proposé ;
  - une mise au-delà du plus gros tapis adverse encore en jeu est un tapis effectif.
Fin de tour : « fold » (un seul joueur restant), « showdown » (au moins un joueur à tapis : on abat les cartes),
ou « flop » (au moins deux joueurs avec des jetons derrière : valeur donnée par le modèle postflop).
"""
from dataclasses import dataclass, field

POS = {3: ('BTN', 'SB', 'BB'), 2: ('SB', 'BB')}
BLINDS = {3: (0.0, 0.5, 1.0), 2: (0.5, 1.0)}
EPS = 1e-9


@dataclass
class TreeConfig:
    open_btn: float = 2.3
    open_sb: float = 3.5
    iso_bb_vs_sb: float = 3.0
    iso_base: float = 3.5
    iso_per_limper: float = 1.0
    threebet_vs_btn: float = 3.3
    threebet_bb_vs_sb: float = 2.5
    threebet_sb_vs_bb: float = 2.6
    threebet_ip: float = 2.5
    threebet_per_caller: float = 1.0
    allin_fraction: float = 0.40
    max_raises: int = 3
    flats_per_level: int = 1
    allow_limp: bool = True


@dataclass
class Node:
    id: int
    kind: str                       # 'decision' ou 'terminal'
    key: str                        # clé lisible, même format que spinsacademy.hrc.key_of
    contrib: tuple                  # mises totales de chaque joueur
    folded: tuple
    player: int = -1
    actions: list = field(default_factory=list)       # étiquettes : F, X, C, R<x>, A
    children: list = field(default_factory=list)
    terminal: str = ''              # 'fold', 'showdown', 'flop'


class Tree:
    def __init__(self, stacks, cfg=None):
        self.st = tuple(float(x) for x in stacks); self.n = len(stacks); self.cfg = cfg or TreeConfig()
        self.names = POS[self.n]; self.nodes = []
        c = list(BLINDS[self.n]); c = [min(x, s) for x, s in zip(c, self.st)]
        self.root = self._build(tuple(c), (False,) * self.n, actor=0, acted=frozenset(), raises=0, last_raise=1.0,
                                aggressor=None, flats=0, limpers=(), callers=0, hist=())

    # ------------------------------------------------------------------ construction
    def _new(self, **kw):
        nd = Node(id=len(self.nodes), **kw); self.nodes.append(nd); return nd

    def _active(self, folded): return [p for p in range(self.n) if not folded[p]]

    def _left(self, c, p): return self.st[p] - c[p]

    def _cap(self, c, folded, p):
        others = [self.st[q] for q in self._active(folded) if q != p]
        return min(self.st[p], max(others)) if others else self.st[p]

    def _next(self, p, folded, c):
        for k in range(1, self.n + 1):
            q = (p + k) % self.n
            if not folded[q] and self._left(c, q) > EPS: return q
        return None

    def _round_over(self, c, folded, acted):
        act = self._active(folded); mx = max(c)
        live = [p for p in act if self._left(c, p) > EPS]
        if len(act) == 1: return True
        return all(p in acted and abs(c[p] - mx) < EPS for p in live) and all(c[p] >= mx - EPS or self._left(c, p) <= EPS for p in act)

    def _terminal(self, c, folded, hist):
        act = self._active(folded)
        if len(act) == 1: kind = 'fold'
        elif any(self._left(c, p) <= EPS for p in act): kind = 'showdown'
        else: kind = 'flop'
        return self._new(kind='terminal', key='_'.join(hist) or 'root', contrib=c, folded=folded, terminal=kind)

    def _raise_sizes(self, c, folded, p, raises, last_raise, limpers, callers, aggressor):
        cfg = self.cfg; names = self.names; mx = max(c)
        if raises == 0:
            if not limpers:
                size = cfg.open_btn if names[p] == 'BTN' else cfg.open_sb if names[p] == 'SB' else cfg.iso_base
            elif names[p] == 'BB' and limpers == (self.names.index('SB'),):
                size = cfg.iso_bb_vs_sb
            else:
                size = cfg.iso_base + cfg.iso_per_limper * len(limpers)
        elif raises == 1:
            ag = names[aggressor]
            if names[p] == 'BB' and ag == 'SB': mult = cfg.threebet_bb_vs_sb
            elif names[p] == 'SB' and ag == 'BB': mult = cfg.threebet_sb_vs_bb
            elif ag == 'BTN': mult = cfg.threebet_vs_btn
            else: mult = cfg.threebet_ip
            size = last_raise * (mult + cfg.threebet_per_caller * callers)
        else:
            return []                                      # 4-bet : tapis uniquement
        return [size] if size > mx + EPS else []

    def _build(self, c, folded, actor, acted, raises, last_raise, aggressor, flats, limpers, callers, hist):
        if self._round_over(c, folded, acted): return self._terminal(c, folded, hist)
        p = actor
        if folded[p] or self._left(c, p) <= EPS:
            q = self._next(p, folded, c)
            if q is None: return self._terminal(c, folded, hist)
            return self._build(c, folded, q, acted, raises, last_raise, aggressor, flats, limpers, callers, hist)
        node = self._new(kind='decision', key='_'.join(hist) or 'root', contrib=c, folded=folded, player=p)
        mx = max(c); to_call = mx - c[p]; name = self.names[p]; cap = self._cap(c, folded, p)
        opts = []                                          # (label, nouvelle mise totale, type)
        if to_call > EPS: opts.append(('F', c[p], 'fold'))
        else: opts.append(('X', c[p], 'check'))
        if to_call > EPS:
            closes = self._closes(c, folded, p, acted, aggressor)
            if (raises == 0 and self.cfg.allow_limp) or (raises > 0 and (flats < self.cfg.flats_per_level or closes)):
                opts.append(('C', min(mx, self.st[p]), 'call'))
        if raises < self.cfg.max_raises and cap > mx + EPS:
            for size in self._raise_sizes(c, folded, p, raises, last_raise, limpers, callers, aggressor):
                if size >= cap - EPS or size >= self.cfg.allin_fraction * cap - EPS: continue     # seuil sur le tapis effectif
                opts.append((f'R{round(size, 4):g}', size, 'raise'))
            opts.append(('A', cap, 'allin'))
        for lab, amt, typ in opts:
            c2 = list(c); f2 = list(folded); acted2 = set(acted) | {p}
            r2, lr2, ag2, fl2, lim2, cal2 = raises, last_raise, aggressor, flats, limpers, callers
            if typ == 'fold': f2[p] = True; t = 'fold'
            elif typ == 'check': t = 'check'
            elif typ == 'call':
                c2[p] = amt; t = 'call'
                if raises == 0: lim2 = limpers + (p,)
                else: fl2 = flats + 1; cal2 = callers + 1
            else:
                prev = max(c); c2[p] = amt; r2 = raises + 1; lr2 = amt; ag2 = p; fl2 = 0; cal2 = 0
                acted2 = {p}
                t = 'allin' if typ == 'allin' else f'raise{round(amt, 4):g}'
            child = self._build(tuple(c2), tuple(f2), (p + 1) % self.n, frozenset(acted2), r2, lr2, ag2, fl2, lim2, cal2,
                                hist + (f'{name}-{t}',))
            node.actions.append(lab); node.children.append(child)
        return node

    def _closes(self, c, folded, p, acted, aggressor):
        """vrai si, après p, l'action revient à l'agresseur (ou se termine) sans autre joueur à parler"""
        q = (p + 1) % self.n
        while q != p:
            if q == aggressor: return True
            if not folded[q] and self._left(c, q) > EPS: return False
            q = (q + 1) % self.n
        return True

    # ------------------------------------------------------------------ outils
    def decisions(self): return [n for n in self.nodes if n.kind == 'decision']

    def terminals(self): return [n for n in self.nodes if n.kind == 'terminal']

    def by_key(self): return {n.key: n for n in self.decisions()}
