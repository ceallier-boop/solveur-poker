"""Lecture des exports HRC (settings.json + nodes/*.json) : empreintes d'arbre, clés de nœuds, étiquettes d'action."""
import glob, hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, 'data', 'hrc', 'raw')
POS3, POS2 = ['BTN', 'SB', 'BB'], ['SB', 'BB']
NC = lambda h: 6 if len(h) == 2 else (4 if h[2] == 's' else 12)
# Ordre de préférence quand plusieurs exports existent pour les mêmes stacks : le plus récent d'abord
BASE_PREFERENCE = ['v2', 'complement2', 'complement', 'min_raise_hu', 'min_raise_3way']


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


def labels(node, st):
    out = []
    for a in node['actions']:
        amt = a['amount'] / 10000
        if a['type'] == 'R':
            out.append('A' if amt >= st[node['player']] - 1e-9 else f'R{amt:g}')
        else:
            out.append(a['type'])
    return out


def key_of(seq, st, names=None):
    names = names or positions(st)
    out = []
    for a in seq:
        amt = a['amount'] / 10000
        t = {'F': 'fold', 'C': 'call', 'X': 'check'}.get(a['type'])
        if a['type'] == 'R':
            t = 'allin' if amt >= st[a['player']] - 1e-9 else f'raise{amt:g}'
        out.append(f"{names[a['player']]}-{t}")
    return '_'.join(out) or 'root'


def load(d):
    """(settings, stacks, {clé: nœud}) pour un dossier d'export"""
    s = json.load(open(os.path.join(d, 'settings.json'))); st = stacks_of(s)
    nodes = {}
    for f in glob.glob(os.path.join(d, 'nodes', '*.json')):
        n = json.load(open(f)); nodes[key_of(n['sequence'], st)] = n
    return s, st, nodes


def exports(raw=RAW):
    """tous les dossiers d'export, dans l'ordre de préférence des bases"""
    ds = glob.glob(os.path.join(raw, '*', 'hand_*'))
    rank = lambda d: (BASE_PREFERENCE.index(d.split(os.sep)[-2]) if d.split(os.sep)[-2] in BASE_PREFERENCE else 99, int(d.rsplit('_', 1)[1]))
    return sorted(ds, key=rank)
