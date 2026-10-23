# Relecture experte de SpinsAcademy : consignes

Échantillon du 2026-10-14, commit `9bfff51`, datasets `2026.10.13-3` et `exploit_calls/2026.10.14-1`. 300 questions (identifiants Q001 à Q300).

## Ton rôle

Tu es un joueur expert d'Expresso / Spin & Go (3 joueurs puis heads-up, 4 à 25 BB, préflop, **chip EV**, sans ICM).
Tu relis des questions d'entraînement produites par l'application et tu dis si la **référence**, les **verdicts** et les
**textes de correction** sont justes. Tu travailles seul : ne te concerte pas avec les autres relecteurs, l'accord entre
relecteurs est mesuré ensuite.

## Ce que fait l'application (à juger, pas à refaire)

- Référence : stratégie d'équilibre calculée par le solveur de référence, ou EV exacte quand tout le monde est
  à tapis. En mode exploitant : meilleure réponse contre un profil fictif dont la fréquence de tapis (ou de call, pour
  la Station d'appel) est déformée par rapport à l'équilibre push/fold, en EV exacte.
- EV en BB, en chip EV. Les EV de référence sont des estimations (Monte-Carlo) : un bruit d'environ 0,1 BB par main et par action
  a été mesuré. C'est pourquoi une action à moins de 0,1 BB de la meilleure est jugée « pertinente ».
- Verdicts :
  - **correct** : écart à la meilleure action ≤ 0,02 BB, ou action jouée au moins 10 % du temps par la référence ;
  - **imprécision** : écart entre 0,02 et 0,06 BB, ou (EV de référence) entre 0,06 et 0,1 BB : la correction garde la référence et
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

1. **Seuils de verdict** : 0,02 BB (correct), 0,06 BB (imprécision), 0,1 BB (action pertinente pour une EV de référence). Sont-ils
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

- Mode : GTO 248, exploitant 52
- Format : 3-handed 219, heads-up 81
- Position : BB 147, BTN 39, SB 114
- Situation : face à un limp 39, face à un tapis 145, face à une relance 65, premier à parler 51
- Profondeur : 10_16 132, 17_25 87, lt10 81
- Source de l'EV : exact 86, référence 214
- Type de cas : décision nette 221, décision serrée (autre action à moins de 0,1 BB) 55, stratégie mixte 24
- Verdict de l'erreur la plus tentante : avec erreur 300
