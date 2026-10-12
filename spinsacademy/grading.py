"""Correction d'une réponse et affichage arrondi d'une stratégie.

Barème (cahier des charges §4.2), sur l'EV de référence du spot (exacte ou HRC, voir importer) :
  - regret = EV de la meilleure action - EV de l'action choisie, en mBB ;
  - « correct »   : regret <= TOLERANCE_MBB, ou bien, quand l'EV de référence est celle de HRC, action jouée par HRC
                    au moins MIXED_MIN de la fois (stratégie mixte : on ne la présente pas comme une erreur) ;
  - « imprécision » : regret <= 3 x TOLERANCE_MBB (actions de valeur proche) ;
  - « erreur »    : au-delà.
Points : 1 / 0,5 / 0. Les fréquences affichées sont arrondies (pas de DISPLAY_STEP), la correction utilise les valeurs exactes.
"""
TOLERANCE_MBB = 20.0          # ≈ plancher de bruit de HRC (docs/audit/AUDIT_PHASE0.md §2)
MIXED_MIN = 0.10
DISPLAY_STEP = 5              # en points de pourcentage
POINTS = {'correct': 1.0, 'imprécision': 0.5, 'erreur': 0.0}


def reference_ev(spot, hand):
    h = spot['hands'][hand]
    return h['ev_exact'] if spot['ev_reference'] == 'exact' else h['ev_hrc']


def grade(spot, hand, action_id):
    ids = [a['id'] for a in spot['actions']]
    if action_id not in ids: raise ValueError(f"action {action_id!r} non proposée dans ce spot ({ids})")
    j = ids.index(action_id); ev = reference_ev(spot, hand); freq = spot['hands'][hand]['freq']
    best = max(range(len(ev)), key=lambda k: ev[k])
    regret = 1000 * (ev[best] - ev[j])
    mixed_ok = spot['ev_reference'] == 'hrc' and freq[j] >= MIXED_MIN
    if regret <= TOLERANCE_MBB or mixed_ok: verdict = 'correct'
    elif regret <= 3 * TOLERANCE_MBB: verdict = 'imprécision'
    else: verdict = 'erreur'
    return dict(verdict=verdict, points=POINTS[verdict], regret_mbb=round(regret, 1), best_action=ids[best],
                chosen_frequency=freq[j], ev_source=spot['ev_reference'])


def displayed_mix(spot, hand, step=DISPLAY_STEP):
    """fréquences arrondies au pas `step`, de somme 100 (méthode du plus fort reste) ; actions à 0 omises"""
    freq = spot['hands'][hand]['freq']; units = 100 // step
    raw = [f * units for f in freq]; base = [int(x) for x in raw]
    for k in sorted(range(len(raw)), key=lambda k: raw[k] - base[k], reverse=True)[:units - sum(base)]:
        base[k] += 1
    return [(a['id'], b * step) for a, b in zip(spot['actions'], base) if b > 0]
