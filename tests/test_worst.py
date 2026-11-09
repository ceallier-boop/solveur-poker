"""les 3 pires erreurs de la journée (chantier N2, 09/11/2026)"""
import datetime, sqlite3
import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz

A = {'X-Player-Id': 'worst-a-0000'}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def play(c, H, body, worst=True):
    """une série en jouant le coup le plus coûteux (worst) ou le meilleur"""
    s = c.post('/sessions', json=body, headers=H).json()
    for i in range(s['size']):
        q = c.get(f"/quiz/next?session_id={s['session_id']}").json()['question']
        reg = sorted((quiz.correct(s['dataset_version'], q['spot_id'], q['hand'], o['id'])['regret_mbb'], o['id']) for o in q['options'])
        c.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': reg[-1 if worst else 0][1]}, headers=H)
    return s


def get(c, mode='gto', tz=60): return c.get(f'/users/me/worst-today?mode={mode}&tz={tz}', headers=A).json()


def test_empty_and_identity(client):
    r = get(client)
    assert r['errors'] == [] and r['mode'] == 'gto' and r['date']                 # aucune erreur : liste vide, pas d'erreur
    assert client.get('/users/me/worst-today?mode=gto').status_code == 400          # sans pseudo
    assert client.get('/users/me/worst-today?mode=x', headers=A).status_code == 422
    play(client, A, {'mode': 'gto'}, worst=False)
    assert get(client)['errors'] == []                                               # que des bonnes réponses


def test_three_worst_sorted(client):
    for _ in range(2): play(client, A, {'mode': 'gto'})
    e = get(client)['errors']
    assert len(e) == 3 and [x['regret_mbb'] for x in e] == sorted((x['regret_mbb'] for x in e), reverse=True)
    x = e[0]
    assert x['prompt_fr'] and x['chosen_fr'] and x['best_fr'] and x['chosen_fr'] != x['best_fr'] and x['cost_fr'].endswith('BB')
    assert x['verdict'] in ('erreur', 'imprécision') and x['cost_bb'] == round(x['regret_mbb'] / 1000, 2) and x['session_id']


def test_mode_and_placement(client):
    play(client, A, {'mode': 'exploit'})
    assert get(client, 'gto')['errors'] == []                                        # séparé par mode
    ex = get(client, 'exploit')['errors']
    assert ex and all(x['regret_mbb'] > 0 for x in ex)                               # lecture du vilain (sans EV) exclue
    play(client, A, {'mode': 'gto', 'plan': 'placement'})
    assert get(client, 'gto')['errors'] == []                                        # test de placement exclu


def test_timezone(client, tmp_path):
    play(client, A, {'mode': 'gto'})
    now = datetime.datetime.now(datetime.timezone.utc)
    late = (now.replace(hour=23, minute=30, second=0, microsecond=0) - datetime.timedelta(days=1)).isoformat(timespec='seconds')
    con = sqlite3.connect(str(tmp_path / 'test.sqlite')); con.execute('UPDATE attempts SET answered_at = ?', (late,)); con.commit()
    # hier 23 h 30 UTC : aujourd'hui pour un fuseau à + 1 h (si on n'est pas déjà au lendemain là-bas), hier en UTC
    assert get(client, tz=0)['errors'] == []
    if (now + datetime.timedelta(hours=1)).date() == now.date():
        assert get(client, tz=60)['errors']
