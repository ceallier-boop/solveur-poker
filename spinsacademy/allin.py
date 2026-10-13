"""EV exactes (chip EV) des décisions d'all-in à deux joueurs, effet de bloqueurs compris.

Toutes les EV sont relatives au fold, comme dans les exports HRC, et exprimées en BB.
  - call d'un all-in :  eq * (2 L + mort) - L + blind_payée
  - all-in contre un seul joueur restant :
      somme sur ses mains j de P(j | ma main) * [ (1 - c_j) * (sa blind + mort) + c_j * (E_ij * (2 L + mort) - L) ] + ma blind
L = stack effectif. P(j | ma main) est proportionnel au nombre de combos disjoints D_ij et au poids d'atteinte de j.
"""
import os
import numpy as np
from .cards import DISJOINT

EQUITY_FILE = os.path.join(os.path.dirname(__file__), 'data', 'equity_169.npy')
E = np.load(EQUITY_FILE)       # E[i, j] : équité de la classe i contre la classe j (combos disjoints)


def equity_vs_range(q):
    """équité de chaque classe contre la range q (poids par classe, 169 valeurs) ; nan si la range est vide une fois bloquée"""
    J = DISJOINT * np.asarray(q, float)[None, :]
    den = J.sum(1)
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.where(den > 0, (J * E).sum(1) / den, np.nan)


def call_ev(shove_range, L, dead=0.0, blind=0.0):
    return equity_vs_range(shove_range) * (2 * L + dead) - L + blind


def shove_ev(caller_reach, caller_call, L, dead=0.0, my_blind=0.0, his_blind=0.0):
    r = np.asarray(caller_reach, float); c = np.asarray(caller_call, float)
    P = DISJOINT * r[None, :]
    P = P / P.sum(1, keepdims=True)
    win_fold = his_blind + dead
    showdown = E * (2 * L + dead) - L
    return (P * ((1 - c)[None, :] * win_fold + c[None, :] * showdown)).sum(1) + my_blind


# Nœuds où un calcul exact est possible (clés au format spinsacademy.hrc.key_of)
#   call : nœud du joueur qui paie -> (nœud et action du shove, indices des deux joueurs, argent mort, blind payée par celui qui paie)
#   shove : nœud du joueur qui pousse -> (nœud de réponse de l'adversaire, indices, argent mort, blind du héros, blind de l'adversaire)
CALL_NODES = {
    2: {'SB-allin': (('root', 'A'), (0, 1), 0.0, 1.0),
        'SB-call_BB-allin': (('SB-call', 'A'), (0, 1), 0.0, 1.0),          # le SB a complété, le BB pousse
        'SB-raise3.5_BB-allin': (('SB-raise3.5', 'A'), (0, 1), 0.0, 3.5)},  # le SB a relancé à 3,5 BB, le BB pousse
    3: {'BTN-fold_SB-allin': (('BTN-fold', 'A'), (1, 2), 0.0, 1.0),
        'BTN-allin_SB-fold': (('root', 'A'), (0, 2), 0.5, 1.0)},
}
SHOVE_NODES = {
    2: {'root': ('SB-allin', (0, 1), 0.0, 0.5, 1.0)},
    3: {'BTN-fold': ('BTN-fold_SB-allin', (1, 2), 0.0, 0.5, 1.0)},
}
APPROXIMATE_3WAY = True   # à 3 joueurs, les cartes du joueur qui a foldé ne sont pas retirées du paquet
