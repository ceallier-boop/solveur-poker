"""Nom de l'application (23/11 : SpinXpresso, « Poker Trainer ») : une seule source, <meta name="application-name"> d'index.html.
Le manifest servi, le titre de l'onglet et la page d'administration suivent ; l'ancien nom n'apparaît plus dans ce que voit le joueur ;
les noms internes (module Python, clés de stockage local) restent « spinsacademy », pour que les testeurs gardent leur progression."""
import json, os, re
import pytest
from fastapi.testclient import TestClient

WEB = os.path.join(os.path.dirname(__file__), '..', 'spinsacademy', 'web')
read = lambda f: open(os.path.join(WEB, f), encoding='utf-8').read()


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'b.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def meta():
    m = re.search(r'<meta name="application-name" content="([^"]+)" data-tagline="([^"]*)" data-slug="([^"]+)">', read('index.html'))
    assert m, 'index.html doit porter <meta name="application-name" content=… data-tagline=… data-slug=…>'
    return m.groups()


def test_one_source_for_the_name():
    name, tagline, slug = meta()
    assert name == 'SpinXpresso' and tagline == 'Poker Trainer' and slug == 'spinxpresso'
    html = read('index.html')
    assert f'<title>{name} · {tagline}</title>' in html                   # le seul doublon : le titre avant le script
    assert html.count(name) == 2                                          # la balise meta et ce titre, rien d'autre en dur
    assert 'data-brand' in html and 'BRAND.name' in read('app.js')
    assert f'<title>{name} · Signalements</title>' in read('admin.html')


def test_manifest_follows_index(client):
    name, tagline, _ = meta()
    m = client.get('/manifest.json')
    assert m.status_code == 200 and 'manifest' in m.headers['content-type']
    j = m.json(); assert j['short_name'] == name and j['name'] == f'{name} · {tagline}' and j['start_url'] == '/'


def test_old_name_gone_from_what_players_see():
    for f in ('index.html', 'app.js', 'app.css', 'admin.html', 'lexique.json', 'sw.js', 'conseil.html'):
        assert not re.search(r'Spins ?Academy', read(f)), f
    assert not os.path.exists(os.path.join(WEB, 'manifest.json'))         # remplacé par /manifest.json (nom d'index.html)


def test_internal_storage_keys_unchanged():
    js = read('app.js')
    assert "a.download = `${BRAND.slug}-mes-donnees.json`" in js           # l'export prend le nouveau nom
    assert "store.get('player_id')" in js or "'player_id'" in js           # l'identifiant du joueur garde sa clé : la progression reste
    assert not re.search(r"(store\.(get|set|del)|localStorage\.\w+Item)\([^)]*BRAND", js)   # le nom n'entre dans aucune clé de stockage
    assert not re.search(r"store\.(get|set|del)\('spinxpresso", js)
