"""Exercice « Construis ta range » (chantier 2, 24/10/2026, corrigé après le test joueurs du même jour), mode GTO.

Le joueur voit une situation (table, tapis, actions précédentes) et colorie, sur la grille 13 × 13, les mains avec lesquelles
il joue une action donnée. La question dit ce que font les autres mains (« les autres limpent ou se couchent »), puisque la
référence n'est pas toujours du push/fold. La correction compare sa range à la stratégie de référence, main par main :
  - une main jouée au moins IN_MIN du temps est « à jouer », au plus OUT_MAX « à laisser », entre les deux « mixte » (les deux
    réponses sont acceptées). Aucune main en jeu n'est grisée : une seule version de chaque situation est servie, la marque
    des mains dont la référence changeait d'un arbre à l'autre ne s'applique plus ici ;
  - le coût d'une main mal classée est son écart en EV avec le meilleur coup ; sous CLOSE_BB, l'erreur ne coûte rien de
    mesurable et compte comme mixte ;
  - chaque erreur dit le coup de référence de la main (« la référence la limpe ») ;
  - un seul calcul de part de range partout (combinaisons, pondérées par la probabilité d'arriver à la situation) : ta range,
    celle de la référence et la règle « À retenir » utilisent le même ;
  - note : part des combinaisons bien classées, et BB perdus pour 100 mains jouées dans cette situation.
Seules les mains qui atteignent vraiment la situation (REACH_MIN) sont à classer ; au premier coup, toutes. Les mêmes données
servent à l'API et à la démo autonome, qui refait la correction dans le navigateur avec la même règle (grade).
"""
import random
from functools import lru_cache
from . import grading, quiz
from .cards import NAMES, W

TARGET_ORDER = ('allin', 'call_allin', 'raise', 'call', 'limp')       # l'action qui dessine le mieux la range de la situation
SHARE_MIN, SHARE_MAX = 8, 85                                          # en % des mains : une range à dessiner, ni vide ni pleine
REACH_MIN = 0.05
IN_MIN, OUT_MAX = 0.75, 0.25
CLOSE_BB = 0.01
VERB_Q = {'allin': 'pousses-tu à tapis', 'call_allin': 'paies-tu le tapis', 'raise': 'relances-tu à {to} BB', 'call': 'paies-tu la relance',
          'limp': 'limpes-tu'}
VERB_ON = {'allin': 'on pousse à tapis', 'call_allin': 'on paie le tapis', 'raise': 'on relance', 'call': 'on paie', 'limp': 'on limpe'}
OTHERS = {'fold': 'se couchent', 'check': 'checkent', 'limp': 'limpent', 'call': 'paient', 'call_allin': 'paient le tapis',
          'raise': 'relancent à {to} BB', 'allin': 'partent à tapis'}
REF_FR = {'fold': 'la couche', 'check': 'la checke', 'limp': 'la limpe', 'call': 'la paie', 'call_allin': 'paie le tapis',
          'raise': 'la relance à {to} BB', 'allin': 'la pousse à tapis'}


def _fmt(table, a):
    return table[a['type']].format(to=quiz.bb1(a['to_bb']) if a.get('to_bb') else '')


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
    poids, instable (0/1), coup de référence] ; None si la situation ne s'y prête pas"""
    a = target_action(sp)
    if not a: return None
    acts = sp['actions']; ids = [x['id'] for x in acts]; j = ids.index(a['id']); hands = {}
    for h in NAMES:
        x = sp['hands'][h]
        if x.get('reach', 0) < REACH_MIN or not x.get('freq'): continue
        ev = grading.reference_ev(sp, h)
        if ev is None or None in ev: continue
        f = grading.reference_freq(sp, h); top = max(ev); out_best = max(e for k, e in enumerate(ev) if k != j)
        main = max(range(len(acts)), key=lambda k: f[k])                     # le coup le plus fréquent de la référence
        hands[h] = [round(f[j], 3), round(max(0.0, top - ev[j]), 4), round(max(0.0, top - out_best), 4),
                    round(W[NAMES.index(h)] * x['reach'], 5), 0, _fmt(REF_FR, acts[main])]
    if len(hands) < 20: return None
    share = quiz.range_grid(sp)['share_pct']
    others = [_fmt(OTHERS, x) for k, x in enumerate(acts) if k != j and share[k] >= 1]
    rest = (f"Les autres mains {', '.join(others[:-1])} ou {others[-1]}." if len(others) > 1 else f"Les autres mains {others[0]}." if others else '')
    where = (f"au {sp['hero']} {quiz.SITUATION_FR[quiz.family(sp)]}, avec {quiz.bb(quiz.hero_effective(sp))} BB de tapis"
             + (' (heads-up)' if sp['table'] == 'heads-up' else ''))
    return dict(spot_id=sp['spot_id'], situation_fr=situation_fr(sp), question_fr=f"Avec quelles mains {_fmt(VERB_Q, a)} ?", others_fr=rest,
                action_id=a['id'], action_type=a['type'], table=sp['table'], hero=sp['hero'], effective_stack_bb=sp['effective_stack_bb'],
                family=quiz.family(sp), band=quiz.stack_band(sp), hands=hands, where_fr=where, verb_fr=VERB_ON[a['type']])


def grade(t, selected):
    """correction d'une range : statut de chaque main, part des combinaisons bien classées, BB perdus pour 100 mains"""
    sel = set(selected); cells = {}; wt = good = lost = 0.0; errs = []
    for h, (f, cost_in, cost_out, w, unstable, ref_fr) in t['hands'].items():
        played = h in sel; cost = cost_in if played else cost_out
        ref = 'mixed' if unstable else 'in' if f >= IN_MIN else 'out' if f <= OUT_MAX else 'mixed'
        if ref == 'mixed': status = 'mixed'; ok = True
        elif ref == 'in': status = 'ok_in' if played else 'missing'; ok = played
        else: status = 'extra' if played else 'ok_out'; ok = not played
        if status in ('extra', 'missing') and cost < CLOSE_BB: status = 'mixed'; ok = True     # erreur sans coût mesurable
        cells[h] = status; wt += w; good += w * ok; lost += w * cost
        if status in ('extra', 'missing'): errs.append((cost, h))
    ref_share = round(100 * sum(w * x[0] for x in t['hands'].values() for w in [x[3]]) / wt) if wt else 0
    my_share = round(100 * sum(t['hands'][h][3] for h in sel if h in t['hands']) / wt) if wt else 0
    worst = sorted(errs, reverse=True)[:5]
    return dict(spot_id=t['spot_id'], cells=cells, accuracy_pct=round(100 * good / wt, 1) if wt else 0.0,
                bb_per_100=round(100 * lost / wt, 2) if wt else 0.0, extra=sum(1 for s in cells.values() if s == 'extra'),
                missing=sum(1 for s in cells.values() if s == 'missing'),
                worst=[dict(hand=h, cost_bb=round(c, 2), kind=cells[h], ref_fr=t['hands'][h][5]) for c, h in worst],
                ref_share_pct=ref_share, my_share_pct=my_share,
                rule_fr=f"À retenir : {t['where_fr']}, {t['verb_fr']} avec environ {ref_share} % des mains.")


@lru_cache(maxsize=4)
def drawable(version):
    """situations qui se prêtent à l'exercice (calcul de quelques secondes, gardé en mémoire)"""
    return frozenset(sp['spot_id'] for sp in quiz.pool(version) if target_action(sp))


def pick(version, filters=None, seed=None, exclude=()):
    """une situation à dessiner, jamais une des dernières (exclude). Pour varier : famille de décision puis tranche de tapis
    tirées à parts égales, puis situation selon sa fréquence réelle"""
    rnd = random.Random(seed)
    weights = quiz.situation_weights(version); ok = drawable(version)
    cands = [sp for sp in quiz.pool(version, filters) if sp['spot_id'] in ok and sp['spot_id'] not in exclude]
    if not cands: cands = [sp for sp in quiz.pool(version, filters) if sp['spot_id'] in ok]          # tout vu : on recommence
    while cands:
        fam = rnd.choice(sorted({quiz.family(sp) for sp in cands})); c = [sp for sp in cands if quiz.family(sp) == fam]
        band = rnd.choice(sorted({quiz.stack_band(sp) for sp in c})); c = [sp for sp in c if quiz.stack_band(sp) == band]
        w = [weights.get((sp['table'], band, quiz.situation_key(sp)), quiz.RARE_FLOOR) for sp in c]
        sp = rnd.choices(c, w)[0]; t = task(sp)
        if t: return t
        cands.remove(sp)
    return None
