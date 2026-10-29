"""Défis (programme de travail, étape 5, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §7).

Courts et facultatifs, ils donnent du rythme sans changer la correction ni la progression :
  - défi du jour : les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date UTC), au chrono 15 s ; une seule
    tentative par jour, tous modes confondus, enregistrée dès la création de la série (une série abandonnée se reprend, elle
    ne se recommence pas ; le serveur refuse une deuxième série, 409) ; réussi à DAILY_WIN bonnes réponses ou plus ;
  - série parfaite : 5 bonnes réponses sur 5 sur le thème de la séance du jour du joueur (donc dans son niveau) ;
  - sous pression (semaine) : une série au chrono 8 s sans coup joué au temps, à PRESSURE_WIN bonnes réponses ou plus ;
  - range au cordeau (semaine) : une range à moins de RANGE_BB BB perdus pour 100 mains et au moins RANGE_ACC % de mains bien classées ;
  - lecteur de vilain (semaine, mode exploitant) : 5 lectures justes sur 5, dont au moins READER_PASTILLES « Quelle pastille ? » ;
  - semaine pleine (mois) : 7 jours d'affilée sans jour manqué dans le mois (la série de jours de l'accueil, elle, pardonne un
    jour par semaine : la carte le dit).
Une série de défi est marquée en base (sessions.plan = « challenge_<défi> ») ; les tentatives finies (réussies ou non) forment
l'historique « Mes défis » (test joueurs 9, 29/10/2026).
"""
import datetime
from . import today as td

DAILY_WIN = 4
PRESSURE_WIN = 4          # test joueurs 9 : 3 sur 5 était trop facile
RANGE_BB = 2.0
RANGE_ACC = 85            # test joueurs 9 : une range « trop serrée » ne valide plus le défi
READER_PASTILLES = 2      # test joueurs 9 : pas seulement des « Défaut du vilain », qui se lisent sur les barres
HISTORY_DAYS = 60
SERIES = {'daily': 'challenge_daily', 'perfect': 'challenge_perfect', 'pressure': 'challenge_pressure', 'reader': 'challenge_reader'}
INFO = {
    'daily': ('Défi du jour', f"Les mêmes 5 mains pour tous aujourd'hui, au chrono 15 s. Réussi à {DAILY_WIN} sur 5. Une seule tentative par jour, tous modes confondus."),
    'perfect': ('Série parfaite', "5 bonnes réponses sur 5 sur le thème de ta séance du jour."),
    'pressure': ('Sous pression', f"Une série au chrono 8 s sans coup joué au temps, à {PRESSURE_WIN} sur 5 ou plus."),
    'range': ('Range au cordeau', f"Une range à moins de {str(RANGE_BB).replace('.0', '').replace('.', ',')} BB perdus pour 100 mains, avec au moins {RANGE_ACC} % de mains bien classées."),
    'reader': ('Lecteur de vilain', f"5 lectures justes sur 5, dont au moins {READER_PASTILLES} « Quelle pastille ? »."),
    'full_week': ('Semaine pleine', "7 jours d'affilée dans le mois, sans jour manqué. La série de jours de l'accueil, elle, pardonne un jour par semaine."),
}


def daily_seed(utc_day):
    return int(utc_day.strftime('%Y%m%d'))


def _result(s):
    return f"{s['correct']}/{s['size']}" + (f", {s['timeouts']} au temps" if s.get('timeouts') else '')


def won(kind, s):
    if kind == 'daily': return s['correct'] >= DAILY_WIN
    if kind == 'perfect': return s['correct'] == s['size']
    if kind == 'pressure': return s['timeouts'] == 0 and s['correct'] >= PRESSURE_WIN
    if kind == 'reader': return s['correct'] == s['size']
    return False


def range_won(r):
    return r['bb_per_100'] < RANGE_BB and r['accuracy_pct'] >= RANGE_ACC


def full_week(active, day):
    """plus longue suite de jours d'activité sans jour manqué dans le mois de `day` (jours locaux)"""
    run, best = 0, 0; d = day.replace(day=1)
    while d <= day:
        run = run + 1 if d in active else 0; best = max(best, run); d += datetime.timedelta(days=1)
    return best


def build(sessions, ranges_rows, active, day, tz, mode, utc_day, theme):
    """sessions : dicts {id, created_at, plan, mode, size, answered, correct, timeouts} de tous les modes (séries finies ou non) ;
    ranges_rows : {answered_at, bb_per_100, accuracy_pct} ; active : jours locaux avec activité (tous modes) ; theme : (libellé,
    filtres) de la séance du jour dans ce mode. Renvoie les défis du jour, de la semaine, du mois et l'historique"""
    start = day - datetime.timedelta(days=day.weekday())
    done = [s for s in sessions if s['answered'] >= s['size']]
    of = lambda kind, xs=done: sorted([s for s in xs if s['plan'] == SERIES[kind] and (kind == 'daily' or s['mode'] == mode)], key=lambda s: s['created_at'])
    today_ = lambda xs: [s for s in xs if td.local_day(s['created_at'], tz) == day]
    week_ = lambda xs: [s for s in xs if start <= td.local_day(s['created_at'], tz) <= day]

    def card(kind, attempts, window, action):
        title, rule = INFO[kind]
        win = any(won(kind, s) for s in attempts)
        best = max(attempts, key=lambda s: (won(kind, s), s['correct'])) if attempts else None
        return dict(kind=kind, window=window, title_fr=title, rule_fr=rule, status='won' if win else 'tried' if attempts else 'todo',
                    result_fr=_result(best) if attempts else None, action=action)

    # défi du jour : la première série du jour UTC (celui du tirage), finie ou non, dans n'importe quel mode
    first = next(iter(of('daily', [s for s in sessions if td.local_day(s['created_at'], 0) == utc_day])), None)
    title, rule = INFO['daily']
    if first is None:
        daily0 = dict(kind='daily', window='jour', title_fr=title, rule_fr=rule, status='todo', result_fr=None,
                      action=dict(type='challenge', challenge='daily', chrono=15))
    elif first['answered'] < first['size']:                                # entamée : elle se reprend, elle ne se recommence pas
        daily0 = dict(kind='daily', window='jour', title_fr=title, rule_fr=rule, status='started',
                      result_fr=f"{first['answered']}/{first['size']} mains jouées", action=dict(type='resume', session_id=first['id'], chrono=15, challenge='daily'))
    else:
        daily0 = dict(kind='daily', window='jour', title_fr=title, rule_fr=rule, status='won' if won('daily', first) else 'tried',
                      result_fr=_result(first), action=None, next_fr='Nouveau défi demain.')
    daily = [daily0, dict(card('perfect', today_(of('perfect')), 'jour', dict(type='challenge', challenge='perfect')), theme_fr=theme[0])]
    weekly = [card('pressure', week_(of('pressure')), 'semaine', dict(type='challenge', challenge='pressure', chrono=8))]
    rw = [r for r in ranges_rows if r['answered_at'] and start <= td.local_day(r['answered_at'], tz) <= day]
    best_r = min(rw, key=lambda r: (not range_won(r), r['bb_per_100'])) if rw else None
    title, rule = INFO['range']
    weekly.append(dict(kind='range', window='semaine', title_fr=title, rule_fr=rule,
                       status='won' if best_r and range_won(best_r) else 'tried' if rw else 'todo',
                       result_fr=(f"meilleure : {best_r['bb_per_100']:g} BB pour 100, {best_r['accuracy_pct']:g} % bien classées".replace('.', ',') if best_r else None),
                       action=dict(type='range')))
    if mode == 'exploit':
        weekly.append(card('reader', week_(of('reader')), 'semaine', dict(type='challenge', challenge='reader')))
    run = full_week(active, day); title, rule = INFO['full_week']
    monthly = [dict(kind='full_week', window='mois', title_fr=title, rule_fr=rule, status='won' if run >= 7 else 'tried' if run else 'todo',
                    result_fr=f"meilleure suite sans jour manqué ce mois-ci : {run} jour{'s' if run > 1 else ''}", action=None)]
    hist = []
    for kind in ('daily', 'perfect', 'pressure', 'reader'):
        seen = set()
        for s in of(kind):
            d = td.local_day(s['created_at'], tz)
            if (day - d).days > HISTORY_DAYS or (kind == 'daily' and d in seen): seen.add(d); continue
            seen.add(d)
            hist.append(dict(kind=kind, title_fr=INFO[kind][0], date=d.isoformat(), result_fr=_result(s), won=won(kind, s), at=s['created_at']))
    for r in ranges_rows:
        if r['answered_at'] and range_won(r) and (day - td.local_day(r['answered_at'], tz)).days <= HISTORY_DAYS:
            hist.append(dict(kind='range', title_fr=INFO['range'][0], date=td.local_day(r['answered_at'], tz).isoformat(),
                             result_fr=f"{r['bb_per_100']:g} BB pour 100".replace('.', ','), won=True, at=r['answered_at']))
    hist = sorted(hist, key=lambda h: h['at'], reverse=True)[:30]
    for h in hist: h.pop('at')
    return dict(daily=daily, weekly=weekly, monthly=monthly, history=hist)
