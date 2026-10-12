import numpy as np, time
from numba import njit
import postflop_core as pc
from pushfold import eval7

# ---- 1) test de symétrie et de sanité sur des ranges simples
rng = np.random.default_rng(1)
wa = np.zeros(1326); wb = np.zeros(1326)
for k in rng.choice(1326, 300, replace=False): wa[k] = rng.random()
for k in rng.choice(1326, 300, replace=False): wb[k] = rng.random()
t = time.time(); e1 = pc.range_equity(['As', '7d', '2c'], wa, wb); dt = time.time() - t
e2 = pc.range_equity(['As', '7d', '2c'], wb, wa)
print(f"1) symétrie : eq(A,B)+eq(B,A) = {e1+e2:.12f} (attendu 1) ; temps {dt:.1f} s (compilation incluse)")

# ---- 2) validation contre une simulation indépendante (tirage aléatoire des mains et des cartes)
@njit(cache=True)
def mc_equity(board, wa, wb, CC, MASK, N, seed):
    np.random.seed(seed)
    ca = np.cumsum(wa) / wa.sum(); cb = np.cumsum(wb) / wb.sum()
    bm = np.int64(0)
    for k in range(3): bm |= (np.int64(1) << board[k])
    cards = np.zeros(7, np.int64); cards[2] = board[0]; cards[3] = board[1]; cards[4] = board[2]
    s = 0.0; n = 0
    while n < N:
        x = np.searchsorted(ca, np.random.random()); y = np.searchsorted(cb, np.random.random())
        if x > 1325: x = 1325
        if y > 1325: y = 1325
        if (MASK[x] & bm) != 0 or (MASK[y] & bm) != 0 or (MASK[x] & MASK[y]) != 0: continue
        used = bm | MASK[x] | MASK[y]
        t = np.random.randint(52)
        while (used >> t) & 1: t = np.random.randint(52)
        used |= (np.int64(1) << t)
        r = np.random.randint(52)
        while (used >> r) & 1: r = np.random.randint(52)
        cards[5] = t; cards[6] = r
        cards[0] = CC[x, 0]; cards[1] = CC[x, 1]; ra = eval7(cards)
        cards[0] = CC[y, 0]; cards[1] = CC[y, 1]; rb = eval7(cards)
        s += 1.0 if ra > rb else (0.5 if ra == rb else 0.0); n += 1
    return s / N
CC = pc.CC; MASK = pc.MASK
print("2) équité exacte contre simulation indépendante (3 000 000 tirages) :")
worst = 0
for board in (['As', '7d', '2c'], ['9s', '8s', '7d'], ['Kh', 'Qd', 'Jc'], ['Ts', 'Td', '4h']):
    wa = np.zeros(1326); wb = np.zeros(1326)
    for k in rng.choice(1326, 350, replace=False): wa[k] = rng.random()
    for k in rng.choice(1326, 350, replace=False): wb[k] = rng.random()
    ex = pc.range_equity(board, wa, wb)
    mc = mc_equity(np.array([pc.card(c) for c in board], dtype=np.int64), wa, wb, CC, MASK, 3000000, int(rng.integers(1e6)))
    se = 0.5 / np.sqrt(3000000)
    worst = max(worst, abs(ex - mc) / se)
    print(f"   {' '.join(board)} : exact {100*ex:.3f} %  simulation {100*mc:.3f} %  écart {100*(ex-mc):+.3f} pt ({abs(ex-mc)/se:.1f} erreurs-types)")
print(f"   pire écart : {worst:.1f} erreurs-types")

# ---- 3) cas connus : tirage couleur contre top pair, énumération exacte
def hv(h, board):
    wa = np.zeros(1326); wb = np.zeros(1326)
    return wa
def combo_index(c1, c2):
    a, b = sorted([pc.card(c1), pc.card(c2)]); return int(np.where((pc.CC[:, 0] == a) & (pc.CC[:, 1] == b))[0][0])
def eq_hands(h1, h2, board):
    wa = np.zeros(1326); wb = np.zeros(1326); wa[combo_index(*h1)] = 1; wb[combo_index(*h2)] = 1
    return pc.range_equity(board, wa, wb)
print("3) cas connus (énumération exacte de la turn et de la river) :")
print(f"   Ah Kh contre Qs Qd sur 2h 7h 9c : {100*eq_hands(('Ah','Kh'),('Qs','Qd'),['2h','7h','9c']):.2f} %  (tirage couleur nut + deux surcartes contre une paire de dames ; attendu entre 40 et 55 %)")
print(f"   As Ks contre Qh Qd sur 2c 7d 9s : {100*eq_hands(('As','Ks'),('Qh','Qd'),['2c','7d','9s']):.2f} %  (deux surcartes contre une paire ; attendu environ 28 à 32 %)")
print(f"   Ah 2h contre Kd Kc sur 7h 8h Jc  : {100*eq_hands(('Ah','2h'),('Kd','Kc'),['7h','8h','Jc']):.2f} %  (tirage couleur nut contre une paire de rois ; règle des 4 et 2 : 9 outs, environ 35 %)")
