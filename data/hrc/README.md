# Exports HRC de référence

**Ces fichiers ne doivent jamais être embarqués dans l'application** (frontend, API publique, bundle, datasets publiés). Ils servent uniquement de source pour générer, valider et documenter les datasets. Ils ont été obtenus légalement par le propriétaire du projet.

## Contenu

Ce dossier contient les mains exportées depuis HRC, toutes préflop (44 dans les premières bases, puis v2 et v3 ci-dessous). Chaque main a un fichier `settings.json` (configuration) et un dossier `nodes/*.json` (un fichier par nœud, avec la stratégie et les EV par classe de main).

Configuration commune :
- modèle : chip EV, sans rake ;
- blinds 0,5 / 1, ante à 0 ;
- moteur HRC Monte-Carlo ;
- tailles : open du BTN à 2,3 BB, open du SB à 3,5 BB, iso-raise du BB à 3 BB, puis all-in.

Seule différence d'arbre entre les dossiers : `min_raise_3way` interdit le limp du BTN.

La colonne « Clé `hrcdata` » donne la correspondance avec les scripts de `legacy/conversation/` (`hrcdata.load(kind, hand)`).

| Dossier | Main | Table | Stacks (BB) | Limp BTN autorisé | Nœuds | Empreinte arbre | Clé `hrcdata` |
|---|---|---|---|---|---|---|---|
| `complement/hand_1` | 1 | 3 joueurs | 4 / 4 / 4 | oui | 8 | `58407ad7` | `3wc/1` |
| `complement/hand_2` | 2 | 3 joueurs | 6 / 6 / 6 | oui | 10 | `58407ad7` | `3wc/2` |
| `complement/hand_3` | 3 | 3 joueurs | 15 / 15 / 15 | oui | 11 | `58407ad7` | `3wc/3` |
| `complement/hand_4` | 4 | heads-up | 15 / 15 | — | 4 | `58407ad7` | `huc/4` |
| `complement2/hand_1` | 1 | 3 joueurs | 4 / 8 / 8 | oui | 8 | `58407ad7` | `c2/1` |
| `complement2/hand_2` | 2 | 3 joueurs | 8 / 4 / 8 | oui | 10 | `58407ad7` | `c2/2` |
| `complement2/hand_3` | 3 | 3 joueurs | 8 / 8 / 4 | oui | 10 | `58407ad7` | `c2/3` |
| `complement2/hand_4` | 4 | 3 joueurs | 8 / 4 / 4 | oui | 8 | `58407ad7` | `c2/4` |
| `complement2/hand_5` | 5 | 3 joueurs | 4 / 8 / 4 | oui | 8 | `58407ad7` | `c2/5` |
| `complement2/hand_6` | 6 | 3 joueurs | 4 / 4 / 8 | oui | 8 | `58407ad7` | `c2/6` |
| `complement2/hand_7` | 7 | 3 joueurs | 12 / 12 / 12 | oui | 11 | `58407ad7` | `c2/7` |
| `complement2/hand_8` | 8 | heads-up | 4 / 8 | — | 3 | `58407ad7` | `c2/8` |
| `complement2/hand_9` | 9 | heads-up | 8 / 4 | — | 3 | `58407ad7` | `c2/9` |
| `complement2/hand_10` | 10 | heads-up | 4 / 8 | — | 3 | `58407ad7` | `c2/10` |
| `complement2/hand_11` | 11 | heads-up | 15 / 15 | — | 4 | `58407ad7` | `c2/11` |
| `complement2/hand_12` | 12 | heads-up | 12 / 12 | — | 4 | `58407ad7` | `c2/12` |
| `complement2/hand_13` | 13 | heads-up | 20 / 20 | — | 3 | `58407ad7` | `c2/13` |
| `complement2/hand_14` | 14 | 3 joueurs | 20 / 20 / 20 | oui | 8 | `58407ad7` | `c2/14` |
| `complement2/hand_15` | 15 | 3 joueurs | 14 / 14 / 14 | oui | 11 | `58407ad7` | `c2/15` |
| `complement2/hand_16` | 16 | 3 joueurs | 14 / 18 / 18 | oui | 10 | `58407ad7` | `c2/16` |
| `complement2/hand_17` | 17 | 3 joueurs | 18 / 12 / 18 | oui | 11 | `58407ad7` | `c2/17` |
| `complement2/hand_18` | 18 | 3 joueurs | 18 / 18 / 12 | oui | 11 | `58407ad7` | `c2/18` |
| `complement2/hand_19` | 19 | 3 joueurs | 18 / 12 / 12 | oui | 11 | `58407ad7` | `c2/19` |
| `complement2/hand_20` | 20 | 3 joueurs | 12 / 18 / 12 | oui | 11 | `58407ad7` | `c2/20` |
| `complement2/hand_21` | 21 | 3 joueurs | 12 / 12 / 18 | oui | 11 | `58407ad7` | `c2/21` |
| `min_raise_3way/hand_4` | 4 | 3 joueurs | 25 / 25 / 25 | non | 6 | `c22b0ad6` | `3w/4` |
| `min_raise_3way/hand_5` | 5 | 3 joueurs | 18 / 18 / 18 | non | 15 | `c22b0ad6` | `3w/5` |
| `min_raise_3way/hand_6` | 6 | 3 joueurs | 12 / 12 / 12 | non | 9 | `c22b0ad6` | `3w/6` |
| `min_raise_3way/hand_7` | 7 | 3 joueurs | 10 / 10 / 10 | non | 9 | `c22b0ad6` | `3w/7` |
| `min_raise_3way/hand_8` | 8 | 3 joueurs | 8 / 8 / 8 | non | 8 | `c22b0ad6` | `3w/8` |
| `min_raise_3way/hand_9` | 9 | 3 joueurs | 12 / 21 / 21 | non | 8 | `c22b0ad6` | `3w/9` |
| `min_raise_3way/hand_10` | 10 | 3 joueurs | 21 / 12 / 21 | non | 7 | `c22b0ad6` | `3w/10` |
| `min_raise_3way/hand_11` | 11 | 3 joueurs | 21 / 21 / 12 | non | 7 | `c22b0ad6` | `3w/11` |
| `min_raise_3way/hand_12` | 12 | 3 joueurs | 8 / 14 / 14 | non | 9 | `c22b0ad6` | `3w/12` |
| `min_raise_3way/hand_13` | 13 | 3 joueurs | 14 / 8 / 14 | non | 8 | `c22b0ad6` | `3w/13` |
| `min_raise_3way/hand_14` | 14 | 3 joueurs | 14 / 14 / 8 | non | 8 | `c22b0ad6` | `3w/14` |
| `min_raise_hu/hand_15` | 15 | heads-up | 25 / 25 | — | 3 | `58407ad7` | `hu/15` |
| `min_raise_hu/hand_16` | 16 | heads-up | 18 / 18 | — | 5 | `58407ad7` | `hu/16` |
| `min_raise_hu/hand_17` | 17 | heads-up | 12 / 12 | — | 4 | `58407ad7` | `hu/17` |
| `min_raise_hu/hand_18` | 18 | heads-up | 10 / 10 | — | 7 | `58407ad7` | `hu/18` |
| `min_raise_hu/hand_19` | 19 | heads-up | 8 / 8 | — | 3 | `58407ad7` | `hu/19` |
| `min_raise_hu/hand_20` | 20 | heads-up | 6 / 6 | — | 3 | `58407ad7` | `hu/20` |
| `min_raise_hu/hand_21` | 21 | heads-up | 4 / 4 | — | 3 | `58407ad7` | `hu/21` |
| `min_raise_hu/hand_22` | 22 | heads-up | 2 / 2 | — | 3 | `58407ad7` | `hu/22` |

## Base v2 (12 octobre 2026)

Calculs demandés dans `docs/hrc/EXPORTS_A_PRODUIRE.md` §1. L'arbre préflop est identique à `complement` et `complement2` (empreinte préflop `daa9aaa0`). En revanche, le postflop est en mode « general » (mise flop 66 %, mise à faible SPR « 66g », seuil SPR 2,5) au lieu de « simple ». À 12 / 12 / 12, la comparaison avec `complement2/hand_7` donne les mêmes fréquences globales à 1 ou 2 points près ; l'écart de regret, de 5 à 34 mBB selon le nœud, reste de l'ordre du bruit propre de HRC.

| Dossier | Table | Stacks (BB) | Nœuds | Empreinte préflop |
|---|---|---|---|---|
| `v2/hand_1` | 3 joueurs | 8 / 8 / 8 | 10 | `daa9aaa0` |
| `v2/hand_2` | 3 joueurs | 10 / 10 / 10 | 11 | `daa9aaa0` |
| `v2/hand_3` | 3 joueurs | 12 / 12 / 12 | 11 | `daa9aaa0` |
| `v2/hand_4` | 3 joueurs | 16 / 16 / 16 | 10 | `daa9aaa0` |
| `v2/hand_5` | 3 joueurs | 18 / 18 / 18 | 10 | `daa9aaa0` |
| `v2/hand_6` | 3 joueurs | 22 / 22 / 22 | 8 | `daa9aaa0` |
| `v2/hand_7` | 3 joueurs | 25 / 25 / 25 | 8 | `daa9aaa0` |
| `v2/hand_8` | heads-up | 14 / 14 | 4 | `daa9aaa0` |
| `v2/hand_9` | heads-up | 16 / 16 | 3 | `daa9aaa0` |
| `v2/hand_10` | heads-up | 22 / 22 | 3 | `daa9aaa0` |

Le contrôle complet (structure et EV) est dans `docs/hrc/VALIDATION_HRC.md` (`python tools/hrc/validate.py`).

## Base v3 (13 octobre 2026)

Reçue après les relectures croisées (`docs/audit/RELECTURES_2026-10-13.md`). 63 mains, **arbre complet** (30 à 73 nœuds par main à 3 joueurs, contre 8 à 11 dans les bases précédentes) : décisions du BTN après sa première action, du SB après avoir complété, pots à trois, squeeze, sur-call. Tapis déséquilibrés des §6.1 et tailles d'ouverture des §6.2 et §7.3 de `docs/hrc/EXPORTS_A_PRODUIRE.md`. Moteur et abstractions identiques à v2 : à tapis égaux, l'écart avec l'EV exacte des calls de tapis est inchangé (par exemple 12 / 12 / 12 : médiane 116 mBB contre 110 en v2, mains atteintes). Le tapis direct du SB au-delà de 16 BB (§7.1) n'y est pas : mêmes réglages d'arbre (`PREFLOP_ADD_ALLIN_SPR` 7, `PREFLOP_ALLIN_THRESHOLD` 40).

Importeur 1.4.0 : les six arbres ci-dessous sont importés ; à arbre et tapis égaux, v3 passe avant les bases précédentes, et le mode postflop « simple » avant « general » (`hand_1`, `hand_2`, `hand_10` sont donc doublés par `hand_5`, `hand_4`, `hand_33`).

| Dossier | Table | Stacks (BB) | Nœuds | Postflop | Empreinte préflop | Tailles d'ouverture |
|---|---|---|---|---|---|---|
| `v3/hand_1` | 3 joueurs | 8 / 8 / 8 | 30 | general | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_2` | 3 joueurs | 10 / 10 / 10 | 32 | general | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_3` | 3 joueurs | 12 / 12 / 12 | 44 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_4` | 3 joueurs | 10 / 10 / 10 | 32 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_5` | 3 joueurs | 8 / 8 / 8 | 30 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_6` | 3 joueurs | 16 / 16 / 16 | 52 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_7` | 3 joueurs | 18 / 18 / 18 | 52 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_8` | 3 joueurs | 20 / 20 / 20 | 58 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_9` | 3 joueurs | 22 / 22 / 22 | 60 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_10` | 3 joueurs | 25 / 25 / 25 | 64 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_11` | heads-up | 8 / 8 | 6 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_12` | heads-up | 10 / 10 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_13` | heads-up | 12 / 12 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_14` | heads-up | 14 / 14 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_15` | heads-up | 16 / 16 | 6 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_16` | heads-up | 18 / 18 | 6 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_17` | heads-up | 22 / 22 | 10 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_18` | heads-up | 25 / 25 | 10 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_19` | 3 joueurs | 35 / 25 / 15 | 62 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_20` | 3 joueurs | 25 / 35 / 15 | 62 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_21` | 3 joueurs | 15 / 25 / 35 | 73 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_22` | 3 joueurs | 35 / 15 / 25 | 63 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_23` | 3 joueurs | 40 / 20 / 15 | 65 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_24` | 3 joueurs | 20 / 40 / 15 | 65 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_25` | 3 joueurs | 15 / 20 / 40 | 66 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_26` | 3 joueurs | 30 / 30 / 15 | 64 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_27` | 3 joueurs | 45 / 20 / 10 | 52 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_28` | 3 joueurs | 20 / 45 / 10 | 52 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_29` | 3 joueurs | 10 / 20 / 45 | 64 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_30` | 3 joueurs | 30 / 25 / 20 | 63 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_31` | 3 joueurs | 50 / 15 / 10 | 48 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_32` | 3 joueurs | 15 / 50 / 10 | 48 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_33` | 3 joueurs | 25 / 25 / 25 | 64 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_34` | 3 joueurs | 20 / 30 / 25 | 70 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_35` | heads-up | 30 / 20 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_36` | heads-up | 35 / 15 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_37` | heads-up | 40 / 10 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_38` | heads-up | 20 / 30 | 8 | simple | `daa9aaa0` | référence : BTN 2,3 BB, SB 3,5 BB |
| `v3/hand_39` | 3 joueurs | 12 / 12 / 12 | 44 | simple | `279f59f1` | BTN 2 BB, SB 3 BB |
| `v3/hand_40` | 3 joueurs | 16 / 16 / 16 | 52 | simple | `279f59f1` | BTN 2 BB, SB 3 BB |
| `v3/hand_41` | 3 joueurs | 20 / 20 / 20 | 60 | simple | `279f59f1` | BTN 2 BB, SB 3 BB |
| `v3/hand_42` | 3 joueurs | 20 / 20 / 20 | 60 | simple | `4d2f96f7` | BTN 2 BB, SB 2,5 BB |
| `v3/hand_43` | 3 joueurs | 16 / 16 / 16 | 54 | simple | `4d2f96f7` | BTN 2 BB, SB 2,5 BB |
| `v3/hand_44` | 3 joueurs | 12 / 12 / 12 | 54 | simple | `4d2f96f7` | BTN 2 BB, SB 2,5 BB |
| `v3/hand_45` | 3 joueurs | 12 / 12 / 12 | 44 | simple | `13f58826` | BTN 2,5 BB, SB 3,5 BB |
| `v3/hand_46` | 3 joueurs | 16 / 16 / 16 | 52 | simple | `13f58826` | BTN 2,5 BB, SB 3,5 BB |
| `v3/hand_47` | 3 joueurs | 20 / 20 / 20 | 50 | simple | `13f58826` | BTN 2,5 BB, SB 3,5 BB |
| `v3/hand_48` | 3 joueurs | 20 / 20 / 20 | 58 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_49` | 3 joueurs | 25 / 25 / 25 | 64 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_50` | 3 joueurs | 18 / 18 / 18 | 52 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_51` | 3 joueurs | 16 / 16 / 16 | 52 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_52` | 3 joueurs | 14 / 14 / 14 | 54 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_53` | 3 joueurs | 12 / 12 / 12 | 44 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_54` | 3 joueurs | 10 / 10 / 10 | 32 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_55` | 3 joueurs | 8 / 8 / 8 | 30 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_56` | 3 joueurs | 6 / 6 / 6 | 28 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_57` | 3 joueurs | 4 / 4 / 4 | 18 | simple | `821ee345` | BTN 2,3 BB, SB 3,3 BB |
| `v3/hand_58` | heads-up | 4 / 4 | 4 | simple | `100650d1` | heads-up, SB 2 BB |
| `v3/hand_59` | heads-up | 6 / 6 | 8 | simple | `100650d1` | heads-up, SB 2 BB |
| `v3/hand_60` | heads-up | 8 / 8 | 8 | simple | `100650d1` | heads-up, SB 2 BB |
| `v3/hand_61` | heads-up | 10 / 10 | 8 | simple | `100650d1` | heads-up, SB 2 BB |
| `v3/hand_62` | heads-up | 12 / 12 | 8 | simple | `100650d1` | heads-up, SB 2 BB |
| `v3/hand_63` | heads-up | 16 / 16 | 10 | simple | `100650d1` | heads-up, SB 2 BB |
