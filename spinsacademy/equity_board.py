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
WHY_FR = ['', 'fait une paire', 'fait une double paire', 'fait un brelan', 'fait la suite', 'fait la couleur', 'fait un full', 'fait un carré', 'fait la quinte flush']
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
    return dict(street='flop', board=[name(c) for c in q['board']], board_display=[disp(c) for c in q['board']],
                hero_cards=[hand_s[:2], hand_s[2:]], hand_display=hand_display(hand_s), villain_cards=None, ranges=[], dead_cards=[])


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
                 value_bp=None if b['topic'] == 'nombre' else b['value'], outs=[dict(card=name(c), display=disp(c), category_fr=CAT_FR[cat], why_fr=WHY_FR[cat]) for c, cat in o],
                 outs_fr=detail,
                 outs_count=N, turn_bp=turn_bp, river_bp=river_bp, rule_turn_pct=2 * N, rule_river_pct=4 * N,
                 board=[name(c) for c in board], street='flop')
    return essential, method, lines, extra


def _int(n): return f"{n:,}".replace(',', ' ')


def _rule_gap(rule, exact):
    d = rule - exact
    if abs(d) < 1.5: return f"(valeur exacte {str(round(exact, 1)).replace('.', ',')} % : la règle tombe juste)"
    return f"(valeur exacte {str(round(exact, 1)).replace('.', ',')} % : la règle {'surestime' if d > 0 else 'sous-estime'} de {str(round(abs(d), 1)).replace('.', ',')} point{'s' if abs(d) >= 2 else ''})"


# ================================================================== sorte « board_equity » : équité d'une main sur un flop connu
# Équité exacte d'une main précise contre une main au hasard ou contre la range de tapis du SB (banque du solveur), une fois le flop
# connu : les 1 081 turns et rivers possibles, chaque main adverse pondérée par sa fréquence, cartes bloquées retirées, égalité pour
# moitié. Le héros paie le tapis : sa main est tirée dans la range de call du BB à ce tapis (main au hasard : n'importe quelle main).
# Identifiant : eq:board_equity:{hasard | huN_sb_tapis}:L{niveau}:{flop}:w{largeur}:n{tranches}:p{rang} ; main exacte dans hand.
from functools import lru_cache
from numba import njit
from .postflop.kernels import CC, CLASS_OF

EQ_TOPICS_L1 = ('hasard', 'hu8_sb_tapis', 'hu12_sb_tapis')
EQ_TOPICS = ('hasard', 'hu6_sb_tapis', 'hu8_sb_tapis', 'hu10_sb_tapis', 'hu12_sb_tapis')
CALLER = {f'hu{n}_sb_tapis': f'hu{n}_bb_paie' for n in (6, 8, 10, 12)}


@njit(cache=True)
def hero_equity(h0, h1, flop, opp, CC):
    """(gain, total) : masse adverse battue (égalité pour moitié) et masse adverse compatible, sommées sur les 1 081 turns et rivers"""
    used = np.zeros(52, np.bool_); used[h0] = True; used[h1] = True
    for k in range(3): used[flop[k]] = True
    cards = np.zeros(7, np.int64); cards[2] = flop[0]; cards[3] = flop[1]; cards[4] = flop[2]
    hc = np.zeros(7, np.int64); hc[0] = h0; hc[1] = h1; hc[2] = flop[0]; hc[3] = flop[1]; hc[4] = flop[2]
    win = 0.0; tot = 0.0
    for t in range(52):
        if used[t]: continue
        for r in range(t + 1, 52):
            if used[r]: continue
            hc[5] = t; hc[6] = r; me = evaln(hc, 7)
            cards[5] = t; cards[6] = r
            for c in range(1326):
                w = opp[c]
                if w <= 0: continue
                a = CC[c, 0]; b = CC[c, 1]
                if used[a] or used[b] or a == t or a == r or b == t or b == r: continue
                cards[0] = a; cards[1] = b; v = evaln(cards, 7)
                tot += w
                if me > v: win += w
                elif me == v: win += 0.5 * w
    return win, tot


@lru_cache(maxsize=16)
def class_weights(rid):
    """poids (0 à 1) de chaque classe de main dans une range de la banque : atteinte × fréquence de l'action (comme equities.build)"""
    from . import equities, quiz
    from .cards import NAMES
    rid_table = {r[0]: r for r in equities.RANGES}
    _, table, stack, hero, node, act = rid_table[rid][1:]
    _, spots = quiz.load(equities.BANK)
    sp = next(s for s in spots.values() if s['table'] == table and s['stacks_bb'] == [float(stack)] * len(s['stacks_bb']) and s['hero'] == hero and s['node_key'] == node)
    types = [a['type'] for a in sp['actions']]
    j = types.index('allin') if act == 'allin' else types.index('call_allin') if 'call_allin' in types else types.index('call')
    return tuple(round(sp['hands'][h]['reach'] * sp['hands'][h]['freq'][j], 4) for h in NAMES)


def combo_weights(topic):
    if topic == 'hasard': return np.ones(1326)
    w = np.array(class_weights(topic)); return w[np.asarray(CLASS_OF)]


@lru_cache(maxsize=4096)
def equity_on_board(topic, hand_s, board_s):
    """équité exacte (dix-millièmes) de la main sur le flop contre la range"""
    hand, board = cards_of(hand_s), cards_of(board_s)
    win, tot = hero_equity(hand[0], hand[1], np.array(board, np.int64), combo_weights(topic), CC)
    return round(10000 * win / tot)


def range_view(topic):
    """la range pour l'écran : {who, label_fr, pct, hands: {classe: poids}}"""
    from . import equities
    from .cards import NAMES
    r = next(x for x in equities.ranges() if x['id'] == topic)
    w = class_weights(topic)
    return dict(who='villain', label_fr=f"SB, tapis à {topic[2:-9]} BB en heads-up ({round(r['share'] / 100)} %)", pct=round(r['share'] / 100, 1),
                hands={h: x for h, x in zip(NAMES, w) if x > 0})


def situation_fr(hand, board):
    """ce que la main a pour l'instant, sans attribuer au joueur ce qui est sur le tableau"""
    c, cb = category(hand + board), category(board)
    if c <= cb: return f"rien de plus que le tableau ({CAT_FR[cb]} sur le tableau)" if cb else "carte haute"
    return CAT_FR[c] + (" (avec la paire du tableau)" if cb == 1 and c == 2 else "")


def eq_spot_id(topic, level, board, w, n, pos): return f"eq:board_equity:{topic}:L{level}:{''.join(name(c) for c in board)}:w{w}:n{n}:p{pos}"


def eq_parse(sid):
    p = sid.split(':')
    if len(p) != 8 or p[0] != 'eq' or p[1] != 'board_equity' or p[2] not in EQ_TOPICS: raise ValueError
    board = cards_of(p[4])
    if len(board) != 3: raise ValueError
    return dict(kind='board_equity', topic=p[2], level=int(p[3][1:]), board=board, w=int(p[5][1:]), n=int(p[6][1:]), pos=int(p[7][1:]))


def eq_built(q, hand_s):
    from . import equity_quiz as E
    hand = cards_of(hand_s)
    if len(hand) != 2 or set(hand) & set(q['board']): raise ValueError
    if q['level'] == 1 and q['topic'] not in EQ_TOPICS_L1: raise ValueError
    v = equity_on_board(q['topic'], hand_s, ''.join(name(c) for c in q['board']))
    f = E.frontiers(v, q['w'], q['n'], q['pos'])
    if f is None: raise ValueError
    return dict(q, hand=hand, value=v, f=f, options=E.band_labels(f), correct=q['pos'])


def _hand_from(topic, rnd, board, avoid):
    """main exacte du héros : n'importe laquelle (main au hasard), sinon tirée dans la range de call du BB, pondérée"""
    from .cards import NAMES
    live = [c for c in range(1326) if CC[c, 0] not in board and CC[c, 1] not in board]
    w = np.ones(1326) if topic == 'hasard' else np.array(class_weights(CALLER[topic]))[np.asarray(CLASS_OF)]
    for _ in range(20):
        c = rnd.choices(live, [w[i] for i in live])[0]
        hs = ''.join(name(x) for x in sorted((int(CC[c, 0]), int(CC[c, 1])), reverse=True))
        if hs not in avoid: return hs
    return hs


def eq_draw_one(level, rnd, avoid=frozenset(), topic=None):
    from . import equity_quiz as E
    topics = EQ_TOPICS_L1 if level == 1 else EQ_TOPICS
    for _ in range(40):
        t = topic or rnd.choice(topics)
        board = sorted(rnd.sample(range(52), 3), reverse=True)
        hs = _hand_from(t, rnd, board, avoid)
        n = 4 if level == 1 else rnd.choice((5, 6))
        v = equity_on_board(t, hs, ''.join(name(c) for c in board))
        if not 300 <= v <= 9700: continue                       # 3 % à 97 % : pas de question jouée d'avance
        opts = E.feasible(v, level, n)
        if not opts: continue
        pos = rnd.choice(sorted({p for _, p in opts})); w = next(w for w, p in opts if p == pos)
        return eq_spot_id(t, level, board, w, n, pos), hs
    return None


def eq_prompt(q, hand_s):
    hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in q['board'])
    if q['topic'] == 'hasard':
        return (f"Tu as {hd}, le flop est {bd}. Contre une main au hasard, quelles sont tes chances de gagner à la fin du coup ? (une égalité compte pour moitié)"
                if q['level'] == 1 else f"Tu as {hd}, le flop est {bd}. Quelle est ton équité contre une main au hasard ?")
    n = q['topic'][2:-9]
    return (f"Le SB part à tapis à {n} BB en heads-up, tu paies avec {hd}. Le flop est {bd}. Quelles sont tes chances de gagner maintenant ?"
            if q['level'] == 1 else f"Tu as payé le tapis du SB à {n} BB en heads-up avec {hd}. Le flop est {bd}. Quelle est ton équité contre sa range ?")


def eq_question_extra(q, hand_s):
    return dict(street='flop', board=[name(c) for c in q['board']], board_display=[disp(c) for c in q['board']], hero_cards=[hand_s[:2], hand_s[2:]],
                hand_display=hand_display(hand_s), villain_cards=None, ranges=[] if q['topic'] == 'hasard' else [range_view(q['topic'])], dead_cards=[])


def eq_correction(b, hand_s):
    from . import equity_quiz as E, equities
    from .cards import NAMES
    hand, board = b['hand'], b['board']; hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in board); v = b['value']
    a, c = sorted(hand, reverse=True); cls = RANKS[a >> 2] + RANKS[c >> 2] + ('' if a >> 2 == c >> 2 else 's' if a % 4 == c % 4 else 'o')
    pre = equities.equity_random(cls) if b['topic'] == 'hasard' else equities.equity_vs_range(cls, b['topic'])
    who = "une main au hasard" if b['topic'] == 'hasard' else f"la range de tapis du SB à {b['topic'][2:-9]} BB"
    essential = f"Sur {bd}, {hd} a {E.pct_fr(v)} d'équité contre {who}."
    method = ("Calcul : les 1 081 turns et rivers possibles, contre chaque main adverse" + ("" if b['topic'] == 'hasard' else " de la range, pondérée par sa fréquence dans la banque du solveur")
              + " ; les cartes déjà vues (ta main, le flop) sont retirées ; une égalité compte pour moitié.")
    d = (v - pre) / 100
    move = ("le flop t'aide nettement" if d >= 3 else "le flop te dessert nettement" if d <= -3 else "le flop change peu de chose")
    now = situation_fr(hand, board); o = outs(hand, board)
    lines = [f"Avant le flop : {E.pct_fr(pre)} ({cls}, toutes couleurs confondues) ; au flop : {E.pct_fr(v)} : {move} ({'+' if d >= 0 else '−'}{str(round(abs(d), 1)).replace('.', ',')} points).",
             f"Ta main pour l'instant : {now} ; {_plural(len(o))} l'améliorent au turn.",
             "L'équité dit qui est devant si toutes les cartes sont retournées, pas qui gagnera l'argent : la position et les mises à venir comptent aussi."]
    extra = dict(value_bp=v, value_fr=E.pct_fr(v), board=[name(x) for x in board], street='flop', range_id=None if b['topic'] == 'hasard' else b['topic'],
                 by_street=[dict(street='preflop', value_bp=pre), dict(street='flop', value_bp=v)], hand_category_fr=now, outs_count=len(o))
    return essential, method, lines, extra
