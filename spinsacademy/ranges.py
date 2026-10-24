"""Exercice « Construis ta range » (chantier 2, 24/10/2026), mode GTO.

Le joueur voit une situation (table, tapis, actions précédentes) et colorie, sur la grille 13 × 13, les mains avec lesquelles
il joue une action donnée (« Quelles mains pousses-tu à tapis ? »). La correction compare sa range à la stratégie de référence,
main par main :
  - une main jouée au moins IN_MIN du temps est « à jouer », au plus OUT_MAX « à laisser », entre les deux « mixte » (les deux
    réponses sont acceptées) ;
  - le coût d'une main mal classée est son écart en EV avec le meilleur coup : jouée à tort, ce que coûte l'action ; oubliée,
    ce que coûte la meilleure des autres actions ;
  - la note résume la range entière, pondérée par le nombre de combinaisons et la probabilité d'atteindre la situation : part
    des combinaisons bien classées, et BB perdus pour 100 mains jouées dans cette situation.
Seules les mains qui atteignent vraiment la situation (REACH_MIN) sont à classer. Les mêmes données (TASK) servent à
l'API et à la démo autonome, qui refait la correction dans le navigateur avec la même règle (grade).
"""
import random
from functools import lru_cache
from . import grading, quiz
from .cards import NAMES, W

TARGET_ORDER = ('allin', 'call_allin', 'raise', 'call', 'limp')       # l'action qui dessine le mieux la range de la situation
SHARE_MIN, SHARE_MAX = 8, 85                                          # en % des mains : une range à dessiner, ni vide ni pleine
REACH_MIN = 0.05
IN_MIN, OUT_MAX = 0.75, 0.25
VERB_Q = {'allin': 'pousses-tu à tapis', 'call_allin': 'paies-tu le tapis', 'raise': 'relances-tu à {to} BB', 'call': 'paies-tu la relance',
          'limp': 'limpes-tu'}


def target_action(sp):
    """l'action à dessiner, ou None si la situation ne s'y prête pas"""
    if sp.get('field') or sp.get('_poor'): return None
    share = dict(zip([a['id'] for a in sp['actions']], quiz.range_grid(sp)['share_pct']))
    for t in TARGET_ORDER:
        a = next((a for a in sp['actions'] if a['type'] == t), None)
        if a and SHARE_MIN <= share[a['id']] <= SHARE_MAX: return a
    return None


def situation_fr(sp):
    """la situation, sans main : table, tapis, actions précédentes, place du joueur"""
    table = '3 joueurs' if sp['table'] == '3-handed' else 'Heads-up'
    stacks = ' / '.join(quiz.bb(x) for x in sp['stacks_bb']); pos = ' / '.join(sp['players'])
    hist = quiz.history_text(sp)
    return '\n'.join([f"{table}, tapis {stacks} BB ({pos})."] + [h + '.' for h in hist] + [f"Tu es au {sp['hero']}."])


def task(sp):
    """l'exercice d'une situation : énoncé, action, et pour chaque main à classer [fréquence, coût si jouée, coût si laissée,
    poids] ; None si la situation ne s'y prête pas"""
    a = target_action(sp)
    if not a: return None
    ids = [x['id'] for x in sp['actions']]; j = ids.index(a['id']); hands = {}
    for h in NAMES:
        x = sp['hands'][h]
        if x.get('reach', 0) < REACH_MIN or not x.get('freq') or h in sp.get('_unreliable', ()): continue
        ev = grading.reference_ev(sp, h)
        if ev is None or None in ev: continue
        top = max(ev); out_best = max(e for k, e in enumerate(ev) if k != j)
        hands[h] = [round(grading.reference_freq(sp, h)[j], 3), round(max(0.0, top - ev[j]), 4), round(max(0.0, top - out_best), 4),
                    round(W[NAMES.index(h)] * x['reach'], 5)]
    if len(hands) < 20: return None
    verb = VERB_Q[a['type']].format(to=quiz.bb1(a['to_bb']) if a.get('to_bb') else '')
    labels = {x['id']: quiz.action_label(sp, x) for x in sp['actions']}
    rule = quiz.rule_to_remember(sp, a['id'], labels)
    return dict(spot_id=sp['spot_id'], situation_fr=situation_fr(sp), question_fr=f"Avec quelles mains {verb} ?", action_id=a['id'],
                action_label=labels[a['id']], table=sp['table'], hero=sp['hero'], effective_stack_bb=sp['effective_stack_bb'],
                family=quiz.family(sp), hands=hands, rule_fr=rule)


def grade(t, selected):
    """correction d'une range : statut de chaque main, part des combinaisons bien classées, BB perdus pour 100 mains"""
    sel = set(selected); cells = {}; wt = good = lost = 0.0; extra = []; missing = []
    for h, (f, cost_in, cost_out, w) in t['hands'].items():
        played = h in sel
        ref = 'in' if f >= IN_MIN else 'out' if f <= OUT_MAX else 'mixed'
        cost = cost_in if played else cost_out
        if ref == 'mixed': status = 'mixed'; ok = True
        elif ref == 'in': status = 'ok_in' if played else 'missing'; ok = played
        else: status = 'extra' if played else 'ok_out'; ok = not played
        cells[h] = status; wt += w; good += w * ok; lost += w * cost
        if status == 'extra': extra.append((cost, h))
        if status == 'missing': missing.append((cost, h))
    ref_share = sum(w * f for f, _, _, w in t['hands'].values()) / wt if wt else 0     # même mesure que « À retenir » (part jouée)
    my_share = sum(t['hands'][h][3] for h in sel if h in t['hands']) / wt if wt else 0
    worst = sorted(extra + missing, reverse=True)[:5]
    return dict(spot_id=t['spot_id'], cells=cells, accuracy_pct=round(100 * good / wt, 1) if wt else 0.0,
                bb_per_100=round(100 * lost / wt, 2) if wt else 0.0, extra=len(extra), missing=len(missing),
                worst=[dict(hand=h, cost_bb=round(c, 2), kind=cells[h]) for c, h in worst],
                ref_share_pct=round(100 * ref_share), my_share_pct=round(100 * my_share), rule_fr=t['rule_fr'])


@lru_cache(maxsize=4)
def drawable(version):
    """situations qui se prêtent à l'exercice (calcul de quelques secondes, gardé en mémoire)"""
    return frozenset(sp['spot_id'] for sp in quiz.pool(version) if target_action(sp))


def pick(version, filters=None, seed=None, exclude=()):
    """une situation à dessiner, tirée selon sa fréquence réelle (comme les séries GTO), parmi celles qui s'y prêtent"""
    rnd = random.Random(seed)
    weights = quiz.situation_weights(version); ok = drawable(version)
    cands = [sp for sp in quiz.pool(version, filters) if sp['spot_id'] in ok and sp['spot_id'] not in exclude]
    rnd.shuffle(cands)
    for sp in sorted(cands, key=lambda s: -rnd.random() * weights.get((s['table'], quiz.stack_band(s), quiz.situation_key(s)), quiz.RARE_FLOOR)):
        t = task(sp)
        if t: return t
    return None
