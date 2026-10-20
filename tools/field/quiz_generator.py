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
N_TARGET = int(os.environ.get('EXPRESSO_N_QUIZ', 400))
N_OBS = (20, 40, 80)          # occasions observées pour les adaptations
N_THIN = (3, 5)               # read trop mince (type « échantillon »)

SIT = {
 ('3w', "BB face à l'all-in du SB (BTN fold)"): "3 joueurs, {S} BB chacun. Le BTN fold et le SB pousse all-in. Tu es au BB.",
 ('3w', "BB face à l'all-in du BTN (SB fold)"): "3 joueurs, {S} BB chacun. Le BTN pousse all-in et le SB fold. Tu es au BB.",
 ('3w', "SB face à l'all-in du BTN"):           "3 joueurs, {S} BB chacun. Le BTN pousse all-in. Tu es au SB (le BB est derrière).",
 ('3w', "SB pousse (BTN fold) face au BB"):      "3 joueurs, {S} BB chacun. Le BTN fold. Tu es au SB, le BB est derrière.",
 ('3w', "BTN pousse face au SB et au BB"):       "3 joueurs, {S} BB chacun. Tu es au BTN, le SB et le BB sont derrière.",
 ('hu', "BB face à l'all-in du SB"):             "Heads-up, {S} BB chacun. Le SB pousse all-in. Tu es au BB.",
 ('hu', "SB pousse face au BB"):                 "Heads-up, {S} BB chacun. Tu es au SB (bouton), le BB est derrière.",
}
LEAKS = {('call', +1): "pousse trop souvent", ('call', -1): "ne pousse pas assez",
         ('shove', +1): "paie trop souvent", ('shove', -1): "ne paie pas assez"}
LEAK_OPTIONS = ["Il pousse trop souvent", "Il ne pousse pas assez", "Il paie trop souvent", "Il ne paie pas assez"]
LEAK_ANS = {('call', +1): 0, ('call', -1): 1, ('shove', +1): 2, ('shove', -1): 3}
LABEL = {'paie': 'Payer', 'pousse': 'Pousser all-in', 'limpe': 'Limp', 'fold': 'Fold'}

RULES = {
 'R0': "Vilain inconnu = rec passif, pas GTO : il paie et relance moins que la théorie. Vole plus (limp en heads-up, tapis en BvB et au BTN), paie plus serré (sauf à 4 BB ou moins).",
 'R1': "Contre un vilain qui pousse trop, paie plus large : overfolder contre lui est la pire fuite.",
 'R2': "Contre un vilain qui pousse peu, paie plus serré : sa range d'all-in est forte.",
 'R3': "Contre un vilain qui paie peu, pousse plus large, poubelles comprises.",
 'R4': "Au SB contre un passif, limpe : la main qui ne se pousse plus ne se folde pas, et celle que son call ne paierait plus se limpe aussi.",
 'R5': "Ne folde un push théorique que sur un read solide et un gain net.",
 'R6': "Contre un dégène qui iso ou paie tout, folde le bas de range.",
 'R7': "Au BTN 3-way, jamais de limp : fold ou push.",
 'R9': "Un écart de fréquence qui ne retourne pas la décision ne change rien.",
 'R10': "Quelques occasions ne font pas une tendance : reste sur le profil par défaut.",
 'R11': "Contre un reg identifié, joue la théorie : n'invente pas d'exploit.",
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
    if spec['type'] == 'call':
        return f"Sur {n} occasions dans cette situation, ce vilain a poussé {k} fois ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."
    if r.get('vill_freq2') is not None:
        pct2 = 100 * round(n * r['vill_freq2'] / 100) / n      # v4.1 : le 2e pourcentage vient aussi de k / n (cohérent avec l'export)
        return (f"Sur {n} occasions, ce vilain a payé {pct:.0f} % des all-in au SB (GTO : {r['vill_freq_gto']:.0f} %) "
                f"et {pct2:.0f} % au BB quand le SB fold (GTO : {r['vill_freq2_gto']:.0f} %).")
    return f"Sur {n} occasions, ce vilain a payé {k} all-in ({pct:.0f} % ; GTO : {r['vill_freq_gto']:.0f} %)."



def stats_struct(spec, r, n):
    """statistiques observées sous forme structurée (export application) : k sur n, % observé, % GTO"""
    if n == 0: return []
    k = round(n * r['vill_freq'] / 100)
    out = [dict(stat='shove_pct' if spec['type'] == 'call' else 'call_pct', n=n, k=k, observed_pct=round(100 * k / n, 1), gto_pct=round(r['vill_freq_gto'], 1))]
    if r.get('vill_freq2') is not None:
        k2 = round(n * r['vill_freq2'] / 100)
        out.append(dict(stat='call_pct_bb_sb_fold', n=n, k=k2, observed_pct=round(100 * k2 / n, 1), gto_pct=round(r['vill_freq2_gto'], 1)))
    return out


INF = {"pousse trop souvent": "pousser trop souvent", "ne pousse pas assez": "ne pas pousser assez",
       "paie trop souvent": "payer trop souvent", "ne paie pas assez": "ne pas payer assez"}


def rule_for(spec, gto, ex, pname, hero_btn):
    if ex == 'limpe': return 'R4'
    if spec['type'] == 'call':
        return 'R1' if ex == 'paie' else 'R2'
    if ex == 'pousse': return 'R3'
    if hero_btn: return 'R7'
    return 'R6' if not pf.PROFILES[pname]['passif'] else 'R5'


def options_for(spec, r):
    if spec['type'] == 'call':
        return ['Payer', 'Fold']
    return ['Pousser all-in', 'Limp', 'Fold'] if r['ev_limp'] is not None else ['Pousser all-in', 'Fold']


def ev_of(r, i, action):
    if action == 'fold': return 0.0
    if action == 'paie': return float(r['ev_raw'][i])
    if action == 'limpe': return float(r['ev_limp'][i])
    return float(r['ev_raw'][i])


def margin(spec, r, i):
    """écart d'EV entre l'action choisie et la meilleure autre action disponible (pièges : la décision est nette)"""
    acts = ['paie', 'fold'] if spec['type'] == 'call' else (['pousse', 'limpe', 'fold'] if r['ev_limp'] is not None else ['pousse', 'fold'])
    ch = r['expl'][i]
    return ev_of(r, i, ch) - max(ev_of(r, i, a) for a in acts if a != ch)


def explain(kind_q, leak, ans, gto_ans, gain, noise, r, i, rule, n, spec, pname=''):
    verbe = 'payer' if spec['type'] == 'call' else 'pousser'
    evs = f"EV par rapport au fold : {verbe} {1000 * float(r['ev_raw'][i]):+.0f} mBB"
    if r['ev_limp'] is not None and not spec.get('limp_estimate'):
        evs += f", limp {1000 * float(r['ev_limp'][i]):+.0f} mBB (borne basse : EV HRC contre un BB qui jouerait la théorie ; en BvB, les coachs limpent peu)"
    elif r['ev_limp'] is not None:
        evs += (f", limp {1000 * float(r['ev_limp'][i]):+.0f} mBB (estimation : contre lui, le BB relance ton limp environ {r['iso_pct']:.0f} % du temps, "
                f"{r['iso_pct_gto']:.0f} % en théorie)")
    lesson = RULES[rule]
    if kind_q == 'adaptation':
        return (f"Le vilain {leak} ({n} occasions). Contre lui, {ans.lower()} bat l'action GTO ({gto_ans.lower()}) de {gain:.0f} mBB, "
                f"au-delà du bruit du moteur ({noise} mBB). {evs}. Règle {rule} : {lesson}")
    if kind_q == 'inconnu':
        return (f"Sans read, le vilain est un rec passif. Contre lui, {ans.lower()} bat l'action GTO ({gto_ans.lower()}) de {gain:.0f} mBB. "
                f"{evs}. Règle R0 : {RULES['R0']}")
    if kind_q == 'échantillon':
        return (f"Le vilain semble {INF.get(leak, leak)}, mais sur {n} occasions seulement : combiné au profil par défaut, le read ne change pas la décision. "
                f"Règle R10 : {RULES['R10']}")
    if rule == 'R11':
        return f"Piège : ce vilain est un reg, donc la théorie s'applique et {ans.lower()} reste la meilleure action. {evs}. Règle R11 : {RULES['R11']}"
    who = 'un rec passif' if n == 0 else 'ce vilain'
    return f"Piège : même contre {who}, {ans.lower()} reste la meilleure action. {evs}. Règle R9 : {RULES['R9']}"


PROFIL_OPTIONS = ['Rec passif', 'Reg', 'Calling station', 'Dégène', 'Nit']      # v4.2 : rec passif et reg séparés
PROFIL_KEY = {'Rec passif': pf.DEFAULT, 'Reg': 'Reg', 'Calling station': 'Calling station', 'Dégène': 'Dégène', 'Nit': 'Nit'}
GROUP = {lab: (key,) for lab, key in PROFIL_KEY.items()}
PROFIL_N = (40, 80, 150)
MIX_MAX = 0.30            # v4.2 : HRC joue déjà la réponse 30 % du temps ou plus → pas une vraie déviation
TRAP_MIN_GAP = 5.0        # v4.2 : un piège montre un vilain écarté d'au moins 5 points du GTO
TRAP_MAX_MARGIN = 10.0    # v4.2 : au-delà de 10 x le bruit, la décision est triviale
HRC_LABEL = {'paie': 'C', 'pousse': 'A', 'limpe': 'C', 'fold': 'F'}


def gto_freq(kind, S, spec, i, action):
    """fréquence HRC (0-1) de l'action du héros pour la main i"""
    n = ee.node(kind, S, spec['hero'])
    if n is None: return 0.0
    labs, F, _ = n; lab = HRC_LABEL[action]
    return float(F[i, labs.index(lab)]) if lab in labs else 0.0


def shown_gap(spec, r, robs, n):
    """écart du vilain au GTO tel qu'affiché (k / n), en points ; sans observation : écart du profil par défaut"""
    if n == 0: return r['vill_freq'] - r['vill_freq_gto']
    return 100 * round(n * robs['vill_freq'] / 100) / n - robs['vill_freq_gto']


def acceptables(spec, r, i, noise):
    """actions dont l'EV est à moins de 1 x bruit de la meilleure (affichées comme acceptées)"""
    acts = ['paie', 'fold'] if spec['type'] == 'call' else (['pousse', 'limpe', 'fold'] if r['ev_limp'] is not None else ['pousse', 'fold'])
    best = max(ev_of(r, i, a) for a in acts)
    return [LABEL[a] for a in acts if a != r['expl'][i] and best - ev_of(r, i, a) < noise]


def _freqs(S, fac):
    """fréquences du vilain (all-in en premier au SB ; call d'un all-in au BB) en heads-up pour des facteurs donnés"""
    out = []
    for (kind, name) in (('hu', "BB face à l'all-in du SB"), ('hu', 'SB pousse face au BB')):
        r = ee.run_spot(kind, S, name, ee.SPOTS[(kind, name)], profiles={'x': fac})
        out.append((r['x']['vill_freq'], r['x']['vill_freq_gto']))
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
                    k = [round(n * exp[member][j][0] / 100) for j in (0, 1)]
                    obs = [100 * kk / n for kk in k]
                    chi = {}
                    for l2 in PROFIL_OPTIONS:
                        best = 1e9
                        for m2 in GROUP[l2]:
                            c = 0.0
                            for j in (0, 1):
                                p = min(max(exp[m2][j][0] / 100, 0.01), 0.99)
                                c += (obs[j] / 100 - p) ** 2 / (p * (1 - p) / n)
                            best = min(best, c)
                        chi[l2] = best
                    order = sorted(chi, key=chi.get)
                    if order[0] != lab or chi[order[1]] - chi[order[0]] < 4.0:
                        continue
                    if n == 150 and any(q0['profil'] == member and q0['stack'] == S for q0 in out):
                        continue                                  # 150 occasions : seulement si 40 et 80 ne suffisent pas
                    q = dict(id=f"pf-{S}-" + hashlib.md5(f'profil|{member}|{S}|{n}'.encode()).hexdigest()[:6], type='profil', kind='hu', stack=S,
                             situation='Heads-up : lecture du vilain', hero_hand='',
                             enonce=(f"Heads-up, {S} BB chacun. Sur {n} occasions, ce vilain a poussé all-in {k[0]} fois quand il était au SB ({obs[0]:.0f} % ; GTO : {gto[0][0]:.0f} %) "
                                     f"et a payé {k[1]} all-in sur {n} ({obs[1]:.0f} % ; GTO : {gto[1][0]:.0f} %). Quelle pastille lui donnes-tu ?"),
                             stats=[dict(stat='shove_pct', n=n, k=k[0], observed_pct=round(obs[0], 1), gto_pct=round(gto[0][0], 1)), dict(stat='call_pct', n=n, k=k[1], observed_pct=round(obs[1], 1), gto_pct=round(gto[1][0], 1))],
                             options=PROFIL_OPTIONS, bonne_reponse=lab, action_GTO='', gain_mBB=0, seuil_bruit_mBB=0, leak='', intensite=1.0,
                             observations=n, profil=member, regle='R10',
                             explication=(f"Il pousse {'plus' if obs[0] > gto[0][0] + 2 else 'moins' if obs[0] < gto[0][0] - 2 else 'comme le GTO'} que le GTO et paie "
                                          f"{'plus' if obs[1] > gto[1][0] + 2 else 'moins' if obs[1] < gto[1][0] - 2 else 'comme le GTO'} : à {S} BB, ces deux fréquences sont plus proches du profil « {lab.lower()} » "
                                          f"que de toute autre pastille, et {n} occasions suffisent pour trancher. "
                                          + ("Le reg colle à la théorie ; le rec passif pousse et paie moins : c'est la distinction qui rapporte le plus. " if lab in ('Rec passif', 'Reg') else '')
                                          + f"Règle R10 : {RULES['R10']}"),
                             difficulte='moyen', niveau_donnees='profil du moteur (hypothèse de coachs, non mesuré)', poids=pf.prevalence(member))
                    out.append(q)
    return out


def make(seed=11, per_cell=30):
    rnd = random.Random(seed); cands = []
    advers = [p for p in pf.PROFILES if p != 'Reg']
    for lam in (1.0, 0.5):
        ee.INTENSITE = lam
        for (kind, name), spec in ee.SPOTS.items():
            hero_btn = name.startswith('BTN')
            for S in (4, 6, 8, 10, 12):
                noise = ee.NOISE_BB[S]
                full = ee.run_spot(kind, S, name, spec, profiles={p: pf.factors(p, S) for p in pf.PROFILES})
                if full is None: continue
                reg = full['Reg']
                incoherent = reg['valid'] & (reg['gto'] != reg['expl'])        # la décision change même contre le GTO : base HRC incohérente
                # R8 : limp-trap des paires premium = désaccord des coachs, exclu des questions notées
                prem = np.array([NAMES[i] in pf.PREMIUM_PAIRS for i in range(169)]) & (spec['formula'] == 'hu_sb') & (S >= 6)
                # --- R11 : vilain identifié reg → théorie ; on ne garde que les décisions nettes
                if lam == 1.0:
                    for n in (40, 80):
                        r = reg
                        ok = r['valid'] & ~incoherent & ~prem & (r['gto'] == r['expl'])
                        idx = [i for i in np.where(ok)[0] if 3 * noise <= margin(spec, r, i) <= TRAP_MAX_MARGIN * noise]
                        for i in rnd.sample(idx, min(4, len(idx))):      # v4.1 : 4 par cellule (le reg pesait 7 % pour 15 % du field)
                            cands.append(build_q('piège', 'Reg', n, lam, kind, name, spec, S, noise, r, r, i, 'R11', '', 0.0))
                for pname in advers:
                    fobs = pf.factors(pname, S)
                    ns = (0,) if pname == pf.DEFAULT else N_OBS + N_THIN
                    effs = {n: (pf.posterior(fobs, S, n) if n else pf.factors(pf.DEFAULT, S)) for n in ns}
                    res = ee.run_spot(kind, S, name, spec, profiles={n: f for n, f in effs.items()})
                    robs = full[pname]
                    sgn = 1 if robs['vill_freq'] > robs['vill_freq_gto'] else -1
                    leak = LEAKS[(spec['type'], sgn)]
                    for n, r in res.items():
                        valid = r['valid'] & ~incoherent & r['robuste'] & ~prem
                        gain = np.where(valid, r['ev_expl'] - r['ev_gto'], 0.0)
                        flip = valid & (r['gto'] != r['expl'])
                        thin = n in N_THIN
                        if thin:     # le read complet changerait la décision, le read combiné non
                            pool = [i for i in np.where(valid & ~flip & robs['valid'] & (robs['gto'] != robs['expl']))[0]
                                    if (robs['ev_expl'][i] - robs['ev_gto'][i]) >= 2 * noise]
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
                                dfreq = 100 * round(n * robs['vill_freq'] / 100) / n - robs['vill_freq_gto']      # écart tel qu'AFFICHÉ (k / n)
                                def sens_ok(i):
                                    e, g0 = r['expl'][i], r['gto'][i]
                                    if abs(dfreq) < 5: return False
                                    if spec['type'] == 'call': return (e == 'paie') == (dfreq > 0)
                                    if e == 'pousse': return dfreq < 0
                                    if e == 'fold' and g0 == 'pousse': return dfreq > 0
                                    return True
                                pool = [i for i in pool if sens_ok(i)]
                        gap = shown_gap(spec, r, robs, n)
                        traps = ([i for i in np.where(valid & ~flip)[0] if 3 * noise <= margin(spec, r, i) <= TRAP_MAX_MARGIN * noise
                                  and not (hero_btn and S >= 10 and r['expl'][i] == 'fold')]   # v4.2 (PA) : à 10 BB et plus, le BTN min-raise : hors domaine
                                 if not thin and abs(gap) >= TRAP_MIN_GAP else [])           # v4.2 : vrai écart du vilain, décision non triviale
                        for kindq, idxs, nmax in ((kq, pool, per_cell), ('piège', traps, 2)):
                            for i in rnd.sample(idxs, min(nmax, len(idxs))):
                                rule = ('R0' if kindq == 'inconnu' else 'R10' if kindq == 'échantillon' else 'R9' if kindq == 'piège'
                                        else rule_for(spec, r['gto'][i], r['expl'][i], pname, hero_btn))
                                q = build_q(kindq, pname, n, lam, kind, name, spec, S, noise, r, robs, i, rule, leak, gain[i])
                                cands.append(q)
                                if kindq == 'adaptation' and abs(robs['vill_freq'] - robs['vill_freq_gto']) >= 3 and rnd.random() < 0.4:
                                    base = SIT[(kind, name)].format(S=S)
                                    cands.append(dict(id=q['id'] + '-leak', type='identification', kind=kind, stack=S, situation=name, hero_hand=q['hero_hand'],
                                                      enonce=f"{base} {stat_line(spec, robs, n)} Quel est le défaut de ce vilain ?",
                                                      options=LEAK_OPTIONS, bonne_reponse=LEAK_OPTIONS[LEAK_ANS[(spec['type'], sgn)]], intensite=lam,
                                                      observations=n, profil=pname, regle='R10', poids=q['poids'],
                                                      explication=f"Sa fréquence ({'supérieure' if sgn > 0 else 'inférieure'} au GTO, sur {n} occasions) montre qu'il {leak}.",
                                                      stats=stats_struct(spec, robs, n), difficulte='facile', niveau_donnees='A (stack résolu par HRC)'))
    cands += profile_questions(rnd)
    # dédoublonnage (type, situation, stack, main, réponse, défaut, profil si piège) : on garde l'intensité la plus forte
    best = {}
    for q in cands:
        k = (q['type'], q['kind'], q['situation'], q['stack'], q['hero_hand'], q['bonne_reponse'], q.get('leak', ''), q['profil'] if q['type'] in ('piège', 'profil') else '', q['observations'] if q['type'] in ('piège', 'profil') else 0)
        if k not in best or q['intensite'] > best[k]['intensite']:
            best[k] = q
    pool = list(best.values())
    # v4.1 : (1) pas de questions « défaut du vilain » à énoncé identique (la main n'apparaît pas dans l'énoncé)
    seen_e = set(); p2 = []
    for q in sorted(pool, key=lambda q: q['id']):
        if q['type'] == 'identification':
            if q['enonce'] in seen_e: continue
            seen_e.add(q['enonce'])
        p2.append(q)
    pool = p2
    # quotas par profil proportionnels à sa fréquence dans le field ; tirage pondéré (Efraimidis-Spirakis) par le réalisme du défaut ;
    # pièges + échantillons au plus 40 % ; les questions « profil » comptent pour leur profil
    prev = {p: pf.prevalence(p) for p in pf.PROFILES}; tot = sum(prev.values())
    quota = {p: round(N_TARGET * v / tot) for p, v in prev.items()}
    keyed = sorted(pool, key=lambda q: -math.log(rnd.random() + 1e-12) / max(q['poids'], 1e-6))
    out, n_trap, used, taken = [], 0, {p: 0 for p in pf.PROFILES}, set()
    inc = collections.Counter()
    for strict in (True, False):
        for q in keyed:
            if len(out) >= N_TARGET: break
            cap = quota[q['profil']] if strict else 2 * quota[q['profil']]      # v4 : jamais plus de 2 x la part du profil dans le field
            if q['id'] in taken or used[q['profil']] >= cap: continue
            if q['type'] == 'inconnu':      # v4.1 : pas plus de 22 « inconnu » par (stack, réponse) : évite 57 « Pousser » à 8 BB
                kk = (q['stack'], q['bonne_reponse'])
                if inc[kk] >= 22: continue
                inc[kk] += 1
            if q['type'] in ('piège', 'échantillon'):
                if n_trap >= 0.35 * N_TARGET: continue
                n_trap += 1
            out.append(q); taken.add(q['id']); used[q['profil']] += 1
    # v4.1 : part des pièges + échantillons ramenée à 35 % de la banque finale (la banque finale peut être plus petite que N_TARGET)
    non = [q for q in out if q['type'] not in ('piège', 'échantillon')]
    allow = int(0.35 / 0.65 * len(non)); kept = 0; o2 = []
    for q in out:
        if q['type'] in ('piège', 'échantillon'):
            if kept >= allow: continue
            kept += 1
        o2.append(q)
    out = o2
    # v4.1 : ordre des options mélangé, position de la bonne réponse équilibrée (déterministe)
    cnt = collections.Counter()
    for q in sorted(out, key=lambda q: q['id']):
        o = list(q['options']); m = len(o)
        if q['type'] == 'profil': continue         # liste de pastilles : ordre fixe, conservé
        rr = random.Random(q['id']); others = [x for x in o if x != q['bonne_reponse']]; rr.shuffle(others)
        pos = min(range(m), key=lambda p: (cnt[(m, p)], rr.random())); cnt[(m, pos)] += 1
        q['options'] = others[:pos] + [q['bonne_reponse']] + others[pos:]
    return out


def build_q(kindq, pname, n, lam, kind, name, spec, S, noise, r, rshow_src, i, rule, leak, gain_i):
    h = NAMES[i]
    ans, gto_ans = LABEL[r['expl'][i]], LABEL[r['gto'][i]]
    base = SIT[(kind, name)].format(S=S)
    rshow = rshow_src if n else r
    read = "Tu n'as aucune information sur ce vilain." if n == 0 else stat_line(spec, rshow, n)
    g = round(1000 * float(gain_i))
    fac = {k: round(float(v), 4) for k, v in r['facteurs'].items() if k != 'limp'}
    fac['limp'] = bool(r['facteurs'].get('limp', True))
    q = dict(id=f"{kind}-{S}-" + hashlib.md5(f'{name}|{pname}|{lam}|{n}|{h}|{kindq}'.encode()).hexdigest()[:6],
             type=kindq, kind=kind, stack=S, situation=name, hero_hand=h,
             enonce=f"{base} Ta main : {hand_txt(h)}. {read} Que fais-tu ?",
             options=options_for(spec, r), bonne_reponse=ans, action_GTO=gto_ans, gain_mBB=g,
             seuil_bruit_mBB=round(1000 * noise), leak=('' if n == 0 else leak), intensite=lam, observations=n,
             profil=pname, regle=rule, niveau_donnees='A (stack résolu par HRC)' + ((' ; limp : EV estimée (décomposition de l\'EV HRC)' if spec.get('limp_estimate') else ' ; limp : borne basse HRC') if r['ev_limp'] is not None else ''),
             facteurs=fac, ev_jeu_vs_fold_mBB=round(1000 * float(r['ev_raw'][i])),
             ev_limp_vs_fold_mBB=(round(1000 * float(r['ev_limp'][i])) if r['ev_limp'] is not None else None),
             marge_mBB=round(1000 * margin(spec, r, i)),
             acceptables=acceptables(spec, r, i, noise), freq_gto_reponse_pct=round(100 * gto_freq(kind, S, spec, i, r['expl'][i]), 1),
             iso_pct=(round(r['iso_pct']) if r.get('iso_pct') is not None else None), iso_pct_gto=(round(r['iso_pct_gto']) if r.get('iso_pct_gto') is not None else None))
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
