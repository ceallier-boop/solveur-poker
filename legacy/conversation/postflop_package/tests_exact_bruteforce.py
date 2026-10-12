"""Test d'exactitude indépendante : équité de petites ranges contre énumération brute avec ref_eval (meilleure main de 5 cartes parmi 7).
Aucun code du noyau n'est réutilisé, hors la lecture des cartes."""
import itertools, random, numpy as np
import postflop_core as pc, ref_eval as ref

def rc(s): c = pc.card(s); return (c // 4, c % 4)

def brute(board, ha, hb):
    """ha, hb : listes de combos (c1, c2) ; équité de A, enumération complète des cartes à venir, cartes bloquées"""
    bd = [pc.card(x) for x in board]; tot = win = tie = 0.0
    for a in ha:
        for b in hb:
            used = set(bd) | set(a) | set(b)
            if len(used) != len(bd) + 4: continue
            rest = [c for c in range(52) if c not in used]
            for run in itertools.combinations(rest, 5 - len(bd)):
                full = [(c // 4, c % 4) for c in bd + list(run)]
                r = ref.compare([(x // 4, x % 4) for x in a] + full, [(x // 4, x % 4) for x in b] + full)
                tot += 1; win += r > 0; tie += r == 0
    return (win + 0.5 * tie) / tot

def weights(combos):
    w = np.zeros(1326)
    for a in combos:
        w += pc.single_combo(pc.card_str(a[0]), pc.card_str(a[1]))
    return w

rng = random.Random(5); worst = 0.0
for case in range(12):
    n_board = rng.choice([4, 4, 5])                                  # turn ou river : énumération brute rapide
    deck = list(range(52)); rng.shuffle(deck); bd = deck[:n_board]; rest = deck[n_board:]
    ha = [tuple(rest[2 * i:2 * i + 2]) for i in range(2)]
    hb = [tuple(rest[4 + 2 * i:6 + 2 * i]) for i in range(2)]
    if rng.random() < .5: hb.append(tuple(rng.sample(rest, 2)))        # combos partiellement bloqués
    ha = [tuple(sorted(x)) for x in ha]; hb = [tuple(sorted(x)) for x in hb]
    e1 = brute([pc.card_str(c) for c in bd], ha, hb)
    e2 = pc.range_equity([pc.card_str(c) for c in bd], weights(ha), weights(hb))
    worst = max(worst, abs(e1 - e2)); assert abs(e1 - e2) < 1e-10, (case, e1, e2)
print(f"OK : 12 cas, écart maximal {worst:.2e}")
