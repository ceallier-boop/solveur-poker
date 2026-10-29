"""Séance du jour (programme de travail, étape 1, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md).

Une séance de 15 minutes, construite à partir de ce que l'application sait déjà :
  1. révision : les mains ratées arrivées à échéance (révision espacée) ; faite quand une série de révision est finie dans la
     journée, ou d'office s'il n'y a rien à revoir ;
  2. thème du jour : SERIES_PER_THEME séries de 5 sur le thème à travailler (diagnostic « À travailler maintenant »), sinon un
     thème du cycle THEMES selon le jour ; le thème choisi reste le même toute la journée (celui de la première série du jour) ;
  3. range du jour : un exercice « Construis ta range » sur la situation du thème.
La journée se compte dans le fuseau du joueur (décalage `tz` en minutes, envoyé par l'appareil). Série de jours : jours avec au
moins une série finie ou une range ; un jour manqué par période de 7 jours est pardonné, aujourd'hui sans activité ne casse rien.
"""
import datetime
import json

MINUTES = 15
SERIES_PER_THEME = 2
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


def theme_of_day(focus, nth, first_today):
    """(libellé, filtres) du thème du jour : celui de la première série du jour, sinon le diagnostic, sinon le cycle, pris dans
    l'ordre des jours de travail (un nouveau joueur commence par les tapis courts)"""
    if first_today: return first_today
    if focus and focus.get('filters'):
        f = {k: v for k, v in focus['filters'].items() if k != 'mode'}
        label = focus.get('label') or 'Ton thème à travailler'
        for m in ('GTO · ', 'Exploitant · '): label = label[len(m):] if label.startswith(m) else label   # le mode est déjà choisi
        return label, f
    return THEMES[nth % len(THEMES)]


def range_filters(f):
    """filtres de l'exercice de range tirés de ceux du thème (pas de famille « lecture du vilain »)"""
    out = {k: f[k] for k in RANGE_KEYS if f.get(k) is not None}
    if out.get('family') == 'read': out.pop('family')
    return out


def build(sessions, ranges, due, focus, today, tz, bb7=None, bb7_prev=None):
    """sessions : dicts {created_at, plan, filters (JSON), size, answered} du joueur dans ce mode ; ranges : horodatages des ranges ;
    due : mains à réviser aujourd'hui ; focus : diagnostic de progress.compute. Renvoie le plan du jour"""
    done_s = [s for s in sessions if s['answered'] >= s['size']]
    today_s = [s for s in done_s if local_day(s['created_at'], tz) == today]
    first_theme = next((s for s in sorted(sessions, key=lambda s: s['created_at'])
                        if s['plan'] == 'theme' and local_day(s['created_at'], tz) == today), None)
    first = None
    if first_theme:
        f = json.loads(first_theme['filters'] or '{}')
        first = (next((l for l, x in THEMES if x == f), None) or (focus or {}).get('label') or 'Ton thème du jour', f)
    active = {local_day(s['created_at'], tz) for s in done_s} | {local_day(r, tz) for r in ranges}
    label, f = theme_of_day(focus, sum(1 for d in active if d < today), first)
    reviewed = any(s['plan'] == 'review' for s in today_s)
    themed = sum(1 for s in today_s if s['plan'] == 'theme')
    ranged = sum(1 for r in ranges if local_day(r, tz) == today)
    steps = [
        dict(kind='review', done=reviewed or due == 0, count=due,
             label_fr=(f"Révision : {due} main{'s' if due > 1 else ''} à revoir" if due else "Révision : rien à revoir aujourd'hui")),
        dict(kind='theme', done=themed >= SERIES_PER_THEME, count=min(themed, SERIES_PER_THEME), total=SERIES_PER_THEME,
             label_fr=f"Thème : {label}", filters=f),
        dict(kind='range', done=ranged >= 1, label_fr="Range : la situation du thème", filters=range_filters(f)),
    ]
    nxt = next((i for i, s in enumerate(steps) if not s['done']), None)
    return dict(minutes=MINUTES, date=today.isoformat(), steps=steps, next=nxt, done=nxt is None,
                started=(reviewed or themed > 0 or ranged > 0) and nxt is not None,
                streak=streak(active, today), active_today=today in active, theme_fr=label, bb7=bb7, bb7_prev=bb7_prev)
