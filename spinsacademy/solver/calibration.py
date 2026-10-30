"""Calage du solveur maison sur la référence : la référence ne sert qu'à mesurer le solveur, jamais à le calculer.

Pour chaque nœud de la référence qui existe dans l'arbre maison :
  - TV : distance de variation totale moyenne entre les deux stratégies (0 = identiques, 100 % = disjointes) ;
  - accord : part des mains (pondérées par combos et atteinte de la référence) où l'action dominante est la même ;
  - perte : regret de la stratégie maison mesuré avec les EV de la référence ; plancher : regret de la référence elle-même
    (son propre bruit) ;
  - hors référence : part de la stratégie maison sur des actions absentes de l'arbre de référence (non évaluable).
"""
import numpy as np
from ..cards import NAMES, W
from ..hrc import labels


def compare(strategy, st, nodes):
    rows = []
    for key, n in nodes.items():
        if key not in strategy: continue
        hl = labels(n, st); ours = strategy[key]
        P = np.array([n['hands'][h]['played'] for h in NAMES]); EV = np.array([n['hands'][h]['evs'] for h in NAMES])
        w = W * np.array([n['hands'][h]['weight'] for h in NAMES])
        if w.sum() <= 0: continue
        M = np.zeros_like(P); outside = np.zeros(169)
        for j, a in enumerate(ours['actions']):
            if a in hl: M[:, hl.index(a)] += ours['freq'][:, j]
            else: outside += ours['freq'][:, j]
        Mn = M / np.maximum(M.sum(1, keepdims=True), 1e-12)
        tv = 0.5 * np.abs(Mn - P).sum(1)
        agree = Mn.argmax(1) == P.argmax(1)
        best = EV.max(1); loss = best - (Mn * EV).sum(1); floor = best - (P * EV).sum(1)
        avg = lambda x: float((w * x).sum() / w.sum())
        glob = lambda F: [round(100 * float((w * F[:, j]).sum() / w.sum()), 1) for j in range(F.shape[1])]
        rows.append(dict(node=key, actions=hl, hrc=glob(P), ours=glob(Mn), tv=100 * avg(tv), agree=100 * avg(agree),
                         loss=1000 * avg(loss), floor=1000 * avg(floor), outside=100 * avg(outside), share=float(w.sum() / W.sum())))
    return rows


def summary(rows):
    """moyennes pondérées par la part de mains qui atteint chaque nœud : TV (%), accord (%), perte et plancher (mBB),
    et le pire nœud (perte la plus haute au-delà du plancher)"""
    if not rows: return None
    w = np.array([r['share'] for r in rows]); avg = lambda k: round(float(np.dot(w, [r[k] for r in rows]) / w.sum()), 1)
    worst = max(rows, key=lambda r: r['loss'] - r['floor'])
    return dict(nodes=len(rows), tv=avg('tv'), agree=avg('agree'), loss_mbb=avg('loss'), floor_mbb=avg('floor'), outside=avg('outside'),
                worst=dict(node=worst['node'], loss_mbb=round(worst['loss'], 1), floor_mbb=round(worst['floor'], 1)))
