"""Paquet de version (tools/ops/release.sh) : construit depuis HEAD, extrait dans un dossier temporaire, puis lancé avec `python -I`
depuis ce dossier (sans le dépôt dans le chemin) : l'API s'importe, /health répond, et une série de chaque sorte d'équités se joue,
y compris les sortes avec tableau qui utilisent les noyaux numba (spinsacademy/postflop/kernels.py, gardé dans le paquet).
Le test porte sur le dernier commit (git archive) : les changements non commités n'y sont pas."""
import json, os, subprocess, sys, tarfile, time
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SCRIPT = r'''
import json, os, sys, time
sys.path.insert(0, os.getcwd())
t0 = time.time()
from fastapi.testclient import TestClient
import spinsacademy, spinsacademy.api as api
from spinsacademy import equity_quiz
assert os.path.dirname(os.path.abspath(spinsacademy.__file__)).startswith(os.getcwd()), spinsacademy.__file__
out = dict(import_s=round(time.time() - t0, 2), kinds={})
c = TestClient(api.app)
h = c.get('/health'); out['health'] = h.status_code
for kind in equity_quiz.KINDS:
    t = time.time()
    r = c.post('/sessions', json={'mode': 'equity', 'size': 1, 'seed': 3, 'filters': {'kind': kind}}); assert r.status_code == 201, (kind, r.text)
    sid = r.json()['session_id']
    q = c.get('/quiz/next', params={'session_id': sid}).json()['question']
    a = c.post('/attempts', json={'session_id': sid, 'question_index': 0, 'action_id': q['options'][0]['id']}).json()
    assert q['kind'] == kind and a['verdict'] in ('correct', 'imprécision', 'erreur') and a['regret_mbb'] == 0, (kind, a)
    out['kinds'][kind] = round(time.time() - t, 2)
t = time.time(); r = c.post('/sessions', json={'mode': 'equity', 'size': 5, 'seed': 8}); assert r.status_code == 201
out['series5_s'] = round(time.time() - t, 2)
print(json.dumps(out))
'''


def _build(tmp):
    out = tmp / 'dist'
    r = subprocess.run(['bash', 'tools/ops/release.sh', 'HEAD', str(out)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    tgz = next(out.glob('spinsacademy-HEAD.tar.gz'))
    with tarfile.open(tgz) as t: t.extractall(tmp / 'x', filter='data')
    return tmp / 'x' / 'spinsacademy-HEAD'


def test_release_package_runs_equities(tmp_path):        # environ 20 s, compilation numba comprise (cache vide) : suite rapide
    t0 = time.time()
    pkg = _build(tmp_path)
    assert not (pkg / 'spinsacademy' / 'solver').exists() and not (pkg / 'data' / 'hrc').exists() and not (pkg / 'tests').exists()
    assert sorted(p.name for p in (pkg / 'spinsacademy' / 'postflop').iterdir()) == ['__init__.py', 'kernels.py']
    assert json.loads((pkg / 'RELEASE.json').read_text())['tag'] == 'HEAD'
    assert 'numba' in (pkg / 'requirements-app.txt').read_text() and 'numba==' in (pkg / 'requirements-app.lock').read_text()
    env = dict(os.environ, SPINSACADEMY_DB=str(tmp_path / 'app.sqlite'), SPINSACADEMY_ALLOW_STAGING='1', SPINSACADEMY_RATE_LIMIT='0',
               NUMBA_CACHE_DIR=str(tmp_path / 'numba-cache'))
    env.pop('PYTHONPATH', None)
    r = subprocess.run([sys.executable, '-I', '-c', SCRIPT], cwd=pkg, env=env, capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-4000:]
    res = json.loads(r.stdout.strip().splitlines()[-1])
    assert res['health'] == 200 and set(res['kinds']) == {'hit', 'equity', 'labels', 'outs', 'board_equity', 'flop_help', 'range_help', 'nut_help'}
    print(json.dumps(dict(res, total_s=round(time.time() - t0, 1))))
