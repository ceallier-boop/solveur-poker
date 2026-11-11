"""Questions d'équités avec un tableau (v2, CE4) : sorte « outs » (tirages et cartes qui améliorent la main).

Définition (décision du porteur, 11/11/2026) : une carte améliore ta main si, une fois ajoutée, ta main monte de catégorie
(carte haute, paire, double paire, brelan, suite, couleur, full, carré, quinte flush) PLUS que le tableau seul. Ainsi une carte qui
paire le tableau n'est pas comptée quand elle ne fait que donner la même paire à tout le monde, mais elle compte quand elle
transforme ton brelan en full.
  - Δ main = catégorie(main + tableau + carte) − catégorie(main + tableau)
  - Δ tableau = catégorie(tableau + carte) − catégorie(tableau)
  - la carte compte si Δ main > Δ tableau.
Jusqu'à la river, même règle avec les deux cartes (turn et river) : on énumère les 1 081 couples possibles, les améliorations en
deux cartes (tirage « runner-runner ») comprises.

Trois sujets, sur une main exacte (cartes et couleurs) et un flop :
  nombre : « Combien de cartes améliorent ta main au turn ? » (réponses : nombres de cartes, la bonne parmi quatre) ;
  turn   : « Quelle est la probabilité d'améliorer ta main au turn ? » (tranches, marge de 1,5 point) ;
  river  : « … au turn ou à la river ? » (tranches, marge de 1,5 point).
Identifiant : eq:outs:{sujet}:L{niveau}:{flop}:w{pas}:n{nombre d'options}:p{rang de la bonne}, main exacte dans la colonne hand
(« 9s8s »). La correction compare la valeur exacte à la règle des 2 et 4.
"""
import itertools, random
import numpy as np
from .postflop.kernels import evaln

RANKS = '23456789TJQKA'
SUITS = 'shdc'
SYM = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}
CAT_FR = ['carte haute', 'paire', 'double paire', 'brelan', 'suite', 'couleur', 'full', 'carré', 'quinte flush']
TOPICS = ('nombre', 'turn', 'river')
TOPICS_L1 = ('nombre', 'turn')
N_TURN = 47
N_RUNOUTS = 1081                       # C(47, 2)
STEP = {1: 3, 2: 2}                    # écart entre deux réponses proposées pour « nombre »
MIN_OUTS, MAX_OUTS = 2, 21
DRAW_SHARE = 0.6                       # part des questions tirées sur une main avec un tirage suite ou couleur


def card(t):
    if len(t) != 2 or t[0] not in RANKS or t[1] not in SUITS: raise ValueError(f'carte inconnue : {t}')
    return RANKS.index(t[0]) * 4 + SUITS.index(t[1])


def name(c): return RANKS[c >> 2] + SUITS[c & 3]


def disp(c): return RANKS[c >> 2] + SYM[SUITS[c & 3]]


def cards_of(s):
    out = [card(s[i:i + 2]) for i in range(0, len(s), 2)]
    if len(set(out)) != len(out): raise ValueError(f'carte en double : {s}')
    return out


def category(cs):
    """catégorie (0 carte haute … 8 quinte flush) de 3 à 7 cartes ; sous 5 cartes, ni suite ni couleur possibles"""
    if len(cs) >= 5: return int(evaln(np.array(cs, np.int64), len(cs))) >> 20
    cnt = sorted((sum(1 for c in cs if c >> 2 == r) for r in {c >> 2 for c in cs}), reverse=True)
    if cnt[0] == 4: return 7
    if cnt[0] == 3: return 3
    if cnt[0] == 2: return 2 if len(cnt) > 1 and cnt[1] == 2 else 1
    return 0


def improves(hand, board, extra):
    """la ou les cartes `extra` améliorent la main plus que le tableau seul (règle du module)"""
    return category(hand + board + extra) - category(hand + board) > category(board + extra) - category(board)


def outs(hand, board):
    """[(carte, nouvelle catégorie)] des cartes du paquet qui améliorent la main au turn"""
    dead = set(hand + board)
    return [(c, category(hand + board + [c])) for c in range(52) if c not in dead and improves(hand, board, [c])]


def river_count(hand, board):
    """nombre de couples (turn, river) sur 1 081 qui améliorent la main à la river"""
    live = [c for c in range(52) if c not in set(hand + board)]
    return sum(1 for t, r in itertools.combinations(live, 2) if improves(hand, board, [t, r]))


def value(topic, hand, board):
    """nombre de cartes (nombre) ou probabilité en dix-millièmes (turn, river)"""
    if topic == 'nombre': return len(outs(hand, board))
    if topic == 'turn': return round(10000 * len(outs(hand, board)) / N_TURN)
    return round(10000 * river_count(hand, board) / N_RUNOUTS)


# ------------------------------------------------------------------ identifiants
def spot_id(topic, level, board, w, n, pos): return f"eq:outs:{topic}:L{level}:{''.join(name(c) for c in board)}:w{w}:n{n}:p{pos}"


def parse(sid):
    p = sid.split(':')
    if len(p) != 8 or p[0] != 'eq' or p[1] != 'outs' or p[2] not in TOPICS: raise ValueError
    board = cards_of(p[4])
    if len(board) != 3: raise ValueError
    return dict(kind='outs', topic=p[2], level=int(p[3][1:]), board=board, w=int(p[5][1:]), n=int(p[6][1:]), pos=int(p[7][1:]))


def count_options(N, w, n, pos):
    """nombres proposés : N au rang pos, espacés de w ; None si un nombre sortirait de 0 à 47"""
    opts = [N + (k - pos) * w for k in range(n)]
    return opts if opts[0] >= 0 and opts[-1] <= N_TURN else None


def _plural(x): return f"{x} carte" + ('s' if x > 1 else '')


def built(q, hand_s):
    """q : parse(spot_id) ; vérifie la question et renvoie dict(q, hand, value, options, correct, …) ; ValueError si invalide"""
    from . import equity_quiz as E
    hand = cards_of(hand_s)
    if len(hand) != 2 or set(hand) & set(q['board']): raise ValueError
    if q['level'] == 1 and q['topic'] not in TOPICS_L1: raise ValueError
    if category(hand + q['board']) > 1: raise ValueError
    N = len(outs(hand, q['board']))
    if not MIN_OUTS <= N <= MAX_OUTS: raise ValueError
    if q['topic'] == 'nombre':
        opts = count_options(N, q['w'], q['n'], q['pos'])
        if opts is None or q['w'] != STEP[1 if q['level'] == 1 else 2]: raise ValueError
        return dict(q, hand=hand, value=N, options=[_plural(x) for x in opts], numbers=opts, correct=q['pos'])
    v = value(q['topic'], hand, q['board'])
    f = E.frontiers(v, q['w'], q['n'], q['pos'])
    if f is None: raise ValueError
    return dict(q, hand=hand, value=v, f=f, options=E.band_labels(f), correct=q['pos'])


# ------------------------------------------------------------------ tirage
def _has_draw(hand, board): return any(cat in (4, 5, 8) for _, cat in outs(hand, board))


def draw_one(level, rnd, avoid=frozenset(), topic=None):
    """(spot_id, main) ou None : flop sans paire, main au plus une paire, entre 2 et 21 cartes qui l'améliorent"""
    from . import equity_quiz as E
    topics = TOPICS_L1 if level == 1 else TOPICS
    for _ in range(400):
        t = topic or rnd.choice(topics)
        deck = list(range(52)); rnd.shuffle(deck)
        board, hand = deck[:3], deck[3:5]
        hs = ''.join(name(c) for c in sorted(hand, reverse=True))
        if hs in avoid or len({c >> 2 for c in board}) < 3 or category(hand + board) > 1: continue
        o = outs(hand, board)
        if not MIN_OUTS <= len(o) <= MAX_OUTS: continue
        if rnd.random() < DRAW_SHARE and not any(cat in (4, 5, 8) for _, cat in o): continue
        n = 4 if (level == 1 or t == 'nombre') else rnd.choice((5, 6)); pos = rnd.randrange(n)
        if t == 'nombre':
            w = STEP[1 if level == 1 else 2]
            if count_options(len(o), w, n, pos) is None: continue
        else:
            v = value(t, hand, board)
            ws = [w for w, p in E.feasible(v, level, n) if p == pos]
            if not ws: continue
            w = ws[0]
        return spot_id(t, level, board, w, n, pos), hs
    return None


# ------------------------------------------------------------------ énoncé et correction
def hand_display(hand_s): return ''.join(disp(c) for c in cards_of(hand_s))


def prompt(q, hand_s):
    hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in q['board'])
    word = "de cartes améliorent ta main" if q['level'] == 1 else "d'outs (cartes qui améliorent ta main)"
    if q['topic'] == 'nombre': return f"Tu as {hd}, le flop est {bd}. Combien {word} au turn ?"
    if q['topic'] == 'turn': return f"Tu as {hd}, le flop est {bd}. Quelle est la probabilité d'améliorer ta main au turn ?"
    return f"Tu as {hd}, le flop est {bd}. Quelle est la probabilité d'améliorer ta main au turn ou à la river ?"


def question_extra(q, hand_s):
    """champs propres aux questions avec tableau"""
    return dict(street='flop', board=[disp(c) for c in q['board']], board_cards=[name(c) for c in q['board']],
                hand_cards=[hand_s[:2], hand_s[2:]], hand_display=hand_display(hand_s), villain_hand=None)


def correction(b, hand_s):
    """(essentiel, méthode, lignes, extra) d'une question « outs » construite par built()"""
    from . import equity_quiz as E
    hand, board = b['hand'], b['board']; hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in board)
    o = outs(hand, board); N = len(o); now = CAT_FR[category(hand + board)]
    groups = {}
    for c, cat in sorted(o, key=lambda x: (-x[1], -x[0])): groups.setdefault(cat, []).append(c)
    detail = ' ; '.join(f"{CAT_FR[cat]} : {_plural(len(cs))} ({', '.join(disp(c) for c in cs)})" for cat, cs in groups.items())
    turn_bp = round(10000 * N / N_TURN); rc = river_count(hand, board); river_bp = round(10000 * rc / N_RUNOUTS)
    if b['topic'] == 'nombre': essential = f"Avec {hd} sur {bd} (pour l'instant : {now}), {_plural(N)} sur 47 améliorent ta main au turn."
    elif b['topic'] == 'turn': essential = f"Avec {hd} sur {bd}, tu améliores ta main au turn {E.pct_fr(turn_bp)} du temps ({N} cartes sur 47)."
    else: essential = f"Avec {hd} sur {bd}, tu améliores ta main au turn ou à la river {E.pct_fr(river_bp)} du temps."
    method = ("Calcul : chacune des 47 cartes inconnues est essayée au turn ; elle compte si ta main monte de catégorie (paire, double paire, "
              "brelan, suite, couleur…) plus que le tableau seul. Une carte qui paire seulement le tableau ne compte pas.")
    if b['topic'] == 'river':
        method += " Jusqu'à la river : les 1 081 couples de turn et river possibles, en comptant aussi les améliorations qui demandent les deux cartes."
    lines = [f"Les cartes qui t'améliorent : {detail}.",
             f"Au turn : {N} sur 47 = {E.pct_fr(turn_bp)}. Jusqu'à la river : {_int(rc)} couples sur 1 081 = {E.pct_fr(river_bp)}.",
             f"Règle des 2 et 4 : {N} × 2 = {2 * N} % au turn, {N} × 4 = {4 * N} % jusqu'à la river "
             + _rule_gap(4 * N, river_bp / 100) + ".",
             "Attention : une carte qui t'améliore ne te fait pas toujours passer devant (elle peut aussi donner une suite ou une couleur à l'adversaire)."]
    extra = dict(value=b['value'], value_fr=(_plural(b['value']) if b['topic'] == 'nombre' else E.pct_fr(b['value'])),
                 value_bp=None if b['topic'] == 'nombre' else b['value'], outs=[dict(card=name(c), display=disp(c), category_fr=CAT_FR[cat]) for c, cat in o],
                 outs_count=N, turn_bp=turn_bp, river_bp=river_bp, rule_turn_pct=2 * N, rule_river_pct=4 * N,
                 board=[disp(c) for c in board], street='flop')
    return essential, method, lines, extra


def _int(n): return f"{n:,}".replace(',', ' ')


def _rule_gap(rule, exact):
    d = rule - exact
    if abs(d) < 1.5: return f"(valeur exacte {str(round(exact, 1)).replace('.', ',')} % : la règle tombe juste)"
    return f"(valeur exacte {str(round(exact, 1)).replace('.', ',')} % : la règle {'surestime' if d > 0 else 'sous-estime'} de {str(round(abs(d), 1)).replace('.', ',')} point{'s' if abs(d) >= 2 else ''})"
