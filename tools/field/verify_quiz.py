"""Vérification automatique du jeu de questions : structure, cohérence des explications, recalcul indépendant, simulation des formules d'EV."""
import json, re, sys
import numpy as np
import exploit_engine as ee
from hrcdata import NAMES, W
from pushfold import build_classes, eval7
from numba import njit

import os
qs = json.load(open(os.environ.get('EXPRESSO_QUIZ', 'quiz_field_v4_2.json')))
fails = []
def check(cond, msg, q=None):
    if not cond: fails.append((msg, q['id'] if q else None))

# ---------- 1) structure et cohérence du texte
for q in qs:
    check(q['bonne_reponse'] in q['options'], "bonne réponse absente des options", q)
    check(len(set(q['options'])) == len(q['options']), "options dupliquées", q)
    if q['type'] == 'profil':
        check(q['bonne_reponse'] in q['options'] and q['observations'] in (40, 80, 150), "question profil mal formée", q)
        check('Rec passif' in q['options'] and 'Reg' in q['options'], "v4.2 : rec passif et reg sont deux réponses distinctes", q); continue
    if q['type'] in ('adaptation', 'piège', 'inconnu', 'échantillon'):
        check(q['gain_mBB'] >= 0, "gain négatif", q)
        ev, evl = q['ev_jeu_vs_fold_mBB'], q.get('ev_limp_vs_fold_mBB')
        best = {'Fold': 0.0, 'Limp': evl}
        if 'limp du SB' in q['situation']:              # v4.2 : le BB face au limp, check ou tapis
            evc = q['ev_check_vs_fold_mBB']
            check(evc is not None and (ev >= evc if q['bonne_reponse'] == 'Pousser all-in' else evc >= ev), "limp du SB : la réponse n'est pas la meilleure action", q)
        elif q['bonne_reponse'] == 'Fold':
            check(ev < 0 and (evl is None or evl < 0), "réponse Fold mais une autre action a une EV >= 0", q)
        elif q['bonne_reponse'] == 'Limp':
            check(evl is not None and evl >= max(ev, 0), "réponse Limp mais le limp n'est pas la meilleure action", q)
        else:
            check(ev >= 0 and (evl is None or ev >= evl), "réponse de jeu mais une autre action est meilleure", q)
        check(f"Règle {q['regle']}" in q['explication'], "explication sans règle", q)
    if q['type'] in ('adaptation', 'inconnu'):
        check(q['bonne_reponse'] != q['action_GTO'], "adaptation sans changement de décision", q)
        mult = 3 if (q['action_GTO'] == 'Pousser all-in' and q['bonne_reponse'] == 'Fold') else 2
        if q['type'] == 'adaptation':
            check(q['gain_mBB'] >= mult * q['seuil_bruit_mBB'] - 1, f"gain sous {mult} x bruit", q)
    if q['type'] in ('piège', 'échantillon'):
        check(q['bonne_reponse'] == q['action_GTO'] or q['type'] == 'échantillon', "piège dont la décision change", q)
# v4 : contrôles propres aux corrections de l'audit
import profils_field as pf
for q in qs:
    if q['type'] in ('identification', 'profil'): continue
    check(not (q['hero_hand'] in pf.PREMIUM_PAIRS and 'Limp' in q['options'] and q['stack'] >= 6), "paire premium avec option limp (R8, exclue)", q)
    if q['bonne_reponse'] == 'Limp':
        check(q['facteurs'].get('limp') is True and q['profil'] not in ('Nit', 'Dégène', 'Reg'), "limp conseillé contre un profil qui ne limpe pas", q)
    check('marge_mBB' in q and (q['type'] in ('échantillon',) or q['marge_mBB'] >= 0), "marge d'EV absente ou négative", q)
    if q['type'] in ('adaptation', 'inconnu'):
        check(q['marge_mBB'] >= q['seuil_bruit_mBB'] - 1, "marge sur la 2e meilleure action sous 1 x bruit", q)
    if q['type'] == 'piège':
        check(q['marge_mBB'] >= 3 * q['seuil_bruit_mBB'] - 1, "piège dont la décision n'est pas nette (3 x bruit)", q)
    if q['type'] in ('adaptation', 'inconnu') and q['bonne_reponse'] == 'Fold':
        check(q['stack'] > 4, "fold exploitant à 4 BB ou moins (R5)", q)
        check(not (q['stack'] == 6 and 0 < q['observations'] < 40), "fold exploitant à 6 BB avec moins de 40 occasions", q)
    if q['type'] in ('adaptation', 'inconnu') and q['bonne_reponse'] == 'Limp':
        check(q['stack'] > 4, "limp exploitant à 4 BB ou moins", q)
    if q['regle'] == 'R11':
        check(q['profil'] == 'Reg' and q['bonne_reponse'] == q['action_GTO'], "R11 : contre un reg la réponse est le GTO", q)
    if q['observations'] in (20, 40, 80) or q['observations'] in (3, 5):
        check(f"{q['observations']} occasions" in q['enonce'] or f"Sur {q['observations']}" in q['enonce'], "nombre d'observations absent de l'énoncé", q)
# v4.2 : corrections de l'audit des coachs de la v4.1
import quiz_generator as qg
for q in qs:
    if q['type'] in ('identification', 'profil'): continue
    if q['type'] in ('adaptation', 'inconnu'):
        check(q['freq_gto_reponse_pct'] < 100 * qg.MIX_MAX, "v4.2 : HRC joue déjà la réponse 30 % du temps ou plus", q)
        check(not (q['stack'] <= 6 and q['situation'].startswith(('BB', 'SB face')) and q['bonne_reponse'] == 'Fold' and q['observations'] < 80), "v4.2 : R2 à 6 BB avec moins de 80 occasions", q)
    if q['type'] == 'piège':
        check(q['marge_mBB'] <= qg.TRAP_MAX_MARGIN * q['seuil_bruit_mBB'] + 1, "v4.2 : piège trivial (marge > 10 x bruit)", q)
        if q['regle'] == 'R9' and q['stats']:
            check(abs(q['stats'][0]['observed_pct'] - q['stats'][0]['gto_pct']) >= qg.TRAP_MIN_GAP - 0.05, "v4.2 : piège sans écart du vilain (< 5 points)", q)
    if q.get('ev_limp_vs_fold_mBB') is not None and q['type'] != 'échantillon':
        hu = q['kind'] == 'hu'
        check(('estimée' if hu else 'borne basse') in q['niveau_donnees'] and ('estimation' if hu else 'borne basse') in q['explication'], "v4.2 : nature de l'EV du limp indiquée", q)
    check(q['bonne_reponse'] not in q['acceptables'], "réponse listée parmi les alternatives", q)
print(f"1) structure et explications : {len(qs)} questions, {len(fails)} échec(s)")

# ---------- 2) recalcul : on rejoue le moteur avec les facteurs enregistrés et on compare la décision, le gain et l'EV
n_rec = 0; bad = 0
cache = {}
for q in qs:
    if q['type'] in ('identification', 'profil'): continue
    key = (q['kind'], q['situation'], q['stack'], q['facteurs']['shove'], q['facteurs']['call'], q['facteurs'].get('iso', 1.0), q['facteurs'].get('limp_k', 1.0), q['facteurs'].get('limp', True))
    if key not in cache:
        ee.PROFILES.clear(); ee.PROFILES['x'] = dict(shove=q['facteurs']['shove'], call=q['facteurs']['call'], iso=q['facteurs'].get('iso', 1.0), limp_k=q['facteurs'].get('limp_k', 1.0), limp=q['facteurs'].get('limp', True)); ee.INTENSITE = 1.0
        cache[key] = ee.run_spot(q['kind'], q['stack'], q['situation'], ee.SPOTS[(q['kind'], q['situation'])])['x']
    r = cache[key]; i = NAMES.index(q['hero_hand'])
    play = 'Payer' if ee.SPOTS[(q['kind'], q['situation'])]['type'] == 'call' else 'Pousser all-in'
    expl = {'paie': play, 'pousse': play, 'limpe': 'Limp', 'checke': 'Check'}.get(r['expl'][i], 'Fold')
    n_rec += 1
    if expl != q['bonne_reponse'] or abs(1000 * float(r['ev_raw'][i]) - q['ev_jeu_vs_fold_mBB']) > 1.0 or not r['valid'][i]:
        bad += 1; fails.append(("recalcul différent", q['id']))
print(f"2) recalcul avec les facteurs enregistrés : {n_rec - bad}/{n_rec} identiques")

# ---------- 3) simulation de parties réelles : décalage d'EV profil - GTO, formule contre simulation
combos, nc, names = build_classes()
@njit(cache=True)
def sim_decalage(hero, q_prof, q_gto, c_prof, c_gto, kind, S, N, seed):
    # kind 0 : BB face à l'all-in du SB (heads-up) ; 1 : BB face au BTN (SB fold) ; 2 : SB face au BTN (BB fold)
    np.random.seed(seed)
    cum_p = np.cumsum(q_prof) / q_prof.sum(); cum_g = np.cumsum(q_gto) / q_gto.sum()
    tot_p = 0.0; tot_g = 0.0
    cards = np.zeros(7, np.int64)
    for rep in range(2):
        cum = cum_p if rep == 0 else cum_g
        acc = 0.0; done = 0
        while done < N:
            j = np.searchsorted(cum, np.random.random())
            if j > 168: j = 168
            a = np.random.randint(nc[hero]); b = np.random.randint(nc[j])
            a0, a1 = combos[hero, a, 0], combos[hero, a, 1]; b0, b1 = combos[j, b, 0], combos[j, b, 1]
            if a0 == b0 or a0 == b1 or a1 == b0 or a1 == b1: continue
            used = np.zeros(52, np.bool_); used[a0] = used[a1] = used[b0] = used[b1] = True
            m = 0
            while m < 5:
                x = np.random.randint(52)
                if not used[x]:
                    used[x] = True; cards[2 + m] = x; m += 1
            cards[0] = a0; cards[1] = a1; sa = eval7(cards)
            cards[0] = b0; cards[1] = b1; sb = eval7(cards)
            s = 1.0 if sa > sb else (0.5 if sa == sb else 0.0)
            if kind == 0: v = S * (2 * s - 1) + 1.0
            elif kind == 1: v = s * (2 * S + 0.5) - S + 1.0
            else: v = s * (2 * S + 1.0) - S + 0.5
            acc += v; done += 1
        if rep == 0: tot_p = acc / N
        else: tot_g = acc / N
    return tot_p - tot_g

KIND = {"BB face à l'all-in du SB (BTN fold)": 0, "BB face à l'all-in du BTN (SB fold)": 1, "SB face à l'all-in du BTN": 2, "BB face à l'all-in du SB": 0}
rng = np.random.default_rng(5); diffs = []
for (kind, name), spec in ee.SPOTS.items():
    if spec['type'] != 'call': continue
    for S in (6, 10):
        ee.PROFILES.clear(); ee.PROFILES.update({'m': dict(shove=2.0, call=1.0), 'n': dict(shove=0.5, call=1.0)}); ee.INTENSITE = 1.0
        res = ee.run_spot(kind, S, name, spec)
        for pname in ('m', 'n'):
            r = res[pname]; idx = [i for i in np.where(r['valid'])[0]]
            for i in rng.choice(idx, 3, replace=False):
                sim = sim_decalage(int(i), (P_ := ee.P) * r['vec'], P_ * r['vec_gto'], r['vec'], r['vec_gto'], KIND[name], float(S), 500000, int(rng.integers(1e6)))
                q_p = ee.P * r['vec']; q_p /= q_p.sum(); q_g = ee.P * r['vec_gto']; q_g /= q_g.sum()
                form = ee.ev_call(spec['formula'], S, q_p)[i] - ee.ev_call(spec['formula'], S, q_g)[i]
                diffs.append((name, S, pname, NAMES[i], form, sim))
d = np.array([x[4] - x[5] for x in diffs])
se = np.array([np.sqrt(2) * 0.95 * x[1] / np.sqrt(500000) for x in diffs])      # erreur-type de l'écart simulé : écart-type d'un gain de partie ~ 0,95 x stack
z = d / se
print(f"3) simulation de parties réelles ({len(diffs)} cas de calls, 500 000 parties par distribution) : écart formule - simulation moyen {1000*d.mean():+.1f} mBB, maximum {1000*np.abs(d).max():.1f} mBB ; |écart| < 2 erreurs-types dans {100*np.mean(np.abs(z)<2):.0f} % des cas, maximum {np.abs(z).max():.1f} erreurs-types")
for S_ in (6, 10):
    dd = np.array([abs(x[4] - x[5]) for x in diffs if x[1] == S_]); print(f"   stack {S_} BB : écart absolu moyen {1000*dd.mean():.1f} mBB, maximum {1000*dd.max():.1f} mBB")
fails_total = len(fails)
print("\nÉCHECS :", fails_total)
for f in fails[:10]: print("  ", f)
