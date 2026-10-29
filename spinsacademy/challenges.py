"""Défis (programme de travail, étape 5, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §7).

Courts et facultatifs, ils donnent du rythme sans changer la correction ni la progression :
  - défi du jour : les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date UTC), au chrono 15 s ; une seule
    tentative par jour UTC, tous modes confondus, comptée dès la création de la série (une tentative abandonnée compte, elle se
    reprend mais ne se refait pas ; le serveur refuse la deuxième) ; réussi à DAILY_WIN bonnes réponses ou plus ;
  - série parfaite : 5 bonnes réponses sur 5 sur le thème de la séance du jour du joueur ;
  - sous pression (semaine) : une série au chrono 8 s sans coup joué au temps, à PRESSURE_WIN bonnes réponses ou plus ;
  - range au cordeau (semaine) : une range à moins de RANGE_BB BB perdus pour 100 mains et au moins RANGE_ACC % de mains bien classées ;
  - lecteur de vilain (semaine, mode exploitant) : 5 lectures justes sur 5, dont au moins READER_PROFILES « Quelle pastille ? » ;
  - semaine pleine (mois) : une série de 7 jours dans le mois, comptée comme la série de jours de l'accueil (un jour manqué par
    période de 7 jours est pardonné).
Une série de défi est marquée en base (sessions.plan = « challenge_<défi> ») ; « Mes défis » garde les tentatives (réussies ou non).
Corrections du neuvième test joueurs (29/10/2026) : tentative unique du défi du jour, bilan « Nouveau défi demain », série parfaite
sur le thème de la séance, semaine pleine alignée sur la série de jours, seuils relevés, tentatives visibles.
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
    'daily': ('Défi du jour', f"Les mêmes 5 mains pour tous aujourd'hui, au chrono 15 s. Réussi à {DAILY_WIN} sur 5. Une seule tentative par jour, tous modes confondus."),
    'perfect': ('Série parfaite', "5 bonnes réponses sur 5 sur le thème de ta séance du jour."),
    'pressure': ('Sous pression', f"Une série au chrono 8 s sans coup joué au temps, à {PRESSURE_WIN} sur 5 ou plus."),
    'range': ('Range au cordeau', f"Une range à moins de {str(RANGE_BB).replace('.0', '').replace('.', ',')} BB perdus pour 100 mains, avec au moins {RANGE_ACC} % de mains bien classées."),
    'reader': ('Lecteur de vilain', f"5 lectures justes sur 5, dont au moins {READER_PROFILES} « Quelle pastille ? »."),
    'full_week': ('Semaine pleine', "7 jours de suite d'entraînement dans le mois, comptés comme ta série de jours (un jour manqué par semaine est pardonné)."),
}


def daily_seed(utc_day):
    return int(utc_day.strftime('%Y%m%d'))


def utc_day_of(iso):
    return td.local_day(iso, 0)


def _result(s):
    if s['answered'] < s['size']: return f"en cours : {s['answered']}/{s['size']} répondues, {s['correct']} bonne{'s' if s['correct'] > 1 else ''}"
    return f"{s['correct']}/{s['size']}" + (f", {s['timeouts']} au temps" if s.get('timeouts') else '')


def won(kind, s):
    if s.get('answered', s['size']) < s['size']: return False
    if kind == 'daily': return s['correct'] >= DAILY_WIN
    if kind == 'perfect': return s['correct'] == s['size']
    if kind == 'pressure': return s['timeouts'] == 0 and s['correct'] >= PRESSURE_WIN
    if kind == 'reader': return s['correct'] == s['size']
    return False


def range_won(r):
    return r['bb_per_100'] < RANGE_BB and r.get('accuracy_pct', 100) >= RANGE_ACC


def full_week(active, day):
    """meilleure série de jours du mois de `day`, avec la règle de la série de jours de l'accueil (today.streak)"""
    start = day.replace(day=1); month = {d for d in active if start <= d <= day}; best = 0; d = start
    while d <= day:
        if d in month: best = max(best, td.streak(month, d))
        d += datetime.timedelta(days=1)
    return best


def daily_attempt(sessions, utc_day):
    """la tentative du défi du jour (la première créée ce jour UTC, tous modes), ou None"""
    xs = sorted([s for s in sessions if s['plan'] == SERIES['daily'] and utc_day_of(s['created_at']) == utc_day], key=lambda s: s['created_at'])
    return xs[0] if xs else None


def build(sessions, ranges_rows, active, day, tz, mode, utc_day, theme_fr=None, all_sessions=None):
    """sessions : dicts {id, created_at, plan, size, answered, correct, timeouts} du mode (séries finies ou non) ; all_sessions : idem,
    tous modes (défi du jour) ; ranges_rows : {answered_at, bb_per_100, accuracy_pct} ; active : jours locaux avec activité ;
    theme_fr : thème de la séance du jour. Renvoie les défis du jour, de la semaine, du mois et l'historique des tentatives"""
    start = day - datetime.timedelta(days=day.weekday())
    done = [s for s in sessions if s['answered'] >= s['size']]
    of = lambda kind: sorted([s for s in done if s['plan'] == SERIES[kind]], key=lambda s: s['created_at'])
    today_ = lambda xs: [s for s in xs if td.local_day(s['created_at'], tz) == day]
    week_ = lambda xs: [s for s in xs if start <= td.local_day(s['created_at'], tz) <= day]

    def card(kind, attempts, window, action):
        title, rule = INFO[kind]
        win = any(won(kind, s) for s in attempts)
        best = max(attempts, key=lambda s: (won(kind, s), s['correct'])) if attempts else None
        return dict(kind=kind, window=window, title_fr=title, rule_fr=rule, status='won' if win else 'tried' if attempts else 'todo',
                    result_fr=_result(best) if best else None, action=action)

    first = daily_attempt(all_sessions if all_sessions is not None else sessions, utc_day)
    title, rule = INFO['daily']
    if first is None: dcard = dict(kind='daily', window='jour', title_fr=title, rule_fr=rule, status='todo', result_fr=None,
                                   action=dict(type='challenge', challenge='daily', chrono=15))
    else:
        open_ = first['answered'] < first['size']                     # tentative abandonnée : elle se reprend, elle ne se refait pas
        dcard = dict(kind='daily', window='jour', title_fr=title, rule_fr=rule, status='won' if won('daily', first) else 'tried',
                     result_fr=_result(first), action=dict(type='resume', session_id=first['id'], challenge='daily', chrono=15) if open_ else None,
                     next_fr=None if open_ else 'Nouveau défi demain.')
    daily = [dcard, dict(card('perfect', today_(of('perfect')), 'jour', dict(type='challenge', challenge='perfect')), theme_fr=theme_fr)]
    weekly = [card('pressure', week_(of('pressure')), 'semaine', dict(type='challenge', challenge='pressure', chrono=8))]
    rw = [r for r in ranges_rows if r['answered_at'] and start <= td.local_day(r['answered_at'], tz) <= day]
    best_r = min(rw, key=lambda r: (not range_won(r), r['bb_per_100'])) if rw else None
    title, rule = INFO['range']
    weekly.append(dict(kind='range', window='semaine', title_fr=title, rule_fr=rule,
                       status='won' if best_r and range_won(best_r) else 'tried' if rw else 'todo',
                       result_fr=(f"meilleure : {best_r['bb_per_100']:g} BB pour 100, {best_r.get('accuracy_pct', 0):g} % bien classées".replace('.', ',') if best_r else None),
                       action=dict(type='range')))
    if mode == 'exploit':
        weekly.append(card('reader', week_(of('reader')), 'semaine', dict(type='challenge', challenge='reader')))
    run = full_week(active, day); title, rule = INFO['full_week']
    monthly = [dict(kind='full_week', window='mois', title_fr=title, rule_fr=rule, status='won' if run >= 7 else 'tried' if run else 'todo',
                    result_fr=f"meilleure série du mois : {run} jour{'s' if run > 1 else ''}", action=None)]
    hist = []
    for kind in ('daily', 'perfect', 'pressure', 'reader'):
        seen = set()
        for s in of(kind):
            d = td.local_day(s['created_at'], tz)
            if (day - d).days > HISTORY_DAYS: continue
            if kind == 'daily':                                        # seule la tentative du jour compte
                u = utc_day_of(s['created_at'])
                if u in seen: continue
                seen.add(u)
            hist.append(dict(kind=kind, title_fr=INFO[kind][0], date=d.isoformat(), result_fr=_result(s), won=won(kind, s)))
    for r in ranges_rows:
        if r['answered_at'] and range_won(r) and (day - td.local_day(r['answered_at'], tz)).days <= HISTORY_DAYS:
            hist.append(dict(kind='range', title_fr=INFO['range'][0], date=td.local_day(r['answered_at'], tz).isoformat(),
                             result_fr=f"{r['bb_per_100']:g} BB pour 100".replace('.', ','), won=True))
    return dict(daily=daily, weekly=weekly, monthly=monthly, history=sorted(hist, key=lambda h: h['date'], reverse=True)[:30])
