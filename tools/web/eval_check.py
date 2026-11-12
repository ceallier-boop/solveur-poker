"""Relais de l'évaluateur indépendant pour les recettes dans le navigateur : lit une question par ligne (JSON : kind, topic, hero_cards,
board, ranges, exact) sur l'entrée, écrit une réponse JSON par ligne : outs (cartes), turn_bp, river_bp, et value_bp si « exact » est vrai
(équité sur les 1 081 suites, environ 8 s). Aucun import de spinsacademy.
Usage : python3 tools/web/eval_check.py   (lancé par e2e_equites_recette.cjs et e2e_ui_categories_recette.cjs)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_independant as EV

for line in sys.stdin:
    q = json.loads(line); hand, board = q['hero_cards'], q['board']; out = {}
    if q['kind'] == 'outs':
        o = EV.outs(hand, board); out = dict(outs=o, turn_bp=round(1e4 * len(o) / 47), river_bp=round(1e4 * EV.improve_by_river(hand, board) / 1081))
    if q.get('exact'):
        rg = q.get('ranges') or []
        out['value_bp'] = EV.equity(hand, board, rg[0]['hands'] if rg else None)
    print(json.dumps(out), flush=True)
