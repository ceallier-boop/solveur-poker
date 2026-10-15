"""Échantillon stratifié de questions pour la relecture experte (évaluation du MVP, remarque 14).

Usage : python tools/audit/expert_sample.py <dossier de sortie> [--n 300] [--seed 14]

Strates : mode (GTO, exploitant), format, situation, position, profondeur, source de l'EV. Chaque strate non vide a au
moins une question ; le reste est réparti selon la racine carrée de sa taille (les petites strates ne sont pas noyées).
Dans une strate, la main est tirée comme dans l'application (mains retenues, poids d'atteinte en racine carrée), en
visant trois types de cas : décision nette, décision serrée (une autre action à moins de 0,1 BB : nuance « pertinente »)
et stratégie mixte (au moins deux actions jouées 10 % ou plus).

Produit, pour chaque question : l'énoncé, les options, l'EV de chaque option, le verdict qu'en donne l'application, la
correction affichée quand on joue la référence et quand on fait l'erreur la plus tentante (avec la règle à retenir).
  questions.md         lecture humaine ou IA, une fiche par question
  lots/                les mêmes fiches par lots de 50, chacune avec sa grille de réponse
  questions.jsonl      même contenu, une question par ligne (lecture automatique)
  questions.csv        même contenu, une ligne par question (tableur)
  reponses_modele.csv  grille de réponse à remplir par chaque expert (une ligne par question)
  CONSIGNES.md         consignes communes aux experts, avec les questions générales (seuils, profils, règles)
Le dossier ne contient aucun export HRC brut ; il contient des EV dérivées d'HRC (droits à clarifier avant diffusion
hors de l'équipe : voir docs/produit/PLAN_EVALUATION_MVP_2026-10-14.md, remarque 27).
"""
import argparse, collections, csv, datetime, json, math, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy import grading, profiles, progress, quiz  # noqa: E402
from spinsacademy.cards import NAMES, W  # noqa: E402
from spinsacademy.hrc import ROOT  # noqa: E402

CASES = (('serree', 0.20), ('mixte', 0.15), ('nette', 0.65))      # parts visées des types de cas
CASE_FR = {'nette': 'décision nette', 'serree': 'décision serrée (autre action à moins de 0,1 BB)', 'mixte': 'stratégie mixte'}
FEEDBACK = ['id', 'expert', 'reference_ok', 'action_attendue', 'verdicts_ok', 'verdict_conteste', 'correction_ok', 'regle_ok',
            'gravite', 'commentaire']


def stratum(sp):
    return ('exploitant' if sp.get('villain') else 'GTO', sp['table'], quiz.family(sp), sp['hero'],
            progress.depth_of(quiz.hero_effective(sp)), sp['ev_reference'])


def case_of(sp, h):
    ev = grading.reference_ev(sp, h); top = max(ev)
    if sum(1 for _, p in grading.displayed_mix(sp, h) if p >= 10) >= 2: return 'mixte'
    if sorted(ev)[-2] >= top - grading.PERTINENT_MBB / 1000 and len(ev) > 1: return 'serree'
    return 'nette'


def allocate(sizes, n):
    keys = sorted(sizes); base = {k: 1 for k in keys}; left = n - len(keys)
    if left < 0: raise SystemExit(f'{len(keys)} strates pour {n} questions : augmenter --n')
    w = {k: math.sqrt(sizes[k]) for k in keys}; tot = sum(w.values())
    raw = {k: left * w[k] / tot for k in keys}
    for k in keys: base[k] += int(raw[k])
    for k in sorted(keys, key=lambda k: raw[k] - int(raw[k]), reverse=True)[:n - sum(base.values())]: base[k] += 1
    return base


def sample(n, seed):
    rnd = random.Random(seed); items = collections.defaultdict(list); refs = {}
    for ref in (quiz.DEFAULT_VERSION, quiz.DEFAULT_EXPLOIT):
        for sp in quiz.pool(ref):
            hs = sorted(quiz.teachable(sp))
            if hs: items[stratum(sp)].append((ref, sp, hs)); refs[sp['spot_id']] = ref
    quota = allocate({k: sum(len(hs) for *_, hs in v) for k, v in items.items()}, n)
    want = [c for c, share in CASES for _ in range(round(share * n))]; rnd.shuffle(want)
    out, used_spots = [], set()
    for k in sorted(quota):
        spots = items[k][:]; rnd.shuffle(spots)
        for i in range(quota[k]):
            target = want[len(out) % len(want)]
            pick = None
            for ref, sp, hs in sorted(spots, key=lambda x: x[1]['spot_id'] in used_spots):   # d'abord des spots pas encore pris
                cand = [h for h in hs if case_of(sp, h) == target]
                if cand: pick = (ref, sp, cand); break
            if pick is None: ref, sp, hs = spots[i % len(spots)]; pick = (ref, sp, hs)
            ref, sp, hs = pick
            wts = [W[NAMES.index(h)] * sp['hands'][h]['reach'] ** 0.5 for h in hs]
            taken = {(o['spot_id'], o['hand']) for o in out}
            free = [(h, w) for h, w in zip(hs, wts) if (sp['spot_id'], h) not in taken] or list(zip(hs, wts))
            h = rnd.choices([x for x, _ in free], [w for _, w in free])[0]
            out.append(dict(ref=ref, spot_id=sp['spot_id'], hand=h, stratum=k, case=case_of(sp, h))); used_spots.add(sp['spot_id'])
    rnd.shuffle(out)
    return out


def describe(i, x):
    ref, sid, h = x['ref'], x['spot_id'], x['hand']
    _, spots = quiz.load(ref); sp = spots[sid]
    labels = {a['id']: quiz.action_label(sp, a) for a in sp['actions']}; ids = list(labels)
    ev = grading.reference_ev(sp, h); best = quiz.reference_action(sp, h)
    grades = {a: grading.grade(sp, h, a) for a in ids}
    mix = dict(grading.displayed_mix(sp, h))
    errs = sorted((a for a in ids if grades[a]['verdict'] == 'erreur'), key=lambda a: grades[a]['regret_mbb'])
    tempting = errs[0] if errs else None
    r_best = quiz.correct(ref, sid, h, best)
    r_err = quiz.correct(ref, sid, h, tempting) if tempting else None
    pr = profiles.for_villain(sp.get('villain'))
    v = sp.get('villain')
    return dict(
        id=f'Q{i + 1:03d}', mode=x['stratum'][0], dataset=ref, spot_id=sid, main=h, type_de_cas=CASE_FR[x['case']],
        format=sp['table'], position=sp['hero'], situation=quiz.SITUATION_FR[quiz.family(sp)],
        tapis_bb=' / '.join(f"{p} {s:g}" for p, s in zip(sp['players'], sp['stacks_bb'])), tapis_effectif_bb=f'{quiz.hero_effective(sp):g}',
        arbre_preflop=sp.get('preflop_tree', ''), source_ev=sp['ev_reference'],
        profil=(f"{pr['name_fr']} : part à tapis avec {quiz.bb(v['observed_pct'])} % de ses mains (équilibre push/fold : {quiz.bb(v['gto_pct'])} %)" if pr else ''),
        enonce=quiz.prompt(sp, h),
        options=[dict(action=labels[a], ev_bb=round(ev[j], 3), frequence_reference_pct=mix.get(a, 0),
                      ecart_bb=round(grades[a]['regret_mbb'] / 1000, 3), verdict_application=grades[a]['verdict'])
                 for j, a in enumerate(ids)],
        reference=labels[best],
        correction_si_reference=r_best['explanation_fr'],
        erreur_la_plus_tentante=(labels[tempting] if tempting else ''),
        correction_si_erreur=(r_err['explanation_fr'] if r_err else ''))


def md(q):
    t = [f"## {q['id']} · {q['mode']} · {q['format']} · {q['position']} {q['situation']} · {q['tapis_effectif_bb']} BB · {q['main']}", '',
         f"Type : {q['type_de_cas']} · EV : {'exacte (tout le monde à tapis)' if q['source_ev'] == 'exact' else 'HRC' if q['source_ev'] == 'hrc' else q['source_ev']}"
         f" · tapis {q['tapis_bb']}" + (f" · arbre {q['arbre_preflop']}" if q['arbre_preflop'] else ''), '']
    if q['profil']: t += [f"Profil adverse (fictif) : {q['profil']}", '']
    t += [f"**Énoncé** : {q['enonce']}", '', '| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l\'application |', '|---|---|---|---|---|']
    t += [f"| {o['action']} | {o['ev_bb']:+.3f} | {o['frequence_reference_pct']} % | {o['ecart_bb']:.3f} | {o['verdict_application']} |" for o in q['options']]
    t += ['', f"**Référence de l'application** : {q['reference']}", '', '**Correction affichée si le joueur joue la référence**', '',
          *[f"> {l}" for l in q['correction_si_reference'].split('\n')], '']
    if q['erreur_la_plus_tentante']:
        t += [f"**Correction affichée si le joueur joue « {q['erreur_la_plus_tentante']} » (erreur la plus tentante)**", '',
              *[f"> {l}" for l in q['correction_si_erreur'].split('\n')], '']
    return '\n'.join(t)


CONSIGNES = """# Relecture experte de SpinsAcademy : consignes

Échantillon du {date}, commit `{commit}`, datasets `{gto}` et `{exp}`. {n} questions (identifiants Q001 à Q{n:03d}).

## Ton rôle

Tu es un joueur expert d'Expresso / Spin & Go (3 joueurs puis heads-up, 4 à 25 BB, préflop, **chip EV**, sans ICM).
Tu relis des questions d'entraînement produites par l'application et tu dis si la **référence**, les **verdicts** et les
**textes de correction** sont justes. Tu travailles seul : ne te concerte pas avec les autres relecteurs, l'accord entre
relecteurs est mesuré ensuite.

## Ce que fait l'application (à juger, pas à refaire)

- Référence : stratégie d'équilibre calculée par HoldemResources Calculator (HRC), ou EV exacte quand tout le monde est
  à tapis. En mode exploitant : meilleure réponse contre un profil fictif dont la fréquence de tapis (ou de call, pour
  la Station d'appel) est déformée par rapport à l'équilibre push/fold, en EV exacte.
- EV en BB, en chip EV. Les EV HRC sont des estimations (Monte-Carlo) : un bruit d'environ 0,1 BB par main et par action
  a été mesuré. C'est pourquoi une action à moins de 0,1 BB de la meilleure est jugée « pertinente ».
- Verdicts :
  - **correct** : écart à la meilleure action ≤ 0,02 BB, ou action jouée au moins 10 % du temps par la référence ;
  - **imprécision** : écart entre 0,02 et 0,06 BB, ou (EV HRC) entre 0,06 et 0,1 BB : la correction garde la référence et
    ajoute une « nuance : … est aussi pertinente » ;
  - **erreur** : au-delà.
- Points : correct 1, imprécision 0,5, erreur 0.
- Après une erreur ou une imprécision, une ligne « À retenir » résume la range de la référence en règle à seuils
  (« 22+, A2+, K7s+ ») ; elle annonce la part des mains qu'elle classe bien.

## Pour chaque question

Les questions sont dans `questions.md`, ou par lots de 50 dans `lots/` (chaque lot a sa grille `…_reponses.csv`).
Remplis une ligne de la grille par question (séparateur `;`, ne change ni l'ordre des lignes ni celui des colonnes ;
réponds en CSV brut, sans mise en forme) :

| Colonne | Valeurs | Sens |
|---|---|---|
| `id` | Q001… | déjà rempli |
| `expert` | ton nom de relecteur (ex. `expert_A`) | |
| `reference_ok` | `oui` / `non` / `incertain` | la référence de l'application est-elle la bonne décision en chip EV ? |
| `action_attendue` | libellé d'une option | seulement si `reference_ok` = `non` |
| `verdicts_ok` | `oui` / `non` | les verdicts des options sont-ils raisonnables ? |
| `verdict_conteste` | `option : verdict attendu` | seulement si `verdicts_ok` = `non` (plusieurs séparés par ` | `) |
| `correction_ok` | `oui` / `non` | les textes sont-ils justes, compréhensibles par un joueur amateur, sans affirmation fausse ? |
| `regle_ok` | `oui` / `non` / `sans objet` | la ligne « À retenir » est-elle juste et utile ? (sans objet si absente) |
| `gravite` | `bloquant` / `majeur` / `mineur` / `aucun` | bloquant : apprend une décision fausse ; majeur : texte faux ou trompeur ; mineur : formulation |
| `commentaire` | texte libre court | ce qui est faux et ce qu'il faudrait dire |

Règles de jugement :
- Juge en **chip EV**, préflop, sans lecture d'adversaire réel. Ne pénalise pas l'absence d'ICM.
- Une décision serrée (écart < 0,1 BB) n'est pas une erreur de l'application si elle choisit l'une ou l'autre : juge
  surtout si le texte le dit honnêtement.
- En mode exploitant, le profil est une **hypothèse** : juge la meilleure réponse contre la range annoncée, pas le réalisme du profil
  (c'est la question générale 3).
- Si tu n'es pas sûr, réponds `incertain` plutôt que de deviner.

## Questions générales (une réponse argumentée chacune, dans `questions_generales.md`)

1. **Seuils de verdict** : 0,02 BB (correct), 0,06 BB (imprécision), 0,1 BB (action pertinente pour une EV HRC). Sont-ils
   adaptés à 4-25 BB ? Faut-il des seuils différents selon la profondeur ou le format ?
2. **Stratégies mixtes** : une action jouée au moins 10 % du temps par la référence est acceptée. Seuil adapté ?
3. **Profils fictifs** : Serré = cote de tapis × 0,5 ; Prudent × 0,7 ; Agressif × 1,4 ; Maniaque × 2 (fréquence p devient
   k·p / (1 + (k − 1)·p)) ; Station d'appel = cote de call × 2 face au tapis du SB (le joueur pousse ou se couche). Ces écarts correspondent-ils à des joueurs qu'on rencontre en Expresso ? Les fourchettes de
   reconnaissance (Serré sous × 0,59, Prudent × 0,59 à 0,84, Agressif × 1,18 à 1,67, Maniaque au-delà) sont-elles utiles ?
   La fiche « Reconnaître ce profil » (signes observables, nombre d'occasions nécessaire) est-elle juste et prudente ?
4. **Règles à retenir** : sur l'ensemble des questions, sont-elles assez simples et assez justes pour être mémorisées ?
   Proposer de meilleures formulations pour les situations les plus fréquentes.
5. **Ce qui manque** : situations, tailles d'ouverture ou explications dont un joueur d'Expresso aurait besoin.

## Répartition de l'échantillon

{strata}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--n', type=int, default=300); ap.add_argument('--seed', type=int, default=14)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    qs = [describe(i, x) for i, x in enumerate(sample(a.n, a.seed))]
    with open(os.path.join(a.out, 'questions.jsonl'), 'w') as f:
        for q in qs: f.write(json.dumps(q, ensure_ascii=False) + '\n')
    with open(os.path.join(a.out, 'questions.md'), 'w') as f:
        f.write(f"# SpinsAcademy : {len(qs)} questions à relire\n\nConsignes : `CONSIGNES.md`. Réponses : `reponses_modele.csv`.\n\n")
        f.write('\n\n'.join(md(q) for q in qs) + '\n')
    lot = 50; os.makedirs(os.path.join(a.out, 'lots'), exist_ok=True)              # par lots de 50 : une conversation par lot pour un relecteur IA
    for k in range(0, len(qs), lot):
        part = qs[k:k + lot]; name = f"questions_{k + 1:03d}-{k + len(part):03d}"
        with open(os.path.join(a.out, 'lots', name + '.md'), 'w') as f:
            f.write(f"# SpinsAcademy : questions {part[0]['id']} à {part[-1]['id']}\n\nConsignes : `CONSIGNES.md`.\n\n" + '\n\n'.join(md(q) for q in part) + '\n')
        with open(os.path.join(a.out, 'lots', name + '_reponses.csv'), 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, FEEDBACK, delimiter=';'); w.writeheader(); w.writerows({'id': q['id']} for q in part)
    flat = [dict({k: v for k, v in q.items() if k != 'options'},
                 options=' | '.join(f"{o['action']} : EV {o['ev_bb']:+.3f}, réf. {o['frequence_reference_pct']} %, écart {o['ecart_bb']:.3f}, {o['verdict_application']}" for o in q['options']))
            for q in qs]
    with open(os.path.join(a.out, 'questions.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, list(flat[0]), delimiter=';'); w.writeheader(); w.writerows(flat)
    with open(os.path.join(a.out, 'reponses_modele.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, FEEDBACK, delimiter=';'); w.writeheader(); w.writerows({'id': q['id']} for q in qs)
    cnt = lambda key: collections.Counter(key(q) for q in qs)
    strata = '\n'.join(f"- {name} : " + ', '.join(f"{k} {v}" for k, v in sorted(cnt(fn).items())) for name, fn in (
        ('Mode', lambda q: q['mode']), ('Format', lambda q: q['format']), ('Position', lambda q: q['position']),
        ('Situation', lambda q: q['situation']), ('Profondeur', lambda q: progress.depth_of(float(q['tapis_effectif_bb']))),
        ('Source de l\'EV', lambda q: q['source_ev']), ('Type de cas', lambda q: q['type_de_cas']),
        ('Verdict de l\'erreur la plus tentante', lambda q: 'avec erreur' if q['erreur_la_plus_tentante'] else 'sans erreur')))
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    with open(os.path.join(a.out, 'CONSIGNES.md'), 'w') as f:
        f.write(CONSIGNES.format(date=datetime.date.today().isoformat(), commit=commit, gto=quiz.DEFAULT_VERSION, exp=quiz.DEFAULT_EXPLOIT, n=len(qs), strata=strata))
    with open(os.path.join(a.out, 'questions_generales.md'), 'w') as f:
        f.write('# Questions générales : réponses de <expert>\n\n' + '\n\n'.join(f'## {i}. {t}\n\n' for i, t in enumerate(
            ['Seuils de verdict', 'Stratégies mixtes', 'Profils fictifs', 'Règles à retenir', 'Ce qui manque'], 1)))
    print(f"{len(qs)} questions dans {a.out}\n{strata}")


if __name__ == '__main__':
    main()
