"""Recommandations de l'accueil (programme de travail, étape 2, 29/10/2026 ; docs/produit/PROGRAMME_TRAVAIL_2026-10-29.md §5).

Au plus MAX_RECS recommandations, chacune avec un constat chiffré et une action en un toucher, dans cet ordre de priorité :
  1. révisions en retard de plus de LATE_DAYS jours ;
  2. thème fragile (au moins 2 erreurs), autre que le thème de la séance du jour, avec le sens des erreurs (trop serré, trop large) ;
  3. dernière range trop serrée, trop large ou sous RANGE_MIN % de mains bien classées : la refaire ;
  4. coups joués au temps sur 7 jours (au moins TIMEOUTS_MIN) : une série au chrono 15 s ;
  5. découverte : une situation jamais jouée dans ce mode.
(Le niveau presque validé et les mains réelles viendront avec les niveaux et « Mes mains ».)
Chaque recommandation : kind, text_fr (constat), label_fr (bouton), action = dict(type=review|series|range, filters, spot_id, chrono).
"""
import datetime
from . import progress, ranges

MAX_RECS = 2
LATE_DAYS = 2
RANGE_MIN = 80
TIMEOUTS_MIN = 2
SIDE = {'tight': ("le plus souvent en mettant moins de jetons qu'il ne fallait : tu te couches ou tu paies quand il fallait relancer ou pousser",),
        'loose': ("le plus souvent en mettant plus de jetons qu'il ne fallait : tu paies, relances ou pousses quand il fallait te coucher ou payer",)}   # test joueurs 9 : « trop large » se lisait comme la taille de la mise
DISCOVER = (     # situations proposées à la découverte, de la plus simple à la plus fine
    ('first_in', 'Premier à parler'), ('vs_allin', 'Face à un tapis'), ('vs_limp', 'Face à un limp'), ('vs_raise', 'Face à une relance'))


def _strip(label):
    for m in ('GTO · ', 'Exploitant · '): label = label[len(m):] if label.startswith(m) else label
    return label


def review_late(items, now):
    late = [x for x in items if x['due'] and datetime.datetime.fromisoformat(x['due_at']) <= now - datetime.timedelta(days=LATE_DAYS)]
    if not late: return None
    n = len(late)
    return dict(kind='review', text_fr=f"{n} main{'s' if n > 1 else ''} ratée{'s' if n > 1 else ''} attend{'ent' if n > 1 else ''} {'leur' if n > 1 else 'sa'} révision depuis plus de {LATE_DAYS} jours.",
                label_fr='Revoir mes mains', action=dict(type='review'))


def fragile(stats, today_filters):
    for t in stats.get('recurring_errors') or []:
        f = {k: v for k, v in t['filters'].items() if k != 'mode'}
        if today_filters and all(today_filters.get(k) == v for k, v in f.items()): continue      # déjà le thème de la séance
        side = 'tight' if t.get('tight', 0) > t.get('loose', 0) else 'loose' if t.get('loose', 0) > t.get('tight', 0) else None
        return dict(kind='theme', text_fr=f"{_strip(t['label'])} : {t['errors']} erreurs sur {t['questions']}" + (f", {SIDE[side][0]}." if side else '.'),
                    label_fr='Une série ciblée', action=dict(type='series', filters=f))
    return None


def range_redo(last):
    """last : dernière range du joueur (spot_id, hands, accuracy_pct, dataset_version)"""
    if not last: return None
    from . import quiz
    _, spots = quiz.load(last['dataset_version']); sp = spots.get(last['spot_id'])
    t = ranges.task(sp) if sp else None
    if not t: return None
    g = ranges.grade(t, last['hands'])
    ratio = g['my_share_pct'] / g['ref_share_pct'] if g['ref_share_pct'] else 1
    where = t['where_fr'][0].upper() + t['where_fr'][1:]
    if ratio < 0.75: msg = f"Ta dernière range était trop serrée : {g['my_share_pct']} % des mains au lieu de {g['ref_share_pct']} % ({where})."
    elif ratio > 1.33: msg = f"Ta dernière range était trop large : {g['my_share_pct']} % des mains au lieu de {g['ref_share_pct']} % ({where})."
    elif g['accuracy_pct'] < RANGE_MIN: msg = f"Ta dernière range : {str(g['accuracy_pct']).replace('.', ',')} % de mains bien classées ({where})."
    else: return None
    return dict(kind='range', text_fr=msg, label_fr='Refaire cette range', action=dict(type='range', spot_id=last['spot_id']))


def timeouts(rows, now):
    n = sum(1 for r in rows if r.get('timed_out') and (r['answered_at'] or '') >= (now - datetime.timedelta(days=7)).isoformat())
    if n < TIMEOUTS_MIN: return None
    return dict(kind='chrono', text_fr=f"{n} coups joués au temps cette semaine : une série au chrono 15 s pour prendre le rythme.",
                label_fr='Série au chrono 15 s', action=dict(type='series', filters={}, chrono=15))


def discover(stats, today_filters=None):
    played = {r['filters'].get('family') for r in (stats.get('by') or {}).get('family', [])}
    for fam, label in DISCOVER:
        if fam not in played and (today_filters or {}).get('family') != fam:     # pas la situation de la séance
            return dict(kind='discover', text_fr=f"Découvre une situation que tu n'as jamais jouée ici : {label.lower()}.",
                        label_fr='Découvrir', action=dict(type='series', filters=dict(family=fam)))
    return None


def build(stats, review_items, last_range, rows, today_filters, now=None, level_msg=None, level_next=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cands = [review_late(review_items, now), fragile(stats, today_filters), range_redo(last_range), timeouts(rows, now),
             dict(kind='level', text_fr=level_msg, label_fr='Voir mon niveau', action=dict(type='level')) if level_msg else None,   # étape 4
             discover(stats, today_filters)]
    return [c for c in cands if c][:MAX_RECS]
