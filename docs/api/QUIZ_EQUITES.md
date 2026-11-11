# Questions d'équités (CE3, 10/11/2026)

Module `spinsacademy/equity_quiz.py`. Toutes les valeurs viennent de la table fixe `spinsacademy/data/equites.json` (`spinsacademy/equities.py`, voir `docs/solver/EQUITES.md`). Aucun dataset n'est publié pour ces questions.

## Une série d'équités se demande explicitement

```
POST /sessions  {"mode": "equity", "size": 5, "seed": 4, "filters": {"kind": "hit"}}
```

- `mode: "equity"` est un mode à part. Il est servi par la référence virtuelle `equites/2026-11-10` (champ `dataset_version`). Une série GTO ou exploitant ne tire jamais de question d'équités.
- `filters.kind` est facultatif. Il prend la valeur `hit`, `equity` ou `labels` pour une seule sorte de question. Sans lui, les trois sortes alternent dans un ordre tiré au hasard. Tout autre filtre donne une erreur 422, et `kind` est ignoré dans les autres modes.
- La révision espacée (`review: true`, `GET /users/me/reviews?mode=equity`), les défis, la séance du jour et le placement ne s'appliquent pas à ce mode (erreur 422). C'est la décision du 10/11 : pas de coût en BB, donc pas de révision ni de pires erreurs du jour pour l'instant. `equity_quiz.valid()` permettra de la brancher plus tard.
- Le niveau des questions est celui du joueur : niveau 1, ou « 2 » pour les niveaux 2 et plus. Sans `X-Player-Id`, c'est le niveau 1. La réponse le renvoie dans `level`.
- Une main ne revient pas deux fois dans une série. Le tirage évite aussi les mains des dernières séries du joueur.

## Question (`GET /quiz/next`)

```json
{"spot_id": "eq:hit:au_moins_double_paire:L2:w5:n5:p0", "hand": "AQo", "hand_display": "A♠Q♥",
 "prompt_fr": "Tu as A♠Q♥. Quelle est la chance de toucher une double paire ou mieux au flop ?",
 "mode": "equity", "family": "equity", "category_fr": "Équités", "kind": "hit", "kind_fr": "Toucher le flop",
 "topic": "au_moins_double_paire", "level": 2, "answer": "band", "multiple": false,
 "options": [{"id": "b0", "label_fr": "moins de 10 %"}, {"id": "b1", "label_fr": "de 10 à 15 %"}, "…", {"id": "b4", "label_fr": "25 % ou plus"}]}
```

Pour garder la forme des autres questions, les champs de table sont présents mais vides : `table` et `hero` à `null`, `players` et `history` vides.

| `kind` | Question | Réponses |
|---|---|---|
| `hit` (« Toucher le flop ») | « Quelle est la chance de toucher … au flop ? ». Sujets : au moins une paire, top paire ou mieux, double paire ou mieux, brelan ou mieux, suite, couleur, tirage couleur, tirage quinte ouvert. Niveau 1 : paire, brelan, suite, couleur et tirage couleur seulement. | tranches `b0`… |
| `equity` (« Équité contre une range ») | « Quelle est l'équité de … contre une main au hasard / contre les mains avec lesquelles le SB part à tapis en heads-up à 8 BB (44 % des mains) ? ». Il y a dix ranges de la banque. Au niveau 1, seuls « une main au hasard » et les tapis du SB sont posés, avec les mots « chances de gagner ». | tranches `b0`… |
| `labels` (« Forces et faiblesses ») | « Laquelle de ces affirmations est vraie ? » (aux niveaux 2 et plus, aussi « … fausse ? »). Les quatre affirmations sont générées par les 14 règles de la table. | `o0` à `o3`, `answer: "statement"` |

Choix des sujets, valeurs et tranches :
- Un sujet qui ne s'applique pas à la main n'est pas posé. Une paire de poche n'a pas de question « au moins une paire », et une main dépareillée n'a pas de question « couleur ». Une valeur sous 0,5 % n'est pas posée non plus.
- Il y a 4 tranches au niveau 1 et 5 ou 6 aux niveaux 2 et plus. Elles mesurent 10 ou 5 points au niveau 1, et 5 ou 4 points ensuite. La première tranche est « moins de X % », la dernière « Y % ou plus ».
- La valeur exacte n'est jamais à moins de 1,5 point d'une frontière. Le rang de la bonne tranche est tiré d'abord, pour que la bonne réponse ne soit pas toujours la première, puis on cherche un sujet et une main qui conviennent.
- Une affirmation n'est proposée que si elle est **nettement** vraie ou fausse pour la main. Pour une règle à seuil, la valeur mesurée doit être à au moins 20 % du seuil (et au moins 1 point). Les règles pensées pour deux cartes de hauteurs différentes (cartes hautes, dépareillée, top paire souvent ou rarement, paire faible) ne sont pas posées sur une paire. Deux contraires (assortie et dépareillée, par exemple) ne sont jamais proposés ensemble. Au niveau 1, les affirmations « dominée », « bloque les As », « cartes éloignées » et « paire faible » ne sont pas proposées.

L'identifiant `spot_id` porte toute la question : sorte, sujet, niveau, largeur `w`, nombre `n` et rang `p` de la bonne tranche, ou les quatre affirmations dans l'ordre. La question et la correction sont recalculées depuis la table, et la base ne stocke rien de plus que pour une question GTO.

## Correction (`POST /attempts`)

`action_id` est l'identifiant d'une option. La forme de la correction est la même que pour une question GTO, avec quelques champs propres aux équités.

- **Notation.** Les tranches se notent ainsi :
  - bonne tranche : `verdict: "correct"`, 1 point ;
  - tranche voisine : `"imprécision"`, 0,5 point ;
  - sinon : `"erreur"`, 0 point.

  Pour les affirmations, c'est 1 ou 0. `regret_mbb` vaut toujours 0 et `loss_fr` vaut `null` : pas de BB perdus. Un chrono écoulé (`timed_out`) compte comme une erreur, comme ailleurs.
- **`essential_fr`.** La valeur exacte en une phrase : « A♠Q♥ touche une double paire ou mieux au flop 5,8 % du temps, environ une fois sur 17. »
- **`method_fr`.** Comment on l'a calculée, en une phrase : « sur les 19 600 flops possibles une fois tes deux cartes retirées du paquet, environ 1 141 donnent … ». Pour l'équité : calcul exact avant le flop contre chaque main de la range, pondérée par sa fréquence, cartes bloquées retirées, égalité pour moitié.
- **`strengths_fr` et `weaknesses_fr`.** Les forces et faiblesses de la main, en phrases simples. La valeur mesurée est ajoutée entre parenthèses aux niveaux 2 et plus.
- **`details_fr` et `explanation_fr`.** Les lignes de la correction : méthode, bonne tranche ou explication de chaque affirmation, forces, faiblesses.
- **`equity`.** Il contient :
  - `kind`, `category_fr`, `correct_option`, `options` ;
  - pour les tranches : `value_bp` (dix-millièmes) et `value_fr` (« 5,8 % »), ainsi que `flops` (19 600) ou `range_id` ;
  - pour les affirmations : `statements: [{id, label_fr, label_id, true, why_fr}]`, où `why_fr` vaut par exemple « Faux : il faut au moins 60 % d'équité contre une main au hasard ; T♠5♥ : équité contre une main au hasard 44,2 %. ».

Aucune correction ne cite d'expert. Le niveau 1 n'emploie ni « outs » ni « range » dans l'énoncé.

## Bilan et statistiques

- `GET /sessions/{id}/summary` : la forme habituelle, avec `bb_lost: null`, `bb_per_100: null` et `ev_questions: 0`. `by_theme` est groupé par sorte (`kind`, `label_fr`), et chaque erreur porte sa valeur exacte (`value_fr`).
- `GET /users/me/stats` : ces questions ne comptent ni dans le score, ni dans les thèmes, ni dans le BB/100 des modes GTO et exploitant. Le bloc `equity` les résume : `{questions, sessions, points, score_pct, verdicts, by_kind: [{kind, label_fr, questions, score_pct}]}`.
- Les autres écrans (séance du jour, objectifs, pires erreurs, défis, niveaux, recommandations, révision) filtrent par mode GTO ou exploitant et ne voient donc pas ces réponses. Le test `test_other_routes_ignore_equity` le vérifie.

## Réponses multiples (plus tard)

La route `POST /attempts` le permet sans changement de schéma. `action_id` est une chaîne : on pourra envoyer `"o0+o2"` et noter partiellement dans `equity_quiz.correct`, avec un champ `multiple: true` dans la question. Rien de cela n'est actif en v1.

## Démo autonome

`tools/web/build_offline.py` embarque 40 questions par sorte et par niveau, calculées par le même code Python (même énoncé, même correction). Le moteur local de la page tire la série au niveau du joueur, applique les mêmes refus que l'API et garde ces réponses hors des statistiques GTO. Test : `DEMO_URL=… node tools/web/e2e_equity_demo.cjs`.

## v2 : questions avec tableau, sorte « outs » (11/11/2026, `spinsacademy/equity_board.py`)

Ces questions se demandent avec `POST /sessions {"mode": "equity", "filters": {"kind": "outs"}}`. Elles n'entrent pas dans une série d'équités sans filtre (`equity_quiz.DEFAULT_KINDS`) tant que l'écran qui affiche le tableau n'est pas livré.

**Définition (décision du porteur du 11/11).** Une carte « améliore ta main » si ta main monte de catégorie plus que le tableau seul :

```
Δ main    = catégorie(main + tableau + carte) − catégorie(main + tableau)
Δ tableau = catégorie(tableau + carte) − catégorie(tableau)
la carte compte si Δ main > Δ tableau
```

Les catégories, de la plus basse à la plus haute : carte haute, paire, double paire, brelan, suite, couleur, full, carré, quinte flush.

Conséquences :
- une carte qui paire seulement le tableau ne compte pas ;
- une carte qui transforme un brelan en full compte.

Il n'y a pas de main adverse : améliorer ne veut pas dire passer devant, et la correction le rappelle. Jusqu'à la river, on applique la même règle aux deux cartes, en énumérant les 1 081 couples de turn et river possibles ; les améliorations qui demandent les deux cartes sont comptées.

**Tirage des questions.**
- Le flop n'est jamais pairé.
- La main a au plus une paire.
- Entre 2 et 21 cartes l'améliorent.
- 60 % des questions sont tirées sur une main avec un tirage suite ou couleur.

| `topic` | Question | Réponses |
|---|---|---|
| `nombre` | « Combien de cartes améliorent ta main au turn ? » (au niveau 2 et plus : « Combien d'outs (cartes qui améliorent ta main) … ») | quatre nombres espacés de 3 (niveau 1) ou de 2 ; nombre exact = correct, nombre voisin = imprécision |
| `turn` | « Quelle est la probabilité d'améliorer ta main au turn ? » (outs ÷ 47) | tranches, marge de 1,5 point |
| `river` (niveaux 2 et plus) | « … au turn ou à la river ? » (calcul exact sur les 1 081 suites) | tranches, marge de 1,5 point |

**Champs ajoutés à la question** (alignés sur la demande d'Interface du 11/11) :
- `street: "flop"`.
- `board: ["Qs", "7s", "2d"]` : cartes précises, de 3 à 5, dans l'ordre du tableau. Chaque carte est codée sur deux caractères, le rang (23456789TJQKA) puis la couleur (`s`, `h`, `d` ou `c`, en minuscule). `board_display: ["Q♠", "7♠", "2♦"]` sert pour le texte.
- `hero_cards: ["As", "Ks"]` : le héros a toujours ses deux cartes connues. `hand` vaut la main exacte (« AsKs ») et `hand_display` vaut « A♠K♠ ».
- `villain_cards: null`, `ranges: []`, `dead_cards: []` : ces champs sont prévus pour les sortes suivantes. Pour la main contre main, la main adverse pourra être `["??","??"]`, puis dévoilée dans `equity.villain_cards`. Pour les ranges, chaque entrée aura la forme `[{who, label_fr, pct, hands: {classe: poids}}]`, avec les deux ranges pour un exercice de range contre range.

Pour les questions sans tableau, `board` est vide, `street` vaut `null` et `hero_cards` vaut `null` (la v1 porte sur une classe de mains, pas sur des cartes précises).

**Correction.** Comme pour les autres sortes, avec en plus :
- `essential_fr`, la valeur exacte ;
- `method_fr`, la règle de comptage ;
- dans `details_fr`, la liste des cartes groupées par main obtenue (« couleur : 9 cartes (A♠, …) ; paire : 6 cartes (…) »), les probabilités exactes au turn et jusqu'à la river, la règle des 2 et 4 comparée à la valeur exacte (« la règle surestime de 4,8 points ») et l'avertissement « améliorer n'est pas toujours passer devant ».

Le bloc `equity` contient en plus :
- `outs` : `[{card, display, category_fr, why_fr}]`, où `why_fr` vaut par exemple « fait la couleur », ainsi que `outs_fr`, le résumé en une phrase ;
- `outs_count`, `turn_bp` et `river_bp` ;
- `rule_turn_pct` et `rule_river_pct` (2 × outs et 4 × outs) ;
- `board` et `street`.

**Vérification.** `tests/test_equity_board.py` recompte tout avec un évaluateur indépendant, écrit en pur Python sans le kernel `evaln` :
- 3 000 catégories de 3 à 7 cartes ;
- 300 situations de turn ;
- 4 situations complètes jusqu'à la river ;
- cinq cas connus (AsKs sur Qs7s2d = 15 cartes, 7h7d sur Ks9c2s = 2…).

La démo embarque 10 questions d'outs par niveau (+11 Ko).

**Suite de la v2.** Équité d'une main sur un flop connu, puis les exercices de range, puis turn et river.
