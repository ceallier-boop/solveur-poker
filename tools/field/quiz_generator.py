"""Générateur de questions exploitantes v4.2 (stratégie exploitante v1, corrigée après l'audit des coachs de la v4.1).

v4.2 (audit Lucho / PA / Lucky de la banque v4.1, 258 questions : 8 ❌, 10 ⚠️, remarques de pédagogie) :
  1. limp du SB : EV estimée contre le vilain (exploit_engine.limp_ev) au lieu de la borne basse HRC ; les 8 questions
     « inconnu » HU à 8 BB (pousser au lieu de limper contre un rec qui iso peu) disparaissent ;
  2. « quelle pastille ? » : rec passif et reg deviennent deux réponses distinctes (la distinction qui fait l'essentiel
     des gains, selon Lucky) ; question gardée seulement si l'échantillon les sépare (40, 80 ou 150 occasions) ;
  3. pièges : le vilain doit s'écarter du GTO d'au moins 5 points (sinon ce n'est pas un piège) et la décision ne doit
     pas être triviale (marge entre 3 et 10 x le bruit) ;
  4. adaptations et « inconnu » : exclues quand HRC joue déjà la réponse au moins 30 % du temps (déviation faible) ;
  5. à 6 BB, payer moins contre un vilain qui pousse peu (R2) exige 80 occasions (field proche de la théorie vers 5-6 BB) ;
  6. chaque question donne les actions acceptées (EV à moins de 1 x bruit de la meilleure) et la fréquence HRC de la réponse.

Nouveautés par rapport à v2 :
  - profils v3 (rec passif par défaut, facteurs selon la profondeur) ; le Reg sert de contrôle de cohérence ;
  - option LIMP au SB (HU, BvB) contre un vilain passif (R4) ; seules les décisions robustes sont gardées ;
  - seuil asymétrique : folder un push théorique demande 3 x le bruit (R5) ;
  - chaque vilain est observé n fois : la décision utilise le read combiné au défaut (R10) ;
    nouveaux types « inconnu » (n = 0) et « échantillon » (read trop mince pour changer la décision) ;
  - tirage pondéré par la fréquence du profil et du défaut dans le field ;
  - l'explication cite la règle (R1-R10) et sa leçon.
"""
import os, json, csv, random, hashlib, math, collections
import numpy as np
import exploit_engine as ee
import profils_field as pf
from hrcdata import NAMES

OUT_DIR = os.environ.get('EXPRESSO_OUT', ee.DATA_DIR)
# v4.3 : x 10 (4400). Le volume prime sur les proportions (porteur du projet, 21/10) : les parts de référence sont visées
# d'abord, puis une dernière passe complète sans plafond (le rec passif et le vilain inconnu manquent de candidats).
N_TARGET = int(os.environ.get('EXPRESSO_N_QUIZ', 550 if int(os.environ.get('EXPRESSO_SCALE', 10)) == 1 else 800 * int(os.environ.get('EXPRESSO_SCALE', 10))))   # v4.5 : 8000 questions (4 à 25 BB, 12 situations)
SITU_MAX = 0.12          # v4.2 : aucune situation au-delà de 12 % de la banque (les limps du SB l'auraient envahie)
SCALE = int(os.environ.get('EXPRESSO_SCALE', 10))      # v4.3 : banque x 10 (variantes d'échantillon, d'intensité et de plafonds)
N_OBS = (20, 40, 80) if SCALE == 1 else (20, 25, 30, 40, 50, 60, 80, 100, 120, 150)    # occasions observées pour les adaptations
N_THIN = (3, 5) if SCALE == 1 else (3, 4, 5, 6)                     # read trop mince (type « échantillon »)
LAMS = (1.0, 0.5) if SCALE == 1 else (1.0, 0.85, 0.7, 0.5)               # intensité du profil (facteur ** intensité)

SIT = {
 ('3w', "BB face à l'all-in du SB (BTN fold)"): "3 joueurs, {S} BB chacun. Le BTN fold et le SB pousse all-in. Tu es au BB.",
 ('3w', "BB face à l'all-in du BTN (SB fold)"): "3 joueurs, {S} BB chacun. Le BTN pousse all-in et le SB fold. Tu es au BB.",
 ('3w', "SB face à l'all-in du BTN"):           "3 joueurs, {S} BB chacun. Le BTN pousse all-in. Tu es au SB (le BB est derrière).",
 ('3w', "SB pousse (BTN fold) face au BB"):      "3 joueurs, {S} BB chacun. Le BTN fold. Tu es au SB, le BB est derrière.",
 ('3w', "BTN pousse face au SB et au BB"):       "3 joueurs, {S} BB chacun. Tu es au BTN, le SB et le BB sont derrière.",
 ('hu', "BB face à l'all-in du SB"):             "Heads-up, {S} BB chacun. Le SB pousse all-in. Tu es au BB.",
 ('hu', "SB pousse face au BB"):                 "Heads-up, {S} BB chacun. Tu es au SB (bouton), le BB est derrière.",
 ('hu', "BB face au limp du SB"):                "Heads-up, {S} BB chacun. Le SB complète. Tu es au BB.",
 ('3w', "BB face au limp du SB (BTN fold)"):     "3 joueurs, {S} BB chacun. Le BTN fold et le SB complète. Tu es au BB.",
 ('3w', "BB face au limp du BTN (SB fold)"):     "3 joueurs, {S} BB chacun. Le BTN complète et le SB se couche. Tu es au BB.",
 ('hu', "SB face au tapis du BB après son limp"): "Heads-up, {S} BB chacun. Tu complètes au SB et le BB part à tapis.",
 ('3w', "BB face à l'open du BTN (SB fold)"):    "3 joueurs, {S} BB chacun. Le BTN relance à 2,3 BB et le SB se couche. Tu es au BB.",
}
LEAKS = {('iso', +1): "complète trop souvent", ('iso', -1): "ne complète pas assez",
         ('call', +1): "pousse trop souvent", ('call', -1): "ne pousse pas assez",
         ('shove', +1): "paie trop souvent", ('shove', -1): "ne paie pas assez",
         ('iso_call', +1): "paie souvent ton tapis", ('iso_call', -1): "se couche souvent face au tapis",
         ('vsopen', +1): "ouvre trop souvent", ('vsopen', -1): "n'ouvre pas assez",
         ('defend', +1): "défend trop face à ta relance", ('defend', -1): "se couche trop face à ta relance"}
MIN_LIMPS = 10            # v4.3 (PA, Lucho) : sa stat de call après limp ne se lit qu'à partir de 10 limps observés
MIN_MARGIN = 0.05         # v4.3 : en dessous de 0,05 BB d'écart, les deux options se valent : pas de question notée


Z_MIN = 1.5               # v4.4 (audit Lucky, Lucho, PA) : un read ne compte que si l'écart affiché dépasse 1,5 écart-type


def zscore(k, n, p0_pct):
    """écart de k / n à la fréquence théorique, en écarts-types (loi binomiale)"""
    if not n: return 0.0
    p0 = min(max(p0_pct / 100, 0.01), 0.99)
    return abs(k / n - p0) / math.sqrt(p0 * (1 - p0) / n)


def shown_z(spec, robs, n):
    """significativité des stats affichées : (z de la fréquence principale, z du call après limp ou du call du BB)"""
    k = round(n * robs['vill_freq'] / 100); z1 = zscore(k, n, robs['vill_freq_gto']); z2 = 0.0
    if spec['type'] == 'iso' and k >= MIN_LIMPS and robs.get('has_jam', True):
        z2 = zscore(round(k * robs['call_after_pct'] / 100), k, robs['call_after_pct_gto'])
    elif robs.get('vill_freq2') is not None:
        n2 = n - k; z2 = zscore(round(n2 * robs['vill_freq2'] / 100), n2, robs['vill_freq2_gto'])
    return z1, z2


def shown(spec, robs, n):
    """écarts au GTO tels qu'AFFICHÉS (k / n), en points : (fréquence principale, call après limp, limps observés)"""
    k = round(n * robs['vill_freq'] / 100); dfreq = 100 * k / n - robs['vill_freq_gto']
    if spec['type'] != 'iso': return dfreq, 0.0, k
    dcall = (100 * round(k * robs['call_after_pct'] / 100) / k - robs['call_after_pct_gto']) if k >= MIN_LIMPS and robs.get('has_jam', True) else 0.0
    return dfreq, dcall, k


def iso_read(e, dfreq, dcall, z=(Z_MIN, Z_MIN)):
    """face au limp : la règle et le défaut qui justifient la réponse, d'après les stats affichées (None si aucune).
    v4.4 : la stat citée doit être significative ; R12 n'est pas citée quand il paie aussi plus que la théorie (calling station)"""
    c = ([('R12', dfreq, LEAKS[('iso', +1)], z[0]), ('R13', -dcall, LEAKS[('iso_call', -1)], z[1])] if e in ('pousse', 'relance')
         else [('R15', -dfreq, LEAKS[('iso', -1)], z[0]), ('R14', dcall, LEAKS[('iso_call', +1)], z[1])])
    c = [x[:3] for x in c if x[1] >= 5 and x[3] >= Z_MIN and not (x[0] == 'R12' and dcall >= 5)]
    return max(c, key=lambda x: x[1])[::2] if c else None


def stat_kind(spec, r):
    """famille de la stat principale affichée : call d'un tapis, défense face à une relance (arbres sans tapis), open, limp"""
    if spec['type'] == 'shove' and r.get('stat_kind') == 'defend': return 'defend'
    return spec['type']


def shown_leak(spec, dfreq, dcall, r=None):
    """le défaut que montrent les stats affichées (le plus grand écart)"""
    if spec['type'] == 'iso' and abs(dcall) > abs(dfreq): return LEAKS[('iso_call', 1 if dcall > 0 else -1)]
    return LEAKS[(stat_kind(spec, r or {}), 1 if dfreq > 0 else -1)]
LEAK_OPTIONS = ["Il pousse trop souvent", "Il ne pousse pas assez", "Il paie trop souvent", "Il ne paie pas assez"]
LEAK_ANS = {('call', +1): 0, ('call', -1): 1, ('shove', +1): 2, ('shove', -1): 3}
LABEL = {'paie': 'Payer', 'pousse': 'Pousser all-in', 'limpe': 'Limp', 'fold': 'Fold', 'checke': 'Check', 'relance': 'Relancer'}
ACT_ORDER = ('pousse', 'relance', 'paie', 'limpe', 'checke', 'fold')

RULES = {
 'R0': "Inconnu = rec passif : il paie et relance peu. Vole plus, paie plus serré (sauf à 4 BB ou moins).",
 'R1': "Il pousse trop : paie plus large.",
 'R2': "Il pousse peu : son tapis est fort, paie plus serré.",
 'R3': "Il paie peu : pousse plus large, même avec des mains faibles.",
 'R4': "Au SB, contre un joueur qui paie trop, complète les mains trop faibles pour pousser ou relancer.",
 'R5': "Ne folde une main à pousser que si le read est solide et le gain net.",
 'R6': "Contre un joueur qui relance ou paie tout, folde le bas de ta range.",
 'R7': "Au BTN à 3 joueurs, jamais de limp : fold ou tapis.",
 'R9': "Un écart de stats qui ne change pas la décision ne change rien.",
 'R10': "Trop peu de coups pour conclure : joue le profil par défaut.",
 'R11': "Ses stats collent à la théorie : joue la théorie.",
 'R12': "Il complète beaucoup : son limp est faible, pousse plus large.",
 'R13': "Il se couche souvent face au tapis : pousse plus large.",
 'R14': "Il paie souvent ton tapis : garde le tapis pour tes bonnes mains, checke les autres.",
 'R15': "Il complète peu : son limp est fort, checke tes mains moyennes.",
 'R16': "Il paie trop ton tapis : garde-le pour les mains qui battent ses calls, folde les autres.",
 'R17': "Il ouvre trop : défends plus large, à tapis ou en payant.",
 'R18': "Il ouvre peu : son open est fort, défends plus serré.",
 'R19': "Il se couche trop face à une relance : vole avec une petite relance, pas besoin du tapis.",
 'R20': "Il défend beaucoup face à une relance : relance tes bonnes mains, complète ou folde les autres.",
}
# poids de réalisme du défaut à cette profondeur (stratégie §1, point 4)
def realism(leak, S):
    if leak == 'ne pousse pas assez': return 1.0 if S >= 6 else 0.6
    if leak == 'pousse trop souvent': return 0.5
    if leak == 'ne paie pas assez': return 1.0 if S >= 6 else 0.25
    if leak == 'paie trop souvent': return 1.0 if S <= 4 else 0.5
    return 1.0


def hand_txt(h):
    if len(h) == 2: return f"{h} (paire)"
    return f"{h[:2]} {'assortis' if h[2] == 's' else 'dépareillés'}"


def stat_line(spec, r, n):
    """statistique observée affichée en « k sur n » ; le pourcentage est celui de l'échantillon (k / n)"""
    k = round(n * r['vill_freq'] / 100); pct = 100 * k / n
    if spec['type'] == 'iso':
        k2 = round(k * r['call_after_pct'] / 100)               # les calls se comptent sur ses limps, pas sur les occasions
        head = f"Sur {n} occasions, ce vilain a complété {k} fois ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)"
        if k < MIN_LIMPS or not r.get('has_jam', True): return head + "."
        return head + f" et, face à un tapis après son limp, il a payé {k2} fois sur {k} ({100 * k2 / k:.0f} % ; GTO : {r['call_after_pct_gto']:.0f} %)."
    if spec['type'] == 'call':
        return f"Sur {n} occasions dans cette situation, ce vilain a poussé {k} fois ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."
    if spec['type'] == 'vsopen':
        return f"Sur {n} occasions, ce vilain a relancé {k} fois au BTN ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."
    if r.get('stat_kind') == 'defend':
        return f"Sur {n} occasions, ce vilain a défendu {k} fois face à une relance ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."
    if r.get('vill_freq2') is not None:
        n2 = n - k; pct2 = 100 * round(n2 * r['vill_freq2'] / 100) / n2 if n2 else 0.0   # v4.4 : sur les folds du SB
        return (f"Sur {n} occasions, ce vilain a payé {pct:.0f} % des all-in au SB (GTO : {r['vill_freq_gto']:.0f} %) "
                f"et {pct2:.0f} % au BB quand le SB fold (GTO : {r['vill_freq2_gto']:.0f} %).")
    return f"Sur {n} occasions, ce vilain a payé {k} all-in ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."



def stats_struct(spec, r, n):
    """statistiques observées sous forme structurée (export application) : k sur n, % observé, % GTO"""
    if n == 0: return []
    k = round(n * r['vill_freq'] / 100)
    if spec['type'] == 'iso':                                     # v4.2 : limp du SB, puis call de ton tapis après son limp
        k2 = round(k * r['call_after_pct'] / 100)
        out = [dict(stat='limp_pct', n=n, k=k, observed_pct=round(100 * k / n, 1), gto_pct=round(r['vill_freq_gto'], 1))]
        if k >= MIN_LIMPS and r.get('has_jam', True): out.append(dict(stat='call_after_limp_pct', n=k, k=k2, observed_pct=round(100 * k2 / k, 1), gto_pct=round(r['call_after_pct_gto'], 1)))   # v4.4 : rien sous 10 limps
        return out
    st = ('jam_over_limp_pct' if spec.get('hero_range') else 'shove_pct' if spec['type'] == 'call' else 'open_pct' if spec['type'] == 'vsopen'
          else 'defend_pct' if r.get('stat_kind') == 'defend' else 'call_pct')
    out = [dict(stat=st, n=n, k=k, observed_pct=round(100 * k / n, 1), gto_pct=round(r['vill_freq_gto'], 1))]
    if r.get('vill_freq2') is not None:      # v4.4 (audit, bloquant) : les calls du BB se comptent sur les folds du SB
        n2 = n - k; k2 = round(n2 * r['vill_freq2'] / 100)
        if n2: out.append(dict(stat='call_pct_bb_sb_fold', n=n2, k=k2, observed_pct=round(100 * k2 / n2, 1), gto_pct=round(r['vill_freq2_gto'], 1)))
    return out


INF = {"complète trop souvent": "compléter trop souvent", "ne complète pas assez": "ne pas compléter assez",
       "pousse trop souvent": "pousser trop souvent", "ne pousse pas assez": "ne pas pousser assez",
       "paie trop souvent": "payer trop souvent", "ne paie pas assez": "ne pas payer assez",
       "paie souvent ton tapis": "payer souvent ton tapis", "se couche souvent face au tapis": "se coucher souvent face au tapis"}


def rule_for(spec, gto, ex, pname, hero_btn, r=None):
    if spec['type'] == 'vsopen': return 'R17' if ex in ('paie', 'pousse') else 'R18'
    if spec['type'] == 'call':
        return 'R1' if ex == 'paie' else 'R2'
    if gto == 'relance' and ex in ('limpe', 'fold'): return 'R20'      # il défend trop : on ne relance plus ces mains
    if ex == 'limpe': return 'R4'
    if ex == 'relance': return 'R19'
    if ex == 'pousse': return 'R3'
    if hero_btn: return 'R7'
    return 'R6' if not pf.PROFILES[pname]['passif'] else 'R5'


def acts_of(spec, r):
    """actions évaluées par le moteur pour cette situation (v4.5 : liste fournie par le moteur, dont la relance)"""
    if r.get('acts'): return [a for a in ACT_ORDER if a in r['acts']]
    if spec['type'] == 'iso': return ['pousse', 'checke']
    if spec['type'] == 'call': return ['paie', 'fold']
    return ['pousse', 'limpe', 'fold'] if r.get('ev_limp') is not None else ['pousse', 'fold']


def options_for(spec, r):
    return [LABEL[a] for a in acts_of(spec, r)]


def ev_of(r, i, action):
    if r.get('evs') and action in r['evs']: return float(r['evs'][action][i])
    if action == 'fold': return 0.0
    if action == 'limpe': return float(r['ev_limp'][i])
    if action == 'checke': return float(r['ev_check'][i])
    return float(r['ev_raw'][i])


def margin(spec, r, i):
    """écart d'EV entre l'action choisie et la meilleure autre action disponible (pièges : la décision est nette)"""
    acts = acts_of(spec, r); ch = r['expl'][i]
    return ev_of(r, i, ch) - max(ev_of(r, i, a) for a in acts if a != ch)


def explain(kind_q, leak, ans, gto_ans, gain, noise, r, i, rule, n, spec, pname=''):
    evs = "EV par rapport au fold : " + ', '.join(f"{LABEL[a].lower()} {1000 * ev_of(r, i, a):+.0f} mBB" for a in acts_of(spec, r) if a != 'fold')
    if r.get('ev_limp') is not None:
        evs += (" (limp : estimation, contre un BB qui relance ton limp moins que la théorie)" if spec.get('limp_estimate')
                else " (limp : borne basse, EV HRC contre un BB qui jouerait la théorie)")
    lesson = RULES[rule]
    if kind_q == 'adaptation':
        return (f"Le vilain {leak} ({n} occasions). Contre lui, {ans.lower()} bat l'action GTO ({gto_ans.lower()}) de {gain:.0f} mBB, "
                f"au-delà du bruit du moteur ({noise} mBB). {evs}. Règle {rule} : {lesson}")
    if kind_q == 'inconnu':
        return (f"Sans read, le vilain est un rec passif. Contre lui, {ans.lower()} bat l'action GTO ({gto_ans.lower()}) de {gain:.0f} mBB. "
                f"{evs}. Règle R0 : {RULES['R0']}")
    if kind_q == 'échantillon':
        return (f"Il semble {INF.get(leak, leak)}, mais sur {n} coups seulement : c'est trop peu pour changer la décision. "
                f"Règle R10 : {RULES['R10']}")
    if rule == 'R11':
        return f"Piège : ce vilain est un reg, donc la théorie s'applique et {ans.lower()} reste la meilleure action. {evs}. Règle R11 : {RULES['R11']}"
    who = 'un rec passif' if n == 0 else 'ce vilain'
    return f"Piège : même contre {who}, {ans.lower()} reste la meilleure action. {evs}. Règle R9 : {RULES['R9']}"


PROFIL_OPTIONS = ['Rec passif', 'Reg', 'Calling station', 'Dégène', 'Nit']      # v4.2 : rec passif et reg séparés
PROFIL_KEY = {'Rec passif': pf.DEFAULT, 'Reg': 'Reg', 'Calling station': 'Calling station', 'Dégène': 'Dégène', 'Nit': 'Nit'}
GROUP = {lab: (key,) for lab, key in PROFIL_KEY.items()}
PROFIL_N = (40, 80, 150) if SCALE == 1 else (40, 60, 80, 100, 150, 200)
REG_PER_CELL = 6 * SCALE
QUOTA_RELAX = 1.0         # v4.2 : aucun profil au-delà de sa part dans le field (2 x en v4.1) ; le rec passif prend les places libres
INCONNU_MAX = 30 * SCALE          # v4.2 : « inconnu » par (stack, réponse) (22 en v4.1)
MIX_MAX = 0.30            # v4.2 : HRC joue déjà la réponse 30 % du temps ou plus → pas une vraie déviation
TRAP_MIN_GAP = 5.0        # v4.2 : un piège montre un vilain écarté d'au moins 5 points du GTO
TRAP_MAX_MARGIN = 10.0    # v4.2 : au-delà de 10 x le bruit, la décision est triviale
HRC_LABEL = {'paie': 'C', 'pousse': 'A', 'limpe': 'C', 'fold': 'F', 'checke': 'X', 'relance': 'R'}


def gto_freq(kind, S, spec, i, action):
    """fréquence HRC (0-1) de l'action du héros pour la main i"""
    n = ee.node(kind, S, spec['hero']) if spec.get('hero') else None
    if n is None: return 0.0
    labs, F, _ = n; lab = HRC_LABEL[action]
    if lab == 'R': lab = ee.raise_label(labs)
    return float(F[i, labs.index(lab)]) if lab in labs else 0.0


def shown_gap(spec, r, robs, n):
    """écart du vilain au GTO tel qu'affiché (k / n), en points ; sans observation : écart du profil par défaut"""
    if n == 0: return r['vill_freq'] - r['vill_freq_gto']
    return 100 * round(n * robs['vill_freq'] / 100) / n - robs['vill_freq_gto']


def acceptables(spec, r, i, noise):
    """actions dont l'EV est à moins de 1 x bruit de la meilleure (affichées comme acceptées)"""
    acts = acts_of(spec, r)
    best = max(ev_of(r, i, a) for a in acts)
    return [LABEL[a] for a in acts if a != r['expl'][i] and best - ev_of(r, i, a) < noise]


def _freqs(S, fac):
    """fréquences du vilain (all-in en premier au SB ; call d'un all-in au BB) en heads-up pour des facteurs donnés"""
    out = []
    for (kind, name) in (('hu', "BB face à l'all-in du SB"), ('hu', 'SB pousse face au BB'), ('hu', 'BB face au limp du SB')):
        r = ee.run_spot(kind, S, name, ee.SPOTS[(kind, name)], profiles={'x': fac})
        out.append((r['x']['vill_freq'], r['x']['vill_freq_gto']) if r else None)
    return out


def profile_questions(rnd):
    """v4 : « quelle pastille ? » — deux statistiques observées (all-in en premier, call d'un all-in) → pastille. Le rec passif et le reg ne se
    distinguent pas sur 40 à 80 occasions : ils forment une seule réponse. Une question n'est gardée que si la bonne pastille est plus proche
    (chi²) d'au moins 4 que toute autre, c'est-à-dire si l'échantillon permet de trancher."""
    out = []; ee.INTENSITE = 1.0
    for S in (4, 6, 8, 10, 12):
        exp = {}
        for pn in pf.PROFILES:
            exp[pn] = _freqs(S, pf.factors(pn, S))
        gto = exp['Reg']
        for lab in PROFIL_OPTIONS:
            for member in GROUP[lab]:
                for n in PROFIL_N:
                    J = (0, 1, 2) if exp[member][2] and gto[2][0] >= 5 else (0, 1)     # v4.4 (PA, Lucho) : le limp sépare le rec passif du nit
                    k = {j: round(n * exp[member][j][0] / 100) for j in J}
                    obs = {j: 100 * kk / n for j, kk in k.items()}
                    chi = {}
                    for l2 in PROFIL_OPTIONS:
                        best = 1e9
                        for m2 in GROUP[l2]:
                            c = 0.0
                            for j in J:
                                p = min(max(exp[m2][j][0] / 100, 0.01), 0.99)
                                c += (obs[j] / 100 - p) ** 2 / (p * (1 - p) / n)
                            best = min(best, c)
                        chi[l2] = best
                    order = sorted(chi, key=chi.get)
                    if order[0] != lab or chi[order[1]] - chi[order[0]] < 4.0:
                        continue
                    if SCALE == 1 and n == 150 and any(q0['profil'] == member and q0['stack'] == S for q0 in out):
                        continue                                  # 150 occasions : seulement si 40 et 80 ne suffisent pas
                    q = dict(id=f"pf-{S}-" + hashlib.md5(f'profil|{member}|{S}|{n}'.encode()).hexdigest()[:6], type='profil', kind='hu', stack=S,
                             situation='Heads-up : lecture du vilain', hero_hand='',
                             enonce=(f"Heads-up, {S} BB chacun. Sur {n} occasions, ce vilain a poussé all-in {k[0]} fois quand il était au SB ({obs[0]:.0f} % ; GTO : {gto[0][0]:.0f} %)"
                                     + (f", a complété {k[2]} fois au SB ({obs[2]:.0f} % ; GTO : {gto[2][0]:.0f} %)" if 2 in k else '')
                                     + f" et a payé {k[1]} all-in sur {n} ({obs[1]:.0f} % ; GTO : {gto[1][0]:.0f} %). Quelle pastille lui donnes-tu ?"),
                             stats=[dict(stat='shove_pct', n=n, k=k[0], observed_pct=round(obs[0], 1), gto_pct=round(gto[0][0], 1)), dict(stat='call_pct', n=n, k=k[1], observed_pct=round(obs[1], 1), gto_pct=round(gto[1][0], 1))]
                                   + ([dict(stat='limp_pct', n=n, k=k[2], observed_pct=round(obs[2], 1), gto_pct=round(gto[2][0], 1))] if 2 in k else []),
                             options=PROFIL_OPTIONS, bonne_reponse=lab, action_GTO='', gain_mBB=0, seuil_bruit_mBB=0, leak='', intensite=1.0,
                             observations=n, profil=member, regle='R10',
                             explication=(f"Il pousse {'plus que la théorie' if obs[0] > gto[0][0] + 2 else 'moins que la théorie' if obs[0] < gto[0][0] - 2 else 'comme la théorie'} et paie "
                                          f"{'plus' if obs[1] > gto[1][0] + 2 else 'moins' if obs[1] < gto[1][0] - 2 else 'comme elle'} : à {S} BB, ces deux fréquences sont plus proches du profil « {lab.lower()} » "
                                          f"que de toute autre pastille, et {n} occasions suffisent pour trancher. "
                                          + ("Le reg colle à la théorie ; le rec passif pousse et paie moins, mais complète beaucoup : c'est la distinction qui rapporte le plus. " if lab in ('Rec passif', 'Reg')
                                             else "Le nit pousse, paie et complète peu : il se couche beaucoup. " if lab == 'Nit' else '')
                                          + f"Règle R10 : {RULES['R10']}"),
                             difficulte='moyen', niveau_donnees='profil du moteur (hypothèse de coachs, non mesuré)', poids=pf.prevalence(member))
                    out.append(q)
    return out


# v4.3 : banque x 10 en gardant les proportions de la banque 2026.10.20-4 (440 questions) : par type, par profil et par situation
REF_N = 440
REF_SHARES = {
    'type': {'adaptation': 160, 'piège': 141, 'inconnu': 83, 'identification': 27, 'profil': 16, 'échantillon': 13},
    'profil': {'Rec passif (défaut)': 258, 'Calling station': 53, 'Reg': 52, 'Dégène': 49, 'Nit': 28},
    # v4.5 : parts par situation (en % x 4,4), nouvelles situations comprises, au plus près de leur fréquence en jeu
    'situation': {'BTN pousse face au SB et au BB': 61.6, 'SB pousse face au BB': 61.6, 'SB pousse (BTN fold) face au BB': 48.4, "BB face à l'open du BTN (SB fold)": 44.0, 'BB face au limp du SB': 39.6, 'SB face au tapis du BB après son limp': 35.2, "BB face à l'all-in du SB (BTN fold)": 30.8, "BB face à l'all-in du SB": 30.8, 'BB face au limp du SB (BTN fold)': 30.8, "SB face à l'all-in du BTN": 22.0, "BB face à l'all-in du BTN (SB fold)": 22.0, 'BB face au limp du BTN (SB fold)': 4.4, 'Heads-up : lecture du vilain': 8.8},
}


def shared_targets(dim, avail, N):
    """part de chaque type (ou profil) ; celui qui manque de candidats (vilain inconnu : une question par main et par
    situation) est pris en entier, et son manque se répartit sur les autres au prorata de leur part"""
    sh = {t: v / REF_N for t, v in REF_SHARES[dim].items()}; tgt = {}; free = dict(sh)
    while True:
        rest = N - sum(tgt.values()); tot = sum(free.values())
        short = {t for t in free if avail[t] < rest * free[t] / tot}
        if not short: break
        for t in short: tgt[t] = avail[t]; free.pop(t)
    tgt.update({t: rest * v / tot for t, v in free.items()})
    return tgt


def select_targets(pool, rnd):
    """sélection sur objectifs : chaque type, profil et situation vise sa part de la banque de référence ; un type ou un
    profil qui manque de candidats est pris en entier, les autres complètent au prorata"""
    avail = {d: collections.Counter(q[d] for q in pool) for d in ('type', 'profil')}
    dims = lambda q: (('type', q['type']), ('profil', q['profil']), ('situation', q['situation']))
    keyed = sorted(pool, key=lambda q: -math.log(rnd.random() + 1e-12) / max(q['poids'], 1e-6))
    N = N_TARGET
    tgt = {d: {k: v * N / REF_N for k, v in m.items()} for d, m in REF_SHARES.items()}
    tgt.update({d: shared_targets(d, avail[d], N) for d in ('type', 'profil')})
    used = collections.Counter(); out = []; taken = set()
    for slack in ({'type': 1.0, 'profil': 1.0, 'situation': 1.0}, {'type': 1.0, 'profil': 1.03, 'situation': 1.05},
                  {'type': 1.0, 'profil': 1.06, 'situation': 1.10}, None):   # v4.3 : le volume prime, la dernière passe complète sans plafond
        for q in keyed:
            if len(out) >= N: break
            if q['id'] in taken: continue
            if slack is None:
                out.append(q); taken.add(q['id']); continue
            lim = dict(slack, situation=min(slack['situation'], 1.05)) if 'limp du SB' in q['situation'] else slack
            if any(used[(d, k)] >= lim[d] * tgt[d].get(k, 0) for d, k in dims(q)): continue
            out.append(q); taken.add(q['id'])
            for dk in dims(q): used[dk] += 1
    return out


def select_quotas(pool, rnd):
    # quotas par profil proportionnels à sa fréquence dans le field ; tirage pondéré (Efraimidis-Spirakis) par le réalisme du défaut ;
    # pièges + échantillons au plus 40 % ; les questions « profil » comptent pour leur profil
    prev = {p: pf.prevalence(p) for p in pf.PROFILES}; tot = sum(prev.values())
    quota = {p: round(N_TARGET * v / tot) for p, v in prev.items()}
    keyed = sorted(pool, key=lambda q: -math.log(rnd.random() + 1e-12) / max(q['poids'], 1e-6))
    out, n_trap, used, taken = [], 0, {p: 0 for p in pf.PROFILES}, set()
    inc = collections.Counter(); n_situ = collections.Counter()
    for strict in (True, False):
        for q in keyed:
            if len(out) >= N_TARGET: break
            cap = quota[q['profil']] if strict else round(QUOTA_RELAX * quota[q['profil']]) + (N_TARGET if q['profil'] == pf.DEFAULT else 0)   # v4.2 : profils à leur part ; le rec passif complète
            if q['id'] in taken or used[q['profil']] >= cap: continue
            if q['type'] != 'profil' and n_situ[(q['kind'], q['situation'])] >= SITU_MAX * N_TARGET: continue
            if q['type'] == 'inconnu':      # v4.1 : pas plus de 22 « inconnu » par (stack, réponse) : évite 57 « Pousser » à 8 BB
                kk = (q['stack'], q['bonne_reponse'])
                if inc[kk] >= INCONNU_MAX: continue
                inc[kk] += 1
            if q['type'] in ('piège', 'échantillon'):
                if n_trap >= 0.35 * N_TARGET: continue
                n_trap += 1
            out.append(q); taken.add(q['id']); used[q['profil']] += 1; n_situ[(q['kind'], q['situation'])] += 1
    # v4.1 : part des pièges + échantillons ramenée à 35 % de la banque finale (la banque finale peut être plus petite que N_TARGET)
    non = [q for q in out if q['type'] not in ('piège', 'échantillon')]
    allow = int(0.35 / 0.65 * len(non)); kept = 0; o2 = []
    for q in out:
        if q['type'] in ('piège', 'échantillon'):
            if kept >= allow: continue
            kept += 1
        o2.append(q)
    out = o2
    return out


def make(seed=11, per_cell=30 * SCALE):
    rnd = random.Random(seed); cands = []
    advers = [p for p in pf.PROFILES if p != 'Reg']
    for lam in LAMS:
        ee.INTENSITE = lam
        for (kind, name), spec in ee.SPOTS.items():
            hero_btn = name.startswith('BTN')
            for S in spec.get('stacks', ee.STACKS):
                noise = ee.NOISE_BB[S]
                full = ee.run_spot(kind, S, name, spec, profiles={p: pf.factors(p, S) for p in pf.PROFILES})
                if full is None: continue
                if spec['type'] == 'iso' and full['Reg']['vill_freq_gto'] < 5: continue     # le SB ne complète presque jamais à cette profondeur
                reg = full['Reg']
                incoherent = reg['valid'] & (reg['gto'] != reg['expl'])        # la décision change même contre le GTO : base HRC incohérente
                # R8 : limp-trap des paires premium = désaccord des coachs, exclu des questions notées
                prem = np.array([NAMES[i] in pf.PREMIUM_PAIRS for i in range(169)]) & (spec.get('formula') == 'hu_sb') & (S >= 6)
                # --- R11 : vilain identifié reg → théorie ; on ne garde que les décisions nettes
                if lam == 1.0:
                    for n in (40, 80):
                        r = reg
                        ok = r['valid'] & ~incoherent & ~prem & (r['gto'] == r['expl'])
                        idx = [i for i in np.where(ok)[0] if max(3 * noise, MIN_MARGIN) <= margin(spec, r, i) <= TRAP_MAX_MARGIN * noise]
                        for i in rnd.sample(idx, min(REG_PER_CELL, len(idx))):      # v4.1 : 4 par cellule ; v4.2 : 6 (le reg pesait 9 % pour 15 % du field)
                            cands.append(build_q('piège', 'Reg', n, lam, kind, name, spec, S, noise, r, r, i, 'R11', '', 0.0))
                for pname in advers:
                    fobs = pf.factors(pname, S)
                    ns = (0,) + N_OBS if pname == pf.DEFAULT else N_OBS + N_THIN      # v4.2 : le rec passif observé (il pousse et paie moins) a aussi ses questions
                    effs = {n: (pf.posterior(fobs, S, n) if n else pf.factors(pf.DEFAULT, S)) for n in ns}
                    res = ee.run_spot(kind, S, name, spec, profiles={n: f for n, f in effs.items()})
                    robs = full[pname]
                    sgn = 1 if robs['vill_freq'] > robs['vill_freq_gto'] else -1
                    for n, r in res.items():
                        dfreq, dcall, kl = shown(spec, robs, n) if n else (0.0, 0.0, 0)
                        z1, z2 = shown_z(spec, robs, n) if n else (0.0, 0.0)
                        if n and spec['type'] == 'iso' and kl == 0: continue        # v4.3 (Lucho) : « complété 0 fois » alors qu'il complète dans ce coup
                        leak = shown_leak(spec, dfreq, dcall, robs) if n else LEAKS[(stat_kind(spec, robs), sgn)]   # v4.3 : le défaut cité est celui des stats affichées
                        valid = r['valid'] & ~incoherent & r['robuste'] & ~prem
                        gain = np.where(valid, r['ev_expl'] - r['ev_gto'], 0.0)
                        flip = valid & (r['gto'] != r['expl'])
                        thin = n in N_THIN
                        if thin:     # le read complet changerait la décision, le read combiné non
                            pool = [i for i in np.where(valid & ~flip & robs['valid'] & (robs['gto'] != robs['expl']))[0]
                                    if (robs['ev_expl'][i] - robs['ev_gto'][i]) >= 2 * noise] if max(abs(dfreq), abs(dcall)) >= 5 else []   # v4.3 : le read affiché suggère bien le défaut
                            kq = 'échantillon'
                        else:
                            pool = [i for i in np.where(flip)[0] if gain[i] >= pf.threshold(r['gto'][i], r['expl'][i], S) * noise
                                    and margin(spec, r, i) >= 1.0 * noise       # v4 : l'action choisie bat aussi la 2e meilleure d'au moins 1 x bruit
                                    and not (S <= 4 and r['expl'][i] in ('fold', 'limpe'))   # v4 (R5, audit PA/Lucky) : à 4 BB ou moins on ne folde ni ne limpe : on pousse et on paie
                                    and not (S == 6 and r['expl'][i] == 'fold' and 0 < n < 40)   # à 6 BB le field est proche de la théorie : read d'au moins 40 occasions
                                    and not (S <= 6 and spec['type'] == 'call' and r['expl'][i] == 'fold' and n < 80)   # v4.2 (PA, Lucky) : R2 à 6 BB, 80 occasions
                                    and gto_freq(kind, S, spec, i, r['expl'][i]) < MIX_MAX]          # v4.2 : HRC ne joue pas déjà la réponse 30 % du temps
                            kq = 'inconnu' if n == 0 else 'adaptation'
                            if n:   # v4 : le read affiché doit montrer un écart net (>= 5 points) et aller dans le sens de la réponse
                                def sens_ok(i):
                                    e, g0 = r['expl'][i], r['gto'][i]
                                    if spec['type'] == 'iso': return iso_read(e, dfreq, dcall, (z1, z2)) is not None   # v4.3 : la règle colle aux stats affichées
                                    if abs(dfreq) < 5 or max(z1, z2) < Z_MIN: return False          # v4.4 : écart net ET significatif
                                    if spec['type'] == 'vsopen':                                     # défendre plus large contre un open large, plus serré sinon
                                        if e == 'paie' and g0 == 'pousse': return False             # ralentir un monstre n'est pas « défendre plus large »
                                        return (e in ('paie', 'pousse')) == (dfreq > 0)
                                    if e == 'limpe': return dfreq > 0                                 # v4.4 (Lucky) : R4 = il paie trop, on limpe au lieu de pousser
                                    if spec['type'] == 'call': return (e == 'paie') == (dfreq > 0)
                                    agg = ('pousse', 'relance')                                       # v4.5 : plus agressif contre un joueur qui défend peu
                                    if e in agg and g0 not in agg: return dfreq < 0
                                    if e not in agg and g0 in agg: return dfreq > 0
                                    return True
                                pool = [i for i in pool if sens_ok(i)]
                                # v4.4 (les trois coachs) : contre un joueur qui paie trop, la leçon « tapis plus serré » (tapis théorique -> fold)
                                tight = [i for i in np.where(flip)[0] if r['gto'][i] == 'pousse' and r['expl'][i] == 'fold' and S > 4
                                         and gain[i] >= 2.0 * noise and margin(spec, r, i) >= max(MIN_MARGIN, noise) and sens_ok(i)
                                         and not (S == 6 and n < 40) and gto_freq(kind, S, spec, i, 'fold') < MIX_MAX]
                                pool = sorted(set(pool) | set(tight))
                                pool = [i for i in pool if sens_ok(i)]
                        gap = shown_gap(spec, r, robs, n)
                        traps = ([i for i in np.where(valid & ~flip)[0] if 3 * noise <= margin(spec, r, i) <= TRAP_MAX_MARGIN * noise
                                  and not (hero_btn and S >= 10 and r['expl'][i] == 'fold' and 'relance' not in r.get('acts', ()))]   # v4.2 (PA) : sans option de relance, hors domaine
                                 if not thin and abs(gap) >= TRAP_MIN_GAP else [])           # v4.2 : vrai écart du vilain, décision non triviale
                        for kindq, idxs, nmax in ((kq, pool, per_cell), ('piège', traps, 2)):
                            idxs = [i for i in idxs if margin(spec, r, i) >= MIN_MARGIN]      # v4.3 : pas de quasi-égalité présentée comme une seule bonne réponse
                            for i in rnd.sample(idxs, min(nmax, len(idxs))):
                                rule = ('R0' if kindq == 'inconnu' else 'R10' if kindq == 'échantillon' else 'R9' if kindq == 'piège'
                                        else rule_for(spec, r['gto'][i], r['expl'][i], pname, hero_btn, r))
                                lk = leak
                                if (kindq == 'adaptation' and spec['type'] == 'shove' and r['gto'][i] == 'pousse' and r['expl'][i] == 'fold'
                                        and dfreq > 0): rule = 'R16'                       # v4.4 : tapis plus serré contre un joueur qui paie trop
                                if kindq == 'adaptation' and spec['type'] == 'iso': rule, lk = iso_read(r['expl'][i], dfreq, dcall, (z1, z2))
                                q = build_q(kindq, pname, n, lam, kind, name, spec, S, noise, r, robs, i, rule, lk, gain[i])
                                cands.append(q)
                                if kindq == 'adaptation' and spec['type'] in ('call', 'shove') and stat_kind(spec, robs) != 'defend' and abs(dfreq) >= 5 and z1 >= Z_MIN and rnd.random() < 0.4:   # v4.4 : écart net et significatif
                                    sgs = 1 if dfreq > 0 else -1
                                    base = SIT[(kind, name)].format(S=S)
                                    cands.append(dict(id=q['id'] + '-leak', type='identification', kind=kind, stack=S, situation=name, hero_hand=q['hero_hand'],
                                                      enonce=f"{base} {stat_line(spec, robs, n)} Quel est le défaut de ce vilain ?",
                                                      options=LEAK_OPTIONS, bonne_reponse=LEAK_OPTIONS[LEAK_ANS[(spec['type'], sgs)]], intensite=lam,
                                                      observations=n, profil=pname, regle='R10', poids=q['poids'],
                                                      explication=f"Sa fréquence est {'au-dessus' if sgs > 0 else 'en dessous'} de la théorie, sur {n} occasions : il {leak}.",
                                                      stats=stats_struct(spec, robs, n), difficulte='facile', niveau_donnees='A (stack résolu par HRC)'))
    cands += profile_questions(rnd)
    # dédoublonnage (type, situation, stack, main, réponse, défaut, profil si piège) : on garde l'intensité la plus forte
    best = {}
    for q in cands:
        variant = SCALE > 1 and q['type'] not in ('inconnu',)       # v4.3 : un autre échantillon ou une autre intensité = une autre question (stats affichées différentes)
        k = (q['type'], q['kind'], q['situation'], q['stack'], q['hero_hand'], q['bonne_reponse'], q.get('leak', ''),
             q['profil'] if q['type'] in ('piège', 'profil') or variant else '', q['observations'] if q['type'] in ('piège', 'profil') or variant else 0,
             q['intensite'] if variant else 0)
        if k not in best or q['intensite'] > best[k]['intensite']:
            best[k] = q
    pool = list(best.values())
    # v4.3 (Lucho, Lucky) : même main, même décision, mêmes EV = doublon, même si l'échantillon affiché diffère
    sig = {}
    for q in sorted(pool, key=lambda q: (-q['intensite'], q['id'])):
        if q['type'] in ('identification', 'profil'): sig[q['id']] = q; continue
        k = (q['type'], q['kind'], q['situation'], q['stack'], q['hero_hand'], q['bonne_reponse'],
             tuple(sorted((a, round(v, -1)) for a, v in (q.get('ev_options_mBB') or {}).items())))
        sig.setdefault(k, q)
    pool = list(sig.values())
    # v4.4 (Lucho, PA) : une adaptation dont l'EV est celle du vilain inconnu n'apprend rien du read ; un énoncé identique ne sert qu'une fois
    evsig = lambda q: (q['kind'], q['situation'], q['stack'], q['hero_hand'], q['bonne_reponse'],
                       tuple(sorted((a, round(v, -1)) for a, v in (q.get('ev_options_mBB') or {}).items())))
    base = {evsig(q) for q in pool if q['type'] == 'inconnu'}
    seen_txt = set(); p3 = []
    for q in sorted(pool, key=lambda q: ({'inconnu': 0, 'adaptation': 1}.get(q['type'], 2), -q['intensite'], q['id'])):
        if q['type'] == 'adaptation' and evsig(q) in base: continue
        t = (q['enonce'], q['type'] in ('identification', 'profil'))
        if t in seen_txt: continue
        seen_txt.add(t); p3.append(q)
    pool = p3
    # v4.1 : (1) pas de questions « défaut du vilain » à énoncé identique (la main n'apparaît pas dans l'énoncé)
    seen_e = set(); p2 = []
    for q in sorted(pool, key=lambda q: q['id']):
        if q['type'] == 'identification':
            if q['enonce'] in seen_e: continue
            seen_e.add(q['enonce'])
        p2.append(q)
    pool = p2
    if SCALE > 1:
        out = select_targets(pool, rnd)
    else:
        out = select_quotas(pool, rnd)
    # v4.1 : ordre des options mélangé, position de la bonne réponse équilibrée (déterministe)
    cnt = collections.Counter()
    for q in sorted(out, key=lambda q: q['id']):
        o = list(q['options']); m = len(o)
        if q['type'] == 'profil': continue         # liste de pastilles : ordre fixe, conservé
        rr = random.Random(q['id']); others = [x for x in o if x != q['bonne_reponse']]; rr.shuffle(others)
        pos = min(range(m), key=lambda p: (cnt[(m, p)], rr.random())); cnt[(m, pos)] += 1
        q['options'] = others[:pos] + [q['bonne_reponse']] + others[pos:]
    return out


TOP_SHARE = 0.15          # « mains fortes » : les 15 % de mains les plus fortes contre une main au hasard


def _eq(i, rng):
    q = ee.P * rng; s = q.sum()
    return float(ee.E[i] @ q / s) if s > 0 else None


def theory(spec, kind, S, r, i):
    """éléments théoriques d'une question (exacts, préflop) : cote du pot, équité contre la range du vilain et contre la range
    théorique, fréquence de fold face à ton tapis ou à ta relance"""
    pct = lambda x: None if x is None else round(100 * x, 1)
    rnd1 = lambda x: None if x is None else round(x, 1)
    if spec['type'] == 'call':
        call, final = {'hu_bb': (S - 1, 2 * S), 'btn_bb': (S - 1, 2 * S + 0.5), 'btn_sb': (S - 0.5, 2 * S + 1)}[spec['formula']]
        return dict(kind='call', call_bb=call, pot_bb=final, need_pct=round(100 * call / final, 1), range_pct=round(r['vill_freq'], 1),
                    range_gto_pct=round(r['vill_freq_gto'], 1), eq_pct=pct(_eq(i, r['vec'])), eq_gto_pct=pct(_eq(i, r['vec_gto'])),
                    after_limp=bool(spec.get('hero_range')))
    if spec['type'] == 'iso':
        out = dict(kind='iso', limp_pct=round(r['vill_freq'], 1), limp_gto_pct=round(r['vill_freq_gto'], 1), eq_limp_pct=pct(_eq(i, r['vec'])),
                   win_bb=2.0 + spec.get('dead', 0.0), limper=('BTN' if spec.get('dead') else 'SB'), has_jam=bool(r.get('has_jam', True)))
        if r.get('has_jam', True):
            out.update(fold_pct=round(r['fold_pct'], 1), fold_gto_pct=round(r['fold_pct_gto'], 1), eq_called_pct=pct(_eq(i, r['vec'] * r['call_vec'])),
                       eq_called_gto_pct=pct(_eq(i, r['vec_gto'] * r['call_vec_gto'])))
        if r.get('raise_bb'): out.update(raise_bb=r['raise_bb'], raise_fold_pct=rnd1(r['raise_fold_pct']), raise_fold_gto_pct=rnd1(r['raise_fold_pct_gto']))
        return out
    if spec['type'] == 'vsopen':
        return dict(kind='vsopen', open_bb=r['open_bb'], open_pct=round(r['vill_freq'], 1), open_gto_pct=round(r['vill_freq_gto'], 1),
                    fold_pct=round(r['fold_pct'], 1), fold_gto_pct=round(r['fold_pct_gto'], 1), eq_open_pct=pct(_eq(i, r['vec'])),
                    eq_called_pct=pct(_eq(i, r['vec'] * r['call_vec'])), win_bb=round(r['open_bb'] + 1 + spec.get('dead', 0.5), 2))
    raise_info = (dict(raise_bb=r['raise_bb'], raise_fold_pct=rnd1(r['raise_fold_pct']), raise_fold_gto_pct=rnd1(r['raise_fold_pct_gto']))
                  if r.get('raise_bb') else {})
    if r.get('stat_kind') == 'defend':                       # arbre sans tapis (18 BB et plus) : seule la relance met la pression
        return dict(kind='open', defend_pct=round(r['vill_freq'], 1), defend_gto_pct=round(r['vill_freq_gto'], 1),
                    eq_called_pct=pct(_eq(i, r['vec'])), win_bb=1.5, **raise_info)
    fold = float(ee.P @ (1 - r['vec'])); fold0 = float(ee.P @ (1 - r['vec_gto']))
    if r.get('vec2') is not None:
        fold *= float(ee.P @ (1 - r['vec2'])); fold0 *= float(ee.P @ (1 - r['vec2_gto']))
    out = dict(kind='shove', fold_pct=round(100 * fold, 1), fold_gto_pct=round(100 * fold0, 1), win_bb=1.5 if spec.get('formula') == 'btn' else 1.0,
               eq_called_pct=pct(_eq(i, r['vec'])), eq_called_gto_pct=pct(_eq(i, r['vec_gto'])), call_pct=round(r['vill_freq'], 1), call_gto_pct=round(r['vill_freq_gto'], 1),
               **raise_info)
    if r.get('iso_pct') is not None: out.update(iso_pct=round(r['iso_pct'], 1), iso_gto_pct=round(r['iso_pct_gto'], 1))
    return out


def postflop(spec, kind, S, r, i):
    """ce qui se joue après le flop quand la main voit un flop (limp checké, check du BB sur un limp, call d'un open) :
    équité de la main et de la range contre la range adverse qui voit le flop, mains fortes dans cette range, position, SPR"""
    pot = 2.0
    if spec['type'] == 'iso':
        hero = r['hero_range_gto']; vill, vill0 = r['vec'], r['vec_gto']; pot = 2.0 + spec.get('dead', 0.0)
        pos = spec.get('position') or ('OOP' if kind == 'hu' else 'IP')   # v4.3 : en heads-up le SB est au bouton ; v4.5 : le BTN parle après le BB
        seat = 'BB'
    elif spec['type'] == 'vsopen':
        hero = r['hero_range_gto']; vill, vill0 = r['vec'], r['vec_gto']; pot = 2 * r['open_bb'] + spec.get('dead', 0.5)
        pos = 'OOP'; seat = 'BB'
    elif r.get('ev_limp') is not None:
        n = ee.node(kind, S, spec['limp_node']); labs, F, _ = n
        iso = sum(F[:, j] for j, l in enumerate(labs) if l.startswith('R') or l == 'A')
        vill0 = 1 - iso; vill = 1 - ee.scale_freq(iso, ee.W * np.ones(169), r['facteurs']['iso'])
        hn = ee.node(kind, S, spec['hero']); hero = hn[1][:, hn[0].index('C')]
        pos = 'IP' if kind == 'hu' else 'OOP'          # SB qui complète : au bouton en heads-up, premier à parler en BvB
        seat = 'SB'
    else:
        return None
    left = S - (r['open_bb'] if spec['type'] == 'vsopen' else 1.0)      # tapis restant de chacun après le préflop
    top = ee.VSR >= np.quantile(ee.VSR, 1 - TOP_SHARE)
    share = lambda v: float((ee.P * v * top).sum() / (ee.P * v).sum())
    qh = ee.P * hero; qv = ee.P * vill
    range_eq = float(qh @ ee.E @ qv / (qh.sum() * qv.sum())) if qh.sum() > 0 and qv.sum() > 0 else None
    return dict(position=pos, hero_seat=seat, table=kind, spr=round(left / pot, 1), pot_bb=round(pot, 2), left_bb=round(left, 2), line=spec['type'],
                eq_hand_pct=round(100 * _eq(i, vill), 1), eq_hand_gto_pct=round(100 * _eq(i, vill0), 1),
                eq_range_pct=(round(100 * range_eq, 1) if range_eq is not None else None),
                villain_range_pct=round(100 * float((ee.P * vill).sum()), 1), villain_range_gto_pct=round(100 * float((ee.P * vill0).sum()), 1),
                strong_pct=round(100 * share(vill), 1), strong_gto_pct=round(100 * share(vill0), 1))


def build_q(kindq, pname, n, lam, kind, name, spec, S, noise, r, rshow_src, i, rule, leak, gain_i):
    h = NAMES[i]
    ans, gto_ans = LABEL[r['expl'][i]], LABEL[r['gto'][i]]
    base = SIT[(kind, name)].format(S=S)
    rshow = rshow_src if n else r
    read = "Tu n'as aucune information sur ce vilain." if n == 0 else stat_line(spec, rshow, n)
    g = round(1000 * float(gain_i))
    fac = {k: round(float(v), 6) for k, v in r['facteurs'].items() if k not in ('limp', 'shape')}
    fac['limp'] = bool(r['facteurs'].get('limp', True)); fac['shape'] = bool(r['facteurs'].get('shape', False))
    evo = {LABEL[a]: round(1000 * ev_of(r, i, a)) for a in acts_of(spec, r)}      # v4.5 : EV de chaque option, par libellé
    q = dict(id=f"{kind}-{S}-" + hashlib.md5(f'{name}|{pname}|{lam}|{n}|{h}|{kindq}'.encode()).hexdigest()[:6],
             type=kindq, kind=kind, stack=S, situation=name, hero_hand=h,
             enonce=f"{base} Ta main : {hand_txt(h)}. {read} Que fais-tu ?",
             options=options_for(spec, r), bonne_reponse=ans, action_GTO=gto_ans, gain_mBB=g,
             seuil_bruit_mBB=round(1000 * noise), leak=('' if n == 0 else leak), intensite=lam, observations=n,
             profil=pname, regle=rule, niveau_donnees='A (stack résolu par HRC)' + ((' ; limp : EV estimée (décomposition de l\'EV HRC)' if spec.get('limp_estimate') else ' ; limp : borne basse HRC') if r['ev_limp'] is not None else ''),
             facteurs=fac, ev_jeu_vs_fold_mBB=(round(1000 * float(r['ev_raw'][i])) if r.get('ev_raw') is not None else None),
             ev_options_mBB=evo, relance_bb=r.get('raise_bb'), open_bb=r.get('open_bb'),
             ev_limp_vs_fold_mBB=(round(1000 * float(r['ev_limp'][i])) if r['ev_limp'] is not None else None),
             marge_mBB=round(1000 * margin(spec, r, i)),
             acceptables=acceptables(spec, r, i, noise), freq_gto_reponse_pct=round(100 * gto_freq(kind, S, spec, i, r['expl'][i]), 1),
             iso_pct=(round(r['iso_pct']) if r.get('iso_pct') is not None else None), iso_pct_gto=(round(r['iso_pct_gto']) if r.get('iso_pct_gto') is not None else None),
             ev_check_vs_fold_mBB=(round(1000 * float(r['ev_check'][i])) if r.get('ev_check') is not None else None),
             theorie=theory(spec, kind, S, r, i), postflop=postflop(spec, kind, S, r, i))
    q['stats'] = stats_struct(spec, rshow, n)
    q['explication'] = explain(kindq, leak, ans, gto_ans, g, q['seuil_bruit_mBB'], r, i, rule, n, spec, pname)
    q['difficulte'] = 'piège' if kindq in ('piège', 'échantillon') else ('facile' if gain_i >= 4 * noise else 'moyen')
    q['poids'] = pf.prevalence(pname) * (1.0 if n == 0 else realism(leak, S))
    return q


if __name__ == '__main__':
    qs = make()
    json.dump(qs, open(os.path.join(OUT_DIR, 'quiz_field_v4_2.json'), 'w'), ensure_ascii=False, indent=1)
    cols = ['id', 'type', 'difficulte', 'kind', 'stack', 'situation', 'hero_hand', 'enonce', 'options', 'bonne_reponse', 'action_GTO',
            'gain_mBB', 'seuil_bruit_mBB', 'leak', 'observations', 'profil', 'regle', 'intensite', 'niveau_donnees', 'explication']
    with open(os.path.join(OUT_DIR, 'quiz_field_v4_2.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
        for q in qs:
            w.writerow({**q, 'options': ' | '.join(q['options'])})
    from collections import Counter
    print(len(qs), 'questions', Counter(q['type'] for q in qs), Counter(q.get('regle') for q in qs))
