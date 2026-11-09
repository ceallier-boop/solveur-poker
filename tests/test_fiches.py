"""N3 « fiches à emporter » (tools/solver/build_fiches.py) : fiches.json se régénère à l'identique depuis la banque, fréquences cohérentes,
noms d'action de l'application, aucun nom d'expert, taille bornée."""
import importlib.util, json, os, re
import pytest
from spinsacademy import quiz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'spinsacademy', 'data', 'fiches.json')
spec = importlib.util.spec_from_file_location('build_fiches', os.path.join(ROOT, 'tools', 'solver', 'build_fiches.py'))
bf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bf)


@pytest.fixture(scope='module')
def data():
    return json.load(open(PATH, encoding='utf-8'))


def test_file_is_regenerated_identically_from_the_bank():
    text = json.dumps(bf.build(), ensure_ascii=False, separators=(',', ':'))
    assert text == open(PATH, encoding='utf-8').read()


def test_selection_follows_the_rules(data):
    fs = data['fiches']
    assert len(fs) == 342 and [f['order'] for f in fs] == list(range(342))
    assert len({f['id'] for f in fs}) == 342
    for f in fs:
        assert f['stack'] <= 16 and f['stack'] >= (2 if f['reliability'] == 'tapis' else 8)
        assert f['table'] in ('heads-up', '3-handed') and f['node'] in ('first_in', 'vs_limp', 'vs_raise', 'vs_allin')
        assert f['title_fr'].startswith(('Heads-up, ', '3 joueurs, ')) and f" {f['stack']} BB · " in f['title_fr']
    assert {f['reliability'] for f in fs} == {'tapis', 'flop'}
    # approximation : une entrée par table et profondeur « flop », avec l'écart mesuré
    for f in fs:
        if f['reliability'] == 'flop': assert str(f['stack']) in data['approximation'][f['table']]
    assert all({'perte_mbb', 'plancher_mbb', 'accord_pct', 'note_fr'} <= set(a) for t in data['approximation'].values() for a in t.values())


def test_frequencies_sum_to_100_on_reached_hands_and_dead_hands_are_not_flagged(data):
    for f in data['fiches']:
        dead = bf.dead_set(f['dead'])
        assert len(f['f']) == len(f['actions']) >= 2 and all(len(row) == 169 for row in f['f'])
        for i in range(169):
            tot = sum(row[i] for row in f['f'])
            if i in dead: assert tot == 0, (f['id'], i)
            else: assert 99 <= tot <= 101, (f['id'], data['hands'][i], tot)
        assert all(data['hands'].index(e['hand']) not in dead for e in f['expert_hands'])


def test_action_names_are_the_application_names_and_every_action_has_a_row(data):
    _, spots = quiz.load(data['bank'])
    for f in data['fiches']:
        sp = spots[f['id']]
        assert f['actions'] == [quiz.action_label(sp, a) for a in sp['actions']]


def test_expert_hands_are_numbers_only_and_differ_from_the_bank(data):
    n = 0
    for f in data['fiches']:
        for e in f['expert_hands']:
            n += 1
            assert set(e['experts']) <= set(f['actions']) and all(isinstance(v, int) and 1 <= v <= 3 for v in e['experts'].values())
            assert e['recommended'] != e['bank'] or len(e['experts']) > 1          # diffère de la banque, ou experts partagés
    assert n > 0


def test_no_expert_name_nor_brand_in_the_file(data):
    text = open(PATH, encoding='utf-8').read()
    assert not re.search(r'hrc|holdem resources|coach|lucho|lucky|pasg8|spinpro|kill tilt|professionnels', text, re.I)


def test_size_stays_under_500_ko():
    assert os.path.getsize(PATH) < 500_000
