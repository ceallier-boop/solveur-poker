"""Banque GTO produite par le solveur maison : résolution, contrôles, calage sur la référence, spots au format des banques.

But : les questions servies viennent de notre solveur ; la référence ne sert plus qu'à le caler et à le contrôler
(décision du 29/10/2026, docs/solver/INVENTAIRE_MOTEUR_GTO_2026-10-29.md).

Étapes, pour chaque configuration de tapis :
  1. résolution (pipeline.solve : préflop CFR+ et sous-jeux postflop heads-up alternés ; ou préflop seul, modèle showdown) ;
  2. résultat enregistré dans data/solver/runs/<run>/<config>.json (nœuds au format des exports, informations de calcul) :
     c'est la source de la banque, comme data/hrc/raw pour la référence. Une configuration déjà résolue avec les mêmes
     réglages n'est pas recalculée (une série longue peut reprendre) ;
  3. contrôles propres au solveur : exploitabilité de la stratégie (meilleure réponse de chaque joueur, mBB par main),
     stabilité entre les deux derniers tours préflop / postflop (dérive : exploitabilité de la stratégie de l'avant-dernier
     tour dans le modèle du dernier ; les fréquences des mains mixtes, presque indifférentes, peuvent bouger sans effet) ;
  4. calage, quand la référence a un export du même arbre et des mêmes tapis : perte de la stratégie maison mesurée avec
     les EV de la référence, à comparer au plancher de bruit de la référence (calibration.py). Information, non bloquant ;
  5. spots construits par le même cœur que l'importeur (importer.make_spot) : mêmes champs, mêmes règles (EV exacte
     quand chaque action autre que fold en a une, sinon EV du solveur, champ `ev_reference` = 'hrc' tant que les
     identifiants techniques ne sont pas renommés : l'application l'affiche déjà « solveur »), mêmes mains proposables.
La publication est bloquée si un spot est invalide ou si une configuration dépasse les seuils de contrôle.

Usage :
  python -m spinsacademy.solver.dataset --version 2026.10.30-s1 --configs hu:12-12,3w:12-12-12
  python -m spinsacademy.solver.dataset --version 2026.10.30-s1 --grid p1 --tree v5   # les 58 configurations P1, ouvertures à 2 BB
  python -m spinsacademy.solver.dataset --check gto_preflop/2026.10.30-s1          # recalcule et compare (test de référence)
"""
import argparse, dataclasses, datetime, hashlib, json, os, time
import numpy as np
from .. import allin, hrc, importer
from ..cards import NAMES
from ..grading import MIXED_MIN
from ..postflop.hu_solver import PRESETS, PostflopConfig
from . import calibration
from .cfr import Solver
from .postflop import Showdown
from .tree import POS, TreeConfig

SOLVER_VERSION = '1.0.0'
RUNS = os.path.join(hrc.ROOT, 'data', 'solver', 'runs')
REFERENCE_TREES = {'daa9aaa0': TreeConfig()}      # arbre de la référence : notre arbre par défaut en reproduit exactement les actions
# Arbres nommés pour la ligne de commande. v5 : commande de calage du 30/10/2026 (EXPORTS_A_PRODUIRE.md §11), ouvertures à
# 2 BB (BTN et SB, à 3 joueurs comme en heads-up), tapis direct toujours proposé ; c'est l'arbre des banques à venir.
TREES = {'reference': TreeConfig(), 'v5': TreeConfig(open_btn=2.0, open_sb=2.0, unopened_allin_max=0)}
MAX_EXPLOITABILITY_MBB = 5.0      # meilleure réponse d'un joueur contre la stratégie : au-delà, la résolution n'a pas convergé
MAX_DRIFT_MBB = 1.0               # exploitabilité de la stratégie de l'avant-dernier tour dans le modèle du dernier (pipeline.solve)

# Commande v4, lot P1 (docs/reference/EXPORTS_A_PRODUIRE.md §10.2) : tapis BTN / SB / BB, ou SB / BB en heads-up.
# 58 configurations distinctes : la commande en annonce 59 car 25 / 25 / 25 figure aussi dans la liste du §6.1
GRID_P1 = ([('3w', (x, x, x)) for x in (4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25)]
           + [('hu', (x, x)) for x in (2, 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25)]
           + [('hu', s) for s in ((4, 8), (8, 4), (10, 20), (20, 10), (12, 18), (18, 12), (15, 25), (25, 15), (20, 30), (30, 20), (35, 15), (15, 35))]
           + [('3w', s) for s in ((35, 25, 15), (25, 35, 15), (15, 25, 35), (35, 15, 25), (40, 20, 15), (20, 40, 15), (15, 20, 40), (30, 30, 15),
                                  (45, 20, 10), (20, 45, 10), (10, 20, 45), (30, 25, 20), (50, 15, 10), (15, 50, 10), (20, 30, 25),
                                  (6, 10, 14), (6, 14, 10), (10, 6, 14), (10, 14, 6), (14, 6, 10), (14, 10, 6))])


@dataclasses.dataclass
class SolveParams:
    model: str = 'realization'        # 'realization' (préflop + postflop) ou 'showdown' (préflop seul, pas de jeu après le flop)
    pre_iters: int = 1500
    outer: int = 12                   # tours préflop / postflop au plus ; arrêt dès que la dérive passe sous tol_mbb
    tol_mbb: float = 0.6              # la dérive comprend l'exploitabilité propre du préflop (≈ 0,5 mBB à 1 500 itérations)
    post_iters: int = 3000
    boards: int = 1000
    damping: object = 'linear'        # corrections postflop moyennées sur tous les tours (postflop.Realization.commit)
    seed: int = 1
    postflop: dict = dataclasses.field(default_factory=lambda: dataclasses.asdict(PostflopConfig()))


def _md5(obj):
    return hashlib.md5(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:8]


def tree_id(cfg):
    """empreinte de notre arbre préflop (réglages TreeConfig) ; celle de la référence quand il en reproduit les actions"""
    d = dataclasses.asdict(cfg)
    for ref, rc in REFERENCE_TREES.items():
        if dataclasses.asdict(rc) == d: return ref
    return 's' + _md5(d)[:7]


def run_id(cfg, params):
    return f'{tree_id(cfg)}_{_md5([dataclasses.asdict(cfg), dataclasses.asdict(params), SOLVER_VERSION])}'


def config_name(stacks):
    return f"{'3w' if len(stacks) == 3 else 'hu'}_{'-'.join(f'{x:g}' for x in stacks)}"


def parse_configs(text):
    """« hu:12-12,3w:12-12-12 » -> [(12.0, 12.0), (12.0, 12.0, 12.0)]"""
    out = []
    for tok in text.split(','):
        table, _, st = tok.strip().partition(':'); st = tuple(float(x) for x in st.split('-'))
        if (table, len(st)) not in (('hu', 2), ('3w', 3)): raise ValueError(f'configuration illisible : {tok}')
        out.append(st)
    return out


# ------------------------------------------------------------------ résolution
def solve(stacks, cfg, params, workers=4, log=print):
    """(Solver, informations de calcul)"""
    t0 = time.time(); history = []
    if params.model == 'showdown':
        s = Solver(stacks, cfg, postflop=Showdown()).solve(params.pre_iters)
    elif params.model == 'realization':
        from .pipeline import solve as full
        s, _, history = full(stacks, cfg, outer=params.outer, pre_iters=params.pre_iters, post_iters=params.post_iters,
                             pf_cfg=PostflopConfig(**params.postflop), boards=params.boards, workers=workers, seed=params.seed,
                             damping=params.damping, log=log, tol_mbb=params.tol_mbb)
    else:
        raise ValueError(f'modèle inconnu : {params.model}')
    expl = [round(1000 * x, 3) for x in s.exploitability()]
    return s, dict(seconds=round(time.time() - t0, 1), exploitability_mbb=expl, iterations=s.t,
                   shift_pts=round(history[-1]['shift_pts'], 3) if history else None,
                   drift_mbb=round(history[-1]['drift_mbb'], 3) if history else None, rounds=history)


def to_nodes(solver):
    """stratégie du solveur au format des exports (séquence et actions en jetons : 1 BB = 10 000 ; par main : weight,
    played, evs relatives au fold) : importer.make_spot et calibration.compare les lisent tels quels. Les nœuds qu'aucun
    adversaire n'atteint (EV indéfinies) sont omis."""
    tree = solver.tree; strat = solver.strategy(); chips = lambda x: int(round(10000 * x))
    seqs = {tree.root.id: []}
    for nd in tree.nodes:                                  # préordre : un parent précède ses enfants
        if nd.kind != 'decision': continue
        p = nd.player
        for lab, ch in zip(nd.actions, nd.children):
            if lab == 'C': a = dict(player=p, type='C', amount=chips(ch.contrib[p] - nd.contrib[p]))
            elif lab[0] in 'RA': a = dict(player=p, type='R', amount=chips(ch.contrib[p]))
            else: a = dict(player=p, type=lab, amount=0)
            seqs[ch.id] = seqs[nd.id] + [a]
    out = {}
    for nd in tree.decisions():
        x = strat[nd.key]
        if not np.isfinite(x['ev']).all(): continue
        acts = []
        for lab, ch in zip(nd.actions, nd.children):
            a = seqs[ch.id][-1]; acts.append(dict(type=a['type'], amount=a['amount']))
        hands = {h: dict(weight=round(float(x['reach'][i]), 6), played=[round(float(v), 6) for v in x['freq'][i]],
                         evs=[round(float(v), 6) for v in x['ev'][i]]) for i, h in enumerate(NAMES)}
        out[nd.key] = dict(player=nd.player, sequence=seqs[nd.id], actions=acts, hands=hands)
    return out


def run(stacks, cfg, params, workers=4, runs=RUNS, log=print):
    """résultat enregistré d'une configuration : le calcule s'il n'existe pas encore avec ces réglages"""
    path = os.path.join(runs, run_id(cfg, params), config_name(stacks) + '.json')
    if os.path.isfile(path): return json.load(open(path)), path
    if log: log(f'{config_name(stacks)} : résolution ({params.model})')
    s, info = solve(stacks, cfg, params, workers, log)
    res = dict(solver=SOLVER_VERSION, stacks=list(stacks), tree=tree_id(cfg), tree_config=dataclasses.asdict(cfg),
               params=dataclasses.asdict(params), info=info, nodes=to_nodes(s))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'; json.dump(res, open(tmp, 'w'), separators=(',', ':')); os.replace(tmp, path)
    if log: log(f"{config_name(stacks)} : {info['seconds']:.0f} s, exploitabilité {', '.join(f'{x:.2f}' for x in info['exploitability_mbb'])} mBB par main")
    return res, path


# ------------------------------------------------------------------ contrôles et calage
def controls(info, params):
    """[(id, libellé, ok, détail)] propres au solveur ; tous bloquants"""
    worst = max(info['exploitability_mbb'])
    out = [('exploitability', 'Exploitabilité de la stratégie', worst <= MAX_EXPLOITABILITY_MBB,
            f'{worst:.2f} mBB par main au pire (seuil {MAX_EXPLOITABILITY_MBB:g})')]
    if params['model'] == 'realization':
        dr = info.get('drift_mbb')
        out.append(('stability', 'Stabilité préflop / postflop', dr is not None and dr <= MAX_DRIFT_MBB,
                    f"dérive au dernier tour {dr} mBB par main (seuil {MAX_DRIFT_MBB:g}), variation des fréquences {info['shift_pts']} points"))
    return out


def reference_nodes(tree, stacks, raw=None):
    """nœuds de la référence pour ce même arbre et ces tapis (répétitions moyennées), ou None"""
    found = []
    for d in hrc.exports(raw) if raw else hrc.exports():
        s, st, nodes = hrc.load(d)
        if hrc.preflop_hash(s) == tree and tuple(st) == tuple(float(x) for x in stacks): found.append((d, s, st, nodes))
    if not found: return None
    mode = lambda s: s['treeconfig']['postflop']['id'].split('.')[-1]
    best = min(found, key=lambda x: importer.POSTFLOP_PREFERENCE.index(mode(x[1])) if mode(x[1]) in importer.POSTFLOP_PREFERENCE else 9)
    base = lambda d: d.split(os.sep)[-2]
    runs = [x for x in found if base(x[0]) == base(best[0]) and hrc.tree_hash(x[1]) == hrc.tree_hash(best[1])]
    nodes = hrc.average([x[1:] for x in runs]) if len(runs) > 1 else best[3]
    return dict(exports=[os.path.relpath(x[0], hrc.ROOT) for x in runs], nodes=nodes)


def calibrate(res, raw=None):
    """calage d'une configuration sur la référence (None si la référence n'a pas cet arbre et ces tapis)"""
    if not res['tree'] in REFERENCE_TREES: return None
    ref = reference_nodes(res['tree'], res['stacks'], raw)
    if ref is None: return None
    st = [float(x) for x in res['stacks']]
    ours = {k: dict(actions=hrc.labels(n, st), freq=np.array([n['hands'][h]['played'] for h in NAMES])) for k, n in res['nodes'].items()}
    out = calibration.summary(calibration.compare(ours, st, ref['nodes']))
    return out and dict(out, exports=ref['exports'])


# ------------------------------------------------------------------ spots et publication
def spots_of(res, path):
    st = [float(x) for x in res['stacks']]; cfg = res['tree_config']; nodes = res['nodes']
    sizes = dict(BTN=cfg['open_btn'] if len(st) == 3 else None, SB=cfg['open_sb'], BB_iso=cfg['iso_base'])
    prov = dict(source='solveur', solver=res['solver'], run=os.path.relpath(path, hrc.ROOT), model=res['params']['model'],
                iterations=res['info']['iterations'], exploitability_mbb=res['info']['exploitability_mbb'],
                equity_matrix=os.path.basename(allin.EQUITY_FILE))
    spots, skipped = [], []
    for key in sorted(nodes, key=lambda k: (k.count('_'), k)):
        sp = importer.make_spot(st, nodes, key, res['tree'], sizes, prov)
        if sp and sp['eligible_hands'] == 0: skipped.append((config_name(st), f'{key} : aucune main proposable'))
        elif sp: spots.append(sp)
    return spots, skipped


def build(configs, cfg=None, params=None, workers=4, runs=RUNS, raw=None, log=print):
    """(spots, rejets, rapport par configuration, écartés)"""
    cfg = cfg or TreeConfig(); params = params or SolveParams()
    spots, rejected, report, skipped = [], [], [], []
    for stacks in configs:
        res, path = run(stacks, cfg, params, workers, runs, log)
        ctl = controls(res['info'], res['params'])
        for cid, label, ok, detail in ctl:
            if not ok: rejected.append((config_name(stacks), cid, f'{label} : {detail}'))
        try:
            sp, sk = spots_of(res, path); spots += sp; skipped += sk
        except importer.InvalidSpot as e:
            rejected.append((config_name(stacks), 'spot', str(e))); sp = []
        report.append(dict(config=config_name(stacks), stacks=list(stacks), run=os.path.relpath(path, hrc.ROOT), spots=len(sp),
                           seconds=res['info']['seconds'], exploitability_mbb=res['info']['exploitability_mbb'], shift_pts=res['info']['shift_pts'], drift_mbb=res['info'].get('drift_mbb'),
                           controls=[dict(id=c, label_fr=l, ok=bool(o), details_fr=d) for c, l, o, d in ctl], calibration=calibrate(res, raw)))
    return spots, rejected, report, skipped


def publish(version, out, configs, cfg=None, params=None, workers=4, runs=RUNS, raw=None, log=print):
    cfg = cfg or TreeConfig(); params = params or SolveParams()
    target = os.path.join(out, version)
    if os.path.exists(target): raise SystemExit(f'{target} existe déjà : une version publiée est immuable, choisir un nouveau numéro')
    spots, rejected, report, skipped = build(configs, cfg, params, workers, runs, raw, log)
    if rejected: raise SystemExit('Publication bloquée :\n' + '\n'.join(f'  {c} {k} : {m}' for c, k, m in rejected))
    os.makedirs(target)
    with open(os.path.join(target, 'spots.jsonl'), 'w') as f:
        for sp in spots: f.write(json.dumps(sp, ensure_ascii=False, separators=(',', ':')) + '\n')
    digest = hashlib.sha256(open(os.path.join(target, 'spots.jsonl'), 'rb').read()).hexdigest()
    manifest = dict(dataset='gto_preflop', version=version, created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                    source='solveur', solver=SOLVER_VERSION, importer=importer.IMPORTER_VERSION, reference_preflop_tree=tree_id(cfg),
                    tree_config=dataclasses.asdict(cfg), params=dataclasses.asdict(params), run=run_id(cfg, params), model='chip_ev',
                    spots=len(spots), spots_sha256=digest,
                    ev_reference_rule="EV exacte si chaque action autre que fold en a une, sinon EV du solveur",
                    min_reach_for_questions=importer.MIN_REACH, max_self_regret_mbb=importer.MAX_SELF_REGRET_MBB,
                    mixed_min=MIXED_MIN, max_mixed_regret_mbb=importer.MAX_MIXED_REGRET_MBB,
                    max_exploitability_mbb=MAX_EXPLOITABILITY_MBB, max_drift_mbb=MAX_DRIFT_MBB,
                    questions_eligible=sum(sp['eligible_hands'] for sp in spots),
                    configs=report, sources=[r['run'] for r in report], skipped=[dict(export=c, reason=r) for c, r in skipped],
                    status='staging')
    json.dump(manifest, open(os.path.join(target, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    return manifest


def rebuild(manifest, runs_root=hrc.ROOT):
    """spots reconstruits depuis les résultats enregistrés (sans recalcul) : {spot_id: spot}"""
    out = {}
    for r in manifest['configs']:
        path = os.path.join(runs_root, r['run']); res = json.load(open(path))
        for sp in spots_of(res, path)[0]: out[sp['spot_id']] = sp
    return out


def check(ref, datasets, workers=4, log=print):
    """test de référence complet : recalcule chaque configuration avec les réglages du manifeste et compare les spots"""
    d = os.path.join(datasets, ref); manifest = json.load(open(os.path.join(d, 'manifest.json')))
    published = {}
    for line in open(os.path.join(d, 'spots.jsonl')):
        sp = json.loads(line); published[sp['spot_id']] = sp
    cfg = TreeConfig(**manifest['tree_config']); params = SolveParams(**manifest['params'])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        rebuilt = {}
        for r in manifest['configs']:
            res, path = run(tuple(r['stacks']), cfg, params, workers, tmp, log)
            for sp in spots_of(res, os.path.join(hrc.ROOT, r['run']))[0]: rebuilt[sp['spot_id']] = sp
    norm = lambda o: json.loads(json.dumps(o))
    diff = [k for k, sp in published.items() if k not in rebuilt or norm(rebuilt[k]) != norm(sp)]
    return not diff, diff


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--version'); ap.add_argument('--check', metavar='REF')
    ap.add_argument('--out', default=os.path.join(hrc.ROOT, 'data', 'datasets', 'gto_preflop'))
    ap.add_argument('--configs', help='par exemple hu:12-12,3w:12-12-12'); ap.add_argument('--grid', choices=['p1'])
    ap.add_argument('--model', default='realization', choices=['realization', 'showdown'])
    ap.add_argument('--pre-iters', type=int, default=1500); ap.add_argument('--outer', type=int, default=10)
    ap.add_argument('--post-iters', type=int, default=3000); ap.add_argument('--boards', type=int, default=1000)
    ap.add_argument('--workers', type=int, default=4, help='processus pour les sous-jeux postflop (mettre le nombre de cœurs)')
    ap.add_argument('--tree', default='reference', choices=list(TREES), help='reference : BTN 2,3 BB, SB 3,5 BB ; v5 : ouvertures à 2 BB')
    ap.add_argument('--postflop', default='production', choices=list(PRESETS), help='réglage de regroupement après le flop (G13)')
    a = ap.parse_args()
    if a.check:
        ok, diff = check(a.check, os.path.dirname(os.path.dirname(a.out)), a.workers)
        raise SystemExit(0 if ok else f'{len(diff)} spots diffèrent du recalcul (premier : {diff[0]})')
    if not a.version or not (a.configs or a.grid): ap.error('--version et --configs (ou --grid) sont requis')
    configs = [st for _, st in GRID_P1] if a.grid else parse_configs(a.configs)
    p = SolveParams(model=a.model, pre_iters=a.pre_iters, outer=a.outer, post_iters=a.post_iters, boards=a.boards,
                    postflop=dataclasses.asdict(PostflopConfig(**PRESETS[a.postflop])))
    m = publish(a.version, a.out, configs, cfg=TREES[a.tree], params=p, workers=a.workers)
    print(f"{m['spots']} spots publiés en staging : {m['version']} ({len(m['configs'])} configurations, {m['questions_eligible']} questions)")
