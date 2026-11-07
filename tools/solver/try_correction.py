"""Essai d'une table de correction G17 sur quelques configurations : résout (grille v5, ehs2_texture, réglages de la grille p1),
puis compare à une banque de référence sur les mains suivies et rejoue les coachs.

Usage : python tools/solver/try_correction.py g17-v3a hu:25-25,hu:22-22 [--workers 4]
Les résultats vont dans data/solver/g17/essais/<table>/ (non publiés).
"""
import argparse, dataclasses, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc  # noqa: E402
from spinsacademy.postflop.hu_solver import PRESETS, PostflopConfig  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BASE = os.path.join(ROOT, 'data', 'solver', 'runs', 'sf3dc2e6_48fa0906')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('table'); ap.add_argument('configs'); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--no-compare', action='store_true'); a = ap.parse_args()
    out = os.path.join(ROOT, 'data', 'solver', 'g17', 'essais', a.table)
    p = ds.SolveParams(outer=10, postflop=dataclasses.asdict(PostflopConfig(**PRESETS['ehs2_texture'])), correction=None if a.table == 'none' else a.table)
    for st in ds.parse_configs(a.configs): ds.run(st, ds.TREES['v5'], p, workers=a.workers, runs=out)
    d = os.path.join(out, ds.run_id(ds.TREES['v5'], p))
    if not a.no_compare:
        subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'solver', 'compare_runs.py'), BASE, d, '--hands', 'K5o,K4o,Q8o,T9o,Q4o,Q5o,KJo,22'])
    print('dossier :', d)


if __name__ == '__main__':
    main()
