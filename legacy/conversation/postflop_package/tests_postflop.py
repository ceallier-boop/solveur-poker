"""Tests autonomes du noyau postflop (aucune dépendance au modèle préflop) : python tests_postflop.py"""
import json, time, sys
from itertools import combinations
import numpy as np
from numba import njit
import postflop_core as pc
import ref_eval

FAILS = []
def check(cond, msg):
    print(("  OK  " if cond else "  ÉCHEC ") + msg)
    if not cond: FAILS.append(msg)

# ============ 1. évaluateur : dénombrement exact de toutes les mains de 5 puis de 7 cartes
@njit(cache=True)
def count5():
    cnt = np.zeros(9, np.int64); c = np.zeros(5, np.int64)
    for a in range(52):
        for b in range(a + 1, 52):
            for d in range(b + 1, 52):
                for e in range(d + 1, 52):
                    for f in range(e + 1, 52):
                        c[0] = a; c[1] = b; c[2] = d; c[3] = e; c[4] = f
                        cnt[pc.evaln(c, 5) >> 20] += 1
    return cnt

@njit(cache=True)
def count7():
    cnt = np.zeros(9, np.int64); c = np.zeros(7, np.int64)
    for a in range(52):
        for b in range(a + 1, 52):
            for d in range(b + 1, 52):
                for e in range(d + 1, 52):
                    for f in range(e + 1, 52):
                        for g in range(f + 1, 52):
                            for h in range(g + 1, 52):
                                c[0] = a; c[1] = b; c[2] = d; c[3] = e; c[4] = f; c[5] = g; c[6] = h
                                cnt[pc.evaln(c, 7) >> 20] += 1
    return cnt

print("1) évaluateur de mains")
K5 = [1302540, 1098240, 123552, 54912, 10200, 5108, 3744, 624, 40]       # carte haute, paire, double paire, brelan, quinte, couleur, full, carré, quinte flush
K7 = [23294460, 58627800, 31433400, 6461620, 6180020, 4047644, 3473184, 224848, 41584]
c5 = count5(); check([int(x) for x in c5] == K5, "5 cartes : les 2 598 960 mains sont réparties exactement comme la théorie (carte haute 1 302 540, paire 1 098 240, double paire 123 552, brelan 54 912, quinte 10 200, couleur 5 108, full 3 744, carré 624, quinte flush 40)")
t = time.time(); c7 = count7(); check([int(x) for x in c7] == K7, f"7 cartes : les 133 784 560 mains sont réparties comme la théorie ({time.time()-t:.0f} s)")
rng = np.random.default_rng(3); bad = 0; N = 60000
for _ in range(N):
    cs = [int(x) for x in rng.choice(52, 14, replace=False)]; a = cs[:7]; b = cs[7:]
    ra = pc.evaln(np.array(a, dtype=np.int64), 7); rb = pc.evaln(np.array(b, dtype=np.int64), 7)
    mine = int(ra > rb) - int(ra < rb)
    ref = ref_eval.compare([(x // 4, x % 4) for x in a], [(x // 4, x % 4) for x in b])
    bad += mine != ref
check(bad == 0, f"classement identique à l'évaluateur de référence sur {N} duels de 7 cartes ({bad} désaccord(s))")

# ============ 2. équité : propriétés exactes
print("2) équité")
def rand_range(n, rng):
    w = np.zeros(1326)
    for k in rng.choice(1326, n, replace=False): w[k] = rng.random() + 0.05
    return w
rng = np.random.default_rng(1)
wa = rand_range(300, rng); wb = rand_range(300, rng)
for board in (['As', '7d', '2c'], ['9s', '8s', '7d', 'Kh'], ['Ts', 'Td', '4h', '4d', '2c']):
    e1 = pc.range_equity(board, wa, wb); e2 = pc.range_equity(board, wb, wa)
    check(abs(e1 + e2 - 1) < 1e-10, f"conservation (tolérance 1e-10, arrondi des sommes en flottants) sur {' '.join(board)} : équité A + équité B = {e1+e2:.15f}")
d = pc.equity_breakdown(['As', '7d', '2c'], wa, wb)
check(abs(d['win'] + d['tie'] + d['loss'] - 1) < 1e-12, "gain + égalité + perte = 1")

@njit(cache=True)
def mc(board, wa, wb, CC, MASK, N, seed):
    np.random.seed(seed)
    ca = np.cumsum(wa) / wa.sum(); cb = np.cumsum(wb) / wb.sum(); L = len(board)
    bm = np.int64(0)
    for k in range(L): bm |= (np.int64(1) << board[k])
    cards = np.zeros(7, np.int64)
    for k in range(L): cards[2 + k] = board[k]
    s = 0.0; n = 0
    while n < N:
        x = min(np.searchsorted(ca, np.random.random()), 1325); y = min(np.searchsorted(cb, np.random.random()), 1325)
        if (MASK[x] & bm) != 0 or (MASK[y] & bm) != 0 or (MASK[x] & MASK[y]) != 0: continue
        used = bm | MASK[x] | MASK[y]
        for k in range(5 - L):
            t = np.random.randint(52)
            while (used >> t) & 1: t = np.random.randint(52)
            used |= (np.int64(1) << t); cards[2 + L + k] = t
        cards[0] = CC[x, 0]; cards[1] = CC[x, 1]; ra = pc.evaln(cards, 7)
        cards[0] = CC[y, 0]; cards[1] = CC[y, 1]; rb = pc.evaln(cards, 7)
        s += 1.0 if ra > rb else (0.5 if ra == rb else 0.0); n += 1
    return s / N

def cls_range(names):
    f = np.zeros(169)
    for n in names: f[pc.CLASS_NAMES.index(n)] = 1.0
    return pc.range_from_class_freq(f)
aces = np.array([1.0 if (c[0] // 4 == 12 or c[1] // 4 == 12) else 0.0 for c in pc.CC])              # toutes les mains avec un as : très bloquées
spades = np.array([1.0 if (c[0] % 4 == 3 and c[1] % 4 == 3) else 0.0 for c in pc.CC])              # uniquement des mains assorties en pique
top = cls_range(['AA', 'KK', 'QQ', 'JJ', 'AKs', 'AKo', 'AQs']); wide = cls_range([n for n in pc.CLASS_NAMES if n[1] != n[0] or True][:100])
CASES = [("ranges larges aléatoires", wa, wb), ("range concentrée (top 7 classes) contre large", top, wb), ("deux ranges d'as (très bloquées)", aces, aces),
         ("pique assorti contre as", spades, aces), ("range contre la même range", wb, wb)]
N = 4_000_000; worst = 0.0
for name, a, b in CASES:
    for board in (['As', '7d', '2c'], ['9s', '8s', '7s']):
        try: ex = pc.range_equity(board, a, b)
        except ValueError as e: print("   ignoré :", name, board, e); continue
        m = mc(np.array([pc.card(c) for c in board], dtype=np.int64), a, b, pc.CC, pc.MASK, N, int(rng.integers(1e6)))
        z = abs(ex - m) / (0.5 / np.sqrt(N)); worst = max(worst, z)
        print(f"   {name:46s} {' '.join(board)} : exact {100*ex:.3f} % simulation {100*m:.3f} % ({z:.1f} erreurs-types)")
check(worst < 4.5, f"énumération exacte contre simulation indépendante : pire écart {worst:.1f} erreurs-types (seuil 4,5)")
e_single = pc.hand_vs_range(('Ah', 'Kh'), ['2h', '7h', '9c'], single := pc.single_combo('Qs', 'Qd'))
check(0.50 < e_single < 0.58, f"Ah Kh contre Qs Qd sur 2h 7h 9c : {100*e_single:.2f} % (15 outs environ)")

# ============ 3. entrées invalides
print("3) entrées invalides")
def raises(f):
    try: f(); return False
    except ValueError: return True
check(raises(lambda: pc.range_equity(['As', 'As', '2c'], wa, wb)), "board avec carte dupliquée refusé")
check(raises(lambda: pc.range_equity(['As', '2c'], wa, wb)), "board de 2 cartes refusé")
check(raises(lambda: pc.range_equity(['As', '7d', '2c'], -wa, wb)), "poids négatifs refusés")
check(raises(lambda: pc.range_equity(['As', '7d', '2c'], np.zeros(1326), wb)), "range vide refusée")
check(raises(lambda: pc.range_equity(['As', '7d', '2c'], wa[:100], wb)), "mauvaise taille refusée")
only_as = np.zeros(1326); only_as[int(np.where((pc.CC[:, 0] == pc.card('As')) | (pc.CC[:, 1] == pc.card('As')))[0][0])] = 1
check(raises(lambda: pc.range_equity(['As', '7d', '2c'], only_as, wb)), "range entièrement bloquée par le board refusée")
check(raises(lambda: pc.card('1x')), "carte invalide refusée")

# ============ 4. métriques distinctes : cohérence interne
print("4) métriques")
ok = True
for board in (['As', '7d', '2c'], ['9s', '8s', '7d'], ['Kh', 'Qd', 'Jc'], ['6c', '5c', '2d']):
    cat = pc.flop_categories(board, wa); ok &= abs(sum(cat.values()) - 1) < 1e-12
    mh = pc.made_hand_comparison(board, wa, wb); ok &= abs(mh['ahead'] + mh['tied'] + mh['behind'] - 1) < 1e-12
    it = pc.improvement(board, wa, 'turn'); ir = pc.improvement(board, wa, 'river'); ok &= (0 <= it <= ir <= 1)
    dr = pc.draws(board, wa); ok &= all(0 <= v <= 1 for v in dr.values())
check(ok, "somme des catégories = 1 ; devant + égalité + derrière = 1 ; amélioration turn <= river dans [0, 1] ; tirages dans [0, 1]")
# deux métriques qui ne doivent pas être confondues : devant maintenant, équité
mh = pc.made_hand_comparison(['9s', '8s', '7d'], wa, wb); eq = pc.range_equity(['9s', '8s', '7d'], wa, wb)
print(f"   exemple de métriques distinctes sur 9s 8s 7d : devant maintenant {100*mh['ahead']:.1f} %, équité {100*eq:.1f} %, amélioration d'ici la river {100*pc.improvement(['9s','8s','7d'], wa, 'river'):.1f} %")
# probabilités de tirage exactes
from math import comb
d1 = pc.draws_of_combo(['7h', '8h', 'Jc'], 'Ah', '2h')
check(abs(d1['p_couleur_river'] - (1 - comb(38, 2) / comb(47, 2))) < 1e-12 and d1['tirage_couleur'], f"tirage couleur à 9 outs : {100*d1['p_couleur_river']:.2f} % d'ici la river (théorie {100*(1-comb(38,2)/comb(47,2)):.2f} %)")
d2 = pc.draws_of_combo(['7d', '6c', '2h'], '9s', '8s')
check(d2['outs_quinte'] == 8 and abs(d2['p_quinte_ou_mieux_river'] - (1 - comb(39, 2) / comb(47, 2))) < 1e-12, f"tirage de quinte ouvert à 8 outs : {100*d2['p_quinte_ou_mieux_river']:.2f} % (théorie {100*(1-comb(39,2)/comb(47,2)):.2f} %)")
d3 = pc.draws_of_combo(['6c', '5h', 'Kd'], '9s', '8s')
check(d3['outs_quinte'] == 4 and abs(d3['p_quinte_ou_mieux_river'] - (1 - comb(43, 2) / comb(47, 2))) < 1e-12, f"tirage de quinte interne à 4 outs : {100*d3['p_quinte_ou_mieux_river']:.2f} % (théorie {100*(1-comb(43,2)/comb(47,2)):.2f} %)")

# ============ 5. ranges exportées du modèle préflop
print("5) ranges issues du modèle préflop")
check(list(np.bincount(pc.CLASS_OF)) == [6 if n[1] == n[0] else (4 if n.endswith('s') else 12) for n in pc.CLASS_NAMES], "169 classes : 6 combinaisons par paire, 4 par main assortie, 12 par main dépareillée")
data = json.load(open('ranges_export.json')); ok = True; mass_ok = True
for L in data['lines']:
    for p in L['players']:
        f = np.array(p['class_freq']); ok &= bool(f.shape == (169,) and np.all(f >= 0) and np.all(f <= 1 + 1e-9))
        w = pc.range_from_class_freq(f); mass_ok &= abs(w.sum() - float((f * np.bincount(pc.CLASS_OF)).sum())) < 1e-9
check(ok, f"{len(data['lines'])} lignes : fréquences de classe dans [0, 1]")
check(mass_ok, "masse de chaque range = somme des fréquences de classe pondérées par leur nombre de combinaisons")


# ============ 7. métriques pédagogiques
print("7) métriques pédagogiques")
data = json.load(open('ranges_export.json'))
L = [x for x in data['lines'] if x['table'] == 'heads-up' and x['stack_bb'] == 12 and 'limp' in x['description_fr']][0]
RA = pc.range_from_class_freq(L['players'][0]['class_freq']); RB = pc.range_from_class_freq(L['players'][1]['class_freq'])
board = ['9s', '8s', '7d']
eq0, rows = pc.turn_shift(board, RA, RB)
mean = sum(r['equity'] * r['weight'] for r in rows) / sum(r['weight'] for r in rows)
check(abs(mean - eq0) < 1e-9, f"cohérence entre rues : moyenne pondérée des équités de turn = équité du flop ({mean:.9f} contre {eq0:.9f})")
pa = pc.pedagogical_profile(board, RA, RB, with_turns=False); pb = pc.pedagogical_profile(board, RB, RA, with_turns=False)
check(abs(pa['strong_gap_pts'] + pb['strong_gap_pts']) < 1e-9 and abs(pa['nut_gap_pts'] + pb['nut_gap_pts']) < 1e-9, "antisymétrie : écarts de mains fortes et de nuts changent de signe quand on échange les ranges")
check(abs(pa['equity_A'] + pb['equity_A'] - 1) < 1e-10, "antisymétrie de l'équité")
perm = {'s': 'h', 'd': 'c', 'h': 'd', 'c': 's'}                           # permutation des couleurs : les ranges par classe y sont insensibles
board2 = [c[0] + perm[c[1]] for c in board]
pp = pc.pedagogical_profile(board2, RA, RB, with_turns=False)
inv = all(abs(pa[k] - pp[k]) < 1e-9 for k in ('equity_A', 'strong_A', 'strong_B', 'nut_A', 'nut_B', 'ahead_now_A', 'improve_turn_A', 'draw_share_A', 'draw_share_B'))
check(inv, f"invariance par permutation des couleurs ({' '.join(board)} contre {' '.join(board2)}) : toutes les métriques identiques à 1e-9")
sa, sb = pc.nut_shares(board, RA, RB, 0.10)
check(0.10 - 1e-9 <= 0.5 * (sa + sb) <= 0.35, f"nuts : le top 10 % de l'ensemble contient {100*0.5*(sa+sb):.1f} % de l'ensemble (égalités comprises)")
cf = pc.canonical_flops()
check(len(cf) == 1755 and sum(n for _, n in cf) == 22100, f"flops équivalents par les couleurs : {len(cf)} classes, {sum(n for _, n in cf)} flops")
check(pc.flop_texture(['As', '7d', '2c']) == pc.flop_texture(['As', '7d', '2c']) and pc.flop_texture(['As', '7d', '2c'])['label'] == 'A-haut, déconnecté, arc-en-ciel', "texture déterministe")
fake = [dict(concepts=['RANGE_ADVANTAGE_A'], range_adv_pts=x) for x in (6, 9, 7)] + [dict(concepts=[], range_adv_pts=20)]
check([p['range_adv_pts'] for p in pc.select_flops(fake, 'RANGE_ADVANTAGE_A', 2)] == [9, 7], "sélection : classement par intensité, flops sans le concept exclus")
print("   profil (heads-up 12 BB, SB limp / BB check, 9s 8s 7d) :", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in pa.items() if k in ('equity_A', 'range_adv_pts', 'strong_gap_pts', 'nut_gap_pts', 'concepts')})

# ============ 6. performance
print("6) performances (équité exacte, un flop, ranges de taille croissante)")
for n in (1, 50, 200, 600, 1200):
    a = rand_range(n, rng); b = rand_range(n, rng); t = time.time(); pc.range_equity(['As', '7d', '2c'], a, b); print(f"   {n:5d} combinaisons par range : {time.time()-t:5.2f} s")

print("\nÉCHECS :", len(FAILS))
for f in FAILS: print("  -", f)
sys.exit(1 if FAILS else 0)
