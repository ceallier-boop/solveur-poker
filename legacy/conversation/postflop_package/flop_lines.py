"""Carte des situations qui atteignent le flop dans les arbres HRC : ligne préflop, fréquence, pot, stack restant, SPR.
Version corrigée : la probabilité d'une ligne est le produit, sur les joueurs, de la probabilité jointe de leurs actions
(la fréquence HRC du DERNIER noeud d'un joueur contient déjà ses actions précédentes via son poids d'atteinte) ;
les lignes où un joueur est à tapis (aucune décision postflop) sont écartées ; un contrôle vérifie que les feuilles de l'arbre somment à 1."""
import numpy as np
from hrcdata import *
import hrc_surrogate as hs
import eval_vs_hrc as ev


def _leaf_prob(path_i, node_player, g_action):
    last = {}
    for p, gp in path_i: last[p] = gp          # dernier noeud de chaque joueur sur le chemin
    last[node_player] = g_action               # l'action courante remplace le dernier noeud du joueur qui agit
    return float(np.prod(list(last.values())))


def lines(kd, h):
    s, nodes = load(kd, h); st = stacks_of(s); n = len(st)
    names = ['BTN', 'SB', 'BB'] if n == 3 else ['SB', 'BB']
    init = [0.0, 0.5, 1.0] if n == 3 else [0.5, 1.0]
    path, g = ev.path_probs(nodes, st)
    out = []; leaves = 0.0; allin_mass = 0.0
    for i, nd in nodes.items():
        commit = list(init); folded = [False] * n
        for a in nd['sequence']:
            p = a['player']; amt = a['amount'] / 10000
            if a['type'] == 'F': folded[p] = True
            elif a['type'] == 'C': commit[p] += amt
            elif a['type'] == 'R': commit[p] = amt
        for j, a in enumerate(nd['actions']):
            prob = _leaf_prob(path[i], nd['player'], g[(i, j)])
            if a.get('node') is None: leaves += prob                       # feuille de l'arbre exporté
            if a['type'] not in ('C', 'X') or a.get('node') is not None: continue
            c2 = list(commit); p = nd['player']
            if a['type'] == 'C': c2[p] += a['amount'] / 10000
            mx = max(c2)
            inpot = [q for q in range(n) if not folded[q] and abs(c2[q] - mx) < 1e-9]
            if len(inpot) < 2: continue
            rem = min(st[q] - c2[q] for q in inpot)
            if rem <= 1e-9:                                                # un joueur est à tapis : pas de décision postflop
                allin_mass += prob; continue
            pot = sum(c2)
            seq = ' ; '.join(f"{names[x['player']]} {('fold' if x['type']=='F' else 'check' if x['type']=='X' else 'paie' if x['type']=='C' else ('all-in' if x['amount']/10000>=st[x['player']]-1e-9 else 'raise '+format(x['amount']/10000,'g')))}" for x in nd['sequence'])
            last = names[nd['player']] + (' paie' if a['type'] == 'C' else ' check')
            out.append(dict(prob=prob, pot=pot, rem=rem, spr=rem / pot, players=[names[q] for q in inpot], line=(seq + ' ; ' if seq else '') + last))
    return st, sorted(out, key=lambda r: -r['prob']), leaves, allin_mass


if __name__ == '__main__':
    for kind, base in (('hu', hs.EQHU), ('3w', hs.EQ3)):
        for S in (8, 10, 12, 15, 18, 25):
            v = base[S]; loc = v[0] if isinstance(v, list) else v
            kd, h = hs._loc(kind, loc)
            st, L, leaves, am = lines(kd, h)
            tot = sum(r['prob'] for r in L)
            print(f"\n== {'Heads-up' if kind=='hu' else '3 joueurs'} {S} BB : mains qui voient le flop {100*tot:.1f} % | somme des feuilles de l'arbre {leaves:.4f}")
            for r in L[:5]:
                print(f"   {100*r['prob']:5.1f} %  pot {r['pot']:4.1f}  reste {r['rem']:5.1f}  SPR {r['spr']:4.1f}  joueurs {'/'.join(r['players'])} | {r['line']}")
