import json, os, shutil
import pytest
from fastapi.testclient import TestClient
from spinsacademy import catalog, quiz

ADMIN = {'X-Admin-Token': 'jeton-de-test'}
GTO, OLD, EXP = 'gto_preflop/2026.10.13-3', 'gto_preflop/2026.10.12-1', 'exploit_calls/2026.10.13-4'


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'c.sqlite'))
    monkeypatch.setenv('SPINSACADEMY_ADMIN_TOKEN', ADMIN['X-Admin-Token'])
    monkeypatch.delenv('SPINSACADEMY_ALLOW_STAGING')                      # production : seules les versions publiées sont servies
    from spinsacademy.api import app
    return TestClient(app)


def post(c, path, **body): return c.post(path, json=dict(actor='Expert test', **body), headers=ADMIN)


def test_reports_on_real_datasets():
    assert catalog.validate(GTO)['ok'] and catalog.validate(EXP)['ok']
    old = catalog.validate(OLD)
    assert not old['ok'] and {c['id'] for c in old['checks'] if c['level'] == 'fail'} == {'spots', 'questions'}
    assert {c['id']: c['level'] for c in old['checks']}['rebuild'] == 'warn'          # importeur différent : non comparable, signalé


@pytest.fixture()
def copy(tmp_path, monkeypatch):
    """copie modifiable du dataset GTO dans un répertoire de datasets temporaire"""
    root = tmp_path / 'datasets'; shutil.copytree(quiz.ref_path(GTO), root / GTO)
    monkeypatch.setattr(quiz, 'DATASETS', str(root)); quiz.load.cache_clear()
    yield root / GTO
    quiz.load.cache_clear()


from conftest import needs_raw


@needs_raw
def test_tampered_file_is_rejected(copy):
    lines = open(copy / 'spots.jsonl').read().splitlines()
    sp = json.loads(lines[0]); sp['hands']['AA']['freq'] = [0.2, 0.2]; lines[0] = json.dumps(sp)
    open(copy / 'spots.jsonl', 'w').write('\n'.join(lines) + '\n')
    rep = catalog.validate(GTO); fails = {c['id'] for c in rep['checks'] if c['level'] == 'fail'}
    assert not rep['ok'] and {'integrity', 'spots', 'rebuild'} <= fails
    m = json.load(open(copy / 'manifest.json')); m['spots_sha256'] = catalog._sha(copy / 'spots.jsonl')     # même avec une empreinte recalculée
    json.dump(m, open(copy / 'manifest.json', 'w'))
    rep = catalog.validate(GTO); fails = {c['id'] for c in rep['checks'] if c['level'] == 'fail'}
    assert 'integrity' not in fails and 'spots' in fails and 'rebuild' in fails


def test_nothing_is_served_before_publication(client):
    assert client.post('/sessions', json={}).status_code == 503
    assert client.get('/health').json()['published'] == {'gto_preflop': None, 'exploit_calls': None}
    rows = {r['ref']: r for r in client.get('/admin/datasets', headers=ADMIN).json()}
    assert {r['status'] for r in rows.values()} == {'staging'} and {GTO, OLD, EXP} <= set(rows)
    assert post(client, f'/admin/datasets/{GTO}/publish', reason='trop tôt').status_code == 409     # pas encore contrôlé


def test_full_lifecycle(client):
    assert post(client, f'/admin/datasets/{OLD}/validate').json()['status'] == 'rejected'
    assert post(client, f'/admin/datasets/{OLD}/publish', reason='forcer').status_code == 409
    assert post(client, f'/admin/datasets/{EXP}/validate').json()['status'] == 'validated'
    r = post(client, f'/admin/datasets/{EXP}/publish', reason='source pas publiée')
    assert r.status_code == 409 and 'source' in r.json()['detail']
    assert post(client, f'/admin/datasets/{GTO}/validate').json()['ok']
    assert post(client, f'/admin/datasets/{GTO}/publish', reason='validé par l\'expert').json()['status'] == 'published'
    assert post(client, f'/admin/datasets/{EXP}/publish', reason='validé par l\'expert').status_code == 200
    s = client.post('/sessions', json={'seed': 1}).json(); assert s['dataset_version'] == GTO
    e = client.post('/sessions', json={'mode': 'exploit', 'seed': 1}).json(); assert e['dataset_version'] == EXP
    assert client.get('/quiz/next', params={'session_id': s['session_id']}).status_code == 200
    d = post(client, f'/admin/datasets/{GTO}/disable', reason='erreur détectée').json()
    assert d['also_disabled'] == [EXP]                                                   # l'exploitant dérivé est retiré aussi
    assert client.get('/quiz/next', params={'session_id': s['session_id']}).status_code == 410
    assert client.post('/sessions', json={}).status_code == 503
    assert post(client, f'/admin/datasets/{GTO}/publish', reason='retour arrière après vérification').status_code == 200
    assert client.get('/quiz/next', params={'session_id': s['session_id']}).status_code == 200
    assert client.get(f'/admin/datasets/{GTO}/report', headers=ADMIN).json()['ok']
    log = [x['action'] for x in client.get('/admin/log', headers=ADMIN).json()]
    assert log.count('publish_dataset') == 3 and log.count('disable_dataset') == 1 and log.count('validate_dataset') == 3
    assert client.get('/admin/datasets').status_code == 403


def test_new_publication_retires_previous_and_rollback(tmp_path, monkeypatch, client):
    root = tmp_path / 'datasets'; new = 'gto_preflop/2026.10.13-9'
    shutil.copytree(quiz.ref_path(GTO), root / GTO); shutil.copytree(quiz.ref_path(GTO), root / new)
    m = json.load(open(root / new / 'manifest.json')); m['version'] = '2026.10.13-9'; json.dump(m, open(root / new / 'manifest.json', 'w'))
    monkeypatch.setattr(quiz, 'DATASETS', str(root)); quiz.load.cache_clear()
    for ref in (GTO, new): assert post(client, f'/admin/datasets/{ref}/validate').json()['status'] == 'validated'
    post(client, f'/admin/datasets/{GTO}/publish', reason='première')
    assert post(client, f'/admin/datasets/{new}/publish', reason='nouvelle version').json()['replaced'] == GTO
    st = {r['ref']: r['status'] for r in client.get('/admin/datasets', headers=ADMIN).json()}
    assert st[GTO] == 'retired' and st[new] == 'published'
    assert client.post('/sessions', json={}).json()['dataset_version'] == new
    assert post(client, f'/admin/datasets/{GTO}/publish', reason='retour arrière').json()['replaced'] == new
    shutil.rmtree(root / new)                                                            # dossier supprimé : publication refusée proprement
    assert post(client, f'/admin/datasets/{new}/publish', reason='fichiers absents').status_code == 409
    quiz.load.cache_clear()
