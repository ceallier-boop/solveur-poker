"""progression présentée en positif (chantier AU5, 06/11/2026)"""
import datetime
import pytest
from fastapi.testclient import TestClient
from spinsacademy import levels, quiz, wins

D = datetime.date(2026, 11, 6)
V = quiz.DEFAULT_VERSION
SPOTS = list(quiz.load(V)[1].values())
L1 = [sp['spot_id'] for sp in SPOTS if levels.in_level(1, sp)]
L3 = [sp['spot_id'] for sp in SPOTS if levels.in_level(3, sp)]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def at(days_ago, hour=12):
    return datetime.datetime(D.year, D.month, D.day, hour, tzinfo=datetime.timezone.utc) - datetime.timedelta(days=days_ago)


def rows(n, days_ago, regret=0, errors=0, spots=L1, hand='AKo'):
    """n réponses il y a `days_ago` jours, `errors` d'entre elles en erreur, chacune avec `regret` mbb"""
    return [dict(dataset_version=V, spot_id=spots[i % len(spots)], hand=hand, verdict='erreur' if i < errors else 'correct',
                 regret_mbb=regret, answered_at=at(days_ago).isoformat(timespec='seconds')) for i in range(n)]


def kinds(out): return [w['kind'] for w in out['wins']]


def no_negative(out):
    for w in out['wins']:
        for k, v in w.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool) and k not in ('from_level',): assert v >= 0, (k, v)


def test_no_history(client):
    r = client.get('/users/me/wins?mode=gto&tz=60', headers={'X-Player-Id': 'wins-new-0000'}).json()
    assert r['wins'] == [] and r['effort']['decisions'] == 0 and r['effort']['text_fr']      # jamais d'écran vide
    assert {s['kind'] for s in r['not_enough']} == {'bb_recovered', 'fewer_errors'}
    assert client.get('/users/me/wins?mode=x', headers={'X-Player-Id': 'wins-new-0000'}).status_code == 422
    assert client.get('/users/me/wins?mode=gto').status_code == 400


def test_bb_recovered_and_minimum():
    better = rows(60, 2, regret=50) + rows(60, 9, regret=150)        # 5 puis 15 BB perdus pour 100 décisions
    out = wins.build(better, 'gto', D, 0)
    w = next(x for x in out['wins'] if x['kind'] == 'bb_recovered')
    assert w['gain_per_100'] == 10 and w['bb_recovered'] == 6 and w['text_fr'] == 'Environ 6 BB récupérés sur tes 60 décisions par rapport à la semaine passée.'
    out = wins.build(rows(49, 2, regret=50) + rows(60, 9, regret=150), 'gto', D, 0)      # moins de 50 décisions : rien
    assert 'bb_recovered' not in kinds(out)
    s = next(x for x in out['not_enough'] if x['kind'] == 'bb_recovered')
    assert s['decisions_now'] == 49 and s['needed'] == 50


def test_regression_never_negative():
    worse = rows(80, 2, regret=200, errors=30) + rows(80, 9, regret=50, errors=5) + rows(80, 20, errors=2)
    out = wins.build(worse, 'gto', D, 0)
    assert 'bb_recovered' not in kinds(out) and 'fewer_errors' not in kinds(out)
    assert out['not_enough'] == [] and out['effort']['decisions'] == 80                # recul : ni gain, ni manque, l'effort reste
    no_negative(out)


def test_fewer_errors():
    out = wins.build(rows(80, 3, errors=4) + rows(80, 20, errors=20), 'gto', D, 0)       # 5 contre 25 erreurs pour 100
    w = next(x for x in out['wins'] if x['kind'] == 'fewer_errors')
    assert w['fewer_per_100'] == 20 and w['text_fr'].startswith('20 erreurs de moins')
    noise = wins.build(rows(60, 3, errors=9) + rows(60, 20, errors=11), 'gto', D, 0)     # 15 contre 18,3 : sous le seuil et le bruit
    assert 'fewer_errors' not in kinds(noise)


def test_level_change_limits_to_current_level():
    # semaine passée au niveau 1 (tapis courts, peu de pertes), cette semaine au niveau 3 : la comparaison brute serait fausse
    data = rows(60, 9, regret=50, spots=L1) + rows(60, 2, regret=250, spots=L3) + rows(60, 10, regret=300, spots=L3)
    lv = dict(level=3, promoted_at=at(4).isoformat(), updated_at=at(4).isoformat(), onboarded_at=at(40).isoformat())
    out = wins.build(data, 'gto', D, 0, lv)
    w = next(x for x in out['wins'] if x['kind'] == 'bb_recovered')
    assert w['level_only'] and w['bb_per_100_before'] == 30 and 'de ton niveau' in w['text_fr']
    assert wins.build(data, 'gto', D, 0, None)['wins'] == []                            # sans filtre : recul, rien d'affiché
    up = next(x for x in out['wins'] if x['kind'] == 'level_up')
    assert up['to_level'] == 3 and up['from_level'] == 2 and kinds(out)[0] == 'level_up'
    old = dict(lv, promoted_at=at(30).isoformat(), updated_at=at(30).isoformat())
    assert 'level_up' not in kinds(wins.build(data, 'gto', D, 0, old))
    legacy = dict(level=1, promoted_at=None, updated_at=at(1).isoformat(), onboarded_at=at(1).isoformat())   # arrivée au niveau 1
    short = wins.build(rows(60, 2, spots=L3) + rows(60, 9, spots=L3), 'gto', D, 0, legacy)['not_enough']
    assert 'bb_recovered' not in [x['kind'] for x in short]                             # pas de filtre de niveau : les 60 + 60 comptent


def test_review_recovered():
    miss = [dict(dataset_version=V, spot_id=L1[0], hand='72o', verdict='erreur', regret_mbb=500, answered_at=at(12).isoformat())]
    ok = lambda d: dict(miss[0], verdict='correct', regret_mbb=0, answered_at=at(d).isoformat())
    out = wins.build(miss + [ok(11), ok(8), ok(1)], 'gto', D, 0)                        # J+1, J+3, J+7 : acquise cette semaine
    w = next(x for x in out['wins'] if x['kind'] == 'review_recovered')
    assert w['mastered'] == 1 and w['stage_ups'] == 1 and w['paid_feature'] is True     # une seule montée dans les 7 jours
    assert 'review_recovered' not in kinds(wins.build(miss + [ok(11)], 'gto', D, 0))    # trop ancien et pas acquise


def test_timezone_boundary():
    late = [dict(r, answered_at=datetime.datetime(2026, 10, 30, 23, 30, tzinfo=datetime.timezone.utc).isoformat()) for r in rows(5, 0)]
    assert wins.build(late, 'gto', D, 0)['effort']['decisions'] == 0                     # 30/10 en UTC : hors des 7 jours
    assert wins.build(late, 'gto', D, 60)['effort']['decisions'] == 5                    # 31/10 à Paris : dedans


def test_by_category():
    """catégories (10/11) : Préflop GTO, Préflop exploitant sans la lecture, Profils en nombre, Ranges, Équités réservé"""
    field = list(quiz.load(quiz.DEFAULT_FIELD)[1].values())
    reads = [sp['spot_id'] for sp in field if sp['field']['type'] in ('identification', 'profil')]
    plays = [sp['spot_id'] for sp in field if sp['field']['type'] not in ('identification', 'profil')]
    fr = lambda n, d, spots, err=0: [dict(r, dataset_version=quiz.DEFAULT_FIELD) for r in rows(n, d, errors=err, spots=spots, hand='')]
    data = rows(60, 2, regret=50) + rows(60, 9, regret=150) + fr(6, 1, reads) + fr(3, 1, plays)
    rg = [dict(answered_at=at(1).isoformat(), accuracy_pct=90), dict(answered_at=at(2).isoformat(), accuracy_pct=70)]
    out = wins.by_category(data, rg, D, 0)
    c = {x['category']: x for x in out}
    assert list(c) == ['gto', 'exploit', 'profils', 'ranges', 'equites'] and not c['equites']['available'] and c['equites']['wins'] == []
    assert [w['kind'] for w in c['gto']['wins']] == ['bb_recovered']
    assert c['exploit']['effort']['decisions'] == 3 and c['profils']['effort']['decisions'] == 6            # la lecture sort de l'exploitant
    assert c['profils']['wins'][0] == dict(kind='reads_correct', window_days=7, correct=6, answered=6, text_fr='6 lectures justes cette semaine.')
    assert c['ranges']['wins'][0]['good'] == 1 and 'accuracy_avg' not in c['ranges']['wins'][0]                # moyenne seulement dès 3 ranges
    few = {x['category']: x for x in wins.by_category(fr(4, 1, reads), [], D, 0)}
    assert few['profils']['wins'] == [] and few['ranges']['wins'] == []                                      # moins de 5 lectures : rien
    for x in out: no_negative(x)


def test_route_keeps_fields_and_adds_by_category(client):
    r = client.get('/users/me/wins?mode=gto&tz=60', headers={'X-Player-Id': 'wins-cat-0000'}).json()
    assert {'mode', 'as_of', 'wins', 'effort', 'not_enough', 'by_category'} <= set(r)
    assert [c['category'] for c in r['by_category']] == ['gto', 'exploit', 'profils', 'ranges', 'equites']
