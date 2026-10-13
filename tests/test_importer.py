import json, os
import numpy as np
import pytest
from spinsacademy import importer as im, grading
from spinsacademy.cards import NAMES, W


@pytest.fixture(scope='module')
def built():
    return im.build_dataset()


def test_no_rejection_and_known_trees_only(built):
    spots, rejected, used, skipped = built
    assert not rejected
    assert all(s['provenance']['hrc_preflop_tree'] in im.TREES and s['preflop_tree'] == s['provenance']['hrc_preflop_tree'] for s in spots)
    assert any('min_raise_3way' in d and 'arbre' in r for d, r in skipped)                 # arbre sans limp du BTN : écarté
    assert {s['preflop_tree'] for s in spots} == set(im.TREES)


def test_one_export_per_stack_configuration(built):
    spots, _, used, _ = built
    keys = [(s['preflop_tree'], tuple(s['stacks_bb']), s['node_key']) for s in spots]
    assert len(keys) == len(set(keys))
    assert len({s['spot_id'] for s in spots}) == len(spots)


def test_spots_are_legal_and_normalised(built):
    for s in built[0]:
        hero = s['players'].index(s['hero']); stack = s['stacks_bb'][hero]
        ids = [a['id'] for a in s['actions']]
        assert len(ids) >= 2 and len(set(ids)) == len(ids)
        if s['to_call_bb'] == 0: assert 'F' not in ids
        else: assert 'X' not in ids
        for a in s['actions']:
            if 'to_bb' in a: assert a['to_bb'] <= stack + 1e-6
        assert len(s['hands']) == 169
        for h in s['hands'].values():
            assert abs(sum(h['freq']) - 1) < 2e-3 and len(h['freq']) == len(h['ev_hrc']) == len(ids)


def test_exact_ev_matches_hrc_where_hrc_is_precise(built):
    """à 2 BB heads-up, HRC est précis : le calcul exact (call et shove) doit coïncider à quelques mBB près"""
    for s in built[0]:
        if s['table'] == 'heads-up' and s['stacks_bb'] == [2.0, 2.0] and s['node_key'] in ('root', 'SB-allin'):
            ids = [a['id'] for a in s['actions']]; j = ids.index('A' if s['node_key'] == 'root' else 'C')
            hrc = np.array([s['hands'][x]['ev_hrc'][j] for x in NAMES]); ex = np.array([s['hands'][x]['ev_exact'][j] for x in NAMES], float)
            w = W * np.array([s['hands'][x]['reach'] for x in NAMES])
            assert abs(np.average(hrc - ex, weights=w)) < 0.005 and np.average(np.abs(hrc - ex), weights=w) < 0.015


def test_publish_is_immutable(tmp_path):
    m = im.publish('test-1', str(tmp_path))
    d = tmp_path / 'test-1'
    assert m['status'] == 'staging' and m['spots'] == sum(1 for _ in open(d / 'spots.jsonl'))
    assert json.load(open(d / 'manifest.json'))['spots_sha256'] == m['spots_sha256']
    with pytest.raises(SystemExit):
        im.publish('test-1', str(tmp_path))


def test_grading_rules(built):
    spot = next(s for s in built[0] if s['table'] == 'heads-up' and s['stacks_bb'] == [10.0, 10.0] and s['node_key'] == 'SB-allin')
    assert spot['ev_reference'] == 'exact'
    aa = grading.grade(spot, 'AA', 'C'); assert aa['verdict'] == 'correct' and aa['regret_mbb'] <= 0
    bad = grading.grade(spot, 'AA', 'F'); assert bad['verdict'] == 'erreur' and bad['regret_mbb'] > 1000
    with pytest.raises(ValueError): grading.grade(spot, 'AA', 'X')
    checked = 0
    for mixed in [s for s in built[0] if s['ev_reference'] == 'hrc'][:60]:
        for h in NAMES:
            H = mixed['hands'][h]
            if not H['quiz_eligible']:
                with pytest.raises(ValueError): grading.grade(mixed, h, mixed['actions'][0]['id'])
                continue
            for j, a in enumerate(mixed['actions']):
                r = grading.grade(mixed, h, a['id'])
                if H['freq'][j] >= grading.MIXED_MIN and r['regret_mbb'] <= 3 * grading.TOLERANCE_MBB: assert r['verdict'] == 'correct'
                if r['regret_mbb'] > 3 * grading.TOLERANCE_MBB: assert r['verdict'] == 'erreur'   # la stratégie mixte ne couvre pas une action coûteuse
                checked += 1
    assert checked > 1000


def test_eligibility_excludes_reach_and_inconsistent_hrc(built):
    for s in built[0]:
        for name, h in s['hands'].items():
            ev = grading.reference_ev(s, name)
            mixed_ok = all(f < grading.MIXED_MIN or 1000 * (max(ev) - ev[j]) <= im.MAX_MIXED_REGRET_MBB + 1e-6 for j, f in enumerate(h['freq']))
            assert h['quiz_eligible'] == (h['reach'] >= im.MIN_REACH and h['hrc_self_regret_mbb'] <= im.MAX_SELF_REGRET_MBB and mixed_ok)


def test_mixed_strategy_actions_are_never_penalised(built):
    for s in built[0]:
        for name, h in s['hands'].items():
            if not h['quiz_eligible']: continue
            for j, a in enumerate(s['actions']):
                if grading.reference_freq(s, name)[j] >= grading.MIXED_MIN: assert grading.grade(s, name, a['id'])['verdict'] == 'correct'


def test_displayed_mix_rounds_to_100(built):
    for s in built[0][:40]:
        for h in NAMES:
            mix = grading.displayed_mix(s, h)
            assert sum(p for _, p in mix) == 100 and all(p % grading.DISPLAY_STEP == 0 for _, p in mix)


def test_publication_blocked_by_injected_invalid_spot(tmp_path):
    """un export volontairement corrompu (fréquences d'une main non normalisées) doit bloquer la publication"""
    import shutil
    src = os.path.join(im.ROOT, 'data', 'hrc', 'raw', 'v2', 'hand_8')
    dst = tmp_path / 'raw' / 'v2' / 'hand_8'; shutil.copytree(src, dst)
    f = next(p for p in sorted((dst / 'nodes').iterdir()))
    node = json.load(open(f)); node['hands']['AA']['played'][0] += 0.3; json.dump(node, open(f, 'w'))
    with pytest.raises(SystemExit, match='Publication bloquée'):
        im.publish('x', str(tmp_path / 'out'), raw=str(tmp_path / 'raw'))
    assert not (tmp_path / 'out' / 'x').exists()


def test_publication_blocked_by_illegal_action(tmp_path):
    import shutil
    src = os.path.join(im.ROOT, 'data', 'hrc', 'raw', 'v2', 'hand_8')
    dst = tmp_path / 'raw' / 'v2' / 'hand_8'; shutil.copytree(src, dst)
    for f in sorted((dst / 'nodes').iterdir()):
        node = json.load(open(f))
        r = [a for a in node['actions'] if a['type'] == 'R']
        if r: r[-1]['amount'] *= 3; json.dump(node, open(f, 'w')); break      # relance au-delà du stack
    with pytest.raises(SystemExit, match='au-delà du stack'):
        im.publish('x', str(tmp_path / 'out'), raw=str(tmp_path / 'raw'))
