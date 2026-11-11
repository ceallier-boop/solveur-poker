"""Bibliothèque d'équités (CE2, 10/11/2026) : chances de toucher au flop, équité contre une range de la banque, forces et faiblesses d'une main.

Tout est précalculé dans une table fixe (spinsacademy/data/equites.json, lisible sans numpy ni numba, par le serveur comme par le navigateur) :
  - chances de toucher au flop, par classe de main (169), énumération de tous les flops (postflop/flop_hits.py) : catégories exclusives
    (la meilleure main touchée, « rien » comprise, somme exacte 100 %), cumulées (« au moins une paire »…) et tirages ;
  - équité de chaque main contre une main au hasard et contre quelques ranges de la banque du solveur (tapis du SB, call du BB à 6, 8, 10 et 12 BB,
    tapis du BTN à 3 joueurs à 8 et 12 BB), à partir des équités exactes préflop du dépôt (data/equity_169.npy) ; l'égalité compte pour une moitié ;
  - étiquettes de forces et de faiblesses, produites par règles ; chaque règle porte son seuil chiffré, chaque main porte la valeur mesurée.
Les valeurs sont des entiers en dix-millièmes (10 000 = 100 %), sauf indication contraire. L'API ci-dessous ne lit que cette table.
Reconstruire : python -m spinsacademy.equities --build   (environ 10 secondes)
"""
import json, os, sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'equites.json')
BANK = 'gto_preflop/2026.11.07-s2'
VERSION = 1
DATE = '2026-11-10'
RANKS = '23456789TJQKA'

HITS_FR = {'rien': "ne touche pas le flop (carte haute, ou paire déjà sur le tableau)", 'paire_poche_sous_tableau': "paire de poche sous le tableau",
           'paire_basse': "paire avec la plus basse carte du tableau", 'paire_intermediaire': "paire intermédiaire", 'top_paire': "top paire",
           'paire_poche_sur_tableau': "paire de poche au-dessus du tableau", 'double_paire': "double paire", 'set': "brelan avec une paire de poche (set)",
           'brelan': "brelan avec une carte de la main et une paire du tableau", 'suite': "suite", 'couleur': "couleur", 'full': "full", 'carre': "carré",
           'quinte_flush': "quinte flush"}
HITS = list(HITS_FR)
CUMUL = {'au_moins_paire': ('toucher au moins une paire', HITS[1:]),
         'au_moins_top_paire': ('toucher au moins la top paire', ['top_paire', 'paire_poche_sur_tableau'] + HITS[6:]),
         'au_moins_double_paire': ('toucher au moins une double paire', HITS[6:]),
         'au_moins_brelan': ('toucher au moins un brelan', HITS[7:]),
         'au_moins_suite': ('toucher au moins une suite', HITS[9:]),
         'au_moins_couleur': ('toucher au moins une couleur', HITS[10:]),
         'au_moins_full': ('toucher au moins un full', HITS[11:])}
DRAWS_FR = {'tirage_couleur': "tirage couleur (quatre cartes de la même couleur, dont une de la main)",
            'tirage_quinte_8': "tirage quinte à 8 outs ou plus (ouvert ou double ventral)", 'tirage_quinte_4': "tirage quinte à 4 outs (ventral ou aux extrémités)",
            'tirage_couleur_et_quinte': "tirage couleur et tirage quinte en même temps"}
DRAWS = list(DRAWS_FR)
KEYS = HITS + list(CUMUL) + DRAWS
MESURES = ['domination', 'part_paire_faible']        # mesures des règles qui ne sont pas déjà dans `flop` ; pour toutes les mains, appliquées ou non

# Règles des étiquettes. `test` reçoit les mesures de la main (voir measures) et renvoie la valeur mesurée si l'étiquette s'applique, sinon None.
# Les seuils sont des nombres ronds posés d'après la distribution des 169 mains (quartiles de la table).
LABELS = [
    dict(id='assortie', groupe='force', fr="assortie : peut faire une couleur et des tirages couleur", regle_fr="deux cartes de la même couleur", seuil=2, sens=None,
         test=lambda m: m['tirage_couleur'] if m['suited'] else None, unite='dix-millièmes de tirage couleur au flop'),
    dict(id='connectee', groupe='force', fr="connectée : fait des suites et des tirages quinte", regle_fr="deux rangs qui se suivent (écart 0) et un tirage quinte à 8 outs au moins 3 % du temps (pas une main de bord comme AK)", seuil=300, sens='>=',
         test=lambda m: m['tirage_quinte_8'] if (m['gap'] == 0 and m['tirage_quinte_8'] >= 300) else None, unite='dix-millièmes de tirage quinte à 8 outs au flop'),
    dict(id='paire_de_poche', groupe='force', fr="paire de poche : un brelan au flop une fois sur neuf", regle_fr="deux cartes du même rang", seuil=2, sens=None,
         test=lambda m: m['set'] if m['pair'] else None, unite='dix-millièmes de set au flop'),
    dict(id='cartes_hautes', groupe='force', fr="deux cartes hautes (dix ou plus)", regle_fr="les deux rangs sont T, J, Q, K ou A (rang d'au moins 8, avec 0 = 2)", seuil=8, sens='>=',
         test=lambda m: m['hi'] if (not m['pair'] and m['lo'] >= 8) else None, unite='rang de la plus haute carte (0 = 2, 12 = A)'),
    dict(id='top_paire_souvent', groupe='force', fr="fait souvent la top paire ou mieux", regle_fr="sans paire de poche : top paire ou mieux au flop au moins 25 % du temps", seuil=2500, sens='>=',
         test=lambda m: m['au_moins_top_paire'] if (not m['pair'] and m['au_moins_top_paire'] >= 2500) else None, unite='dix-millièmes'),
    dict(id='beaucoup_de_tirages', groupe='force', fr="beaucoup de tirages au flop", regle_fr="tirage couleur au moins 10 % du temps, ou tirage quinte à 8 outs au moins 9 %",
         seuil=[1000, 900], sens='>=', test=lambda m: max(m['tirage_couleur'], m['tirage_quinte_8']) if (m['tirage_couleur'] >= 1000 or m['tirage_quinte_8'] >= 900) else None,
         unite='dix-millièmes (le plus grand des deux tirages)'),
    dict(id='bloque_les_as', groupe='force', fr="bloque les As : l'adversaire en a moins", regle_fr="contient un As", seuil=1, sens=None,
         test=lambda m: 1 if m['has_ace'] else None, unite=''),
    dict(id='forte_contre_au_hasard', groupe='force', fr="forte contre une main au hasard", regle_fr="équité d'au moins 60 % contre une main au hasard", seuil=6000, sens='>=',
         test=lambda m: m['equity_random'] if m['equity_random'] >= 6000 else None, unite='dix-millièmes'),
    dict(id='depareillee', groupe='faiblesse', fr="dépareillée : peu de couleurs, peu de tirages couleur", regle_fr="deux couleurs différentes (ni paire ni assortie)", seuil=2, sens=None,
         test=lambda m: m['tirage_couleur'] if (not m['pair'] and not m['suited']) else None, unite='dix-millièmes de tirage couleur au flop'),
    dict(id='cartes_eloignees', groupe='faiblesse', fr="cartes éloignées : presque pas de tirage quinte ouvert", regle_fr="au moins deux rangs entre les deux cartes (écart d'au moins 2), sans paire, et un tirage quinte à 8 outs moins de 2 % du temps", seuil=200, sens='<',
         test=lambda m: m['tirage_quinte_8'] if (not m['pair'] and m['gap'] >= 2 and m['tirage_quinte_8'] < 200) else None, unite='dix-millièmes de tirage quinte à 8 outs'),
    dict(id='dominee', groupe='faiblesse', fr="dominée : souvent battue par les mains fortes qui partagent une carte", regle_fr="au moins 30 % des 20 % meilleures mains (équité contre une main au hasard) la dominent : "
         "même carte haute avec un meilleur second rang, ou même second rang avec une meilleure carte haute", seuil=3000, sens='>=',
         test=lambda m: m['domination'] if m['domination'] >= 3000 else None, unite='dix-millièmes des combinaisons fortes qui la dominent'),
    dict(id='top_paire_rarement', groupe='faiblesse', fr="fait rarement la top paire", regle_fr="sans paire de poche : top paire ou mieux au flop moins de 12 % du temps", seuil=1200, sens='<',
         test=lambda m: m['au_moins_top_paire'] if (not m['pair'] and m['au_moins_top_paire'] < 1200) else None, unite='dix-millièmes'),
    dict(id='paire_faible', groupe='faiblesse', fr="quand elle touche, c'est souvent une paire faible", regle_fr="sans paire de poche : au moins 60 % des fois où elle touche, c'est une paire basse ou intermédiaire", seuil=6000, sens='>=',
         test=lambda m: m['part_paire_faible'] if (not m['pair'] and m['au_moins_paire'] > 0 and m['part_paire_faible'] >= 6000) else None, unite='dix-millièmes des flops touchés'),
    dict(id='faible_contre_au_hasard', groupe='faiblesse', fr="faible contre une main au hasard", regle_fr="équité de moins de 45 % contre une main au hasard", seuil=4500, sens='<',
         test=lambda m: m['equity_random'] if m['equity_random'] < 4500 else None, unite='dix-millièmes'),
]

# ranges de la banque (tapis et call, heads-up de 6 à 12 BB, BTN à 3 joueurs) : (id, texte, table, tapis, hero, nœud, action)
RANGES = [(f'hu{n}_sb_tapis', f"Heads-up {n} BB : le SB part à tapis", 'heads-up', n, 'SB', 'root', 'allin') for n in (6, 8, 10, 12)] \
       + [(f'hu{n}_bb_paie', f"Heads-up {n} BB : le BB paie le tapis du SB", 'heads-up', n, 'BB', 'SB-allin', 'call') for n in (6, 8, 10, 12)] \
       + [(f'3j{n}_btn_tapis', f"3 joueurs {n} BB : le BTN part à tapis", '3-handed', n, 'BTN', 'root', 'allin') for n in (8, 12)]


def _parse(h):
    return RANKS.index(h[0]), RANKS.index(h[1]), h[2] if len(h) == 3 else ''


def _bp(counts, n):
    """comptes -> dix-millièmes entiers dont la somme fait exactement 10 000 (plus grands restes)"""
    exact = [10000 * c / n for c in counts]; base = [int(x) for x in exact]
    left = 10000 - sum(base)
    for i in sorted(range(len(exact)), key=lambda i: (-(exact[i] - base[i]), i))[:left]: base[i] += 1
    return base


def measures(i, name, hit_bp, draw_bp, eq_random, domination):
    a, b, s = _parse(name); h = dict(zip(HITS, hit_bp)); d = dict(zip(DRAWS, draw_bp))
    m = dict(suited=s == 's', pair=a == b, hi=a, lo=b, gap=a - b - 1 if a != b else None, has_ace=12 in (a, b), equity_random=eq_random, domination=domination, **d)
    for k, (_, parts) in CUMUL.items(): m[k] = sum(h[p] for p in parts)
    m['set'] = h['set']
    weak = h['paire_basse'] + h['paire_intermediaire']                  # paires de poche exclues : la mesure ne vaut que pour les mains sans paire
    m['part_paire_faible'] = round(10000 * weak / m['au_moins_paire']) if m['au_moins_paire'] else 0
    return m


def build():
    """(table, JSON) : recalcule tout depuis l'énumération des flops, les équités exactes et la banque du solveur"""
    import numpy as np
    from . import allin, quiz
    from .cards import NAMES, W
    from .postflop import flop_hits
    hits, draws, n = flop_hits.counts()
    eq_random = [round(10000 * float(x)) for x in allin.equity_vs_range(np.ones(169))]
    eqs = np.array(allin.equity_vs_range(np.ones(169)))
    order = np.argsort(-eqs, kind='stable'); strong = []; tot = 0
    for i in order:                                          # les 20 % meilleures combinaisons de départ (équité contre une main au hasard)
        strong.append(int(i)); tot += int(W[i])
        if tot >= 0.2 * 1326: break
    dom = []
    for i, name in enumerate(NAMES):
        a, b, _ = _parse(name); num = 0
        if a != b:
            for j in strong:
                c, d, _ = _parse(NAMES[j])
                if c == d: continue
                if (c == a and d > b and d != a) or (d == a and c > b and c != a) or (d == b and c > a) or (c == b and d > a): num += int(W[j])
        dom.append(round(10000 * num / sum(int(W[j]) for j in strong)))
    flop = []; labels = []; mesures = []; lab_defs = [{k: v for k, v in L.items() if k != 'test'} for L in LABELS]
    for i, name in enumerate(NAMES):
        hit_bp = _bp(list(hits[i]), int(n[i])); draw_bp = [round(10000 * int(x) / int(n[i])) for x in draws[i]]
        m = measures(i, name, hit_bp, draw_bp, eq_random[i], dom[i])
        flop.append(hit_bp + [m[k] for k in CUMUL] + draw_bp)
        labels.append([[L['id'], v] for L in LABELS for v in [L['test'](m)] if v is not None])
        mesures.append([m[k] for k in MESURES])
    _, spots = quiz.load(BANK); ranges = []
    for rid, label, table, stack, hero, node, act in RANGES:
        sp = next(s for s in spots.values() if s['table'] == table and s['stacks_bb'] == [float(stack)] * len(s['stacks_bb']) and s['hero'] == hero and s['node_key'] == node)
        ids = [a['id'] for a in sp['actions']]; types = [a['type'] for a in sp['actions']]
        j = types.index('allin') if act == 'allin' else types.index('call_allin') if 'call_allin' in types else types.index('call')
        q = np.array([sp['hands'][h]['reach'] * sp['hands'][h]['freq'][j] for h in NAMES])
        eq = allin.equity_vs_range(q)
        ranges.append(dict(id=rid, label_fr=label, spot=sp['spot_id'], hero=hero, share=round(10000 * float((W * q).sum() / W.sum())),
                           equity=[None if np.isnan(x) else round(10000 * float(x)) for x in eq]))
    return dict(version=VERSION, date=DATE, bank=BANK, unite="dix-millièmes (10 000 = 100 %) ; égalité = une moitié", hands=list(NAMES), keys=KEYS, hits=HITS, cumul=list(CUMUL),
                draws=DRAWS, flop=flop, equity_random=eq_random, ranges=ranges, labels_def=lab_defs, labels=labels, mesures_keys=MESURES, mesures=mesures)


def _dump(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))


_TABLE = None


def table():
    global _TABLE
    if _TABLE is None:
        with open(PATH, encoding='utf-8') as f: _TABLE = json.load(f)
    return _TABLE


def _i(hand): return table()['hands'].index(hand)


def hit_chances(hand):
    """{clé : dix-millièmes} : catégories exclusives (somme 10 000), cumulées et tirages ; clés dans HITS, CUMUL, DRAWS"""
    return dict(zip(table()['keys'], table()['flop'][_i(hand)]))


def equity_random(hand):
    return table()['equity_random'][_i(hand)]


def ranges():
    return [{k: v for k, v in r.items() if k != 'equity'} for r in table()['ranges']]


def equity_vs_range(hand, range_id):
    """équité (dix-millièmes) de la classe contre la range ; None si la range est vide une fois la main retirée du paquet"""
    r = next(r for r in table()['ranges'] if r['id'] == range_id)
    return r['equity'][_i(hand)]


def measures_of(hand):
    """toutes les mesures utilisées par les règles d'étiquettes, pour n'importe quelle main : les chances de toucher, les tirages, l'équité contre une main au hasard
    et `domination`, `part_paire_faible` (dix-millièmes) ; `part_paire_faible` ne vaut que pour les mains sans paire de poche"""
    out = dict(hit_chances(hand)); out['equity_random'] = equity_random(hand)
    out.update(zip(table()['mesures_keys'], table()['mesures'][_i(hand)]))
    return out


def labels(hand):
    """[{id, groupe, fr, regle_fr, seuil, valeur, unite}] : forces et faiblesses, avec la règle, le seuil et la valeur mesurée"""
    defs = {d['id']: d for d in table()['labels_def']}
    return [dict(defs[k], valeur=v) for k, v in table()['labels'][_i(hand)]]


if __name__ == '__main__':
    if '--build' in sys.argv:
        text = _dump(build())
        with open(PATH, 'w', encoding='utf-8') as f: f.write(text)
        print(f'{PATH} : {len(text.encode("utf-8")) / 1024:.0f} Ko')
    else:
        print(__doc__)
