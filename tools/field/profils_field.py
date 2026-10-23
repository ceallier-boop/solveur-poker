"""Profils adverses v3 : calqués sur les pastilles de Lucho, PA et Lucky (stratégie exploitante v1, §2 et §4).

Convention inchangée par rapport au moteur v2 : un facteur multiplie les COTES de la fréquence GTO de l'action
du vilain (1 = GTO, < 1 = plus serré, > 1 = plus large).
  shove : fréquence d'all-in en premier (BTN, SB)
  call  : fréquence de call d'un all-in
  iso   : fréquence d'iso sur un limp (sert à décider si l'EV du limp HRC est une borne basse)

Le rec passif est le profil PAR DÉFAUT d'un vilain inconnu. Ses facteurs dépendent de la profondeur
(le field paie large à 4 BB, joue la théorie vers 6 BB, est trop serré à partir de 8 BB).
Ce sont des hypothèses de départ tirées des déclarations des coachs : à recaler avec calibrate_profiles.py.
"""
import math

STACKS = (4, 6, 8, 10, 12)

# rec passif : (all-in en premier, call d'un all-in) par stack  — stratégie §2
FIELD_REC = {4: (1.0, 1.5), 6: (0.9, 1.0), 8: (0.8, 0.7), 10: (0.7, 0.65), 12: (0.6, 0.6)}
FIELD_ISO = 0.4          # iso HU d'un limp : 11-16 % au lieu de 25-30 % (Lucky)

DEFAULT = 'Rec passif (défaut)'

# v4.2 : limp_k = facteur sur les cotes de la fréquence de limp du SB (situation « BB face au limp du SB ») : le rec passif et
# la station complètent beaucoup (y compris des mains qu'ils ne poussent pas), le dégène relance ou pousse au lieu de compléter,
# le nit se couche plus souvent
PROFILES = {
    DEFAULT: dict(shove=None, call=None, iso=FIELD_ISO, limp_k=2.0, passif=True, limp=True, shape=True, pastille='serpillère / rec passif',
                  prevalence=0.55),
    'Calling station': dict(shove=0.8, call=1.8, iso=0.5, limp_k=2.0, passif=True, limp=True, shape=True, pastille='calling station', prevalence=0.15),
    'Dégène': dict(shove=2.0, call=1.3, iso=2.0, limp_k=0.6, passif=False, limp=False, pastille='dégène / agressif', prevalence=0.10),
    'Nit': dict(shove=0.5, call=0.5, iso=0.5, limp_k=0.7, passif=True, limp=False, pastille='nit (jackpot)', prevalence=0.05),
    'Reg': dict(shove=1.0, call=1.0, iso=1.0, limp_k=1.0, passif=False, limp=False, pastille='reg', prevalence=0.15),
}

# v4.5 (décision du porteur du projet, compromis Lucho / Lucky) : la range de tapis du récréatif n'est pas le haut de la range
# théorique. Il pousse moins (Lucky : on paie plus serré), mais il complète ou relance une partie de ses grosses mains et garde
# ses As faibles (Lucho) : la moitié de la réduction porte sur ses mains fortes, l'autre sur ses mains faibles (exploit_engine.rec_shape).
REC_TOP = 0.5                                      # part de la réduction de tapis prise sur ses mains fortes
REC_AX = tuple(f'A{r}{s}' for r in '98765432' for s in 'so')

# v4 : paires premium que les coachs divergent à limper entre 5 et 10 BB (R8) : exclues des questions notées
PREMIUM_PAIRS = ('AA', 'KK', 'QQ', 'JJ')

N0 = 20   # pseudo-observations du profil par défaut : à 20 occasions, read observé et défaut pèsent autant (R10)


def _interp_log(table, S, j):
    """interpolation log-linéaire du facteur j entre les stacks de la table ; constant au-delà des bornes"""
    ks = sorted(table)
    if S <= ks[0]:
        return table[ks[0]][j]
    if S >= ks[-1]:
        return table[ks[-1]][j]
    lo = max(k for k in ks if k <= S); hi = min(k for k in ks if k >= S)
    if lo == hi:
        return table[lo][j]
    t = (S - lo) / (hi - lo)
    return math.exp((1 - t) * math.log(table[lo][j]) + t * math.log(table[hi][j]))


# v4 : le limp n'est une réponse que contre un vilain qui PAIE (rec passif, station) : contre un nit qui folde trop, on vole (R3) ;
# contre un dégène on ne limp-fold pas (R6) ; contre un reg on joue la théorie (R11)
def factors(profile, S):
    """facteurs {'shove','call','iso'} du profil à la profondeur S, plus le drapeau 'limp'"""
    p = PROFILES[profile]
    sh = p['shove'] if p['shove'] is not None else _interp_log(FIELD_REC, S, 0)
    ca = p['call'] if p['call'] is not None else _interp_log(FIELD_REC, S, 1)
    return dict(shove=sh, call=ca, iso=p['iso'], limp_k=p['limp_k'], limp=p['limp'], shape=p.get('shape', False))


def posterior(observed, S, n, n0=N0):
    """facteurs effectifs après n occasions observées : moyenne des log-facteurs observé / défaut, pondérée n / n0.
    n = 0 → profil par défaut ; n → ∞ → facteurs observés."""
    prior = factors(DEFAULT, S)
    out = {'limp': bool(observed.get('limp', prior['limp'])) if n >= n0 else prior['limp'],
           'shape': bool(observed.get('shape', prior['shape'])) if n >= n0 else prior['shape']}
    for k in ('shove', 'call', 'iso', 'limp_k'):
        if k not in observed: out[k] = prior[k]; continue
        lo, lp = math.log(observed[k]), math.log(prior[k])
        out[k] = math.exp((n * lo + n0 * lp) / (n + n0))
    return out


def prevalence(profile):
    return PROFILES[profile]['prevalence']


def is_passive(f):
    """un vilain qui iso moins que le GTO ET qui paie : l'EV du limp donnée par HRC est alors une borne basse (v4 : drapeau 'limp')"""
    return f['iso'] <= 1.0 and f.get('limp', True)


# seuils d'adaptation (multiples du bruit du moteur) — R5 : folder un push théorique demande plus de preuve
def threshold(gto_action, expl_action, S):
    if gto_action == 'pousse' and expl_action == 'fold':
        return 3.0
    return 2.0
