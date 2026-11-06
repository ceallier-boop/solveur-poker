"""Progression présentée en positif (chantier AU5, 06/11/2026 ; docs/produit/NOTE_PROGRES_POSITIFS_2026-11-06.md).

Indicateurs renvoyés seulement quand ils montrent un progrès net, jamais un chiffre négatif :
  1. BB récupérés : BB perdus pour 100 décisions des 7 derniers jours contre les 7 précédents, au moins BB_MIN décisions chiffrées
     dans chaque fenêtre ; gain d'au moins BB_GAIN pour 100, BB_REL de l'ancien chiffre et une erreur type ; après un changement
     de niveau dans les 14 jours (mode GTO), calcul limité aux questions du niveau actuel ;
  2. erreurs en moins : erreurs (verdict « erreur ») pour 100 décisions des 15 derniers jours contre les 15 précédents, au moins
     ERR_MIN décisions dans chaque fenêtre ; écart d'au moins ERR_GAIN pour 100, ERR_REL de l'ancien chiffre et z >= 1 ;
  3. mains rattrapées en révision : sur 7 jours, réussites qui font monter une main d'étape (règle de review.items) et mains
     acquises ; renvoyé dès 1 main acquise ou REVIEW_MIN réussites ; marqué `paid_feature` (frontière gratuit / payant P14) ;
  4. passage de niveau : passage automatique (player_level.promoted_at) dans les 7 derniers jours ;
  5. effort : décisions et jours d'entraînement des 7 derniers jours, toujours renvoyé (jamais d'écran vide).
Journées dans le fuseau de l'appareil ; « 7 derniers jours » = aujourd'hui et les 6 jours précédents.
"""
import datetime
import math
from . import levels, quiz, review
from .today import local_day

BB_DAYS, BB_MIN, BB_GAIN, BB_REL = 7, 50, 1.0, 0.10
ERR_DAYS, ERR_MIN, ERR_GAIN, ERR_REL = 15, 60, 2.0, 0.15
REVIEW_DAYS, REVIEW_MIN = 7, 3
LEVEL_DAYS, EFFORT_DAYS = 7, 7
ORDER = ('level_up', 'bb_recovered', 'fewer_errors', 'review_recovered')


def fr(x, d=1):
    """nombre à la française : virgule décimale, sans zéro inutile"""
    s = f"{x:.{d}f}".rstrip('0').rstrip('.') if d else str(round(x))
    return s.replace('.', ',')


def _plural(n, word, plural=None):
    return f"{fr(n, 0)} {word if n < 2 else (plural or word + 's')}"


def _windows(rows, day, tz, days):
    """(fenêtre récente, fenêtre précédente) de `days` jours locaux chacune"""
    d = lambda r: (day - local_day(r['answered_at'], tz)).days
    return [r for r in rows if 0 <= d(r) < days], [r for r in rows if days <= d(r) < 2 * days]


def _has_ev(r):
    sp = quiz.load(r['dataset_version'])[1][r['spot_id']]
    return not (sp.get('field') and sp['field']['type'] in ('identification', 'profil'))      # lecture du vilain : pas d'EV


def _regrets(rows):
    return [10 * round((r['regret_mbb'] or 0) / 10) for r in rows if _has_ev(r)]          # comme progress.compute


def _var(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1) if len(xs) > 1 else 0.0


def bb_recovered(rows, day, tz, level=None):
    """(gain ou None, manque ou None) ; level : niveau actuel si le calcul doit s'y limiter"""
    if level is not None:
        rows = [r for r in rows if levels.in_level(level, quiz.load(r['dataset_version'])[1][r['spot_id']])]
    now, before = (_regrets(w) for w in _windows(rows, day, tz, BB_DAYS))
    if len(now) < BB_MIN or len(before) < BB_MIN:
        return None, dict(kind='bb_recovered', window_days=BB_DAYS, decisions_now=len(now), decisions_before=len(before), needed=BB_MIN,
                          level_only=level is not None)
    b0, b1 = sum(now) / 10 / len(now), sum(before) / 10 / len(before)       # mbb -> BB pour 100 décisions
    gain = b1 - b0; se = 100 * math.sqrt(_var(now) / len(now) + _var(before) / len(before)) / 1000
    if gain < BB_GAIN or gain < BB_REL * b1 or gain < se: return None, None
    rec = gain * len(now) / 100
    return dict(kind='bb_recovered', window_days=BB_DAYS, bb_per_100_now=round(b0, 2), bb_per_100_before=round(b1, 2), gain_per_100=round(gain, 2),
                bb_recovered=round(rec, 1), decisions_now=len(now), decisions_before=len(before), level_only=level is not None,
                text_fr=(f"Environ {fr(rec)} BB récupérés sur tes {fr(len(now), 0)} décisions" + (" de ton niveau" if level is not None else '')
                         + " par rapport à la semaine passée.")), None     # AU2 : un seul chiffre de BB dans la phrase


def fewer_errors(rows, day, tz):
    now, before = _windows(rows, day, tz, ERR_DAYS)
    if len(now) < ERR_MIN or len(before) < ERR_MIN:
        return None, dict(kind='fewer_errors', window_days=ERR_DAYS, decisions_now=len(now), decisions_before=len(before), needed=ERR_MIN)
    k0, k1 = (sum(r['verdict'] == 'erreur' for r in w) for w in (now, before))
    e0, e1 = 100 * k0 / len(now), 100 * k1 / len(before); diff = e1 - e0
    p = (k0 + k1) / (len(now) + len(before)); se = 100 * math.sqrt(p * (1 - p) * (1 / len(now) + 1 / len(before)))
    if diff < ERR_GAIN or diff < ERR_REL * e1 or (se and diff / se < 1): return None, None
    return dict(kind='fewer_errors', window_days=ERR_DAYS, errors_per_100_now=round(e0, 1), errors_per_100_before=round(e1, 1), fewer_per_100=round(diff, 1),
                decisions_now=len(now), decisions_before=len(before),
                text_fr=f"{_plural(round(diff), 'erreur')} de moins pour 100 décisions qu'il y a {ERR_DAYS} jours."), None


def review_recovered(rows, day, tz):
    """réussites qui font monter une main d'étape et mains acquises dans les REVIEW_DAYS derniers jours (même règle que
    review.items : réussite le jour de l'échéance ou après)"""
    state = {}; ups = mastered = 0; n = len(review.INTERVALS_DAYS)
    for r in sorted(rows, key=lambda r: r['answered_at'] or ''):
        k = (r['spot_id'], r['hand']); at = review._t(r['answered_at'])
        if r['verdict'] != 'correct':
            state[k] = dict(stage=0, since=at); continue
        st = state.get(k)
        if not st or st['stage'] >= n: continue
        if review._day(at, tz) >= review._day(st['since'], tz) + datetime.timedelta(days=review.INTERVALS_DAYS[st['stage']]):
            st['stage'] += 1; st['since'] = at
            if 0 <= (day - review._day(at, tz)).days < REVIEW_DAYS:
                ups += 1; mastered += st['stage'] >= n
    if mastered < 1 and ups < REVIEW_MIN: return None
    text = f"{_plural(ups, 'main ratée réussie', 'mains ratées réussies')} en révision cette semaine"
    if mastered: text += f", dont {_plural(mastered, 'acquise')} pour de bon"
    return dict(kind='review_recovered', window_days=REVIEW_DAYS, stage_ups=ups, mastered=mastered, paid_feature=True, text_fr=text + '.')


def level_up(level_row, day, tz):
    at = level_row and level_row.get('promoted_at')
    if not at or not 0 <= (day - local_day(at, tz)).days < LEVEL_DAYS: return None
    to = level_row['level']; name = levels.LEVELS[to]['name']
    return dict(kind='level_up', from_level=to - 1, to_level=to, level_name_fr=name, at=at, text_fr=f"Niveau {to} atteint : {name}.")


def effort(rows, day, tz):
    now, _ = _windows(rows, day, tz, EFFORT_DAYS)
    days = len({local_day(r['answered_at'], tz) for r in now})
    text = (f"{_plural(len(now), 'décision')} sur {_plural(days, 'jour')} cette semaine." if now
            else "Ta première série de la semaine t'attend.")
    return dict(window_days=EFFORT_DAYS, decisions=len(now), active_days=days, text_fr=text)


def build(rows, mode, day, tz, level_row=None):
    """rows : réponses du joueur dans le mode (dataset_version, spot_id, hand, verdict, regret_mbb, answered_at), ordre quelconque ;
    level_row : ligne player_level (level, promoted_at, updated_at, onboarded_at) ou None ; un changement manuel se lit dans
    updated_at (différent d'onboarded_at, écrit à l'arrivée au niveau 1)"""
    rows = [r for r in rows if r.get('answered_at')]
    changed = None
    if mode == 'gto' and level_row and level_row.get('level', 1) < 4:          # changement de niveau dans les 14 jours
        manual = level_row.get('updated_at') if level_row.get('updated_at') != level_row.get('onboarded_at') else None   # pas l'arrivée au niveau 1
        last = max(level_row.get('promoted_at') or '', manual or '')
        if last and (day - local_day(last, tz)).days < 2 * BB_DAYS: changed = level_row['level']
    wins, short = [], []
    lv = level_up(level_row, day, tz)
    if lv: wins.append(lv)
    for w, s in (bb_recovered(rows, day, tz, changed), fewer_errors(rows, day, tz)):
        if w: wins.append(w)
        if s: short.append(s)
    rv = review_recovered(rows, day, tz)
    if rv: wins.append(rv)
    wins.sort(key=lambda w: ORDER.index(w['kind']))
    return dict(mode=mode, as_of=day.isoformat(), wins=wins, effort=effort(rows, day, tz), not_enough=short)
