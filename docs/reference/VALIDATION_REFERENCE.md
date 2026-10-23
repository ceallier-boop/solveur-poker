# Validation des exports de référence

Généré par `python tools/hrc/validate.py`. Ne pas modifier à la main.

## Structure

| Export | Stacks (BB) | Arbre préflop | Postflop | Nœuds | Profondeur | Raises sans nœud fils | Anomalies |
|---|---|---|---|---|---|---|---|
| `data/hrc/raw/v2/hand_1` | 8 / 8 / 8 | `daa9aaa0` | general | 10 | 2 | 1 | — |
| `data/hrc/raw/v2/hand_2` | 10 / 10 / 10 | `daa9aaa0` | general | 11 | 2 | 1 | — |
| `data/hrc/raw/v2/hand_3` | 12 / 12 / 12 | `daa9aaa0` | general | 11 | 2 | 3 | — |
| `data/hrc/raw/v2/hand_4` | 16 / 16 / 16 | `daa9aaa0` | general | 10 | 2 | 3 | — |
| `data/hrc/raw/v2/hand_5` | 18 / 18 / 18 | `daa9aaa0` | general | 10 | 2 | 3 | — |
| `data/hrc/raw/v2/hand_6` | 22 / 22 / 22 | `daa9aaa0` | general | 8 | 2 | 6 | — |
| `data/hrc/raw/v2/hand_7` | 25 / 25 / 25 | `daa9aaa0` | general | 8 | 2 | 6 | — |
| `data/hrc/raw/v2/hand_8` | 14 / 14 | `daa9aaa0` | general | 4 | 1 | 1 | — |
| `data/hrc/raw/v2/hand_9` | 16 / 16 | `daa9aaa0` | general | 3 | 1 | 1 | — |
| `data/hrc/raw/v2/hand_10` | 22 / 22 | `daa9aaa0` | general | 3 | 1 | 2 | — |
| `data/hrc/raw/complement2/hand_1` | 4 / 8 / 8 | `daa9aaa0` | simple | 8 | 2 | 2 | — |
| `data/hrc/raw/complement2/hand_2` | 8 / 4 / 8 | `daa9aaa0` | simple | 10 | 2 | 1 | — |
| `data/hrc/raw/complement2/hand_3` | 8 / 8 / 4 | `daa9aaa0` | simple | 10 | 2 | 0 | — |
| `data/hrc/raw/complement2/hand_4` | 8 / 4 / 4 | `daa9aaa0` | simple | 8 | 2 | 0 | — |
| `data/hrc/raw/complement2/hand_5` | 4 / 8 / 4 | `daa9aaa0` | simple | 8 | 2 | 1 | — |
| `data/hrc/raw/complement2/hand_6` | 4 / 4 / 8 | `daa9aaa0` | simple | 8 | 2 | 2 | — |
| `data/hrc/raw/complement2/hand_7` | 12 / 12 / 12 | `daa9aaa0` | simple | 11 | 2 | 3 | — |
| `data/hrc/raw/complement2/hand_8` | 4 / 8 | `daa9aaa0` | simple | 3 | 1 | 1 | — |
| `data/hrc/raw/complement2/hand_9` | 8 / 4 | `daa9aaa0` | simple | 3 | 1 | 0 | — |
| `data/hrc/raw/complement2/hand_10` | 4 / 8 | `daa9aaa0` | simple | 3 | 1 | 1 | — |
| `data/hrc/raw/complement2/hand_11` | 15 / 15 | `daa9aaa0` | simple | 4 | 1 | 1 | — |
| `data/hrc/raw/complement2/hand_12` | 12 / 12 | `daa9aaa0` | simple | 4 | 1 | 1 | — |
| `data/hrc/raw/complement2/hand_13` | 20 / 20 | `daa9aaa0` | simple | 3 | 1 | 1 | — |
| `data/hrc/raw/complement2/hand_14` | 20 / 20 / 20 | `daa9aaa0` | simple | 8 | 2 | 5 | — |
| `data/hrc/raw/complement2/hand_15` | 14 / 14 / 14 | `daa9aaa0` | simple | 11 | 2 | 3 | — |
| `data/hrc/raw/complement2/hand_16` | 14 / 18 / 18 | `daa9aaa0` | simple | 10 | 2 | 5 | — |
| `data/hrc/raw/complement2/hand_17` | 18 / 12 / 18 | `daa9aaa0` | simple | 11 | 2 | 5 | — |
| `data/hrc/raw/complement2/hand_18` | 18 / 18 / 12 | `daa9aaa0` | simple | 11 | 2 | 3 | — |
| `data/hrc/raw/complement2/hand_19` | 18 / 12 / 12 | `daa9aaa0` | simple | 11 | 2 | 3 | — |
| `data/hrc/raw/complement2/hand_20` | 12 / 18 / 12 | `daa9aaa0` | simple | 11 | 2 | 5 | — |
| `data/hrc/raw/complement2/hand_21` | 12 / 12 / 18 | `daa9aaa0` | simple | 11 | 2 | 7 | — |
| `data/hrc/raw/complement/hand_1` | 4 / 4 / 4 | `daa9aaa0` | simple | 8 | 2 | 0 | — |
| `data/hrc/raw/complement/hand_2` | 6 / 6 / 6 | `daa9aaa0` | simple | 10 | 2 | 0 | — |
| `data/hrc/raw/complement/hand_3` | 15 / 15 / 15 | `daa9aaa0` | simple | 11 | 2 | 3 | — |
| `data/hrc/raw/complement/hand_4` | 15 / 15 | `daa9aaa0` | simple | 4 | 1 | 1 | — |
| `data/hrc/raw/min_raise_hu/hand_15` | 25 / 25 | `daa9aaa0` | simple | 3 | 1 | 2 | — |
| `data/hrc/raw/min_raise_hu/hand_16` | 18 / 18 | `daa9aaa0` | simple | 5 | 2 | 0 | — |
| `data/hrc/raw/min_raise_hu/hand_17` | 12 / 12 | `daa9aaa0` | simple | 4 | 1 | 1 | — |
| `data/hrc/raw/min_raise_hu/hand_18` | 10 / 10 | `daa9aaa0` | simple | 7 | 2 | 0 | — |
| `data/hrc/raw/min_raise_hu/hand_19` | 8 / 8 | `daa9aaa0` | simple | 3 | 1 | 1 | — |
| `data/hrc/raw/min_raise_hu/hand_20` | 6 / 6 | `daa9aaa0` | simple | 3 | 1 | 0 | — |
| `data/hrc/raw/min_raise_hu/hand_21` | 4 / 4 | `daa9aaa0` | simple | 3 | 1 | 0 | — |
| `data/hrc/raw/min_raise_hu/hand_22` | 2 / 2 | `daa9aaa0` | simple | 3 | 1 | 0 | — |
| `data/hrc/raw/min_raise_3way/hand_4` | 25 / 25 / 25 | `16c57008` | simple | 6 | 2 | 4 | — |
| `data/hrc/raw/min_raise_3way/hand_5` | 18 / 18 / 18 | `16c57008` | simple | 15 | 3 | 0 | — |
| `data/hrc/raw/min_raise_3way/hand_6` | 12 / 12 / 12 | `16c57008` | simple | 9 | 2 | 1 | — |
| `data/hrc/raw/min_raise_3way/hand_7` | 10 / 10 / 10 | `16c57008` | simple | 9 | 2 | 1 | — |
| `data/hrc/raw/min_raise_3way/hand_8` | 8 / 8 / 8 | `16c57008` | simple | 8 | 2 | 1 | — |
| `data/hrc/raw/min_raise_3way/hand_9` | 12 / 21 / 21 | `16c57008` | simple | 8 | 2 | 3 | — |
| `data/hrc/raw/min_raise_3way/hand_10` | 21 / 12 / 21 | `16c57008` | simple | 7 | 2 | 4 | — |
| `data/hrc/raw/min_raise_3way/hand_11` | 21 / 21 / 12 | `16c57008` | simple | 7 | 2 | 2 | — |
| `data/hrc/raw/min_raise_3way/hand_12` | 8 / 14 / 14 | `16c57008` | simple | 9 | 2 | 2 | — |
| `data/hrc/raw/min_raise_3way/hand_13` | 14 / 8 / 14 | `16c57008` | simple | 8 | 2 | 2 | — |
| `data/hrc/raw/min_raise_3way/hand_14` | 14 / 14 / 8 | `16c57008` | simple | 8 | 2 | 1 | — |

« Profondeur » : nombre maximal d'actions avant un nœud exporté. « Raises sans nœud fils » : relances non all-in dont la suite n'est pas exportée.

## EV de référence contre EV exacte sur les calls d'all-in

Écart entre l'EV du call exportée par la référence et l'EV exacte (chip EV, bloqueurs compris) calculée à partir de la range de shove exportée. Une « décision fausse » est une main où la référence joue majoritairement l'action dont l'EV exacte est inférieure de plus de 20 mBB.

Heads-up : le calcul est exact. À 3 joueurs, il ignore les cartes du joueur qui a foldé : le biais négatif de quelques dizaines de mBB vient en partie de cette approximation, et les « décisions fausses » proches du seuil sont à confirmer.

| Export | Stacks | Nœud | Shove adverse | Écart moyen | Écart max | Biais | Décisions fausses |
|---|---|---|---|---|---|---|---|
| `data/hrc/raw/v2/hand_1` | 8 / 8 / 8 | BTN-fold_SB-allin | 54 % | 64 mBB | 221 mBB | -34 mBB | Q5s |
| `data/hrc/raw/v2/hand_1` | 8 / 8 / 8 | BTN-allin_SB-fold | 28 % | 67 mBB | 258 mBB | -33 mBB | T9s, 98s |
| `data/hrc/raw/v2/hand_2` | 10 / 10 / 10 | BTN-fold_SB-allin | 35 % | 90 mBB | 520 mBB | -50 mBB | K3s, 98s |
| `data/hrc/raw/v2/hand_2` | 10 / 10 / 10 | BTN-allin_SB-fold | 26 % | 87 mBB | 488 mBB | -30 mBB | K8s, Q9s |
| `data/hrc/raw/v2/hand_3` | 12 / 12 / 12 | BTN-fold_SB-allin | 28 % | 120 mBB | 535 mBB | -46 mBB | K6s, K5s, Q8s, K8o |
| `data/hrc/raw/v2/hand_3` | 12 / 12 / 12 | BTN-allin_SB-fold | 19 % | 117 mBB | 495 mBB | -25 mBB | A2s |
| `data/hrc/raw/v2/hand_4` | 16 / 16 / 16 | BTN-allin_SB-fold | 7 % | 236 mBB | 953 mBB | +10 mBB | A6s, QJs, JTs, 22 |
| `data/hrc/raw/v2/hand_5` | 18 / 18 / 18 | BTN-allin_SB-fold | 3 % | 326 mBB | 1703 mBB | -64 mBB | KJs, KTs, QTs, A8o |
| `data/hrc/raw/v2/hand_8` | 14 / 14 | SB-allin | 10 % | 139 mBB | 639 mBB | +6 mBB | K8s, J9s, J8s, QTo, T8s |
| `data/hrc/raw/complement2/hand_1` | 4 / 8 / 8 | BTN-fold_SB-allin | 51 % | 73 mBB | 297 mBB | -41 mBB | — |
| `data/hrc/raw/complement2/hand_1` | 4 / 8 / 8 | BTN-allin_SB-fold | 43 % | 36 mBB | 159 mBB | -18 mBB | T4s, T3s, 76o, Q4o, 43s |
| `data/hrc/raw/complement2/hand_2` | 8 / 4 / 8 | BTN-fold_SB-allin | 73 % | 29 mBB | 110 mBB | -18 mBB | 94s, 86o |
| `data/hrc/raw/complement2/hand_2` | 8 / 4 / 8 | BTN-allin_SB-fold | 32 % | 81 mBB | 265 mBB | -53 mBB | K5s, Q9s, Q8s |
| `data/hrc/raw/complement2/hand_3` | 8 / 8 / 4 | BTN-fold_SB-allin | 73 % | 33 mBB | 110 mBB | -21 mBB | 93s, 84s, 96o, 86o, 64s |
| `data/hrc/raw/complement2/hand_3` | 8 / 8 / 4 | BTN-allin_SB-fold | 30 % | 36 mBB | 204 mBB | -16 mBB | T4s, 84s, T7o, 97o, 63s |
| `data/hrc/raw/complement2/hand_4` | 8 / 4 / 4 | BTN-fold_SB-allin | 73 % | 34 mBB | 112 mBB | -18 mBB | 94s, 93s, 84s, 53s |
| `data/hrc/raw/complement2/hand_4` | 8 / 4 / 4 | BTN-allin_SB-fold | 42 % | 33 mBB | 171 mBB | -20 mBB | T5s, 84s, 74s, 63s, 53s |
| `data/hrc/raw/complement2/hand_5` | 4 / 8 / 4 | BTN-fold_SB-allin | 73 % | 35 mBB | 132 mBB | -22 mBB | 93s, 74s, 86o, 76o, 53s |
| `data/hrc/raw/complement2/hand_5` | 4 / 8 / 4 | BTN-allin_SB-fold | 43 % | 41 mBB | 157 mBB | -27 mBB | 84s, 83s, 63s |
| `data/hrc/raw/complement2/hand_6` | 4 / 4 / 8 | BTN-fold_SB-allin | 73 % | 30 mBB | 104 mBB | -22 mBB | 93s, 84s, 64s |
| `data/hrc/raw/complement2/hand_6` | 4 / 4 / 8 | BTN-allin_SB-fold | 42 % | 40 mBB | 130 mBB | -25 mBB | T3s, 84s, 97o, 74s, 76o |
| `data/hrc/raw/complement2/hand_7` | 12 / 12 / 12 | BTN-fold_SB-allin | 27 % | 136 mBB | 648 mBB | -63 mBB | K6s, JTo, T9s, T8s |
| `data/hrc/raw/complement2/hand_7` | 12 / 12 / 12 | BTN-allin_SB-fold | 20 % | 127 mBB | 531 mBB | -55 mBB | A2s, K9s, A5o |
| `data/hrc/raw/complement2/hand_8` | 4 / 8 | SB-allin | 74 % | 17 mBB | 82 mBB | +2 mBB | 63s |
| `data/hrc/raw/complement2/hand_9` | 8 / 4 | SB-allin | 74 % | 14 mBB | 73 mBB | +1 mBB | — |
| `data/hrc/raw/complement2/hand_10` | 4 / 8 | SB-allin | 74 % | 17 mBB | 76 mBB | -1 mBB | — |
| `data/hrc/raw/complement2/hand_11` | 15 / 15 | SB-allin | 8 % | 180 mBB | 976 mBB | -15 mBB | J9s, KTo, QTo, T8s, 98s |
| `data/hrc/raw/complement2/hand_12` | 12 / 12 | SB-allin | 15 % | 111 mBB | 452 mBB | -17 mBB | K6s, K4s, Q8s, J8s, T8s, T7s, 98s |
| `data/hrc/raw/complement2/hand_15` | 14 / 14 / 14 | BTN-fold_SB-allin | 21 % | 150 mBB | 737 mBB | -80 mBB | K8s, QTo, K9o |
| `data/hrc/raw/complement2/hand_15` | 14 / 14 / 14 | BTN-allin_SB-fold | 11 % | 167 mBB | 699 mBB | +17 mBB | KJo, 22 |
| `data/hrc/raw/complement2/hand_16` | 14 / 18 / 18 | BTN-allin_SB-fold | 12 % | 162 mBB | 816 mBB | -55 mBB | A6s, A5s, A4s, A3s, KJo, 22 |
| `data/hrc/raw/complement2/hand_17` | 18 / 12 / 18 | BTN-fold_SB-allin | 28 % | 118 mBB | 509 mBB | -60 mBB | K5s, J8s |
| `data/hrc/raw/complement2/hand_17` | 18 / 12 / 18 | BTN-allin_SB-fold | 7 % | 260 mBB | 1142 mBB | -35 mBB | A5s, QJs |
| `data/hrc/raw/complement2/hand_18` | 18 / 18 / 12 | BTN-fold_SB-allin | 27 % | 129 mBB | 559 mBB | -63 mBB | Q8s |
| `data/hrc/raw/complement2/hand_18` | 18 / 18 / 12 | BTN-allin_SB-fold | 7 % | 155 mBB | 793 mBB | -2 mBB | KJo |
| `data/hrc/raw/complement2/hand_19` | 18 / 12 / 12 | BTN-fold_SB-allin | 27 % | 122 mBB | 496 mBB | -81 mBB | Q8s, K8o |
| `data/hrc/raw/complement2/hand_19` | 18 / 12 / 12 | BTN-allin_SB-fold | 19 % | 105 mBB | 475 mBB | -39 mBB | A2s, JTs |
| `data/hrc/raw/complement2/hand_20` | 12 / 18 / 12 | BTN-fold_SB-allin | 26 % | 119 mBB | 443 mBB | -65 mBB | T8s, K8o |
| `data/hrc/raw/complement2/hand_20` | 12 / 18 / 12 | BTN-allin_SB-fold | 18 % | 127 mBB | 680 mBB | -36 mBB | QTs, Q9s, KTo |
| `data/hrc/raw/complement2/hand_21` | 12 / 12 / 18 | BTN-fold_SB-allin | 27 % | 126 mBB | 500 mBB | -43 mBB | K6s, Q8s, J8s, T8s |
| `data/hrc/raw/complement2/hand_21` | 12 / 12 / 18 | BTN-allin_SB-fold | 19 % | 122 mBB | 513 mBB | -53 mBB | K9s |
| `data/hrc/raw/complement/hand_1` | 4 / 4 / 4 | BTN-fold_SB-allin | 73 % | 35 mBB | 114 mBB | -22 mBB | 94s, 84s, 74s, 96o, 76o, 53s |
| `data/hrc/raw/complement/hand_1` | 4 / 4 / 4 | BTN-allin_SB-fold | 42 % | 38 mBB | 131 mBB | -22 mBB | 74s, 76o, 43s |
| `data/hrc/raw/complement/hand_2` | 6 / 6 / 6 | BTN-fold_SB-allin | 63 % | 51 mBB | 165 mBB | -32 mBB | J4s, 98o, 86s, J7o |
| `data/hrc/raw/complement/hand_2` | 6 / 6 / 6 | BTN-allin_SB-fold | 33 % | 62 mBB | 312 mBB | -36 mBB | Q6s, 76s |
| `data/hrc/raw/complement/hand_3` | 15 / 15 / 15 | BTN-fold_SB-allin | 19 % | 157 mBB | 716 mBB | -69 mBB | K7s, QJo, T9s |
| `data/hrc/raw/complement/hand_3` | 15 / 15 / 15 | BTN-allin_SB-fold | 8 % | 203 mBB | 1024 mBB | -53 mBB | QTs, JTs |
| `data/hrc/raw/complement/hand_4` | 15 / 15 | SB-allin | 7 % | 211 mBB | 767 mBB | +8 mBB | KQo, KJo, QJo, J8s |
| `data/hrc/raw/min_raise_hu/hand_17` | 12 / 12 | SB-allin | 14 % | 101 mBB | 502 mBB | -20 mBB | K6s, QTo, T8s, 87s, A2o |
| `data/hrc/raw/min_raise_hu/hand_18` | 10 / 10 | SB-allin | 22 % | 74 mBB | 396 mBB | +3 mBB | — |
| `data/hrc/raw/min_raise_hu/hand_19` | 8 / 8 | SB-allin | 43 % | 42 mBB | 223 mBB | +5 mBB | Q4s, Q3s |
| `data/hrc/raw/min_raise_hu/hand_20` | 6 / 6 | SB-allin | 60 % | 27 mBB | 156 mBB | +4 mBB | — |
| `data/hrc/raw/min_raise_hu/hand_21` | 4 / 4 | SB-allin | 74 % | 18 mBB | 71 mBB | +1 mBB | 74s |
| `data/hrc/raw/min_raise_hu/hand_22` | 2 / 2 | SB-allin | 88 % | 7 mBB | 31 mBB | +1 mBB | — |
| `data/hrc/raw/min_raise_3way/hand_5` | 18 / 18 / 18 | BTN-allin_SB-fold | 4 % | 321 mBB | 1803 mBB | -94 mBB | A7s, A3s, JTs, A8o, A7o |
| `data/hrc/raw/min_raise_3way/hand_6` | 12 / 12 / 12 | BTN-fold_SB-allin | 27 % | 122 mBB | 579 mBB | -70 mBB | Q8s |
| `data/hrc/raw/min_raise_3way/hand_6` | 12 / 12 / 12 | BTN-allin_SB-fold | 19 % | 111 mBB | 446 mBB | -46 mBB | KTo |
| `data/hrc/raw/min_raise_3way/hand_7` | 10 / 10 / 10 | BTN-fold_SB-allin | 32 % | 96 mBB | 334 mBB | -39 mBB | K3s, K2s, J8s, 98s |
| `data/hrc/raw/min_raise_3way/hand_7` | 10 / 10 / 10 | BTN-allin_SB-fold | 28 % | 85 mBB | 334 mBB | -23 mBB | — |
| `data/hrc/raw/min_raise_3way/hand_8` | 8 / 8 / 8 | BTN-fold_SB-allin | 53 % | 63 mBB | 280 mBB | -38 mBB | Q5s, Q4s, T7s, K3o |
| `data/hrc/raw/min_raise_3way/hand_8` | 8 / 8 / 8 | BTN-allin_SB-fold | 30 % | 64 mBB | 376 mBB | -25 mBB | Q9s, QTo, T9s |
| `data/hrc/raw/min_raise_3way/hand_9` | 12 / 21 / 21 | BTN-allin_SB-fold | 20 % | 113 mBB | 585 mBB | -21 mBB | A2s |
| `data/hrc/raw/min_raise_3way/hand_10` | 21 / 12 / 21 | BTN-fold_SB-allin | 26 % | 120 mBB | 583 mBB | -63 mBB | K6s, K5s, Q8s |
| `data/hrc/raw/min_raise_3way/hand_11` | 21 / 21 / 12 | BTN-fold_SB-allin | 27 % | 110 mBB | 656 mBB | -25 mBB | JTo |
| `data/hrc/raw/min_raise_3way/hand_12` | 8 / 14 / 14 | BTN-fold_SB-allin | 22 % | 159 mBB | 707 mBB | -79 mBB | K7s, J9s, JTo, T8s |
| `data/hrc/raw/min_raise_3way/hand_12` | 8 / 14 / 14 | BTN-allin_SB-fold | 30 % | 63 mBB | 358 mBB | -30 mBB | K6s, T9s |
| `data/hrc/raw/min_raise_3way/hand_13` | 14 / 8 / 14 | BTN-fold_SB-allin | 53 % | 67 mBB | 279 mBB | -33 mBB | — |
| `data/hrc/raw/min_raise_3way/hand_13` | 14 / 8 / 14 | BTN-allin_SB-fold | 19 % | 134 mBB | 723 mBB | -40 mBB | QTs, QJo, A5o |
| `data/hrc/raw/min_raise_3way/hand_14` | 14 / 14 / 8 | BTN-fold_SB-allin | 54 % | 61 mBB | 249 mBB | -35 mBB | J7s, K3o |
| `data/hrc/raw/min_raise_3way/hand_14` | 14 / 14 / 8 | BTN-allin_SB-fold | 18 % | 81 mBB | 368 mBB | -19 mBB | K7s, QTo, T8s |
