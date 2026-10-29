"""Défis (programme de travail, étape 5, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §7).

Courts et facultatifs, ils donnent du rythme sans changer la correction ni la progression :
  - défi du jour : les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date UTC), au chrono 15 s ; seule la
    première tentative du jour compte ; réussi à DAILY_WIN bonnes réponses ou plus ;
  - série parfaite : 5 bonnes réponses sur 5 sur le thème du jour (le même pour tous, tournant avec la date) ;
  - sous pression (semaine) : une série au chrono 8 s sans coup joué au temps, à PRESSURE_WIN bonnes réponses ou plus ;
  - range au cordeau (semaine) : une range à moins de RANGE_BB BB perdus pour 100 mains ;
  - lecteur de vilain (semaine, mode exploitant) : 5 lectures justes sur 5 (« Défaut du vilain », « Quelle pastille ? ») ;
  - semaine pleine (mois) : 7 jours de suite d'activité dans le mois.
Une série de défi est marquée en base (sessions.plan = « challenge_<défi> ») ; les réussites forment l'historique « Mes défis ».
"""
import datetime
from . import today as td

DAILY_WIN = 4
PRESSURE_WIN = 3
RANGE_BB = 2.0
HISTORY_DAYS = 60
SERIES = {'daily': 'challenge_daily', 'perfect': 'challenge_perfect', 'pressure': 'challenge_pressure', 'reader': 'challenge_reader'}
INFO = {
    'daily': ('Défi du jour', f"Les mêmes 5 mains pour tous aujourd'hui, au chrono 15 s. Réussi à {DAILY_WIN} sur 5. Seule ta première tentative compte."),
    'perfect': ('Série parfaite', "5 bonnes réponses sur 5 sur le thème du jour."),
    'pressure': ('Sous pression', f"Une série au chrono 8 s sans coup joué au temps, à {PRESSURE_WIN} sur 5 ou plus."),
    'range': ('Range au cordeau', f"Une range à moins de {str(RANGE_BB).replace('.0', '').replace('.', ',')} BB perdus pour 100 mains."),
    'reader': ('Lecteur de vilain', "5 lectures justes sur 5 : défaut du vilain ou pastille."),
    'full_week': ('Semaine pleine', "7 jours de suite d'entraînement dans le mois."),
}


def daily_seed(utc_day):
    return int(utc_day.strftime('%Y%m%d'))


def perfect_theme(utc_day):
    """(libellé, filtres) du thème de la série parfaite : le même pour tous, tournant avec la date"""
    return td.THEMES[utc_day.toordinal() % len(td.THEMES)]


def _result(s):
    return f"{s['correct']}/{s['size']}" + (f", {s['timeouts']} au temps" if s.get('timeouts') else '')


def won(kind, s):
    if kind == 'daily': return s['correct'] >= DAILY_WIN
    if kind == 'perfect': return s['correct'] == s['size']
    if kind == 'pressure': return s['timeouts'] == 0 and s['correct'] >= PRESSURE_WIN
    if kind == 'reader': return s['correct'] == s['size']
    return False


def full_week(active, day):
    """7 jours de suite d'activité dans le mois de `day` (jours locaux)"""
    run, best = 0, 0; d = day.replace(day=1)
    while d <= day:
        run = run + 1 if d in active else 0; best = max(best, run); d += datetime.timedelta(days=1)
    return best


def build(sessions, ranges_rows, active, day, tz, mode, utc_day):
    """sessions : dicts {created_at, plan, size, answered, correct, timeouts} (séries finies ou non) ; ranges_rows : {answered_at,
    bb_per_100} ; active : jours locaux avec activité. Renvoie les défis du jour, de la semaine, du mois et l'historique"""
    start = day - datetime.timedelta(days=day.weekday())
    done = [s for s in sessions if s['answered'] >= s['size']]
    of = lambda kind: sorted([s for s in done if s['plan'] == SERIES[kind]], key=lambda s: s['created_at'])
    today_ = lambda xs: [s for s in xs if td.local_day(s['created_at'], tz) == day]
    week_ = lambda xs: [s for s in xs if start <= td.local_day(s['created_at'], tz) <= day]

    def card(kind, attempts, window, action):
        title, rule = INFO[kind]
        first = attempts[0] if attempts else None
        win = (first is not None and won(kind, first)) if kind == 'daily' else any(won(kind, s) for s in attempts)
        best = max(attempts, key=lambda s: (won(kind, s), s['correct'])) if attempts else None
        status = 'won' if win else 'tried' if attempts else 'todo'
        res = (_result(first) if kind == 'daily' else _result(best)) if attempts else None
        return dict(kind=kind, window=window, title_fr=title, rule_fr=rule, status=status, result_fr=res,
                    action=None if (kind == 'daily' and attempts) else action)

    th_label, th_filters = perfect_theme(utc_day)
    daily = [card('daily', today_(of('daily')), 'jour', dict(type='challenge', challenge='daily', chrono=15)),
             dict(card('perfect', today_(of('perfect')), 'jour', dict(type='challenge', challenge='perfect')), theme_fr=th_label)]
    weekly = [card('pressure', week_(of('pressure')), 'semaine', dict(type='challenge', challenge='pressure', chrono=8))]
    rw = [r for r in ranges_rows if r['answered_at'] and start <= td.local_day(r['answered_at'], tz) <= day]
    best_r = min((r['bb_per_100'] for r in rw), default=None)
    title, rule = INFO['range']
    weekly.append(dict(kind='range', window='semaine', title_fr=title, rule_fr=rule,
                       status='won' if best_r is not None and best_r < RANGE_BB else 'tried' if rw else 'todo',
                       result_fr=(f"meilleure : {best_r:g} BB pour 100".replace('.', ',') if best_r is not None else None), action=dict(type='range')))
    if mode == 'exploit':
        weekly.append(card('reader', week_(of('reader')), 'semaine', dict(type='challenge', challenge='reader')))
    run = full_week(active, day); title, rule = INFO['full_week']
    monthly = [dict(kind='full_week', window='mois', title_fr=title, rule_fr=rule, status='won' if run >= 7 else 'tried' if run else 'todo',
                    result_fr=f"meilleure suite du mois : {run} jour{'s' if run > 1 else ''}", action=None)]
    hist = []
    for kind in ('daily', 'perfect', 'pressure', 'reader'):
        seen = set()
        for s in of(kind):
            d = td.local_day(s['created_at'], tz)
            if (day - d).days > HISTORY_DAYS or (kind == 'daily' and d in seen): seen.add(d); continue
            seen.add(d)
            if won(kind, s): hist.append(dict(kind=kind, title_fr=INFO[kind][0], date=d.isoformat(), result_fr=_result(s)))
    for r in ranges_rows:
        if r['answered_at'] and r['bb_per_100'] < RANGE_BB and (day - td.local_day(r['answered_at'], tz)).days <= HISTORY_DAYS:
            hist.append(dict(kind='range', title_fr=INFO['range'][0], date=td.local_day(r['answered_at'], tz).isoformat(), result_fr=f"{r['bb_per_100']:g} BB pour 100".replace('.', ',')))
    return dict(daily=daily, weekly=weekly, monthly=monthly, history=sorted(hist, key=lambda h: h['date'], reverse=True)[:30])
