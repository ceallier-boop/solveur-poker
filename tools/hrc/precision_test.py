"""Test de précision des exports HRC : écart avec l'EV exacte et dispersion entre exports répétés d'une même main.

Usage : python tools/hrc/precision_test.py <dossier contenant hand_*/> [--groups 1-4,5-8]
Pour chaque export : écart |EV HRC − EV exacte| sur les nœuds à EV exacte (mains atteintes à 5 % au moins, pire action).
Pour chaque groupe d'exports identiques (mêmes réglages et tapis) : dispersion des EV et des fréquences entre répétitions,
et écart avec l'EV exacte de la moyenne de 1, 2, 4… répétitions (un bruit aléatoire baisse comme 1/√n, un biais non).
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy import hrc, importer  # noqa: E402
from spinsacademy.cards import NAMES  # noqa: E402


def spots(d):
    s, st, nodes = hrc.load(d); out = {}
    for k in nodes:
        try:
            sp = importer.build_spot(d, st, nodes, k, s, 'test')
            if sp: out[k] = sp
        except importer.InvalidSpot:
            pass
    return out


def exact_error(runs):
    """écarts (mBB) entre la moyenne des EV HRC de `runs` et la moyenne de leurs EV exactes"""
    errs = []
    for k, s0 in runs[0].items():
        if s0['ev_reference'] != 'exact' or any(k not in r for r in runs): continue
        for h in NAMES:
            xs = [r[k]['hands'][h] for r in runs]
            if min(x['reach'] for x in xs) < 0.05: continue
            n = len(xs[0]['ev_exact'])
            ex = np.array([np.mean([x['ev_exact'][j] for x in xs]) if xs[0]['ev_exact'][j] is not None else np.nan for j in range(n)])
            d = np.abs(ex - np.mean([x['ev_hrc'] for x in xs], 0)) * 1000; d = d[~np.isnan(d)]
            if len(d): errs.append(d.max())
    return np.array(errs)


def main(folder, groups):
    dirs = sorted((d for d in os.listdir(folder) if d.startswith('hand_')), key=lambda s: int(s.split('_')[1]))
    S = {d: spots(os.path.join(folder, d)) for d in dirs}
    for d in dirs:
        e = exact_error([S[d]]); print(f'{d} : {len(e)} mains, écart avec l\'EV exacte médiane {np.median(e):.0f} mBB, 90e centile {np.percentile(e, 90):.0f}')
    for g in groups:
        runs = [S[f'hand_{i}'] for i in g]
        for m in sorted({1, 2, 4, len(runs)} & set(range(1, len(runs) + 1))):
            e = exact_error(runs[:m]); print(f'groupe {g[0]}-{g[-1]}, moyenne de {m} : médiane {np.median(e):.0f} mBB, 90e centile {np.percentile(e, 90):.0f}')
        keys = set.intersection(*[set(r) for r in runs]); dev, fdev = [], []
        for k in keys:
            for h in NAMES:
                xs = [r[k]['hands'][h] for r in runs]
                if min(x['reach'] for x in xs) < 0.05: continue
                dev.append(1000 * np.std([x['ev_hrc'] for x in xs], 0).max()); fdev.append(100 * np.std([x['freq'] for x in xs], 0).max())
        print(f'groupe {g[0]}-{g[-1]} : dispersion entre répétitions, EV médiane {np.median(dev):.0f} mBB (90e centile {np.percentile(dev, 90):.0f}), '
              f'fréquences médiane {np.median(fdev):.1f} points (90e centile {np.percentile(fdev, 90):.0f})')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('--groups', default='1-4,5-8')
    a = ap.parse_args()
    main(a.folder, [list(range(int(x.split('-')[0]), int(x.split('-')[1]) + 1)) for x in a.groups.split(',')])
