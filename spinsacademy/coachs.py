"""Avis des coachs et règle des désaccords (décision du porteur du 05/11/2026, docs/produit/DECISIONS_2026-11-05.md).

Les trois coachs ont rejoué 60 situations (relecture du 30/10/2026). Pour chaque main relue :
  - toute action donnée par au moins un coach est acceptée par la correction (« les deux stratégies sont possibles ») ;
  - quand les coachs se partagent (par exemple deux contre un), l'action la plus soutenue est la recommandée, avec la nuance
    « 2 experts sur 3 » : c'est un argument, pas une interdiction ;
  - quand les trois coachs jouent la même action et que le solveur préfère une autre, la réponse est acceptée et la
    correction dit ce que préfère le solveur (le défaut connu du solveur, docs/solver/BANQUE_SOLVEUR.md).
Aucun nom de coach n'apparaît : seulement un nombre de coachs. Les avis viennent de spinsacademy/data/avis_coachs.json
(tools/solver/build_avis_coachs.py). Une situation est retrouvée par son nom, sans l'empreinte de l'arbre : un autre arbre
qui garde les mêmes options reçoit les mêmes avis.
"""
import json
import os
import re

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'avis_coachs.json')
TYPES = {'FOLD': ('fold',), 'CHECK': ('check',), 'CALL': ('call', 'call_allin', 'limp'), 'ALL-IN': ('allin',), 'RAISE': ('raise',)}
_AVIS = None


def _avis():
    global _AVIS
    if _AVIS is None:
        try:
            with open(PATH, encoding='utf-8') as f: _AVIS = json.load(f)['avis']
        except OSError: _AVIS = {}
    return _AVIS


def situation(spot_id): return spot_id.rsplit('-', 1)[0]


def action_id(sp, label):
    """l'option du spot que désigne le libellé d'un coach (« RAISE TO 2,3 BB », « CALL 0,5 BB »…), None si aucune ou plusieurs"""
    word = label.split()[0]
    c = [a for a in sp['actions'] if a['type'] in TYPES.get(word, ())]
    if word == 'RAISE' and len(c) > 1:
        m = re.search(r'([\d,]+) BB', label)
        to = float(m.group(1).replace(',', '.')) if m else None
        c = [a for a in c if to is not None and abs(a['to_bb'] - to) < 0.01]
    return c[0]['id'] if len(c) == 1 else None


def lookup(sp, hand):
    """avis résolu sur les options du spot : {votes: {id d'action: nombre de coachs}, coachs, recommended, split}, ou None
    (situation non relue, ou une action des coachs qui ne correspond à aucune option de ce spot)"""
    if sp.get('field') or 'spot_id' not in sp: return None
    e = _avis().get(f"{situation(sp['spot_id'])}|{hand}")
    if not e: return None
    votes = {}
    for label, n in e['votes'].items():
        aid = action_id(sp, label)
        if aid is None: return None
        votes[aid] = votes.get(aid, 0) + n
    top = max(votes, key=lambda a: votes[a])
    return dict(votes=votes, coachs=e['coachs'], recommended=top, split=len(votes) > 1)


def _n(n, total): return f"{n} expert{'s' if n > 1 else ''} sur {total}"      # l'application ne cite ni coach ni nom : « experts »


def judge(avis, chosen, labels, best_label, solver_best, solver_gain_bb):
    """ce que la correction dit d'une réponse quand des experts ont relu la main : (acceptée par les coachs, lignes, détail structuré)"""
    if not avis: return False, [], None
    total, votes = avis['coachs'], avis['votes']; rec = avis['recommended']
    if chosen not in votes:             # aucune action des experts : le joueur voit tout de même leur partage (Interface, 05/11), sans acceptation
        return False, [], dict(split=avis['split'], experts=total, nuance_fr=None, recommended=False, recommended_label=labels[rec],
                               options=[dict(id=a, label_fr=labels[a], experts=votes[a]) for a in sorted(votes, key=lambda a: (-votes[a], a))])
    others = sorted((a for a in votes if a != chosen), key=lambda a: -votes[a])
    detail = dict(split=avis['split'], experts=total, nuance_fr=_n(votes[chosen], total), recommended=chosen == rec,
                  recommended_label=labels[rec], options=[dict(id=a, label_fr=labels[a], experts=votes[a]) for a in sorted(votes, key=lambda a: (-votes[a], a))])
    if avis['split']:
        alt = ' ou '.join(labels[a] for a in others)
        if chosen == rec:
            line = (f"Les experts ne sont pas d'accord sur cette main : {labels[chosen]} ({_n(votes[chosen], total)}) est le plus recommandé, "
                    f"{alt} ({' / '.join(_n(votes[a], total) for a in others)}) se joue aussi. Les deux stratégies sont possibles.")
        else:
            line = (f"Les experts ne sont pas d'accord sur cette main : {labels[chosen]} ({_n(votes[chosen], total)}) est une stratégie possible. "
                    f"{labels[rec]} est plus souvent recommandé ({_n(votes[rec], total)}), sans que l'autre soit une erreur.")
    else:
        line = None
        if solver_best != chosen and solver_gain_bb:
            line = (f"Les {total} experts jouent {labels[chosen]} ici. Le solveur préfère {best_label}, avec {solver_gain_bb} de plus : "
                    "réponse acceptée, l'écart vient de la limite connue du solveur.")
    return True, [line] if line else [], detail
