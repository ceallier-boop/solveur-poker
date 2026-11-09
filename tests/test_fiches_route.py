"""Rythme N3 : la route /fiches sert le fichier des fiches à emporter"""
import json
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_fiches_route_serves_the_generated_file(client):
    r = client.get('/fiches')
    assert r.status_code == 200 and r.headers['content-type'].startswith('application/json') and 'max-age' in r.headers['cache-control']
    d = r.json()
    assert d['version'] == 1 and len(d['hands']) == 169 and len(d['fiches']) == 342 and d['bank'].startswith('gto_preflop/')
    f = d['fiches'][0]
    assert set(f) >= {'id', 'order', 'title_fr', 'table', 'stack', 'hero', 'node', 'reliability', 'actions', 'f', 'dead', 'expert_hands'} and len(f['f']) == len(f['actions'])
    assert not any('coach' in json.dumps(f).lower() for f in d['fiches'])
