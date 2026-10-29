"""Défis (programme de travail, étape 5, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §7 et §16).

Courts et facultatifs, ils donnent du rythme sans changer la correction ni la progression :
  - défi du jour : les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date UTC), au chrono 15 s ; une seule
    tentative par jour UTC, tous modes confondus, comptée dès la création de la série (une question laissée sans réponse
    compte comme fausse) ; réussi à DAILY_WIN bonnes réponses ou plus ;
  - série parfaite : 5 bonnes réponses sur 5 sur le thème de la séance du jour du joueur ;
  - sous pression (semaine) : une série au chrono 8 s sans coup joué au temps, à PRESSURE_WIN bonnes réponses ou plus ;
  - range au cordeau (semaine) : une range à moins de RANGE_BB BB perdus pour 100 mains et à RANGE_ACC % de justesse ou plus ;
  - lecteur de vilain (semaine, mode exploitant) : 5 lectures justes sur 5, dont au moins READER_PROFILES « Quelle pastille ? » ;
  - semaine pleine (mois) : 7 jours d'entraînement dans le mois, comptés comme la série de jours (un jour manqué par période
    de 7 jours est pardonné).
Une série de défi est marquée en base (sessions.plan = « challenge_<défi> ») ; réussites et tentatives forment « Mes défis ».
Corrections du neuvième test joueurs (29/10/2026) : tentative unique du défi du jour, série parfaite sur le thème de la
séance, semaine pleine alignée sur la série de jours, seuils relevés, tentatives visibles.
"""
import datetime
from . import today as td

DAILY_WIN = 4
PRESSURE_WIN = 4
RANGE_BB = 2.0
RANGE_ACC = 85
READER_PROFILES = 2
HISTORY_DAYS = 60
SERIES = {'daily': 'challenge_daily', 'perfect': 'challenge_perfect', 'pressure': 'challenge_pressure', 'reader': 'challenge_reader'}
INFO = {
    'daily': ('Défi du jour', f"Les mêmes 5 mains pour tous aujourd'hui, au chrono 15 s. Réussi à {DAILY_WIN} sur 5. Une seule tentative par jour, tous modes confondus : elle compte dès que tu la lances."),
    'perfect': ('Série parfaite', "5 bonnes réponses sur 5 sur le thème de ta séance du jour."),
    'pressure': ('Sous pression', f"Une série au chrono 8 s sans coup joué au temps, à {PRESSURE_WIN} sur 5 ou plus."),
    'range': ('Range au cordeau', f"Une range à moins de {str(RANGE_BB).replace('.0', '').replace('.', ',')} BB perdus pour 100 mains, avec au moins {RANGE_ACC} % de justesse."),
    'reader': ('Lecteur de vilain', f"5 lectures justes sur 5, dont au moins {READER_PROFILES} « Quelle pastille ? »."),
    'full_week': ('Semaine pleine', "7 jours d'entraînement dans le mois, comptés comme ta série de jours : un jour manqué par semaine est pardonné."),
}
NEXT_DAILY_FR = 'Nouveau défi demain.'


def daily_seed(utc_day):
    return int(utc_day.strftime('%Y%m%d'))


def _result(s):
    left = s['size'] - s.get('answered', s['size'])
    return (f"{s['correct']}/{s['size']}" + (f", {s['timeouts']} au temps" if s.get('timeouts') else '')
            + (f", {left} sans réponse" if left > 0 else ''))


def won(kind, s):
    if kind == 'daily': return s['correct'] >= DAILY_WIN
    if kind == 'perfect': return s['correct'] == s['size']
    if kind == 'pressure': return s['timeouts'] == 0 and s['correct'] >= PRESSURE_WIN
    if kind == 'reader': return s['correct'] == s['size']
    return False


def range_won(r):
    return r['bb_per_100'] < RANGE_BB and r['accuracy_pct'] >= RANGE_ACC


def full_week(active, day):
    """meilleure série de jours du mois de `day`, avec la règle de la série de jours (today.streak : un jour manqué par période
    de 7 jours est pardonné), en ne comptant que les jours du mois"""
    first = day.replace(day=1); month = {d for d in active if first <= d <= day}; best = 0; d = first
    while d <= day:
        best = max(best, td.streak(month, d)); d += datetime.timedelta(days=1)
    return best


def build(sessions, daily_sessions, ranges_rows, active, day, tz, mode, utc_day, theme):
    """sessions : dicts {created_at, plan, size, answered, correct, timeouts} du mode (séries finies ou non) ; daily_sessions :
    séries du défi du jour, tous modes ; ranges_rows : {answered_at, accuracy_pct, bb_per_100} ; active : jours locaux avec
    activité ; theme : (libellé, filtres) du thème de la séance du jour. Renvoie les défis du jour, de la semaine, du mois et
    l'historique (réussites et tentatives)"""
    start = day - datetime.timedelta(days=day.weekday())
    done = [s for s in sessions if s['answered'] >= s['size']]
    of = lambda kind: sorted([s for s in done if s['plan'] == SERIES[kind]], key=lambda s: s['created_at'])
    today_ = lambda xs: [s for s in xs if td.local_day(s['created_at'], tz) == day]
    week_ = lambda xs: [s for s in xs if start <= td.local_day(s['created_at'], tz) <= day]
    utc = lambda s: td.local_day(s['created_at'], 0)
    dailies = sorted([s for s in daily_sessions if s['plan'] == SERIES['daily']], key=lambda s: s['created_at'])

    def card(kind, attempts, window, action):
        title, rule = INFO[kind]
        best = max(attempts, key=lambda s: (won(kind, s), s['correct'])) if attempts else None
        status = 'won' if best is not None and won(kind, best) else 'tried' if attempts else 'todo'
        return dict(kind=kind, window=window, title_fr=title, rule_fr=rule, status=status, result_fr=_result(best) if best else None, action=action)

    first = next((s for s in dailies if utc(s) == utc_day), None)           # la tentative du jour, même abandonnée
    d_card = card('daily', [first] if first else [], 'jour', None if first else dict(type='challenge', challenge='daily', chrono=15))
    if first: d_card['next_fr'] = NEXT_DAILY_FR
    daily = [d_card, dict(card('perfect', today_(of('perfect')), 'jour', dict(type='challenge', challenge='perfect')), theme_fr=theme[0])]
    weekly = [card('pressure', week_(of('pressure')), 'semaine', dict(type='challenge', challenge='pressure', chrono=8))]
    rw = [r for r in ranges_rows if r['answered_at'] and start <= td.local_day(r['answered_at'], tz) <= day]
    best_r = max(rw, key=lambda r: (range_won(r), -r['bb_per_100'], r['accuracy_pct']), default=None)
    title, rule = INFO['range']
    weekly.append(dict(kind='range', window='semaine', title_fr=title, rule_fr=rule,
                       status='won' if best_r and range_won(best_r) else 'tried' if rw else 'todo',
                       result_fr=(f"meilleure : {best_r['bb_per_100']:g} BB pour 100, {best_r['accuracy_pct']:g} % de justesse".replace('.', ',') if best_r else None),
                       action=dict(type='range')))
    if mode == 'exploit':
        weekly.append(card('reader', week_(of('reader')), 'semaine', dict(type='challenge', challenge='reader')))
    run = full_week(active, day); title, rule = INFO['full_week']
    monthly = [dict(kind='full_week', window='mois', title_fr=title, rule_fr=rule, status='won' if run >= 7 else 'tried' if run else 'todo',
                    result_fr=f"meilleure série du mois : {run} jour{'s' if run > 1 else ''}", action=None)]
    hist = []                                                       # une ligne par défi et par jour : la meilleure tentative
    for d in sorted({utc(s) for s in dailies}):
        s = next(x for x in dailies if utc(x) == d)
        if (utc_day - d).days <= HISTORY_DAYS:
            hist.append(dict(kind='daily', title_fr=INFO['daily'][0], date=d.isoformat(), result_fr=_result(s), won=won('daily', s)))
    for kind in ('perfect', 'pressure', 'reader'):
        by = {}
        for s in of(kind): by.setdefault(td.local_day(s['created_at'], tz), []).append(s)
        for d, xs in by.items():
            if (day - d).days > HISTORY_DAYS: continue
            b = max(xs, key=lambda s: (won(kind, s), s['correct']))
            hist.append(dict(kind=kind, title_fr=INFO[kind][0], date=d.isoformat(), result_fr=_result(b), won=won(kind, b)))
    for r in ranges_rows:                                           # toute range n'est pas une tentative : seules les réussites
        if r['answered_at'] and range_won(r) and (day - td.local_day(r['answered_at'], tz)).days <= HISTORY_DAYS:
            hist.append(dict(kind='range', title_fr=INFO['range'][0], date=td.local_day(r['answered_at'], tz).isoformat(),
                             result_fr=f"{r['bb_per_100']:g} BB pour 100, {r['accuracy_pct']:g} % de justesse".replace('.', ','), won=True))
    return dict(daily=daily, weekly=weekly, monthly=monthly, history=sorted(hist, key=lambda h: h['date'], reverse=True)[:30])
