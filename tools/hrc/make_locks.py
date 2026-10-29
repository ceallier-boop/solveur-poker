"""Stratégies adverses à verrouiller dans HRC (node locking) pour le mode exploitant.

Pour chaque export HRC GTO, chaque position du héros et chaque profil, on prend tous les nœuds
exportés des adversaires et on déforme leur stratégie GTO selon le profil. On verrouille ensuite
ces nœuds dans HRC et on relance le calcul : la stratégie du héros devient la meilleure réponse
au profil.

Profils : ceux du moteur exploitant (tools/field/profils_field.py), seule source des facteurs : rec passif (défaut,
facteurs selon la profondeur), calling station, dégène, nit. Le reg (tous ses facteurs à 1) est la solution GTO : aucun calcul.
Règles de déformation (à valider avec l'expert poker), alignées sur tools/field/exploit_engine.py :
  - les actions d'un nœud sont regroupées : AGG (raise, all-in), PAS (limp, call), F (fold),
    X (check gratuit) ;
  - le facteur dépend du contexte du nœud, comme dans le moteur :
      premier à parler : AGG × shove (open ou tapis), PAS × limp_k (limp) ;
      face à un limp : AGG × iso, PAS × limp_k ;
      face à une relance ou à un tapis : on continue (AGG + PAS) × call ;
  - la fréquence globale d'un groupe est multipliée sur les cotes : p' = k p / (1 + (k - 1) p) ;
  - quand un groupe augmente, on y ajoute les mains qui foldaient, de la plus forte à la plus faible
    (ordre : fréquence GTO du groupe, puis équité contre une main aléatoire) ;
  - quand un groupe baisse, on retire les mains les plus faibles (équité contre une main aléatoire) ; elles vont au fold ;
  - récréatifs (rec passif, station : drapeau `shape`) premier à parler : leur agressivité retirée devient du limp, et
    comme exploit_engine.rec_shape, REC_TOP de la baisse porte sur leurs mains fortes (As faibles gardés), le reste sur
    les plus faibles ;
  - si le nœud n'a pas de fold, ou si checker est gratuit (BB face à un limp), le check sert de réserve.
Le profil à la profondeur du calcul est pris au tapis effectif (stacks égaux) : au-delà de 12 BB, les facteurs du rec
passif restent ceux de 12 BB, comme dans le moteur.

Usage : python tools/hrc/make_locks.py [--out data/hrc/locks]
"""
import argparse, csv, glob, json, os, sys
import numpy as np

from hrc_io import RAW, ROOT, NC, POS3, POS2, preflop_hash, labels, key_of, exports, stacks_of
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'field'))
import profils_field as pf  # noqa: E402

VSR = json.load(open(os.path.join(os.path.dirname(__file__), 'equity_vs_random.json')))['equity_vs_random']

# profils du moteur verrouillés, avec leur nom de dossier ; le reg n'en a pas (solution GTO)
SLUG = {pf.DEFAULT: 'rec_passif', 'Calling station': 'station', 'Dégène': 'degene', 'Nit': 'nit'}
PROFILES = {SLUG[name]: name for name in pf.PROFILES if name in SLUG}
MIN_STACK = 10          # sous 10 BB, l'exploitant tout ou rien (exploit_engine) et exp_hu_solver suffisent
PRIORITY_STACKS = (12, 15, 20)
REF_PREFLOP = 'daa9aaa0'   # empreinte de l'arbre préflop retenu (limp du BTN autorisé), voir data/hrc/README.md


def group_of(lab, labs):
    if lab in ('A',) or lab.startswith('R'): return 'AGG'
    if lab == 'X': return 'X'
    if lab == 'C': return 'PAS'
    return 'F'


def context(node):
    """'raise' (face à une relance ou un tapis), 'limp' (face à un limp) ou 'first' (premier à parler)"""
    seq = node['sequence']
    if any(a['type'] == 'R' for a in seq): return 'raise'
    return 'limp' if any(a['type'] == 'C' for a in seq) else 'first'


def factors(profile, st):
    """facteurs du profil (nom du moteur) au tapis effectif du calcul"""
    return pf.factors(profile, min(st))


def plan(ctx, f):
    """(groupes, facteur, destination des mains retirées, forme du récréatif) dans l'ordre d'application"""
    rec = bool(f.get('shape'))
    if ctx == 'first': return [(('AGG',), f['shove'], 'PAS' if rec else 'F', rec), (('PAS',), f['limp_k'], 'F', False)]
    if ctx == 'limp': return [(('AGG',), f['iso'], 'F', False), (('PAS',), f['limp_k'], 'F', False)]
    return [(('AGG', 'PAS'), f['call'], 'F', False)]


def odds(p, k):
    return k * p / (1 + (k - 1) * p) if 0 < p < 1 else p


REC_AX = set(pf.REC_AX)


def deform(node, st, f):
    """stratégie du nœud déformée par les facteurs f du profil (profils_field.factors)"""
    labs = labels(node, st); hands = list(node['hands'])
    P = np.array([node['hands'][h]['played'] for h in hands], float)
    mass = np.array([NC(h) * node['hands'][h]['weight'] for h in hands], float)
    if mass.sum() <= 0: return None
    grp = [group_of(l, labs) for l in labs]
    sink = grp.index('F') if 'F' in grp else (grp.index('X') if 'X' in grp else None)
    if 'X' in grp and 'F' in grp:
        sink = grp.index('X')      # check gratuit : un fold n'a pas de sens
    if sink is None: return None
    vsr = np.array([VSR[h] for h in hands])
    weak_ax = np.array([h in REC_AX for h in hands])
    for gs, k, cut_to, shape in plan(context(node), f):
        cols = [j for j, x in enumerate(grp) if x in gs and j != sink]
        if not cols or k == 1: continue
        x = float((mass * P[:, cols].sum(1)).sum() / mass.sum()); target = odds(x, k)
        delta = (target - x) * mass.sum()
        main = max(cols, key=lambda j: (mass * P[:, j]).sum())
        gf = P[:, cols].sum(1)
        if delta > 0:                          # ajouter des mains depuis la réserve, des plus fortes aux plus faibles
            for i in np.lexsort((-vsr, -gf)):
                if delta <= 1e-12: break
                take = min(P[i, sink], delta / mass[i]) if mass[i] > 0 else 0
                P[i, sink] -= take; P[i, main] += take; delta -= take * mass[i]
        elif delta < 0:                        # retirer des mains : les plus faibles, ou pour un récréatif, aussi des fortes
            dest = sink
            if cut_to == 'PAS':
                pas = [j for j, y in enumerate(grp) if y == 'PAS']
                if pas: dest = pas[0]
            need = -delta
            passes = [(np.argsort(-vsr, kind='stable'), need * pf.REC_TOP, True), (np.argsort(vsr, kind='stable'), None, False)] if shape \
                else [(np.argsort(vsr, kind='stable'), None, False)]
            for order, budget, top in passes:
                budget = need if budget is None else budget
                for i in order:
                    if budget <= 1e-12: break
                    if mass[i] <= 0 or (top and weak_ax[i]): continue
                    have = P[i, cols].sum()
                    if have <= 0: continue
                    take = min(have, budget / mass[i]); share = P[i, cols] / have
                    P[i, cols] -= take * share; P[i, dest] += take; budget -= take * mass[i]; need -= take * mass[i]
    P = np.clip(P, 0, 1); P /= P.sum(1, keepdims=True)
    return labs, hands, P, mass


def range_text(hands, freq, mass=None):
    """notation « main:poids » (poids arrondi au centième), mains jouées à 0 omises"""
    return ','.join(f'{h}:{f:.2f}' if f < 0.995 else h for h, f in zip(hands, freq) if f >= 0.005)


def main(out):
    manifest = []; seen = set()
    for d in exports():                                    # le plus récent d'abord quand les stacks sont en double
        s = json.load(open(os.path.join(d, 'settings.json')))
        if preflop_hash(s) != REF_PREFLOP: continue
        st = stacks_of(s)
        if len(set(st)) > 1 or st[0] < MIN_STACK or tuple(st) in seen: continue     # stacks égaux à partir de 10 BB, un export par profondeur
        seen.add(tuple(st))
        names = POS3 if len(st) == 3 else POS2
        nodes = [json.load(open(f)) for f in glob.glob(os.path.join(d, 'nodes', '*.json'))]
        tag = ('3w_' if len(st) == 3 else 'hu_') + '-'.join(f'{x:g}' for x in st)
        src = os.path.relpath(d, ROOT)
        for pname, profile in PROFILES.items():
            prof = factors(profile, st)
            for hero in range(len(st)):
                locks = []
                for n in nodes:
                    if n['player'] == hero or len(n['actions']) < 2: continue
                    r = deform(n, st, prof)
                    if r is None: continue
                    labs, hands, P, mass = r
                    locks.append(dict(node=key_of(n['sequence'], st, names), player=names[n['player']], actions=labs,
                                      strategy={h: [round(float(x), 4) for x in P[i]] for i, h in enumerate(hands)},
                                      ranges={l: range_text(hands, P[:, j]) for j, l in enumerate(labs)}))
                if not locks: continue
                rel = os.path.join(pname, tag, f'hero_{names[hero]}')
                os.makedirs(os.path.join(out, rel), exist_ok=True)
                json.dump(dict(source=src, profile=pname, engine_profile=profile, factors={k: (round(v, 4) if isinstance(v, float) else v) for k, v in prof.items()}, hero=names[hero], stacks_bb=st, locks=locks),
                          open(os.path.join(out, rel, 'locks.json'), 'w'), ensure_ascii=False, indent=1)
                with open(os.path.join(out, rel, 'ranges.txt'), 'w') as f:
                    f.write(f"Source GTO : {src}\nProfil : {profile} ({pname}) : " + ', '.join(f"{k} {v:.2f}" for k, v in prof.items() if isinstance(v, float)) + f"\nHéros (nœuds libres) : {names[hero]}\n\n")
                    for L in sorted(locks, key=lambda x: (x['node'].count('_'), x['node'])):
                        f.write(f"=== Nœud {L['node']} (joue : {L['player']})\n")
                        for lab, txt in L['ranges'].items(): f.write(f"  {lab}: {txt or '(aucune main)'}\n")
                        f.write('\n')
                manifest.append(dict(priority='P1' if st[0] in PRIORITY_STACKS else 'P2', solve_id=f'{pname}_{tag}_hero{names[hero]}', profile=pname, engine_profile=profile, table='3-handed' if len(st) == 3 else 'heads-up',
                                     stacks=' / '.join(f'{x:g}' for x in st), hero=names[hero], gto_source=src, nodes_locked=len(locks), lock_file=os.path.join(rel, 'locks.json')))
    manifest.sort(key=lambda r: (r['priority'], r['table'], float(r['stacks'].split(' / ')[0]), r['profile'], r['hero']))
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)
    return manifest


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(ROOT, 'data', 'hrc', 'locks'))
    m = main(ap.parse_args().out); print(len(m), 'calculs à lancer dans HRC')
