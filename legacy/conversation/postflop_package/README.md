# Noyau postflop (prototype autonome)

Aucune dépendance au modèle préflop : seulement `numpy` et `numba`.

- `postflop_core.py` : ranges à 1 326 combinaisons, équité exacte (cartes bloquées, égalités), main actuelle contre range, catégories, amélioration, tirages.
- `ref_eval.py` : évaluateur de référence indépendant (meilleure main de 5 cartes parmi les sous-ensembles).
- `ranges_export.json` : ranges préflop (169 classes) des lignes de flop principales, issues des exports de référence.
- `tests_postflop.py` : `python tests_postflop.py` (environ 1 minute, compilation comprise).

## Métriques (jamais confondues)
| Fonction | Définition |
| --- | --- |
| `range_equity`, `equity_breakdown` | part du pot théorique sur toutes les cartes à venir (gain + moitié des égalités) |
| `made_hand_comparison` | main actuelle devant, à égalité ou derrière la range adverse, sans cartes à venir |
| `improvement` | probabilité de monter d'au moins une catégorie à la turn ou d'ici la river |
| `draws`, `draws_of_combo` | tirage couleur, outs de quinte, probabilité de compléter d'ici la river (énumération exacte) |
| `flop_categories` | distribution des catégories (paire détaillée : overpair, top pair, médiane, basse, poche, board) |
| `street_metrics` | tableau de bord regroupant ces métriques |

## Conventions
Carte = rang * 4 + couleur, rang 0..12 (2..A), couleur 0..3 (c, d, h, s). Classes de main : grille 13 x 13, indice = ligne * 13 + colonne.

## Métriques pédagogiques (calibrées sur `library_profiles.json`)
| Fonction | Rôle | Seuil par défaut |
| --- | --- | --- |
| `pedagogical_profile` | profil complet d'un flop pour deux ranges (équité, mains fortes, nuts, tirages, texture, changement à la turn, concepts) | |
| avantage de range | équité de A moins 50 % | 5 points (parité : 2 points) |
| avantage de mains fortes | part « top pair ou mieux » de A moins celle de B | 6 points |
| avantage de nuts | part de chaque range dans le top 10 % des deux ranges réunies | 8 points |
| `turn_shift` | équité de A sur chaque turn, variation par rapport au flop | 4 points |
| `flop_texture` | hauteur, pairé, connexion, motif de couleurs, étiquette | |
| `canonical_flops` | les 1 755 flops équivalents par permutation des couleurs (22 100 flops) | |
| `select_flops`, `apply_thresholds` | sélection par concept, recalcul des concepts avec d'autres seuils | |

`python build_library.py` recalcule la bibliothèque (environ 20 minutes pour 63 flops et 2 lignes).

## Questions de quiz et tests de l'évaluation AMO
- `postflop_quiz.py` : génère les questions (avantage de range, mains fortes, nuts, variation à la turn, équité d'une main, tirages). Chaque question porte sa définition, la note « conditionnel aux ranges de référence, pas une recommandation GTO », ses métriques et un hachage de contenu. Une question dont la mesure est à moins de 0,5 point d'un seuil est écartée. Aucune question « amélioration » n'est produite : l'écart maximal entre les deux ranges (2,8 points) reste sous le seuil de 3 points.
- `tests_exact_bruteforce.py` : exactitude indépendante par énumération brute (évaluateur de référence).
- `verify_postflop_quiz.py` : cohérence (chaque réponse recalculée depuis le noyau, définition présente, explication qui cite la valeur recalculée) et robustesse (structure, cartes bloquées, doublons, 300 quiz de 10 questions, 5 graines). Durée : environ 20 minutes (recalcul des turns), génération de la banque : 13 secondes.
- Performance pour l'application : servir `postflop_quiz_bank.json` précalculé ; aucun calcul d'équité en ligne (un flop avec deux ranges de 1 200 combinaisons coûte environ 4,5 s).
