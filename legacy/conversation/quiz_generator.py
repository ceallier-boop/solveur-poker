"""Générateur de questions exploitantes : uniquement des cas où l'adaptation dépasse le bruit du moteur,
avec les statistiques du vilain affichées (pas de profil nommé), plus des questions « piège » sans adaptation."""
import json, csv, random, hashlib
import numpy as np
import exploit_engine as ee
from hrcdata import NAMES

SIT = {
 ('3w',"BB face à l'all-in du SB (BTN fold)"): "3 joueurs, {S} BB chacun. Le BTN fold et le SB pousse all-in. Tu es au BB.",
 ('3w',"BB face à l'all-in du BTN (SB fold)"): "3 joueurs, {S} BB chacun. Le BTN pousse all-in et le SB fold. Tu es au BB.",
 ('3w',"SB face à l'all-in du BTN"):           "3 joueurs, {S} BB chacun. Le BTN pousse all-in. Tu es au SB (le BB est derrière).",
 ('3w',"SB pousse (BTN fold) face au BB"):      "3 joueurs, {S} BB chacun. Le BTN fold. Tu es au SB, le BB est derrière.",
 ('3w',"BTN pousse face au SB et au BB"):       "3 joueurs, {S} BB chacun. Tu es au BTN, le SB et le BB sont derrière.",
 ('hu',"BB face à l'all-in du SB"):             "Heads-up, {S} BB chacun. Le SB pousse all-in. Tu es au BB.",
 ('hu',"SB pousse face au BB"):                 "Heads-up, {S} BB chacun. Tu es au SB (bouton), le BB est derrière.",
}
LEAKS = {   # (type de spot, sens) -> phrase
 ('call', +1): "pousse trop souvent", ('call', -1): "ne pousse pas assez",
 ('shove', +1): "paie trop souvent", ('shove', -1): "ne paie pas assez",
}
LEAK_OPTIONS = ["Il pousse trop souvent", "Il ne pousse pas assez", "Il paie trop souvent", "Il ne paie pas assez"]
LEAK_ANS = {('call', +1): 0, ('call', -1): 1, ('shove', +1): 2, ('shove', -1): 3}


def hand_txt(h):
    if len(h) == 2: return f"{h} (paire)"
    return f"{h[:2]} {'assortis' if h[2]=='s' else 'dépareillés'}"


def stat_line(spec, r, S):
    if spec['type'] == 'call':
        return f"Ce vilain pousse {r['vill_freq']:.0f} % de ses mains dans cette situation (GTO : {r['vill_freq_gto']:.0f} %)."
    if r.get('vill_freq2') is not None:
        return (f"Ce vilain paie {r['vill_freq']:.0f} % des all-in au SB (GTO : {r['vill_freq_gto']:.0f} %) "
                f"et {r['vill_freq2']:.0f} % au BB quand le SB fold (GTO : {r['vill_freq2_gto']:.0f} %).")
    return f"Ce vilain paie {r['vill_freq']:.0f} % des all-in dans cette situation (GTO : {r['vill_freq_gto']:.0f} %)."


def make(seed=11, max_adapt=2, control_per=1):
    rnd = random.Random(seed); qs = []
    for lam in (1.0, 0.5):
        ee.INTENSITE = lam
        for (kind, name), spec in ee.SPOTS.items():
            for S in (4, 6, 8, 10, 12):
                res = ee.run_spot(kind, S, name, spec)
                if res is None: continue
                noise = ee.NOISE_BB[S]
                shark = [v for k, v in res.items() if k.startswith('Shark')][0]
                inconsistent = shark['valid'] & (shark['gto'] != shark['expl'])        # la décision change même contre le vilain GTO : base HRC incohérente
                for pname, r in res.items():
                    if pname.startswith('Shark'): continue
                    valid = r['valid']; gain = np.where(valid, r['ev_expl'] - r['ev_gto'], 0.0)
                    flip = valid & (r['gto'] != r['expl'])
                    strong = [i for i in np.where(flip)[0] if gain[i] >= 2 * noise and not inconsistent[i]]
                    robust = [i for i in np.where(valid & ~flip)[0] if abs(r['ev_raw'][i]) >= 3 * noise and not inconsistent[i]]
                    sgn = 1 if r['vill_freq'] > r['vill_freq_gto'] else -1
                    gap = abs(r['vill_freq'] - r['vill_freq_gto'])
                    leak = LEAKS[(spec['type'], sgn)]
                    play = 'Payer' if spec['type'] == 'call' else 'Pousser all-in'
                    for kindq, pool, nmax in (('adaptation', strong, max_adapt), ('piège', robust, control_per)):
                        if not pool: continue
                        for i in rnd.sample(pool, min(nmax, len(pool))):
                            h = NAMES[i]
                            ge, ex = r['gto'][i], r['expl'][i]
                            ans = play if ex in ('paie', 'pousse') else 'Fold'
                            gto_ans = play if ge in ('paie', 'pousse') else 'Fold'
                            q = dict(id=f"{kind}-{S}-"+hashlib.md5(f'{name}|{pname}|{lam}|{h}'.encode()).hexdigest()[:6], type=kindq, kind=kind, stack=S, situation=name, hero_hand=h,
                                     enonce=f"{SIT[(kind,name)].format(S=S)} Ta main : {hand_txt(h)}. {stat_line(spec, r, S)} Que fais-tu ?",
                                     options=[play, 'Fold'], bonne_reponse=ans, action_GTO=gto_ans, gain_mBB=round(1000 * float(gain[i]), 0),
                                     seuil_bruit_mBB=round(1000 * noise), leak=leak, intensite=lam, niveau_donnees='A (stack résolu par HRC)',
                                     facteurs=dict(shove=round(ee.PROFILES[pname]['shove'] ** lam, 4), call=round(ee.PROFILES[pname]['call'] ** lam, 4)))
                            evp = 1000 * float(r['ev_raw'][i])                                   # EV de l'action de jeu par rapport au fold
                            q['ev_jeu_vs_fold_mBB'] = round(evp, 0)
                            verbe = 'payer' if spec['type'] == 'call' else 'pousser'
                            if evp >= 0: etat = f"{verbe} rapporte {evp:+.0f} mBB par rapport au fold"
                            else: etat = f"{verbe} serait à {evp:.0f} mBB par rapport au fold"
                            if kindq == 'adaptation':
                                q['explication'] = (f"Le vilain {leak}. Contre lui, {ans.lower()} est meilleur que l'action GTO ({gto_ans.lower()}) de {q['gain_mBB']:.0f} mBB : {etat}. "
                                                    f"Cet écart dépasse le bruit de calcul ({q['seuil_bruit_mBB']} mBB) : l'adaptation est réelle.")
                                q['difficulte'] = 'facile' if gain[i] >= 4 * noise else 'moyen'
                            else:
                                q['explication'] = (f"Piège : même contre ce vilain, {ans.lower()} reste la meilleure action : {etat}. "
                                                    f"Ne change pas de stratégie quand l'écart de fréquence ne retourne pas la décision.")
                                q['difficulte'] = 'piège'
                            qs.append(q)
                            # question d'identification du défaut
                            if kindq == 'adaptation' and gap >= 3 and rnd.random() < 0.5:
                                qs.append(dict(id=q['id']+'-leak', type='identification', kind=kind, stack=S, situation=name, hero_hand=h,
                                               enonce=f"{SIT[(kind,name)].format(S=S)} {stat_line(spec, r, S)} Quel est le défaut de ce vilain ?",
                                               options=LEAK_OPTIONS, bonne_reponse=LEAK_OPTIONS[LEAK_ANS[(spec['type'], sgn)]], intensite=lam,
                                               explication=f"Sa fréquence ({'supérieure' if sgn>0 else 'inférieure'} au GTO) montre qu'il {leak}.", difficulte='facile', niveau_donnees='A (stack résolu par HRC)'))
    # dédoublonnage : une question par (type, situation, stack, main, défaut) ; à égalité, l'intensité la plus forte
    best = {}
    for q in qs:
        k = (q['type'], q['kind'], q['situation'], q['stack'], q['hero_hand'], q.get('leak', q['bonne_reponse']))
        if k not in best or q['intensite'] > best[k]['intensite']:
            best[k] = q
    out = list(best.values())
    # les pièges représentent au plus la moitié du nombre d'adaptations, tirés au hasard par (type de partie, stack)
    ad = [q for q in out if q['type'] == 'adaptation']; tr = [q for q in out if q['type'] == 'piège']; other = [q for q in out if q['type'] not in ('piège',)]
    rnd.shuffle(tr); out = other + tr[:max(1, len(ad) // 2)]
    seen = set(); res = []
    for q in out:
        if q['id'] in seen: continue
        seen.add(q['id']); res.append(q)
    return res


if __name__ == '__main__':
    qs = make()
    json.dump(qs, open('/home/claude/quiz_exploit.json', 'w'), ensure_ascii=False, indent=1)
    keys = ['id','type','difficulte','kind','stack','situation','hero_hand','enonce','options','bonne_reponse','action_GTO','gain_mBB','seuil_bruit_mBB','leak','intensite','niveau_donnees','explication']
    with open('/home/claude/quiz_exploit.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader()
        for q in qs:
            q2 = dict(q); q2['options'] = ' | '.join(q['options']); w.writerow(q2)
    import collections
    print(len(qs), 'questions')
    print(collections.Counter(q['type'] for q in qs), collections.Counter(q['difficulte'] for q in qs))
    print(collections.Counter(q['stack'] for q in qs))
