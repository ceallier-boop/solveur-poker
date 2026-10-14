import pytest
from fastapi.testclient import TestClient
from spinsacademy import ratelimit


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    monkeypatch.setenv('SPINSACADEMY_RATE_LIMIT', '0.1')             # plafonds divisés par 10 : 30 par adresse, 12 par joueur, 3 séries
    ratelimit.reset()
    from spinsacademy.api import app
    yield TestClient(app)
    ratelimit.reset()


def test_series_creation_is_capped_per_player(client):
    h = {'X-Player-Id': 'b' * 32}
    codes = [client.post('/sessions', json={'seed': i, 'adaptive': False}, headers=h).status_code for i in range(4)]
    assert codes == [201, 201, 201, 429]
    r = client.post('/sessions', json={'seed': 9}, headers=h)
    assert r.status_code == 429 and int(r.headers['Retry-After']) >= 1 and 'Trop de requêtes' in r.json()['detail']
    assert client.post('/sessions', json={'seed': 9, 'adaptive': False}, headers={'X-Player-Id': 'c' * 32}).status_code == 201   # autre joueur


def test_ip_cap_and_exemptions(client):
    for _ in range(40): assert client.get('/health').status_code == 200                 # non limitée
    codes = [client.get('/profiles').status_code for _ in range(31)]
    assert codes.count(200) == 30 and codes[-1] == 429


def test_window_slides(monkeypatch):
    ratelimit.reset(); monkeypatch.setenv('SPINSACADEMY_RATE_LIMIT', '0.1')
    assert all(ratelimit.check('GET', '/profiles', '1.2.3.4', None, now=t) is None for t in range(30))
    assert ratelimit.check('GET', '/profiles', '1.2.3.4', None, now=30) == 30
    assert ratelimit.check('GET', '/profiles', '1.2.3.4', None, now=61) is None          # la première requête est sortie de la fenêtre
    ratelimit.reset()


def test_forwarded_for_only_behind_proxy(monkeypatch):
    hdr = {'x-forwarded-for': '9.9.9.9, 5.6.7.8'}
    monkeypatch.delenv('SPINSACADEMY_TRUST_PROXY', raising=False)
    assert ratelimit.client_ip(hdr, '127.0.0.1') == '127.0.0.1'
    monkeypatch.setenv('SPINSACADEMY_TRUST_PROXY', '1')
    assert ratelimit.client_ip(hdr, '127.0.0.1') == '5.6.7.8'
