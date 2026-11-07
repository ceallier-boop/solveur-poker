"""Apprentissage et contrôle de la correction G17 (spinsacademy.solver.correction).

Sous-jeux : les pots relancés heads-up les plus fréquents d'une banque de notre solveur (ranges d'arrivée au flop tirées
de la stratégie enregistrée), par défaut la relance payée (le SB ouvre, le BB paie) et l'iso payé (le SB limpe, le BB
isole, le SB paie). Sur chaque flop tiré au hasard : calcul exact (postflop.exact_flop), stratégie abstraite de production
rejouée, écart des gains par classe des deux joueurs. Une ligne par flop dans <dossier>/<config>_<sous-jeu>.jsonl : un
calcul interrompu reprend au flop suivant en relançant la même commande.

Deux jeux disjoints (tapis et flops différents) :
  learn : HU 25, 18, 12 ; la correction en est tirée ;
  check : HU 22, 15 (et 8 pour les tapis courts), flops d'une autre graine : contrôle hors échantillon.

Usage :
  python tools/solver/learn_correction.py --set learn --threads 4 --low-memory
  python tools/solver/learn_correction.py --set short --threads 4 --low-memory   # tapis courts 6 et 10 BB
  python tools/solver/learn_correction.py --set check --threads 4 --low-memory
  python tools/solver/learn_correction.py --report --name g17-v1      # table + contrôle
"""
import argparse, glob, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.cards import DISJOINT as D  # noqa: E402
from spinsacademy.postflop import fast  # noqa: E402
from spinsacademy.postflop.exact import average_sigma  # noqa: E402
from spinsacademy.postflop.exact_flop import ExactFlopHU, class_values, flop_buckets  # noqa: E402
from spinsacademy.postflop.hu_solver import PRESETS, HUPostflop, PostflopConfig  # noqa: E402
from spinsacademy.postflop.kernels import CLASS_OF  # noqa: E402
from spinsacademy.solver import correction as corr  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402
from spinsacademy.solver.cfr import Solver  # noqa: E402
from spinsacademy.solver.postflop import Realization  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BANK = os.path.join(ROOT, 'data', 'solver', 'runs', 'sf3dc2e6_48fa0906')      # banque v5 2026.11.02-s2, ehs2_texture
OUT = os.path.join(ROOT, 'data', 'solver', 'g17')
SETS = {'learn': dict(configs=('hu_25-25', 'hu_18-18', 'hu_12-12'), seed=101, flops=8),
        'short': dict(configs=('hu_10-10', 'hu_6-6'), seed=303, flops=8),     # tapis courts (G17, 05/11) ; 8 BB reste en contrôle
        'check': dict(configs=('hu_8-8', 'hu_15-15', 'hu_22-22'), seed=202, flops=6)}
SUBGAMES = {'raise': 'SB-raise', 'iso': 'SB-call_BB-raise'}     # préfixe de la clé du nœud terminal (ligne préflop)


def load_solver(path):
    """Solver dont la stratégie moyenne est celle enregistrée (nœuds absents : uniformes)"""
    res = json.load(open(path)); cfg = ds.TreeConfig(**res['tree_config'])
    s = Solver(tuple(res['stacks']), cfg)
    for nd in s.dec:
        x = res['nodes'].get(nd.key)
        if x is not None: s.S[nd.id] = np.array([x['hands'][h]['played'] for h in NAMES])
    return s, res


def subgames(path):
    """{nom : (pot, tapis, agresseur, w0, w1)} des pots relancés suivis, avec les ranges qui arrivent au flop"""
    s, res = load_solver(path); _, reach = s._pass(avg=True); out = {}
    for nd, o, i, pot, stack, ag in Realization.subgames(s):
        if ag not in (0, 1): continue
        for name, pre in SUBGAMES.items():
            if nd.key.startswith(pre) and nd.key.count('_') == pre.count('_') + 1 and nd.key.endswith('-call'):
                m = float(reach[nd.id][o] @ D @ reach[nd.id][i])
                if name not in out or m > out[name][-1]: out[name] = (pot, stack, ag, reach[nd.id][o].copy(), reach[nd.id][i].copy(), nd.key, m)
    return {k: v[:6] for k, v in out.items()}, res


def run_job(config, name, sg, flops, seed, iters, preset, low_memory, min_weight, out, log=print):
    pot, stack, ag, w0, w1, key = sg
    path = os.path.join(out, f'{config}_{name}.jsonl')
    done = sum(1 for _ in open(path)) if os.path.isfile(path) else 0
    if done >= flops: log(f'{config} {name} : {done} flops déjà faits'); return
    cfg = PostflopConfig(**PRESETS[preset]); base = PostflopConfig()
    t0 = time.time()
    pool = fast.board_pool(1000, cfg.buckets, cfg.rollouts, 1, cfg.metric, cfg.textured, cfg.flop_buckets)
    hp = HUPostflop(pot, stack, cfg, aggressor=ag).fast_solve(w0, w1, pool, iters=3000, seed=1); tab = average_sigma(hp)
    log(f'{config} {name} ({key}) : pot {pot:g}, tapis {stack:g}, SPR {stack / pot:.2f} ; stratégie abstraite {time.time() - t0:.0f} s')
    r0 = w0[CLASS_OF]; r1 = w1[CLASS_OF]
    r0 = np.where(r0 > min_weight, r0, 0.0); r1 = np.where(r1 > min_weight, r1, 0.0)
    rng = np.random.default_rng(seed + 31 * sum(map(ord, config + name)))
    allf = [sorted(rng.choice(52, 3, replace=False).tolist()) for _ in range(flops)]
    for f in range(done, flops):
        flop = allf[f]; t1 = time.time()
        ex = ExactFlopHU(pot, stack, flop, base, aggressor=ag, low_memory=low_memory).solve(r0, r1, iters=iters)
        Ve = ex.values(r0, r1, mode=1); e_ex = ex.exploitability(r0, r1)
        ex.set_abstract(tab, flop_buckets(ex, cfg, 1))
        Va = ex.values(r0, r1, mode=2); e_ab = ex.exploitability(r0, r1, mode=2)
        ce = class_values(ex, Ve, r0, r1); ca = class_values(ex, Va, r0, r1)
        row = dict(config=config, subgame=name, key=key, pot=pot, stack=stack, aggressor=ag, flop=flop, iters=iters,
                   exploitability_exact=round(e_ex, 5), exploitability_abstract=round(e_ab, 5), seconds=round(time.time() - t1),
                   players=[dict(num_exact=[round(float(x), 5) for x in ce[p][0]], num_abstract=[round(float(x), 5) for x in ca[p][0]],
                                 den=[round(float(x), 5) for x in ce[p][1]]) for p in (0, 1)])
        with open(path, 'a') as fh: fh.write(json.dumps(row) + '\n')
        log(f'  flop {f + 1}/{flops} : {row["seconds"]} s, exploitabilité exacte {100 * e_ex:.2f} %, abstraite {100 * e_ab:.2f} % du pot')
        del ex


def rows(out, configs):
    res = []
    for c in configs:
        for f in sorted(glob.glob(os.path.join(out, f'{c}_*.jsonl'))):
            res += [json.loads(x) for x in open(f) if x.strip()]
    return res


def samples(rs):
    """un échantillon par (config, sous-jeu, joueur) pour correction.fit"""
    acc = {}
    for r in rs:
        for p in (0, 1):
            k = (r['config'], r['subgame'], p)
            a = acc.setdefault(k, dict(role=corr.role(p, r['aggressor']), spr=r['stack'] / r['pot'], pot=r['pot'], d_num=0, den=0, flops=0))
            pl = r['players'][p]
            a['d_num'] = a['d_num'] + np.array(pl['num_exact']) - np.array(pl['num_abstract']); a['den'] = a['den'] + np.array(pl['den']); a['flops'] += 1
    return acc


def evaluate(rs, table):
    """écart restant exact - (abstrait + correction), en mBB, par (config, sous-jeu, joueur) et famille de mains, pondéré
    par la masse de la classe dans la range du joueur ; et la même chose sans correction"""
    out = {}
    for k, a in samples(rs).items():
        cfg, sg, p = k; any_r = next(r for r in rs if r['config'] == cfg and r['subgame'] == sg)
        pot, stack, ag = any_r['pot'], any_r['stack'], any_r['aggressor']
        den = a['den']; ok = den > 0
        d = np.where(ok, a['d_num'] / np.where(ok, den, 1), 0)                  # BB : exact - abstrait
        eff = min(float(x) for x in cfg.split('_')[1].split('-'))           # tapis de départ effectif du duel
        c = pot * table(corr.role(p, ag), stack / pot) if table and eff >= table.min_stack else np.zeros(169)
        w = den * W                                                              # masse observée (range x compatibilité)
        fams = {}
        for f in sorted(set(corr.FAMILY)):
            ix = [i for i in range(169) if corr.FAMILY[i] == f and ok[i]]
            if ix and w[ix].sum() > 0.01 * w[ok].sum():
                fams[f] = (round(1000 * float(np.average(d[ix], weights=w[ix])), 0), round(1000 * float(np.average(d[ix] - c[ix], weights=w[ix])), 0))
        rms = lambda x: float(np.sqrt(np.average(x[ok] ** 2, weights=w[ok])))
        ex_ab = np.mean([r['exploitability_abstract'] for r in rs if r['config'] == cfg and r['subgame'] == sg])
        ex_ex = np.mean([r['exploitability_exact'] for r in rs if r['config'] == cfg and r['subgame'] == sg])
        out[f'{cfg} {sg} {corr.role(p, ag)}'] = dict(spr=round(stack / pot, 2), flops=a['flops'], rms_before_mbb=round(1000 * rms(d)),
                                                    rms_after_mbb=round(1000 * rms(d - c)), families=fams,
                                                    exploitability_abstract_pct=round(100 * ex_ab, 2), exploitability_exact_pct=round(100 * ex_ex, 2))
    return out


def report(out, name, shrink, min_stack=0.0, learn_sets=('learn',), scale=1.0, zero=()):
    learn = rows(out, [c for k in learn_sets for c in SETS[k]['configs']]); check = rows(out, SETS['check']['configs'])
    if not learn: raise SystemExit('aucun flop du jeu learn')
    roles = corr.fit(list(samples(learn).values()), shrink=shrink)
    for ks in roles.values():                                   # amplitude réduite ; familles non fiables mises à zéro (G17, v3)
        for k in ks:
            k['delta'] = [0.0 if corr.FAMILY[i] in zero else round(scale * x, 5) for i, x in enumerate(k['delta'])]
    data = dict(name=name, method='exact - abstrait par classe, fraction du pot ; 0 à SPR nul, interpolation linéaire',
                preset='ehs2_texture', bank=os.path.basename(BANK), learn=sorted({f"{r['config']} {r['subgame']}" for r in learn}),
                flops=len(learn), shrink=shrink, min_stack=min_stack, scale=scale, zero=list(zero), roles=roles)
    os.makedirs(corr.DIR, exist_ok=True)
    json.dump(data, open(os.path.join(corr.DIR, name + '.json'), 'w'), ensure_ascii=False, indent=0)
    table = corr.Table(data)
    res = dict(table=name, learn=evaluate(learn, table), check=evaluate(check, table) if check else {})
    json.dump(res, open(os.path.join(out, f'report_{name}.json'), 'w'), ensure_ascii=False, indent=1)
    for part in ('learn', 'check'):
        print(f'\n== {part} (écart exact - abstrait, mBB : sans correction -> avec)')
        for k, v in res[part].items():
            print(f"{k} (SPR {v['spr']}, {v['flops']} flops) : écart quadratique {v['rms_before_mbb']} -> {v['rms_after_mbb']} ; "
                  f"exploitabilité abstraite {v['exploitability_abstract_pct']} %")
            print('   ' + ' ; '.join(f'{f} {a:+.0f} -> {b:+.0f}' for f, (a, b) in v['families'].items()))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', choices=list(SETS), default='learn'); ap.add_argument('--configs', help='sous-ensemble des configurations du jeu, séparées par des virgules')
    ap.add_argument('--subgames', default='raise,iso'); ap.add_argument('--flops', type=int, help='flops par sous-jeu (par défaut : 8 pour learn, 6 pour check)'); ap.add_argument('--iters', type=int, default=100)
    ap.add_argument('--preset', default='ehs2_texture'); ap.add_argument('--threads', type=int, default=0)
    ap.add_argument('--low-memory', action='store_true'); ap.add_argument('--min-weight', type=float, default=1e-3)
    ap.add_argument('--bank', default=BANK); ap.add_argument('--out', default=OUT)
    ap.add_argument('--learn-sets', default='learn', help='jeux d\'apprentissage du rapport, séparés par des virgules (learn, short)')
    ap.add_argument('--scale', type=float, default=1.0, help='amplitude de la correction (0 à 1)'); ap.add_argument('--zero', default='', help='familles de mains à ne pas corriger, séparées par des virgules')
    ap.add_argument('--report', action='store_true'); ap.add_argument('--name', default='g17-v1'); ap.add_argument('--shrink', type=float, default=8.0)
    ap.add_argument('--min-stack', type=float, default=12.0, help='tapis effectif minimal (BB) où la correction s\'applique')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.report: report(a.out, a.name, a.shrink, a.min_stack, a.learn_sets.split(','), a.scale, [x for x in a.zero.split(',') if x]); return
    if a.threads:
        import numba; numba.set_num_threads(a.threads)
    st = SETS[a.set]; configs = a.configs.split(',') if a.configs else st['configs']
    for c in configs:
        sgs, _ = subgames(os.path.join(a.bank, c + '.json'))
        for name in a.subgames.split(','):
            if name not in sgs: print(f'{c} : pas de sous-jeu {name}'); continue
            run_job(c, name, sgs[name], a.flops or st['flops'], st['seed'], a.iters, a.preset, a.low_memory, a.min_weight, a.out, log=lambda m: print(m, flush=True))
    print('FIN', flush=True)


if __name__ == '__main__':
    main()
