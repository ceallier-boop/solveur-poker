"""Contrôle des situations relevées par la relecture des coachs : décision du solveur dans deux banques (avant / après une
correction), à côté de la référence et de l'avis majoritaire des coachs.

Les situations viennent de l'échantillon G12 (`docs/relecture/solveur_2026-10-30/cle.csv`, réponses `reponses_*.csv`) : un
spot (même identifiant dans toutes les banques du même arbre et des mêmes tapis) et une main. Pour chaque banque : action
dominante du solveur, sa fréquence, et l'EV de chaque action.

Usage : python tools/solver/control_spots.py --before gto_preflop/2026.10.29-s1 --after gto_preflop/<nouvelle version>
        [--sample docs/relecture/solveur_2026-10-30] [--only desaccord]
"""
import argparse, collections, csv, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import quiz  # noqa: E402


def bank(ref):
    d = quiz.ref_path(ref)
    return {sp['spot_id']: sp for sp in map(json.loads, open(os.path.join(d, 'spots.jsonl')))}


def read(path):
    return list(csv.DictReader(open(path, encoding='utf-8-sig'), delimiter=';'))


def coaches(sample):
    """avis majoritaire des coachs par situation : 'solveur', 'référence', 'les deux' ou '—'"""
    key = {r['id']: r for r in read(os.path.join(sample, 'cle.csv'))}; votes = collections.defaultdict(list)
    for f in sorted(os.listdir(sample)):
        if not (f.startswith('reponses_') and f.endswith('.csv')): continue
        for r in read(os.path.join(sample, f)):
            v = (r.get('calcul_le_plus_juste') or '').strip()
            if r['id'] in key and v in ('A', 'B'): votes[r['id']].append(key[r['id']][v])
            elif r['id'] in key and v: votes[r['id']].append(v)
    out = {}
    for i, vs in votes.items():
        top, n = collections.Counter(vs).most_common(1)[0]
        out[i] = f'{top} ({n}/{len(vs)})' if n * 2 > len(vs) else '—'
    return out


def decision(sp, hand):
    if sp is None or hand not in sp['hands']: return None
    H = sp['hands'][hand]; ev = H['ev_exact'] if sp['ev_reference'] == 'exact' else H['ev_hrc']
    j = max(range(len(H['freq'])), key=lambda k: H['freq'][k])
    return dict(action=sp['actions'][j]['id'], freq=H['freq'][j], ev={a['id']: e for a, e in zip(sp['actions'], ev)})


def main(before, after, sample, only=None):
    A, B = bank(before), bank(after) if after else {}; votes = coaches(sample); rows = []
    for k in read(os.path.join(sample, 'cle.csv')):
        if only and k['type'] != only: continue
        a = decision(A.get(k['spot']), k['main']); b = decision(B.get(k['spot']), k['main']) if after else None
        rows.append((k, a, b, votes.get(k['id'], '—')))
    fmt = lambda d: '—' if d is None else f"{d['action']} {100 * d['freq']:.0f} %"
    print(f"{'id':5s} {'spot':58s} {'main':5s} {'référence':10s} {'coachs':16s} {'avant':12s} {'après':12s}")
    changed = 0
    for k, a, b, v in rows:
        print(f"{k['id']:5s} {k['spot']:58s} {k['main']:5s} {k['action_reference']:10s} {v:16s} {fmt(a):12s} {fmt(b):12s}")
        changed += bool(a and b and a['action'] != b['action'])
    if after: print(f'{changed} décisions changent sur {len(rows)}')
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--before', default='gto_preflop/2026.10.29-s1'); ap.add_argument('--after')
    ap.add_argument('--sample', default=os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'relecture', 'solveur_2026-10-30'))
    ap.add_argument('--only', choices=['desaccord', 'serree', 'accord'])
    a = ap.parse_args(); main(a.before, a.after, a.sample, a.only)
