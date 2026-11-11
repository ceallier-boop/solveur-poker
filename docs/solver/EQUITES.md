# Bibliothèque d'équités (CE2, 10/11/2026)

Module `spinsacademy/equities.py`, table fixe `spinsacademy/data/equites.json` (47 Ko, JSON simple : le serveur comme le navigateur la lisent sans numpy ni numba). Reconstruction : `python -m spinsacademy.equities --build` (environ 10 secondes ; test de régénération à l'identique : `tests/test_equities.py`).

## Ce que contient la table

Toutes les valeurs sont des entiers en **dix-millièmes** (10 000 = 100 %) ; l'égalité compte pour une moitié ; les 169 classes de mains sont dans l'ordre de `spinsacademy.cards.NAMES`.

1. **Chances de toucher au flop** (`hit_chances(main)`), par énumération de **tous les flops** : 19 600 par combinaison de départ (les deux cartes de la main sont retirées du paquet ; 22 100 flops en tout). Code : `spinsacademy/postflop/flop_hits.py`.
   - « Toucher » = la main **améliore le tableau seul** : au moins une de ses cartes sert. Une paire ou un brelan déjà sur le tableau n'est pas touché.
   - *Catégories exclusives* (la meilleure main touchée ; somme exacte 10 000) : `rien`, `paire_poche_sous_tableau`, `paire_basse`, `paire_intermediaire`, `top_paire`, `paire_poche_sur_tableau`, `double_paire`, `set` (paire de poche + une carte du tableau), `brelan` (une carte de la main + une paire du tableau), `suite`, `couleur`, `full`, `carre`, `quinte_flush`. « Double paire » comprend la paire du tableau complétée par une paire de la main.
   - *Cumulées* (« au moins ») : `au_moins_paire`, `au_moins_top_paire`, `au_moins_double_paire`, `au_moins_brelan`, `au_moins_suite`, `au_moins_couleur`, `au_moins_full`, égales à la somme des exclusives concernées.
   - *Tirages* (comptés seulement si la main n'est pas déjà suite, couleur ou mieux) : `tirage_couleur` (quatre cartes de la même couleur dont une de la main), `tirage_quinte_8` (au moins deux rangs complètent une suite : ouvert ou double ventral), `tirage_quinte_4` (un seul rang : ventral ou quatre cartes d'une extrémité), `tirage_couleur_et_quinte`.
2. **Équité** (`equity_random(main)`, `equity_vs_range(main, id)`) : contre une main au hasard et contre dix ranges de la banque `gto_preflop/2026.11.07-s2` (`ranges()`) : tapis du SB et call du BB à 6, 8, 10 et 12 BB en heads-up, tapis du BTN à 3 joueurs à 8 et 12 BB. Équités exactes préflop du dépôt (`data/equity_169.npy`), cartes bloquées comprises. Équité de la **classe** (169), pas d'une combinaison de couleurs précise : l'écart ne dépasse pas un demi-point.
3. **Forces et faiblesses** (`labels(main)`) : 14 étiquettes produites par règles, chacune avec son identifiant, son groupe (force ou faiblesse), sa règle en français, son seuil chiffré (`seuil`, avec `sens` `>=` ou `<`), et pour chaque main la **valeur mesurée** qui a déclenché l'étiquette. Les seuils sont des nombres ronds posés d'après les quartiles de la table.

| Étiquette | Règle (seuil) |
|---|---|
| assortie / dépareillée | deux cartes de la même couleur / de couleurs différentes |
| connectée | rangs qui se suivent et tirage quinte à 8 outs ≥ 3 % (exclut AK, AQ) |
| paire de poche | deux cartes du même rang (set 10,8 %) |
| cartes hautes | les deux rangs ≥ T |
| fait souvent la top paire ou mieux / rarement | sans paire de poche : top paire ou mieux au flop ≥ 25 % / < 12 % |
| beaucoup de tirages | tirage couleur ≥ 10 % ou tirage quinte à 8 outs ≥ 9 % |
| bloque les As | contient un As |
| forte / faible contre une main au hasard | équité ≥ 60 % / < 45 % |
| cartes éloignées | écart ≥ 2 rangs, sans paire, tirage quinte à 8 outs < 2 % |
| dominée | ≥ 30 % des 20 % meilleures mains la dominent (même carte haute avec un meilleur second rang, ou même second rang avec une meilleure carte haute) |
| quand elle touche, souvent une paire faible | sans paire de poche : ≥ 60 % des touches sont une paire basse ou intermédiaire |

Les paires de poche ne reçoivent que « paire de poche » (et les étiquettes qui ont un sens pour elles : bloque les As, forte ou faible contre une main au hasard) : leur « top paire ou mieux » comprend la double paire avec une paire du tableau, ce qui ne dit rien de la force de la main. `measures_of(main)` donne les mesures de toutes les règles pour n'importe quelle main (domination, part de paire faible, équité contre une main au hasard, chances de toucher), qu'une étiquette s'applique ou non ; la part de paire faible est 0 pour une paire de poche et ne s'y lit pas.

## Pièges traités

- **Toucher** n'est pas « avoir une paire » : une paire du tableau seul n'est pas touchée (comparaison avec la catégorie du tableau seul).
- **Cartes mortes** : la main est retirée du paquet (50 cartes restantes, 19 600 flops) ; l'équité contre une range retire les mains qui partagent une carte.
- **Égalités** : l'équité est une valeur unique ; victoire et égalité ne sont pas séparées.
- **Classes** : les 12 combinaisons d'une main dépareillée ont exactement les mêmes chances de toucher le flop (symétrie des couleurs) ; seule l'équité contre une range dépend des couleurs, par la range elle-même.
- **Domination** : mesurée au niveau des classes (sans retirer les cartes communes) ; c'est une indication.

## Valeurs de contrôle (testées)

AKs : tirage couleur 10,9 %, couleur 0,84 % ; paire de poche : set 10,8 %, carré 0,24 % ; main dépareillée sans paire : brelan avec une paire du tableau 1,35 %, au moins une paire 32,43 % ; équité contre une main au hasard : AA 85,2 %, AKs 67,1 %, 72o 34,6 %. Un recalcul indépendant (sans numba) sur les 19 600 flops de A♠K♠, 7♦2♣, 9♥9♣ et T♦9♦ retrouve la table à 1,5 dix-millième près.
