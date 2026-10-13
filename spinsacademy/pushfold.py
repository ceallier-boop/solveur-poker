"""Équilibre push/fold (Nash) en chip EV, effet de bloqueurs compris : référence des profils exploitants (générateur 2.0.0).

Pourquoi : l'arbre HRC autorise le limp, et le SB y limpe ses paires hautes (AA à QQ à 100 % de 8 à 18 BB). La range
de tapis HRC n'est donc pas une range de tapis réaliste : un profil « serré » qui en dérive n'a aucune paire haute
(relecture du 2026-10-13). Ici, le joueur qui parle en premier n'a que deux options, tapis ou fold, comme un joueur qui
ne limpe jamais ; ses adversaires paient ou se couchent.

Situations couvertes (celles des calls de tapis à EV exacte) :
  - heads-up : SB tapis ou fold, BB paie ou se couche ;
  - 3 joueurs, BTN couché : idem entre SB et BB (pas d'argent mort) ;
  - 3 joueurs, BTN tapis ou fold : le SB paie ou se couche, puis le BB si le SB s'est couché. Approximation : si le SB
    paie, le BB se couche (pas de sur-call) ; les probabilités de call du SB et du BB sont supposées indépendantes.
Résolution par jeu fictif (meilleures réponses successives, stratégies moyennées), sur les 169 classes de mains.
"""
from functools import lru_cache
import numpy as np
from .allin import E, call_ev
from .cards import DISJOINT

ITERATIONS = 400


def _cond(r):
    """P(j | ma main i) pour un adversaire de range r (poids par classe), cartes retirées"""
    P = DISJOINT * np.asarray(r, float)[None, :]
    return P / P.sum(1, keepdims=True)


def _hu_shove_ev(c, L, my_blind, his_blind, dead=0.0):
    """EV (relative au fold) du tapis contre un adversaire qui paie avec la fréquence c par classe"""
    P = _cond(np.ones(169)); sd = E * (2 * L + dead) - L
    return (P * ((1 - c)[None, :] * (his_blind + dead) + c[None, :] * sd)).sum(1) + my_blind


@lru_cache(maxsize=256)
def heads_up(L, my_blind=0.5, his_blind=1.0):
    """(fréquence de tapis, fréquence de call, EV du tapis à l'équilibre) ; L = tapis effectif en BB"""
    push = np.ones(169); call = np.zeros(169); ps = np.zeros(169); cs = np.zeros(169)
    for n in range(1, ITERATIONS + 1):
        bc = (call_ev(push, L, 0.0, his_blind) > 0).astype(float)              # meilleure réponse du joueur qui paie
        cs += bc; call = cs / n
        bp = (_hu_shove_ev(call, L, my_blind, his_blind) > 0).astype(float)    # meilleure réponse du joueur qui pousse
        ps += bp; push = ps / n
    return push, call, _hu_shove_ev(call, L, my_blind, his_blind)


@lru_cache(maxsize=256)
def three_way_button(btn, sb, bb):
    """BTN tapis ou fold contre SB puis BB : (fréquence de tapis du BTN, call du SB, call du BB, EV du tapis du BTN)"""
    Ls, Lb = min(btn, sb), min(btn, bb)
    push = np.ones(169); cs_s = np.zeros(169); cs_b = np.zeros(169); ps = np.zeros(169)
    c_s = np.zeros(169); c_b = np.zeros(169)
    P = _cond(np.ones(169)); sd_s = E * (2 * Ls + 1.0) - Ls; sd_b = E * (2 * Lb + 0.5) - Lb

    def shove(c_s, c_b):
        after = (P * ((1 - c_b)[None, :] * 1.5 + c_b[None, :] * sd_b)).sum(1)   # le SB s'est couché
        return (P * c_s[None, :] * sd_s).sum(1) + (1 - P @ c_s) * after

    for n in range(1, ITERATIONS + 1):
        cs_s += (call_ev(push, Ls, 1.0, 0.5) > 0); c_s = cs_s / n               # le SB paie (blinde du BB morte)
        cs_b += (call_ev(push, Lb, 0.5, 1.0) > 0); c_b = cs_b / n               # le BB paie après le fold du SB
        ps += (shove(c_s, c_b) > 0); push = ps / n
    return push, c_s, c_b, shove(c_s, c_b)


def shover_range(sp, villain_pos):
    """(fréquence de tapis à l'équilibre push/fold, EV de ces tapis) du joueur qui pousse dans le call de tapis sp"""
    st = dict(zip(sp['players'], sp['stacks_bb']))
    if sp['table'] == 'heads-up' or villain_pos == 'SB':
        hero = sp['hero']; L = min(st[villain_pos], st[hero])
        push, _, value = heads_up(round(L, 4))
        return push, value
    push, _, _, value = three_way_button(st['BTN'], st['SB'], st['BB'])
    return push, value
