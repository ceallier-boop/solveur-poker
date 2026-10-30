"""Lecture des exports HRC (settings.json + nodes/*.json) : empreintes d'arbre, clés de nœuds, étiquettes d'action,
moyenne des exports répétés d'un même calcul."""
import copy, glob, hashlib, json, os, re
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'hrc', 'raw')
POS3, POS2 = ['BTN', 'SB', 'BB'], ['SB', 'BB']
from .cards import NC
# Ordre de préférence quand plusieurs exports existent pour les mêmes stacks : le plus récent d'abord
BASE_PREFERENCE = ['v4', 'v3', 'v2', 'complement2', 'complement', 'min_raise_hu', 'min_raise_3way']


def _md5(obj):
    return hashlib.md5(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:8]


def tree_hash(settings):
    """empreinte de tous les réglages sauf les stacks (préflop, postflop, modèle, moteur)"""
    s = dict(settings); s.pop('handdata')
    return _md5(s)


def preflop_hash(settings):
    """empreinte de ce qui définit l'arbre préflop et sa valeur : préflop, modèle d'équité, moteur, blinds (sans les stacks)"""
    hd = {k: v for k, v in settings['handdata'].items() if k != 'stacks'}
    return _md5(dict(preflop=settings['treeconfig']['preflop'], eqmodel=settings['eqmodel'], engine=settings['engine'], handdata=hd))


def stacks_of(settings):
    return [x / 10000 for x in settings['handdata']['stacks']]


def positions(st):
    return POS3 if len(st) == 3 else POS2


def _cap(st, seq, player):
    """mise maximale utile pour `player` : son stack, plafonné au plus gros stack adverse encore en jeu (tapis effectif)"""
    folded = {a['player'] for a in seq if a['type'] == 'F'}
    others = [st[q] for q in range(len(st)) if q != player and q not in folded]
    return min(st[player], max(others)) if others else st[player]


def is_allin(amount_bb, st, seq, player):
    return amount_bb >= _cap(st, seq, player) - 1e-9


def labels(node, st):
    out = []
    for a in node['actions']:
        amt = a['amount'] / 10000
        if a['type'] == 'R':
            out.append('A' if is_allin(amt, st, node['sequence'], node['player']) else f'R{amt:g}')
        else:
            out.append(a['type'])
    return out


def key_of(seq, st, names=None):
    names = names or positions(st)
    out = []
    for k, a in enumerate(seq):
        amt = a['amount'] / 10000
        t = {'F': 'fold', 'C': 'call', 'X': 'check'}.get(a['type'])
        if a['type'] == 'R':
            t = 'allin' if is_allin(amt, st, seq[:k], a['player']) else f'raise{amt:g}'
        out.append(f"{names[a['player']]}-{t}")
    return '_'.join(out) or 'root'


def load(d):
    """(settings, stacks, {clé: nœud}) pour un dossier d'export"""
    s = json.load(open(os.path.join(d, 'settings.json'))); st = stacks_of(s)
    nodes = {}
    for f in glob.glob(os.path.join(d, 'nodes', '*.json')):
        n = json.load(open(f)); nodes[key_of(n['sequence'], st)] = n
    return s, st, nodes


def _natural(name):
    """clé de tri naturelle : hand_2 avant hand_10, hu_12-12_r2 avant hu_12-12_r10"""
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', name)]


def exports(raw=RAW):
    """tous les dossiers d'export (`<base>/<dossier>/settings.json` : hand_N jusqu'à la v3, <table>_<tapis>_r<n> en v4),
    dans l'ordre de préférence des bases"""
    ds = [os.path.dirname(f) for f in glob.glob(os.path.join(raw, '*', '*', 'settings.json'))]
    base = lambda d: d.split(os.sep)[-2]
    return sorted(ds, key=lambda d: (BASE_PREFERENCE.index(base(d)) if base(d) in BASE_PREFERENCE else 99, base(d), _natural(os.path.basename(d))))


def _signature(node):
    return [(a['player'], a['type'], a['amount']) for a in node['sequence']], node['player'], [(a['type'], a['amount']) for a in node['actions']]


def average(runs):
    """Moyenne de répétitions d'un même calcul (mêmes réglages, mêmes tapis) : [(settings, stacks, nodes)] -> nodes.

    Le bruit Monte-Carlo de la référence est aléatoire (docs/reference/TEST_PRECISION_2026-10-14.md) : la moyenne de n
    exports le divise à peu près par √n. Pour chaque nœud et chaque main :
      - weight (poids d'atteinte) : moyenne simple ;
      - played (fréquences) : moyenne pondérée par le poids d'atteinte de chaque répétition (moyenne simple si la main
        n'atteint le nœud dans aucune). L'arbre reste cohérent : poids moyen du nœud × fréquence moyenne = poids moyen du fils ;
      - evs : moyenne simple ; evs_se : erreur type de cette moyenne (écart type entre répétitions / √n), en BB.
    Un nœud absent d'une répétition est moyenné sur celles qui l'ont (`repetitions` du nœud). Des répétitions dont un même
    nœud n'a pas la même séquence ou les mêmes actions ne sont pas le même calcul : ValueError."""
    if len({json.dumps(dict(s, handdata=None), sort_keys=True) for s, _, _ in runs}) > 1 or len({tuple(st) for _, st, _ in runs}) > 1:
        raise ValueError('répétitions de réglages ou de tapis différents')
    out = {}
    for key in sorted(set().union(*[set(nodes) for _, _, nodes in runs])):
        ns = [nodes[key] for _, _, nodes in runs if key in nodes]
        if any(_signature(n) != _signature(ns[0]) for n in ns): raise ValueError(f'{key} : séquence ou actions différentes selon la répétition')
        node = copy.deepcopy(ns[0]); node['repetitions'] = len(ns)
        for h in node['hands']:
            w = np.array([n['hands'][h]['weight'] for n in ns], float)
            p = np.array([n['hands'][h]['played'] for n in ns], float); e = np.array([n['hands'][h]['evs'] for n in ns], float)
            H = node['hands'][h]
            H['weight'] = float(w.mean())
            H['played'] = (w @ p / w.sum() if w.sum() > 0 else p.mean(0)).tolist()
            H['evs'] = e.mean(0).tolist()
            H['evs_se'] = (e.std(0, ddof=1) / np.sqrt(len(ns)) if len(ns) > 1 else np.zeros(e.shape[1])).tolist()
        out[key] = node
    return out
