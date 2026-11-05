"""Objectifs de la semaine (programme de travail, étape 3, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §6).

Trois objectifs par semaine (du lundi au dimanche, dans le fuseau du joueur), proposés à la première visite de la semaine puis
gardés tels quels (le joueur peut les modifier) :
  - régularité : nombre de jours d'entraînement (une série finie, séance ou jeu libre, ou une range) ;
  - précision : BB perdus pour 100 décisions de la semaine sous la cible, sur au moins MIN_DECISIONS décisions ;
  - ranges : nombre de ranges à RANGE_GOOD % ou plus de mains bien classées.
Cibles proposées : régularité 5, ranges 3 ; précision = moyenne des 4 dernières semaines (assez fournies) moins 10 %, sinon
DEFAULT_BB. Un objectif manqué la semaine d'avant est reconduit plus facile (jamais affiché en échec).
Bilan de la semaine passée : objectifs tenus, BB perdus des deux dernières semaines.
"""
import datetime
from . import progress, today as td

KINDS = ('days', 'precision', 'ranges')
DEFAULT = {'days': 5, 'ranges': 3}
DEFAULT_NEW = {'days': 3, 'ranges': 1}       # premier passage : cibles atteignables par un débutant
DEFAULT_BB = 20.0
MIN_DECISIONS = 30
RANGE_GOOD = 85
BOUNDS = {'days': (1, 7), 'ranges': (1, 10), 'precision': (2, 60)}
LABEL = {'days': "Jours d'entraînement", 'precision': 'BB perdus pour 100 décisions', 'ranges': f'Ranges à {RANGE_GOOD} % ou plus'}


def week_start(day):
    return day - datetime.timedelta(days=day.weekday())


def _n(x):
    return f'{x:g}'.replace('.', ',')


def _round_half(x):
    return max(BOUNDS['precision'][0], round(x * 2) / 2)


def week_values(rows, sessions, ranges_rows, start, tz):
    """valeurs d'une semaine : jours d'entraînement (séries finies, ranges), BB/100 et décisions, ranges réussies"""
    end = start + datetime.timedelta(days=7)
    inw = lambda iso: iso and start <= td.local_day(iso, tz) < end
    days = ({td.local_day(s['created_at'], tz) for s in sessions if s['answered'] >= s['size'] and inw(s['created_at'])}
            | {td.local_day(r['answered_at'], tz) for r in ranges_rows if inw(r['answered_at'])})
    wr = [r for r in rows if inw(r['answered_at'])]
    st = progress.compute(wr) if wr else {}
    good = sum(1 for r in ranges_rows if inw(r['answered_at']) and r['accuracy_pct'] >= RANGE_GOOD)
    return dict(days=len(days), day_set=days, precision=st.get('bb_per_100'), decisions=st.get('ev_questions', 0), ranges=good)


def done(kind, target, v):
    if kind == 'precision': return v['precision'] is not None and v['decisions'] >= MIN_DECISIONS and v['precision'] <= target
    return v[kind] >= target


def days_cap(v, day):
    """jours encore atteignables cette semaine : ceux déjà faits avant aujourd'hui, plus aujourd'hui et les jours qui restent"""
    before = sum(1 for d in v.get('day_set', ()) if d < day)
    return max(BOUNDS['days'][0], min(BOUNDS['days'][1], before + 7 - day.weekday()))


def propose(prev_targets, prev_values, history_bb, new=False):
    """cibles de la semaine : celles d'avant (plus faciles si manquées), précision tirée des 4 dernières semaines ; new : premier passage"""
    out = {}
    for k in ('days', 'ranges'):
        t = prev_targets.get(k, (DEFAULT_NEW if new else DEFAULT)[k])
        out[k] = max(BOUNDS[k][0], t - 1) if prev_values and k in prev_targets and not done(k, t, prev_values) else t
    bb = [x for x in history_bb if x is not None]
    base = _round_half(sum(bb) / len(bb) * 0.9) if bb else DEFAULT_BB
    if prev_values and 'precision' in prev_targets and not done('precision', prev_targets['precision'], prev_values):
        base = max(base, _round_half(prev_targets['precision'] * 1.1))
    out['precision'] = base
    return out


def view(targets, v, cap=None):
    """cap : plafond de la cible de jours (days_cap)"""
    items = []
    for k in KINDS:
        t = targets[k]
        if k == 'precision':
            cur = v['precision']
            text = (f"{_n(cur)} cette semaine ({v['decisions']} décisions) · cible : moins de {_n(t)}" if cur is not None
                    else f"cible : moins de {_n(t)}") + (f" (au moins {MIN_DECISIONS} décisions)" if v['decisions'] < MIN_DECISIONS else '')
            frac = 0 if cur is None else min(1.0, v['decisions'] / MIN_DECISIONS) * (1.0 if cur <= t else max(0.0, min(1.0, t / cur)))
        else:
            text = f"{v[k]} / {int(t)}"; frac = min(1.0, v[k] / t) if t else 1.0
        items.append(dict(kind=k, label_fr=LABEL[k], target=t, value=v[k] if k != 'precision' else v['precision'],
                          text_fr=text, progress=round(frac, 2), done=done(k, t, v), min=BOUNDS[k][0],
                          max=min(BOUNDS[k][1], cap) if k == 'days' and cap else BOUNDS[k][1]))
    return items
