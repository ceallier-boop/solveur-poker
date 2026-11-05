"""Révision espacée des erreurs (évaluation du MVP, 2026-10-14 : « revoir mes erreurs quelques jours plus tard »).

Règle, affichée au joueur :
  - une main ratée (erreur ou imprécision) revient 1 jour, puis 3 jours, puis 7 jours après ;
  - une bonne réponse à la révision passe à l'étape suivante ; après la révision à 7 jours, la main est acquise ;
  - une nouvelle erreur ramène la main à l'étape 1 (1 jour après cette erreur) ;
  - une main n'est révisée que si sa situation existe dans le dataset servi (même identifiant de spot) et y reste proposable.
Les échéances se comptent en jours du joueur (décalage `tz` en minutes) : une main due aujourd'hui l'est dès le matin, et une
réussite compte dès le jour de l'échéance (test joueurs 9 : « rien à revoir aujourd'hui » et « prochaine révision : aujourd'hui »).
La correction ne change pas : une révision est notée comme une question normale.
"""
import datetime
from . import quiz

INTERVALS_DAYS = (1, 3, 7)
RULE_FR = "Une main ratée revient 1 jour, puis 3 jours, puis 7 jours après. Une bonne réponse la fait avancer ; une nouvelle erreur la fait repartir à 1 jour."


def _t(s):
    if not s: return None
    d = datetime.datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)      # date sans fuseau (ancienne ligne, saisie manuelle) : UTC


def _day(t, tz):
    return (t.astimezone(datetime.timezone.utc) + datetime.timedelta(minutes=tz)).date()


def items(rows, version, now=None, tz=0):
    """état de révision de chaque main ratée : [dict(spot_id, hand, stage, due_at, due, last_miss_at, prompt_fr)], la plus en retard d'abord.
    rows : réponses du joueur dans le mode (dataset_version, spot_id, hand, verdict, answered_at), dans l'ordre chronologique"""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    _, spots = quiz.load(version); state = {}; today = _day(now, tz)
    for r in sorted(rows, key=lambda r: r['answered_at'] or ''):
        k = (r['spot_id'], r['hand']); at = _t(r['answered_at'])
        if r['verdict'] != 'correct':
            state[k] = dict(stage=0, since=at, last_miss_at=at)                 # (re)part à l'étape 1
        elif k in state:
            st = state[k]
            if _day(at, tz) >= _day(st['since'], tz) + datetime.timedelta(days=INTERVALS_DAYS[st['stage']]):   # réussite le jour de l'échéance ou après : étape suivante
                st['stage'] += 1; st['since'] = at
    out = []
    for (sid, hand), st in state.items():
        if st['stage'] >= len(INTERVALS_DAYS): continue                         # acquise
        sp = spots.get(sid)
        if sp is None or hand not in quiz.teachable(sp): continue
        due_at = st['since'] + datetime.timedelta(days=INTERVALS_DAYS[st['stage']])
        out.append(dict(spot_id=sid, hand=hand, stage=st['stage'] + 1, due_at=due_at.isoformat(timespec='seconds'), due=_day(due_at, tz) <= today,
                        last_miss_at=st['last_miss_at'].isoformat(timespec='seconds'), interval_days=INTERVALS_DAYS[st['stage']]))
    return sorted(out, key=lambda x: x['due_at'])


def summary(rows, version, now=None, tz=0):
    it = items(rows, version, now, tz); due = [x for x in it if x['due']]; later = [x for x in it if not x['due']]
    return dict(rule_fr=RULE_FR, due=len(due), pending=len(later), next_due_at=later[0]['due_at'] if later else None, due_items=due)


def purpose_fr(item):
    d = _t(item['last_miss_at'])
    return f"Révision de ton erreur du {d:%d/%m} (étape {item['stage']} sur {len(INTERVALS_DAYS)})"
