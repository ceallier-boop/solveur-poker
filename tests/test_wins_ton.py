"""Ton de GET /users/me/wins (chantier AU5) : jamais de chiffre négatif, jamais de recul présenté au joueur, quel que soit son
historique. Complète tests/test_wins.py (7 cas de Défis) par un test de propriété sur des historiques tirés au hasard et un
passage par l'API."""
import datetime, json, random, re
from fastapi.testclient import TestClient
from spinsacademy import quiz, wins
from tests.test_wins import D, L1, L3, V, at

NEGATIVE_TEXT = re.compile(r'(?<![\w,])[-−–]\s?\d')
REGRESSION_WORDS = re.compile(r'\b(pire|recul|régress\w*|moins bien|de plus pour 100)\b', re.I)


def scan(obj, path='wins'):
    """aucun nombre négatif, aucun texte qui affiche un chiffre négatif ou un recul"""
    if isinstance(obj, dict):
        for k, v in obj.items(): scan(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj): scan(v, f'{path}[{i}]')
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        assert obj >= 0, (path, obj)
    elif isinstance(obj, str):
        assert not NEGATIVE_TEXT.search(obj) and not REGRESSION_WORDS.search(obj), (path, obj)


def history(rnd):
    """réponses réparties sur 30 jours, chaque fenêtre avec son propre niveau de jeu (progrès, recul ou rien)"""
    rows = []
    for days_ago in range(30):
        n = rnd.choice((0, 0, 3, 10, 25)); err = rnd.random() * 0.5; regret = rnd.choice((0, 30, 100, 250, 600))
        spots = rnd.choice((L1, L3))
        for i in range(n):
            bad = rnd.random() < err
            rows.append(dict(dataset_version=V, spot_id=rnd.choice(spots), hand=rnd.choice(('AKo', '72o', 'T9s', '55')),
                             verdict='erreur' if bad else rnd.choice(('correct', 'correct', 'imprécision')),
                             regret_mbb=regret * bad + rnd.choice((0, 0, 10, 40)),
                             answered_at=at(days_ago, rnd.randrange(24)).isoformat(timespec='seconds')))
    return rows


def level_row(rnd):
    if rnd.random() < 0.4: return None
    lv = rnd.randint(1, 4); promoted = at(rnd.randrange(20)).isoformat() if lv > 1 and rnd.random() < 0.6 else None
    return dict(level=lv, promoted_at=promoted, updated_at=at(rnd.randrange(20)).isoformat(), onboarded_at=at(25).isoformat())


def test_random_histories_never_show_a_negative_figure():
    rnd = random.Random(20261106); shown = set()
    for _ in range(300):
        out = wins.build(history(rnd), 'gto', D, rnd.choice((-600, -300, 0, 60, 120, 540, 840)), level_row(rnd))
        scan(json.loads(json.dumps(out, ensure_ascii=False)))
        for w in out['wins']:
            shown.add(w['kind'])
            if w['kind'] == 'bb_recovered': assert w['bb_per_100_before'] > w['bb_per_100_now'] and w['bb_recovered'] > 0
            if w['kind'] == 'fewer_errors': assert w['errors_per_100_before'] > w['errors_per_100_now']
            if w['kind'] == 'level_up': assert w['to_level'] > w['from_level'] >= 1
        assert out['effort']['text_fr']
    assert {'bb_recovered', 'fewer_errors'} <= shown, f'le tirage doit aussi produire des progrès, sinon le test ne prouve rien : {shown}'


def test_api_after_a_bad_session(tmp_path, monkeypatch):
    """un joueur qui ne fait que des erreurs : la réponse de l'API reste positive (effort, pas de reproche)"""
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    client = TestClient(app); h = {'X-Player-Id': 'wins-ton-0001'}
    sid = client.post('/sessions', json={'seed': 7}, headers=h).json()['session_id']
    for i in range(5):
        q = client.get('/quiz/next', params={'session_id': sid}, headers=h).json()['question']
        cost = lambda o: quiz.correct(V, q['spot_id'], q['hand'], o['id'])['regret_mbb']
        worst = max(q['options'], key=cost)                              # l'option qui coûte le plus : une vraie mauvaise séance
        a = client.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': worst['id']}, headers=h)
        assert a.status_code == 200 and a.json()['verdict'] != 'correct'
    r = client.get('/users/me/wins?mode=gto&tz=60', headers=h); assert r.status_code == 200
    out = r.json(); scan(out)
    assert out['effort']['decisions'] == 5 and out['wins'] == []
