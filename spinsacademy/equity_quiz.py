"""Classe de questions « Équités » (CE3, 10/11/2026) : une main seule, sans tableau.

Trois sortes de questions, toutes tirées de la table fixe spinsacademy/data/equites.json (spinsacademy.equities) :
  - hit    : « Quelle est la chance de toucher … au flop ? » (paire, top paire, double paire, brelan, suite, couleur, tirages) ;
  - equity : « Quelle est l'équité de cette main contre … ? » (une main au hasard, ou une range de tapis ou de call de la banque) ;
  - labels : « Forces et faiblesses » : quatre affirmations générées par les règles de la table, trouver la vraie (ou la fausse).
Réponse par tranches pour hit et equity : 4 tranches au niveau 1, 5 ou 6 aux niveaux 2 et plus ; la valeur exacte n'est jamais à moins
de MARGIN points d'une frontière entre deux tranches (les mains et les sujets sont tirés en conséquence). Notation : bonne tranche
= point plein (« correct »), tranche voisine = demi-point (« imprécision »), sinon « erreur ». Affirmations : un point ou zéro.
Pas de BB perdus : regret_mbb vaut toujours 0 et ces questions sont hors du bilan BB/100 (mode à part, comme la lecture du vilain).

Intégration : un mode « equity » servi par la référence virtuelle REF (pas de dataset publié). Chaque question est un spot virtuel
dont l'identifiant porte tout ce qu'il faut pour la reconstruire (sorte, sujet, niveau, tranches ou affirmations) ; la main est à
part, comme pour les autres questions. Exemples :
  eq:hit:au_moins_paire:L1:w10:n4:p1      chance de toucher au moins une paire, niveau 1, tranches de 10 points, 4 tranches, la bonne est la 2e
  eq:equity:hu8_sb_tapis:L2:w5:n6:p3      équité contre le tapis du SB à 8 BB en heads-up
  eq:labels:vraie:L2:assortie.dominee.cartes_hautes.connectee   trouver la vraie parmi ces quatre affirmations (dans cet ordre)
Réponses : action_id « b0 » à « b5 » (tranche) ou « o0 » à « o3 » (affirmation).
"""
import math, random
from . import equities, equity_board, grading
from .cards import NAMES

REF = f'equites/{equities.DATE}'
KINDS = ('hit', 'equity', 'labels', 'outs', 'board_equity', 'flop_help')
DEFAULT_KINDS = ('hit', 'equity', 'labels')     # série sans filtre ; « outs » (avec tableau, v2) seulement sur demande tant que l'écran n'est pas prêt
BOARD_KINDS = ('outs', 'board_equity', 'flop_help')                         # sortes avec un tableau : spinsacademy.equity_board, main exacte (« 9s8s »)
KIND_FR = {'hit': 'Toucher le flop', 'equity': 'Équité contre une range', 'labels': 'Forces et faiblesses', 'outs': 'Tirages et outs', 'board_equity': 'Équité sur le flop', 'flop_help': 'Ce flop t\'aide-t-il ?'}
CATEGORY_FR = 'Équités'
MARGIN = 1.5                          # points : écart minimal entre la valeur exacte et toute frontière de tranche
MIN_BP = 50                           # valeur minimale d'un sujet (0,5 %) : un « 0 % » ou presque n'apprend rien
N_FLOPS = 19600
SERIES_SIZE = 5

_R = '23456789TJQKA'
_W = {h: (6 if len(h) == 2 else 4 if h[2] == 's' else 12) for h in NAMES}      # combinaisons par classe


def level_of(level):
    """niveau du joueur -> niveau des questions d'équités : 1, ou 2 (niveaux 2 et plus)"""
    return 1 if (level or 1) <= 1 else 2


def is_pair(h): return len(h) == 2


def is_suited(h): return len(h) == 3 and h[2] == 's'


# ------------------------------------------------------------------ sujets « toucher le flop »
# (énoncé niveau 1, énoncé niveaux 2+, phrase de calcul, mains admises, niveau minimal, valeur)
def _v(*keys): return lambda hc: sum(hc[k] for k in keys)


HIT_TOPICS = {
    'au_moins_paire': dict(fr="au moins une paire", what="au moins une paire avec une de tes cartes (une paire déjà sur le tableau ne compte pas)",
                           ok=lambda h: not is_pair(h), level=1, value=_v('au_moins_paire')),
    'au_moins_top_paire': dict(fr="la top paire ou mieux", what="une paire avec la plus haute carte du flop, ou mieux",
                               ok=lambda h: not is_pair(h), level=2, value=_v('au_moins_top_paire')),
    'au_moins_double_paire': dict(fr="une double paire ou mieux", what="au moins une double paire qui utilise tes cartes",
                                  ok=lambda h: not is_pair(h), level=2, value=_v('au_moins_double_paire')),
    'au_moins_brelan': dict(fr="un brelan ou mieux", what="au moins un brelan qui utilise tes cartes", ok=lambda h: True, level=1, value=_v('au_moins_brelan')),
    'suite': dict(fr="une suite", what="une suite (cinq cartes qui se suivent) avec tes cartes", ok=lambda h: not is_pair(h), level=1,
                  value=_v('suite', 'quinte_flush')),
    'couleur': dict(fr="une couleur", what="une couleur (cinq cartes de la même couleur) avec tes deux cartes", ok=is_suited, level=1,
                    value=_v('couleur', 'quinte_flush')),
    'tirage_couleur': dict(fr="un tirage couleur", what="un tirage couleur : quatre cartes de la même couleur, dont au moins une des tiennes",
                           ok=lambda h: True, level=1, value=_v('tirage_couleur')),
    'tirage_quinte_8': dict(fr="un tirage quinte ouvert", what="un tirage quinte ouvert : deux hauteurs de carte complètent ta suite (8 cartes)",
                            ok=lambda h: not is_pair(h), level=2, value=_v('tirage_quinte_8')),
}


def _range_text(rid):
    """« le SB part à tapis en heads-up à 8 BB » d'après l'identifiant de la range (spinsacademy.equities.RANGES)"""
    if rid.startswith('hu') and rid.endswith('_sb_tapis'): return f"le SB part à tapis en heads-up à {rid[2:-9]} BB"
    if rid.startswith('hu') and rid.endswith('_bb_paie'): return f"le BB paie le tapis du SB en heads-up à {rid[2:-8]} BB"
    if rid.startswith('3j') and rid.endswith('_btn_tapis'): return f"le BTN part à tapis à 3 joueurs à {rid[2:-10]} BB"
    return rid


def equity_topics(level):
    """sujets « équité » du niveau : une main au hasard, puis les ranges de la banque (niveau 1 : seulement les tapis du SB)"""
    rids = [r['id'] for r in equities.ranges()]
    if level == 1: rids = [r for r in rids if r.endswith('_sb_tapis')]
    return ['hasard'] + rids


def _range(rid): return next(r for r in equities.ranges() if r['id'] == rid)


def topic_value(kind, topic, hand):
    """valeur exacte du sujet en dix-millièmes, ou None si le sujet ne s'applique pas à cette main"""
    if kind == 'hit':
        t = HIT_TOPICS.get(topic)
        if t is None or not t['ok'](hand): return None
        return t['value'](equities.hit_chances(hand))
    if kind == 'equity':
        if topic == 'hasard': return equities.equity_random(hand)
        return equities.equity_vs_range(hand, topic)
    return None


# ------------------------------------------------------------------ tranches
WIDTHS = {1: (10, 5), 2: (5, 4)}      # largeur des tranches (points), par ordre de préférence


def _int_fr(n): return f"{n:,}".replace(',', '\u202f')


def pct_fr(bp, d=1):
    """dix-millièmes -> « 31,4 % »"""
    s = f"{bp / 100:.{d}f}".rstrip('0').rstrip('.') if d else str(round(bp / 100))
    return s.replace('.', ',') + ' %'


def frontiers(value_bp, w, n, pos):
    """frontières (points) des n tranches de largeur w dont la tranche pos contient la valeur ; None si impossible ou trop près"""
    v = value_bp / 100; m = math.floor(v / w)
    f = [(m - pos + 1 + k) * w for k in range(n - 1)]
    if not f or f[0] <= 0 or f[-1] >= 100: return None
    if any(abs(v - x) < MARGIN - 1e-9 for x in f): return None
    lo = f[pos - 1] if pos > 0 else -math.inf; hi = f[pos] if pos < n - 1 else math.inf
    return f if lo <= v < hi else None


def band_of(value_bp, f):
    v = value_bp / 100
    return sum(1 for x in f if v >= x)


def band_labels(f):
    n = len(f) + 1; out = []
    for i in range(n):
        if i == 0: out.append(f"moins de {f[0]} %")
        elif i == n - 1: out.append(f"{f[-1]} % ou plus")
        else: out.append(f"de {f[i - 1]} à {f[i]} %")
    return out


def feasible(value_bp, level, n):
    """[(w, pos)] possibles pour cette valeur : les largeurs du niveau, la bonne tranche à n'importe quel rang qui garde la marge"""
    return [(w, p) for w in WIDTHS[level] for p in range(n) if frontiers(value_bp, w, n, p)]


# ------------------------------------------------------------------ affirmations (forces et faiblesses)
LABEL_DEFS = None


def label_defs():
    global LABEL_DEFS
    if LABEL_DEFS is None: LABEL_DEFS = {d['id']: d for d in equities.table()['labels_def']}
    return LABEL_DEFS


LEVEL1_LABELS = ('assortie', 'depareillee', 'paire_de_poche', 'cartes_hautes', 'connectee', 'top_paire_souvent', 'top_paire_rarement',
                 'beaucoup_de_tirages', 'forte_contre_au_hasard', 'faible_contre_au_hasard')
OPPOSITES = ({'assortie', 'depareillee'}, {'top_paire_souvent', 'top_paire_rarement'}, {'forte_contre_au_hasard', 'faible_contre_au_hasard'},
             {'connectee', 'cartes_eloignees'})
PAIR_UNCLEAR = ('cartes_hautes', 'depareillee', 'top_paire_souvent', 'top_paire_rarement', 'paire_faible')   # règles pensées pour deux rangs différents


def domination(hand):
    """part (dix-millièmes) des combinaisons fortes qui dominent la main (mesure de la table, toutes mains)"""
    return equities.measures_of(hand)['domination']


def measures(hand):
    mo = equities.measures_of(hand); a, b = _R.index(hand[0]), _R.index(hand[1])
    return dict(pair=a == b, suited=is_suited(hand), hi=a, lo=b, gap=(a - b - 1) if a != b else None, has_ace=12 in (a, b),
                tirage_couleur=mo['tirage_couleur'], tirage_quinte_8=mo['tirage_quinte_8'], au_moins_top_paire=mo['au_moins_top_paire'],
                equity_random=mo['equity_random'], domination=mo['domination'], part_paire_faible=mo['part_paire_faible'])


def _m(s): return max(100, round(0.2 * s))      # marge d'une règle à seuil : 1 point au moins, 20 % du seuil sinon


def clarity(label_id, hand):
    """True : l'affirmation est nettement vraie ; False : nettement fausse ; None : trop près du seuil ou peu claire pour cette main"""
    m = measures(hand)
    if m['pair'] and label_id in PAIR_UNCLEAR: return None

    def thr(v, s, sens):
        if sens == '>=': return True if v >= s + _m(s) else False if v < s - _m(s) else None
        return True if v < s - _m(s) else False if v >= s + _m(s) else None
    if label_id == 'assortie': return m['suited']
    if label_id == 'depareillee': return not m['suited']
    if label_id == 'paire_de_poche': return m['pair']
    if label_id == 'bloque_les_as': return m['has_ace']
    if label_id == 'cartes_hautes': return m['lo'] >= 8
    if label_id == 'connectee':
        if m['pair'] or m['gap'] != 0: return False
        return thr(m['tirage_quinte_8'], 300, '>=')
    if label_id == 'cartes_eloignees':
        if m['pair'] or m['gap'] == 0: return False
        if m['gap'] < 2: return None
        return thr(m['tirage_quinte_8'], 200, '<')
    if label_id == 'top_paire_souvent': return thr(m['au_moins_top_paire'], 2500, '>=')
    if label_id == 'top_paire_rarement': return thr(m['au_moins_top_paire'], 1200, '<')
    if label_id == 'beaucoup_de_tirages':
        tc, tq = m['tirage_couleur'], m['tirage_quinte_8']
        if tc >= 1000 + _m(1000) or tq >= 900 + _m(900): return True
        if tc < 1000 - _m(1000) and tq < 900 - _m(900): return False
        return None
    if label_id == 'forte_contre_au_hasard': return thr(m['equity_random'], 6000, '>=')
    if label_id == 'faible_contre_au_hasard': return thr(m['equity_random'], 4500, '<')
    if label_id == 'dominee':
        if m['pair']: return False
        return thr(m['domination'], 3000, '>=')
    if label_id == 'paire_faible': return thr(m['part_paire_faible'], 6000, '>=')
    return None


def statement_fr(label_id):
    """l'affirmation telle qu'elle est proposée : « Elle est assortie : peut faire une couleur… »"""
    t = label_defs()[label_id]['fr']
    return t[0].upper() + t[1:]


def allowed_labels(level):
    ids = list(label_defs())
    return [i for i in ids if i in LEVEL1_LABELS] if level == 1 else ids


def _compatible(ids):
    return not any(o <= set(ids) for o in OPPOSITES)


def make_labels(hand, level, rnd):
    """(mode, [4 identifiants]) ou None : mode « vraie » (une vraie, trois fausses) ou « fausse » (trois vraies, une fausse)"""
    ids = allowed_labels(level)
    true = [i for i in ids if clarity(i, hand) is True]; false = [i for i in ids if clarity(i, hand) is False]
    modes = ['vraie'] + (['fausse'] if level >= 2 else [])
    rnd.shuffle(modes)
    for mode in modes:
        need_t, need_f = (1, 3) if mode == 'vraie' else (3, 1)
        if len(true) < need_t or len(false) < need_f: continue
        for _ in range(30):
            pick = rnd.sample(true, need_t) + rnd.sample(false, need_f)
            if _compatible(pick):
                rnd.shuffle(pick); return mode, pick
    return None


# ------------------------------------------------------------------ identifiants
def spot_id_bands(kind, topic, level, w, n, pos): return f'eq:{kind}:{topic}:L{level}:w{w}:n{n}:p{pos}'


def spot_id_labels(mode, level, ids): return f"eq:labels:{mode}:L{level}:{'.'.join(ids)}"


def parse(spot_id):
    """dict(kind, topic | mode, level, w, n, pos | ids) ; ValueError si l'identifiant est mal formé"""
    p = spot_id.split(':')
    try:
        if p[0] != 'eq' or p[1] not in KINDS: raise ValueError
        if p[1] in BOARD_KINDS: return equity_board.HANDLERS[p[1]]['parse'](spot_id)
        level = int(p[3][1:])
        if p[1] == 'labels':
            ids = p[4].split('.')
            if p[2] not in ('vraie', 'fausse') or len(ids) != 4 or any(i not in label_defs() for i in ids): raise ValueError
            return dict(kind='labels', mode=p[2], level=level, ids=ids)
        return dict(kind=p[1], topic=p[2], level=level, w=int(p[4][1:]), n=int(p[5][1:]), pos=int(p[6][1:]))
    except (ValueError, IndexError):
        raise ValueError(f'question d\'équité inconnue : {spot_id}')


def _built(spot_id, hand):
    """reconstruit la question et vérifie qu'elle reste valable : dict(kind, …, value, f, options, correct) ; ValueError sinon"""
    q = parse(spot_id)
    if q['kind'] in BOARD_KINDS:
        try: return equity_board.HANDLERS[q['kind']]['built'](q, hand)
        except ValueError: raise ValueError(f'question d\'équité invalide pour {hand} : {spot_id}')
    if hand not in NAMES: raise ValueError(f'main inconnue : {hand}')
    if q['kind'] == 'labels':
        cl = [clarity(i, hand) for i in q['ids']]
        want = True if q['mode'] == 'vraie' else False
        if None in cl or cl.count(want) != 1 or not set(q['ids']) <= set(allowed_labels(q['level'])):
            raise ValueError(f'question d\'équité invalide pour {hand} : {spot_id}')
        return dict(q, clarity=cl, options=[statement_fr(i) for i in q['ids']], correct=cl.index(want))
    v = topic_value(q['kind'], q['topic'], hand)
    if q['kind'] == 'hit' and (v is None or HIT_TOPICS[q['topic']]['level'] > q['level']): v = None
    if q['kind'] == 'equity' and q['topic'] not in equity_topics(q['level']): v = None
    f = frontiers(v, q['w'], q['n'], q['pos']) if v is not None and v >= MIN_BP else None
    if f is None: raise ValueError(f'question d\'équité invalide pour {hand} : {spot_id}')
    return dict(q, value=v, f=f, options=band_labels(f), correct=q['pos'])


def valid(spot_id, hand):
    try: _built(spot_id, hand); return True
    except ValueError: return False


# ------------------------------------------------------------------ tirage
def _hand(rnd, ok, avoid):
    cand = [h for h in NAMES if ok(h) and h not in avoid] or [h for h in NAMES if ok(h)]
    return rnd.choices(cand, [_W[h] for h in cand])[0] if cand else None


def draw_one(kind, level, rnd, avoid=frozenset(), topic=None):
    """(spot_id, main) d'une sorte donnée, ou None après plusieurs essais"""
    if kind in BOARD_KINDS: return equity_board.HANDLERS[kind]['draw'](level, rnd, avoid, topic)
    for _ in range(200):
        if kind == 'labels':
            h = _hand(rnd, lambda h: True, avoid); r = make_labels(h, level, rnd)
            if r: return spot_id_labels(r[0], level, r[1]), h
            continue
        topics = [t for t, d in HIT_TOPICS.items() if d['level'] <= level] if kind == 'hit' else equity_topics(level)
        t = topic or rnd.choice(topics)
        n = 4 if level == 1 else rnd.choice((5, 6))
        pos = rnd.randrange(n)                                  # rang de la bonne tranche d'abord : pas toujours « moins de … »
        h = _hand(rnd, lambda h: (v := topic_value(kind, t, h)) is not None and v >= MIN_BP and any(p == pos for _, p in feasible(v, level, n)), avoid)
        if h is None: continue
        w = next(w for w, p in feasible(topic_value(kind, t, h), level, n) if p == pos)
        return spot_id_bands(kind, t, level, w, n, pos), h
    return None


def draw(level, size=SERIES_SIZE, seed=None, kind=None, avoid_hands=frozenset()):
    """[(spot_id, main)] : les trois sortes en alternance (ordre au hasard), une main ne revient pas dans la série, un sujet non plus
    tant que possible. kind : une seule sorte. avoid_hands : mains des dernières séries, évitées si possible"""
    rnd = random.Random(seed); level = level_of(level)
    kinds = [kind] if kind else list(DEFAULT_KINDS)
    order = []
    while len(order) < size:
        k = kinds[:]; rnd.shuffle(k); order += k
    out = []; seen = set(); topics = set()
    for k in order[:size]:
        best = None
        for _ in range(6):                                      # un sujet pas encore servi dans la série, si possible
            r = draw_one(k, level, rnd, frozenset(seen) | frozenset(avoid_hands))
            if r is None: continue
            best = r
            if ':'.join(r[0].split(':')[:3]) not in topics or k == 'labels': break
        if best is None: raise ValueError(f'aucune question d\'équité disponible ({k}, niveau {level})')
        out.append(best); seen.add(best[1]); topics.add(':'.join(best[0].split(':')[:3]))
    return out


# ------------------------------------------------------------------ énoncé
def _hd(hand):
    from .quiz import hand_display
    return hand_display(hand)


def prompt(spot_id, hand):
    q = parse(spot_id)
    if q['kind'] in BOARD_KINDS: return equity_board.HANDLERS[q['kind']]['prompt'](q, hand)
    hd = _hd(hand)
    if q['kind'] == 'hit':
        return f"Tu as {hd}. Quelle est la chance de toucher {HIT_TOPICS[q['topic']]['fr']} au flop ?"
    if q['kind'] == 'equity':
        if q['topic'] == 'hasard':
            return (f"Tu as {hd} et tu es à tapis avant le flop contre une main au hasard. Quelles sont tes chances de gagner ? (une égalité compte pour moitié)"
                    if q['level'] == 1 else f"Quelle est l'équité de {hd} contre une main au hasard ?")
        r = _range(q['topic']); txt = _range_text(q['topic'])
        return (f"Tu as {hd}. {txt[0].upper() + txt[1:]} avec {pct_fr(r['share'], 0)} des mains. Si tu paies, quelles sont tes chances de gagner ?"
                if q['level'] == 1 else f"Quelle est l'équité de {hd} contre les mains avec lesquelles {txt} ({pct_fr(r['share'], 0)} des mains) ?")
    return f"Tu as {hd}. Laquelle de ces affirmations est {'vraie' if q['mode'] == 'vraie' else 'fausse'} ?"


def question(spot_id, hand):
    """ce que voit le joueur, sans la solution"""
    b = _built(spot_id, hand); pre = 'b' if b['kind'] != 'labels' else 'o'
    board = equity_board.HANDLERS[b['kind']]['extra'](b, hand) if b['kind'] in BOARD_KINDS else dict(street=None, board=[], board_display=[], hero_cards=None, villain_cards=None, ranges=[], dead_cards=[])
    return dict(spot_id=spot_id, hand=hand, hand_display=board.pop('hand_display', None) or _hd(hand), prompt_fr=prompt(spot_id, hand), mode='equity', family='equity', **board,
                category_fr=CATEGORY_FR, kind=b['kind'], kind_fr=KIND_FR[b['kind']], topic=b.get('topic') or b.get('mode'), level=b['level'],
                answer='band' if pre == 'b' else 'statement', multiple=False,
                table=None, players=[], stacks_bb=[], hero=None, history=[], history_fr=[], pot_bb=None, to_call_bb=None, difficulty=None,
                villain=None, profile=None, node_key=None,
                options=[dict(id=f'{pre}{i}', label_fr=t) for i, t in enumerate(b['options'])])


# ------------------------------------------------------------------ correction
def _label_line(lab, level):
    """« Assortie : peut faire une couleur… » avec la valeur mesurée quand elle parle (pourcentage), sauf au niveau 1"""
    t = lab['fr'][0].upper() + lab['fr'][1:]
    if level >= 2 and isinstance(lab.get('valeur'), (int, float)) and str(lab.get('unite', '')).startswith('dix-millièmes') and lab['id'] not in ('assortie', 'depareillee'):
        t += f" ({pct_fr(lab['valeur'])})"
    return t


def strengths(hand, level=2):
    """(forces, faiblesses) en phrases simples ; pour une paire, les règles pensées pour deux rangs différents sont écartées"""
    labs = [l for l in equities.labels(hand) if not (is_pair(hand) and l['id'] in PAIR_UNCLEAR)]
    f = [_label_line(l, level) for l in labs if l['groupe'] == 'force']; w = [_label_line(l, level) for l in labs if l['groupe'] == 'faiblesse']
    return f, w


PLAIN_RULE = {   # la règle en mots simples (la table garde la règle complète, avec ses seuils)
    'assortie': "deux cartes de la même couleur", 'depareillee': "deux cartes de couleurs différentes", 'paire_de_poche': "deux cartes de même hauteur",
    'cartes_hautes': "deux cartes de dix ou plus (T, J, Q, K, A)", 'bloque_les_as': "un As dans la main",
    'connectee': "deux hauteurs qui se suivent, et un tirage quinte ouvert au flop au moins 3 % du temps",
    'cartes_eloignees': "au moins deux hauteurs d'écart, et un tirage quinte ouvert moins de 2 % du temps",
    'top_paire_souvent': "la top paire ou mieux au flop au moins 25 % du temps", 'top_paire_rarement': "la top paire ou mieux au flop moins de 12 % du temps",
    'beaucoup_de_tirages': "un tirage couleur au moins 10 % du temps, ou un tirage quinte ouvert au moins 9 %",
    'forte_contre_au_hasard': "au moins 60 % d'équité contre une main au hasard", 'faible_contre_au_hasard': "moins de 45 % d'équité contre une main au hasard",
    'dominee': "au moins 30 % des mains fortes (les 20 % meilleures) ont la même carte avec une meilleure deuxième carte",
    'paire_faible': "au moins 60 % des fois où elle touche, c'est une paire plus basse que la plus haute carte du tableau",
}


def _measured(label_id, m):
    """ce qu'on a mesuré sur la main, en mots ; None pour une règle sans mesure (couleur, hauteur)"""
    if label_id in ('connectee', 'cartes_eloignees'): return f"tirage quinte ouvert au flop {pct_fr(m['tirage_quinte_8'])}"
    if label_id in ('top_paire_souvent', 'top_paire_rarement'): return f"top paire ou mieux au flop {pct_fr(m['au_moins_top_paire'])}"
    if label_id in ('forte_contre_au_hasard', 'faible_contre_au_hasard'): return f"équité contre une main au hasard {pct_fr(m['equity_random'])}"
    if label_id == 'beaucoup_de_tirages': return f"tirage couleur {pct_fr(m['tirage_couleur'])}, tirage quinte ouvert {pct_fr(m['tirage_quinte_8'])}"
    if label_id == 'dominee': return f"{pct_fr(m['domination'], 0)} des mains fortes la dominent"
    if label_id == 'paire_faible': return f"paire faible dans {pct_fr(m['part_paire_faible'], 0)} des flops touchés"
    return None


def _why_statement(label_id, hand, truth):
    """« Faux : il faut la top paire ou mieux au flop au moins 25 % du temps ; 9♠8♥ : top paire ou mieux au flop 14,2 %. »"""
    meas = _measured(label_id, measures(hand)); rule = PLAIN_RULE[label_id]; hd = _hd(hand)
    if meas is None:
        return f"{'Vrai' if truth else 'Faux'} : {hd} {'a' if truth else 'n’a pas'} {rule}."
    return f"{'Vrai' if truth else 'Faux'} : il faut {rule} ; {hd} : {meas}."


def correct(spot_id, hand, action_id):
    """correction : verdict, valeur exacte, comment on l'a calculée, forces et faiblesses ; ValueError si la réponse n'est pas proposée"""
    b = _built(spot_id, hand); pre = 'b' if b['kind'] != 'labels' else 'o'
    ids = [f'{pre}{i}' for i in range(len(b['options']))]
    if action_id not in ids: raise ValueError(f'réponse non proposée : {action_id}')
    j = ids.index(action_id); c = b['correct']; level = b['level']
    if b['kind'] == 'labels':
        verdict = 'correct' if j == c else 'erreur'
    else:
        verdict = 'correct' if j == c else 'imprécision' if abs(j - c) == 1 else 'erreur'
    forces, faiblesses = ([], []) if b['kind'] in BOARD_KINDS else strengths(hand, level)
    extra = {}
    if b['kind'] in BOARD_KINDS:
        essential, method, board_lines, extra = equity_board.HANDLERS[b['kind']]['correction'](b, hand)
    elif b['kind'] == 'hit':
        hd = _hd(hand)
        t = HIT_TOPICS[b['topic']]; v = b['value']
        value_fr = pct_fr(v); n = round(N_FLOPS * v / 10000)
        essential = f"{hd} touche {t['fr']} au flop {value_fr} du temps, environ une fois sur {max(1, round(10000 / v))}."
        method = f"Calcul : sur les {_int_fr(N_FLOPS)} flops possibles une fois tes deux cartes retirées du paquet, environ {_int_fr(n)} donnent {t['what']}."
        extra = dict(value_bp=v, value_fr=value_fr, flops=N_FLOPS)
    elif b['kind'] == 'equity':
        hd = _hd(hand); v = b['value']; value_fr = pct_fr(v)
        if b['topic'] == 'hasard':
            essential = (f"Contre une main au hasard, {hd} gagne {value_fr} du temps (égalités comptées pour moitié)." if level == 1
                         else f"L'équité de {hd} contre une main au hasard est de {value_fr}.")
            method = "Calcul : équité exacte avant le flop contre chacune des mains adverses possibles, en tirant les cinq cartes du tableau jusqu'au bout ; une égalité compte pour moitié."
        else:
            r = _range(b['topic']); txt = _range_text(b['topic'])
            essential = (f"Quand {txt}, {hd} gagne {value_fr} du temps (égalités comptées pour moitié)." if level == 1
                         else f"L'équité de {hd} contre la range ({txt}, {pct_fr(r['share'], 0)} des mains) est de {value_fr}.")
            method = ("Calcul : équité exacte avant le flop contre chaque main de cette range, pondérée par sa fréquence dans la banque du solveur ; "
                      "les mains qui partagent une de tes cartes sont retirées ; une égalité compte pour moitié.")
        extra = dict(value_bp=v, value_fr=value_fr, range_id=None if b['topic'] == 'hasard' else b['topic'])
    else:
        truth = [x for x in b['clarity']]
        essential = f"La bonne réponse : « {b['options'][c]} »."
        method = "Les affirmations viennent de règles chiffrées, appliquées aux chances de toucher au flop et à l'équité de la main."
        extra = dict(statements=[dict(id=ids[i], label_fr=b['options'][i], label_id=b['ids'][i], true=bool(truth[i]),
                                      why_fr=_why_statement(b['ids'][i], hand, truth[i])) for i in range(4)])
    lines = [essential, method]
    if b['kind'] in BOARD_KINDS:
        lines.append(f"Bonne réponse : {b['options'][c]}." + ('' if verdict == 'correct' else f" Ta réponse : {b['options'][j]}"
                                                                    + (" (réponse voisine : demi-point)." if verdict == 'imprécision' else ".")))
        lines += board_lines
    elif b['kind'] != 'labels':
        lines.append(f"Bonne tranche : {b['options'][c]}." + ('' if verdict == 'correct' else f" Ta réponse : {b['options'][j]}"
                                                                   + (" (tranche voisine : demi-point)." if verdict == 'imprécision' else ".")))
    else:
        lines += [s['why_fr'] for s in extra['statements']]
    sw = []
    if forces: sw.append('Forces : ' + ' ; '.join(forces) + '.')
    if faiblesses: sw.append('Faiblesses : ' + ' ; '.join(faiblesses) + '.')
    core = lines + sw
    return dict(verdict=verdict, points=grading.POINTS[verdict], regret_mbb=0.0, best_action=ids[c], best_label=b['options'][c],
                top_action=ids[c], chosen_action=action_id, chosen_label=b['options'][j], gto_action=None, gto_label=None,
                good_actions=[], good_labels=[], strategy=[], loss_fr=None, ev_source='table', exploit=None, avis=None, solver_regret_mbb=None,
                why_fr=[], next=None, range=None, explanation_fr='\n'.join(core), core_fr='\n'.join(core), essential_fr=essential,
                remember_fr=None, details_fr=core[1:], method_fr=method, strengths_fr=forces, weaknesses_fr=faiblesses,
                equity=dict(kind=b['kind'], category_fr=CATEGORY_FR, correct_option=ids[c], options=b['options'], **extra),
                field=None)


# ------------------------------------------------------------------ bilan et statistiques
def summary(answers):
    """answers : [(spot_id, main, résultat de correct())] -> bilan de série (même forme que quiz.summary, sans BB perdus)"""
    n = len(answers); pts = sum(r['points'] for _, _, r in answers)
    by = {}
    for sid, h, r in answers:
        k = parse(sid)['kind']; b = by.setdefault(k, [0, 0.0]); b[0] += 1; b[1] += r['points']
    errors = [dict(spot_id=sid, hand=h, prompt_fr=prompt(sid, h), chosen=r['chosen_label'], best=r['best_label'], regret_mbb=0.0, verdict=r['verdict'],
                   timed_out=bool(r.get('timed_out')), loss_fr=None, value_fr=(r.get('equity') or {}).get('value_fr'))
              for sid, h, r in answers if r['verdict'] != 'correct']
    errors.sort(key=lambda e: e['verdict'] != 'erreur')
    return dict(questions=n, points=pts, score_pct=round(100 * pts / n, 1) if n else 0.0, bb_lost=None, ev_questions=0, bb_per_100=None,
                timeouts=sum(1 for *_, r in answers if r.get('timed_out')), verdicts={v: sum(1 for *_, r in answers if r['verdict'] == v) for v in grading.POINTS},
                by_theme=[dict(family='equity', kind=k, label_fr=KIND_FR[k], hero=None, questions=c, points=s) for k, (c, s) in sorted(by.items())],
                errors=errors, review=[e['prompt_fr'] for e in errors[:3]], category_fr=CATEGORY_FR)


def stats(rows):
    """bloc « Équités » de /users/me/stats : rows = réponses du joueur dans ce mode (spot_id, verdict, points, session_id)"""
    if not rows: return dict(questions=0, sessions=0, score_pct=None, verdicts={v: 0 for v in grading.POINTS}, by_kind=[], category_fr=CATEGORY_FR)
    by = {}
    for r in rows:
        try: k = parse(r['spot_id'])['kind']
        except ValueError: continue
        b = by.setdefault(k, [0, 0.0]); b[0] += 1; b[1] += r['points']
    n = len(rows); pts = sum(r['points'] for r in rows)
    return dict(questions=n, sessions=len({r['session_id'] for r in rows}), points=round(pts, 1), score_pct=round(100 * pts / n, 1),
                verdicts={v: sum(1 for r in rows if r['verdict'] == v) for v in grading.POINTS},
                by_kind=[dict(kind=k, label_fr=KIND_FR[k], questions=c, score_pct=round(100 * s / c, 1)) for k, (c, s) in sorted(by.items())],
                category_fr=CATEGORY_FR)
