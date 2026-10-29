# Moteur GTO : ce qu'il faut, ce qui existe (29/10/2026)

Inventaire fait à la prise en charge du moteur GTO. Sources : code (`spinsacademy/solver`, `spinsacademy/postflop`, `allin.py`, `pushfold.py`, `tools/solver`, `tools/hrc`), documents (`docs/solver`, `docs/reference`, `docs/dataset`, `docs/produit`) et documents partagés (stratégie exploitante v1, ranges push/fold, évaluation du MVP).

Légende : ✅ en place et contrôlé ; ⚠️ existe, insuffisant ; ❌ absent.

## 1. Situation de départ

Les banques servies (GTO `2026.10.13-3`, exploitant `2026.10.23-1`) viennent **des exports de la référence**, pas du solveur maison. Le solveur maison existe, est testé, mais reste 2 à 3 fois au-dessus du bruit de la référence sur certains nœuds (`docs/exploitation/ANOMALIES_CONNUES.md`). La commande v4 (base unique, précise) n'est pas reçue (`docs/reference/EXPORTS_A_PRODUIRE.md` §10).

## 2. Les éléments d'un moteur GTO

| # | Élément | État | Ce qui existe | Ce qui manque |
|---|---|---|---|---|
| 1 | Règles et arbre préflop (2 et 3 joueurs, limp, relances, tapis) | ✅ | `solver/tree.py` : `TreeConfig`, seuils de tapis de la référence (`UNOPENED_ALLIN`), même actions que la référence sur tous les nœuds exportés (tests) | tailles d'ouverture de la v4 (choix A) ; tapis direct jusqu'à 25 BB (§10.1) |
| 2 | Équités préflop et bloqueurs | ✅ / ⚠️ | `data/equity_169.npy`, `equity3_169.npy`, matrice de combos disjoints | à 3 joueurs : adversaires supposés indépendants, cartes du joueur couché non retirées |
| 3 | EV exactes des décisions de tapis | ✅ / ⚠️ | `allin.py` (exact en heads-up), `pushfold.py` (équilibre push/fold) | EV exacte à 3 joueurs (lot C5) |
| 4 | Solveur préflop | ✅ | `solver/cfr.py` : CFR+ vectorisé sur 169 classes, chip EV, mesure d'exploitabilité ; `solver/dataset.py` : banque au format `spots.jsonl`, contrôles, calage (29/10, `docs/solver/BANQUE_SOLVEUR.md`) | — |
| 5 | Valeur des pots qui vont au flop | ⚠️ | `solver/postflop.py` (showdown, réalisation par corrections additives), `solver/pipeline.py` (alternance préflop / postflop) | modèle à 3 joueurs approché par duels ; écart restant sur le BB face à une relance |
| 6 | Solveur postflop heads-up | ⚠️ | `postflop/hu_solver.py`, `fast.py`, `kernels.py` (numba, 16 groupes, 24 tirages, pas de donk bet, option texture) | exploitabilité 5 % (river) à 13-17 % du pot (turn) ; stratégie partagée entre tous les flops ; pas de postflop à 3 |
| 7 | Contrôle exact des sous-jeux | ✅ | `postflop/exact.py`, `tools/solver/exact_check.py` (CFR+ combo par combo, river et turn) | — |
| 8 | Évaluateur de mains | ✅ | `postflop/kernels.py` (dénombrement exact 5 et 7 cartes, 0 désaccord sur 60 000 duels) | — |
| 9 | Comparaison avec la référence | ✅ | `solver/calibration.py` (calage enregistré dans chaque banque du solveur), `tools/solver/benchmark_hrc.py`, `docs/solver/CONTROLE_ABSTRACTION.md` | à refaire sur la v4 dès réception |
| 10 | Données de référence | ⚠️ | bases `complement`, `complement2`, `min_raise_*`, v2, v3 (63 mains, arbre complet) dans `data/hrc/raw/` | **v4 non reçue** ; choix A à F de §10.3 à trancher ; pilote 12/12/12 et HU 12/12 |
| 11 | Import, validation, publication | ✅ | `hrc.py`, `importer.py` 1.5.0 (moyenne des exports répétés, 29/10), `tools/hrc/validate.py`, `precision_test.py`, `catalog.py`, administration | — |
| 12 | Bruit et notation | ✅ | seuils 20 / 60 mBB (`grading.py`), filtre `REF_NOISE_MBB` à 150 mBB, retrait des mains mal résolues | seuil à baisser selon la précision v4 ; seuils non validés par un expert |
| 13 | Exploitant (verrouillage de nœuds, profils) | ⚠️ | `field.py`, `tools/field/*` (profils v4, limp au SB), `tools/hrc/make_locks.py` (135 calculs) | profils = hypothèses de coachs ; historique de mains pour calibrer (B2) ; calculs verrouillés non lancés |
| 14 | Contenu postflop | ❌ | statistiques de flop par main (`postflop_profiles.json`), paquet postflop de `legacy/` (bibliothèque de flops, quiz d'équité) | aucune stratégie postflop de référence ; exports §9.7 non commandés |
| 15 | ICM | ❌ | — | hors périmètre (décision du 13/10 : chip EV) |
| 16 | Tests | ✅ | `tests/test_solver.py`, `test_postflop_solver.py`, `test_exact.py` | — |

## 3. Ce qu'il me faut

### Décisions
1. **Rôle du moteur maison : tranché le 29/10/2026.** À terme, les résultats servis viennent de notre solveur ; la référence ne sert plus qu'à le caler et à le contrôler. Conséquences : la précision de la référence compte pour mesurer le solveur (d'où la moyenne des répétitions), et le solveur doit produire des spots au même format, avec ses propres contrôles avant publication.
2. **Choix A à F de la commande v4** (§10.3), en premier A (tailles d'ouverture) et B (nombre de répétitions).

### Données
3. Le pilote v4 (3 joueurs 12/12/12 et HU 12/12, 4 exports chacun), puis les 58 configurations P1 (la commande en annonce 59 : 25 / 25 / 25 y figure deux fois).
4. Un historique de mains réel pour calibrer les profils exploitants (B2).
5. Plus tard : exports postflop de la référence sur une vingtaine de textures (pots limpés, 15-25 BB).

### Travaux de mon côté
6. ~~Importeur : moyenne des répétitions~~ : fait le 29/10 (importeur 1.5.0). Reste le contrôle de précision à réception de la v4.
7. ~~Format de sortie du solveur maison vers `spots.jsonl`~~ : fait le 29/10 (`docs/solver/BANQUE_SOLVEUR.md`).
8. Précision : BB face à une relance et SB face au limp du BTN (2 à 3 fois le plancher), puis l'abstraction postflop (groupes selon le potentiel de la main, stratégie par famille de flops).
9. EV exacte à 3 joueurs (cartes du joueur couché retirées), qui sert aussi à mesurer la référence à 3 joueurs.

### Environnement
10. Temps de calcul : 5 à 14 minutes par configuration heads-up sur 4 cœurs ; une série de 59 configurations à 3 joueurs demande une machine dédiée ou des sessions longues.
11. `pytest` à installer dans l'environnement cloud (`pip install -r requirements.txt`) pour faire tourner les tests du solveur.
