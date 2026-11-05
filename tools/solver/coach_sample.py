"""Échantillon pour les coachs : situations du solveur maison, en priorité celles où il s'écarte de la référence (action G12, 30/10/2026).

Pour chaque spot d'une banque du solveur dont la référence a le même arbre et les mêmes tapis, et pour chaque main
proposable : action dominante du solveur et de la référence, et perte de la stratégie du solveur mesurée avec les EV de la
référence (moins le regret de la référence elle-même, son bruit). Tirage :
  - désaccords (actions dominantes différentes) qui coûtent plus que le bruit de la référence (MIN_GAP_MBB au-delà de son
    propre regret), classés par fréquence réelle de la situation (probabilité de la ligne × atteinte de la main × combos), au
    plus MAX_PER_SPOT par spot. Les lignes rares sont celles où le Monte-Carlo de la référence est le plus maigre : ses EV y
    sont parfois impossibles (payer un tapis qui « coûte » plus que la mise) ; ces mains sont écartées, et comptées ;
  - quelques décisions serrées (même action dominante, autre action à moins de 0,1 BB chez l'un des deux) ;
  - des témoins où les deux sont d'accord, pour mesurer l'accord des coachs avec les deux calculs.
Les deux calculs sont présentés à l'aveugle (« calcul A » / « calcul B », tirés au hasard à chaque question) : la clé est
dans cle.csv, à ne pas donner aux coachs.

Usage : python tools/solver/coach_sample.py docs/relecture/solveur_2026-10-30 --bank gto_preflop/2026.10.29-s1 [--n 60]
"""
import argparse, csv, json, os, random, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import hrc, quiz  # noqa: E402
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.ranges import situation_fr  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402

MAX_PER_SPOT = 3
MIN_GAP_MBB = 50.0
MIN_LINE = 0.02                   # témoins et décisions serrées : lignes qui arrivent au moins 2 % du temps
SHARES = (('desaccord', 0.65), ('serree', 0.15), ('accord', 0.20))
SUITS = '♠♥♦♣'
GRID = ['id', 'coach', 'meilleure_action', 'calcul_le_plus_juste', 'confiance', 'commentaire']


def cards(h):
    """une écriture de la main avec des couleurs (paire : deux couleurs ; assortie : même couleur)"""
    if len(h) == 2: return f'{h[0]}{SUITS[0]} {h[1]}{SUITS[1]}'
    return f'{h[0]}{SUITS[0]} {h[1]}{SUITS[0] if h[2] == "s" else SUITS[1]}'


def rows_of(bank):
    d = quiz.ref_path(bank); m = json.load(open(os.path.join(d, 'manifest.json')))
    spots = [json.loads(l) for l in open(os.path.join(d, 'spots.jsonl'))]
    refs = {}; out = []
    for sp in spots:
        st = tuple(sp['stacks_bb'])
        if st not in refs: refs[st] = ds.reference_nodes(sp['preflop_tree'], st)
        ref = refs[st]
        if ref is None or sp['node_key'] not in ref['nodes']: continue
        n = ref['nodes'][sp['node_key']]; hl = hrc.labels(n, list(st)); ids = [a['id'] for a in sp['actions']]
        if not set(ids) <= set(hl): continue
        line = line_prob(sp, ref['nodes'], list(st))
        hero = sp['players'].index(sp['hero']); room = sp['stacks_bb'][hero] - sp['hero_committed_bb']
        for h in NAMES:
            H = sp['hands'][h]
            if not H['quiz_eligible']: continue
            rf = np.array([n['hands'][h]['played'][hl.index(a)] for a in ids]); re = np.array([n['hands'][h]['evs'][hl.index(a)] for a in ids])
            rf = rf / max(rf.sum(), 1e-12)
            sf = np.array(H['freq']); se = np.array(H['ev_exact'] if sp['ev_reference'] == 'exact' else H['ev_hrc'], float)
            loss = 1000 * (re.max() - (sf * re).sum()); floor = 1000 * (re.max() - (rf * re).sum())
            close = lambda e: sorted(e)[-1] - sorted(e)[-2] < 0.1 if len(e) > 1 else False
            impossible = bool(re.min() < -(room + 0.05))              # perdre plus que ce qu'il reste à miser : EV de référence aberrante
            out.append(dict(spot=sp, hand=h, ids=ids, sf=sf, se=se, rf=rf, re=re, loss=loss, floor=floor, reach=H['reach'], line=line,
                            weight=line * H['reach'] * W[NAMES.index(h)], impossible=impossible,
                            kind='desaccord' if sf.argmax() != rf.argmax() else ('serree' if close(se) or close(re) else 'accord')))
    return m, out


def line_prob(sp, nodes, st):
    """probabilité que la ligne de la situation se produise, d'après la référence : produit, sur l'historique, de la fréquence
    globale (combos x atteinte) de l'action jouée par chaque joueur"""
    p = 1.0; keys = sp['node_key'].split('_') if sp['node_key'] != 'root' else []
    for k in range(len(keys)):
        prev = '_'.join(keys[:k]) or 'root'; n = nodes.get(prev)
        if n is None: return 0.0
        seq = keys[k]; lab = hrc.labels(n, st)
        w = W * np.array([n['hands'][h]['weight'] for h in NAMES])
        # action jouée : retrouvée par la clé du fils
        j = next((i for i, a in enumerate(n['actions']) if hrc.key_of(n['sequence'] + [dict(a, player=n['player'])], st).split('_')[-1] == seq), None)
        if j is None: return 0.0
        f = np.array([n['hands'][h]['played'][j] for h in NAMES]); p *= float((w * f).sum() / max(w.sum(), 1e-12))
    return p


def pick(rows, n, rng):
    per = {k: int(round(n * s)) for k, s in SHARES}; per['accord'] = n - per['desaccord'] - per['serree']
    out = []
    for kind, k in per.items():
        cand = [r for r in rows if r['kind'] == kind and not r['impossible'] and (kind == 'desaccord' or r['line'] >= MIN_LINE)]
        if kind == 'desaccord':
            cand = [r for r in cand if r['loss'] - r['floor'] > MIN_GAP_MBB]; cand.sort(key=lambda r: -r['weight'])
        else: rng.shuffle(cand)
        used = {}
        for r in cand:
            key = r['spot']['spot_id']
            if used.get(key, 0) >= MAX_PER_SPOT: continue
            used[key] = used.get(key, 0) + 1; out.append(r)
            if sum(1 for x in out if x['kind'] == kind) >= k: break
    rng.shuffle(out)
    return out


def fiche(i, r, a_is_solver):
    sp = r['spot']; labels = [quiz.action_label(sp, a) for a in sp['actions']]
    A = (r['sf'], r['se']) if a_is_solver else (r['rf'], r['re']); B = (r['rf'], r['re']) if a_is_solver else (r['sf'], r['se'])
    L = [f"## S{i:03d} · {'3 joueurs' if sp['table'] == '3-handed' else 'heads-up'} · {sp['hero']} · {quiz.bb(quiz.hero_effective(sp))} BB effectifs · {r['hand']}", '',
         situation_fr(sp).replace('\n', '  \n') + f"  \nTa main : **{cards(r['hand'])}** ({r['hand']}). Que fais-tu ?", '',
         '| Option | Calcul A : fréquence | Calcul A : EV (BB) | Calcul B : fréquence | Calcul B : EV (BB) |', '|---|---|---|---|---|']
    for j, lab in enumerate(labels):
        L.append(f'| {lab} | {100 * A[0][j]:.0f} % | {A[1][j]:+.3f} | {100 * B[0][j]:.0f} % | {B[1][j]:+.3f} |')
    L += ['', f"Action dominante : calcul A **{labels[int(A[0].argmax())]}**, calcul B **{labels[int(B[0].argmax())]}**.", '']
    return '\n'.join(L)


CONSIGNES = """# Relecture des calculs du solveur : consignes

Échantillon du {date} : {n} situations préflop (identifiants S001 à S{n:03d}), banque `{bank}`.

## Ton rôle

Tu es un joueur expert d'Expresso / Spin & Go (3 joueurs puis heads-up, préflop, **chip EV**, sans ICM, blinds 0,5 / 1 BB, sans ante).
Pour chaque situation, deux calculs d'équilibre proposent une stratégie pour ta main : le **calcul A** et le **calcul B**. Tu dis lequel
te paraît le plus juste. Les deux sont présentés à l'aveugle : leur ordre change d'une situation à l'autre. Tu travailles seul : ne te
concerte pas avec les autres coachs, l'accord entre coachs est mesuré ensuite.

## Ce que montrent les fiches

- L'arbre est le même pour les deux calculs : ouverture du BTN à 2,3 BB, du SB à 3,5 BB, iso du BB à 3 BB face au limp du SB
  (3,5 BB + 1 BB par limper sinon), puis 3-bets et tapis.
- **Fréquence** : part du temps où le calcul joue chaque option avec cette main. **EV** : gain moyen de l'option en BB, relatif au fold
  (fold = 0). Les EV des deux calculs ne sont pas mesurées de la même façon et peuvent contenir un bruit de l'ordre de 0,1 BB :
  juge d'abord la décision, ensuite les montants.
- La plupart des situations sont choisies là où les deux calculs ne jouent pas la même action ; quelques-unes sont des témoins.

## Grille

Remplis une ligne par situation dans `reponses_modele.csv` (séparateur `;`, ne change ni l'ordre des lignes ni celui des colonnes) :

| Colonne | Valeurs | Sens |
|---|---|---|
| `id` | S001… | déjà rempli |
| `coach` | ton nom | |
| `meilleure_action` | le libellé d'une option (ex. `ALL-IN 25 BB`) | ce que tu joues avec cette main, en chip EV, contre des adversaires qui jouent l'équilibre |
| `calcul_le_plus_juste` | `A` / `B` / `les deux` / `aucun` | `les deux` : les deux options se valent (écart négligeable) |
| `confiance` | `forte` / `moyenne` / `faible` | |
| `commentaire` | texte libre, court | ce qui te fait trancher (une phrase suffit) |
"""


def main(out, bank, n, seed):
    rng = random.Random(seed); m, rows = rows_of(bank); sample = pick(rows, n, rng)
    os.makedirs(out, exist_ok=True)
    fiches, key = [], []
    for i, r in enumerate(sample, 1):
        a_is_solver = rng.random() < 0.5
        fiches.append(fiche(i, r, a_is_solver))
        key.append(dict(id=f'S{i:03d}', A='solveur' if a_is_solver else 'référence', B='référence' if a_is_solver else 'solveur', type=r['kind'],
                        spot=r['spot']['spot_id'], main=r['hand'], frequence_ligne=round(r['line'], 4), perte_solveur_mbb=round(r['loss'], 1), bruit_reference_mbb=round(r['floor'], 1),
                        atteinte=r['reach'], action_solveur=r['ids'][int(r['sf'].argmax())], action_reference=r['ids'][int(r['rf'].argmax())]))
    date = m['created_at'][:10]
    open(os.path.join(out, 'CONSIGNES.md'), 'w').write(CONSIGNES.format(date=date, n=len(sample), bank=bank))
    open(os.path.join(out, 'questions.md'), 'w').write(f"# Calculs A et B : situations S001 à S{len(sample):03d}\n\nConsignes : `CONSIGNES.md`.\n\n" + '\n'.join(fiches))
    with open(os.path.join(out, 'reponses_modele.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(GRID)
        for k in key: w.writerow([k['id']] + [''] * (len(GRID) - 1))
    with open(os.path.join(out, 'cle.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(key[0]), delimiter=';'); w.writeheader(); w.writerows(key)
    stats = {k: sum(1 for r in rows if r['kind'] == k) for k, _ in SHARES}
    gap = [r for r in rows if r['kind'] == 'desaccord' and not r['impossible'] and r['loss'] - r['floor'] > MIN_GAP_MBB]
    return dict(rows=len(rows), stats=stats, impossible=sum(r['impossible'] for r in rows), desaccords_au_dela_du_bruit=len(gap),
                part_ponderee_des_desaccords=round(sum(r['weight'] for r in gap) / max(sum(r['weight'] for r in rows), 1e-12), 4),
                sample={k: sum(1 for x in key if x['type'] == k) for k, _ in SHARES})


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--bank', default='gto_preflop/2026.10.29-s1')
    ap.add_argument('--n', type=int, default=60); ap.add_argument('--seed', type=int, default=30)
    a = ap.parse_args(); print(main(a.out, a.bank, a.n, a.seed))
