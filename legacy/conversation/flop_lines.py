"""Carte des situations qui atteignent le flop dans les arbres HRC : ligne préflop, fréquence, pot, stack restant, SPR."""
import numpy as np
from hrcdata import *
import hrc_surrogate as hs
import eval_vs_hrc as ev

def lines(kd, h):
    s, nodes = load(kd, h); st = stacks_of(s); n = len(st)
    names = ['BTN', 'SB', 'BB'] if n == 3 else ['SB', 'BB']
    init = [0.0, 0.5, 1.0] if n == 3 else [0.5, 1.0]
    path, g = ev.path_probs(nodes, st)
    out = []
    for i, nd in nodes.items():
        labs = act_labels(nd, st)
        reach = 1.0
        for (p_, gp) in path[i]: reach *= gp
        # engagements au noeud : rejouer la séquence
        commit = list(init); folded = [False] * n
        for a in nd['sequence']:
            p = a['player']; amt = a['amount'] / 10000
            if a['type'] == 'F': folded[p] = True
            elif a['type'] == 'C': commit[p] += amt
            elif a['type'] == 'R': commit[p] = amt
        for j, a in enumerate(nd['actions']):
            if a['type'] not in ('C', 'X') or a.get('node') is not None: continue
            if a['type'] == 'C' and a['amount'] / 10000 >= st[nd['player']] - commit[nd['player']] - 1e-9: continue   # call all-in : pas de flop
            c2 = list(commit); p = nd['player']
            if a['type'] == 'C': c2[p] += a['amount'] / 10000
            # joueurs encore dans le coup : ceux qui n'ont pas foldé et ont misé le montant maximal (BB auto-fold si non atteint dans l'arbre HRC)
            mx = max(c2)
            inpot = [q for q in range(n) if not folded[q] and abs(c2[q] - mx) < 1e-9]
            if len(inpot) < 2: continue
            pot = sum(c2); rem = min(st[q] - c2[q] for q in inpot)
            prob = reach * g[(i, j)]
            seq = ' ; '.join(f"{names[x['player']]} {('fold' if x['type']=='F' else 'check' if x['type']=='X' else 'limp' if (x['type']=='C' and x is nd['sequence'][0] and names[x['player']] in ('SB','BTN') and abs(x['amount']/10000-0.5)<1e-9 or (x['type']=='C' and x['amount']/10000==1.0 and names[x['player']]=='BTN')) else 'paie' if x['type']=='C' else ('all-in' if x['amount']/10000>=st[x['player']]-1e-9 else 'raise '+format(x['amount']/10000,'g')))}" for x in nd['sequence'])
            last = names[nd['player']] + (' paie' if a['type'] == 'C' else ' check')
            out.append(dict(prob=prob, pot=pot, rem=rem, spr=rem / pot, players=[names[q] for q in inpot], line=(seq + ' ; ' if seq else '') + last))
    return st, sorted(out, key=lambda r: -r['prob'])

if __name__ == '__main__':
    for kind, base in (('hu', hs.EQHU), ('3w', hs.EQ3)):
        for S in (8, 10, 12, 15, 18, 25):
            v = base[S]; loc = v[0] if isinstance(v, list) else v
            kd, h = hs._loc(kind, loc)
            st, L = lines(kd, h)
            tot = sum(r['prob'] for r in L)
            print(f"\n== {'Heads-up' if kind=='hu' else '3 joueurs'} {S} BB : part des mains qui voient le flop {100*tot:.0f} %")
            for r in L[:5]:
                print(f"   {100*r['prob']:5.1f} %  pot {r['pot']:4.1f}  reste {r['rem']:5.1f}  SPR {r['spr']:4.1f}  joueurs {'/'.join(r['players'])} | {r['line']}")
