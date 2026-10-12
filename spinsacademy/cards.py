"""Classes de mains préflop (grille 13 x 13) et combinaisons."""
import numpy as np

RANKS = '23456789TJQKA'
NC = lambda h: 6 if len(h) == 2 else (4 if h[2] == 's' else 12)


def _build():
    names, combos = [], []
    for row in range(13):
        for col in range(13):
            if row == col:
                r = 12 - row; names.append(RANKS[r] * 2)
                combos.append([(r * 4 + a, r * 4 + b) for a in range(4) for b in range(a + 1, 4)])
            elif row < col:
                hi, lo = 12 - row, 12 - col; names.append(RANKS[hi] + RANKS[lo] + 's')
                combos.append([(hi * 4 + s, lo * 4 + s) for s in range(4)])
            else:
                hi, lo = 12 - col, 12 - row; names.append(RANKS[hi] + RANKS[lo] + 'o')
                combos.append([(hi * 4 + a, lo * 4 + b) for a in range(4) for b in range(4) if a != b])
    return names, combos


NAMES, COMBOS = _build()
INDEX = {h: i for i, h in enumerate(NAMES)}
W = np.array([len(c) for c in COMBOS], float)          # nombre de combinaisons par classe (6, 4 ou 12)
_MASKS = [np.array([(1 << x) | (1 << y) for x, y in c], dtype=np.int64) for c in COMBOS]
# D[i, j] : nombre de couples (combo de i, combo de j) sans carte commune (effet de bloqueurs)
DISJOINT = np.array([[((mi[:, None] & mj[None, :]) == 0).sum() for mj in _MASKS] for mi in _MASKS], float)
