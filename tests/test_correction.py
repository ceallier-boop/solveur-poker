"""Correction G17 des pots relancés (spinsacademy.solver.correction)."""
import dataclasses
import numpy as np
from spinsacademy.solver import correction as corr
from spinsacademy.solver import dataset as ds


def table():
    d0 = np.full(169, 0.02); d1 = np.full(169, -0.01)
    return corr.Table(dict(name='t', roles={'oop_caller': [dict(spr=2.0, delta=list(d0)), dict(spr=4.0, delta=list(2 * d0))],
                                            'ip_aggressor': [dict(spr=4.0, delta=list(d1))]}))


def test_interpolation():
    t = table()
    assert np.allclose(t('oop_caller', 0.0), 0) and np.allclose(t('oop_caller', 1.0), 0.01)
    assert np.allclose(t('oop_caller', 3.0), 0.03) and np.allclose(t('oop_caller', 9.0), 0.04)
    assert np.allclose(t('ip_caller', 3.0), 0)


def test_apply_raised_pot_only():
    t = table(); G0 = np.ones(169); G1 = np.ones(169)
    a0, a1 = t.apply(4.0, 16.0, 1, G0, G1)                      # SPR 4, agresseur IP : OOP appelant
    assert np.allclose(a0, 1 + 4 * 0.04) and np.allclose(a1, 1 - 4 * 0.01)
    b0, b1 = t.apply(4.0, 16.0, -1, G0, G1)                     # pot limpé : inchangé
    assert b0 is G0 and b1 is G1


def test_fit_shrinks_to_family():
    den = np.ones(169); num = np.zeros(169); num[0] = 1.0       # une seule classe (22) écartée
    out = corr.fit([dict(role='oop_caller', spr=3.0, pot=2.0, d_num=num, den=den, flops=4)], shrink=4.0)
    d = np.array(out['oop_caller'][0]['delta'])
    fam = [i for i in range(169) if corr.FAMILY[i] == corr.FAMILY[0]]
    assert 0 < d[0] < 0.5 and all(d[i] > 0 for i in fam) and abs(d[168]) < 1e-9


def test_run_id_unchanged_without_correction():
    p = ds.SolveParams(outer=10, postflop=dataclasses.asdict(ds.PostflopConfig(**ds.PRESETS['ehs2_texture'])))
    assert ds.run_id(ds.TREES['v5'], p) == 'sf3dc2e6_48fa0906'     # banque 2026.11.02-s2
    assert ds.run_id(ds.TREES['v5'], dataclasses.replace(p, correction='g17-v1')) != 'sf3dc2e6_48fa0906'
