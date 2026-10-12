"""Reconstruction minimale (fichier d'origine non disponible) : probabilités de chemin dans un arbre HRC exporté."""
import numpy as np
from hrcdata import NAMES, W
def path_probs(nodes, st):
    g = {}
    for i, n in nodes.items():
        w = np.array([n['hands'][x]['weight'] for x in NAMES])
        for j in range(len(n['actions'])):
            p = np.array([n['hands'][x]['played'][j] for x in NAMES])
            g[(i, j)] = float((W * w * p).sum() / W.sum())
    root = [i for i, n in nodes.items() if not n['sequence']][0]
    path = {root: []}; todo = [root]
    while todo:
        i = todo.pop(); n = nodes[i]
        for j, a in enumerate(n['actions']):
            c = a.get('node')
            if c is not None and c in nodes:
                path[c] = path[i] + [(n['player'], g[(i, j)])]; todo.append(c)
    return path, g
