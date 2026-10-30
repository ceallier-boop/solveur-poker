"""Arbitre des désaccords avec la référence : sous-jeux postflop résolus exactement à partir du flop (action G9, 30/10/2026).

Situation repère : un pot heads-up de la référence (ranges d'entrée au flop tirées de l'export, répétitions moyennées).
Sur F flops tirés au hasard :
  1. le sous-jeu est résolu exactement, combo par combo (spinsacademy.postflop.exact_flop) ;
  2. la stratégie du solveur de production (groupes de force partagés entre tous les flops, entraînée sur 1 000 boards
     avec les mêmes ranges) est rejouée sur ce flop ;
  3. gains G par classe (comme fast_evaluate : somme des valeurs / somme des masses compatibles, cumulées sur les flops).
On compare trois G de l'appelant : exact, production, et celui qu'implique la référence (EV du call + mise engagée − blind
perdue au fold). Exact − production = erreur de notre abstraction ; exact − référence = erreur de la référence (au bruit
de l'échantillon de flops près, que donne l'écart type entre flops).

Usage : python tools/solver/exact_flop_check.py --spot iso --flops 8 --iters 150
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc  # noqa: E402
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.postflop import fast  # noqa: E402
from spinsacademy.postflop.exact import average_sigma  # noqa: E402
from spinsacademy.postflop.exact_flop import ExactFlopHU, class_values, flop_buckets  # noqa: E402
from spinsacademy.postflop.hu_solver import HUPostflop, PostflopConfig  # noqa: E402
from spinsacademy.postflop.kernels import CLASS_OF  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402

R_ = '23456789TJQKA'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'solver')


def family(h):
    if len(h) == 2: return 'paires'
    s = h[2] == 's'; a, b = R_.index(h[0]), R_.index(h[1])
    if h[0] == 'A': return 'As assortis' if s else 'As dépareillés'
    if a >= 8 and b >= 8: return 'broadways assortis' if s else 'broadways dépareillés'
    if s and a - b <= 2: return 'connecteurs assortis'
    return 'autres assorties' if s else 'autres dépareillées'


def spots(stacks):
    """situations repères heads-up : (pot, tapis, poids OOP = BB, poids IP = SB, appelant, EV du call de l'appelant,
    mise de l'appelant après le call, agresseur du duel : 0 OOP, 1 IP, -1 aucun)"""
    st = [float(x) for x in stacks]; ref = ds.reference_nodes('daa9aaa0', st)
    if ref is None: raise SystemExit(f'pas de référence pour {stacks}')
    nd = ref['nodes']; lab = lambda n, a: hrc.labels(n, st).index(a)
    vec = lambda n, f, j=None: np.array([n['hands'][h][f] if j is None else n['hands'][h][f][j] for h in NAMES])
    root, lim = nd['root'], nd['SB-call']; out = {}
    S = st[0]
    out['limp'] = (2.0, S - 1, vec(lim, 'weight') * vec(lim, 'played', lab(lim, 'X')), vec(root, 'weight') * vec(root, 'played', lab(root, 'C')),
                   0, vec(lim, 'evs', lab(lim, 'X')), 1.0, -1)
    iso = next((k for k in nd if k.startswith('SB-call_BB-raise') and k.count('_') == 1), None)
    if iso:
        r = hrc.labels(lim, st)[[a.startswith('R') for a in hrc.labels(lim, st)].index(True)]; x = float(r[1:]); n = nd[iso]
        out['iso'] = (2 * x, S - x, vec(lim, 'weight') * vec(lim, 'played', lab(lim, r)), vec(n, 'weight') * vec(n, 'played', lab(n, 'C')),
                      1, vec(n, 'evs', lab(n, 'C')), x, 0)
    rs = next((a for a in hrc.labels(root, st) if a.startswith('R')), None)
    if rs:
        x = float(rs[1:]); n = nd[f'SB-raise{x:g}']
        out['raise'] = (2 * x, S - x, vec(n, 'weight') * vec(n, 'played', lab(n, 'C')), vec(root, 'weight') * vec(root, 'played', lab(root, rs)),
                        0, vec(n, 'evs', lab(n, 'C')), x, 1)
    return out, ref['exports']


def main(stacks, spot, flops, iters, seed, boards, min_weight=1e-3, log=print):
    sp, exports = spots(stacks)
    pot, stack, w0, w1, caller, ev_call, commit, ag = sp[spot]
    cfg = PostflopConfig(); r0, r1 = w0[CLASS_OF], w1[CLASS_OF]
    r0 = np.where(r0 > min_weight, r0, 0.0); r1 = np.where(r1 > min_weight, r1, 0.0)   # poids infimes : 0,1 à 0,3 % de la masse, 15 % du calcul
    t0 = time.time()
    pool = fast.board_pool(boards, cfg.buckets, cfg.rollouts, seed, cfg.metric, cfg.textured)
    hp = HUPostflop(pot, stack, cfg, aggressor=ag).fast_solve(w0, w1, pool, iters=3000, seed=seed); tab = average_sigma(hp)
    G_prod_pool = hp.fast_evaluate(w0, w1, pool)[caller]
    log(f'production : {time.time() - t0:.0f} s')
    rng = np.random.default_rng(seed); acc = {k: [np.zeros(169), np.zeros(169)] for k in ('exact', 'prod')}; per_flop = []
    for f in range(flops):
        flop = sorted(rng.choice(52, 3, replace=False).tolist()); t1 = time.time()
        ex = ExactFlopHU(pot, stack, flop, cfg, aggressor=ag).solve(r0, r1, iters=iters)
        expl = ex.exploitability(r0, r1)
        Ve = ex.values(r0, r1, mode=1)
        ex.set_abstract(tab, flop_buckets(ex, cfg.buckets, cfg.rollouts, seed)); Va = ex.values(r0, r1, mode=2)
        expl_abs = ex.exploitability(r0, r1, mode=2)
        row = dict(flop=[R_[c // 4] + 'cdhs'[c % 4] for c in flop], exploitability_pct=round(100 * expl, 3), abstract_exploitability_pct=round(100 * expl_abs, 2))
        for k, V in (('exact', Ve), ('prod', Va)):
            num, den = class_values(ex, V, r0, r1)[caller]; acc[k][0] += num; acc[k][1] += den
            w = (w0 if caller == 0 else w1) * W; g = np.where(den > 0, num / np.where(den > 0, den, 1), 0)
            row[f'G_{k}'] = round(float((w * g * (den > 0)).sum() / max((w * (den > 0)).sum(), 1e-12)), 4)
        per_flop.append(row)
        log(f"flop {f + 1}/{flops} {' '.join(row['flop'])} : {time.time() - t1:.0f} s, exploitabilité exacte {row['exploitability_pct']} % du pot, "
            f"abstraite {row['abstract_exploitability_pct']} % ; G appelant exact {row['G_exact']:+.3f}, production {row['G_prod']:+.3f}")
        del ex
    G = {k: np.where(acc[k][1] > 0, acc[k][0] / np.where(acc[k][1] > 0, acc[k][1], 1), np.nan) for k in acc}
    G['ref'] = ev_call + commit - 1.0; G['prod_pool'] = G_prod_pool
    w = (w0 if caller == 0 else w1) * W; ok = np.isfinite(G['exact']) & (w > 0)
    fams = {}
    for i, h in enumerate(NAMES):
        if ok[i]: fams.setdefault(family(h), []).append(i)
    def cmp(a, b):
        d = 1000 * (G[a] - G[b]); return dict(mean=round(float(np.average(d[ok], weights=w[ok])), 1),
                                             families={f: round(float(np.average(d[ix], weights=w[ix])), 1) for f, ix in sorted(fams.items())})
    hands = {h: {k: round(float(G[k][NAMES.index(h)]), 3) for k in ('exact', 'prod', 'ref')} for h in ('J8o', 'K9o', '76s', 'A5s', '22', '44', '66', '88', 'TT', 'QQ') if ok[NAMES.index(h)]}
    sd = np.std([r['G_exact'] for r in per_flop], ddof=1) if len(per_flop) > 1 else None
    res = dict(stacks=stacks, spot=spot, min_weight=min_weight, pot=pot, stack=stack, caller='OOP (BB)' if caller == 0 else 'IP (SB)', reference=exports, flops=flops, iters=iters,
               exact_minus_prod_mbb=cmp('exact', 'prod'), exact_minus_ref_mbb=cmp('exact', 'ref'), prod_minus_ref_mbb=cmp('prod', 'ref'),
               flop_sample_sd_mbb=round(1000 * sd / np.sqrt(len(per_flop)), 1) if sd is not None else None, hands=hands, per_flop=per_flop,
               seconds=round(time.time() - t0))
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--stacks', default='25,25'); ap.add_argument('--spot', default='iso', choices=['limp', 'iso', 'raise'])
    ap.add_argument('--flops', type=int, default=8); ap.add_argument('--iters', type=int, default=150); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--boards', type=int, default=1000)
    a = ap.parse_args(); st = [float(x) for x in a.stacks.split(',')]
    res = main(st, a.spot, a.flops, a.iters, a.seed, a.boards)
    path = os.path.join(OUT, f"exact_flop_hu{int(st[0])}_{a.spot}.json"); json.dump(res, open(path, 'w'), ensure_ascii=False, indent=1)
    for k in ('exact_minus_prod_mbb', 'exact_minus_ref_mbb', 'prod_minus_ref_mbb'):
        print(k, res[k]['mean'], res[k]['families'])
    print('mains', res['hands']); print('écart type de l\'échantillon de flops (G moyen exact, mBB)', res['flop_sample_sd_mbb'])
