"""Données du conseiller préflop (« Comment jouer ma main ? », page /conseil).

Pour chaque table et chaque jeu de tapis, les situations de l'arbre retenu (quiz.in_main_tree : une seule stratégie par
situation, la même que celle servie par le quiz), avec, pour chacune des 169 mains, la stratégie de référence
(grading.reference_freq : stratégie pure quand l'EV exacte fait foi) et l'EV de référence de chaque action.

Sortie : spinsacademy/web/conseil/index.json (liste des tapis) et un fichier par jeu de tapis, chargé à la demande.
Main : null si elle n'atteint pas la situation (reach < quiz REACH), sinon [atteinte %, fréquences % ..., EV en centièmes de BB ...].
Usage : python tools/web/build_conseil.py [--version 2026.10.13-3]
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import grading, quiz
from spinsacademy.cards import NAMES

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'spinsacademy', 'web', 'conseil')
REACH_MIN = 0.02                                           # test joueurs 7 : les mains qui arrivent rarement restent visibles (note « n'arrive ici que x % »)


def kind(sp, a):
    """famille affichée : fold, check, limp (compléter ou payer 1 BB sans relance avant), call, raise, shove"""
    t = a['type']
    if t == 'allin': return 'shove'
    if t == 'call_allin': return 'call'
    if t in ('limp', 'check', 'fold', 'raise'): return t
    return 'limp' if not any(h['action'] in ('raise', 'allin') for h in sp['history']) else 'call'


def spot_entry(sp):
    acts = [dict(k=kind(sp, a), to=a.get('to_bb')) for a in sp['actions']]
    hands = []
    for h in NAMES:
        x = sp['hands'][h]
        if x.get('reach', 0) < REACH_MIN or not x.get('freq'): hands.append(None); continue
        f = grading.reference_freq(sp, h); ev = grading.reference_ev(sp, h)
        hands.append([round(100 * x['reach'])] + [round(100 * v) for v in f] + [round(100 * (v or 0)) for v in ev])
    tokens = [] if sp['node_key'] == 'root' else sp['node_key'].split('_')        # clé de nœud : une action par élément
    assert len(tokens) == len(sp['history']), sp['spot_id']
    hist = [[t, h['action'], h.get('to_bb')] for t, h in zip(tokens, sp['history'])]
    return dict(hero=sp['hero'], hist=hist, pot=sp['pot_bb'], call=quiz.call_terms(sp)[0] if sp['to_call_bb'] else 0,
                eff=quiz.hero_effective(sp), acts=acts, exact=sp['ev_reference'] == 'exact', poor=bool(sp.get('_poor')), hands=hands)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--version', default=quiz.DEFAULT_VERSION); a = ap.parse_args()
    manifest, spots = quiz.load(a.version)
    configs = {}
    for sp in spots.values():
        if not quiz.in_main_tree(a.version, sp): continue
        key = (sp['table'], tuple(sp['stacks_bb']))
        node = sp['node_key']
        assert node not in configs.setdefault(key, {}), (key, node)
        configs[key][node] = spot_entry(sp)
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.json'): os.remove(os.path.join(OUT, f))
    index = []
    for (table, stacks), nodes in sorted(configs.items(), key=lambda kv: (kv[0][0] != '3-handed', kv[0][1])):
        name = ('3w-' if table == '3-handed' else 'hu-') + '-'.join(f'{s:g}' for s in stacks)
        players = list(quiz.PREFLOP_ORDER[len(stacks)])
        with open(os.path.join(OUT, name + '.json'), 'w') as fh:
            json.dump(dict(table=table, players=players, stacks=list(stacks), spots=nodes), fh, separators=(',', ':'))
        index.append(dict(file=name, table=table, players=players, stacks=list(stacks), spots=len(nodes)))
    with open(os.path.join(OUT, 'index.json'), 'w') as fh:
        json.dump(dict(dataset=f"gto_preflop/{manifest['version']}", hands=NAMES, configs=index), fh, separators=(',', ':'))
    print(f"{len(index)} jeux de tapis, {sum(c['spots'] for c in index)} situations -> {os.path.relpath(OUT)}")


if __name__ == '__main__':
    main()
