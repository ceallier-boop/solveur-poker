"""Banques du solveur en test fermé (décision du porteur du 05/11, docs/produit/DECISIONS_2026-11-05.md §4 ; P15) : chaque banque
porte sa version et son empreinte, reste en « staging » tant qu'elle n'est pas publiée, et n'est jamais servie avant.
Non-régression préparée avant P15 : quand Plan publiera la banque du test fermé, test_served_version_is_the_default_reference
devra suivre la version servie (et vérifier qu'elle porte le manifeste et l'empreinte attendus)."""
import hashlib, json, os, sqlite3
import pytest
from fastapi.testclient import TestClient
from spinsacademy import catalog, quiz

GTO = os.path.join(quiz.DATASETS, 'gto_preflop')
CLOSED_TEST = 'gto_preflop/2026.11.02-s2'
CLOSED_TEST_SHA = '4656a71d3f2cff0a6b0a4bdf2a8bdab8ee3fd2277ee6b0a414e469234bed4a12'   # empreinte des spots au 03/11 : une version est immuable


def manifest(version):
    with open(os.path.join(GTO, version, 'manifest.json'), encoding='utf-8') as f: return json.load(f)


SOLVER_BANKS = sorted(v for v in os.listdir(GTO) if os.path.isfile(os.path.join(GTO, v, 'manifest.json')) and manifest(v).get('source') == 'solveur')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''): h.update(block)
    return h.hexdigest()


def test_closed_test_bank_is_a_solver_bank():
    assert CLOSED_TEST.split('/')[1] in SOLVER_BANKS


@pytest.mark.parametrize('version', SOLVER_BANKS)
def test_solver_bank_manifest_and_fingerprint(version):
    m = manifest(version); path = os.path.join(GTO, version, 'spots.jsonl')
    assert (m['dataset'], m['version'], m['status']) == ('gto_preflop', version, 'staging')
    assert m['spots_sha256'] == sha256(path), 'spots modifiés après génération'
    with open(path, encoding='utf-8') as f: spots = [json.loads(line) for line in f]
    assert len(spots) == m['spots'] and len({s['spot_id'] for s in spots}) == m['spots']
    assert all(s['provenance']['source'] == 'solveur' and s['provenance']['solver'] == m['solver'] for s in spots), 'provenance de chaque spot'


def test_closed_test_bank_fingerprint_is_pinned():
    assert manifest(CLOSED_TEST.split('/')[1])['spots_sha256'] == CLOSED_TEST_SHA, \
        'la banque du test fermé a changé sous la même version : une nouvelle banque doit porter une nouvelle version'


@pytest.fixture()
def con(tmp_path):
    c = sqlite3.connect(tmp_path / 'catalog.sqlite'); c.row_factory = sqlite3.Row
    c.executescript(catalog.SCHEMA); catalog.sync(c)
    yield c
    c.close()


def test_solver_banks_stay_in_staging_and_cannot_be_published_unchecked(con):
    for v in SOLVER_BANKS:
        assert catalog.status_of(con, f'gto_preflop/{v}') == 'staging'
        with pytest.raises(catalog.LifecycleError): catalog.publish(con, f'gto_preflop/{v}', 'test', 'publication sans contrôle')
    assert catalog.active(con, 'gto_preflop') is None


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_nothing_served_before_publication(client, monkeypatch):
    monkeypatch.delenv('SPINSACADEMY_ALLOW_STAGING')
    r = client.post('/sessions', json={'seed': 1})
    assert r.status_code == 503, 'sans version publiée, aucune banque (solveur comprise) ne doit être servie'


def test_served_version_is_the_default_reference(client):
    """développement (SPINSACADEMY_ALLOW_STAGING=1) : la version servie est la référence par défaut, jamais une banque du solveur"""
    r = client.post('/sessions', json={'seed': 1}); assert r.status_code == 201
    v = r.json()['dataset_version']
    assert v == quiz.DEFAULT_VERSION and v.split('/')[-1] not in SOLVER_BANKS
