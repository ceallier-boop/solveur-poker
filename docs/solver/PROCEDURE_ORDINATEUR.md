# Calculs longs du solveur sur ton ordinateur (actions O1, O3, O5)

Les calculs de plusieurs heures ne tournent pas dans la session cloud : ils se lancent sur ton ordinateur, puis tu renvoies les fichiers produits. Rien ici ne touche la référence ni l'application.

| Action | Ce que ça calcule | Durée sur 4 cœurs | Fichiers à renvoyer |
|---|---|---|---|
| O1 | Installation (une fois) | 10 minutes | — |
| O3 | Résolution exacte au flop, pour comparer les réglages de regroupement après le flop (G13) | environ 4 h 15 | `docs/solver/exact_flop_hu25_raise_g13.json`, `docs/solver/exact_flop_hu25_iso_g13.json` |
| O5 | Grille complète du solveur sur l'arbre v5 (58 configurations), après le choix du réglage (G16) | environ 12 h | `data/solver/runs/<dossier>/` et `data/datasets/gto_preflop/<version>/` |

## Matériel

- 4 cœurs au moins ; plus il y en a, plus c'est court (le calcul exact et les sous-jeux postflop se répartissent sur tous les cœurs).
- **16 Go de mémoire** : le calcul exact de l'iso payé en utilise environ 7 Go.
- 2 Go d'espace disque.
- Linux, macOS ou Windows. L'ordinateur doit rester allumé et ne pas se mettre en veille pendant le calcul (réglages d'alimentation).

## O1 : installation (une fois)

1. Installer Python 3.11 ou plus récent (testé avec 3.13) : <https://www.python.org/downloads/> ; sous Windows, cocher « Add python.exe to PATH ». Installer git : <https://git-scm.com/downloads>.
2. Dans un terminal (sous Windows : « Invite de commandes » ou PowerShell) :

```bash
git clone https://github.com/ceallier-boop/solveur-poker.git
```

```bash
cd solveur-poker
```

```bash
git checkout claude/poker-expresso-training-app-b63kf9
```

```bash
python -m venv .venv
```

3. Activer l'environnement, à refaire à chaque nouveau terminal. Linux et macOS :

```bash
source .venv/bin/activate
```

Windows :

```bash
.venv\Scripts\activate
```

4. Installer les dépendances, puis vérifier l'installation (deux minutes, tout doit être « passed ») :

```bash
pip install -r requirements.txt
```

```bash
python -m pytest -q tests/test_exact_flop.py tests/test_solver_dataset.py
```

Avant chaque calcul, mettre le code à jour :

```bash
git pull
```

## O3 : mesurer les réglages de regroupement après le flop (après G13)

Deux commandes, l'une après l'autre (dans le dossier `solveur-poker`, environnement activé). Chacune résout exactement 5 flops (les mêmes que la mesure G9 du 30/10) et y rejoue la stratégie des 5 réglages de regroupement : `production`, `ehs2`, `ehs2_flop32`, `ehs2_texture`, `ehs2_flop32_texture`.

```bash
python tools/solver/exact_flop_check.py --spot raise --flops 5 --iters 100 --variants all --out docs/solver/exact_flop_hu25_raise_g13.json
```

```bash
python tools/solver/exact_flop_check.py --spot iso --flops 5 --iters 100 --variants all --out docs/solver/exact_flop_hu25_iso_g13.json
```

Durées sur 4 cœurs : environ 1 h 20 pour la première, 2 h 55 pour la seconde. Chaque flop affiche une ligne de progression ; à la fin, un tableau compare les réglages (écart avec l'exact, transfert de valeur entre familles de mains, exploitabilité). Si un calcul s'arrête, relancer la même commande : elle repart du début de cette situation.

Fichiers à renvoyer : `docs/solver/exact_flop_hu25_raise_g13.json` et `docs/solver/exact_flop_hu25_iso_g13.json`.

## O5 : grille complète sur l'arbre v5 (après G16)

G16 choisit le réglage de regroupement d'après O3 ; la commande exacte, avec ce réglage et le numéro de version, sera donnée à ce moment-là. Sa forme :

```bash
python -m spinsacademy.solver.dataset --version 2026.11.JJ-s2 --grid p1 --tree v5 --postflop <réglage choisi> --workers <nombre de cœurs>
```

- `--tree v5` : ouvertures à 2 BB (BTN et SB, à 3 joueurs comme en heads-up), tapis direct toujours proposé.
- `--workers` : mettre le nombre de cœurs de l'ordinateur.
- Environ 12 h sur 4 cœurs : 3 à 8 minutes par configuration heads-up, 15 à 20 minutes à 3 joueurs. Une ligne s'affiche pour chaque configuration terminée.
- **Reprise** : chaque configuration terminée est enregistrée tout de suite (`data/solver/runs/`). Si le calcul s'arrête, relancer exactement la même commande : les configurations déjà faites ne sont pas recalculées.
- À la fin : « N spots publiés en staging ». La banque n'est pas servie aux joueurs : elle passe ensuite les contrôles du catalogue.

Fichiers à renvoyer : le dossier `data/solver/runs/<dossier>/` créé par le calcul (son nom commence par l'empreinte de l'arbre) et le dossier `data/datasets/gto_preflop/<version>/`.

## Renvoyer les résultats

Au choix.

**Par git** (si ton compte GitHub a accès au dépôt). Après O3 :

```bash
git checkout -b calculs/o3
```

```bash
git add docs/solver/exact_flop_hu25_raise_g13.json docs/solver/exact_flop_hu25_iso_g13.json
```

```bash
git commit -m "O3 : mesure exacte des réglages de regroupement"
```

```bash
git push -u origin calculs/o3
```

Après O5, de même sur une branche `calculs/o5`, avec `git add data/solver/runs data/datasets/gto_preflop`.

**Par archive** : compresser les fichiers ou dossiers indiqués (clic droit, « Compresser » ou « Envoyer vers > Dossier compressé ») et joindre le `.zip` à la conversation.
