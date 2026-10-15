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
| imprécision | regret ≤ 60 mBB, ou regret ≤ 100 mBB quand l'EV de référence est celle de HRC (`PERTINENT_MBB`, champ `pertinent` de la correction ; 2026-10-14) | 0,5 |
| erreur | au-delà | 0 |

Les stratégies affichées ne gardent que les actions jouées au moins 10 % du temps (celles que la correction accepte), renormalisées puis arrondies au pas de 5 %, avec une somme de 100 % (méthode du plus fort reste). Une action affichée est donc toujours acceptée. La correction utilise les valeurs non arrondies.

Une main non proposable (`quiz_eligible` faux) est refusée par la correction.

## Rapports

`python -m spinsacademy.report --version <version>` produit `docs/dataset/RAPPORT_<version>.md`, à partir des seuls fichiers publiés. Il contient :
- l'import : exports retenus et écartés, avec les raisons ;
- la validation : contrôles rejoués sur le fichier publié ;
- la couverture : par table, stacks, position, famille de décision et classe de main ;
- la comparaison avec HRC ;
- la notation : répartition des verdicts et exemples.


## Évolution 2026-10-13 (importeur 1.2.0, dataset gto_preflop 2026.10.13-1)

- Une action jouée au moins 10 % du temps par la stratégie de référence est toujours notée « correcte » (stratégie mixte jamais sanctionnée).
- En contrepartie, une main n'est proposée que si chacune de ses actions jouées au moins 10 % du temps perd au plus 60 mBB selon l'EV de référence (`mixed_min`, `max_mixed_regret_mbb` dans le manifeste). 4 458 mains de la version 2026.10.12-2 avaient des fréquences et des EV HRC contradictoires : elles ne sont plus proposées.
- Tirage : rotation sur la position du joueur (BTN, SB, BB) puis sur la famille de décision ; les mains où toutes les actions sont acceptées ne sont pas tirées ; les mains faciles (la première action sanctionnée coûte plus de 1 BB) sont tirées 4 fois moins souvent ; chaque question porte une difficulté (facile, moyen, difficile : moins de 0,2 BB d'écart).
- Correction : phrase « pourquoi » tirée des données (cote du pot et équité contre la range de tapis pour les calls d'un tapis à EV exacte ; sinon part de la stratégie qui joue l'action de la main) et grille 13 × 13 de la stratégie de référence.

- Correction, sections dépliables :
  - « Pourquoi ? » : pour un call de tapis, cote du pot et équité de la main à une décimale, marge en points et niveau d'écart calculé sur la marge affichée (moins de 5 points : décision serrée ; 5 à 10 : écart moyen ; plus de 10 : écart large ; message différent selon que la réponse est juste ou non, « coûte peu » seulement sous 0,06 BB, la limite d'imprécision), mains qui paient tout juste et qui se couchent déjà, part des mains qui arrivent à cette décision et qui paient (contre le profil et en GTO). Sinon : part de la stratégie (« en fait partie » seulement si la main joue l'action au moins 50 % du temps), repère de cote du pot (approximatif) pour les calls de tapis HRC, deuxième option quand elle n'est ni le choix du joueur ni le fold, jeu mixte (en nommant le choix du joueur s'il n'en fait pas partie), mains jouées en mixte pour l'action ;
  - verdict : seuils dits en clair (moins de 0,02 BB : bruit de calcul ; 0,02 à 0,06 BB : imprécision ; au-delà : erreur ; action jouée au moins 10 % du temps : acceptée). Un gain sous 0,02 BB (la limite entre réponse acceptée et imprécision) est affiché « <0,02 BB » ;
  - « Et ensuite ? » : toujours au sujet de la bonne action (« Avec la bonne action … » quand le joueur en a choisi une autre). Face à un tapis : seule l'équité compte, pas de statistiques de flop. Tapis du joueur : fold equity ou équité, sans décision après le flop. Sinon position après le flop, fréquences au flop comparées à la moyenne des mains du même type (non pairées : paire max ou mieux, deux paires ou mieux, tirage couleur ou quinte ou mieux ; paires : brelan ou mieux, paire plus haute que le board, carte plus haute que la paire au board, où moins est mieux : champ `lower_is_better`, couleur dans `tone`), forces et faiblesses ; équité contre une main au hasard avec cartes retirées (AA : 85 %). Fréquences calculées par énumération exacte des 19 600 flops (`tools/postflop/flop_profiles.py`, `spinsacademy/data/postflop_profiles.json`) ; probabilité de carte plus haute : 1 − C(50 − 4·(cartes au-dessus), 3) / C(50, 3) ;
  - grille 13 × 13.

### Correction après la 2ᵉ relecture joueur (2026-10-13)

- Montants d'un call plafonnés au tapis du joueur (`quiz.call_terms`) : quand un tapis le couvre, l'excédent lui est rendu ; libellé, cote du pot et équité utilisent ces montants (ex. 4 BB effectifs face à 8 BB : 3 BB à payer pour 8,5 BB).
- Action de référence affichée (`quiz.reference_action`) : la plus jouée par la stratégie quand elle vaut, à la limite d'imprécision près (0,06 BB), la plus rentable en EV ; celle-ci est alors citée (« … se vaut presque »). La notation ne change pas (regret mesuré sur l'EV maximale).
- Montants entre 0,055 et 0,065 BB affichés à 3 décimales, pour que montant et verdict concordent ; « bruit de calcul » seulement pour une EV HRC.
- « À la limite » : mains à 2 points d'équité du seuil au plus ; repère de cote du pot exact en heads-up sans tapis couvert.
- « Et ensuite ? » : tapis à 3 joueurs (« tout le monde se couche »), moins de 5 BB restants après l'action : l'essentiel se joue à l'équité ; comparaisons à la moyenne sur les valeurs affichées.
- Libellés : « Compléter (0,5 BB de plus) », relances à une décimale, « Tapis (8 BB, 4 BB effectifs) » quand le joueur couvre ses adversaires.

### Relectures croisées (2026-10-13 ; importeur 1.3.0, dataset gto_preflop 2026.10.13-2)

- Importeur 1.3.0 : calls heads-up exacts face au tapis du BB après un limp (`SB-call_BB-allin`) ou une relance (`SB-raise3.5_BB-allin`) du SB. Seuls ces 3 spots changent par rapport à la 2026.10.13-1 (EV de référence exacte au lieu de HRC).
- Stratégie de référence en EV exacte : l'action la plus rentable (`grading.reference_freq`), pour la notation, les barres, la grille et les parts ; la règle des 10 % s'applique à cette stratégie. Ailleurs, les fréquences HRC.
- Tirage : questions HRC dont la leçon coûte au moins 150 mBB (`quiz.HRC_NOISE_MBB`), tapis effectif d'au moins 4 BB. Détail : `docs/audit/RELECTURES_2026-10-13.md`.

### Tirage après l'évaluation du MVP (2026-10-14)

- Format d'abord : heads-up `quiz.HU_SHARE` (35 %) du temps quand les filtres laissent les deux formats, puis rotation sur la position et la famille.
- Une main ne revient pas deux fois dans une série ; une question facile n'est tirée à dessein que `quiz.EASY_SHARE` (6 %) du temps quand la situation offre mieux (plafond validé : 15 % au total) ; poids de tirage = combos × racine du poids d'atteinte.
- Mains exclues du tirage quand l'EV de référence d'un call perd plus que le montant à payer (`quiz.impossible_ev`, artefact HRC).
- Lot 1 (2026-10-14) : en EV HRC, une main n'est proposée que si la moins chère des vraies erreurs coûte au moins 150 mBB (`quiz.error_gap`, seuil de bruit `HRC_NOISE_MBB`) ; une action à moins de 0,1 BB n'empêche plus la question, elle reçoit une nuance. En EV exacte, toute main avec une erreur est proposable.
