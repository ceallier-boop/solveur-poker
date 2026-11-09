"""Fiches « à emporter » (N3) : données des charts 13 × 13 tirées d'une banque du solveur, sans recalcul.

Sélection : tapis égaux ; décisions « tapis » de 2 à 16 BB, décisions « flop » de 8 à 16 BB (champ `reliability` de la banque). Par fiche :
actions (mêmes noms que l'application), fréquence de chaque action pour les 169 mains (entiers de 0 à 100), mains jamais atteintes, mains
relues par les experts qui diffèrent de la banque (nombres seulement, aucun nom). Pour les décisions « flop », l'écart mesuré par table et par
tapis (courbe de calage, data/solver/g17/courbe_calage_s2.json).

Usage : python tools/solver/build_fiches.py [--bank gto_preflop/2026.11.07-s2] [--out spinsacademy/data/fiches.json]
Le fichier est déterministe : le régénérer depuis la même banque donne les mêmes octets (tests/test_fiches.py).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import coachs, quiz  # noqa: E402
from spinsacademy.cards import NAMES  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BANK = 'gto_preflop/2026.11.07-s2'
OUT = os.path.join(ROOT, 'spinsacademy', 'data', 'fiches.json')
CURVE = os.path.join(ROOT, 'data', 'solver', 'g17', 'courbe_calage_s2.json')
TAPIS_MIN, FLOP_MIN, MAX_BB = 2, 8, 16
NODES = ('first_in', 'vs_limp', 'vs_raise', 'vs_allin')
POS_ORDER = {'heads-up': ('SB', 'BB'), '3-handed': ('BTN', 'SB', 'BB')}
TABLE_FR = {'heads-up': 'Heads-up', '3-handed': '3 joueurs'}
RELIABILITY_FR = {'tapis': "Fiable : décision à tapis ou face à un tapis, validée sur la référence (8 à 16 BB).",
                  'flop': "Approximation : la décision mène au flop ; voir l'écart mesuré."}


def low(line): return line[0].lower() + line[1:]


def situation(sp):
    """« BB face à une ouverture à 2 BB » : situation du héros en français courant"""
    hero, H, fam = sp['hero'], sp['history'], quiz.family(sp); hu = sp['table'] == 'heads-up'
    lines = quiz.history_text(sp)
    if fam == 'first_in':
        return f'{hero} premier à parler' + (f" ({low(lines[0])})" if H else '')
    opp = lambda h: h['position'] != hero
    if fam == 'vs_limp':
        idx = max(i for i, h in enumerate(H) if h['action'] == 'limp' and opp(h)); who = H[idx]['position']
        key = f'un limp du {who}' if not hu else 'un limp'
    elif fam == 'vs_raise':
        idx = max(i for i, h in enumerate(H) if h['action'] == 'raise' and opp(h)); who = H[idx]['position']
        first = not any(h['action'] in ('raise', 'allin') for h in H[:idx]) and not any(h['action'] == 'limp' for h in H[:idx])
        what = 'une ouverture' if first else 'une relance'
        key = f"{what} à {quiz.bb(H[idx]['to_bb'])} BB" + ('' if hu else f' du {who}')
    else:
        idx = max(i for i, h in enumerate(H) if h['action'] == 'allin' and opp(h)); who = H[idx]['position']
        key = f"le tapis du {who} ({quiz.bb(H[idx]['to_bb'])} BB)" if not hu else f"un tapis de {quiz.bb(H[idx]['to_bb'])} BB"
    s = f'{hero} face à {key}'
    before = [low(l) for l in lines[:idx]]; after = [low(l) for l in lines[idx + 1:]]
    if before: s += ' (avant : ' + ', '.join(before) + ')'
    if after: s += ' (ensuite : ' + ', '.join(after) + ')'
    return s


def title(sp):
    return f"{TABLE_FR[sp['table']]}, {sp['stacks_bb'][0]:g} BB · {situation(sp)}"


def dead_hex(dead):
    """mains jamais atteintes, en 43 chiffres hexadécimaux : le chiffre k couvre les mains 4k à 4k + 3, le bit j (valeur 2^j) la main 4k + j"""
    return ''.join(format(sum(1 << j for j in range(4) if 4 * k + j in dead), 'x') for k in range(43))


def dead_set(code):
    return {4 * k + j for k, c in enumerate(code) for j in range(4) if int(c, 16) >> j & 1}


def approximation(curve, table, stack):
    """écart mesuré des décisions « flop » à cette profondeur ; une profondeur sans mesure (15 BB) prend la mesure voisine la plus défavorable"""
    prefix = 'hu' if table == 'heads-up' else '3w'
    def row(n):
        name = f'hu_{n}-{n}' if prefix == 'hu' else f'3w_{n}-{n}-{n}'
        return next((r for r in curve if r['config'] == name), None)
    cands = [n for n in (stack, stack - 1, stack + 1) if row(n) and row(n)['flop']]
    if stack in cands: cands = [stack]
    best = max(cands, key=lambda n: row(n)['flop']['loss'] - row(n)['flop']['floor'])
    f = row(best)['flop']; ex = max(0.0, f['loss'] - f['floor'])
    note = (f"Approximation : à {best:g} BB, notre solveur perd {f['loss']:g} mBB par main contre {f['floor']:g} pour la référence elle-même "
            f"(écart de {ex:.1f} mBB), et recommande la même action que la référence pour {f['agree']:g} % des mains.")
    if table == 'heads-up' and best >= 16:
        note += " Défaut connu : face à une ouverture à 2 BB, le BB se couche environ 8 points de trop (mains marginales)."
    out = dict(perte_mbb=f['loss'], plancher_mbb=f['floor'], accord_pct=f['agree'], note_fr=note)
    if best != stack: out['mesure_bb'] = best
    return out


def build(bank=BANK, curve_path=CURVE):
    manifest, spots = quiz.load(bank); curve = json.load(open(curve_path))
    sel = [s for s in spots.values() if not s.get('field') and len(set(s['stacks_bb'])) == 1 and 2 <= s['stacks_bb'][0] <= MAX_BB
           and (s['reliability'] == 'tapis' or s['stacks_bb'][0] >= FLOP_MIN)]
    key = lambda s: (0 if s['table'] == 'heads-up' else 1, s['stacks_bb'][0], POS_ORDER[s['table']].index(s['hero']), NODES.index(quiz.family(s)), len(s['history']), s['spot_id'])
    sel.sort(key=key)
    minreach = manifest.get('min_reach_for_questions', 0.05)
    fiches = []
    for order, s in enumerate(sel):
        labels = [quiz.action_label(s, a) for a in s['actions']]; ids = [a['id'] for a in s['actions']]
        H = s['hands']
        f = [[round(100 * H[h]['freq'][j]) for h in NAMES] for j in range(len(ids))]
        dead = [i for i, h in enumerate(NAMES) if H[h]['reach'] < minreach]
        for row in f:
            for i in dead: row[i] = 0                          # main jamais atteinte : fréquence sans sens, mise à 0 (le fichier reste sous 500 Ko)
        experts = []
        for i, h in enumerate(NAMES):
            if i in dead: continue
            a = coachs.lookup(s, h)
            if not a: continue
            top = max(range(len(ids)), key=lambda j: H[h]['freq'][j]); rec = ids.index(a['recommended']) if a.get('recommended') in ids else None
            if rec is not None and rec == top and not a.get('split'): continue
            experts.append(dict(hand=h, experts={labels[ids.index(k)]: n for k, n in sorted(a['votes'].items())},
                                recommended=labels[rec] if rec is not None else None, bank=labels[top], bank_pct=f[top][i],
                                recommended_pct=f[rec][i] if rec is not None else None))
        fiches.append(dict(id=s['spot_id'], order=order, title_fr=title(s), table=s['table'], stack=int(s['stacks_bb'][0]), hero=s['hero'], node=quiz.family(s),
                           reliability=s['reliability'], flop_pot=s['flop_pot'], actions=labels, f=f, dead=dead_hex(dead), expert_hands=experts))
    approx = {}
    for t in ('heads-up', '3-handed'):                          # profondeurs entières (les tapis de la banque sont des nombres entiers de BB)
        stacks = sorted({x['stack'] for x in fiches if x['table'] == t and x['reliability'] == 'flop'})
        if stacks: approx[t] = {f'{n:g}': approximation(curve, t, n) for n in stacks}
    return dict(version=1, bank=bank, generated=manifest['created_at'][:10], hands=list(NAMES), reliability_fr=RELIABILITY_FR,
                dead_fr="dead : 43 chiffres hexadécimaux ; le chiffre k couvre les mains 4k à 4k+3 (ordre de hands), le bit j (valeur 2^j) la main 4k+j ; 1 = main jamais atteinte à ce nœud (fréquences à 0, à griser)", approximation=approx, fiches=fiches)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--bank', default=BANK); ap.add_argument('--out', default=OUT); a = ap.parse_args()
    data = build(a.bank)
    text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    with open(a.out, 'w', encoding='utf-8') as fh: fh.write(text)
    n = len(data['fiches'])
    print(f"{n} fiches, {len(text.encode('utf-8')) / 1024:.0f} Ko : {a.out}")


if __name__ == '__main__':
    main()
