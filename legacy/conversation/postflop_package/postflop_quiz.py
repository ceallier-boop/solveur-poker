"""Générateur de questions postflop (conditionnelles aux ranges HRC). Chaque question porte la définition de sa métrique,
la réponse est recalculable depuis postflop_core (voir verify_postflop_quiz.py)."""
import json, random, hashlib, itertools
import postflop_core as pc

NOTE = "Analyse conditionnelle aux ranges HRC préflop fournies ; ce n'est pas une recommandation GTO postflop."
DEF = {
    'RANGE_ADVANTAGE': "Avantage de range = équité exacte de la range sur le flop (toutes les turns et rivers possibles, cartes bloquées, égalités comptées pour moitié) moins 50 %. Ce n'est pas une probabilité de gagner à l'abattage avec la main actuelle.",
    'STRONG_HANDS': "Mains fortes = part de la range qui a au moins top pair (overpair, top pair, deux paires, brelan, quinte, couleur, full ou mieux) sur ce flop.",
    'NUT_ADVANTAGE': "Avantage de nuts = part de la range parmi les 10 % meilleures combinaisons de l'ensemble des deux ranges réunies, sur le flop actuel.",
    'TURN_SHIFT': "Variation à la turn = équité exacte de la range A après la carte de turn moins son équité sur le flop, en points de pourcentage.",
    'HAND_EQUITY': "Équité d'une main = part du pot théorique (victoires + moitié des égalités) contre la range adverse, toutes les cartes à venir énumérées.",
    'IMPROVEMENT': "Amélioration = probabilité moyenne d'une main de la range de monter d'au moins une catégorie (par exemple paire vers brelan) à la turn. Ce n'est pas une probabilité de gagner.",
    'OUTS': "Probabilité de compléter = probabilité d'obtenir la couleur ou la quinte au plus tard à la river, énumération exacte des deux cartes à venir.",
}
MARGIN = 0.5      # une question dont la mesure est à moins de 0,5 point d'un seuil est écartée (réponse ambiguë)
THR = dict(range_adv=5.0, parity=2.0, strong_gap=6.0, nut_gap=8.0, turn=4.0, improve_gap=3.0, hand_gap=6.0)


def _h(d):
    return hashlib.sha1(json.dumps(d, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


def _role(line, who):
    return f"{who} ({line['players'][0 if who == 'A' else 1]['role']})"


def _make(qtype, line, board, prompt, options, correct, explanation, metrics, tag):
    """options : liste de textes ; correct : texte de la bonne option ; mélange déterministe"""
    assert correct in options and len(set(options)) == len(options)
    rnd = random.Random(_h([qtype, board, line['line_id'], tag]))
    opts = options[:]; rnd.shuffle(opts)
    ids = 'ABCD'[:len(opts)]
    q = dict(type=qtype, line_id=line['line_id'], line=line['description_fr'], board=board, prompt_fr=prompt,
             options=[dict(id=i, text=t) for i, t in zip(ids, opts)], correct_option_id=ids[opts.index(correct)],
             explanation_fr=explanation, definition_fr=DEF[qtype], note_fr=NOTE, metrics=metrics)
    q['content_hash'] = _h([qtype, board, line['line_id'], prompt, sorted(options)])
    q['id'] = f"PF-{qtype}-{q['content_hash']}"
    return q


def _fb(b): return ' '.join(b)


def from_profile(p, line):
    out = []; b = p['board']; ra = _role(line, 'A'); rb = _role(line, 'B')
    th = THR; a = p['range_adv_pts']
    # 1) avantage de range
    if abs(a) >= th['range_adv'] + MARGIN or abs(a) <= th['parity'] - MARGIN:
        if a > 0 and abs(a) >= th['range_adv']: c = f"{ra} a l'avantage de range"
        elif a < 0 and abs(a) >= th['range_adv']: c = f"{rb} a l'avantage de range"
        else: c = "Parité : aucune range n'a d'avantage net"
        opts = [f"{ra} a l'avantage de range", f"{rb} a l'avantage de range", "Parité : aucune range n'a d'avantage net"]
        out.append(_make('RANGE_ADVANTAGE', line, b, f"{line['description_fr']}. Flop {_fb(b)}. Quelle range a l'avantage d'équité ?", opts, c,
                         f"Équité de A : {100*p['equity_A']:.1f} % soit {a:+.1f} points par rapport à 50 %. Seuil : {th['range_adv']:.0f} points, parité à {th['parity']:.0f} points.",
                         dict(equity_A=p['equity_A'], range_adv_pts=a), 'ra'))
    # 2) mains fortes
    g = p['strong_gap_pts']
    if abs(g) >= th['strong_gap'] + MARGIN and max(p['strong_A'], p['strong_B']) < 0.9:
        c = f"{ra} a plus de mains fortes" if g > 0 else f"{rb} a plus de mains fortes"
        out.append(_make('STRONG_HANDS', line, b, f"{line['description_fr']}. Flop {_fb(b)}. Quelle range a la plus grande part de mains « top pair ou mieux » ?",
                         [f"{ra} a plus de mains fortes", f"{rb} a plus de mains fortes", "Les deux parts sont équivalentes"], c,
                         f"Part de A : {100*p['strong_A']:.1f} %, part de B : {100*p['strong_B']:.1f} % (écart {g:+.1f} points ; seuil {th['strong_gap']:.0f}).",
                         dict(strong_A=p['strong_A'], strong_B=p['strong_B'], strong_gap_pts=g), 'sh'))
    # 3) nuts
    n = p['nut_gap_pts']
    if abs(n) >= th['nut_gap'] + MARGIN and p['nut_A'] + p['nut_B'] > 0.05:
        c = f"{ra} a l'avantage de nuts" if n > 0 else f"{rb} a l'avantage de nuts"
        out.append(_make('NUT_ADVANTAGE', line, b, f"{line['description_fr']}. Flop {_fb(b)}. Quelle range détient la plus grande part des 10 % meilleures combinaisons ?",
                         [f"{ra} a l'avantage de nuts", f"{rb} a l'avantage de nuts", "Les deux parts sont équivalentes"], c,
                         f"Part de A : {100*p['nut_A']:.1f} %, part de B : {100*p['nut_B']:.1f} % (écart {n:+.1f} points ; seuil {th['nut_gap']:.0f}).",
                         dict(nut_A=p['nut_A'], nut_B=p['nut_B'], nut_gap_pts=n), 'nu'))
    # 4) amélioration
    d = 100 * (p['improve_turn_A'] - p['improve_turn_B'])
    if abs(d) >= th['improve_gap']:
        c = f"{ra} s'améliore plus souvent" if d > 0 else f"{rb} s'améliore plus souvent"
        out.append(_make('IMPROVEMENT', line, b, f"{line['description_fr']}. Flop {_fb(b)}. Quelle range monte le plus souvent d'au moins une catégorie de main à la turn ?",
                         [f"{ra} s'améliore plus souvent", f"{rb} s'améliore plus souvent", "Les deux s'améliorent autant"], c,
                         f"Amélioration à la turn : A {100*p['improve_turn_A']:.1f} %, B {100*p['improve_turn_B']:.1f} % (écart {d:+.1f} points ; seuil {th['improve_gap']:.0f}). Ce n'est pas une probabilité de gagner.",
                         dict(improve_turn_A=p['improve_turn_A'], improve_turn_B=p['improve_turn_B']), 'im'))
    # 5) variation à la turn
    for t in p.get('turn_instructive', [])[:2]:
        dl = t['delta_pts']
        if abs(dl) < th['turn'] + MARGIN: continue
        c = "L'équité de A augmente nettement" if dl > 0 else "L'équité de A diminue nettement"
        out.append(_make('TURN_SHIFT', line, b, f"{line['description_fr']}. Flop {_fb(b)}, turn {t['turn']}. Comment évolue l'équité de A ?",
                         ["L'équité de A augmente nettement", "L'équité de A diminue nettement", "L'équité de A change peu"], c,
                         f"Variation de l'équité de A à cette turn : {dl:+.1f} points (seuil {th['turn']:.0f}).", dict(turn=t['turn'], delta_pts=dl), 'ts' + t['turn']))
    return out


def outs_questions(line, flops, rng, k=6):
    """probabilité de compléter un tirage couleur ou quinte, recalculée par énumération exacte"""
    out = []; tries = 0
    while len(out) < k and tries < 200:
        tries += 1
        fl = rng.choice(flops); b = [pc.card(x) for x in fl]
        deck = [c for c in range(52) if c not in b]
        h = rng.sample(deck, 2)
        d = pc.draws_of_combo(fl, pc.card_str(h[0]), pc.card_str(h[1]))
        if d['tirage_couleur']: kind, p, label = 'couleur', d['p_couleur_river'], "tirage couleur"
        elif d['outs_quinte'] >= 4: kind, p, label = 'quinte', d['p_quinte_ou_mieux_river'], "tirage de quinte"
        else: continue
        if kind == 'couleur' and d['outs_quinte'] >= 4: continue          # cas mixtes exclus (deux tirages)
        correct = f"{100*p:.0f} %"
        pool = sorted({f"{100*p+s:.0f} %" for s in (-15, -9, -5, 5, 9, 15) if 3 < 100 * p + s < 95} - {correct})
        if len(pool) < 3: continue
        opts = [correct] + rng.sample(pool, 3)
        hs = pc.card_str(h[0]) + pc.card_str(h[1])
        out.append(_make('OUTS', line, [pc.card_str(c) for c in b], f"Vous avez {hs} sur le flop {_fb([pc.card_str(c) for c in b])} ({label}). Quelle est la probabilité de compléter au plus tard à la river ?",
                         opts, correct, f"Énumération exacte des 2 cartes à venir : {100*p:.1f} % (outs de quinte à la turn : {d['outs_quinte']}).",
                         dict(hand=hs, kind=kind, p_complete_river=p, outs_quinte=d['outs_quinte']), hs))
    return out


def hand_equity_questions(line, wa, wb, flops, rng, k=4):
    out = []; tries = 0
    while len(out) < k and tries < 60:
        tries += 1
        fl = rng.choice(flops); b = [pc.card(x) for x in fl]
        deck = [c for c in range(52) if c not in b]
        hands = []
        while len(hands) < 3:
            h = tuple(sorted(rng.sample(deck, 2)))
            if h not in hands and not set(h) & {x for g in hands for x in g}: hands.append(h)
        eq = []
        for h in hands:
            try: eq.append(pc.hand_vs_range((pc.card_str(h[0]), pc.card_str(h[1])), fl, wb))
            except ValueError: eq = None; break
        if eq is None: continue
        order = sorted(range(3), key=lambda i: -eq[i])
        if 100 * (eq[order[0]] - eq[order[1]]) < THR['hand_gap'] + MARGIN: continue
        names = [pc.card_str(h[0]) + pc.card_str(h[1]) for h in hands]
        out.append(_make('HAND_EQUITY', line, [pc.card_str(c) for c in b], f"{line['description_fr']}. Flop {_fb([pc.card_str(c) for c in b])}. Contre la range de B, laquelle de ces mains de A a la meilleure équité ?",
                         names, names[order[0]], "Équités exactes : " + ", ".join(f"{n} {100*e:.1f} %" for n, e in zip(names, eq)) + f" (écart minimal exigé : {THR['hand_gap']:.0f} points).",
                         dict(hands=names, equities=eq), '|'.join(sorted(names))))
    return out


def build_bank(seed=7, with_hands=True, hand_flops=20):
    rng = random.Random(seed)
    data = json.load(open('ranges_export.json')); L = {x['line_id']: x for x in data['lines']}
    profiles = json.load(open('library_profiles.json')); bank = []
    for p in profiles:
        bank += from_profile(p, L[p['line_id']])
    if with_hands:
        cf = pc.canonical_flops(); flops = [f for f, n in rng.sample(cf, hand_flops)]
        for lid in sorted({p['line_id'] for p in profiles}):
            ln = L[lid]; wa = pc.range_from_class_freq(ln['players'][0]['class_freq']); wb = pc.range_from_class_freq(ln['players'][1]['class_freq'])
            bank += outs_questions(ln, flops, rng) + hand_equity_questions(ln, wa, wb, flops, rng)
    seen = {}; res = []
    for q in bank:
        if q['content_hash'] not in seen: seen[q['content_hash']] = 1; res.append(q)
    return res


if __name__ == '__main__':
    bank = build_bank()
    json.dump(bank, open('postflop_quiz_bank.json', 'w'), ensure_ascii=False, indent=1)
    import collections
    print(len(bank), collections.Counter(q['type'] for q in bank))
