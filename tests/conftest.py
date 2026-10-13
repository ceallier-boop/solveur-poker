import pytest


@pytest.fixture(autouse=True)
def _staging_fallback(monkeypatch):
    """sans dataset publié dans la base de test, l'API sert les versions par défaut (tests du catalogue : voir test_catalog)"""
    monkeypatch.setenv('SPINSACADEMY_ALLOW_STAGING', '1')
