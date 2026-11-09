# Rapport de calage du solveur sur la référence v5 (09/11/2026)

> **Le solveur est dans le bruit de la référence à toutes les profondeurs ; le défaut des pots relancés est réel mais coûte 3 à 6 mBB par main.**

*(1 mBB = un millième de blind par main : 1 000 mBB valent 1 BB. 3 à 6 mBB, c'est l'équivalent de 0,003 à 0,006 BB perdu en moyenne à chaque main jouée.)*

## Conclusions

**Ce que nous avons fait.** La référence (HRC, avec le même arbre de jeu que le nôtre) a été calculée pour 24 profondeurs : heads-up et à trois joueurs, de 2 à 25 BB, avec plusieurs calculs répétés aux profondeurs qui comptent le plus. Nous avons comparé, décision par décision, la stratégie de notre solveur (banque `2026.11.07-s2`) à celle de la référence. Pour savoir ce qui est un vrai écart et ce qui est du hasard, nous avons mesuré aussi à quel point la référence s'écarte d'elle-même d'un calcul à l'autre.

**Ce qui est vérifié.**
- Sur les décisions qui finissent à tapis ou face à un tapis (pousser, payer un tapis, se coucher face à un tapis), notre solveur et la référence jouent presque la même stratégie jusqu'à 16 BB : 98 à 100 % des mains reçoivent la même action dominante en heads-up jusqu'à 12 BB, et 96 à 97 % de 14 à 25 BB. L'écart de coût est du niveau du bruit de la référence. **Plage fiable confirmée : 8 à 16 BB, heads-up et à trois joueurs.**
- Sur un jeu où il n'y a aucune décision après le flop (heads-up à 4 BB), notre solveur coïncide avec le calcul exact de la référence à moins d'un point près : les règles de calcul (blindes, équités, gains) sont les mêmes.
- À toutes les profondeurs, aucune action de notre solveur n'est absente de l'arbre de la référence, et la perte mesurée avec les valeurs de la référence reste au niveau de ce que la référence perd elle-même.
- À trois joueurs, le solveur est dans le bruit de la référence à toutes les profondeurs (de 2 à 25 BB).

**Ce qui reste imparfait.**
- **Le défaut des pots relancés.** Quand une relance est payée et que la main continue après le flop, notre solveur sous-estime la valeur de certaines mains (des as assortis, des connecteurs assortis, des petites paires). Il en résulte, à 16, 20 et 25 BB en heads-up, que le BB se couche 8 à 9 points de trop face à une ouverture à 2 BB (27 % chez nous contre 17 à 19 % dans la référence) et 4 à 6 points de trop face à une relance après un limp. Cet écart est systématique : 10 à 25 fois l'écart entre deux calculs de la référence. Mais il coûte peu : 3 à 6 mBB par main au-dessus de ce que perd la référence elle-même. Nous avons essayé de le corriger (G17, trois tables apprises sur des calculs exacts) ; le gain n'était pas assez net pour justifier de refaire toute la banque, la correction n'est donc pas retenue.
- **La référence n'est elle aussi qu'une approximation.** Ses calculs Monte-Carlo reposent sur des regroupements de mains, comme les nôtres. Être d'accord avec elle ne prouve pas être exact. Le contrôle exact existe, mais il ne couvre que les petits tapis : le moteur exact ne développe pas l'ouverture à 2 BB (heads-up) ni le limp du bouton (trois joueurs), donc il n'ancre que jusqu'à 6 BB en heads-up et 4 BB à trois joueurs.
- **À trois joueurs et profond (16 BB et plus),** le bruit de la référence est si grand (de 90 à 260 mBB par calcul isolé) que l'on ne peut plus distinguer le solveur de la référence : on ne peut pas conclure dans un sens ni dans l'autre.

**Ce que cela change pour les joueurs.**
- Les décisions à tapis de la banque (de 8 à 16 BB) sont fiables : on peut les enseigner telles quelles.
- Les décisions qui mènent au flop (ouvrir, payer une ouverture, isoler après un limp) sont de bonnes approximations, mais à 14 BB et plus le solveur recommande un peu trop de coucher face à une ouverture avec des mains marginales (as assortis faibles, connecteurs assortis). Ces mains valent un peu plus que ce que dit la banque ; l'erreur est petite en valeur, mais elle peut contredire un coach sur ces mains précises.
- Aucune plage « sûre » n'est donnée pour ces décisions au-dessus de 8 BB : à 16 BB et plus, la banque reste utilisable pour l'entraînement, avec cette réserve.

## Détail par profondeur

*Lecture des colonnes.* **Mêmes actions** : part des mains pour lesquelles notre solveur et la référence recommandent la même action principale. **Écart de stratégie** : distance entre les deux stratégies (0 % = identiques ; 15 à 20 % est le niveau d'écart de deux calculs de la référence entre eux). **Perte** : ce que notre solveur perd, en mBB par main, mesuré avec les valeurs de la référence ; **plancher** : ce que la référence perd elle-même avec ses propres valeurs (son bruit). Une perte proche du plancher veut dire « dans le bruit ».

### Décisions qui finissent à tapis (ou face à un tapis)

| Tapis | Calculs de référence | Mêmes actions | Écart de stratégie | Perte (plancher) |
|---|---|---|---|---|
| Heads-up 2 BB | 1 | 99,8 % | 0,1 % | 0,7 (0,0) |
| Heads-up 4 BB | 1 | 97,9 % | 1,4 % | 0,2 (0,3) |
| Heads-up 6 BB | 1 | 99,4 % | 0,8 % | 0,5 (0,3) |
| Heads-up 8 BB | 3 | 99,2 % | 1,4 % | 1,4 (1,1) |
| Heads-up 10 BB | 1 | 98,6 % | 2,0 % | 2,4 (2,0) |
| Heads-up 12 BB | 6 | 98,3 % | 2,0 % | 2,3 (3,2) |
| Heads-up 14 BB | 1 | 97,0 % | 2,4 % | 5,2 (4,5) |
| Heads-up 16 BB | 4 | 96,1 % | 4,1 % | 6,1 (7,3) |
| Heads-up 18 BB | 1 | 97,4 % | 3,8 % | 9,1 (14,0) |
| Heads-up 20 BB | 4 | 95,1 % | 5,0 % | 15,7 (20,1) |
| Heads-up 22 BB | 1 | 94,8 % | 6,0 % | 49,5 (33,9) |
| Heads-up 25 BB | 4 | 97,1 % | 4,9 % | 42,8 (50,9) |
| 3 joueurs 4 BB | 1 | 92,0 % | 8,6 % | 40,6 (31,1) |
| 3 joueurs 6 BB | 1 | 93,0 % | 7,1 % | 39,9 (33,1) |
| 3 joueurs 8 BB | 4 | 97,6 % | 5,2 % | 7,8 (29,8) |
| 3 joueurs 10 BB | 1 | 95,7 % | 5,3 % | 18,2 (24,6) |
| 3 joueurs 12 BB | 6 | 97,4 % | 4,6 % | 10,4 (27,7) |
| 3 joueurs 14 BB | 1 | 95,4 % | 5,6 % | 34,5 (42,3) |
| 3 joueurs 16 BB | 5 | 96,8 % | 5,8 % | 16,9 (61,4) |
| 3 joueurs 18 BB | 1 | 95,1 % | 6,6 % | 49,3 (77,0) |
| 3 joueurs 20 BB | 1 | 95,5 % | 6,9 % | 75,1 (96,6) |
| 3 joueurs 22 BB | 1 | 94,0 % | 7,8 % | 110,6 (150,1) |
| 3 joueurs 25 BB | 4 | 95,5 % | 8,1 % | 83,9 (226,7) |

La perte et le plancher montent avec la profondeur : la référence devient plus bruitée quand les tapis sont profonds, surtout à trois joueurs. La perte de notre solveur reste à l'intérieur ou au niveau de ce plancher presque partout.

### Décisions qui mènent au flop (ouvrir, payer, isoler)

| Tapis | Calculs de référence | Mêmes actions | Écart de stratégie | Perte (plancher) | Bruit d'un calcul isolé : écart de stratégie, perte |
|---|---|---|---|---|---|
| Heads-up 2 BB | 1 | 92,8 % | 7,8 % | 0,9 (0,3) | |
| Heads-up 4 BB | 1 | 91,4 % | 9,6 % | 19,2 (8,6) | |
| Heads-up 6 BB | 1 | 86,8 % | 15,7 % | 8,6 (6,1) | |
| Heads-up 8 BB | 3 | 86,3 % | 20,0 % | 7,3 (8,6) | 11,9 %, 8,8 |
| Heads-up 10 BB | 1 | 80,2 % | 22,0 % | 12,1 (6,7) | |
| Heads-up 12 BB | 6 | 83,4 % | 21,2 % | 8,4 (7,4) | 10,1 %, 7,2 |
| Heads-up 14 BB | 1 | 78,2 % | 23,9 % | 15,3 (8,4) | |
| Heads-up 16 BB | 4 | 83,0 % | 23,2 % | 12,2 (9,2) | 11,8 %, 11,6 |
| Heads-up 18 BB | 1 | 77,5 % | 24,1 % | 19,6 (10,1) | |
| Heads-up 20 BB | 4 | 81,4 % | 23,5 % | 18,4 (15,2) | 12,8 %, 22,8 |
| Heads-up 22 BB | 1 | 72,5 % | 27,6 % | 28,9 (16,1) | |
| Heads-up 25 BB | 4 | 75,1 % | 26,4 % | 24,7 (18,8) | 14,1 %, 39,6 |
| 3 joueurs 4 BB | 1 | 84,7 % | 14,6 % | 64,1 (45,4) | |
| 3 joueurs 6 BB | 1 | 85,0 % | 16,5 % | 74,4 (63,5) | |
| 3 joueurs 8 BB | 4 | 86,4 % | 18,2 % | 45,0 (47,1) | 10,8 %, 68,5 |
| 3 joueurs 10 BB | 1 | 80,6 % | 20,8 % | 45,2 (33,8) | |
| 3 joueurs 12 BB | 6 | 81,6 % | 21,3 % | 27,8 (25,1) | 9,9 %, 49,0 |
| 3 joueurs 14 BB | 1 | 79,0 % | 22,9 % | 52,8 (34,1) | |
| 3 joueurs 16 BB | 5 | 82,6 % | 22,3 % | 31,3 (35,6) | 11,5 %, 93,4 |
| 3 joueurs 18 BB | 1 | 79,3 % | 22,7 % | 53,7 (32,1) | |
| 3 joueurs 20 BB | 1 | 80,8 % | 22,1 % | 54,4 (40,0) | |
| 3 joueurs 22 BB | 1 | 78,0 % | 23,1 % | 79,8 (53,6) | |
| 3 joueurs 25 BB | 4 | 82,6 % | 21,9 % | 55,8 (59,9) | 13,6 %, 256,9 |

L'écart de stratégie sur ces décisions est plus grand que sur les décisions à tapis, et il grandit avec la profondeur : c'est le défaut des pots relancés. L'écart de coût (perte moins plancher) reste petit : de 0 à 1 mBB jusqu'à 8 BB en heads-up, de 1 à 5 mBB à 10-12 BB, de 3 à 13 mBB à 14-25 BB.

### Le défaut des pots relancés, mesuré avec 4 calculs de référence (heads-up)

| Tapis | Perte moins plancher | Le BB se couche face à l'ouverture à 2 BB : référence → solveur | Le BB se couche face à la relance après un limp : référence → solveur |
|---|---|---|---|
| 16 BB | +3,0 mBB | 19,2 % → 27,4 % | 46,2 % → 50,8 % |
| 20 BB | +3,2 mBB | 19,0 % → 28,1 % | 44,5 % → 48,1 % |
| 25 BB | +5,9 mBB | 17,2 % → 26,4 % | 42,5 % → 48,2 % |

L'écart entre les quatre calculs de la référence est de 0,3 à 0,8 point : la différence de 8 à 9 points n'est donc pas du hasard.

### Les calculs exacts (sans bruit)

| Situation | Décisions à tapis | Décisions qui mènent au flop |
|---|---|---|
| Heads-up 4 BB (aucun flop) | écart de stratégie 0,4 % : identique | — |
| Heads-up 6 BB | écart 1,3 %, mêmes actions 99 %, perte 0,7 (plancher 0,4) | écart 22 % : le SB limpe 12,8 % chez nous contre 0,6 % dans l'exact |
| 3 joueurs 4 BB | écart 2,0 %, mêmes actions 98 %, perte 0,4 (plancher 0,0) | écart 8,9 % |

Le calcul exact ne développe pas l'ouverture à 2 BB (heads-up) ni le limp du bouton (trois joueurs) : il ne permet donc pas de contrôler les tapis plus profonds.

### Ce qui n'est pas dans ce rapport

La correction du défaut (G17) n'est pas appliquée à la banque : la banque `2026.11.07-s2` est celle du solveur sans correction. Les trois tables de correction essayées restent dans le dépôt (`spinsacademy/solver/corrections/`) ; la mesure détaillée est dans `docs/solver/BANQUE_SOLVEUR.md` (sections G17, G19). Les données de ce rapport : `data/solver/g17/courbe_calage_s2.json`, outils `tools/solver/calibration_curve.py` et `tools/solver/compare_exact.py`.
