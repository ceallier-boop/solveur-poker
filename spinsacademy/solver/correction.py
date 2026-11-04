"""Correction des gains postflop apprise du calcul exact (action G17, 03/11/2026).

Défaut corrigé : le solveur postflop abstrait partage une stratégie entre des boards différents (groupes de force communs).
Les mains qui attrapent les bluffs (paires, Kx faibles) ont besoin de décisions propres au board : le solveur abstrait les
sous-évalue de plusieurs centaines de mBB dans les pots relancés (docs/solver/BANQUE_SOLVEUR.md, section G17), et le
préflop les couche à tort.

Principe : sur des sous-jeux heads-up de pots relancés tirés de notre propre banque (ranges réelles d'arrivée au flop), on
résout exactement des flops au hasard (postflop.exact_flop) et on y rejoue la stratégie abstraite. L'écart exact - abstrait
des gains G par classe, en fraction du pot, est la correction. Elle dépend du rôle du joueur dans le duel (agresseur ou
appelant, hors de position ou en position) et du rapport tapis / pot (SPR) ; elle vaut 0 à SPR nul (pas de jeu après le
flop) et est interpolée linéairement entre les SPR appris, constante au-delà du dernier.

Application (pipeline._subgame) : G += pot * correction(rôle, SPR)[classe], avant fit_offsets, pour les duels qui ont un
agresseur préflop (pots relancés). La table est un fichier JSON versionné ; SolveParams.correction en donne le nom (None :
pas de correction), ce qui change l'empreinte des résultats.
"""
import json, os
import numpy as np
from ..cards import NAMES, W as NCOMB
from ..postflop.kernels import CLASS_OF

DIR = os.path.join(os.path.dirname(__file__), 'corrections')
ROLES = ('oop_caller', 'ip_caller', 'oop_aggressor', 'ip_aggressor')
R_ = '23456789TJQKA'


def role(player, aggressor):
    """player : 0 OOP, 1 IP ; aggressor : 0 OOP, 1 IP (agresseur préflop du duel)"""
    return ('oop_' if player == 0 else 'ip_') + ('aggressor' if aggressor == player else 'caller')


def family(h):
    if len(h) == 2:
        r = R_.index(h[0]); return 'petites paires' if r <= 4 else 'paires moyennes' if r <= 8 else 'grosses paires'
    s = h[2] == 's'; a, b = R_.index(h[0]), R_.index(h[1])
    if h[0] == 'A': return 'As assortis' if s else 'As dépareillés'
    if h[0] == 'K': return 'Kx assortis' if s else 'Kx dépareillés'
    if a >= 8 and b >= 8: return 'broadways assortis' if s else 'broadways dépareillés'
    if s and a - b <= 2: return 'connecteurs assortis'
    return 'autres assorties' if s else 'autres dépareillées'


FAMILY = [family(h) for h in NAMES]


class Table:
    """correction(role, spr) -> (169) en fraction du pot"""

    def __init__(self, data):
        self.data = data; self.name = data['name']; self.min_stack = float(data.get('min_stack', 0))
        self.knots = {r: sorted((float(k['spr']), np.array(k['delta'], float)) for k in data['roles'].get(r, [])) for r in ROLES}

    @classmethod
    def load(cls, name):
        return cls(json.load(open(os.path.join(DIR, name + '.json'))))

    def __call__(self, rl, spr):
        ks = self.knots.get(rl) or []
        if not ks or spr <= 0: return np.zeros(169)
        xs = [0.0] + [k[0] for k in ks]; ys = [np.zeros(169)] + [k[1] for k in ks]
        if spr >= xs[-1]: return ys[-1].copy()
        j = int(np.searchsorted(xs, spr)); t = (spr - xs[j - 1]) / (xs[j] - xs[j - 1])
        return (1 - t) * ys[j - 1] + t * ys[j]

    def apply(self, pot, stack, aggressor, G0, G1, eff=None):
        """gains corrigés d'un duel ; aggressor : 0 OOP, 1 IP, -1 aucun (pot limpé, ou agresseur hors du duel) : inchangés.
        eff : tapis de départ effectif du duel (le plus petit des deux, BB) ; sous min_stack, inchangés (le contrôle hors
        échantillon dégradait deux rôles sur quatre à 8 BB)"""
        if aggressor not in (0, 1) or (eff is not None and eff < self.min_stack): return G0, G1
        spr = stack / pot
        return G0 + pot * self(role(0, aggressor), spr), G1 + pot * self(role(1, aggressor), spr)


_CACHE = {}


def get(name):
    if name not in _CACHE: _CACHE[name] = Table.load(name)
    return _CACHE[name]


# ------------------------------------------------------------------ apprentissage
def fit(samples, shrink=8.0):
    """samples : liste de dict(role, spr, pot, d_num (169), den (169), flops) où d_num = somme sur les flops de
    (valeur exacte - valeur abstraite) par classe et den la somme des masses compatibles. Par rôle et par SPR : écart par
    classe en fraction du pot, rapproché de la moyenne de sa famille selon la masse observée (classes peu jouées : surtout la
    famille), poids `shrink` en équivalent flops."""
    groups = {}
    for s in samples:
        groups.setdefault((s['role'], round(s['spr'], 2)), []).append(s)
    out = {}
    for (rl, spr), ss in sorted(groups.items()):
        num = sum(np.asarray(s['d_num']) / s['pot'] for s in ss); den = sum(np.asarray(s['den'], float) for s in ss)
        nfl = sum(s['flops'] for s in ss)
        d = np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)
        w = den * NCOMB
        fam = {}
        for f in set(FAMILY):
            ix = [i for i in range(169) if FAMILY[i] == f and w[i] > 0]
            fam[f] = float(np.average(d[ix], weights=w[ix])) if ix else 0.0
        # part de flops où la classe est présente (masse relative), convertie en équivalent flops
        share = np.where(den > 0, den / max(den.max(), 1e-12), 0.0) * nfl
        lam = share / (share + shrink)
        delta = np.array([fam[FAMILY[i]] for i in range(169)]) * (den > 0) + lam * (d - np.array([fam[FAMILY[i]] for i in range(169)]))
        delta = np.where(den > 0, delta, np.array([fam[FAMILY[i]] for i in range(169)]))
        out.setdefault(rl, []).append(dict(spr=spr, flops=nfl, delta=[round(float(x), 5) for x in delta]))
    return out
