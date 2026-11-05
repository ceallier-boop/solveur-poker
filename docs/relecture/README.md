# Relecture experte (évaluation du MVP, remarque 14)

## Échantillon du 14/10/2026 (`echantillon_2026-10-14/`)

300 questions tirées par `python tools/audit/expert_sample.py docs/relecture/echantillon_2026-10-14` (graine 14), sur
`gto_preflop/2026.10.13-3` et `exploit_calls/2026.10.14-1`. Strates : mode, format, situation, position, profondeur,
source de l'EV ; chaque strate a au moins une question, le reste est réparti selon la racine carrée de sa taille. Types de
cas visés : 65 % de décisions nettes, 20 % de décisions serrées (une autre action à moins de 0,1 BB), 15 % de stratégies mixtes.

| Fichier | Pour qui |
|---|---|
| `CONSIGNES.md` | à donner à chaque expert en premier : rôle, règles de notation de l'application, grille de réponse, questions générales |
| `lots/questions_XXX-YYY.md` + `lots/…_reponses.csv` | une conversation par lot de 50 pour un relecteur IA : la fiche des questions et la grille à rendre |
| `questions.md`, `questions.csv`, `questions.jsonl` | les 300 questions d'un bloc (lecture, tableur, traitement automatique) |
| `reponses_modele.csv` | grille complète (300 lignes) |
| `questions_generales.md` | réponses argumentées aux 5 questions générales (seuils, jeu mixte, profils, règles, manques) |

Déroulé proposé avec trois relecteurs indépendants :
1. Chaque expert reçoit `CONSIGNES.md`, puis les 6 lots l'un après l'autre, et rend les 6 grilles et `questions_generales.md`.
   Il ne voit pas les réponses des autres.
2. Fusion : `python tools/audit/expert_merge.py docs/relecture/echantillon_2026-10-14 A:lot1_A.csv A:lot2_A.csv … B:… C:… -o docs/relecture/SYNTHESE.md`
   (ou un fichier complet par expert). Le rapport donne l'accord entre experts (kappa de Fleiss sur la référence), la
   décision par question (validée, à arbitrer, à corriger), le taux de validation par strate et les commentaires.
3. Les questions « à corriger » sont signalées dans l'administration (retrait du spot) ou corrigées dans le moteur ; les
   questions « à arbitrer » sont tranchées par le porteur du projet. Les réponses aux questions générales décident des
   seuils (0,02 / 0,06 / 0,1 BB), des facteurs des profils et des formulations des règles à retenir.

Si le kappa est inférieur à 0,4, les consignes sont à préciser avant d'exploiter les résultats : un désaccord fort entre
relecteurs mesure les consignes autant que l'application.

Contenu : EV dérivées de la référence, sans export brut. À ne pas diffuser hors de l'équipe tant que les droits sur les données
dérivées ne sont pas clarifiés (remarque 27).

## Calculs du solveur maison contre la référence, 30/10/2026 (`solveur_2026-10-30/`, action G12)

60 situations tirées par `python tools/solver/coach_sample.py docs/relecture/solveur_2026-10-30` (graine 30) dans la banque
pilote du solveur `gto_preflop/2026.10.29-s1` (heads-up 12 et 25 BB, 3 joueurs 12 et 25 BB, arbre de la référence). Les deux
calculs sont présentés à l'aveugle (« calcul A » / « calcul B », ordre tiré au hasard à chaque situation).

| Fichier | Pour qui |
|---|---|
| `CONSIGNES.md` | à donner à chaque coach en premier |
| `questions.md` | les 60 fiches : situation, main, fréquences et EV des deux calculs |
| `reponses_modele.csv` | la grille à rendre (meilleure action, calcul le plus juste, confiance, commentaire) |
| `cle.csv` | **à ne pas donner aux coachs** : quel calcul est le solveur, type de cas, perte du solveur mesurée avec les EV de la référence et bruit de la référence |

Composition : 39 désaccords (actions dominantes différentes, au-delà du bruit de la référence de 50 mBB au moins), 9 décisions
serrées, 12 témoins où les deux calculs sont d'accord. Les désaccords sont classés par fréquence réelle de la situation
(probabilité de la ligne d'après la référence × atteinte de la main × combos) : les lignes rares, où le Monte-Carlo de la
référence est maigre et ses EV parfois aberrantes, passent après. Sur toute la banque, ces désaccords pèsent 3,7 % des
décisions pondérées par leur fréquence (679 mains sur 9 378).

Désaccords les plus fréquents dans l'échantillon : tapis du solveur là où la référence paie ou limpe (8), iso-relance du BB
face au limp du SB là où la référence checke (7), fold du solveur là où la référence paie (7), relance du BTN ou du SB là où
la référence limpe (8, dont AA à 12 BB à 3 joueurs).

Dépouillement : les réponses se rapprochent de la clé (`cle.csv`, colonnes `A` et `B`) ; le taux de « solveur plus juste »
parmi les désaccords, par famille de décision, dit où caler le solveur en priorité.
