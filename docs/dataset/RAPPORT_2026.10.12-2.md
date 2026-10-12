# Rapport du dataset `gto_preflop` 2026.10.12-2

Généré par `python -m spinsacademy.report --version 2026.10.12-2` à partir des fichiers publiés. Statut : **staging**. Importeur 1.1.0.

## 1. Import

- Exports retenus : **39** ; écartés : **15**.
- Spots publiés : **287** ; questions proposables (couples spot × main) : **45 708**.
- Empreinte de `spots.jsonl` : `0711cd658a911ca2…` (conforme).

| Export écarté | Raison |
|---|---|
| `data/hrc/raw/complement2/hand_7` | stacks déjà couverts par un export plus récent |
| `data/hrc/raw/complement2/hand_10` | stacks déjà couverts par un export plus récent |
| `data/hrc/raw/complement/hand_4` | stacks déjà couverts par un export plus récent |
| `data/hrc/raw/min_raise_hu/hand_17` | stacks déjà couverts par un export plus récent |
| `data/hrc/raw/min_raise_3way/hand_4` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_5` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_6` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_7` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_8` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_9` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_10` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_11` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_12` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_13` | arbre préflop différent |
| `data/hrc/raw/min_raise_3way/hand_14` | arbre préflop différent |

| Export retenu | Table | Stacks (BB) | Postflop HRC | Spots | Questions |
|---|---|---|---|---|---|
| `data/hrc/raw/v2/hand_1` | 3-handed | 8 / 8 / 8 | general | 10 | 1 626 |
| `data/hrc/raw/v2/hand_2` | 3-handed | 10 / 10 / 10 | general | 11 | 1 783 |
| `data/hrc/raw/v2/hand_3` | 3-handed | 12 / 12 / 12 | general | 11 | 1 768 |
| `data/hrc/raw/v2/hand_4` | 3-handed | 16 / 16 / 16 | general | 10 | 1 597 |
| `data/hrc/raw/v2/hand_5` | 3-handed | 18 / 18 / 18 | general | 10 | 1 571 |
| `data/hrc/raw/v2/hand_6` | 3-handed | 22 / 22 / 22 | general | 8 | 1 243 |
| `data/hrc/raw/v2/hand_7` | 3-handed | 25 / 25 / 25 | general | 8 | 1 271 |
| `data/hrc/raw/v2/hand_8` | heads-up | 14 / 14 | general | 4 | 641 |
| `data/hrc/raw/v2/hand_9` | heads-up | 16 / 16 | general | 3 | 497 |
| `data/hrc/raw/v2/hand_10` | heads-up | 22 / 22 | general | 3 | 496 |
| `data/hrc/raw/complement2/hand_1` | 3-handed | 4 / 8 / 8 | simple | 8 | 1 276 |
| `data/hrc/raw/complement2/hand_2` | 3-handed | 8 / 4 / 8 | simple | 10 | 1 601 |
| `data/hrc/raw/complement2/hand_3` | 3-handed | 8 / 8 / 4 | simple | 10 | 1 598 |
| `data/hrc/raw/complement2/hand_4` | 3-handed | 8 / 4 / 4 | simple | 8 | 1 229 |
| `data/hrc/raw/complement2/hand_5` | 3-handed | 4 / 8 / 4 | simple | 8 | 1 251 |
| `data/hrc/raw/complement2/hand_6` | 3-handed | 4 / 4 / 8 | simple | 8 | 1 244 |
| `data/hrc/raw/complement2/hand_8` | heads-up | 4 / 8 | simple | 3 | 482 |
| `data/hrc/raw/complement2/hand_9` | heads-up | 8 / 4 | simple | 3 | 488 |
| `data/hrc/raw/complement2/hand_11` | heads-up | 15 / 15 | simple | 4 | 641 |
| `data/hrc/raw/complement2/hand_12` | heads-up | 12 / 12 | simple | 4 | 648 |
| `data/hrc/raw/complement2/hand_13` | heads-up | 20 / 20 | simple | 3 | 493 |
| `data/hrc/raw/complement2/hand_14` | 3-handed | 20 / 20 / 20 | simple | 8 | 1 272 |
| `data/hrc/raw/complement2/hand_15` | 3-handed | 14 / 14 / 14 | simple | 11 | 1 762 |
| `data/hrc/raw/complement2/hand_16` | 3-handed | 14 / 18 / 18 | simple | 10 | 1 587 |
| `data/hrc/raw/complement2/hand_17` | 3-handed | 18 / 12 / 18 | simple | 11 | 1 762 |
| `data/hrc/raw/complement2/hand_18` | 3-handed | 18 / 18 / 12 | simple | 11 | 1 785 |
| `data/hrc/raw/complement2/hand_19` | 3-handed | 18 / 12 / 12 | simple | 11 | 1 770 |
| `data/hrc/raw/complement2/hand_20` | 3-handed | 12 / 18 / 12 | simple | 11 | 1 763 |
| `data/hrc/raw/complement2/hand_21` | 3-handed | 12 / 12 / 18 | simple | 11 | 1 755 |
| `data/hrc/raw/complement/hand_1` | 3-handed | 4 / 4 / 4 | simple | 8 | 1 244 |
| `data/hrc/raw/complement/hand_2` | 3-handed | 6 / 6 / 6 | simple | 10 | 1 601 |
| `data/hrc/raw/complement/hand_3` | 3-handed | 15 / 15 / 15 | simple | 11 | 1 748 |
| `data/hrc/raw/min_raise_hu/hand_15` | heads-up | 25 / 25 | simple | 3 | 496 |
| `data/hrc/raw/min_raise_hu/hand_16` | heads-up | 18 / 18 | simple | 5 | 732 |
| `data/hrc/raw/min_raise_hu/hand_18` | heads-up | 10 / 10 | simple | 7 | 973 |
| `data/hrc/raw/min_raise_hu/hand_19` | heads-up | 8 / 8 | simple | 3 | 506 |
| `data/hrc/raw/min_raise_hu/hand_20` | heads-up | 6 / 6 | simple | 3 | 507 |
| `data/hrc/raw/min_raise_hu/hand_21` | heads-up | 4 / 4 | simple | 3 | 494 |
| `data/hrc/raw/min_raise_hu/hand_22` | heads-up | 2 / 2 | simple | 3 | 507 |

Règle de sélection : arbre préflop `daa9aaa0` uniquement ; pour une même configuration de stacks, l'export le plus récent. Les doublons écartés ont le même arbre préflop ; la comparaison 12 / 12 / 12 (`data/hrc/README.md`) montre des fréquences identiques à 1 ou 2 points près.

## 2. Validation

| Contrôle (rejoué sur le fichier publié) | Échecs |
|---|---|
| actions en double | 0 |
| fold proposé sans mise à payer | 0 |
| check proposé face à une mise | 0 |
| mise au-delà du stack | 0 |
| classes manquantes | 0 |
| fréquences non normalisées | 0 |
| longueurs incohérentes | 0 |
| EV exacte manquante sur un spot « exact » | 0 |

La publication est refusée au moindre spot invalide. Deux tests injectent volontairement une anomalie (`tests/test_importer.py` : fréquences non normalisées, relance au-delà du stack) et vérifient que rien n'est publié.

## 3. Couverture

Une main est proposable si elle atteint le nœud (poids ≥ 0.05) et si la stratégie HRC est cohérente avec l'EV de référence (écart ≤ 60 mBB). « Atteintes » compte les mains au-dessus du seuil de poids ; « proposables » retire les incohérentes.

| Table | Stacks (BB) | Spots | Mains atteintes | Proposables | Retirées pour incohérence |
|---|---|---|---|---|---|
| 3-handed | 4 / 4 / 4 | 8 | 1 352 | 1 244 | 8,0 % |
| 3-handed | 4 / 4 / 8 | 8 | 1 352 | 1 244 | 8,0 % |
| 3-handed | 4 / 8 / 4 | 8 | 1 352 | 1 251 | 7,5 % |
| 3-handed | 4 / 8 / 8 | 8 | 1 352 | 1 276 | 5,6 % |
| 3-handed | 6 / 6 / 6 | 10 | 1 690 | 1 601 | 5,3 % |
| 3-handed | 8 / 4 / 4 | 8 | 1 352 | 1 229 | 9,1 % |
| 3-handed | 8 / 4 / 8 | 10 | 1 690 | 1 601 | 5,3 % |
| 3-handed | 8 / 8 / 4 | 10 | 1 690 | 1 598 | 5,4 % |
| 3-handed | 8 / 8 / 8 | 10 | 1 690 | 1 626 | 3,8 % |
| 3-handed | 10 / 10 / 10 | 11 | 1 859 | 1 783 | 4,1 % |
| 3-handed | 12 / 12 / 12 | 11 | 1 859 | 1 768 | 4,9 % |
| 3-handed | 12 / 12 / 18 | 11 | 1 859 | 1 755 | 5,6 % |
| 3-handed | 12 / 18 / 12 | 11 | 1 859 | 1 763 | 5,2 % |
| 3-handed | 14 / 14 / 14 | 11 | 1 859 | 1 762 | 5,2 % |
| 3-handed | 14 / 18 / 18 | 10 | 1 690 | 1 587 | 6,1 % |
| 3-handed | 15 / 15 / 15 | 11 | 1 859 | 1 748 | 6,0 % |
| 3-handed | 16 / 16 / 16 | 10 | 1 690 | 1 597 | 5,5 % |
| 3-handed | 18 / 12 / 12 | 11 | 1 859 | 1 770 | 4,8 % |
| 3-handed | 18 / 12 / 18 | 11 | 1 859 | 1 762 | 5,2 % |
| 3-handed | 18 / 18 / 12 | 11 | 1 859 | 1 785 | 4,0 % |
| 3-handed | 18 / 18 / 18 | 10 | 1 690 | 1 571 | 7,0 % |
| 3-handed | 20 / 20 / 20 | 8 | 1 352 | 1 272 | 5,9 % |
| 3-handed | 22 / 22 / 22 | 8 | 1 352 | 1 243 | 8,1 % |
| 3-handed | 25 / 25 / 25 | 8 | 1 352 | 1 271 | 6,0 % |
| heads-up | 2 / 2 | 3 | 507 | 507 | 0,0 % |
| heads-up | 4 / 4 | 3 | 507 | 494 | 2,6 % |
| heads-up | 4 / 8 | 3 | 507 | 482 | 4,9 % |
| heads-up | 6 / 6 | 3 | 507 | 507 | 0,0 % |
| heads-up | 8 / 4 | 3 | 507 | 488 | 3,7 % |
| heads-up | 8 / 8 | 3 | 507 | 506 | 0,2 % |
| heads-up | 10 / 10 | 7 | 990 | 973 | 1,7 % |
| heads-up | 12 / 12 | 4 | 676 | 648 | 4,1 % |
| heads-up | 14 / 14 | 4 | 676 | 641 | 5,2 % |
| heads-up | 15 / 15 | 4 | 676 | 641 | 5,2 % |
| heads-up | 16 / 16 | 3 | 507 | 497 | 2,0 % |
| heads-up | 18 / 18 | 5 | 747 | 732 | 2,0 % |
| heads-up | 20 / 20 | 3 | 507 | 493 | 2,8 % |
| heads-up | 22 / 22 | 3 | 507 | 496 | 2,2 % |
| heads-up | 25 / 25 | 3 | 507 | 496 | 2,2 % |

| Table | Position du héros | Questions | | Table | Famille de décision | Questions |
|---|---|---|---|---|---|---|
| 3-handed | BB | 19 262 | | 3-handed | face à un limp | 10 749 |
| 3-handed | BTN | 4 055 | | 3-handed | face à un tapis | 9 942 |
| 3-handed | SB | 13 790 | | 3-handed | face à une relance | 8 308 |
| heads-up | BB | 5 519 | | 3-handed | premier à parler | 8 108 |
| heads-up | SB | 3 082 | | heads-up | face à un limp | 2 476 |
|  |  |  | | heads-up | face à un tapis | 1 929 |
|  |  |  | | heads-up | face à une relance | 1 661 |
|  |  |  | | heads-up | premier à parler | 2 535 |

Les 169 classes sont proposables dans au moins 235 spots. Les moins représentées : QTs (235), T9s (238), Q9s (243), K6s (245), K5s (245), Q8s (245), JTs (245), A2s (246), K4s (246), A5s (248).

La couverture du catalogue de quiz (répartition réellement servie à l'utilisateur) dépendra du générateur de séries : à mesurer sur ses tirages.

## 4. Comparaison avec HRC

**Spots à EV exacte (49)** : décisions tout ou rien. Écart moyen entre l'EV HRC et l'EV exacte : **95 mBB**. Dans 137 cas sur 8 281 (1,7 %), l'action majoritaire de HRC perd plus de 20 mBB selon l'EV exacte. La correction suit l'EV exacte.

**Cohérence interne de HRC** (EV de la meilleure action moins EV de la stratégie HRC, sur l'EV de référence, mains atteintes, pondérées par combos) : médiane 0,5 mBB, 90ᵉ centile 27,0 mBB, 99ᵉ centile 108,9 mBB. Au-delà de 60 mBB, la main n'est pas proposée.

Détail par export et par nœud : `docs/hrc/VALIDATION_HRC.md`.

Limite : à 3 joueurs, l'EV exacte ne retire pas les cartes du joueur qui a foldé (`ev_exact_approximate`). Contrôle indépendant de la matrice d'équité : `spinsacademy/data/equity_169.json`.

## 5. Notation

Barème : correct ≤ 20 mBB de regret, ou ≤ 60 mBB pour une action jouée au moins 10 % du temps par HRC (spots à EV HRC) ; imprécision ≤ 60 mBB ; erreur au-delà. Regret = EV de la meilleure action − EV de l'action choisie, toutes deux relatives au fold, en mBB, sur l'EV de référence du spot.

| Verdict | Points | Réponses possibles (spot × main × action) | Part |
|---|---|---|---|
| correct | 1,0 | 54 987 | 42,9 % |
| imprécision | 0,5 | 4 737 | 3,7 % |
| erreur | 0,0 | 68 552 | 53,4 % |

Dont 4 271 réponses correctes grâce à la tolérance de stratégie mixte (regret entre 20 et 60 mBB).

### Exemples

| Verdict | Spot | Main | Action | Regret | Fréquence HRC | Meilleure action | Source EV |
|---|---|---|---|---|---|---|---|
| correct | `3w-8-4-4-BTN-allin_SB-fold-80d63e` | 98s | C | 0,0 mBB | 100 % | C | exact |
| correct | `3w-18-18-18-BTN-raise2.3_SB-fold-26f277` | TT | A | 0,0 mBB | 100 % | A | hrc |
| correct | `3w-12-12-12-BTN-raise2.3-11a89f` | A3o | F | 22,5 mBB | 54 % | A | hrc |
| correct | `3w-16-16-16-BTN-fold_SB-call-f3e5f4` | Q6o | R3 | 32,1 mBB | 13 % | X | hrc |
| imprécision | `hu-10-10-root-a2da5a` | 65s | R3.5 | 36,2 mBB | 7 % | A | hrc |
| imprécision | `3w-22-22-22-BTN-fold-669553` | T6s | R3.5 | 31,9 mBB | 0 % | C | hrc |
| imprécision | `3w-18-12-18-root-f6b4e5` | 44 | R2.3 | 32,8 mBB | 0 % | A | hrc |
| imprécision | `3w-12-12-12-BTN-fold_SB-call-36f31e` | A7o | X | 41,4 mBB | 0 % | A | hrc |
| erreur | `hu-10-10-SB-call_BB-raise3-d6f260` | 73s | A | 733,6 mBB | 0 % | F | hrc |
| erreur | `3w-4-8-4-BTN-fold-2763b0` | A2o | F | 889,0 mBB | 0 % | A | hrc |
| erreur | `3w-10-10-10-BTN-raise2.3_SB-fold-970467` | A7o | C | 384,4 mBB | 10 % | A | hrc |
| erreur | `3w-18-18-18-BTN-fold-2617f9` | 76s | R3.5 | 140,0 mBB | 2 % | C | hrc |

Ces exemples sont tirés au hasard (graine fixe) ; ils sont à faire relire par l'expert poker, en particulier les cas « correct » obtenus par la tolérance mixte et les « imprécision ».

