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

Contenu : EV dérivées d'HRC, sans export brut. À ne pas diffuser hors de l'équipe tant que les droits sur les données
dérivées ne sont pas clarifiés (remarque 27).
