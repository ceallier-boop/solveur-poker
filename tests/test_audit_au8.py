"""Audit AU8 (06/11/2026) : au niveau 1, les phrases de la correction disent les mots français d'abord"""
import re
import pytest
from fastapi.testclient import TestClient
from spinsacademy import quiz

H = {'X-Player-Id': 'b' * 20}
TERMS = re.compile(r'\b(FOLD|CHECK|CALL|RAISE TO|ALL-IN)\b')


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def _corrections(client, n=6):
    out = []
    for _ in range(n):
        s = client.post('/sessions', json={'mode': 'gto', 'filters': {}}, headers=H).json()
        for i in range(s['size']):
            q = client.get(f"/quiz/next?session_id={s['session_id']}", headers=H).json()['question']
            for o in q['options'][:1]:
                out.append(client.post('/attempts', json={'session_id': s['session_id'], 'question_index': i, 'action_id': o['id']}, headers=H).json())
    return out


def test_level_1_sentences_use_french_words_and_keep_the_client_labels(client):
    assert client.post('/users/me/onboarding', json={'experience': 'debut', 'goal': 'bases'}, headers=H).json()['level'] == 1
    rs = _corrections(client)
    assert rs
    for r in rs:
        text = r['explanation_fr'] + '\n' + r['core_fr'] + '\n' + (r['remember_fr'] or '') + '\n'.join(r['details_fr'] + r['why_fr'])
        for m in TERMS.finditer(text):                                   # un terme du client n'apparaît qu'entre parenthèses
            assert text[max(0, m.start() - 1):m.start()] == '(', (m.group(0), text[max(0, m.start() - 60):m.end() + 20])
        assert 'équité' not in r['essential_fr'] and 'équité' not in r['explanation_fr'].split('\n')[0]
        assert re.match(r'(FOLD|CHECK|CALL|RAISE TO|ALL-IN)', r['best_label']) and re.match(r'(FOLD|CHECK|CALL|RAISE TO|ALL-IN)', r['chosen_label'])   # libellés du client inchangés


def test_level_2_is_untouched(client):
    client.post('/users/me/onboarding', json={'experience': 'confirme', 'goal': 'bases'}, headers=H)
    rs = _corrections(client, 3)
    assert any(re.search(r'\b(FOLD|CALL|ALL-IN)\b', r['explanation_fr']) for r in rs)


def test_simplify_unit():
    t = "Meilleur coup : ALL-IN 4 BB, +3,04 BB par rapport au fold.\nTu perds 3,04 BB par rapport au meilleur coup (ALL-IN 4 BB)."
    out = quiz._plain_terms(t, set())
    assert out.splitlines()[0].startswith('Meilleur coup : Tapis 4 BB (ALL-IN)') and 'au fait de se coucher' in out and '(Tapis 4 BB)' in out
    assert quiz._plain_equity("Il te faut 41,7 % d'équité") == 'Il te faut 41,7 % de chances de gagner'
    assert quiz._plain_terms('RAISE TO 7,6 BB ou CHECK ou FOLD', set()) == 'Relancer à 7,6 BB (RAISE TO) ou Parole (CHECK) ou Se coucher (FOLD)'
