"""Tests AMO 2 (cohérence pédagogique) et 3 (robustesse de génération) du générateur postflop.
Recalcule chaque question depuis postflop_core, indépendamment des profils stockés."""
import json, sys, time, random, collections, re
import postflop_core as pc
import postflop_quiz as pq

fails = []
_TS = {}
def check(c, msg):
    if not c: fails.append(msg)

def ranges():
    d = json.load(open('ranges_export.json')); R = {}
    for l in d['lines']:
        R[l['line_id']] = (pc.range_from_class_freq(l['players'][0]['class_freq']), pc.range_from_class_freq(l['players'][1]['class_freq']))
    return R

def txt(q, i): return next(o['text'] for o in q['options'] if o['id'] == i)

def recompute(q, R, nmax=None):
    """renvoie la bonne réponse (texte) recalculée depuis le noyau, et la marge par rapport au seuil"""
    wa, wb = R[q['line_id']]; b = q['board']; t = q['type']; T = pq.THR
    ra = pq._role(next(l for l in LINES if l['line_id'] == q['line_id']), 'A'); rb = ra.replace('A (', 'B (')
    rb = pq._role(next(l for l in LINES if l['line_id'] == q['line_id']), 'B')
    if t == 'RANGE_ADVANTAGE':
        a = 100 * (pc.range_equity(b, wa, wb) - 0.5)
        ans = f"{ra} a l'avantage de range" if a >= T['range_adv'] else (f"{rb} a l'avantage de range" if a <= -T['range_adv'] else "Parité : aucune range n'a d'avantage net")
        margin = min(abs(abs(a) - T['range_adv']), abs(abs(a) - T['parity'])) if abs(a) > T['parity'] else T['parity'] - abs(a)
        return ans, margin, a
    if t == 'STRONG_HANDS':
        g = 100 * (pc.strong_share(b, wa) - pc.strong_share(b, wb))
        return (f"{ra} a plus de mains fortes" if g > 0 else f"{rb} a plus de mains fortes"), abs(g) - T['strong_gap'], g
    if t == 'NUT_ADVANTAGE':
        na, nb = pc.nut_shares(b, wa, wb); g = 100 * (na - nb)
        return (f"{ra} a l'avantage de nuts" if g > 0 else f"{rb} a l'avantage de nuts"), abs(g) - T['nut_gap'], g
    if t == 'TURN_SHIFT':
        key=(q['line_id'],tuple(b))
        if key not in _TS: _TS[key] = pc.turn_shift(b, wa, wb)
        eq0, rows = _TS[key]; r = next(x for x in rows if x['turn'] == q['metrics']['turn']); dl = 100 * r['delta']
        return ("L'équité de A augmente nettement" if dl > 0 else "L'équité de A diminue nettement"), abs(dl) - T['turn'], dl
    if t == 'OUTS':
        h = q['metrics']['hand']; d = pc.draws_of_combo(b, h[:2], h[2:])
        p = d['p_couleur_river'] if q['metrics']['kind'] == 'couleur' else d['p_quinte_ou_mieux_river']
        return f"{100*p:.0f} %", 0.0, 100 * p
    if t == 'HAND_EQUITY':
        hs = q['metrics']['hands']; eq = [pc.hand_vs_range((h[:2], h[2:]), b, wb) for h in hs]
        order = sorted(range(3), key=lambda i: -eq[i])
        return hs[order[0]], 100 * (eq[order[0]] - eq[order[1]]) - T['hand_gap'], eq
    raise ValueError(t)

def coherence(bank, R, sample=None, rng=None):
    """test 2 : la réponse dérive de la métrique définie, l'explication cite les mêmes valeurs, la définition correspond au type"""
    qs = bank if sample is None else rng.sample(bank, min(sample, len(bank)))
    worst = 99; n_margin = 0
    for q in qs:
        ans, margin, val = recompute(q, R)
        check(txt(q, q['correct_option_id']) == ans, f"réponse incohérente {q['id']}: {txt(q, q['correct_option_id'])} vs {ans}")
        check(q['definition_fr'] == pq.DEF[q['type']], f"définition manquante/inexacte {q['id']}")
        check(q['note_fr'] == pq.NOTE, f"note de conditionnalité absente {q['id']}")
        check(margin >= -1e-9, f"question hors seuil {q['id']} (marge {margin:.2f})")
        if margin < pq.MARGIN - 1e-9 and q['type'] != 'OUTS': n_margin += 1
        worst = min(worst, margin)
        nums = [float(x.replace(',', '.')) for x in re.findall(r'(\d+[.,]\d)', q['explanation_fr'])]
        if q['type'] == 'RANGE_ADVANTAGE': check(any(abs(abs(val) - abs(x)) < 0.06 for x in nums) or abs(val) < 0.06, f"explication sans la valeur recalculée {q['id']}")
        if q['type'] == 'OUTS': check(any(abs(val - x) < 0.06 for x in nums), f"explication OUTS {q['id']}")
        # vocabulaire : amélioration/équité jamais présentées comme une probabilité de gagner
        if q['type'] in ('IMPROVEMENT', 'RANGE_ADVANTAGE', 'TURN_SHIFT'):
            check('probabilité de gagner' not in q['prompt_fr'].lower(), f"formulation ambiguë {q['id']}")
    return len(qs), worst, n_margin

def structure(bank):
    ids = collections.Counter(q['id'] for q in bank); hs = collections.Counter(q['content_hash'] for q in bank)
    check(all(v == 1 for v in ids.values()), "identifiants dupliqués"); check(all(v == 1 for v in hs.values()), "contenus dupliqués")
    for q in bank:
        o = [x['text'] for x in q['options']]
        check(len(set(o)) == len(o), f"options dupliquées {q['id']}")
        check(sum(1 for x in q['options'] if x['id'] == q['correct_option_id']) == 1, f"bonne réponse non unique {q['id']}")
        check(2 <= len(o) <= 4, f"nombre d'options {q['id']}")
        bd = q['board']; check(len(set(bd)) == len(bd) and len(bd) == 3, f"board invalide {q['id']}")
        if q['type'] == 'OUTS':
            h = q['metrics']['hand']; cs = [h[:2], h[2:]]
            check(len(set(cs + bd)) == 5, f"carte bloquée/dupliquée {q['id']}")
        if q['type'] == 'HAND_EQUITY':
            cs = [c for h in q['metrics']['hands'] for c in (h[:2], h[2:])]
            check(len(set(cs + bd)) == 9, f"mains qui se recoupent ou cartes du board {q['id']}")
        for k in ('definition_fr', 'note_fr', 'explanation_fr', 'prompt_fr'):
            check(bool(q.get(k)), f"champ vide {k} {q['id']}")

def quiz_sets(bank, n_quiz=300, size=10, seed=1):
    """test 3 : tirage de n_quiz quiz de `size` questions ; doublons de board et de type dans un même quiz, répartition"""
    rng = random.Random(seed); dup_boards = 0; dup_q = 0; types = collections.Counter(); seen_global = collections.Counter()
    for _ in range(n_quiz):
        qz = rng.sample(bank, size)
        check(len({q['id'] for q in qz}) == size, "question répétée dans un quiz")
        bc = collections.Counter(tuple(sorted(q['board'])) for q in qz); dup_boards += sum(v - 1 for v in bc.values())
        for q in qz: types[q['type']] += 1; seen_global[q['id']] += 1
    return dup_boards / (n_quiz * size), types, len(seen_global)

if __name__ == '__main__':
    LINES = json.load(open('ranges_export.json'))['lines']; R = ranges()
    t0 = time.time(); allfail = {}
    bank = json.load(open('postflop_quiz_bank.json')) if len(sys.argv) < 2 else pq.build_bank(int(sys.argv[1]))
    structure(bank)
    n, worst, nm = coherence(bank, R)
    print(f"banque principale : {len(bank)} questions, recalcul complet {n}, pire marge {worst:.2f} pt, {nm} questions à moins de 0,5 pt du seuil ({time.time()-t0:.0f} s)")
    # robustesse : 5 graines (génération indépendante des questions OUTS/HAND_EQUITY), >= 1200 questions au total, sans doublon entre graines
    allq = {q['content_hash']: q for q in bank}; stats = []
    for s in (11, 12, 13, 14, 15):
        b = pq.build_bank(s)
        structure(b); coherence(b, R, sample=60, rng=random.Random(s))
        for q in b: allq.setdefault(q['content_hash'], q)
        stats.append(len(b))
    print("banques par graine :", stats, "| questions distinctes au total :", len(allq))
    dupb, types, used = quiz_sets(list(allq.values()))
    print(f"300 quiz de 10 : doublons de board par question = {dupb:.3f} ; types = {dict(types)} ; questions utilisées = {used}")
    print("TEMPS TOTAL", f"{time.time()-t0:.0f} s")
    print("ÉCHECS :", len(fails)); [print(' -', f) for f in fails[:30]]
    sys.exit(1 if fails else 0)
