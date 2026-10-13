# Contrôle de l'abstraction postflop : sous-jeux river et turn résolus exactement

Outil : `tools/solver/exact_check.py` (moteur `spinsacademy/postflop/exact.py`). Aucune donnée HRC n'est utilisée comme référence : seules les ranges d'entrée viennent de l'export HRC.

## Protocole

- Spot : heads-up 25 BB, pot limpé (le SB limpe, le BB checke) ; pot 2 BB, 24 BB derrière. Ranges HRC `min_raise_hu/hand_15` : BB = `SB-call:X` (OOP), SB = `root:C` (IP).
- Solveur abstrait de production : 16 groupes de force partagés entre tous les boards, 6 tirages pour la force à la turn, 3 000 itérations sur 1 000 boards, sous-jeu commençant à la rue testée.
- Référence : sur chaque board tiré au hasard, CFR+ complet combo par combo ; à la turn, les 48 rivers sont énumérées. Même arbre de mises.
- Mesures : exploitabilité moyenne (en % du pot), et gains G par classe (comme `fast_evaluate`) de la stratégie abstraite moins les gains exacts.

## Résultats (2026-10-13)

| Rue | Boards | Exploitabilité exacte | Exploitabilité abstraite | BB : G abstrait − exact | SB : G abstrait − exact |
|---|---|---|---|---|---|
| River | 400 | 0,31 % | 5,7 % | +3 mBB | −3 mBB |
| Turn | 80 | 1,4 % | 17,6 % | −28 mBB | +29 mBB |

Écarts par famille, en mBB :

| Famille | River BB | River SB | Turn BB | Turn SB |
|---|---|---|---|---|
| Paires | −4 | −20 | −91 | −3 |
| As assortis | −35 | −8 | −128 | +42 |
| Connecteurs assortis | −3 | +9 | −44 | +39 |
| Autres assorties | +7 | −1 | −37 | +32 |
| Broadways dépareillés | −38 | −5 | −85 | +67 |
| As dépareillés | −44 | −18 | −133 | +31 |
| Dépareillées faibles | +5 | −2 | −20 | +22 |

Détail par classe : `exact_river_hu25_limp.json`, `exact_turn_hu25_limp.json`.

## Lecture

- L'abstraction joue mal (17,6 % du pot exploitables à la turn), mais l'erreur sur les gains reste modérée. Elle transfère environ 30 mBB du BB (OOP) vers le SB (IP) à la turn.
- Les paires ne sont pas surévaluées à la river ni à la turn. La surévaluation de +250 à +590 mBB des paires dans les pots limpés à 25 BB, constatée par rapport à HRC, ne vient donc pas de l'abstraction turn / river.
- Il reste deux causes possibles : le flop (force sur 3 cartes estimée avec 6 tirages seulement, stratégie partagée entre tous les flops), et le modèle de réalisation (corrections additives par classe, ajustées contre une seule paire de ranges).

## Flop : gain du BB dans le pot limpé, comparé à HRC (2026-10-13)

Dans l'export HRC, l'EV du check du BB face au limp, relative au fold, est exactement son gain postflop G dans le pot limpé. On le compare au G du solveur postflop de production (sous-jeu complet à partir du flop, mêmes ranges HRC). Écart en mBB, pondéré par la range de check du BB :

| Variante du solveur postflop | Paires | Connecteurs assortis | Broadways dépareillés | Global |
|---|---|---|---|---|
| Production : 16 groupes, 6 tirages, 3 000 itérations | −56 | −133 | +51 | −72 |
| 3 fois plus d'itérations et de boards | −112 | −119 | +6 | −66 |
| 24 tirages pour la force au flop et à la turn | −30 | −76 | +39 | −36 |
| 32 groupes | −115 | −120 | +16 | −72 |
| Tapis seul après une mise (pas de relance) | −128 | −138 | +146 | −130 |

- L'écart global est divisé par deux avec 24 tirages au lieu de 6. Un tirage bruité mélange des mains de forces différentes dans un même groupe, ce qui pénalise surtout le joueur qui parle en premier.
- Plus d'itérations ou plus de groupes n'aident pas : ce n'est pas un problème de convergence.
- Le coût est faible : les tirages ne servent qu'à préparer le réservoir de boards.

## Arbre préflop : règle de tapis de HRC

HRC ne propose pas de tapis en premier de parole ni face à un limp au-delà de 15 BB de tapis effectif en heads-up. L'arbre maison en proposait toujours un. L'option `TreeConfig(unopened_allin_max=15)` reproduit exactement les actions HRC en heads-up, tapis compris (test `test_unopened_allin_rule_matches_hrc_heads_up`).

Heads-up 25 BB, solveur complet avec réalisation, fréquences globales :

| Nœud | HRC | Sans la règle | Avec la règle |
|---|---|---|---|
| SB premier de parole : fold / limp / relance | 4,6 / 68,8 / 26,5 | 4,5 / 85,0 / 10,4 | 4,6 / 75,5 / 19,9 |
| BB face au limp : check / relance (/ tapis) | 60,6 / 39,4 | 62,9 / 27,0 / 10,1 | 59,3 / 40,7 |
| BB face à la relance : fold / call / relance / tapis | 50,2 / 32,2 / 9,2 / 8,5 | 54,9 / 28,5 / 8,1 / 8,5 | 54,0 / 30,7 / 13,8 / 1,5 |

Écart d'EV du limp du SB pour les paires : +257 mBB sans la règle, +42 mBB avec. Le tapis du BB sur un limp, absent chez HRC, faisait payer les paires du SB et faussait toute la ligne. C'est la cause principale de la surévaluation des paires.

## Benchmark HRC heads-up : règle de tapis et 24 tirages (2026-10-13)

`tools/solver/benchmark_hrc.py --postflop realization --outer 5`. Perte = regret de la stratégie maison mesuré avec les EV HRC (entre parenthèses : regret de HRC lui-même, plancher de bruit), en mBB.

| Tapis | Nœud | Avant | Règle de tapis | Règle + 24 tirages | Plancher HRC |
|---|---|---|---|---|---|
| 25 BB | SB premier de parole | 13,6 | 12,6 | 9,4 | 4,3 |
| 25 BB | BB face au limp | 15,1 | 13,5 | 10,4 | 4,7 |
| 25 BB | BB face à la relance | 44,5 | 32,8 | 28,1 | 12,8 |
| 20 BB | SB premier de parole | 8,3 | 8,8 | 6,8 | 3,4 |
| 20 BB | BB face au limp | 13,8 | 11,8 | 7,9 | 3,5 |
| 20 BB | BB face à la relance | 40,2 | 30,5 | 28,5 | 12,6 |
| 16 BB | SB premier de parole | 6,0 | 5,9 | 5,4 | 2,7 |
| 16 BB | BB face au limp | 9,5 | 8,9 | 5,7 | 4,2 |
| 16 BB | BB face à la relance | 32,7 | 32,0 | 23,2 | 9,3 |

Limp du SB à 25 BB : 85 % avant, 71,5 % maintenant (HRC 68,8 %). Plus aucune action hors de l'arbre HRC.

Les deux réglages sont désormais ceux par défaut :
- `TreeConfig.unopened_allin_max` : 15 BB en heads-up ; à 3 joueurs, le tapis reste toujours proposé, car le seuil de HRC y varie selon la position ;
- `PostflopConfig.rollouts` : 24.

Point restant : le BB face à la relance du SB reste à 2 à 3 fois le plancher HRC.

## Règles postflop de HRC et groupes par texture (2026-10-13)

Paramètres de l'export HRC (`settings.json`) : moteur Monte-Carlo, 256 groupes par rue ; postflop « simple » : mise 66 %, tapis ajouté si SPR ≤ 5, pas de donk bet (`POSTFLOP_ALLOW_DONK = False`), check-down forcé selon le nombre de joueurs (`POSTFLOP_FORCE_CHECKDOWN_AFTER = [3, 3, 2, 1, 0, ...]`, lu comme le nombre de rues jouées : 3 en heads-up, 2 à trois joueurs).

- Règle « pas de donk bet » (`PostflopConfig.donk = False`, désormais par défaut) : OOP ne peut pas ouvrir les mises d'une rue quand IP a été l'agresseur de la rue précédente (le relanceur préflop au flop). L'agresseur préflop est transmis à chaque sous-jeu (`Realization.subgames`).
- Groupes croisés force × texture du board (`PostflopConfig.textured`, 8 classes : couleur possible, board pairé, quinte possible). Effet sur la turn exacte (40 boards, 24 tirages) : exploitabilité 16,9 % → 13,3 % du pot ; biais du BB par famille réduit, par exemple As assortis −118 → −86 mBB et broadways dépareillés −123 → −78 mBB. Sur la river : 6,2 % → 5,3 %. 64 groupes sans texture : 7,1 % (pas mieux).

Benchmark HRC heads-up 25 BB (pertes en mBB : SB premier de parole / BB face au limp / BB face à la relance ; plancher HRC 4,3 / 4,7 / 12,8) :

| Réglage | Pertes | Limp du SB | Durée |
|---|---|---|---|
| Règle de tapis + 24 tirages | 9,4 / 10,4 / 28,1 | 71,5 % | 393 s |
| + groupes par texture, 6 000 itérations postflop | 9,1 / 10,4 / 26,9 | 72,9 % | 855 s |
| + pas de donk bet | 9,3 / 9,1 / 26,9 | 69,9 % (HRC 68,8 %) | 315 s |

La règle « pas de donk bet » est retenue par défaut. Les groupes par texture restent une option : gain faible pour un calcul 2,7 fois plus long.

## Seuils de tapis HRC à 3 joueurs (2026-10-13)

Table `UNOPENED_ALLIN` (`spinsacademy/solver/tree.py`) relevée sur les exports : BTN premier de parole 18 BB ; SB après fold du BTN 15 BB ; SB face au limp du BTN 22 BB ; BB face au limp du SB 15 BB ; BB face au limp du BTN 18 BB. L'arbre par défaut reproduit exactement les actions de tous les nœuds HRC exportés (test `test_default_tree_matches_hrc_actions_exactly`).

Benchmark 3 joueurs 25 BB (`--outer 4`, 24 tirages, donk bet autorisé dans les deux cas). Pertes en mBB :

| Nœud | Tapis toujours proposé | Seuils HRC | Plancher HRC |
|---|---|---|---|
| BTN premier de parole | 7,5 (hors HRC 0 %) | 7,9 | 3,9 |
| SB face au limp du BTN | 40,3 (hors HRC 8,9 %) | 27,5 | 17,6 |
| SB après fold du BTN | 14,2 (hors HRC 2,0 %) | 16,6 | 7,9 |
| SB face à l'open du BTN | 9,9 | 8,5 | 11,8 |
| BB face au limp du BTN | 35,9 (hors HRC 16,3 %) | 16,8 | 12,3 |
| BB face au limp du SB | 18,2 (hors HRC 6,4 %) | 14,3 | 9,2 |
| BB face à l'open du SB | 36,2 | 35,9 | 16,3 |
| BB face à l'open du BTN | 51,7 | 43,8 | 16,2 |

Plus aucune action hors de l'arbre HRC. Restent au-dessus de 2 fois le plancher : le BB face à une relance (BTN ou SB) et le SB face au limp du BTN.
