"""Compare deux dossiers de résultats du solveur (même arbre, configurations communes) : effet d'un réglage (G17) sur la stratégie préflop.

Usage : python tools/solver/compare_runs.py data/solver/runs/<sans> data/solver/runs/<avec> [--hands K5o,K4o,Q8o]
Par configuration et par nœud : fréquences globales des actions (pondérées par combos et atteinte) sans / avec, et décalage moyen de
stratégie (points) ; puis, pour les mains suivies, la fréquence de la première action de chaque nœud (fold) sans / avec.
"""
import argparse, glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy.cards import NAMES, W  # noqa: E402

KEY_NODES = ('root', 'SB-raise2', 'SB-call', 'SB-call_BB-raise3', 'BTN-raise2', 'BTN-raise2_SB-call')


def freqs(node):
    w = np.array([node['hands'][h]['weight'] for h in NAMES]) * W
    f = np.array([node['hands'][h]['played'] for h in NAMES])
    return w, f


def kind(a):
    return {'fold': 'F', 'call': 'C', 'check': 'X', 'call_allin': 'C'}.get(a['type'], 'R' if a['type'] == 'R' else a['type'])


def summarize(node):
    w, f = freqs(node); tot = max(w.sum(), 1e-12); out = {}
    for j, a in enumerate(node['actions']):
        k = kind(a) if a['type'] != 'R' else ('A' if a.get('amount', 0) >= 0.99 * 0 and a is node['actions'][-1] and len(node['actions']) > 2 else 'R')
        out[k] = out.get(k, 0) + float((w * f[:, j]).sum() / tot)
    return out


def shift(n0, n1):
    w, f0 = freqs(n0); _, f1 = freqs(n1)
    return float(100 * (w * 0.5 * np.abs(f0 - f1).sum(1)).sum() / max(w.sum(), 1e-12))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('new'); ap.add_argument('--hands', default='K5o,K4o,Q8o,T9o,Q4o,22,66')
    a = ap.parse_args(); hands = a.hands.split(',')
    cfgs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(a.new, '*.json')) if os.path.isfile(os.path.join(a.base, os.path.basename(p))))
    print(f'{len(cfgs)} configurations communes')
    shifts = []
    for c in cfgs:
        r0 = json.load(open(os.path.join(a.base, c))); r1 = json.load(open(os.path.join(a.new, c)))
        common = [k for k in r0['nodes'] if k in r1['nodes']]
        sh = {k: shift(r0['nodes'][k], r1['nodes'][k]) for k in common}
        w = {k: float(freqs(r0['nodes'][k])[0].sum()) for k in common}
        glob_shift = sum(sh[k] * w[k] for k in common) / max(sum(w.values()), 1e-12)
        shifts.append((c, glob_shift, max(sh, key=lambda k: sh[k] * w[k]), r1['info']['exploitability_mbb'], r1['info'].get('drift_mbb')))
    print('\nConfiguration : décalage moyen de stratégie (points), nœud qui bouge le plus, exploitabilité avec correction')
    for c, g, k, e, d in shifts: print(f'  {c[:-5]:>14} : {g:5.2f} pts ; {k} ; exploitabilité {max(e):.2f} mBB, dérive {d} mBB')
    print('\nNœuds clés, configurations heads-up (fréquences globales sans -> avec, F fold, C call/limp, X check, R relance, A tapis)')
    for c in cfgs:
        if not c.startswith('hu_'): continue
        r0 = json.load(open(os.path.join(a.base, c))); r1 = json.load(open(os.path.join(a.new, c)))
        for k in KEY_NODES:
            if k in r0['nodes'] and k in r1['nodes']:
                s0, s1 = summarize(r0['nodes'][k]), summarize(r1['nodes'][k])
                print(f'  {c[:-5]:>10} {k:<20}: ' + ' ; '.join(f'{x} {100 * s0.get(x, 0):.0f} -> {100 * s1.get(x, 0):.0f}' for x in sorted(set(s0) | set(s1))))
    print('\nMains suivies : fréquence de fold, sans -> avec')
    for c in cfgs:
        if not c.startswith('hu_'): continue
        r0 = json.load(open(os.path.join(a.base, c))); r1 = json.load(open(os.path.join(a.new, c)))
        for k in ('SB-raise2', 'SB-call_BB-raise3', 'SB-call'):
            if k in r0['nodes'] and k in r1['nodes'] and r0['nodes'][k]['actions'][0]['type'] in ('F', 'fold'):
                print(f'  {c[:-5]:>10} {k:<18}: ' + ' ; '.join(f"{h} {100 * r0['nodes'][k]['hands'][h]['played'][0]:.0f} -> {100 * r1['nodes'][k]['hands'][h]['played'][0]:.0f}" for h in hands))
    print('\nBB après un limp du SB : fréquence d\'isolement (relance ou tapis), sans -> avec')
    for c in cfgs:
        if not c.startswith('hu_'): continue
        r0 = json.load(open(os.path.join(a.base, c))); r1 = json.load(open(os.path.join(a.new, c)))
        k = 'SB-call'
        if k in r0['nodes'] and k in r1['nodes']:
            iso = lambda r, h: 100 * (1 - r['nodes'][k]['hands'][h]['played'][0])
            print(f'  {c[:-5]:>10} {k:<18}: ' + ' ; '.join(f"{h} {iso(r0, h):.0f} -> {iso(r1, h):.0f}" for h in hands))


if __name__ == '__main__':
    main()
