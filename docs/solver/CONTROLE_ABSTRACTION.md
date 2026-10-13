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
