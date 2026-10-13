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
