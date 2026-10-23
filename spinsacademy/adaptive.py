"""Exercices adaptatifs (cahier des charges §9.3) : composer une série selon les réponses passées du joueur.

Règle, volontairement simple et affichée au joueur :
  - thème = famille de décision x position x profondeur, dans le mode de la série (GTO ou exploitant) ;
  - difficulté d'un thème = (erreurs + 0,5 x imprécisions + 1) / (réponses + 3) : taux lissé, qui ne conclut pas sur
    quelques réponses ;
  - thème faible : au moins MIN_ANSWERS réponses, au moins MIN_ERRORS erreurs et une difficulté >= WEAK_RATE ;
  - thème acquis : au moins MASTERED_ANSWERS réponses et une difficulté < MASTERED_RATE ;
  - une série : WEAK_SHARE de questions sur les thèmes faibles (tirés au prorata de leur difficulté), REVIEW_SHARE de
    révision (thèmes acquis les moins récemment travaillés), le reste en découverte (thèmes jamais travaillés, sinon
    les moins travaillés) ;
  - sans thème faible, la série est tirée normalement.
Seules les réponses postérieures à la dernière réinitialisation comptent. La sélection ne change jamais la correction.
"""
import random
from . import progress, quiz

MIN_ANSWERS = 3
MIN_ERRORS = 2
WEAK_RATE = 0.40
MASTERED_ANSWERS = 5
MASTERED_RATE = 0.25
WEAK_SHARE = 0.6
REVIEW_SHARE = 0.2
DEPTH_FR = {k: l for k, l, *_ in progress.DEPTHS}
RULE_FR = (f"Un thème (situation, position, profondeur) revient plus souvent quand tu y fais au moins {MIN_ANSWERS} réponses dont {MIN_ERRORS} erreurs. "
           f"Une série adaptée contient environ {round(100 * WEAK_SHARE)} % de questions sur tes thèmes fragiles, {round(100 * REVIEW_SHARE)} % de révision "
           f"et le reste en découverte. La correction ne change pas.")   # A8 : sans « taux lissé »
PURPOSE_FR = {'weak': 'Thème à retravailler', 'review': 'Révision', 'discovery': 'Découverte'}


def theme_of(sp):
    return (quiz.family(sp), sp['hero'], progress.depth_of(sp['effective_stack_bb']))


def label(t):
    return f"{progress.FAMILY_FR[t[0]]} · {t[1]} · {DEPTH_FR[t[2]]}"


def difficulty(s):
    return (s['errors'] + 0.5 * s['imprecisions'] + 1) / (s['answers'] + 3)


def theme_stats(rows):
    """rows : réponses du joueur dans le mode (dicts avec dataset_version, spot_id, verdict, answered_at)"""
    out = {}
    for r in rows:
        _, spots = quiz.load(r['dataset_version']); sp = spots.get(r['spot_id'])
        if sp is None: continue
        s = out.setdefault(theme_of(sp), dict(answers=0, errors=0, imprecisions=0, last=None))
        s['answers'] += 1; s['errors'] += r['verdict'] == 'erreur'; s['imprecisions'] += r['verdict'] == 'imprécision'
        s['last'] = max(s['last'] or '', r['answered_at'] or '')
    return out


def plan(rows, available, size, seed=None):
    """composition d'une série : dict(active, rule_fr, reason_fr, slots=[dict(kind, theme)] ou None, weak, review)"""
    st = theme_stats(rows); rnd = random.Random(seed)
    weak = sorted((t for t, s in st.items() if s['answers'] >= MIN_ANSWERS and s['errors'] >= MIN_ERRORS and difficulty(s) >= WEAK_RATE and t in available),
                  key=lambda t: -difficulty(st[t]))
    review = sorted((t for t, s in st.items() if s['answers'] >= MASTERED_ANSWERS and difficulty(s) < MASTERED_RATE and t in available),
                    key=lambda t: st[t]['last'] or '')
    desc = lambda t: dict(theme=list(t), label_fr=label(t), answers=st[t]['answers'], errors=st[t]['errors'], difficulty_pct=round(100 * difficulty(st[t])))
    info = dict(rule_fr=RULE_FR, weak=[desc(t) for t in weak], review=[desc(t) for t in review])
    if not weak:
        return dict(info, active=False, slots=None,
                    reason_fr=f"Pas encore de thème à retravailler : il faut au moins {MIN_ANSWERS} réponses et {MIN_ERRORS} erreurs sur un même thème. Série tirée normalement.")
    n_weak = max(1, round(size * WEAK_SHARE)); n_review = min(len(review), round(size * REVIEW_SHARE)) if review else 0
    n_disc = size - n_weak - n_review
    slots = [dict(kind='weak', theme=t) for t in rnd.choices(weak, weights=[difficulty(st[t]) for t in weak], k=n_weak)]
    slots += [dict(kind='review', theme=t) for t in review[:n_review]]
    fresh = [t for t in available if t not in st]; rnd.shuffle(fresh)
    seen = sorted((t for t in available if t in st and t not in weak), key=lambda t: st[t]['answers'])
    disc = (fresh + seen)[:n_disc]
    slots += [dict(kind='discovery', theme=t) for t in disc] + [dict(kind='discovery', theme=None)] * (n_disc - len(disc))
    rnd.shuffle(slots)
    return dict(info, active=True, slots=slots,
                reason_fr=f"Série adaptée : {n_weak} question(s) sur tes thèmes à retravailler, {n_review} de révision, {n_disc} de découverte.")
