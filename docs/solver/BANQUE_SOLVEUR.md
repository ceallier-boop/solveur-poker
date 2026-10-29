# Banque GTO produite par le solveur maison

Objectif (décision du 29/10/2026) : les questions servies viennent de notre solveur ; la référence ne sert plus qu'à le caler et à le contrôler. Code : `spinsacademy/solver/dataset.py` (version 1.0.0).

## Chaîne de production

| Étape | Ce qui se passe | Où |
|---|---|---|
| 1. Résolution | Préflop CFR+ sur les 169 classes, sous-jeux postflop heads-up résolus avec les ranges qui arrivent au flop, alternés jusqu'à stabilité (au plus 10 tours, arrêt sous 0,5 point de variation) | `solver/pipeline.py` |
| 2. Résultat enregistré | Nœuds au format des exports (séquence, actions, et par main : atteinte, fréquences, EV relatives au fold), informations de calcul. C'est la source de la banque, comme `data/hrc/raw` pour la référence. Une configuration déjà résolue avec les mêmes réglages n'est pas recalculée | `data/solver/runs/<arbre>_<réglages>/<config>.json` |
| 3. Contrôles du solveur (bloquants) | Exploitabilité : gain de la meilleure réponse de chaque joueur, au plus 5 mBB par main. Stabilité : variation de stratégie au dernier tour préflop / postflop, au plus 1 point | `dataset.controls` |
| 4. Calage (information) | Quand la référence a le même arbre et les mêmes tapis : perte de notre stratégie mesurée avec les EV de la référence, à comparer au plancher (le regret de la référence elle-même, son bruit). Exports répétés moyennés | `solver/calibration.py` |
| 5. Spots | Même cœur que l'importeur (`importer.make_spot`) : mêmes champs, EV exacte quand chaque action autre que fold en a une, mains proposables selon les mêmes règles | `dataset.spots_of` |
| 6. Publication | `data/datasets/gto_preflop/<version>/`, manifeste avec `source: "solveur"`, réglages, rapport par configuration (contrôles, calage). Refusée si un contrôle échoue ou si un spot est invalide | `dataset.publish` |
| 7. Contrôle de publication | Le catalogue vérifie les contrôles du solveur de chaque configuration et reconstruit les spots depuis les résultats enregistrés ; le recalcul complet se lance à part | `catalog.validate`, `--check` |

Identifiants : sur l'arbre de la référence (`daa9aaa0`, notre arbre par défaut), un spot du solveur a le même `spot_id` que le spot de la référence pour la même situation. La progression et les révisions des joueurs restent attachées à la situation quand la source change.

Champs : `ev_reference` vaut `exact` ou `hrc` ; `hrc` désigne ici l'EV du solveur, que l'application affiche déjà « solveur ». Le renommage des identifiants techniques (`ev_hrc`, `hrc_self_regret_mbb`) touche l'application et se fera avec elle.

## Commandes

```bash
python -m spinsacademy.solver.dataset --version 2026.10.29-s1 --configs hu:12-12,3w:12-12-12
```

```bash
python -m spinsacademy.solver.dataset --version 2026.11.01-s1 --grid p1
```

```bash
python -m spinsacademy.solver.dataset --check gto_preflop/2026.10.29-s1
```

`--grid p1` : les 58 configurations P1 de la commande v4 (la commande en annonce 59, mais 25 / 25 / 25 y figure deux fois). `--model showdown` : préflop seul, sans jeu après le flop (rapide, pour les essais).

## Mesures

### Heads-up 12 BB, convergence préflop / postflop (29/10/2026)

Variation de stratégie par tour : 22,6 ; 3,9 ; 2,5 ; 1,5 ; 1,0 ; 0,7 ; 0,5 ; 0,3 points. Avec 3 tours (ancien réglage du banc d'essai), la stratégie n'était pas stabilisée : le contrôle de stabilité la refuse. Le calage change peu (perte 12,1 mBB après 3 tours, 11,6 après 8 ; plancher de la référence 6,9).

Sans jeu après le flop (modèle showdown), la perte monte à 31 mBB en heads-up 12 BB et à 158 mBB à 3 joueurs 12 BB : le modèle postflop est indispensable dès que limps et petites relances existent.
