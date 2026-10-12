# Dataset `gto_preflop` : format et règles

Ce dataset est produit par `python -m spinsacademy.importer --version <version>` à partir de `data/hrc/raw/`. Il est publié dans `data/datasets/gto_preflop/<version>/` :

| Fichier | Contenu |
|---|---|
| `manifest.json` | version, date, version de l'importeur, arbre préflop de référence, règle d'EV, empreinte SHA-256 de `spots.jsonl`, exports utilisés et écartés, statut (`staging` à la création) |
| `spots.jsonl` | un spot par ligne |

Une version publiée ne se réécrit jamais : toute correction donne un nouveau numéro de version. Une session de quiz garde le numéro de version qui a servi à la corriger.

## Spot

Un spot est un nœud de décision de l'arbre HRC. Une question de quiz est un couple (spot, main), tiré parmi les mains marquées `quiz_eligible`.

| Champ | Description |
|---|---|
| `spot_id` | identifiant stable : table, stacks, nœud, empreinte |
| `table`, `players`, `stacks_bb` | `3-handed` (BTN, SB, BB) ou `heads-up` (SB, BB) ; stacks en BB, dans l'ordre de `players` |
| `blinds_bb`, `ante_bb`, `model` | 0,5 / 1, 0, `chip_ev` |
| `hero`, `node_key` | joueur qui décide ; clé du nœud (par exemple `BTN-fold_SB-call`) |
| `history` | actions précédentes : `fold`, `check`, `limp`, `call`, `call_allin`, `raise`, `allin`, avec `to_bb` = mise totale du joueur après l'action |
| `pot_bb`, `to_call_bb`, `hero_committed_bb`, `effective_stack_bb` | état au moment de la décision |
| `actions` | actions légales : `F` fold, `X` check, `C` limp / call / call_allin, `R<x>` relance à x BB, `A` tapis (tapis effectif compris) |
| `ev_reference` | `exact` ou `hrc` : EV utilisée pour corriger |
| `ev_exact_approximate` | vrai à 3 joueurs quand une EV exacte est utilisée : les cartes du joueur couché ne sont pas retirées |
| `reach_share` | part des mains du héros qui atteignent ce nœud |
| `eligible_hands` | nombre de mains proposables en question |
| `hands` | pour chacune des 169 classes : `reach`, `freq` (fréquences HRC), `ev_hrc`, `ev_exact` (`null` si non calculable), `hrc_self_regret_mbb`, `quiz_eligible` ; EV en BB, relatives au fold |
| `provenance` | export source et son SHA-256, empreintes d'arbre HRC, mode postflop, version de l'importeur, matrice d'équité |

## Règles

1. **Arbre unique** : seuls les exports de l'arbre préflop `daa9aaa0` (limp du BTN autorisé) sont importés. `min_raise_3way` est écarté.
2. **Un export par configuration de stacks**. Tous les doublons ont le même arbre préflop. On retient la base la plus récente (ordre `v2`, `complement2`, `complement`, `min_raise_hu`), c'est-à-dire celle calculée pour ce projet avec les réglages documentés dans `docs/hrc/EXPORTS_A_PRODUIRE.md`. La comparaison 12 / 12 / 12 entre deux bases donne des fréquences identiques à 1 ou 2 points près. Chaque export écarté et sa raison figurent dans le manifeste et dans le rapport.
3. **Légalité** : une mise ne peut dépasser le stack. Le fold n'est proposé que face à une mise ; le fold « gratuit » de l'arbre HRC est retiré, après vérification que HRC ne le joue jamais. Le check n'est proposé que sans mise à payer. Une mise qui couvre le plus gros stack adverse encore en jeu est un tapis.
4. **EV de référence** : l'EV exacte si chaque action autre que fold en a une (décisions tout ou rien : call d'un all-in, all-in contre un seul adversaire restant). Sinon, l'EV HRC. La raison est le bruit Monte-Carlo de HRC, mesuré dans `docs/hrc/VALIDATION_HRC.md`.
5. **Mains proposables** : `quiz_eligible` est vrai si `reach` ≥ 0,05 (la main atteint le nœud) **et** `hrc_self_regret_mbb` ≤ 60. Cette seconde valeur vaut EV(meilleure action) − Σ fréquence × EV, sur l'EV de référence. Elle mesure l'incohérence entre la stratégie HRC et l'EV utilisée pour corriger. Au-delà de 60 mBB, la fréquence affichée contredirait la correction : la main n'est pas proposée. Cela concerne environ 5 % des mains atteintes.
6. **Blocage** : un spot invalide (fréquences non normalisées, action illégale, classes manquantes) bloque toute la publication.
7. **Données HRC** : les exports bruts ne sortent jamais du dépôt. Le dataset en contient des valeurs dérivées (fréquences et EV), à couvrir par la vérification des droits HRC (`docs/audit/AUDIT_PHASE0.md` §5.4).

## Conventions d'EV

- Toutes les EV (`ev_hrc`, `ev_exact`) sont en BB, en chip EV, **relatives au fold** du joueur qui décide : EV(fold) = 0. C'est la convention des exports HRC ; elle est vérifiée par le calcul exact aux petits stacks, où HRC est précis (biais inférieur à 5 mBB en heads-up de 2 à 8 BB, sur les calls comme sur les all-in).
- **EV exacte** : uniquement pour (a) le call d'un all-in à deux joueurs et (b) l'all-in contre un seul adversaire restant. On l'obtient à partir de la range adverse exportée par HRC et de la matrice d'équité classe contre classe, bloqueurs compris :
  - call : eq × (2L + mort) − L + blind payée ;
  - all-in : Σ P(j | main) × [(1 − c_j) × (blind adverse + mort) + c_j × (E_ij × (2L + mort) − L)] + blind payée.

  À 3 joueurs, les cartes du joueur qui a foldé ne sont pas retirées (`ev_exact_approximate`).
- **EV de référence d'un spot** : l'EV exacte si **toutes** les actions autres que fold en ont une, sinon l'EV HRC pour **toutes** les actions. On ne mélange jamais les deux sources dans un même spot, et l'EV de référence n'est jamais absente.
- **Regret** = EV(meilleure action) − EV(action choisie), en mBB, sur l'EV de référence. Il est toujours ≥ 0.

## Correction (`spinsacademy/grading.py`)

| Verdict | Condition | Points |
|---|---|---|
| correct | regret ≤ 20 mBB, ou regret ≤ 60 mBB pour une action jouée par HRC au moins 10 % du temps quand l'EV de référence est celle de HRC | 1 |
| imprécision | regret ≤ 60 mBB | 0,5 |
| erreur | au-delà | 0 |

Les stratégies affichées sont arrondies au pas de 5 %, avec une somme de 100 % (méthode du plus fort reste). La correction utilise les valeurs non arrondies.

Une main non proposable (`quiz_eligible` faux) est refusée par la correction.

## Rapports

`python -m spinsacademy.report --version <version>` produit `docs/dataset/RAPPORT_<version>.md`, à partir des seuls fichiers publiés. Il contient :
- l'import : exports retenus et écartés, avec les raisons ;
- la validation : contrôles rejoués sur le fichier publié ;
- la couverture : par table, stacks, position, famille de décision et classe de main ;
- la comparaison avec HRC ;
- la notation : répartition des verdicts et exemples.
