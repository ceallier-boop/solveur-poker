"""Correction d'une réponse et affichage arrondi d'une stratégie.

Barème (cahier des charges §4.2), sur l'EV de référence du spot (exacte ou HRC, voir importer) :
  - regret = EV de la meilleure action - EV de l'action choisie, en mBB ;
  - « correct »   : regret <= TOLERANCE_MBB, ou action jouée au moins MIXED_MIN de la fois par la stratégie de référence
                    (EV exacte : la stratégie de référence est pure, l'action la plus rentable)
                    (stratégie mixte : jamais sanctionnée ; l'importeur 1.2.0 ne propose que des mains où ces actions
                    perdent au plus 60 mBB, donc fréquences et EV concordent) ;
  - « imprécision » : regret <= 3 x TOLERANCE_MBB (actions de valeur proche) ;
  - « erreur »    : au-delà ;
  - EV HRC (bruitée : environ 0,1 BB d'un export à l'autre, docs/hrc/TEST_PRECISION_2026-10-14.md) : une action à
    PERTINENT_MBB ou moins de la meilleure est « pertinente » : au pire une imprécision, jamais une erreur.
Points : 1 / 0,5 / 0. Les fréquences affichées ne gardent que les actions jouées au moins MIXED_MIN de la fois, renormalisées et arrondies
(pas de DISPLAY_STEP) ; la correction utilise les valeurs exactes.
"""
TOLERANCE_MBB = 20.0          # ≈ plancher de bruit de HRC (docs/audit/AUDIT_PHASE0.md §2)
MIXED_MIN = 0.10
PERTINENT_MBB = 100.0         # EV HRC : en dessous, l'action reste pertinente (décision du porteur du projet, 2026-10-14)
DISPLAY_STEP = 5              # en points de pourcentage
POINTS = {'correct': 1.0, 'imprécision': 0.5, 'erreur': 0.0}


def reference_ev(spot, hand):
    h = spot['hands'][hand]
    return h['ev_exact'] if spot['ev_reference'] == 'exact' else h['ev_hrc']


def reference_freq(spot, hand):
    """fréquences de la stratégie de référence. EV exacte : stratégie pure, l'action la plus rentable (le calcul exact fait
    foi, les fréquences HRC n'en sont qu'une approximation) ; sinon les fréquences HRC."""
    h = spot['hands'][hand]
    if spot['ev_reference'] == 'exact' and h.get('ev_exact') and None not in h['ev_exact']:
        ev = h['ev_exact']; top = max(range(len(ev)), key=lambda k: ev[k])
        return [1.0 if k == top else 0.0 for k in range(len(ev))]
    return h['freq']


def grade(spot, hand, action_id):
    if not spot['hands'][hand].get('quiz_eligible', True): raise ValueError(f'{hand} n\'est pas proposable dans ce spot (atteinte ou données HRC incohérentes)')
    ids = [a['id'] for a in spot['actions']]
    if action_id not in ids: raise ValueError(f"action {action_id!r} non proposée dans ce spot ({ids})")
    j = ids.index(action_id); ev = reference_ev(spot, hand); freq = reference_freq(spot, hand)
    best = max(range(len(ev)), key=lambda k: ev[k])
    regret = 1000 * (ev[best] - ev[j])
    mixed_ok = freq[j] >= MIXED_MIN
    pertinent = spot['ev_reference'] == 'hrc' and regret <= PERTINENT_MBB
    if regret <= TOLERANCE_MBB or mixed_ok: verdict = 'correct'
    elif regret <= 3 * TOLERANCE_MBB or pertinent: verdict = 'imprécision'
    else: verdict = 'erreur'
    return dict(verdict=verdict, points=POINTS[verdict], regret_mbb=round(regret, 1), best_action=ids[best],
                chosen_frequency=freq[j], mixed=bool(mixed_ok and regret > TOLERANCE_MBB), ev_source=spot['ev_reference'],
                pertinent=bool(pertinent and regret > TOLERANCE_MBB))


def displayed_mix(spot, hand, step=DISPLAY_STEP):
    """fréquences affichées : seules les actions jouées au moins MIXED_MIN de la fois (celles que la correction accepte),
    renormalisées puis arrondies au pas `step`, de somme 100 (méthode du plus fort reste). Ainsi une action affichée
    est toujours acceptée, et une action non affichée n'est jamais présentée comme jouée."""
    freq = reference_freq(spot, hand); units = 100 // step
    kept = [f if f >= MIXED_MIN else 0.0 for f in freq]
    if not any(kept): kept = [1.0 if f == max(freq) else 0.0 for f in freq]
    tot = sum(kept); raw = [f / tot * units for f in kept]; base = [int(x) for x in raw]
    for k in sorted(range(len(raw)), key=lambda k: raw[k] - base[k], reverse=True)[:units - sum(base)]:
        base[k] += 1
    return [(a['id'], b * step) for a, b in zip(spot['actions'], base) if b > 0]
