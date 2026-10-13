import glob, gzip, os, sqlite3, subprocess, sys, threading
from fastapi.testclient import TestClient

TOOL = os.path.join(os.path.dirname(__file__), '..', 'tools', 'ops', 'backup.py')
ME = {'X-Player-Id': 'appareil-sauvegarde-01'}


def run(*args, env=None):
    return subprocess.run([sys.executable, TOOL, *args], capture_output=True, text=True, env={**os.environ, **(env or {})})


def play(c, n):
    for k in range(n):
        sid = c.post('/sessions', json={'seed': k, 'size': 2}, headers=ME).json()['session_id']
        for i in range(2):
            q = c.get('/quiz/next', params={'session_id': sid}).json()
            c.post('/attempts', json={'session_id': sid, 'question_index': i, 'action_id': q['question']['options'][0]['id']})


def count(db): return sqlite3.connect(db).execute('SELECT COUNT(*) FROM attempts').fetchone()[0]


def test_hot_backup_verify_restore(tmp_path, monkeypatch):
    db = str(tmp_path / 'app.sqlite'); bdir = str(tmp_path / 'sauvegardes')
    monkeypatch.setenv('SPINSACADEMY_DB', db)
    from spinsacademy.api import app
    c = TestClient(app); play(c, 3)
    writer = threading.Thread(target=play, args=(c, 5)); writer.start()                 # écritures pendant la sauvegarde
    r = run('backup', '--db', db, '--dir', bdir); writer.join()
    assert r.returncode == 0, r.stderr
    f = glob.glob(os.path.join(bdir, '*.sqlite.gz'))[0]
    assert run('verify', f).returncode == 0
    open(tmp_path / 'b.sqlite', 'wb').write(gzip.open(f).read())
    n_saved = count(tmp_path / 'b.sqlite'); assert 6 <= n_saved <= 16
    play(c, 2); assert count(db) == 20
    r = run('restore', f, '--db', db); assert r.returncode == 0, r.stderr
    assert count(db) == n_saved and glob.glob(db + '.avant-restauration-*')            # l'ancienne base est conservée
    assert c.get('/users/me/stats', headers=ME).json()['questions'] == n_saved           # l'application relit la base restaurée


def test_tampered_or_corrupt_backup_is_refused(tmp_path):
    db = tmp_path / 'x.sqlite'; con = sqlite3.connect(db); con.execute('CREATE TABLE sessions(id)'); con.commit(); con.close()
    bdir = str(tmp_path / 's')
    assert run('backup', '--db', str(db), '--dir', bdir).returncode == 1                 # tables de l'application absentes : refusée
    f = tmp_path / 's' / 'spinsacademy-20260101T000000Z.sqlite.gz'; os.makedirs(f.parent, exist_ok=True)
    f.write_bytes(gzip.compress(b'pas une base')); r = run('verify', str(f))
    assert r.returncode != 0


def test_retention_keeps_minimum(tmp_path, monkeypatch):
    db = str(tmp_path / 'app.sqlite'); monkeypatch.setenv('SPINSACADEMY_DB', db)
    from spinsacademy.api import connect
    connect().close()
    bdir = tmp_path / 's'; bdir.mkdir()
    for d in range(1, 11): (bdir / f'spinsacademy-202501{d:02d}T000000Z.sqlite.gz').write_bytes(b'x')      # vieilles sauvegardes
    assert run('backup', '--db', db, '--dir', str(bdir), '--keep', '30', '--min', '7').returncode == 0
    assert len(glob.glob(str(bdir / '*.sqlite.gz'))) == 7                                   # la plus récente + 6 anciennes
