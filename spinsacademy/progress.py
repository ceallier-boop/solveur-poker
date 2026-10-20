"""Statistiques de progression d'un joueur (cahier des charges §9.2 et §9.3).

Entrée : les réponses enregistrées du joueur, chacune avec la session, la date, la version du dataset et le spot.
Sortie : totaux, scores par thème (avec seuil d'échantillon), évolution par série, erreurs récurrentes et point faible.
Règles :
  - un score n'est marqué fiable qu'à partir de MIN_SAMPLE questions : on ne conclut pas sur quelques réponses ;
  - le point faible proposé est le thème fiable au score le plus bas ; sans thème fiable, aucun n'est proposé ;
  - un seul diagnostic « À travailler maintenant » (focus), avec la règle des séries adaptées (spinsacademy.adaptive) :
    thème situation · position · profondeur au taux d'erreur lissé le plus haut parmi ceux qui ont au moins 3 réponses
    et 2 erreurs ; à défaut, la dimension fiable au score le plus bas ; à défaut, le nombre de questions qui manquent ;
  - les statistiques ne modifient jamais les solutions ni la correction.
"""
from collections import defaultdict
from . import quiz

MIN_SAMPLE = 10
DEPTHS = (('lt10', 'Moins de 10 BB', 0, 9.5), ('10_16', '10 à 16 BB', 9.5, 16.5), ('17_25', '17 à 25 BB', 16.5, 99))
FAMILY_FR = {'first_in': 'Premier à parler', 'vs_limp': 'Face à un limp', 'vs_raise': 'Face à une relance', 'vs_allin': 'Face à un tapis',
             'read': 'Lecture du vilain'}
TABLE_FR = {'3-handed': '3 joueurs', 'heads-up': 'Heads-up'}
MODE_FR = {'gto': 'GTO', 'exploit': 'Exploitant', 'field': 'Field'}


def depth_of(stack):
    for key, label, lo, hi in DEPTHS:
        if lo <= stack < hi: return key
    return DEPTHS[-1][0]


def _bucket():
    return dict(questions=0, points=0.0, errors=0)


def _close(b, label, filters):
    n = b['questions']
    return dict(label=label, questions=n, score_pct=round(100 * b['points'] / n, 1) if n else None,
                errors=b['errors'], reliable=n >= MIN_SAMPLE, filters=filters)


def compute(rows):
    """rows : dicts {session_id, session_created_at, dataset_version, spot_id, hand, verdict, points, regret_mbb, answered_at}"""
    total = _bucket(); verdicts = defaultdict(int)
    dims = {'mode': defaultdict(_bucket), 'family': defaultdict(_bucket), 'hero': defaultdict(_bucket), 'table': defaultdict(_bucket), 'depth': defaultdict(_bucket)}
    sessions = defaultdict(lambda: dict(questions=0, points=0.0, date=None))
    themes = defaultdict(lambda: dict(errors=0, imprecisions=0, questions=0, regret=0.0, examples=[]))
    for r in rows:
        _, spots = quiz.load(r['dataset_version']); sp = spots[r['spot_id']]
        fam, hero, table, depth = quiz.family(sp), sp['hero'], sp['table'], depth_of(sp['effective_stack_bb'])
        err = r['verdict'] == 'erreur'; mode = quiz.mode_of(r['dataset_version'])
        for b in (total, dims['mode'][mode], dims['family'][fam], dims['hero'][hero], dims['table'][table], dims['depth'][depth]):
            b['questions'] += 1; b['points'] += r['points']; b['errors'] += err
        verdicts[r['verdict']] += 1
        s = sessions[r['session_id']]; s['questions'] += 1; s['points'] += r['points']; s['date'] = r['session_created_at']
        t = themes[(mode, fam, hero, depth)]; t['questions'] += 1; t['imprecisions'] += r['verdict'] == 'imprécision'
        if err:
            t['errors'] += 1; t['regret'] += r['regret_mbb']
            if len(t['examples']) < 2: t['examples'].append(quiz.prompt(sp, r['hand']))
    depth_label = {k: l for k, l, *_ in DEPTHS}
    depth_filter = {k: dict(min_stack=lo, max_stack=hi) for k, _, lo, hi in DEPTHS}
    by = dict(
        mode=[_close(dims['mode'][k], MODE_FR[k], dict(mode=k)) for k in MODE_FR if k in dims['mode']],
        family=[_close(dims['family'][k], FAMILY_FR[k], dict(family=k)) for k in FAMILY_FR if k in dims['family']],
        hero=[_close(dims['hero'][k], k, dict(hero=k)) for k in ('BTN', 'SB', 'BB') if k in dims['hero']],
        table=[_close(dims['table'][k], TABLE_FR[k], dict(table=k)) for k in TABLE_FR if k in dims['table']],
        depth=[_close(dims['depth'][k], depth_label[k], depth_filter[k]) for k, *_ in DEPTHS if k in dims['depth']])
    reliable = [x for v in by.values() for x in v if x['reliable']]
    weakest = min(reliable, key=lambda x: x['score_pct']) if reliable else None
    recurring = sorted(([dict(label=f"{MODE_FR[m]} · {FAMILY_FR[f]} · {h} · {depth_label[d]}", errors=t['errors'], questions=t['questions'],
                              regret_mbb=round(t['regret']), examples=t['examples'],
                              filters=dict(mode=m, hero=h, **depth_filter[d], **({'family': f} if m != 'exploit' else {})))
                         for (m, f, h, d), t in themes.items() if t['errors'] >= 2]), key=lambda x: (-x['errors'], -x['regret_mbb']))[:3]
    evolution = [dict(session_id=k, date=v['date'], questions=v['questions'], score_pct=round(100 * v['points'] / v['questions'], 1))
                 for k, v in sorted(sessions.items(), key=lambda kv: kv[1]['date'] or '')]
    n = total['questions']
    return dict(sessions=len(sessions), questions=n, points=round(total['points'], 1),
                score_pct=round(100 * total['points'] / n, 1) if n else None,
                verdicts={v: verdicts.get(v, 0) for v in ('correct', 'imprécision', 'erreur')},
                min_sample=MIN_SAMPLE, by=by, evolution=evolution[-20:], recurring_errors=recurring, weakest=weakest,
                focus=focus(themes, weakest, n, depth_label, depth_filter))


def focus(themes, weakest, n, depth_label, depth_filter):
    """un seul diagnostic : dict(kind, label, reason_fr, filters, examples) ; kind = weak | watch | dimension | none"""
    from . import adaptive
    cand = [(adaptive.difficulty(dict(errors=t['errors'], imprecisions=t['imprecisions'], answers=t['questions'])), k, t)
            for k, t in themes.items() if t['questions'] >= adaptive.MIN_ANSWERS and t['errors'] >= adaptive.MIN_ERRORS]
    if cand:
        d, (m, f, h, dp), t = max(cand, key=lambda x: (x[0], x[2]['errors']))
        weak = d >= adaptive.WEAK_RATE
        return dict(kind='weak' if weak else 'watch', label=f"{MODE_FR[m]} · {FAMILY_FR[f]} · {h} · {depth_label[dp]}",
                    reason_fr=(f"{t['errors']} erreurs sur {t['questions']} questions (taux lissé {round(100 * d)} %) : "
                               + ("c'est ton thème le plus fragile, les séries adaptées y reviennent." if weak else "à surveiller, sans être encore un point faible.")),
                    filters=dict(mode=m, hero=h, **depth_filter[dp], **({'family': f} if m != 'exploit' else {})), examples=t['examples'][:1])
    if weakest:
        return dict(kind='dimension', label=weakest['label'], filters=weakest['filters'], examples=[],
                    reason_fr=f"Ton score le plus bas : {str(weakest['score_pct']).replace('.', ',')} % sur {weakest['questions']} questions.")
    need = max(MIN_SAMPLE - n, 0)
    return dict(kind='none', label=None, filters=None, examples=[],
                reason_fr=(f"Pas encore assez de réponses pour un diagnostic : encore {need} question{'s' if need > 1 else ''}." if need
                           else "Rien à retravailler pour l'instant : continue avec des séries recommandées."))
