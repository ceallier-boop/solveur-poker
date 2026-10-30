"""Moyenne des exports répétés d'un même calcul (importeur 1.5.0, commande v4 §10.3 B et §10.6)."""
import copy, os
import numpy as np
import pytest
from spinsacademy import hrc, importer as im
from spinsacademy.cards import NAMES

PRECISION = os.path.join(hrc.ROOT, 'data', 'hrc', 'tests', 'precision_v1')     # 4 exports identiques heads-up 12 / 12 (hand_1 à hand_4)


def _node(weight, played, evs):
    return dict(player=1, sequence=[dict(player=0, type='C', amount=5000)], actions=[dict(type='X', amount=0), dict(type='R', amount=30000)],
                hands={'AA': dict(weight=weight, played=played, evs=evs)})


def test_average_weights_frequencies_by_reach_and_keeps_the_tree_coherent():
    s = dict(engine='mc', handdata=dict(stacks=[120000, 120000]))
    runs = [(s, [12.0, 12.0], dict(n=_node(1.0, [1.0, 0.0], [0.0, 1.0]))), (s, [12.0, 12.0], dict(n=_node(0.0, [0.0, 1.0], [0.0, 3.0]))),
            (s, [12.0, 12.0], dict(n=_node(0.5, [0.0, 1.0], [0.0, 2.0])))]
    H = hrc.average(runs)['n']['hands']['AA']
    assert H['weight'] == pytest.approx(0.5)
    assert H['played'] == pytest.approx([2 / 3, 1 / 3])               # la répétition où AA n'atteint pas le nœud ne compte pas
    w = [1.0, 0.0, 0.5]; p1 = [0.0, 1.0, 1.0]                          # poids moyen × fréquence moyenne = poids moyen du fils
    assert H['weight'] * H['played'][1] == pytest.approx(np.mean([a * b for a, b in zip(w, p1)]))
    assert H['evs'] == pytest.approx([0.0, 2.0]) and H['evs_se'] == pytest.approx([0.0, 1 / np.sqrt(3)])
    assert hrc.average(runs)['n']['repetitions'] == 3


def test_average_refuses_runs_that_are_not_the_same_computation():
    s = dict(engine='mc', handdata=dict(stacks=[120000, 120000]))
    other = _node(1.0, [1.0, 0.0], [0.0, 1.0]); other['actions'][1]['amount'] = 25000
    with pytest.raises(ValueError):
        hrc.average([(s, [12.0, 12.0], dict(n=_node(1.0, [1.0, 0.0], [0.0, 1.0]))), (s, [12.0, 12.0], dict(n=other))])
    with pytest.raises(ValueError):
        hrc.average([(s, [12.0, 12.0], {}), (dict(s, engine='enumerated'), [12.0, 12.0], {})])


def test_exports_accept_v4_names_in_natural_order(tmp_path):
    for i in (1, 2, 10):
        (tmp_path / 'v4' / f'hu_12-12_r{i}').mkdir(parents=True); (tmp_path / 'v4' / f'hu_12-12_r{i}' / 'settings.json').write_text('{}')
    (tmp_path / 'v3' / 'hand_1').mkdir(parents=True); (tmp_path / 'v3' / 'hand_1' / 'settings.json').write_text('{}')
    assert [os.path.relpath(d, tmp_path) for d in hrc.exports(str(tmp_path))] == ['v4/hu_12-12_r1', 'v4/hu_12-12_r2', 'v4/hu_12-12_r10', 'v3/hand_1']


def _raw(tmp_path, n):
    root = tmp_path / f'raw{n}' / 'v4'; root.mkdir(parents=True)
    for i in range(1, n + 1): os.symlink(os.path.join(PRECISION, f'hand_{i}'), root / f'hu_12-12_r{i}')
    return str(root.parent)


def _exact_error(spots):
    """écart |EV de référence − EV exacte| (mBB), pire action, mains atteintes à 5 % au moins"""
    out = []
    for sp in spots:
        if sp['ev_reference'] != 'exact': continue
        for h in NAMES:
            H = sp['hands'][h]
            if H['reach'] < 0.05: continue
            d = [abs(a - b) for a, b in zip(H['ev_hrc'], H['ev_exact']) if b is not None]
            out.append(1000 * max(d))
    return np.array(out)


def test_importer_averages_repetitions_and_reduces_the_noise(tmp_path, monkeypatch):
    monkeypatch.setitem(im.TREES, hrc.preflop_hash(hrc.load(os.path.join(PRECISION, 'hand_1'))[0]), 'test de précision')
    one, _, used1, _ = im.build_dataset(_raw(tmp_path, 1))
    four, rejected, used4, skipped = im.build_dataset(_raw(tmp_path, 4))
    assert not rejected and len(used4) == 4 and not any('déjà couverts' in r for _, r in skipped)
    assert {sp['node_key'] for sp in four} == {sp['node_key'] for sp in one}
    for sp in four:
        assert sp['provenance']['repetitions'] == 4 and len(sp['provenance']['exports']) == 4
        for h in sp['hands'].values():
            assert len(h['ev_hrc_se']) == len(h['ev_hrc']) and min(h['ev_hrc_se']) >= 0
            assert abs(sum(h['freq']) - 1) < 2e-3
    assert 'ev_hrc_se' not in one[0]['hands']['AA'] and one[0]['provenance']['repetitions'] == 1
    e1, e4 = _exact_error(one), _exact_error(four)
    assert np.median(e4) < 0.7 * np.median(e1)                         # bruit aléatoire : divisé par environ √4 (mesuré : 100 → 42 mBB)


def test_spot_from_one_export_is_unchanged_by_the_averaging_code(tmp_path, monkeypatch):
    """une seule répétition : average n'est pas appelé, le spot ne porte ni erreur type ni autre champ nouveau qu'en provenance"""
    monkeypatch.setitem(im.TREES, hrc.preflop_hash(hrc.load(os.path.join(PRECISION, 'hand_1'))[0]), 'test de précision')
    s, st, nodes = hrc.load(os.path.join(PRECISION, 'hand_1'))
    direct = {k: im.build_spot(os.path.join(PRECISION, 'hand_1'), st, copy.deepcopy(nodes), k, s, 'x') for k in nodes}
    for sp in im.build_dataset(_raw(tmp_path, 1))[0]:
        assert sp['hands'] == direct[sp['node_key']]['hands']
