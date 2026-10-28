"""Conseiller préflop (/conseil) : les données servies suivent la stratégie du quiz (arbre retenu, stratégie de référence)."""
import json, os
import pytest
from fastapi.testclient import TestClient
from spinsacademy import grading, quiz
from spinsacademy.cards import NAMES

DIR = os.path.join(os.path.dirname(__file__), '..', 'spinsacademy', 'web', 'conseil')


def _index(): return json.load(open(os.path.join(DIR, 'index.json')))


def test_index_matches_served_dataset():
    idx = _index()
    assert idx['dataset'] == f'gto_preflop/{quiz.DEFAULT_VERSION}' and idx['hands'] == NAMES
    _, spots = quiz.load()
    main = [sp for sp in spots.values() if quiz.in_main_tree(quiz.DEFAULT_VERSION, sp)]
    assert sum(c['spots'] for c in idx['configs']) == len(main)
    assert {(c['table'], tuple(c['stacks'])) for c in idx['configs']} == {(sp['table'], tuple(sp['stacks_bb'])) for sp in main}


def test_hands_follow_reference_strategy():
    _, spots = quiz.load()
    for c in _index()['configs'][::9]:
        data = json.load(open(os.path.join(DIR, c['file'] + '.json')))
        for sp in spots.values():
            if (sp['table'], tuple(sp['stacks_bb'])) != (c['table'], tuple(c['stacks'])) or not quiz.in_main_tree(quiz.DEFAULT_VERSION, sp): continue
            e = data['spots'][sp['node_key']]; n = len(sp['actions'])
            assert e['hero'] == sp['hero'] and len(e['acts']) == n
            for i, h in enumerate(NAMES):
                x = e['hands'][i]
                if sp['hands'][h]['reach'] < 0.05: assert x is None; continue
                f = grading.reference_freq(sp, h); ev = grading.reference_ev(sp, h)
                assert x[1:1 + n] == [round(100 * v) for v in f]
                assert x[1 + n:] == [round(100 * v) for v in ev]


def test_action_kinds():
    data = json.load(open(os.path.join(DIR, '3w-20-20-20.json')))['spots']
    assert [a['k'] for a in data['root']['acts']] == ['fold', 'limp', 'raise']
    assert [a['k'] for a in data['BTN-fold_SB-call_BB-raise3']['acts']] == ['fold', 'call', 'raise', 'shove']


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_page_and_data_served(client):
    r = client.get('/conseil'); assert r.status_code == 200 and 'static/conseil/' in r.text
    assert client.get('/static/conseil/index.json').status_code == 200
