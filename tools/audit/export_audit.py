"""Dossier d'audit : contenu lisible (CSV), code du moteur, datasets complets.

Usage : python tools/audit/export_audit.py <dossier de sortie>

Produit :
  - SpinsAcademy_audit_contenu.zip : une ligne par question tirable (GTO et exploitant), avec l'énoncé, les options,
    la stratégie de référence, les EV, le verdict de chaque option et la correction complète quand on joue l'action de
    référence ; le lexique, les profils postflop ; un guide de lecture.
  - SpinsAcademy_code_moteur.zip : le code (spinsacademy/, tools/, tests/), la documentation et les données de calcul
    embarquées (matrice d'équités, profils postflop), sans les exports de référence bruts ni les datasets.
  - SpinsAcademy_datasets.zip : toutes les versions de data/datasets (spots.jsonl et manifest.json), publiées ou non.
Les exports de référence bruts (data/hrc/raw) ne sont pas inclus : ils restent dans le dépôt.
"""
import csv, io, json, os, subprocess, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy import field, grading, quiz  # noqa: E402
from spinsacademy.hrc import ROOT  # noqa: E402

COLS = ['mode', 'spot_id', 'jeu_de_donnees', 'table', 'tapis_bb', 'position', 'tapis_effectif_bb', 'famille', 'arbre_preflop', 'ouvertures',
        'historique', 'main', 'options', 'strategie_affichee', 'action_reference', 'action_plus_rentable', 'source_ev',
        'ev_par_action_bb', 'verdict_par_option', 'difficulte', 'correction', 'pourquoi', 'apres_le_flop']


def rows(ref):
    _, spots = quiz.load(ref)
    for sp in quiz.pool(ref):
        labels = {a['id']: quiz.action_label(sp, a) for a in sp['actions']}; ids = list(labels)
        for h in quiz.teachable(sp):
            ev = grading.reference_ev(sp, h); top = ids[max(range(len(ev)), key=lambda k: ev[k])]
            best = quiz.reference_action(sp, h)
            r = quiz.correct(ref, sp['spot_id'], h, best)
            verdicts = {labels[a]: grading.grade(sp, h, a)['verdict'] for a in ids}
            n = r['next']
            after = '' if not n else '\n'.join(x for x in [n['intro'], n['position'] or ''] + [f"+ {f}" for f in n['forces']] + [f"- {w}" for w in n['weaknesses']] if x)
            yield dict(mode='GTO', spot_id=sp['spot_id'], jeu_de_donnees=ref, table=sp['table'], tapis_bb=' / '.join(f'{x:g}' for x in sp['stacks_bb']),
                       position=sp['hero'], tapis_effectif_bb=f'{quiz.hero_effective(sp):g}', famille=quiz.family(sp),
                       arbre_preflop=sp.get('preflop_tree', ''), ouvertures=json.dumps(sp.get('open_sizes') or {}, ensure_ascii=False),
                       historique=' ; '.join(quiz.history_text(sp)) or 'personne n\'a parlé', main=h,
                       options=' | '.join(labels.values()),
                       strategie_affichee=' | '.join(f"{labels[a]} {p} %" for a, p in grading.displayed_mix(sp, h)),
                       action_reference=labels[best], action_plus_rentable=labels[top], source_ev=sp['ev_reference'],
                       ev_par_action_bb=' | '.join(f"{labels[a]} {e:+.3f}" for a, e in zip(ids, ev)),
                       verdict_par_option=' | '.join(f'{k} : {v}' for k, v in verdicts.items()),
                       difficulte=quiz.difficulty(quiz.lesson_gap(sp, h)) or '',
                       correction=r['core_fr'] or r['explanation_fr'], pourquoi='\n'.join(r['why_fr']), apres_le_flop=after)


FCOLS = ['mode', 'id', 'jeu_de_donnees', 'type', 'table', 'position', 'tapis_bb', 'situation', 'main', 'enonce', 'options', 'reponse', 'action_theorique',
         'ev_par_option_bb', 'regle', 'correction', 'pourquoi', 'gerer_le_postflop']


def field_rows(ref):
    """mode exploitant : une ligne par question fixe, correction de la bonne réponse"""
    _, spots = quiz.load(ref)
    for sp in spots.values():
        f = sp['field']; h = next(iter(sp['hands'])); r = field.correct(sp, f['correct']); n = r['next']
        lab = {o['id']: field._label(sp, o['id']) for o in f['options']}
        yield dict(mode='Exploitant', id=sp['spot_id'], jeu_de_donnees=ref, type=f['type_fr'], table=sp['table'], position=sp['hero'],
                   tapis_bb=f"{sp['effective_stack_bb']:g}", situation=f['situation'], main=h, enonce=sp['prompt_fr'], options=' | '.join(lab.values()),
                   reponse=lab[f['correct']], action_theorique=lab[f['gto']] if f['gto'] else '',
                   ev_par_option_bb=' | '.join(f"{lab[o['id']]} {o['ev_mbb'] / 1000:+.3f}" for o in f['options'] if o['ev_mbb'] is not None),
                   regle=f"{f['rule']} : {r['field']['rule_fr']}", correction=r['explanation_fr'], pourquoi='\n'.join(r['why_fr']),
                   gerer_le_postflop='' if not n else '\n'.join([n['intro'], n['position']] + [f"+ {x}" for x in n['forces']] + [f"- {x}" for x in n['weaknesses']]))


def csv_bytes(it, cols):
    buf = io.StringIO(); w = csv.DictWriter(buf, cols, delimiter=';'); w.writeheader(); n = 0
    for x in it: w.writerow(x); n += 1
    return ('﻿' + buf.getvalue()).encode('utf-8'), n          # BOM : Excel lit l'UTF-8 et les accents


GUIDE = """# Dossier d'audit SpinsAcademy

Généré le {date} depuis le commit `{commit}` (branche de développement).

## Contenu de ce dossier (`SpinsAcademy_audit_contenu.zip`)

| Fichier | Contenu |
|---|---|
| `questions_gto.csv` | {n_gto} questions tirables du dataset GTO `{gto}` (une ligne par situation × main) |
| `questions_exploitant.csv` | {n_exp} questions tirables du dataset exploitant `{exp}` |
| `lexique.csv` | les {n_lex} termes du lexique affiché dans l'application |
| `profils_postflop.json` | fréquences au flop par classe de main (énumération exacte des 19 600 flops) |
| `notation.md` | les règles de notation et de tirage appliquées |

Les CSV sont en UTF-8, séparateur « ; » (ouverture directe dans Excel ou LibreOffice). Une cellule peut contenir plusieurs lignes.

## Colonnes des questions

- `mode`, `spot_id`, `jeu_de_donnees` : identification ; `spot_id` permet de retrouver la situation dans `spots.jsonl`.
- `table`, `tapis_bb` (dans l'ordre BTN / SB / BB, ou SB / BB en heads-up), `position` du joueur, `tapis_effectif_bb` (le plus petit entre son tapis et le plus gros tapis adverse encore en jeu), `famille` (premier à parler, face à un limp, à une relance, à un tapis).
- `arbre_preflop`, `ouvertures` : arbre de référence d'origine et ses tailles d'ouverture (`daa9aaa0` = arbre de référence, BTN 2,3 BB, SB 3,5 BB).
- `historique`, `main`, `options` : ce que voit le joueur (mode exploitant : `enonce`).
- `strategie_affichee` : la stratégie de référence telle qu'affichée (actions jouées au moins 10 % du temps, arrondies à 5 %).
- `action_reference` : l'action présentée comme référence ; `action_plus_rentable` : l'action d'EV maximale (elles diffèrent quand l'action la plus jouée vaut l'EV maximale à 0,06 BB près).
- `source_ev` : `exact` (calcul exact, calls et tapis à deux joueurs) ou `hrc` ; `ev_par_action_bb` : EV de chaque option, relative au fold (ou au check), en BB.
- `verdict_par_option` : le verdict que recevrait chaque option (bonne réponse, imprécision, erreur).
- `difficulte` : facile, moyen, difficile (coût de la moins chère des réponses fausses).
- `correction`, `pourquoi`, `apres_le_flop` : les textes affichés quand le joueur choisit l'action de référence (les textes des autres choix ne diffèrent que par les lignes sur le choix du joueur).

## Les deux autres archives

- `SpinsAcademy_code_moteur.zip` : tout le code (moteur de correction `spinsacademy/grading.py`, tirage et textes `spinsacademy/quiz.py`, import de référence `importer.py`, EV exactes `allin.py`, équilibre push/fold `pushfold.py`, mode exploitant `field.py` (moteur : `tools/field/`), API `api.py`, solveur maison `solver/` et `postflop/`, interface `web/`), les tests (`tests/`, `python -m pytest`), les outils et la documentation (`docs/`, dont `docs/audit/RELECTURES_2026-10-13.md`).
- `SpinsAcademy_datasets.zip` : toutes les versions des datasets (`gto_preflop/<version>/` et `exploit_field/<version>/`, chacune avec `manifest.json` et `spots.jsonl`). Versions publiées : `{gto}` et `{exp}`. Format : `docs/dataset/FORMAT_SPOT.md` et `docs/dataset/EXPLOIT_CALLS.md`.

Les exports de référence bruts ne sont pas dans ce dossier : ils restent dans le dépôt (`data/hrc/raw`, inventaire `data/hrc/README.md`).
"""

NOTATION = """# Règles de notation et de tirage

- Regret = EV de l'action la plus rentable − EV de l'action choisie, sur l'EV de référence du spot (exacte si chaque action autre que fold en a une, sinon de référence).
- Bonne réponse : regret ≤ {tol} mBB, ou action jouée au moins {mix} % du temps par la stratégie de référence. Imprécision : regret ≤ {imp} mBB. Erreur : au-delà. Points 1 / 0,5 / 0.
- En EV exacte, la stratégie de référence est l'action la plus rentable (stratégie pure) ; ailleurs, les fréquences de référence.
- Une main n'est proposée que si elle atteint le nœud (poids ≥ 0,05) et si la stratégie de référence est cohérente avec l'EV de référence (écart ≤ 60 mBB, et toute action jouée au moins 10 % du temps perd au plus 60 mBB).
- Tirage : il faut une action sanctionnée ; sur une EV de référence, la moins chère doit coûter au moins {noise} mBB (bruit mesuré de la référence) ; tapis effectif du joueur entre {lo} et {hi} BB.
- Montants affichés en BB : « <0,02 BB » sous la tolérance ; tout près de 0,02 ou 0,06 BB, trois décimales ou « un peu plus / moins de ».
- Plusieurs actions à 0,02 BB ou moins de la plus rentable : « plusieurs bonnes décisions ».
Code : `spinsacademy/grading.py`, `spinsacademy/quiz.py` (fonctions `candidates`, `teachable`, `correct`).
"""


def main(out):
    import datetime
    os.makedirs(out, exist_ok=True)
    commit = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
    gto, exp = quiz.DEFAULT_VERSION, quiz.DEFAULT_FIELD
    gto_csv, n_gto = csv_bytes(rows(gto), COLS); exp_csv, n_exp = csv_bytes(field_rows(exp), FCOLS)
    lex = json.load(open(os.path.join(ROOT, 'spinsacademy', 'web', 'lexique.json')))
    lex_csv, n_lex = csv_bytes(({'terme': t['term'], 'categorie': lex['categories'][t['cat']], 'definition': t['def'], 'mots_reperes': ', '.join(t['match'])}
                                for t in lex['terms']), ['terme', 'categorie', 'definition', 'mots_reperes'])
    with zipfile.ZipFile(os.path.join(out, 'SpinsAcademy_audit_contenu.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('LISEZ-MOI.md', GUIDE.format(date=datetime.date.today().isoformat(), commit=commit, n_gto=n_gto, n_exp=n_exp, gto=gto, exp=exp,
                                                n_lex=n_lex, cat='profils du field : hypothèses du moteur (tools/field/profils_field.py)'))
        z.writestr('notation.md', NOTATION.format(tol=f'{grading.TOLERANCE_MBB:g}', mix=round(100 * grading.MIXED_MIN), imp=f'{3 * grading.TOLERANCE_MBB:g}',
                                                  noise=quiz.REF_NOISE_MBB, lo=quiz.MIN_STACK_BB, hi=quiz.MAX_STACK_BB))
        z.writestr('questions_gto.csv', gto_csv); z.writestr('questions_exploitant.csv', exp_csv); z.writestr('lexique.csv', lex_csv)
        z.write(quiz.POSTFLOP_FILE, 'profils_postflop.json')
    files = subprocess.run(['git', '-C', ROOT, 'ls-files'], capture_output=True, text=True).stdout.split('\n')
    code = [f for f in files if f and not f.startswith(('data/hrc/raw/', 'data/datasets/', 'legacy/'))]
    with zipfile.ZipFile(os.path.join(out, 'SpinsAcademy_code_moteur.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for f in code: z.write(os.path.join(ROOT, f), 'SpinsAcademy/' + f)
    with zipfile.ZipFile(os.path.join(out, 'SpinsAcademy_datasets.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            if f.startswith('data/datasets/'): z.write(os.path.join(ROOT, f), f[len('data/'):])
    return n_gto, n_exp, len(code)


if __name__ == '__main__':
    print(main(sys.argv[1]))
