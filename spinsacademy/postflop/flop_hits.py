"""Chances exactes de toucher au flop, par classe de main (CE2, 10/11/2026) : énumération de tous les flops (19 600 par combinaison de départ).

« Toucher » : la main améliore le tableau seul, donc au moins une de ses cartes sert. Une paire ou un brelan qui est déjà sur le tableau
n'est pas touché par la main ; la catégorie est celle de la meilleure main de cinq cartes, quand elle bat la catégorie du tableau seul.

Catégories exclusives (la meilleure main touchée ; leur somme fait 100 %, « rien » comprise) : voir HITS.
Tirages (indépendants des catégories, comptés seulement si la main n'est pas déjà une suite, une couleur ou mieux) : voir DRAWS.
  - tirage couleur : quatre cartes de la même couleur parmi les cinq, dont au moins une de la main ;
  - tirage quinte à 8 outs : au moins deux rangs complètent une suite (ouvert, ou double ventral) ;
  - tirage quinte à 4 outs : un seul rang complète une suite (ventral, ou quatre cartes d'une extrémité) ;
  - tirage couleur et quinte : un tirage couleur avec au moins un rang qui complète une suite.
Les valeurs sont des comptes de flops ; equities.py les convertit en dix-millièmes (somme exacte à 10 000).
"""
import itertools
import numpy as np
from numba import njit
from .kernels import CC, CLASS_OF

HITS = ['rien', 'paire_poche_sous_tableau', 'paire_basse', 'paire_intermediaire', 'top_paire', 'paire_poche_sur_tableau', 'double_paire', 'set',
        'brelan', 'suite', 'couleur', 'full', 'carre', 'quinte_flush']
DRAWS = ['tirage_couleur', 'tirage_quinte_8', 'tirage_quinte_4', 'tirage_couleur_et_quinte']
N_FLOPS = 19600                                 # C(50, 3) : flops possibles pour une combinaison de départ (ses deux cartes sont retirées)


@njit(cache=True)
def _rank_cat(cnt, suit_cnt, mask):
    """0 carte haute, 1 paire, 2 double paire, 3 brelan, 4 suite, 5 couleur, 6 full, 7 carré, 8 quinte flush (cinq cartes au plus)"""
    pairs = 0; trips = 0; quads = 0
    for r in range(13):
        if cnt[r] == 2: pairs += 1
        elif cnt[r] == 3: trips += 1
        elif cnt[r] == 4: quads += 1
    flush = False
    for s in range(4):
        if suit_cnt[s] == 5: flush = True
    straight = False
    for lo in range(9):
        if (mask >> lo) & 31 == 31: straight = True
    if (mask & 0b1000000001111) == 0b1000000001111: straight = True
    if straight and flush: return 8
    if quads: return 7
    if trips and pairs: return 6
    if flush: return 5
    if straight: return 4
    if trips: return 3
    if pairs == 2: return 2
    if pairs == 1: return 1
    return 0


@njit(cache=True)
def classify(h1, h2, f0, f1, f2):
    """(catégorie touchée 0..13 dans l'ordre de HITS, tirage couleur, nombre de rangs qui complètent une suite)"""
    cnt = np.zeros(13, np.int64); suit = np.zeros(4, np.int64); hole_suit = np.zeros(4, np.int64)
    bcnt = np.zeros(13, np.int64); bsuit = np.zeros(4, np.int64)
    cards = (h1, h2, f0, f1, f2)
    for i in range(5):
        cnt[cards[i] // 4] += 1; suit[cards[i] % 4] += 1
    for c in (f0, f1, f2):
        bcnt[c // 4] += 1; bsuit[c % 4] += 1
    hole_suit[h1 % 4] += 1; hole_suit[h2 % 4] += 1
    mask = 0; bmask = 0
    for r in range(13):
        if cnt[r] > 0: mask |= 1 << r
        if bcnt[r] > 0: bmask |= 1 << r
    cat = _rank_cat(cnt, suit, mask); bcat = _rank_cat(bcnt, bsuit, bmask)
    hit = 0
    if cat > bcat:                                                    # la main améliore le tableau seul : au moins une de ses cartes sert
        if cat == 1:
            pr = 0
            for q in range(13):
                if cnt[q] == 2: pr = q
            maxb = max(f0 // 4, f1 // 4, f2 // 4); lowb = min(f0 // 4, f1 // 4, f2 // 4)
            if h1 // 4 == h2 // 4: hit = 5 if pr > maxb else 1
            elif pr == maxb: hit = 4
            elif pr == lowb: hit = 2
            else: hit = 3
        elif cat == 2: hit = 6
        elif cat == 3: hit = 7 if h1 // 4 == h2 // 4 else 8
        elif cat == 4: hit = 9
        elif cat == 5: hit = 10
        elif cat == 6: hit = 11
        elif cat == 7: hit = 12
        else: hit = 13
    fd = False
    for s in range(4):
        if suit[s] == 4 and hole_suit[s] >= 1: fd = True
    outs = 0
    for r in range(13):
        if (mask >> r) & 1: continue
        m2 = mask | (1 << r); ok = False
        for lo in range(9):
            if (m2 >> lo) & 31 == 31: ok = True
        if (m2 & 0b1000000001111) == 0b1000000001111: ok = True
        if ok: outs += 1
    if cat >= 4:                                                      # déjà suite, couleur ou mieux : plus de tirage
        fd = False; outs = 0
    return hit, fd, outs


@njit(cache=True)
def _run(flops, CC, CLASS_OF):
    hits = np.zeros((169, 14), np.int64); draws = np.zeros((169, 4), np.int64); n = np.zeros(169, np.int64)
    for k in range(flops.shape[0]):
        f0, f1, f2 = flops[k, 0], flops[k, 1], flops[k, 2]
        for i in range(CC.shape[0]):
            a, b = CC[i, 0], CC[i, 1]
            if a == f0 or a == f1 or a == f2 or b == f0 or b == f1 or b == f2: continue
            c = CLASS_OF[i]; hit, fd, outs = classify(a, b, f0, f1, f2)
            hits[c, hit] += 1; n[c] += 1
            if fd: draws[c, 0] += 1
            if outs >= 2: draws[c, 1] += 1
            elif outs == 1: draws[c, 2] += 1
            if fd and outs >= 1: draws[c, 3] += 1
    return hits, draws, n


def counts():
    """(hits (169, 14), draws (169, 4), n (169)) : comptes de flops sur toutes les combinaisons de départ de chaque classe ; n = combinaisons × 19 600"""
    flops = np.array(list(itertools.combinations(range(52), 3)), np.int64)
    return _run(flops, CC, CLASS_OF)
