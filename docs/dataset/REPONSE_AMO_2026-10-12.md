# Réponse à l'évaluation AMO de `FORMAT_SPOT.md` (12 octobre 2026)

L'évaluation portait sur la spécification seule. Le code, les datasets et les rapports sont dans le dépôt `ceallier-boop/solveur-poker`, branche `claude/poker-expresso-training-app-b63kf9`, et l'AMO peut les auditer :

| Élément | Emplacement |
|---|---|
| Importeur | `spinsacademy/importer.py` |
| EV exactes | `spinsacademy/allin.py` |
| Correction | `spinsacademy/grading.py` |
| Rapports | `spinsacademy/report.py` |
| Validation des exports de référence | `tools/hrc/validate.py` |
| Tests | `tests/` (13 tests) |
| Dataset courant | `data/datasets/gto_preflop/2026.10.12-2/` |
| Rapport du dataset | `docs/dataset/RAPPORT_2026.10.12-2.md` |

Il n'existe pas encore de générateur de quiz : c'est l'étape suivante.

## Points soulevés

### 1. Barème : la règle des 10 % peut couvrir une action coûteuse — **constat confirmé, corrigé**

Mesure sur le dataset `2026.10.12-1` : parmi les couples (main, action) où la référence joue l'action au moins 10 % du temps, **7 222 avaient un regret supérieur à 60 mBB** selon les propres EV de la référence, dont 3 356 au-delà de 150 mBB. Exemple : la référence folde 44 une fois sur dix au SB face au tapis du BTN à 18 BB, pour un coût de 2,7 BB selon son EV.

Il ne s'agit pas d'une stratégie mixte mais d'une incohérence entre la fréquence et l'EV de la référence, sur des nœuds rarement atteints (bruit Monte-Carlo). Deux corrections, dans la version `2026.10.12-2` :
- **La tolérance mixte est plafonnée.** Une action jouée au moins 10 % du temps n'est déclarée correcte que si son regret reste ≤ 60 mBB. Au-delà, c'est une erreur, quelle que soit sa fréquence. Elle couvre maintenant 4 271 réponses, toutes entre 20 et 60 mBB de regret.
- **Les mains incohérentes ne sont plus proposées.** Une main n'est proposable que si EV(meilleure action) − Σ fréquence × EV ≤ 60 mBB. Cela retire environ 5 % des mains atteintes.

Le rapport (§5) donne la répartition des verdicts et des exemples tirés au hasard, à faire relire par l'expert poker.

### 2. Définition du regret et conventions d'EV — **documentées**

`FORMAT_SPOT.md`, section « Conventions d'EV » :
- toutes les EV sont relatives au fold ;
- l'EV exacte n'est calculée que pour le call d'un all-in et l'all-in contre un seul adversaire, avec ses formules ;
- une même source d'EV pour toutes les actions d'un spot, jamais de mélange ni d'EV absente ;
- un regret toujours ≥ 0.

L'EV exacte est exacte en heads-up. À 3 joueurs, elle est approchée, car les cartes du joueur couché ne sont pas retirées ; c'est signalé par `ev_exact_approximate`.

La matrice d'équité a été contrôlée par énumération exhaustive des boards (`spinsacademy/data/equity_169.json`). La convention « relative au fold » est vérifiée contre la référence aux petits stacks, où la référence est précis : biais inférieur à 5 mBB.

### 3. Couverture — **mesurée**

Rapport §3 :
- 48 212 mains atteignent un nœud, dont 45 703 sont proposables.
- La couverture est détaillée par table, stacks, position et famille de décision : premier à parler, face à un limp, face à une relance, face à un tapis.
- Les 169 classes sont proposables dans au moins 235 spots chacune.

La couverture du catalogue réellement servi sera mesurée sur les tirages du générateur de séries, quand il existera.

### 4. Choix des exports de référence — **justifié**

Critères objectifs :
- un arbre préflop unique, identifié par une empreinte de ses réglages ;
- un seul export par configuration de stacks.

Tous les doublons ont le même arbre préflop. On retient la base calculée pour le projet, avec des réglages documentés (`docs/reference/EXPORTS_A_PRODUIRE.md`). La comparaison 12 / 12 / 12 entre deux bases donne des fréquences identiques à 1 ou 2 points près. Chaque export écarté et sa raison sont listés dans le manifeste et dans le rapport §1 : 11 pour arbre différent, 4 doublons.

Limite connue : les exports de référence s'arrêtent à deux actions. Les lignes plus profondes (par exemple SB face à un iso-raise) ne sont pas encore couvertes.

### 5. Droits de référence — **toujours bloquant avant diffusion**

Aucune avancée de notre côté. Le dataset reste au statut `staging`.

## Livrables demandés

| Livrable | Où | État |
|---|---|---|
| Rapport d'import | `RAPPORT_2026.10.12-2.md` §1 | fait |
| Rapport de validation | §2 (contrôles rejoués sur le fichier publié, 0 échec) et `docs/reference/VALIDATION_REFERENCE.md` (exports bruts) | fait |
| Rapport de comparaison de référence | §4 et `docs/reference/VALIDATION_REFERENCE.md` | fait |
| Rapport de notation | §5 | fait, relecture experte à faire |
| Publication bloquée sur spot invalide | `tests/test_importer.py` : `test_publication_blocked_by_injected_invalid_spot`, `test_publication_blocked_by_illegal_action` | fait, tests au vert |

## Ce qui reste

1. Faire relire par l'expert poker les exemples du rapport §5 et valider les seuils (20 / 60 mBB, 10 %).
2. Lever la question des droits de référence.
3. Écrire le générateur de séries, puis mesurer la couverture réellement servie.
4. En option : relancer de référence avec une précision plus élevée et des exports complets, pour réduire les mains retirées et couvrir les lignes profondes.
