"""corrections du neuvième test joueurs (29/10/2026, docs/produit/RETEST9_JOUEURS_2026-10-29.md)"""
import datetime, json, sqlite3
import pytest
from fastapi.testclient import TestClient
from spinsacademy import challenges, goals, levels, progress, quiz, today

H = {'X-Player-Id': 'retest9-aaaa'}
D = datetime.date(2026, 10, 29)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    c = TestClient(app); c.db = str(tmp_path / 'test.sqlite')
    return c


def _create(c, body, H=H):
    return c.post('/sessions', json=body, headers=H)


def _answer(c, sid, n, pick=0):
    for i in range(n):
        q = c.get(f'/quiz/next?session_id={sid}').json()
        if q['done']: return
        c.post('/attempts', json={'session_id': sid, 'question_index': q['question_index'], 'action_id': q['question']['options'][pick]['id']})


# ------------------------------------------------------------------ défis (problèmes 1 à 7)
def test_daily_challenge_one_attempt_per_day_all_modes(client):
    s = _create(client, {'mode': 'gto', 'challenge': 'daily'}).json()
    _answer(client, s['session_id'], 2)                                           # tentative abandonnée après 2 mains
    assert client.get(f"/quiz/next?session_id={s['session_id']}").json()['plan'] == 'challenge_daily'      # le chrono imposé se retrouve
    d = client.get('/users/me/challenges?mode=gto&tz=60', headers=H).json()['daily'][0]
    assert d['status'] == 'tried' and d['result_fr'].startswith('en cours : 2/5')
    assert d['action'] == dict(type='resume', session_id=s['session_id'], challenge='daily', chrono=15)    # elle se reprend, ne se refait pas
    assert _create(client, {'mode': 'gto', 'challenge': 'daily'}).status_code == 409
    assert _create(client, {'mode': 'exploit', 'challenge': 'daily'}).status_code == 409                   # pas une tentative par mode
    _answer(client, s['session_id'], 3)
    d = client.get('/users/me/challenges?mode=exploit&tz=60', headers=H).json()['daily'][0]
    assert d['action'] is None and d['next_fr'] == 'Nouveau défi demain.' and '/5' in d['result_fr']
    hist = client.get('/users/me/challenges?mode=gto&tz=60', headers=H).json()['history']
    assert [h['kind'] for h in hist] == ['daily'] and 'won' in hist[0]                                       # tentative visible, réussie ou non


def test_perfect_series_follows_todays_theme(client):
    t = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    c = client.get('/users/me/challenges?mode=gto&tz=60', headers=H).json()
    assert c['daily'][1]['theme_fr'] == t['theme_fr']
    s = _create(client, {'mode': 'gto', 'challenge': 'perfect', 'tz': 60}).json()
    con = sqlite3.connect(client.db)
    assert json.loads(con.execute('SELECT filters FROM sessions WHERE id = ?', (s['session_id'],)).fetchone()[0]) == t['steps'][1]['filters']


def test_reader_challenge_has_two_profile_questions(client):
    s = _create(client, {'mode': 'exploit', 'challenge': 'reader', 'seed': 3}).json()
    con = sqlite3.connect(client.db); spots = quiz.load(quiz.DEFAULT_FIELD)[1]
    kinds = [spots[r[0]]['field']['type'] for r in con.execute('SELECT spot_id FROM questions WHERE session_id = ?', (s['session_id'],))]
    assert sum(k == 'profil' for k in kinds) >= challenges.READER_PROFILES


def test_challenge_rules():
    s = lambda c, t=0: dict(correct=c, size=5, timeouts=t, answered=5)
    assert challenges.won('pressure', s(4)) and not challenges.won('pressure', s(3))
    assert not challenges.won('daily', dict(s(5), answered=4))                     # pas fini : pas réussi
    assert challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=90)) and not challenges.range_won(dict(bb_per_100=1.2, accuracy_pct=82))
    week = {D - datetime.timedelta(days=k) for k in (0, 1, 2, 4, 5, 6, 7)}         # un jour manqué : la série de jours compte 7
    assert today.streak(week, D) == 7 and challenges.full_week(week, D) == 7


# ------------------------------------------------------------------ séance du jour (problèmes 8 à 11)
def test_theme_and_range_fixed_for_the_day(client):
    t1 = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    for _ in range(2):                                                            # des erreurs ailleurs ne changent plus le thème du jour
        s = _create(client, {'mode': 'gto', 'filters': {'family': 'vs_raise', 'min_stack': 16.5, 'max_stack': 99}}).json()
        _answer(client, s['session_id'], 5, pick=0)
    t2 = client.get('/users/me/today?mode=gto&tz=60', headers=H).json()
    assert t2['theme_fr'] == t1['theme_fr'] and t2['steps'][1]['filters'] == t1['steps'][1]['filters']
    assert t1['steps'][2]['spot_id'] and t2['steps'][2]['spot_id'] == t1['steps'][2]['spot_id']           # même situation de range
    assert t2['steps'][0]['filters'] == levels.depth_filters(1)                    # révision complétée dans la profondeur du niveau
    assert t2['played_before'] and t2['streak'] == 1


def test_review_step_done_only_when_nothing_due():
    sess = [dict(created_at='2026-10-29T10:00:00+00:00', plan='review', filters='{}', size=5, answered=5)]
    t = today.build(sess, [], 3, None, D, 0)
    assert not t['steps'][0]['done'] and t['steps'][0]['label_fr'] == 'Révision : 3 mains à revoir'
    t = today.build(sess, [], 0, None, D, 60, next_due=('2026-10-29T17:30:00+00:00', 23))
    assert t['steps'][0]['done'] and t['steps'][0]['label_fr'] == "Révision : rien à revoir pour l'instant (23 mains à partir de 18 h 30)"


def test_dimension_focus_is_not_a_theme():
    f = dict(label='Position : BB', filters=dict(hero='BB'))                        # pas de situation ni de tapis : on prend le cycle
    assert today.theme_of_day(f, 0, None) == today.THEMES[0]


# ------------------------------------------------------------------ niveaux et mode (12 à 14)
def test_level_criteria_name_the_depth():
    st = levels.status(1, [], [], set())
    assert st['criteria'][0]['label_fr'] == '100 décisions à moins de 10 BB'
    assert levels.EXPERIENCE_FR['confirme'] == '3 mois ou plus'


def test_mode_kept_on_server(client):
    assert client.get('/users/me/preferences', headers=H).json()['mode'] is None
    p = client.put('/users/me/preferences', json={'mode': 'exploit'}, headers=H).json()
    assert p['mode'] == 'exploit' and p['adaptive'] is True
    assert client.put('/users/me/preferences', json={'adaptive': False}, headers=H).json() == dict(adaptive=False, adaptation_reset_at=None, mode='exploit')
    lv = client.get('/users/me/level', headers=H).json()
    assert lv['levels'][3]['depth_fr'] and lv['depth_fr'] == levels.DEPTH_FR[1]


def test_streak_counts_every_mode(client):
    s = _create(client, {'mode': 'gto'}).json(); _answer(client, s['session_id'], 5)
    t = client.get('/users/me/today?mode=exploit&tz=60', headers=H).json()
    assert t['streak'] == 1 and t['played_before']                               # en exploitant, pas « Première séance »


# ------------------------------------------------------------------ objectifs (17 à 19)
def test_goal_days_capped_to_days_left():
    thu = datetime.date(2026, 10, 29)
    assert goals.days_cap(dict(day_set=set()), thu) == 4                          # jeudi : jeudi, vendredi, samedi, dimanche
    assert goals.days_cap(dict(day_set={thu - datetime.timedelta(days=2), thu}), thu) == 5
    assert goals.propose({}, None, [], new=True)['days'] == goals.DEFAULT_NEW['days']


def test_free_play_counts_as_training_day(client):
    s = _create(client, {'mode': 'gto'}).json(); _answer(client, s['session_id'], 5)
    g = client.get('/users/me/goals?mode=gto&tz=60', headers=H).json()
    assert g['items'][0]['value'] == 1 and g['items'][0]['label_fr'] == "Jours d'entraînement"


# ------------------------------------------------------------------ divers (22)
def test_bet_size_errors_are_named_as_size():
    sp = dict(field=dict(options=[dict(id='r', type='raise'), dict(id='a', type='allin'), dict(id='f', type='fold')], correct='a'))
    assert progress.direction(sp, dict(action_id='r')) == 'small' and progress.direction(sp, dict(action_id='f')) == 'tight'
    sp['field']['correct'] = 'r'
    assert progress.direction(sp, dict(action_id='a')) == 'big'
