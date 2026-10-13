"""Profil postflop des 169 mains de départ, par énumération exacte des 19 600 flops (cartes de la main retirées).

Pour un combo représentatif de chaque classe (les couleurs ne changent pas les probabilités) :
  pair_plus      : la main fait au moins une paire avec ses propres cartes (paire du board seule exclue) ;
                   pour une paire servie, toujours vrai
  top_pair_plus  : paire max (une carte de la main avec la plus haute du board), overpair, deux paires ou mieux avec la main
  two_pair_plus  : deux paires ou mieux utilisant la main
  set_plus       : paire servie : brelan ou mieux
  overpair       : paire servie plus haute que les trois cartes du board
  flush_draw_plus: main assortie : au moins deux cartes de sa couleur au board (tirage couleur ou couleur)
  oesd_plus      : quinte faite ou tirage par les deux bouts (8 outs), avec au moins une carte de la main
  gutshot        : tirage ventral seul (4 outs)
  draw_plus      : tirage couleur ou par les deux bouts (ou couleur, quinte faite), sans double compte
  miss           : ni paire avec la main, ni tirage couleur, ni tirage par les deux bouts
Moyennes : moyenne de chaque indicateur, pondérée par le nombre de combos, sur toutes les mains (average), sur les mains
non pairées (average_unpaired) et sur les paires servies (average_pairs) : une main se compare à celles de son type.
Résultat : spinsacademy/data/postflop_profiles.json (le serveur n'exécute pas ce calcul).
Usage : python tools/postflop/flop_profiles.py
"""
import itertools, json, os, sys
import numpy as np
from numba import njit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy.cards import NAMES
from spinsacademy.postflop.kernels import evaln

RANKS = '23456789TJQKA'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'spinsacademy', 'data', 'postflop_profiles.json')


@njit(cache=True)
def _straight(mask):
    for hi in range(12, 3, -1):
        if ((mask >> (hi - 4)) & 31) == 31: return True
    return (mask & (1 << 12)) != 0 and (mask & 15) == 15


@njit(cache=True)
def _count(h0, h1):
    r0, r1, s0, s1 = h0 >> 2, h1 >> 2, h0 & 3, h1 & 3; pair = r0 == r1; suited = s0 == s1
    acc = np.zeros(10); cards = np.zeros(5, np.int64); n = 0
    for a in range(52):
        if a == h0 or a == h1: continue
        for b in range(a + 1, 52):
            if b == h0 or b == h1: continue
            for c in range(b + 1, 52):
                if c == h0 or c == h1: continue
                n += 1
                cards[0] = h0; cards[1] = h1; cards[2] = a; cards[3] = b; cards[4] = c
                cat = evaln(cards, 5) >> 20
                br = np.array([a >> 2, b >> 2, c >> 2]); top = br.max()
                hits0 = (br == r0).sum(); hits1 = (br == r1).sum()
                if pair:
                    pp = 1.0; setp = 1.0 if hits0 >= 1 else 0.0
                    over = 1.0 if r0 > top else 0.0
                    tp = 1.0 if (r0 > top or hits0 >= 1) else 0.0
                    # deux paires avec la main : paire servie + paire au board, ou mieux
                    bp = (br[0] == br[1]) or (br[0] == br[2]) or (br[1] == br[2])
                    tw = 1.0 if (setp == 1.0 or bp) else 0.0
                else:
                    pp = 1.0 if (hits0 + hits1) >= 1 or cat >= 4 else 0.0
                    tw = 1.0 if (hits0 >= 1 and hits1 >= 1) or hits0 >= 2 or hits1 >= 2 or cat >= 4 else 0.0
                    tp = 1.0 if ((r0 == top and hits0 >= 1) or (r1 == top and hits1 >= 1) or tw == 1.0) else 0.0
                    setp = 0.0; over = 0.0
                # couleur
                fd = 0.0
                if suited:
                    k = 0
                    if (a & 3) == s0: k += 1
                    if (b & 3) == s0: k += 1
                    if (c & 3) == s0: k += 1
                    if k >= 2: fd = 1.0
                # quinte : rangs qui complètent une quinte utilisant au moins une carte de la main
                full = (1 << r0) | (1 << r1) | (1 << (a >> 2)) | (1 << (b >> 2)) | (1 << (c >> 2))
                board = (1 << (a >> 2)) | (1 << (b >> 2)) | (1 << (c >> 2))
                made = _straight(full) and not _straight(board)
                outs = 0
                for x in range(13):
                    if (full >> x) & 1: continue
                    if _straight(full | (1 << x)) and not _straight(board | (1 << x)): outs += 1
                oesd = 1.0 if (made or outs >= 2) else 0.0
                gut = 1.0 if (not made and outs == 1) else 0.0
                miss = 1.0 if (pp == 0.0 or pair and False) and fd == 0.0 and oesd == 0.0 else 0.0
                if pair: miss = 0.0
                acc[0] += pp; acc[1] += tp; acc[2] += tw; acc[3] += setp; acc[4] += over
                acc[5] += fd; acc[6] += oesd; acc[7] += gut; acc[8] += miss
                acc[9] += 1.0 if (fd == 1.0 or oesd == 1.0) else 0.0
    return acc / n


def card(r, s): return RANKS.index(r) * 4 + s


def main():
    keys = ['pair_plus', 'top_pair_plus', 'two_pair_plus', 'set_plus', 'overpair', 'flush_draw_plus', 'oesd_plus', 'gutshot', 'miss', 'draw_plus']
    out = {}
    for h in NAMES:
        if len(h) == 2: c0, c1 = card(h[0], 0), card(h[1], 1)
        elif h[2] == 's': c0, c1 = card(h[0], 0), card(h[1], 0)
        else: c0, c1 = card(h[0], 0), card(h[1], 1)
        v = _count(min(c0, c1), max(c0, c1))
        out[h] = {k: round(float(x), 4) for k, x in zip(keys, v)}
    from spinsacademy.cards import W
    w = {h: float(W[i]) for i, h in enumerate(NAMES)}; tot = sum(w.values())
    mean = lambda hs: {k: round(sum(out[h][k] * w[h] for h in hs) / sum(w[h] for h in hs), 4) for k in keys}
    avg = mean(NAMES); pairs = [h for h in NAMES if len(h) == 2]; unpaired = [h for h in NAMES if len(h) == 3]
    json.dump(dict(version='1.2.0', method='énumération exacte des 19 600 flops, tools/postflop/flop_profiles.py', average=avg,
                   average_unpaired=mean(unpaired), average_pairs=mean(pairs), hands=out),
              open(OUT, 'w'), ensure_ascii=False, indent=0)
    print('moyenne', avg); print('non pairées', mean(unpaired)); print('paires', mean(pairs))
    for h in ('AA', '22', 'AKs', 'AKo', 'T9s', '72o', 'K4o', '54s'): print(h, out[h])


if __name__ == '__main__':
    main()
