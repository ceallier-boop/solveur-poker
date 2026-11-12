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
CAVEAT_OUTS = "Attention : une carte qui t'améliore ne te fait pas toujours passer devant (elle peut aussi donner une suite ou une couleur à l'adversaire)."
CAVEAT_MONEY = "L'équité dit qui est devant si toutes les cartes sont retournées, pas qui gagnera l'argent : la position et les mises à venir comptent aussi."
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
             CAVEAT_OUTS]
    extra = dict(caveat_fr=CAVEAT_OUTS, value=b['value'], value_fr=(_plural(b['value']) if b['topic'] == 'nombre' else E.pct_fr(b['value'])),
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
from numba import njit, prange
from .postflop.kernels import CC, CLASS_OF, combo_ranks, showdown

EQ_TOPICS_L1 = ('hasard', 'hu8_sb_tapis', 'hu12_sb_tapis')
EQ_TOPICS = ('hasard', 'hu6_sb_tapis', 'hu8_sb_tapis', 'hu10_sb_tapis', 'hu12_sb_tapis')
CALLER = {f'hu{n}_sb_tapis': f'hu{n}_bb_paie' for n in (6, 8, 10, 12)}


@njit(parallel=True, cache=True)
def hero_equity(h0, h1, flop, opp, CC):
    """(gain, total) : masse adverse battue (égalité pour moitié) et masse adverse compatible, sommées sur les 1 081 turns et rivers ;
    turns réparties entre les cœurs (somme exacte, l'ordre des additions ne change le résultat qu'au-delà de la 12e décimale)"""
    used = np.zeros(52, np.bool_); used[h0] = True; used[h1] = True
    for k in range(3): used[flop[k]] = True
    win = 0.0; tot = 0.0
    for t in prange(52):
        if used[t]: continue
        w1, t1 = _turn_part(h0, h1, flop, opp, CC, used, t)
        win += w1; tot += t1
    return win, tot


@njit(cache=True)
def _turn_part(h0, h1, flop, opp, CC, used, t):
    cards = np.zeros(7, np.int64); cards[2] = flop[0]; cards[3] = flop[1]; cards[4] = flop[2]
    hc = np.zeros(7, np.int64); hc[0] = h0; hc[1] = h1; hc[2] = flop[0]; hc[3] = flop[1]; hc[4] = flop[2]
    win = 0.0; tot = 0.0
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
             CAVEAT_MONEY]
    extra = dict(caveat_fr=CAVEAT_MONEY, value_bp=v, value_fr=E.pct_fr(v), board=[name(x) for x in board], street='flop', range_id=None if b['topic'] == 'hasard' else b['topic'],
                 by_street=[dict(street='preflop', value_bp=pre), dict(street='flop', value_bp=v)], hand_category_fr=now, outs_count=len(o))
    return essential, method, lines, extra


# ================================================================== sorte « flop_help » : ce flop t'aide-t-il plus que la range adverse ?
# Pot limpé en heads-up (le cas le plus fréquent de 8 à 12 BB : le SB complète 59 à 73 % de ses mains, le BB checke 51 à 59 %) : on
# compare l'équité de la main contre la range adverse avant le flop (classe de main, table des équités préflop) et au flop (exacte,
# 1 081 suites). Trois réponses : elle monte nettement (+3 points ou plus), change peu (moins de 3 points), baisse nettement.
# La variation n'est jamais à moins de 1,5 point d'une frontière : |écart| ≥ 4,5 points ou ≤ 1,5 point.
# Identifiant : eq:flop_help:huN_limp_{bb|sb}:L{niveau}:{flop}:w3:n3:p{rang} ; main exacte dans hand.
HELP_SCENARIOS = tuple(f'hu{n}_limp_{h}' for n in (8, 10, 12) for h in ('bb', 'sb'))
HELP_STEP = 3                                           # points : frontière entre « change peu » et « monte / baisse nettement »
HELP_OPTIONS = ("elle monte nettement (+3 points ou plus)", "elle change peu (moins de 3 points)", "elle baisse nettement (−3 points ou plus)")
HELP_OPTIONS_L1 = ("elles augmentent nettement", "elles changent peu", "elles baissent nettement")


@lru_cache(maxsize=16)
def node_weights(stack, node, aid):
    """poids (0 à 1) par classe d'une action de la banque en heads-up : atteinte × fréquence"""
    from . import equities, quiz
    from .cards import NAMES
    _, spots = quiz.load(equities.BANK)
    sp = next(s for s in spots.values() if s['table'] == 'heads-up' and s['stacks_bb'] == [float(stack)] * 2 and s['node_key'] == node)
    j = [a['id'] for a in sp['actions']].index(aid)
    return tuple(round(sp['hands'][h]['reach'] * sp['hands'][h]['freq'][j], 4) for h in NAMES)


def scenario(sc):
    """(tapis, poste du héros, poids du héros par classe, poids adverses par classe)"""
    n, hero = int(sc[2:].split('_')[0]), sc.rsplit('_', 1)[1]
    sb, bb = node_weights(n, 'root', 'C'), node_weights(n, 'SB-call', 'X')
    return n, hero.upper(), (bb if hero == 'bb' else sb), (sb if hero == 'bb' else bb)


@lru_cache(maxsize=16)
def _pre_equities(sc):
    from . import allin
    return tuple(float(x) for x in allin.equity_vs_range(np.array(scenario(sc)[3])))


def class_of(hand):
    a, c = sorted(hand, reverse=True)
    return RANKS[a >> 2] + RANKS[c >> 2] + ('' if a >> 2 == c >> 2 else 's' if a % 4 == c % 4 else 'o')


@lru_cache(maxsize=4096)
def help_values(sc, hand_s, board_s):
    """(équité avant le flop, équité au flop) en dix-millièmes contre la range adverse"""
    from .cards import NAMES
    hand, board = cards_of(hand_s), cards_of(board_s)
    pre = round(10000 * _pre_equities(sc)[NAMES.index(class_of(hand))])
    opp = np.array(scenario(sc)[3])[np.asarray(CLASS_OF)]
    win, tot = hero_equity(hand[0], hand[1], np.array(board, np.int64), opp, CC)
    return pre, round(10000 * win / tot)


def help_answer(pre, flop):
    """rang de la bonne réponse (0 monte, 1 change peu, 2 baisse) ou None si l'écart est trop près d'une frontière"""
    d = (flop - pre) / 100
    if d >= HELP_STEP + 1.5: return 0
    if d <= -HELP_STEP - 1.5: return 2
    if abs(d) <= HELP_STEP - 1.5: return 1
    return None


def help_spot_id(sc, level, board, pos): return f"eq:flop_help:{sc}:L{level}:{''.join(name(c) for c in board)}:w{HELP_STEP}:n3:p{pos}"


def help_parse(sid):
    p = sid.split(':')
    if len(p) != 8 or p[0] != 'eq' or p[1] != 'flop_help' or p[2] not in HELP_SCENARIOS or p[5] != f'w{HELP_STEP}' or p[6] != 'n3': raise ValueError
    board = cards_of(p[4])
    if len(board) != 3: raise ValueError
    return dict(kind='flop_help', topic=p[2], level=int(p[3][1:]), board=board, w=HELP_STEP, n=3, pos=int(p[7][1:]))


def help_built(q, hand_s):
    from .cards import NAMES
    hand = cards_of(hand_s)
    if len(hand) != 2 or set(hand) & set(q['board']): raise ValueError
    if scenario(q['topic'])[2][NAMES.index(class_of(hand))] <= 0: raise ValueError        # la main doit être dans la range du héros
    pre, v = help_values(q['topic'], hand_s, ''.join(name(c) for c in q['board']))
    if help_answer(pre, v) != q['pos']: raise ValueError
    return dict(q, hand=hand, value=v, pre=pre, options=list(HELP_OPTIONS_L1 if q['level'] == 1 else HELP_OPTIONS), correct=q['pos'])


def help_draw_one(level, rnd, avoid=frozenset(), topic=None):
    """la bonne réponse d'abord (monte, change peu, baisse : à parts égales), puis un flop et une main de la range du héros qui la donnent"""
    want = rnd.randrange(3); fallback = None
    for k in range(60):
        if k >= 40 and fallback: return fallback                # après 40 essais (environ 1 s) : la première question valable
        sc = topic or rnd.choice(HELP_SCENARIOS)
        board = sorted(rnd.sample(range(52), 3), reverse=True)
        live = [c for c in range(1326) if CC[c, 0] not in board and CC[c, 1] not in board]
        w = np.array(scenario(sc)[2])[np.asarray(CLASS_OF)]
        c = rnd.choices(live, [w[i] for i in live])[0]
        hs = ''.join(name(x) for x in sorted((int(CC[c, 0]), int(CC[c, 1])), reverse=True))
        if hs in avoid: continue
        if len({x >> 2 for x in board}) == 1: continue          # flop à brelan : rien à lire
        pre, v = help_values(sc, hs, ''.join(name(x) for x in board)); a = help_answer(pre, v)
        if a is None: continue
        if a == want: return help_spot_id(sc, level, board, want), hs
        fallback = fallback or (help_spot_id(sc, level, board, a), hs)
    return fallback


def _help_context(sc):
    n, hero, _, _ = scenario(sc)
    return (f"Heads-up à {n} BB : le SB complète (limp), tu checkes au BB" if hero == 'BB' else f"Heads-up à {n} BB : tu complètes au SB (limp), le BB checke")


def help_prompt(q, hand_s):
    hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in q['board'])
    if q['level'] == 1:
        return f"{_help_context(q['topic'])}, avec {hd}. Le flop est {bd}. Par rapport à avant le flop, tes chances de gagner contre ses mains possibles…"
    return f"{_help_context(q['topic'])}, avec {hd}. Le flop est {bd}. Par rapport à avant le flop, ton équité contre sa range…"


def help_question_extra(q, hand_s):
    from .cards import NAMES
    n, hero, _, opp = scenario(q['topic'])
    who = 'SB, complète (limp)' if hero == 'BB' else 'BB, checke après le limp'
    pct = round(100 * sum(w * (6 if len(h) == 2 else 4 if h[2] == 's' else 12) for h, w in zip(NAMES, opp)) / 1326, 1)
    rng = dict(who='villain', label_fr=f"{who} à {n} BB ({round(pct)} %)", pct=pct, hands={h: x for h, x in zip(NAMES, opp) if x > 0})
    return dict(street='flop', board=[name(c) for c in q['board']], board_display=[disp(c) for c in q['board']], hero_cards=[hand_s[:2], hand_s[2:]],
                hand_display=hand_display(hand_s), villain_cards=None, ranges=[rng], dead_cards=[])


def help_correction(b, hand_s):
    from . import equity_quiz as E
    hand, board = b['hand'], b['board']; hd = hand_display(hand_s); bd = ' '.join(disp(c) for c in board)
    pre, v = b['pre'], b['value']; d = (v - pre) / 100; o = outs(hand, board)
    verdict = ("le flop t'aide plus que sa range" if d > 0 else "le flop aide plus sa range que ta main") if b['correct'] != 1 else "le flop ne change presque rien au rapport de force"
    essential = f"Contre sa range, {hd} passe de {E.pct_fr(pre)} avant le flop à {E.pct_fr(v)} sur {bd} ({_pts(d)}) : {verdict}."
    method = ("Calcul : avant le flop, équité exacte de ta main (toutes couleurs confondues) contre chaque main de sa range ; au flop, les 1 081 turns et "
              "rivers possibles contre chaque main de sa range encore possible, pondérée par sa fréquence dans la banque du solveur ; égalité pour moitié.")
    lines = [f"Ta main pour l'instant : {situation_fr(hand, board)} ; {_plural(len(o))} l'améliorent au turn.",
             "Une équité qui monte veut dire que ce flop touche plus souvent ta main que les mains qu'il peut avoir ; qui baisse, l'inverse.",
             CAVEAT_MONEY]
    extra = dict(caveat_fr=CAVEAT_MONEY, delta_fr=_pts(d), value_bp=v, value_fr=E.pct_fr(v), preflop_bp=pre, delta_bp=v - pre, board=[name(x) for x in board], street='flop', scenario=b['topic'],
                 by_street=[dict(street='preflop', value_bp=pre), dict(street='flop', value_bp=v)], hand_category_fr=situation_fr(hand, board), outs_count=len(o))
    return essential, method, lines, extra


# ================================================================== sorte « range_help » : ce flop aide-t-il plus ta range ou la sienne ?
# Validé par le porteur le 12/11 (seuils à confirmer par les coachs : constantes ci-dessous). Pot limpé en heads-up à 8, 10 ou 12 BB,
# ranges de la banque (SB qui complète, BB qui checke). Pas de main du héros : on compare des ranges.
#   Équité de range : Σ_a Σ_b h_a o_b gain(a, b) / Σ_a Σ_b h_a o_b sur les couples de mains sans carte commune (h, o : poids de la banque).
#   Avant le flop : équités exactes préflop par classe (data/equity_169.npy) et combinaisons disjointes (cards.DISJOINT).
#   Au flop : les 1 081 turns et rivers, chaque couple compatible compté sur toutes les suites possibles ; égalité pour moitié.
# Réponse : écart = équité de ta range au flop − avant le flop (points). « ma range » si écart ≥ RANGE_STEP + RANGE_MARGIN,
# « la sienne » si écart ≤ −(RANGE_STEP + RANGE_MARGIN), « à peu près pareil » si |écart| ≤ RANGE_STEP − RANGE_MARGIN ; sinon pas de question.
# Part des meilleures mains (non notée) : part pondérée de chaque range qui a au moins une double paire au flop avec ses propres cartes
# (catégorie(main + flop) ≥ double paire et > catégorie(flop) : même règle que les outs).
# Identifiant : eq:range_help:huN_limp_{bb|sb}:L{niveau}:{flop}:w2:n3:p{rang} ; colonne hand = « range ».
RANGE_STEP = 2.0            # points : frontière entre « à peu près pareil » et « ma range / la sienne » (porteur, 12/11)
RANGE_MARGIN = 1.0          # points : écart minimal à cette frontière (dérogation validée à la marge habituelle de 1,5 point)
RANGE_OPTIONS = ("ma range", "à peu près pareil", "la sienne")
RANGE_OPTIONS_L1 = ("mes mains possibles", "à peu près pareil", "ses mains possibles")     # niveau 1 : sans le mot « range »
RANGE_HAND = 'range'


@njit(parallel=True, cache=True)
def range_flop(flop, opp, CC):
    """(gain, total) par combinaison du héros contre la range opp sur ce flop, sommés sur les 1 081 turns et rivers"""
    used = np.zeros(52, np.bool_)
    for k in range(3): used[flop[k]] = True
    Wp = np.zeros((52, 1326)); Tp = np.zeros((52, 1326))
    for t in prange(52):
        if used[t]: continue
        b = np.zeros(5, np.int64); b[0] = flop[0]; b[1] = flop[1]; b[2] = flop[2]; b[3] = t
        for r in range(t + 1, 52):
            if used[r]: continue
            b[4] = r
            ranks = combo_ranks(b, CC); win, tie, tot = showdown(ranks, opp, CC)
            for c in range(1326):
                if ranks[c] >= 0 and tot[c] > 0:
                    Wp[t, c] += win[c] + 0.5 * (tie[c] - opp[c]); Tp[t, c] += tot[c] - opp[c]
    return Wp.sum(0), Tp.sum(0)


def preflop_range_equity(hero_w, opp_w):
    """équité exacte avant le flop de la range hero_w contre opp_w (poids par classe), cartes communes exclues"""
    from .allin import E as EQ169
    from .cards import DISJOINT
    J = np.asarray(hero_w, float)[:, None] * np.asarray(opp_w, float)[None, :] * DISJOINT
    return float((J * EQ169).sum() / J.sum())


STRONG_GAIN = 2            # main très forte : au moins deux catégories au-dessus du tableau seul (flop sans paire : double paire, brelan
                           # ou mieux ; flop pairé : brelan ou mieux, la double paire « paire du tableau + paire de poche » ne compte pas)


def is_strong(hand, board): return category(hand + board) >= category(board) + STRONG_GAIN


def strong_share(weights_combo, board):
    """part pondérée (dix-millièmes) des mains très fortes de la range sur ce flop (is_strong)"""
    s = t = 0.0
    for c in range(1326):
        w = weights_combo[c]
        if w <= 0 or CC[c, 0] in board or CC[c, 1] in board: continue
        t += w
        if is_strong([int(CC[c, 0]), int(CC[c, 1])], board): s += w
    return round(10000 * s / t)


@lru_cache(maxsize=1024)
def range_values(sc, board_s):
    """dict : équités de la range du héros avant / au flop (dix-millièmes) et parts des meilleures mains (héros, adversaire)"""
    _, _, mine, opp = scenario(sc); board = cards_of(board_s)
    pre = round(10000 * preflop_range_equity(mine, opp))
    cl = np.asarray(CLASS_OF); h, o = np.array(mine)[cl], np.array(opp)[cl]
    Wh, Th = range_flop(np.array(board, np.int64), o, CC)
    ok = Th > 0
    flop = round(10000 * float((h * Wh)[ok].sum() / (h * Th)[ok].sum()))
    return dict(pre=pre, flop=flop, strong_hero=strong_share(h, board), strong_villain=strong_share(o, board))


def range_answer(pre, flop):
    d = (flop - pre) / 100
    if d >= RANGE_STEP + RANGE_MARGIN: return 0
    if d <= -(RANGE_STEP + RANGE_MARGIN): return 2
    if abs(d) <= RANGE_STEP - RANGE_MARGIN: return 1
    return None


def range_spot_id(sc, level, board, pos): return f"eq:range_help:{sc}:L{level}:{''.join(name(c) for c in board)}:w2:n3:p{pos}"


def range_parse(sid):
    p = sid.split(':')
    if len(p) != 8 or p[0] != 'eq' or p[1] != 'range_help' or p[2] not in HELP_SCENARIOS or p[5] != 'w2' or p[6] != 'n3': raise ValueError
    board = cards_of(p[4])
    if len(board) != 3 or len({c >> 2 for c in board}) == 1: raise ValueError
    return dict(kind='range_help', topic=p[2], level=int(p[3][1:]), board=board, w=2, n=3, pos=int(p[7][1:]))


def range_built(q, hand_s):
    if hand_s != RANGE_HAND: raise ValueError
    v = range_values(q['topic'], ''.join(name(c) for c in q['board']))
    if range_answer(v['pre'], v['flop']) != q['pos']: raise ValueError
    return dict(q, hand=None, value=v['flop'], pre=v['pre'], values=v, options=list(RANGE_OPTIONS_L1 if q['level'] == 1 else RANGE_OPTIONS), correct=q['pos'])


def range_draw_one(level, rnd, avoid=frozenset(), topic=None):
    """la bonne réponse d'abord (à parts égales), puis un flop qui la donne ; après 12 essais, le premier flop valable"""
    want = rnd.randrange(3); fallback = None
    for k in range(30):
        if k >= 12 and fallback: return fallback
        sc = topic or rnd.choice(HELP_SCENARIOS)
        board = sorted(rnd.sample(range(52), 3), reverse=True)
        if len({c >> 2 for c in board}) == 1: continue
        v = range_values(sc, ''.join(name(c) for c in board)); a = range_answer(v['pre'], v['flop'])
        if a is None: continue
        if a == want: return range_spot_id(sc, level, board, a), RANGE_HAND
        fallback = fallback or (range_spot_id(sc, level, board, a), RANGE_HAND)
    return fallback


def _range_entry(who, label, w):
    from .cards import NAMES
    pct = round(100 * sum(x * (6 if len(h) == 2 else 4 if h[2] == 's' else 12) for h, x in zip(NAMES, w)) / 1326, 1)
    return dict(who=who, label_fr=f"{label} ({round(pct)} %)", pct=pct, hands={h: x for h, x in zip(NAMES, w) if x > 0})


def range_prompt(q, hand_s):
    n, hero, _, _ = scenario(q['topic']); bd = ' '.join(disp(c) for c in q['board'])
    ctx = (f"Heads-up à {n} BB : le SB complète (limp), tu checkes au BB" if hero == 'BB' else f"Heads-up à {n} BB : tu complètes au SB (limp), le BB checke")
    if q['level'] == 1: return f"{ctx}. Le flop est {bd}. Ce flop aide-t-il plus l'ensemble de tes mains possibles, ou l'ensemble des siennes ?"
    return f"{ctx}. Le flop est {bd}. Ce flop aide-t-il plus ta range ou la sienne ?"


def range_question_extra(q, hand_s):
    n, hero, mine, opp = scenario(q['topic'])
    me_lab, op_lab = (f"Toi, BB qui checke à {n} BB", f"SB qui complète (limp) à {n} BB") if hero == 'BB' else (f"Toi, SB qui complète (limp) à {n} BB", f"BB qui checke à {n} BB")
    return dict(street='flop', board=[name(c) for c in q['board']], board_display=[disp(c) for c in q['board']], hero_cards=None, hand_display=None,
                villain_cards=None, ranges=[_range_entry('hero', me_lab, mine), _range_entry('villain', op_lab, opp)], dead_cards=[])


def _pts(d): return f"{'+' if d >= 0 else '−'}{str(round(abs(d), 1)).replace('.', ',')} point{'s' if abs(d) >= 2 else ''}"


def range_correction(b, hand_s):
    from . import equity_quiz as E
    v = b['values']; bd = ' '.join(disp(c) for c in b['board']); d = (v['flop'] - v['pre']) / 100
    verdict = {0: "ce flop aide plus ta range", 1: "ce flop ne change presque rien au rapport de force", 2: "ce flop aide plus sa range"}[b['correct']]
    essential = f"Sur {bd}, l'équité de ta range passe de {E.pct_fr(v['pre'])} avant le flop à {E.pct_fr(v['flop'])} ({_pts(d)}) : {verdict}."
    method = ("Calcul : chaque main de ta range contre chaque main de la sienne, pondérées par leur fréquence dans la banque du solveur, sans carte commune ; "
              "avant le flop avec les équités exactes préflop, au flop sur les 1 081 turns et rivers possibles ; égalité pour moitié.")
    lines = [f"Sa range : {E.pct_fr(10000 - v['pre'])} avant le flop, {E.pct_fr(10000 - v['flop'])} au flop.",
             f"Mains très fortes sur ce flop (double paire ou mieux avec ses propres cartes ; brelan ou mieux si le flop est pairé) : ta range {E.pct_fr(v['strong_hero'])}, la sienne {E.pct_fr(v['strong_villain'])} (pour information, non noté).",
             f"Règle : « ma range » ou « la sienne » à partir de {str(RANGE_STEP + RANGE_MARGIN).replace('.0', '')} points d'écart, « à peu près pareil » sous {str(RANGE_STEP - RANGE_MARGIN).replace('.0', '')} point.",
             "Une range profite d'un flop quand ses mains fréquentes touchent ce tableau (hauteurs, couleurs, suites) plus souvent que celles de l'autre.",
             CAVEAT_MONEY]
    extra = dict(caveat_fr=CAVEAT_MONEY, delta_fr=_pts(d), value_bp=v['flop'], value_fr=E.pct_fr(v['flop']), preflop_bp=v['pre'], delta_bp=v['flop'] - v['pre'], villain_preflop_bp=10000 - v['pre'],
                 villain_flop_bp=10000 - v['flop'], strong_hero_bp=v['strong_hero'], strong_villain_bp=v['strong_villain'], board=[name(x) for x in b['board']],
                 street='flop', scenario=b['topic'], by_street=[dict(street='preflop', value_bp=v['pre']), dict(street='flop', value_bp=v['flop'])],
                 thresholds=dict(step=RANGE_STEP, margin=RANGE_MARGIN))
    return essential, method, lines, extra


# ================================================================== sorte « nut_help » : qui a le plus de mains très fortes sur ce flop ?
# Q2 des exercices de range (Plan, 12/11 ; seuils à confirmer par les coachs). Même pot limpé que range_help, pas de main du héros.
# Écart = part de mains très fortes de ta range − part de la sienne (points ; is_strong, poids de la banque, cartes du flop retirées).
# « ma range » si écart ≥ NUT_STEP + NUT_MARGIN, « la sienne » si écart ≤ −(NUT_STEP + NUT_MARGIN), « à peu près autant » si
# |écart| ≤ NUT_STEP − NUT_MARGIN ; sinon pas de question. Identifiant : eq:nut_help:huN_limp_{bb|sb}:L{niveau}:{flop}:w2:n3:p{rang}.
NUT_STEP = 2.0             # points (proposition du 12/11 validée avec Q1 par le porteur, à confirmer par les coachs)
NUT_MARGIN = 1.0
NUT_OPTIONS = ("ma range", "à peu près autant", "la sienne")
NUT_OPTIONS_L1 = ("moi", "à peu près autant", "lui")


@lru_cache(maxsize=1024)
def nut_values(sc, board_s):
    """(part de mains très fortes du héros, de l'adversaire) en dix-millièmes"""
    _, _, mine, opp = scenario(sc); board = cards_of(board_s); cl = np.asarray(CLASS_OF)
    return strong_share(np.array(mine)[cl], board), strong_share(np.array(opp)[cl], board)


def nut_answer(hero, vill):
    d = (hero - vill) / 100
    if d >= NUT_STEP + NUT_MARGIN: return 0
    if d <= -(NUT_STEP + NUT_MARGIN): return 2
    if abs(d) <= NUT_STEP - NUT_MARGIN: return 1
    return None


def nut_spot_id(sc, level, board, pos): return f"eq:nut_help:{sc}:L{level}:{''.join(name(c) for c in board)}:w2:n3:p{pos}"


def nut_parse(sid):
    p = sid.split(':')
    if len(p) != 8 or p[0] != 'eq' or p[1] != 'nut_help' or p[2] not in HELP_SCENARIOS or p[5] != 'w2' or p[6] != 'n3': raise ValueError
    board = cards_of(p[4])
    if len(board) != 3 or len({c >> 2 for c in board}) == 1: raise ValueError
    return dict(kind='nut_help', topic=p[2], level=int(p[3][1:]), board=board, w=2, n=3, pos=int(p[7][1:]))


def nut_built(q, hand_s):
    if hand_s != RANGE_HAND: raise ValueError
    h, v = nut_values(q['topic'], ''.join(name(c) for c in q['board']))
    if nut_answer(h, v) != q['pos']: raise ValueError
    return dict(q, hand=None, value=h, villain=v, options=list(NUT_OPTIONS_L1 if q['level'] == 1 else NUT_OPTIONS), correct=q['pos'])


def nut_draw_one(level, rnd, avoid=frozenset(), topic=None):
    """la bonne réponse d'abord (à parts égales), puis un flop qui la donne (calcul rapide : jusqu'à 300 essais)"""
    want = rnd.randrange(3); fallback = None
    for k in range(300):
        if k >= 200 and fallback: return fallback
        sc = topic or rnd.choice(HELP_SCENARIOS)
        board = sorted(rnd.sample(range(52), 3), reverse=True)
        if len({c >> 2 for c in board}) == 1: continue
        a = nut_answer(*nut_values(sc, ''.join(name(c) for c in board)))
        if a is None: continue
        if a == want: return nut_spot_id(sc, level, board, a), RANGE_HAND
        fallback = fallback or (nut_spot_id(sc, level, board, a), RANGE_HAND)
    return fallback


def nut_prompt(q, hand_s):
    n, hero, _, _ = scenario(q['topic']); bd = ' '.join(disp(c) for c in q['board'])
    ctx = (f"Heads-up à {n} BB : le SB complète (limp), tu checkes au BB" if hero == 'BB' else f"Heads-up à {n} BB : tu complètes au SB (limp), le BB checke")
    if q['level'] == 1: return f"{ctx}. Le flop est {bd}. Parmi toutes vos mains possibles, qui a le plus de mains très fortes sur ce flop ?"
    return f"{ctx}. Le flop est {bd}. Qui a le plus de mains très fortes sur ce flop ?"


def _premium_line(sc):
    """part des paires AA, KK, QQ que chaque range garde (lue dans la banque) : une range qui les relance avant le flop en a moins ici"""
    from .cards import NAMES
    _, hero, mine, opp = scenario(sc)
    share = lambda w: round(100 * sum(w[NAMES.index(h)] for h in ('AA', 'KK', 'QQ')) / 3)
    a, b = share(mine), share(opp)
    rest = " (les autres ont été relancées ou mises à tapis)" if min(a, b) < 100 else ""
    return (f"Avant le flop, ta range garde {a} % de ses AA, KK et QQ, la sienne {b} %{rest} : "
            "une range qui garde ses meilleures paires a plus de mains très fortes sur les flops.")


def nut_correction(b, hand_s):
    from . import equity_quiz as E
    h, v = b['value'], b['villain']; d = (h - v) / 100; bd = ' '.join(disp(c) for c in b['board'])
    verdict = {0: "ta range a plus de mains très fortes", 1: "les deux ranges en ont à peu près autant", 2: "sa range a plus de mains très fortes"}[b['correct']]
    essential = f"Sur {bd}, {E.pct_fr(h)} de ta range a une main très forte, contre {E.pct_fr(v)} de la sienne ({_pts(d)}) : {verdict}."
    method = ("Calcul : chaque main de chaque range, pondérée par sa fréquence dans la banque du solveur (sans les cartes du flop) ; main très forte = au moins "
              "deux catégories au-dessus du tableau seul : double paire, brelan ou mieux sur un flop sans paire, brelan ou mieux sur un flop pairé.")
    lines = [f"Règle : « ma range » ou « la sienne » à partir de {str(NUT_STEP + NUT_MARGIN).replace('.0', '')} points d'écart, « à peu près autant » sous {str(NUT_STEP - NUT_MARGIN).replace('.0', '')} point.",
             "Les mains très fortes sont celles qui peuvent miser gros sans crainte : la range qui en a le plus peut mettre plus de pression sur ce flop.",
             _premium_line(b['topic'])]
    extra = dict(caveat_fr=None, delta_fr=_pts(d), value_bp=h, value_fr=E.pct_fr(h), strong_hero_bp=h, strong_villain_bp=v, delta_bp=h - v, board=[name(x) for x in b['board']], street='flop',
                 scenario=b['topic'], thresholds=dict(step=NUT_STEP, margin=NUT_MARGIN, strong_gain=STRONG_GAIN))
    return essential, method, lines, extra


# ================================================================== aiguillage par sorte (utilisé par equity_quiz)
HANDLERS = {
    'outs': dict(parse=parse, built=built, draw=draw_one, prompt=prompt, extra=question_extra, correction=correction),
    'board_equity': dict(parse=eq_parse, built=eq_built, draw=eq_draw_one, prompt=eq_prompt, extra=eq_question_extra, correction=eq_correction),
    'flop_help': dict(parse=help_parse, built=help_built, draw=help_draw_one, prompt=help_prompt, extra=help_question_extra, correction=help_correction),
    'range_help': dict(parse=range_parse, built=range_built, draw=range_draw_one, prompt=range_prompt, extra=range_question_extra, correction=range_correction),
    'nut_help': dict(parse=nut_parse, built=nut_built, draw=nut_draw_one, prompt=nut_prompt, extra=range_question_extra, correction=nut_correction),
}
