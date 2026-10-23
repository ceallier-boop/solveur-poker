# Travaux antérieurs (conversation Claude)

`conversation/` contient, sans modification, l'ensemble des fichiers récupérés de la conversation de conception : scripts Python, sorties (CSV, JSON, SQLite), fiches PDF et guides. `postflop_package/` est la dernière version du paquet postflop.

Ces fichiers sont une **référence en lecture seule** : le code de l'application sera réécrit dans des modules testés, en reprenant ce qui est conservé dans `docs/audit/AUDIT_PHASE0.md`.

Points à connaître pour les exécuter :
- dépendances : `numpy` et `numba` ;
- chemins codés en dur `/home/claude/...` à remplacer ; les exports de référence sont attendus sous `hrc/x/{3w,hu,3wc,huc,c2}/Hand_N` (correspondance dans `data/hrc/README.md`) ;
- `E3.npy` (matrice d'équité 169 × 169) n'est pas fourni : on le recalcule avec `pushfold.equity_matrix` (2 minutes avec 20 000 tirages) ;
- `eval_vs_hrc.py` et `sim3h.py` n'ont pas pu être récupérés. `reconstructed/eval_vs_hrc.py` reconstruit la seule fonction nécessaire au solveur heads-up et aux évaluations (`path_probs`). Les fonctions de comparaison avec le push/fold (`models_for`, `node_defs`, etc.) manquent, donc `scorecard.py` et `regret_stats.py` ne tournent pas.
- Les fichiers `final_strats.pkl`, `noise_a.pkl`, `noise_b.pkl`, `E_final.npy` et `T_final.npy` (attendus par `tests.py`) ne sont pas fournis.
