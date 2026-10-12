# Push/fold à 3 joueurs (BTN / SB / BB) en chip EV — Expresso

Hypothèses : stacks égaux, SB 0,5 / BB 1, pas d'ante, gagnant prend tout (ICM = chip EV), équités à 3 mains estimées par Monte Carlo, mains indépendantes (pas de card removal entre joueurs). Fréquences mixtes entre 5 % et 95 %.

## Stack 4 BB

**BTN — push (43 %)** : 22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, A2o+, K5o+, Q8o+, J9o+, T9o  |  mixtes : Q4s 69%

**SB — open-shove après fold du BTN (74 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 84s+, 74s+, 64s+, 53s+, A2o+, K2o+, Q2o+, J2o+, T5o+, 96o+, 86o+, 76o  |  mixtes : 43s 44%

**SB — call du push BTN (35 %)** : 22+, A2s+, K3s+, Q7s+, J8s+, T8s+, 98s, 87s, A2o+, K8o+, Q9o+, JTo

**BB — call du push SB (BTN fold) (73 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 53s+, A2o+, K2o+, Q2o+, J2o+, T6o+, 96o+, 86o+  |  mixtes : 76o 84%

**BB — call du push BTN (SB fold) (60 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q5o+, J7o+, T8o+, 98o, 87o, 76o  |  mixtes : 84s 6%

**BB — call face à BTN push + SB call (51 %)** : 22+, A2s+, K2s+, Q3s+, J3s+, T4s+, 95s+, 84s+, 74s+, 63s+, 52s+, 43s, A2o+, K8o+, Q9o+, J9o+, T8o+, 98o, 87o, 76o, 65o  |  mixtes : Q2s 80%

## Stack 6 BB

**BTN — push (38 %)** : 22+, A2s+, K2s+, Q6s+, J7s+, T7s+, 96s+, 86s+, 75s+, 65s, 54s, A2o+, K8o+, QTo+, JTo  |  mixtes : Q9o 72%

**SB — open-shove après fold du BTN (68 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 95s+, 84s+, 74s+, 63s+, 52s+, 43s, A2o+, K2o+, Q2o+, J6o+, T7o+, 97o+, 87o, 76o, 65o  |  mixtes : 93s 28%

**SB — call du push BTN (26 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A4o+, K9o+, QJo  |  mixtes : QTo 42%

**BB — call du push SB (BTN fold) (54 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 97s+, 87s, A2o+, K2o+, Q4o+, J7o+, T8o+  |  mixtes : 98o 67%

**BB — call du push BTN (SB fold) (37 %)** : 22+, A2s+, K2s+, Q6s+, J8s+, T8s+, 98s, 87s, A2o+, K7o+, Q9o+, JTo

**BB — call face à BTN push + SB call (25 %)** : 22+, A3s+, K8s+, Q8s+, J8s+, T7s+, 97s+, 86s+, 76s, 65s, A8o+, KTo+, QJo  |  mixtes : JTo 25%

## Stack 8 BB

**BTN — push (35 %)** : 22+, A2s+, K4s+, Q8s+, J8s+, T7s+, 96s+, 86s+, 75s+, 65s, 54s, A2o+, K9o+, QTo+, JTo  |  mixtes : Q6s 29%, J7s 35%

**SB — open-shove après fold du BTN (62 %)** : 22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q5o+, J8o+, T8o+, 97o+, 87o, 76o, 65o  |  mixtes : J7o 63%

**SB — call du push BTN (21 %)** : 22+, A2s+, K9s+, QTs+, A7o+, KTo+  |  mixtes : A6o 10%, JTs 86%

**BB — call du push SB (BTN fold) (44 %)** : 22+, A2s+, K2s+, Q4s+, J7s+, T8s+, 98s, A2o+, K3o+, Q8o+, J9o+, T9o  |  mixtes : Q7o 82%

**BB — call du push BTN (SB fold) (29 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A2o+, K9o+, QTo+  |  mixtes : K6s 71%

**BB — call face à BTN push + SB call (14 %)** : 33+, A8s+, KTs+, QTs+, J9s+, T9s, 98s, ATo+, KQo

## Stack 10 BB

**BTN — push (33 %)** : 22+, A2s+, K5s+, Q8s+, J8s+, T7s+, 96s+, 86s+, 75s+, 65s, 54s, A3o+, KTo+, QTo+, JTo  |  mixtes : T9o 15%

**SB — open-shove après fold du BTN (58 %)** : 22+, A2s+, K2s+, Q2s+, J3s+, T4s+, 95s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K2o+, Q8o+, J8o+, T8o+, 98o, 87o, 76o  |  mixtes : 97o 86%, 65o 45%

**SB — call du push BTN (17 %)** : 33+, A5s+, KTs+, QJs, A8o+, KJo+  |  mixtes : A7o 11%, A4s 83%

**BB — call du push SB (BTN fold) (37 %)** : 22+, A2s+, K2s+, Q6s+, J8s+, T9s, A2o+, K6o+, Q9o+, JTo  |  mixtes : J9o 68%

**BB — call du push BTN (SB fold) (23 %)** : 22+, A2s+, K9s+, QTs+, JTs, A5o+, KTo+, QJo

**BB — call face à BTN push + SB call (12 %)** : 44+, A9s+, KJs+, QTs+, JTs, ATo+  |  mixtes : KQo 17%

## Stack 12 BB

**BTN — push (29 %)** : 22+, A2s+, K6s+, Q8s+, J8s+, T7s+, 97s+, 86s+, 76s, 65s, A7o+, A5o, KTo+, QJo, JTo  |  mixtes : A6o 22%, QTo 47%, 96s 41%, 75s 83%

**SB — open-shove après fold du BTN (52 %)** : 22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 95s+, 85s+, 74s+, 64s+, 53s+, 43s, A2o+, K5o+, Q9o+, J9o+, T8o+, 98o, 87o, 76o  |  mixtes : K4o 7%, Q8o 93%

**SB — call du push BTN (15 %)** : 44+, A7s+, KTs+, QJs, A9o+, KJo+  |  mixtes : A8o 78%

**BB — call du push SB (BTN fold) (33 %)** : 22+, A2s+, K5s+, Q8s+, J9s+, A2o+, K8o+, QTo+, JTo  |  mixtes : K7o 83%, Q9o 22%

**BB — call du push BTN (SB fold) (19 %)** : 33+, A3s+, KTs+, QTs+, A7o+, KJo+  |  mixtes : KTo 29%

**BB — call face à BTN push + SB call (9 %)** : 55+, ATs+, KQs, AJo+

## Stack 15 BB

**BTN — push (25 %)** : 22+, A2s+, K6s+, Q8s+, J8s+, T7s+, 97s+, 86s+, 75s+, 65s, A8o+, KJo+  |  mixtes : QJo 95%, JTo 19%, 96s 87%

**SB — open-shove après fold du BTN (46 %)** : 22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 95s+, 85s+, 75s+, 64s+, 53s+, A2o+, K7o+, QTo+, J9o+, T8o+, 98o, 87o  |  mixtes : J5s 6%, 74s 68%

**SB — call du push BTN (11 %)** : 55+, A8s+, KJs+, ATo+, KQo

**BB — call du push SB (BTN fold) (27 %)** : 22+, A2s+, K7s+, Q9s+, JTs, A4o+, K9o+, QTo+  |  mixtes : A3o 40%

**BB — call du push BTN (SB fold) (15 %)** : 44+, A7s+, KTs+, A9o+, KJo+  |  mixtes : QJs 87%

**BB — call face à BTN push + SB call (6 %)** : 77+, AJs+, AQo+
