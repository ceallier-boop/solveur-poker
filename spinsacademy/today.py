"""Séance du jour (programme de travail, étape 1, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md).

Une séance de 15 minutes, construite à partir de ce que l'application sait déjà :
  1. révision : les mains ratées arrivées à échéance (révision espacée) ; faite quand une série de révision est finie dans la
     journée, ou d'office s'il n'y a rien à revoir ;
  2. thème du jour : SERIES_PER_THEME séries de 5 sur le thème à travailler (diagnostic « À travailler maintenant »), sinon un
     thème du cycle THEMES selon le jour ; le thème choisi reste le même toute la journée (celui de la première série du jour) ;
  3. range du jour : un exercice « Construis ta range » sur la situation du thème.
La journée se compte dans le fuseau du joueur (décalage `tz` en minutes, envoyé par l'appareil). Série de jours : jours avec au
moins une série finie ou une range, tous modes confondus ; un jour manqué par période de 7 jours est pardonné, aujourd'hui sans
activité ne casse rien.
Neuvième test joueurs (29/10/2026) : le thème et la situation de la range sont fixés au premier affichage de la journée (table
daily_plan, `plan`) et ne changent plus ; un thème tiré du diagnostic doit avoir une situation et une profondeur ; la révision n'est
cochée que quand plus aucune main n'est due (ou après REVIEW_CAP séries de révision dans la journée).
"""
import datetime
import json

MINUTES = 15
SERIES_PER_THEME = 2
REVIEW_CAP = 4            # séries de révision dans la journée au-delà desquelles l'étape est cochée (mains qu'on ne peut plus servir)
THEMES = (       # cycle par défaut quand aucun thème n'est à travailler : du plus simple au plus fin
    ('Premier à parler, moins de 10 BB', dict(family='first_in', min_stack=0, max_stack=9.5)),
    ('Face à un tapis, moins de 10 BB', dict(family='vs_allin', min_stack=0, max_stack=9.5)),
    ('Premier à parler, 10 à 16 BB', dict(family='first_in', min_stack=9.5, max_stack=16.5)),
    ('Face à un limp, 10 à 16 BB', dict(family='vs_limp', min_stack=9.5, max_stack=16.5)),
    ('Face à une relance, 10 à 16 BB', dict(family='vs_raise', min_stack=9.5, max_stack=16.5)),
    ('Face à un tapis, 10 à 16 BB', dict(family='vs_allin', min_stack=9.5, max_stack=16.5)),
    ('Premier à parler, 17 à 25 BB', dict(family='first_in', min_stack=16.5, max_stack=99)),
    ('Face à une relance, 17 à 25 BB', dict(family='vs_raise', min_stack=16.5, max_stack=99)),
)
RANGE_KEYS = ('table', 'hero', 'family', 'min_stack', 'max_stack')


def local_day(iso, tz):
    """jour local (date) d'un horodatage ISO UTC, pour un décalage tz en minutes"""
    t = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00'))
    if t.tzinfo is None: t = t.replace(tzinfo=datetime.timezone.utc)
    return (t.astimezone(datetime.timezone.utc) + datetime.timedelta(minutes=tz)).date()


def streak(days, today):
    """jours de suite avec une activité ; un jour manqué par période de 7 jours est pardonné ; aujourd'hui peut être vide"""
    n, d, miss = 0, today if today in days else today - datetime.timedelta(days=1), None
    while True:
        if d in days: n += 1
        elif miss is None or (miss - d).days >= 7:
            if not any(x < d for x in days): break                     # plus rien avant : on s'arrête
            miss = d
        else: break
        d -= datetime.timedelta(days=1)
    return n


def theme_of_day(focus, nth, first_today, themes=THEMES):
    """(libellé, filtres) du thème du jour : celui de la première série du jour, sinon le diagnostic, sinon le cycle, pris dans
    l'ordre des jours de travail (un nouveau joueur commence par les tapis courts)"""
    if first_today: return first_today
    f = (focus or {}).get('filters') or {}
    if f.get('family') and f.get('max_stack') is not None:                 # un vrai thème : une situation et une tranche de tapis
        f = {k: v for k, v in f.items() if k != 'mode'}
        label = focus.get('label') or 'Ton thème à travailler'
        for m in ('GTO · ', 'Exploitant · '): label = label[len(m):] if label.startswith(m) else label   # le mode est déjà choisi
        return label, f
    return themes[nth % len(themes)]


def range_filters(f):
    """filtres de l'exercice de range tirés de ceux du thème (pas de famille « lecture du vilain »)"""
    out = {k: f[k] for k in RANGE_KEYS if f.get(k) is not None}
    if out.get('family') == 'read': out.pop('family')
    return out


def choose(sessions, ranges, focus, today, tz, themes=THEMES):
    """(libellé, filtres) du thème du jour, tel qu'il est fixé au premier affichage de la journée"""
    done_s = [s for s in sessions if s['answered'] >= s['size']]
    first_theme = next((s for s in sorted(sessions, key=lambda s: s['created_at'])
                        if s['plan'] == 'theme' and local_day(s['created_at'], tz) == today), None)
    first = None
    if first_theme:
        f = json.loads(first_theme['filters'] or '{}')
        first = (next((l for l, x in tuple(themes) + THEMES if x == f), None) or (focus or {}).get('label') or 'Ton thème du jour', f)
    active = {local_day(s['created_at'], tz) for s in done_s} | {local_day(r, tz) for r in ranges}
    return theme_of_day(focus, sum(1 for d in active if d < today), first, themes)


def _hour(iso, tz):
    t = datetime.datetime.fromisoformat(iso)
    t = (t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)).astimezone(datetime.timezone.utc) + datetime.timedelta(minutes=tz)
    return t.date(), f"{t.hour} h {t.minute:02d}" if t.minute else f"{t.hour} h"


def build(sessions, ranges, due, focus, today, tz, bb7=None, bb7_prev=None, themes=THEMES, level=None, plan=None, active=None,
          next_due=None, review_filters=None, played_before=None):
    """sessions : dicts {created_at, plan, filters (JSON), size, answered} du joueur dans ce mode ; ranges : horodatages des ranges ;
    due : mains à réviser maintenant ; focus : diagnostic de progress.compute ; plan : thème fixé pour la journée
    dict(theme_fr, filters, range_filters, range_spot) ; active : jours d'activité tous modes (série de jours) ;
    next_due : (horodatage, nombre) de la prochaine révision ; review_filters : profondeur du niveau pour compléter la révision"""
    done_s = [s for s in sessions if s['answered'] >= s['size']]
    today_s = [s for s in done_s if local_day(s['created_at'], tz) == today]
    if plan: label, f = plan['theme_fr'], plan['filters']
    else: label, f = choose(sessions, ranges, focus, today, tz, themes)
    if active is None: active = {local_day(s['created_at'], tz) for s in done_s} | {local_day(r, tz) for r in ranges}
    reviews = sum(1 for s in today_s if s['plan'] == 'review')
    themed = sum(1 for s in today_s if s['plan'] == 'theme')
    ranged = sum(1 for r in ranges if local_day(r, tz) == today)
    if due: rlabel = f"Révision : {due} main{'s' if due > 1 else ''} à revoir"
    elif next_due and next_due[0] and _hour(next_due[0], tz)[0] == today:
        n = next_due[1]; rlabel = f"Révision : rien à revoir pour l'instant ({n} main{'s' if n > 1 else ''} à partir de {_hour(next_due[0], tz)[1]})"
    else: rlabel = "Révision : rien à revoir aujourd'hui"
    rs = (plan or {}).get('range_filters', range_filters(f))
    steps = [
        dict(kind='review', done=due == 0 or reviews >= REVIEW_CAP, count=due, label_fr=rlabel, filters=review_filters or {}),
        dict(kind='theme', done=themed >= SERIES_PER_THEME, count=min(themed, SERIES_PER_THEME), total=SERIES_PER_THEME,
             label_fr=f"Thème : {label}", filters=f),
        dict(kind='range', done=ranged >= 1, label_fr="Range : la situation du thème", filters=rs, spot_id=(plan or {}).get('range_spot')),
    ]
    nxt = next((i for i, s in enumerate(steps) if not s['done']), None)
    return dict(minutes=MINUTES, date=today.isoformat(), steps=steps, next=nxt, done=nxt is None,
                started=(reviews > 0 or themed > 0 or ranged > 0) and nxt is not None,
                streak=streak(active, today), active_today=today in active, theme_fr=label, bb7=bb7, bb7_prev=bb7_prev, level=level,
                played_before=bool(done_s or ranges) if played_before is None else played_before)
