"""Niveaux du parcours et premier lancement (programme de travail, étape 4, 29/10/2026 ; PROGRAMME_TRAVAIL_2026-10-29.md §2 et §4.1).

Parcours GTO en trois niveaux, puis un niveau exploitant ouvert en continu :
  1. Tapis courts (moins de 10 BB : premier à parler, face à un tapis) ;
  2. Le jeu à 10-16 BB (premier à parler, face à un limp, à une relance, à un tapis) ;
  3. Le jeu à 17-25 BB (premier à parler, face à une relance, face à un limp) ;
  4. Exploiter le field (mode exploitant, toutes profondeurs).
Passage au niveau suivant, mesuré sur les RECENT dernières décisions du niveau (mode GTO) :
  - assez de décisions (DECISIONS) et des BB perdus pour 100 décisions sous la cible (BB_TARGET) ;
  - niveau 1 : en plus, RANGES_L1 ranges du niveau à 85 % ou plus ; niveau 2 : aucun thème du niveau « fragile ».
Le passage se fait tout seul, à la consultation ; le joueur peut aussi choisir son niveau (jamais au-delà de 3 en GTO).
Le niveau de départ vient du premier lancement (expérience déclarée) ; un joueur qui a déjà joué part du niveau 1 et monte
d'après ses résultats.
"""
from . import progress, quiz

LEVELS = {
    1: dict(name='Tapis courts', depth=(0, 9.5), mode='gto', themes=(
        ('Premier à parler, moins de 10 BB', dict(family='first_in', min_stack=0, max_stack=9.5)),
        ('Face à un tapis, moins de 10 BB', dict(family='vs_allin', min_stack=0, max_stack=9.5)))),
    2: dict(name='Le jeu à 10-16 BB', depth=(9.5, 16.5), mode='gto', themes=(
        ('Premier à parler, 10 à 16 BB', dict(family='first_in', min_stack=9.5, max_stack=16.5)),
        ('Face à un limp, 10 à 16 BB', dict(family='vs_limp', min_stack=9.5, max_stack=16.5)),
        ('Face à une relance, 10 à 16 BB', dict(family='vs_raise', min_stack=9.5, max_stack=16.5)),
        ('Face à un tapis, 10 à 16 BB', dict(family='vs_allin', min_stack=9.5, max_stack=16.5)))),
    3: dict(name='Le jeu à 17-25 BB', depth=(16.5, 99), mode='gto', themes=(
        ('Premier à parler, 17 à 25 BB', dict(family='first_in', min_stack=16.5, max_stack=99)),
        ('Face à une relance, 17 à 25 BB', dict(family='vs_raise', min_stack=16.5, max_stack=99)),
        ('Face à un limp, 17 à 25 BB', dict(family='vs_limp', min_stack=16.5, max_stack=99)))),
    4: dict(name='Exploiter le field', depth=(0, 99), mode='exploit', themes=(
        ('Premier à parler contre le field', dict(family='first_in')),
        ('Face à un limp contre le field', dict(family='vs_limp')),
        ('Face à un tapis contre le field', dict(family='vs_allin')),
        ('Lire le vilain', dict(family='read')))),
}
DECISIONS = {1: 100, 2: 150, 3: 150}
BB_TARGET = {1: 15.0, 2: 12.0, 3: 10.0}
RANGES_L1 = 3
RANGE_GOOD = 85
RECENT = 300
START_LEVEL = {'debut': 1, 'confirme': 2, 'gros_volume': 2}
EXPERIENCE_FR = {'debut': 'Moins de 3 mois', 'confirme': 'Plus de 3 mois', 'gros_volume': 'Je joue beaucoup'}
GOAL_FR = {'bases': 'Comprendre les bases', 'recreatifs': 'Gagner plus contre les récréatifs', 'ranges': 'Affûter mes ranges'}


def in_level(level, sp):
    """la situation appartient au niveau (profondeur effective, famille d'un de ses thèmes)"""
    lv = LEVELS[level]; lo, hi = lv['depth']
    return lo <= sp['effective_stack_bb'] < hi and quiz.family(sp) in {f.get('family') for _, f in lv['themes']}


def fits(level, filters):
    """des filtres de thème restent dans le niveau (même tranche de tapis, ou pas de tapis pour le niveau exploitant)"""
    lo, hi = LEVELS[level]['depth']
    a, b = filters.get('min_stack', 0), filters.get('max_stack', 99)
    return (a >= lo and b <= hi) if level < 4 else True


def status(level, rows, range_rows, range_spots):
    """avancement vers le niveau suivant : dict(decisions, needed, bb, target, ranges, ranges_needed, fragile, ready, criteria)"""
    if level not in DECISIONS:
        return dict(level=level, ready=False, criteria=[], final=True)
    mine = [r for r in rows if quiz.mode_of(r['dataset_version']) == 'gto' and in_level(level, quiz.load(r['dataset_version'])[1][r['spot_id']])][-RECENT:]
    st = progress.compute(mine) if mine else {}
    dec, bb = st.get('ev_questions', 0), st.get('bb_per_100')
    crit = [dict(kind='decisions', label_fr=f"{DECISIONS[level]} décisions du niveau", value=dec, target=DECISIONS[level], ok=dec >= DECISIONS[level]),
            dict(kind='bb', label_fr=f"Moins de {BB_TARGET[level]:g} BB perdus pour 100 décisions".replace('.', ','), value=bb, target=BB_TARGET[level],
                 ok=bb is not None and dec >= DECISIONS[level] and bb < BB_TARGET[level])]
    if level == 1:
        good = sum(1 for r in range_rows if r['accuracy_pct'] >= RANGE_GOOD and r['spot_id'] in range_spots)
        crit.append(dict(kind='ranges', label_fr=f"{RANGES_L1} ranges du niveau à {RANGE_GOOD} % ou plus", value=good, target=RANGES_L1, ok=good >= RANGES_L1))
    if level == 2:
        weak = (st.get('focus') or {}).get('kind') == 'weak'
        crit.append(dict(kind='fragile', label_fr='Aucun thème du niveau fragile', value=(st.get('focus') or {}).get('label') if weak else None, target=None, ok=dec > 0 and not weak))
    return dict(level=level, ready=all(c['ok'] for c in crit), criteria=crit, final=False)


def level_spots(version, level):
    """situations de range du niveau (pour compter les ranges réussies du niveau 1)"""
    from . import ranges
    _, spots = quiz.load(version)
    return {s for s in ranges.drawable(version) if in_level(level, spots[s])}


def almost(st):
    """recommandation « niveau presque validé » : il ne manque qu'un critère, et peu de chose"""
    if st.get('final') or st.get('ready'): return None
    miss = [c for c in st['criteria'] if not c['ok']]
    if len(miss) != 1: return None
    c = miss[0]
    if c['kind'] == 'decisions' and c['target'] - c['value'] <= 40:
        return f"Plus que {c['target'] - c['value']} décisions pour passer au niveau {st['level'] + 1}."
    if c['kind'] == 'ranges' and c['target'] - c['value'] == 1:
        return f"Plus qu'une range à {RANGE_GOOD} % pour passer au niveau {st['level'] + 1}."
    if c['kind'] == 'bb' and c['value'] is not None and c['value'] - c['target'] <= 3:
        return f"Encore {str(round(c['value'] - c['target'], 1)).replace('.', ',')} BB pour 100 décisions à gagner pour passer au niveau {st['level'] + 1}."
    return None
