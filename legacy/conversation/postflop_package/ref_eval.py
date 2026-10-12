"""Évaluateur de référence, indépendant du noyau : algorithme volontairement différent (meilleure main de 5 cartes parmi les C(n,5) sous-ensembles)."""
from itertools import combinations
from collections import Counter

def score5(cards):
    """cards : liste de 5 cartes (rang 0..12, couleur 0..3) -> tuple comparable (catégorie, départages)"""
    ranks = sorted((r for r, s in cards), reverse=True)
    flush = len({s for r, s in cards}) == 1
    uniq = sorted(set(ranks), reverse=True)
    straight_high = None
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4: straight_high = uniq[0]
        elif uniq == [12, 3, 2, 1, 0]: straight_high = 3                     # roue A-2-3-4-5
    cnt = Counter(ranks)
    groups = sorted(cnt.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)     # (rang, multiplicité) triés par multiplicité puis rang
    shape = [m for _, m in groups]
    if flush and straight_high is not None: return (8, straight_high)
    if shape == [4, 1]: return (7, groups[0][0], groups[1][0])
    if shape == [3, 2]: return (6, groups[0][0], groups[1][0])
    if flush: return (5, *ranks)
    if straight_high is not None: return (4, straight_high)
    if shape == [3, 1, 1]: return (3, groups[0][0], groups[1][0], groups[2][0])
    if shape == [2, 2, 1]: return (2, groups[0][0], groups[1][0], groups[2][0])
    if shape == [2, 1, 1, 1]: return (1, groups[0][0], groups[1][0], groups[2][0], groups[3][0])
    return (0, *ranks)

def best(cards):
    """meilleure main parmi les sous-ensembles de 5 cartes ; cards : liste de (rang, couleur)"""
    return max(score5(list(c)) for c in combinations(cards, 5))

def compare(a_cards, b_cards):
    sa, sb = best(a_cards), best(b_cards)
    return (sa > sb) - (sa < sb)
