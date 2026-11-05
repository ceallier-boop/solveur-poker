import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'hrc'))
import make_locks as ml
from conftest import needs_raw


def _nodes():
    for d in ml.exports():
        s = json.load(open(os.path.join(d, 'settings.json')))
        if ml.preflop_hash(s) != ml.REF_PREFLOP: continue
        st = [x / 10000 for x in s['handdata']['stacks']]
        for f in glob.glob(os.path.join(d, 'nodes', '*.json')):
            n = json.load(open(f))
            if len(n['actions']) >= 2: yield st, n


@needs_raw
def test_deformation_reaches_target_and_stays_normalised():
    checked = 0
    for st, n in _nodes():
        for profile in ml.PROFILES.values():
            f = ml.factors(profile, st)
            r = ml.deform(n, st, f)
            if r is None: continue
            labs, hands, P, mass = r
            assert np.allclose(P.sum(1), 1) and (P >= -1e-12).all()
            grp = [ml.group_of(l, labs) for l in labs]
            P0 = np.array([n['hands'][h]['played'] for h in hands])
            if ml.context(n) == 'first' and 'AGG' in grp and 'F' in grp and 'X' not in grp and f['shove'] > 1:
                cols = [j for j, g in enumerate(grp) if g == 'AGG']
                x0 = (mass * P0[:, cols].sum(1)).sum() / mass.sum(); x1 = (mass * P[:, cols].sum(1)).sum() / mass.sum()
                fold0 = (mass * P0[:, grp.index('F')]).sum() / mass.sum()
                assert x1 >= x0 - 1e-9
                assert abs(x1 - min(ml.odds(x0, f['shove']), x0 + fold0)) < 1e-4   # 0,01 % : renormalisation finale
            checked += 1
    assert checked > 100


def test_nit_drops_weakest_hands_first():
    for st, n in _nodes():
        r = ml.deform(n, st, ml.factors('Nit', st))
        if r is None: continue
        labs, hands, P, mass = r
        if 'F' not in labs or 'X' in labs: continue
        P0 = np.array([n['hands'][h]['played'] for h in hands]); fi = labs.index('F')
        gained = P[:, fi] - P0[:, fi]
        if gained.max() < 0.5: continue
        vsr = np.array([ml.VSR[h] for h in hands]); dropped = vsr[gained > 0.5]; kept = vsr[(P[:, fi] < 0.01) & (mass > 0)]
        if len(kept): assert dropped.min() <= kept.min() + 1e-9


def test_locked_profiles_are_the_engine_profiles():
    """mêmes profils et mêmes facteurs que le moteur exploitant ; le reg (facteurs à 1) n'a pas de calcul : c'est la solution GTO"""
    import profils_field as pf
    assert set(ml.PROFILES.values()) == {p for p in pf.PROFILES if p != 'Reg'}
    assert all(v == 1.0 for k, v in pf.factors('Reg', 12).items() if k in ('shove', 'call', 'iso', 'limp_k'))
    for st in ([12, 12, 12], [20, 20]):
        assert ml.factors(pf.DEFAULT, st) == pf.factors(pf.DEFAULT, 12)    # rec passif : facteurs de 12 BB au-delà, comme le moteur
    assert ml.plan('first', pf.factors('Dégène', 15))[0][1] == 2.0 and ml.plan('raise', pf.factors('Nit', 15))[0][1] == 0.5
    assert ml.plan('limp', pf.factors('Calling station', 15))[0][1] == 0.5


@needs_raw
def test_rec_keeps_weak_aces_when_jamming_less():
    """récréatif premier à parler : la baisse du tapis devient du limp et épargne ses As faibles (exploit_engine.rec_shape)"""
    import profils_field as pf
    seen = 0
    for st, n in _nodes():
        if ml.context(n) != 'first' or 'C' not in ml.labels(n, st): continue
        f = ml.factors(pf.DEFAULT, st)
        labs, hands, P, mass = ml.deform(n, st, f)
        P0 = np.array([n['hands'][h]['played'] for h in hands]); agg = [j for j, l in enumerate(labs) if ml.group_of(l, labs) == 'AGG']
        cut = P0[:, agg].sum(1) - P[:, agg].sum(1)
        if cut.max() < 0.5: continue
        ax = [i for i, h in enumerate(hands) if h in ml.REC_AX and P0[i, agg].sum() > 0.5]
        strong = [i for i, h in enumerate(hands) if ml.VSR[h] > 0.6 and h not in ml.REC_AX]
        for i in ax:                                                    # un As faible n'est retiré qu'avec les mains plus faibles que lui
            if cut[i] > 1e-3: assert all(P[j, agg].sum() < 1e-3 for j in range(len(hands)) if ml.VSR[hands[j]] < ml.VSR[hands[i]] and mass[j] > 0)
        assert any(cut[i] > 1e-9 for i in strong)                       # une partie des mains fortes est complétée, pas poussée
        seen += 1
    assert seen


def test_validator_structure_and_exact_ev_small_stacks():
    import validate as v
    for d in ml.exports():
        r = v.validate(d)
        assert not r['issues'], (d, r['issues'][:3])
        if len(r['stacks']) == 2 and r['stacks'][0] == r['stacks'][1] == 2:
            assert r['allin'] and r['allin'][0]['mean_abs_mbb'] < 15 and abs(r['allin'][0]['bias_mbb']) < 5   # 2 BB : HRC et calcul exact concordent
