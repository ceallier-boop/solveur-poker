import json, glob, os, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# clés des scripts historiques (legacy/conversation) -> dossiers des exports HRC du dépôt (data/hrc/README.md) ;
# EXPRESSO_DATA garde l'ancienne arborescence hrc/x/<clé>/Hand_<n> si elle est définie
RAW = {'3w': 'min_raise_3way', 'hu': 'min_raise_hu', '3wc': 'complement', 'huc': 'complement', 'c2': 'complement2'}
from pushfold import build_classes
combos, nc, NAMES = build_classes()
IDX = {n: i for i, n in enumerate(NAMES)}
W = nc.astype(float)
def load(kind, hand):
    if os.environ.get('EXPRESSO_DATA'):
        d = os.path.join(os.environ['EXPRESSO_DATA'], 'hrc', 'x', kind, f'Hand_{hand}')
    else:
        d = os.path.join(ROOT, 'data', 'hrc', 'raw', RAW[kind], f'hand_{hand}')
    s = json.load(open(d + '/settings.json'))
    nodes = {int(os.path.basename(f)[:-5]): json.load(open(f)) for f in glob.glob(d + '/nodes/*.json')}
    return s, nodes
def stacks_of(s): return [x / 10000 for x in s['handdata']['stacks']]
def key_of(seq, stacks):
    out = []
    for a in seq:
        amt = a['amount'] / 10000
        allin = a['type'] == 'R' and amt >= stacks[a['player']] - 1e-9
        out.append(f"{a['player']}{a['type']}{'A' if allin else (format(amt,'g') if a['type']=='R' else '')}")
    return '-'.join(out)
def index_nodes(s, nodes):
    st = stacks_of(s)
    return {key_of(n['sequence'], st): i for i, n in nodes.items()}
def act_labels(node, st):
    labs = []
    for a in node['actions']:
        amt = a['amount'] / 10000
        if a['type'] == 'R':
            labs.append('A' if amt >= st[node['player']] - 1e-9 else f"R{amt:g}")
        else:
            labs.append(a['type'])
    return labs
def vec(node, ai):
    """frequence de l'action ai par classe (169) + poids d'atteinte"""
    f = np.zeros(169); wt = np.zeros(169)
    for h, v in node['hands'].items():
        i = IDX[h]; f[i] = v['played'][ai]; wt[i] = v['weight']
    return f, wt
def action_vec(node, st, label):
    labs = act_labels(node, st)
    if label not in labs: return np.zeros(169), None
    return vec(node, labs.index(label))
def pct(v, wt=None):
    w = W if wt is None else W * wt
    return 100 * float((v * w).sum() / w.sum())
