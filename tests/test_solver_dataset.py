"""Banque GTO produite par le solveur maison (spinsacademy.solver.dataset) : format, contrôles, publication, reconstruction."""
import json, os
import numpy as np
import pytest
from spinsacademy import catalog, quiz
from spinsacademy.cards import NAMES, W
from spinsacademy.solver import dataset as ds
from spinsacademy.solver.tree import Tree
from conftest import needs_raw

FAST = ds.SolveParams(model='showdown', pre_iters=2000)            # préflop seul : quelques secondes en heads-up


@pytest.fixture(scope='module')
def hu12(tmp_path_factory):
    runs = str(tmp_path_factory.mktemp('runs'))
    return ds.run((12.0, 12.0), ds.TreeConfig(), FAST, runs=runs, log=None), runs


def test_grid_and_config_names():
    assert len(ds.GRID_P1) == 58 and len({st for _, st in ds.GRID_P1}) == 58
    assert ds.parse_configs('hu:12-12,3w:35-25-15') == [(12.0, 12.0), (35.0, 25.0, 15.0)]
    assert ds.config_name((35.0, 25.0, 15.0)) == '3w_35-25-15'
    with pytest.raises(ValueError): ds.parse_configs('hu:12-12-12')
    assert ds.tree_id(ds.TreeConfig()) == 'daa9aaa0' and ds.tree_id(ds.TreeConfig(open_btn=2.0)).startswith('s')


def test_nodes_follow_the_export_format(hu12):
    (res, path), _ = hu12
    tree = Tree((12.0, 12.0))
    assert set(res['nodes']) == {n.key for n in tree.decisions()}
    for key, n in res['nodes'].items():
        assert len(n['hands']) == 169 and len(n['actions']) == len(tree.by_key()[key].actions)
        for h in n['hands'].values(): assert abs(sum(h['played']) - 1) < 1e-4
    lim = res['nodes']['SB-call']                                       # le SB complète : 5 000 jetons de plus, rien d'autre
    assert lim['sequence'] == [dict(player=0, type='C', amount=5000)] and lim['player'] == 1


def test_spots_have_the_bank_format_and_the_reference_ids(hu12):
    (res, path), _ = hu12
    spots, skipped = ds.spots_of(res, path)
    assert spots and all(sp['provenance']['source'] == 'solveur' for sp in spots)
    published = {json.loads(l)['spot_id'] for l in open(os.path.join(quiz.ref_path('gto_preflop/2026.10.13-3'), 'spots.jsonl'))}
    assert {sp['spot_id'] for sp in spots} <= published                   # même situation, même identifiant que la référence
    call = next(sp for sp in spots if sp['node_key'] == 'SB-allin')
    assert call['ev_reference'] == 'exact'
    for h in NAMES:                                                    # heads-up : l'EV du solveur est l'EV exacte (même matrice d'équité)
        H = call['hands'][h]; assert abs(H['ev_hrc'][1] - H['ev_exact'][1]) < 2e-3


def test_saved_runs_are_reused(hu12):
    (res, path), runs = hu12
    seen = []
    again, p2 = ds.run((12.0, 12.0), ds.TreeConfig(), FAST, runs=runs, log=seen.append)
    assert p2 == path and not seen and again == res


def test_unconverged_solve_is_refused(tmp_path):
    with pytest.raises(SystemExit, match='Exploitabilité'):
        ds.publish('v-1', str(tmp_path / 'out'), [(12.0, 12.0)], params=ds.SolveParams(model='showdown', pre_iters=5), runs=str(tmp_path), log=None)


def test_published_solver_bank_passes_the_catalog_and_rebuilds(tmp_path, monkeypatch):
    runs = os.path.join(quiz.ROOT, 'data', 'solver', 'runs')                   # chemins de provenance relatifs au dépôt
    out = tmp_path / 'datasets' / 'gto_preflop'
    m = ds.publish('test-s1', str(out), [(12.0, 12.0), (8.0, 4.0)], params=FAST, runs=runs, log=None)
    try:
        assert m['source'] == 'solveur' and m['spots'] > 0 and len(m['configs']) == 2
        monkeypatch.setattr(quiz, 'DATASETS', str(tmp_path / 'datasets')); quiz.load.cache_clear()
        rep = catalog.validate('gto_preflop/test-s1'); lv = {c['id']: c['level'] for c in rep['checks']}
        assert rep['ok'] and lv['rebuild'] == 'ok' and lv['solver'] == 'ok', rep
        lines = open(out / 'test-s1' / 'spots.jsonl').read().splitlines()
        sp = json.loads(lines[0]); sp['hands']['AA']['freq'] = [1.0] + [0.0] * (len(sp['actions']) - 1); lines[0] = json.dumps(sp)
        open(out / 'test-s1' / 'spots.jsonl', 'w').write('\n'.join(lines) + '\n')
        mm = json.load(open(out / 'test-s1' / 'manifest.json')); mm['spots_sha256'] = catalog._sha(out / 'test-s1' / 'spots.jsonl')
        json.dump(mm, open(out / 'test-s1' / 'manifest.json', 'w'))
        rep = catalog.validate('gto_preflop/test-s1'); lv = {c['id']: c['level'] for c in rep['checks']}
        assert not rep['ok'] and lv['rebuild'] == 'fail'                       # écart avec les résultats enregistrés du solveur
    finally:
        quiz.load.cache_clear()
        for r in m['sources']: os.remove(os.path.join(quiz.ROOT, r))
        d = os.path.dirname(os.path.join(quiz.ROOT, m['sources'][0]))
        if not os.listdir(d): os.rmdir(d)


@needs_raw
def test_calibration_against_the_reference(hu12):
    (res, _), _ = hu12
    cal = ds.calibrate(res)
    assert cal['exports'] == ['data/hrc/raw/v3/hand_13'] and cal['nodes'] == 8 and cal['outside'] == 0
    assert cal['loss_mbb'] >= cal['floor_mbb'] > 0 and 50 < cal['agree'] <= 100
    assert ds.calibrate(dict(res, stacks=[13.0, 13.0])) is None                 # pas de référence à 13 BB


def test_preflop_solve_matches_push_fold_where_it_should(hu12):
    """à 12 BB, le BB paie le tapis du SB avec une range du même ordre que l'équilibre push/fold (≈ 33 %)"""
    (res, _), _ = hu12
    n = res['nodes']['SB-allin']; call = np.array([n['hands'][h]['played'][1] for h in NAMES])
    assert 25 < 100 * float((W * call).sum() / W.sum()) < 40


def test_linear_averaging_of_postflop_corrections():
    """'linear' : après k tours, la correction est la moyenne des tours pondérée par leur numéro (1, 2, …, k)"""
    from spinsacademy.solver.postflop import Realization

    class Nd: id = 7
    m = Realization(); vals = [np.full(169, x) for x in (3.0, 0.0, 6.0)]
    for v in vals:
        m.store(Nd, 0, 1, v, -v, 'linear'); m.commit('linear')
    assert np.allclose(m.offsets[7][0], (1 * 3 + 2 * 0 + 3 * 6) / 6) and np.allclose(m.offsets[7][1], -(1 * 3 + 3 * 6) / 6)
    m = Realization()
    for v in vals[:2]:
        m.store(Nd, 0, 1, v, -v, 0.5); m.commit(0.5)
    assert np.allclose(m.offsets[7][0], 1.5)                                    # amortissement fixe : inchangé
