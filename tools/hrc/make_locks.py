"""Stratégies adverses à verrouiller dans HRC (node locking) pour le mode exploitant.

Pour chaque export HRC GTO, chaque position du héros et chaque profil, on prend tous les nœuds
exportés des adversaires et on déforme leur stratégie GTO selon le profil. On verrouille ensuite
ces nœuds dans HRC et on relance le calcul : la stratégie du héros devient la meilleure réponse
au profil.

Règles de déformation (à valider avec l'expert poker) :
  - les actions d'un nœud sont regroupées : AGG (raise, all-in), PAS (limp, call), F (fold),
    X (check gratuit) ;
  - la fréquence globale d'un groupe est multipliée sur les cotes : p' = k p / (1 + (k - 1) p),
    comme dans legacy/conversation/exploit_engine.py ;
  - quand un groupe augmente, on y ajoute les mains qui foldaient, de la plus forte à la plus faible
    (ordre : fréquence GTO du groupe, puis équité contre une main aléatoire) ;
  - quand un groupe baisse, on retire les mains les plus faibles (équité contre une main aléatoire) ;
    elles vont au fold, sauf pour
    le fish dont l'agressivité retirée devient passive ;
  - si le nœud n'a pas de fold, ou si checker est gratuit (BB face à un limp), le check sert de réserve.

Usage : python tools/hrc/make_locks.py [--out data/hrc/locks]
"""
import argparse, csv, glob, json, os
import numpy as np

from hrc_io import RAW, ROOT, NC, POS3, POS2, preflop_hash, labels, key_of, exports, stacks_of

VSR = json.load(open(os.path.join(os.path.dirname(__file__), 'equity_vs_random.json')))['equity_vs_random']

PROFILES = {  # facteurs sur les cotes : AGG (raise / all-in), PAS (limp / call)
    'nit': dict(AGG=0.5, PAS=0.5, agg_cut_to='F'),
    'fish': dict(AGG=0.9, PAS=2.0, agg_cut_to='PAS'),
    'maniac': dict(AGG=2.0, PAS=1.3, agg_cut_to='F'),
}
MIN_STACK = 10          # sous 10 BB, l'exploitant tout ou rien (exploit_engine) et exp_hu_solver suffisent
PRIORITY_STACKS = (12, 15, 20)
REF_PREFLOP = 'daa9aaa0'   # empreinte de l'arbre préflop retenu (limp du BTN autorisé), voir data/hrc/README.md


def group_of(lab, labs):
    if lab in ('A',) or lab.startswith('R'): return 'AGG'
    if lab == 'X': return 'X'
    if lab == 'C': return 'PAS'
    return 'F'


def odds(p, k):
    return k * p / (1 + (k - 1) * p) if 0 < p < 1 else p


def deform(node, st, prof):
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
    for g in ('AGG', 'PAS'):
        cols = [j for j, x in enumerate(grp) if x == g and j != sink]
        if not cols: continue
        k = prof[g]
        x = float((mass * P[:, cols].sum(1)).sum() / mass.sum()); target = odds(x, k)
        delta = (target - x) * mass.sum()
        main = max(cols, key=lambda j: (mass * P[:, j]).sum())
        gf = P[:, cols].sum(1)
        if delta > 0:                          # ajouter des mains depuis la réserve, des plus fortes aux plus faibles
            for i in np.lexsort((-vsr, -gf)):
                if delta <= 1e-12: break
                take = min(P[i, sink], delta / mass[i]) if mass[i] > 0 else 0
                P[i, sink] -= take; P[i, main] += take; delta -= take * mass[i]
        elif delta < 0:                        # retirer les mains les plus faibles
            dest = sink
            if g == 'AGG' and prof['agg_cut_to'] == 'PAS':
                pas = [j for j, y in enumerate(grp) if y == 'PAS']
                if pas: dest = pas[0]
            need = -delta
            for i in np.argsort(vsr, kind='stable'):
                if need <= 1e-12: break
                if mass[i] <= 0: continue
                have = P[i, cols].sum()
                if have <= 0: continue
                take = min(have, need / mass[i]); share = P[i, cols] / have
                P[i, cols] -= take * share; P[i, dest] += take; need -= take * mass[i]
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
        for pname, prof in PROFILES.items():
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
                json.dump(dict(source=src, profile=pname, factors=prof, hero=names[hero], stacks_bb=st, locks=locks),
                          open(os.path.join(out, rel, 'locks.json'), 'w'), ensure_ascii=False, indent=1)
                with open(os.path.join(out, rel, 'ranges.txt'), 'w') as f:
                    f.write(f"Source GTO : {src}\nProfil : {pname} {prof}\nHéros (nœuds libres) : {names[hero]}\n\n")
                    for L in sorted(locks, key=lambda x: (x['node'].count('_'), x['node'])):
                        f.write(f"=== Nœud {L['node']} (joue : {L['player']})\n")
                        for lab, txt in L['ranges'].items(): f.write(f"  {lab}: {txt or '(aucune main)'}\n")
                        f.write('\n')
                manifest.append(dict(priority='P1' if st[0] in PRIORITY_STACKS else 'P2', solve_id=f'{pname}_{tag}_hero{names[hero]}', profile=pname, table='3-handed' if len(st) == 3 else 'heads-up',
                                     stacks=' / '.join(f'{x:g}' for x in st), hero=names[hero], gto_source=src, nodes_locked=len(locks), lock_file=os.path.join(rel, 'locks.json')))
    manifest.sort(key=lambda r: (r['priority'], r['table'], float(r['stacks'].split(' / ')[0]), r['profile'], r['hero']))
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)
    return manifest


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(ROOT, 'data', 'hrc', 'locks'))
    m = main(ap.parse_args().out); print(len(m), 'calculs à lancer dans HRC')
