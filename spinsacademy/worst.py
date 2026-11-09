"""Les 3 pires erreurs de la journée (chantier N2, 09/11/2026), pour l'accueil.

Réponses du jour local du joueur, dans le mode demandé, les plus coûteuses (regret_mbb le plus haut), verdict « erreur » ou
« imprécision » : une réponse acceptée (par la référence ou par les experts) a un regret nul et n'y entre pas. Exclus : coups joués
au temps (pas de choix du joueur), questions de lecture du vilain (sans EV, donc sans coût en BB), test de placement (hors
statistiques). Libellés et coût repris du résultat enregistré (attempts.result), comme le bilan de série.
"""
import json
from . import quiz
from .today import local_day

COUNT = 3


def build(rows, day, tz, count=COUNT):
    """rows : réponses du joueur dans le mode, hors placement (session_id, idx, dataset_version, spot_id, hand, verdict, regret_mbb,
    answered_at, timed_out, result). Renvoie au plus `count` erreurs, la plus coûteuse d'abord"""
    out = []
    for r in rows:
        if not r['answered_at'] or local_day(r['answered_at'], tz) != day: continue
        if r['verdict'] not in ('erreur', 'imprécision') or r.get('timed_out') or not (r['regret_mbb'] or 0) > 0: continue
        sp = quiz.load(r['dataset_version'])[1].get(r['spot_id'])
        if sp is None or (sp.get('field') and sp['field']['type'] in ('identification', 'profil')): continue
        res = json.loads(r['result'] or '{}')
        out.append(dict(session_id=r['session_id'], question_index=r['idx'], spot_id=r['spot_id'], hand=r['hand'],
                        prompt_fr=quiz.prompt(sp, r['hand']), chosen_fr=res.get('chosen_label'), best_fr=res.get('best_label'),
                        verdict=r['verdict'], regret_mbb=r['regret_mbb'], cost_bb=round(r['regret_mbb'] / 1000, 2),
                        cost_fr=res.get('loss_fr') or quiz.gain_bb(r['regret_mbb'] / 1000), answered_at=r['answered_at']))
    out.sort(key=lambda e: (-e['regret_mbb'], e['answered_at']))
    return out[:count]
