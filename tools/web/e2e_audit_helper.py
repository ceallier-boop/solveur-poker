"""Aide de tools/web/e2e_audit_recette.cjs : prépare et contrôle côté serveur ce que le navigateur ne voit pas.

  python tools/web/e2e_audit_helper.py seed <player_id>       historique réel dans la base (SPINSACADEMY_DB) : 4 séries sur
                                                              4 jours, la semaine passée à 15 BB perdus pour 100, celle-ci à 5
  python tools/web/e2e_audit_helper.py depth <level> <spot_id>…  tapis effectif et tranche du niveau de chaque spot servi (JSON)
  python tools/web/e2e_audit_helper.py pick <best|worst> <spot_id> <main>   option la moins (best) ou la plus (worst) coûteuse (JSON)
  python tools/web/e2e_audit_helper.py picks                  la même chose en continu : une demande « best|worst spot main »
                                                              par ligne sur l'entrée, une réponse JSON par ligne (données chargées une fois)
  python tools/web/e2e_audit_helper.py fiche <banque> <spot_id>…   stratégie lue dans la banque (pas dans fiches.json) : part de
                                                              chaque famille d'action par main, en %, et mains jamais atteintes (JSON)
"""
import datetime, json, os, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy import levels, quiz

V = quiz.DEFAULT_VERSION


def seed(player_id):
    spots = [sp for sp in quiz.pool(V) if levels.in_level(1, sp)]
    now = datetime.datetime.now(datetime.timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
    con = sqlite3.connect(os.environ['SPINSACADEMY_DB'])
    for k, (days_ago, regret) in enumerate(((10, 150), (9, 150), (3, 50), (2, 50))):     # 15 puis 5 BB perdus pour 100 décisions
        at = (now - datetime.timedelta(days=days_ago)).isoformat(timespec='seconds'); sid = f'seed-{player_id[:8]}-{k}'
        con.execute('INSERT INTO sessions(id, created_at, dataset_version, filters, seed, size, player_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (sid, at, V, '{}', k, 30, player_id))
        for i in range(30):
            sp = spots[(30 * k + i) % len(spots)]; hand = quiz.teachable(sp)[0]
            con.execute('INSERT INTO questions(session_id, idx, spot_id, hand, served_at) VALUES (?, ?, ?, ?, ?)', (sid, i, sp['spot_id'], hand, at))
            con.execute('INSERT INTO attempts(session_id, idx, action_id, verdict, points, regret_mbb, result, answered_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (sid, i, sp['actions'][0]['id'], 'imprécision', 0.5, regret, '{}', at))
    con.commit(); con.close()
    print(json.dumps({'player_id': player_id, 'sessions': 4, 'decisions': 120}))


def depth(level, spot_ids):
    _, all_spots = quiz.load(V); lo, hi = levels.LEVELS[level]['depth']
    out = [dict(spot_id=s, effective_stack_bb=all_spots[s]['effective_stack_bb'], in_band=lo <= all_spots[s]['effective_stack_bb'] < hi) for s in spot_ids]
    print(json.dumps({'band': [lo, hi], 'spots': out}))


def pick(which, spot_id, hand):
    _, spots = quiz.load(V)
    cost = {a['id']: quiz.correct(V, spot_id, hand, a['id'])['regret_mbb'] for a in spots[spot_id]['actions']}
    best = (min if which == 'best' else max)(cost, key=cost.get)
    return {'action_id': best, 'regret_mbb': cost[best], 'verdict': quiz.correct(V, spot_id, hand, best)['verdict']}


KIND = {'fold': 'fold', 'check': 'check', 'call': 'call', 'call_allin': 'call', 'limp': 'call', 'raise': 'raise', 'allin': 'allin'}


def fiche(bank, spot_ids):
    manifest, spots = quiz.load(bank); minreach = manifest.get('min_reach_for_questions', 0.05); out = {}
    for sid in spot_ids:
        sp = spots[sid]; kinds = [KIND[a['type']] for a in sp['actions']]; hands = {}
        for h, x in sp['hands'].items():
            share = {}
            for k, f in zip(kinds, x['freq']): share[k] = share.get(k, 0) + 100 * f
            hands[h] = dict(dead=x['reach'] < minreach, share={k: round(v, 1) for k, v in share.items()})
        out[sid] = dict(kinds=kinds, hands=hands)
    print(json.dumps(out))


if __name__ == '__main__':
    if sys.argv[1] == 'seed': seed(sys.argv[2])
    elif sys.argv[1] == 'fiche': fiche(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == 'pick': print(json.dumps(pick(*sys.argv[2:5])))
    elif sys.argv[1] == 'picks':
        for line in sys.stdin: print(json.dumps(pick(*line.split())), flush=True)
    else: depth(int(sys.argv[2]), sys.argv[3:])
