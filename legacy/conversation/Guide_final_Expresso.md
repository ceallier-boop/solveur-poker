# Guide final Expresso : ranges push/fold et adaptations

Ce document regroupe toutes les ranges calculées (3 joueurs et heads-up), les règles de comportement selon le stack et les ajustements selon le profil des adversaires. Il se lit de haut en bas, mais la section 3 est la fiche à garder sous la main.

## 1. Hypothèses (à connaître avant de s'y fier)

- Format Expresso : 3 joueurs, le gagnant prend tout le prize pool. La valeur d'un stack est donc proportionnelle à ses jetons : on raisonne en chip EV, sans ICM.
- Stacks égaux (en grosses blinds), SB 0,5 BB, BB 1 BB, pas d'ante. En partie réelle les stacks deviennent vite inégaux : les ranges bougent alors.
- Push/fold pur : chaque joueur fold ou envoie tout son stack. Le modèle est surtout adapté sous 12 BB et reste utile jusqu'à 15 BB. Au-delà, les raises de taille normale existent et ne sont pas modélisées ici.
- Les ranges sont celles d'un équilibre de Nash. Elles ne sont pas exploitables, mais elles ne cherchent pas à exploiter un adversaire : la section 6 donne les ajustements.
- Les « ranges à jouer » ci-dessous sont arrondies : une main est jouée si l'équilibre la joue au moins une fois sur deux. L'arrondi coûte moins de 0,3 mBB par main d'écart à l'équilibre, donc c'est négligeable. Les mains jouées de façon mixte (entre 5 et 95 %) sont signalées comme « marges ».

## 2. Fiche rapide : part de mains jouées

### 3 joueurs (pourcentage de mains)

| Stack | BTN push | SB open-shove (BTN fold) | SB call vs BTN | BB call vs SB | BB call vs BTN (SB fold) | BB call vs BTN + SB |
|---|---|---|---|---|---|---|
| 4 BB | 42 % | 74 % | 36 % | 73 % | 63 % | 53 % |
| 6 BB | 38 % | 67 % | 29 % | 54 % | 36 % | 29 % |
| 8 BB | 35 % | 62 % | 22 % | 44 % | 29 % | 18 % |
| 10 BB | 33 % | 57 % | 18 % | 36 % | 24 % | 13 % |
| 12 BB | 32 % | 51 % | 15 % | 33 % | 20 % | 10 % |
| 15 BB | 27 % | 45 % | 13 % | 27 % | 16 % | 8 % |

### Heads-up (SB = bouton)

| Stack | SB push | BB call |
|---|---|---|
| 4 BB | 74 % | 74 % |
| 6 BB | 69 % | 54 % |
| 8 BB | 62 % | 44 % |
| 10 BB | 58 % | 37 % |
| 12 BB | 53 % | 33 % |
| 15 BB | 46 % | 29 % |

## 3. Fiche à garder sous la main : ranges à jouer, stack par stack

Notation : `22+` = toutes les paires à partir de 22, `A2s+` = Axs de A2s à AKs, `ATo+` = ATo, AJo, AQo, AKo, `K5s-K2s` = de K5s à K2s. s = suited, o = offsuit. Lis le bloc de la situation, puis la ligne de ton stack.

### BTN : push (les deux autres ont encore à parler)

- **4 BB (42 %)** : 22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 98s, 87s, A2o+, K5o+, Q8o+, J9o+, T9o  
  *marges : 87s 66%*
- **6 BB (38 %)** : 22+, A2s+, K2s+, Q6s+, J7s+, T7s+, 97s+, 86s+, 76s, 65s, A2o+, K7o+, Q9o+, JTo  
  *marges : T9o 37%*
- **8 BB (35 %)** : 22+, A2s+, K4s+, Q8s+, J7s+, T7s+, 97s+, 86s+, 76s, 65s, A2o+, K9o+, QTo+, JTo
- **10 BB (33 %)** : 22+, A2s+, K5s+, Q8s+, J8s+, T7s+, 97s+, 86s+, 76s, A2o+, KTo+, QTo+, JTo
- **12 BB (32 %)** : 22+, A2s+, K6s+, Q8s+, J8s+, T7s+, 97s+, 87s, 76s, A2o+, KTo+, QTo+, JTo  
  *marges : A2o 58%, K5s 41%*
- **15 BB (27 %)** : 22+, A2s+, K7s+, Q8s+, J8s+, T8s+, 98s, 87s, A7o+, A5o, KTo+, QTo+, JTo  
  *marges : A6o 28%, Q8s 94%*

### SB : open-shove quand le BTN a foldé

- **4 BB (74 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 54s, A2o+, K2o+, Q2o+, J2o+, T5o+, 96o+, 86o+, 76o
- **6 BB (67 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T3s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q2o+, J6o+, T7o+, 97o+, 86o+, 76o
- **8 BB (62 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 74s+, 64s+, 53s+, 43s, A2o+, K2o+, Q5o+, J7o+, T7o+, 97o+, 87o, 76o  
  *marges : Q4o 44%, 43s 50%*
- **10 BB (57 %)** : 22+, A2s+, K2s+, Q2s+, J3s+, T4s+, 95s+, 84s+, 74s+, 64s+, 53s+, 43s, A2o+, K2o+, Q8o+, J8o+, T8o+, 97o+, 87o, 76o  
  *marges : Q7o 7%*
- **12 BB (51 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 95s+, 85s+, 74s+, 64s+, 53s+, A2o+, K4o+, Q8o+, J9o+, T8o+, 98o, 87o  
  *marges : J8o 39%*
- **15 BB (45 %)** : 22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 96s+, 85s+, 75s+, 64s+, 54s, A2o+, K7o+, Q9o+, J9o+, T8o+, 98o  
  *marges : J5s 39%*

### SB : call du push du BTN

- **4 BB (36 %)** : 22+, A2s+, K2s+, Q7s+, J8s+, T8s+, 98s, 87s, A2o+, K7o+, Q9o+, JTo
- **6 BB (29 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A2o+, K9o+, QTo+
- **8 BB (22 %)** : 33+, A2s+, K9s+, QTs+, JTs, A5o+, KTo+
- **10 BB (18 %)** : 33+, A3s+, KTs+, QJs, A7o+, KJo+
- **12 BB (15 %)** : 44+, A5s+, KTs+, QJs, A8o+, KQo  
  *marges : 33 41%*
- **15 BB (13 %)** : 44+, A7s+, KJs+, A9o+, KQo  
  *marges : 44 84%*

### BB : call du push du SB (BTN a foldé)

- **4 BB (73 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 53s+, A2o+, K2o+, Q2o+, J2o+, T6o+, 96o+, 86o+, 76o
- **6 BB (54 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 97s+, 87s, A2o+, K2o+, Q4o+, J7o+, T8o+
- **8 BB (44 %)** : 22+, A2s+, K2s+, Q4s+, J7s+, T8s+, 98s, A2o+, K3o+, Q8o+, J9o+, T9o  
  *marges : K2o 31%*
- **10 BB (36 %)** : 22+, A2s+, K2s+, Q7s+, J8s+, T9s, A2o+, K6o+, Q9o+, JTo  
  *marges : K5o 26%*
- **12 BB (33 %)** : 22+, A2s+, K5s+, Q8s+, J9s+, A2o+, K7o+, QTo+, JTo  
  *marges : K7o 57%*
- **15 BB (27 %)** : 33+, A2s+, K8s+, Q9s+, JTs, A2o+, K9o+, QJo  
  *marges : QTo 45%*

### BB : call du push du BTN (SB a foldé)

- **4 BB (63 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T3s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q4o+, J7o+, T8o+, 97o+, 87o, 76o
- **6 BB (36 %)** : 22+, A2s+, K2s+, Q7s+, J8s+, T8s+, 98s, A2o+, K7o+, Q9o+, JTo  
  *marges : K6o 32%*
- **8 BB (29 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A2o+, K9o+, QTo+
- **10 BB (24 %)** : 22+, A2s+, K9s+, QTs+, JTs, A4o+, KTo+, QJo
- **12 BB (20 %)** : 22+, A2s+, KTs+, QTs+, A6o+, KJo+
- **15 BB (16 %)** : 44+, A5s+, KTs+, QJs, A8o+, KJo+  
  *marges : A4s 16%*

### BB : call quand le BTN a poussé et le SB a call

- **4 BB (53 %)** : 22+, A2s+, K2s+, Q2s+, J3s+, T4s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K7o+, Q8o+, J8o+, T8o+, 98o, 87o, 76o, 65o
- **6 BB (29 %)** : 22+, A2s+, K6s+, Q8s+, J7s+, T7s+, 97s+, 86s+, 75s+, 65s, 54s, A7o+, KTo+, QTo+, JTo
- **8 BB (18 %)** : 33+, A7s+, K9s+, Q9s+, J9s+, T9s, 98s, A9o+, KJo+, QJo
- **10 BB (13 %)** : 44+, A9s+, KTs+, QTs+, JTs, T9s, ATo+, KQo
- **12 BB (10 %)** : 55+, ATs+, KTs+, QJs, JTs, AJo+
- **15 BB (8 %)** : 66+, ATs+, KQs, AJo+

## 4. Heads-up : ranges à jouer

Une fois un joueur éliminé, il ne reste que le SB (bouton) et le BB. Ces ranges supposent des stacks égaux.

### SB : push

- **4 BB (74 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 54s, A2o+, K2o+, Q2o+, J2o+, T5o+, 96o+, 86o+, 76o
- **6 BB (69 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q2o+, J5o+, T7o+, 97o+, 86o+, 76o  
  *marges : 94s 7%, 86o 93%, 63s 70%*
- **8 BB (62 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 74s+, 64s+, 53s+, A2o+, K2o+, Q5o+, J7o+, T7o+, 97o+, 87o, 76o  
  *marges : Q4o 15%*
- **10 BB (58 %)** : 22+, A2s+, K2s+, Q2s+, J3s+, T4s+, 95s+, 84s+, 74s+, 64s+, 53s+, 43s, A2o+, K2o+, Q7o+, J8o+, T8o+, 97o+, 87o, 76o  
  *marges : 43s 77%*
- **12 BB (53 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 95s+, 85s+, 74s+, 64s+, 53s+, A2o+, K3o+, Q8o+, J8o+, T8o+, 98o, 87o  
  *marges : T5s 24%*
- **15 BB (46 %)** : 22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 96s+, 85s+, 75s+, 64s+, 54s, A2o+, K6o+, Q9o+, J9o+, T8o+, 98o  
  *marges : Q4s 74%, J5s 6%*

### BB : call du push du SB

- **4 BB (74 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 53s+, A2o+, K2o+, Q2o+, J2o+, T5o+, 96o+, 86o+, 76o
- **6 BB (54 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 97s+, 87s, A2o+, K2o+, Q4o+, J7o+, T8o+, 98o  
  *marges : 98o 95%*
- **8 BB (44 %)** : 22+, A2s+, K2s+, Q4s+, J7s+, T8s+, 98s, A2o+, K2o+, Q8o+, J9o+, T9o  
  *marges : Q7o 50%*
- **10 BB (37 %)** : 22+, A2s+, K2s+, Q7s+, J8s+, T9s, A2o+, K5o+, Q9o+, JTo  
  *marges : Q6s 21%*
- **12 BB (33 %)** : 22+, A2s+, K4s+, Q8s+, J9s+, A2o+, K7o+, QTo+, JTo
- **15 BB (29 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A2o+, K9o+, QTo+  
  *marges : QTo 72%*

## 5. Comportement selon le stack

- **La règle d'ensemble : plus le stack baisse, plus tu élargis.** Chaque BB en moins ajoute environ 2 à 3 points de push au BTN et 3 à 4 points au SB (de 15 à 6 BB : BTN 27 → 38 %, SB 45 → 67 %).
- **Le SB est le joueur le plus agressif.** Quand le BTN a foldé, il ne reste qu'un adversaire : il pousse 45 % de ses mains à 15 BB et plus de 65 % à 6 BB. Le BTN, lui, laisse deux joueurs derrière et pousse nettement moins large.
- **Face à un push, appelle plus serré qu'en heads-up.** À 10 BB, le BB call 36 % contre le SB, mais seulement 24 % contre le BTN, et 13 % si un deuxième joueur est déjà all-in. Plus il y a de joueurs concernés, plus il faut une vraie main.
- **À 4 BB, c'est presque un jeu à pile ou face** : le BB call 73 % de ses mains contre le SB. Ne foldes pas par réflexe des mains qui ont plus de 40 % d'équité.
- **De 12 à 15 BB**, le modèle devient moins fiable : les ranges de push sont plus étroites et une partie de ta stratégie réelle (raise normal, petit raise) n'est pas couverte. Utilise ces ranges comme plancher pour les mains que tu pousses, pas comme règle absolue.
- **Mains marginales** : celles signalées en « marges » dans la section 3 sont jouées de façon mixte. L'écart d'EV entre push et fold y est très faible (de l'ordre de 0,01 BB ou moins sur les cas testés), donc ne t'attarde pas sur elles.

## 6. Adaptation aux adversaires

Un profil est modélisé en élargissant ou en resserrant la range d'équilibre de l'adversaire : « appelle ×0,6 » signifie qu'il call 40 % de mains en moins que l'équilibre (il retire les plus faibles), « appelle ×1,5 » qu'il en call 50 % de plus. Les gains sont en millième de BB (mBB) par fois que le spot se présente.

### 6.1 Quand tu pousses

| Stack | Équilibre BTN / SB | Adversaires nits (×0,6) | Adversaires larges (×1,5) | Adversaires très larges (×2) |
|---|---|---|---|---|
| 6 BB | 39 % / 67 % | 99 % / 100 % (+128 / +130 mBB) | 33 % / 59 % (+11 / +27) | 35 % / 63 % (+13 / +25) |
| 8 BB | 35 % / 63 % | 99 % / 100 % (+138 / +142 mBB) | 29 % / 49 % (+14 / +39) | 30 % / 54 % (+22 / +42) |
| 10 BB | 33 % / 57 % | 94 % / 100 % (+123 / +155 mBB) | 26 % / 43 % (+18 / +50) | 28 % / 48 % (+29 / +79) |
| 12 BB | 32 % / 51 % | 92 % / 100 % (+124 / +159 mBB) | 24 % / 38 % (+23 / +45) | 24 % / 44 % (+35 / +71) |
| 15 BB | 27 % / 45 % | 85 % / 100 % (+113 / +159 mBB) | 20 % / 35 % (+26 / +43) | 22 % / 37 % (+41 / +73) |
- **Contre des nits** (ceux qui fold presque tout face à un push) : pousse presque toutes tes mains, 85 à 99 % au BTN et 100 % au SB. Le gain est de l'ordre de 0,11 à 0,14 BB par push au BTN et de 0,13 à 0,16 BB au SB.
- **Contre des adversaires qui appellent trop** : resserre, en poussant pour la valeur. À 10 BB, BTN 33 → 26 % et SB 57 → 43 % contre un adversaire qui call 50 % de mains en plus. Le gain à exploiter est de 11 à 50 mBB par spot, et monte jusqu'à environ 80 mBB au SB contre un adversaire qui appelle ×2.

### 6.2 Quand tu appelles

| Stack | Adversaire serré (pousse ×0,6) : BB vs SB / BB vs BTN / SB vs BTN | Équilibre | Adversaire large (pousse ×1,4) |
|---|---|---|---|
| 6 BB | 32 / 25 / 17 % | 54 / 37 / 29 % | 72 / 48 / 36 % |
| 8 BB | 27 / 17 / 13 % | 44 / 29 / 22 % | 60 / 37 / 30 % |
| 10 BB | 23 / 13 / 10 % | 37 / 24 / 18 % | 52 / 32 / 28 % |
| 12 BB | 18 / 11 / 9 % | 32 / 20 / 16 % | 44 / 30 / 26 % |
| 15 BB | 14 / 9 / 8 % | 28 / 16 / 13 % | 37 / 24 / 21 % |
- **Contre un maniaque** (pousse beaucoup) : élargis tes calls d'environ 40 %. À 6 BB, le BB appelle 72 % de ses mains face à un SB qui pousse ×1,4.
- **Contre un joueur serré** : resserre tes calls d'environ 40 %. À 15 BB, le BB appelle 14 % de ses mains face à un SB serré, contre 28 % à l'équilibre.

### 6.3 Repérer le profil (règles de terrain, pas issues du modèle)

- **Nit** : fold presque toujours face à un push, ne défend pas ses blinds, ne pousse qu'avec de très bonnes mains.
- **Joueur qui appelle trop** : call des pushs avec des mains marginales (Kx, Qx offsuit), voit beaucoup de flops, ne fold presque jamais en blind.
- **Maniaque** : pousse presque toutes ses mains en position tardive, relance sans arrêt.
- **Avant de dévier de l'équilibre**, attends quelques mains d'observation. Sans lecture claire, joue la range d'équilibre : elle ne perd rien contre personne.
- **Dévie dans le bon sens** : contre quelqu'un qui appelle peu, élargis ton push. Contre quelqu'un qui appelle beaucoup, resserre-le. Contre quelqu'un qui pousse beaucoup, élargis ton call. Contre quelqu'un qui pousse peu, resserre ton call.

## 7. Tests effectués et fiabilité

| Test | Résultat |
|---|---|
| Simulation complète avec vraies cartes (2,5 M de parties par cas, 30 situations à 10 BB) contre le modèle | Écart moyen 0,010 BB, écart maximal 0,031 BB (bruit statistique de la simulation). Les formules de gain et les blockers sont corrects. |
| Somme des gains des trois joueurs | Nulle (précision de 10⁻⁷) : aucune erreur de comptabilité des jetons. |
| Écart à l'équilibre | Inférieur à 0,0001 BB par main pour les 6 stacks, 3 joueurs comme heads-up. |
| Bruit des équités (deux séries de tirages indépendantes) | Écart moyen de fréquence inférieur à 1,2 point par situation, 0 à 2 mains avec une décision opposée. |
| Convergence (2 000 contre 5 000 itérations) | Écart inférieur à 0,01 point de fréquence. |
| Comparaison à des chiffres publiés (heads-up, 10 BB) | Si le BB call les 34,8 % meilleures mains, la meilleure réponse du SB pousse 65,0 % (publié : 62,3 %). À 29 % de call, il pousse 92 % (publié : presque tout, 63o rentable). Écart de 2 à 3 points, compatible avec des structures de gains légèrement différentes. |
| Cohérence de force des mains | 49 incohérences sur 12 744 comparaisons (par exemple 87s joué et 97s non). Toutes portent sur des mains dont l'écart d'EV est inférieur à 0,01 BB : ce sont des marges d'indifférence, pas des erreurs. |
| Arrondi de la stratégie à 0 ou 100 % | Coût inférieur à 0,3 mBB par main d'écart à l'équilibre : les ranges arrondies de ce guide sont aussi bonnes que les mixtes en pratique. |

Améliorations apportées pendant les tests : prise en compte exacte des blockers (cartes bloquées entre joueurs), données d'équité trois à cinq fois plus précises, vérification par simulation avec vraies cartes. L'effet sur les ranges est modéré : 0,6 à 4 points de fréquence en moyenne par situation, jusqu'à 7 points pour le push BTN à 15 BB.

## 8. Limites et pistes

- **Stacks inégaux** : non modélisés. C'est la limite la plus importante en pratique. Piste : résoudre des configurations typiques (15 / 10 / 5 BB, par exemple).
- **Au-delà de 12 à 15 BB** : raises, limps, 3-bets à taille réelle non couverts. Les tentatives précédentes de modéliser ces cas ont montré que les résultats dépendaient trop de deux paramètres post-flop non calibrés : je ne les inclus pas dans ce guide.
- **Ante** : non pris en compte. Si la structure en comporte, les ranges s'élargissent légèrement.
- **Équités à 3 mains** : estimées par tirages (précision de quelques points sur les cas rares). Elles pèsent peu sur les ranges, car les situations à trois joueurs all-in sont rares.
- **Aucune comparaison à un solveur commercial** : mes seules références externes sont les chiffres publiés cités plus haut.