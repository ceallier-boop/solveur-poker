# Dataset `gto_preflop` : format et règles

Ce dataset est produit par `python -m spinsacademy.importer --version <version>` à partir de `data/hrc/raw/`. Il est publié dans `data/datasets/gto_preflop/<version>/` :

| Fichier | Contenu |
|---|---|
| `manifest.json` | version, date, version de l'importeur, arbre préflop de référence, règle d'EV, empreinte SHA-256 de `spots.jsonl`, exports utilisés et écartés, statut (`staging` à la création) |
| `spots.jsonl` | un spot par ligne |

Une version publiée ne se réécrit jamais : toute correction donne un nouveau numéro de version. Une session de quiz garde le numéro de version qui a servi à la corriger.

## Spot

Un spot est un nœud de décision de l'arbre HRC. Une question de quiz est un couple (spot, main), tiré parmi les mains dont `reach` ≥ `min_reach_for_questions` (0,05).

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
| `hands` | pour chacune des 169 classes : `reach`, `freq` (fréquences HRC), `ev_hrc`, `ev_exact` (`null` si non calculable) ; EV en BB, relatives au fold |
| `provenance` | export source et son SHA-256, empreintes d'arbre HRC, mode postflop, version de l'importeur, matrice d'équité |

## Règles

1. **Arbre unique** : seuls les exports de l'arbre préflop `daa9aaa0` (limp du BTN autorisé) sont importés. `min_raise_3way` est écarté.
2. **Un export par configuration de stacks** : le plus récent (ordre `v2`, `complement2`, `complement`, `min_raise_hu`).
3. **Légalité** : une mise ne peut dépasser le stack. Le fold n'est proposé que face à une mise ; le fold « gratuit » de l'arbre HRC est retiré, après vérification que HRC ne le joue jamais. Le check n'est proposé que sans mise à payer. Une mise qui couvre le plus gros stack adverse encore en jeu est un tapis.
4. **EV de référence** : l'EV exacte si chaque action autre que fold en a une (décisions tout ou rien : call d'un all-in, all-in contre un seul adversaire restant). Sinon, l'EV HRC. La raison est le bruit Monte-Carlo de HRC, mesuré dans `docs/hrc/VALIDATION_HRC.md`.
5. **Blocage** : un spot invalide (fréquences non normalisées, action illégale, classes manquantes) bloque toute la publication.
6. **Données HRC** : les exports bruts ne sortent jamais du dépôt. Le dataset en contient des valeurs dérivées (fréquences et EV), à couvrir par la vérification des droits HRC (`docs/audit/AUDIT_PHASE0.md` §5.4).

## Correction (`spinsacademy/grading.py`)

| Verdict | Condition | Points |
|---|---|---|
| correct | regret ≤ 20 mBB, ou action jouée par HRC au moins 10 % du temps quand l'EV de référence est celle de HRC | 1 |
| imprécision | regret ≤ 60 mBB | 0,5 |
| erreur | au-delà | 0 |

Les stratégies affichées sont arrondies au pas de 5 %, avec une somme de 100 % (méthode du plus fort reste). La correction utilise les valeurs non arrondies.
