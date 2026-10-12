import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'hrc'))
import make_locks as ml


def _nodes():
    for d in sorted(glob.glob(os.path.join(ml.RAW, '*', 'hand_*'))):
        s = json.load(open(os.path.join(d, 'settings.json')))
        if ml.tree_hash(s) != ml.REF_TREE: continue
        st = [x / 10000 for x in s['handdata']['stacks']]
        for f in glob.glob(os.path.join(d, 'nodes', '*.json')):
            n = json.load(open(f))
            if len(n['actions']) >= 2: yield st, n


def test_deformation_reaches_target_and_stays_normalised():
    checked = 0
    for st, n in _nodes():
        for prof in ml.PROFILES.values():
            r = ml.deform(n, st, prof)
            if r is None: continue
            labs, hands, P, mass = r
            assert np.allclose(P.sum(1), 1) and (P >= -1e-12).all()
            grp = [ml.group_of(l, labs) for l in labs]
            P0 = np.array([n['hands'][h]['played'] for h in hands])
            if 'AGG' in grp and 'F' in grp and 'X' not in grp and prof['AGG'] > 1:
                cols = [j for j, g in enumerate(grp) if g == 'AGG']
                x0 = (mass * P0[:, cols].sum(1)).sum() / mass.sum(); x1 = (mass * P[:, cols].sum(1)).sum() / mass.sum()
                fold0 = (mass * P0[:, grp.index('F')]).sum() / mass.sum()
                assert x1 >= x0 - 1e-9
                assert abs(x1 - min(ml.odds(x0, prof['AGG']), x0 + fold0)) < 1e-4   # 0,01 % : renormalisation finale
            checked += 1
    assert checked > 100


def test_nit_drops_weakest_hands_first():
    for st, n in _nodes():
        r = ml.deform(n, st, ml.PROFILES['nit'])
        if r is None: continue
        labs, hands, P, mass = r
        if 'F' not in labs or 'X' in labs: continue
        P0 = np.array([n['hands'][h]['played'] for h in hands]); fi = labs.index('F')
        gained = P[:, fi] - P0[:, fi]
        if gained.max() < 0.5: continue
        vsr = np.array([ml.VSR[h] for h in hands]); dropped = vsr[gained > 0.5]; kept = vsr[(P[:, fi] < 0.01) & (mass > 0)]
        if len(kept): assert dropped.min() <= kept.min() + 1e-9
