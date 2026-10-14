import os
import pytest
from spinsacademy.hrc import RAW

HAS_RAW = os.path.isdir(RAW) and any(os.scandir(RAW))
# exports HRC bruts : présents dans le dépôt, absents des archives d'audit et des livraisons ; sans eux, test ignoré (pas en échec)
needs_raw = pytest.mark.skipif(not HAS_RAW, reason='exports HRC bruts absents (data/hrc/raw) : reconstruction depuis les sources impossible')


@pytest.fixture(autouse=True)
def _staging_fallback(monkeypatch):
    """sans dataset publié dans la base de test, l'API sert les versions par défaut (tests du catalogue : voir test_catalog)"""
    monkeypatch.setenv('SPINSACADEMY_ALLOW_STAGING', '1')


@pytest.fixture(autouse=True)
def _no_rate_limit(monkeypatch):
    """limitation des requêtes coupée dans les tests (sauf test_ratelimit, qui la remet)"""
    monkeypatch.setenv('SPINSACADEMY_RATE_LIMIT', '0')
