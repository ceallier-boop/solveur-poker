# Exports HRC à produire

Ces calculs se lancent sur le poste où HRC est installé (`C:\Users\eline\AppData\Local\Programs\HoldemResources\HRC\hrc.exe`).
La session Claude dans le cloud ne peut pas piloter HRC : elle prépare les entrées, puis importe et valide les exports reçus.

## 0. Réglages communs (arbre de référence)

**Tous** les calculs utilisent les réglages des exports `complement` et `complement2`. C'est l'empreinte d'arbre `00a1dd91` dans `data/hrc/README.md`. Le plus simple : ouvrir l'une de ces mains dans HRC (par exemple 12 / 12 / 12 = `complement2/hand_7`) et ne changer que les stacks.

| Réglage | Valeur |
|---|---|
| Modèle | chip EV, sans rake |
| Blinds / ante | BB 10 000, SB 5 000, ante 0 (stacks exprimés en jetons : 1 BB = 10 000) |
| Moteur | Monte-Carlo, abstractions 169 / 256 / 256 / 256 |
| `ALLOWED_FLATS_PER_RAISE` | `[1, 1, 1, 1, 0]` (**limp du BTN autorisé**) |
| `ALLOW_SB_COMPLETE` | oui |
| `ALLOW_COLD_CALLS` | non |
| Opens | BTN 2,3 BB + 1 BB, SB 3,5 BB + 1 BB, BB iso 3,5 BB + 1 BB (3 BB face au SB) |
| 3-bets | BB contre SB 2,5x ; SB contre BB 2,6x + 1x ; en position 2,5x + 1x ; autres 3,3x + 1x |
| 4-bets, 5-bets | 90 % ou all-in en position, 120 % ou all-in hors de position |
| All-in ajouté | SPR préflop 7, seuil 40 % ; postflop SPR 5, mise géométrique 66 %, pas de donk |

**Profondeur d'export :** si HRC propose de choisir les nœuds à exporter, exporter **tous les nœuds préflop**. Les exports actuels s'arrêtent souvent à deux actions ; par exemple, la réponse du SB à un iso-raise du BB manque.

## 1. Calculs GTO manquants (priorité 1) — **reçus le 12 octobre 2026** (`data/hrc/raw/v2/`)

Objectif : une solution HRC à chaque profondeur proposée dans les quiz (4 à 25 BB), toutes avec le même arbre. L'interpolation entre profondeurs coûte trop cher (8 à 64 mBB par main).

| Table | Stacks à calculer | Pourquoi |
|---|---|---|
| 3 joueurs | 8, 10, 18, 25 | Existent seulement sans limp du BTN (`min_raise_3way`). Le BTN limpe 7 à 11 % de ses mains dès 12 BB |
| 3 joueurs | 16, 22 | Absents |
| Heads-up | 14, 16, 22 | Absents |

À stacks égaux, après ces calculs, la grille couvre :
- 3 joueurs : 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25 ;
- heads-up : 2, 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25.

## 2. Calculs exploitants par verrouillage de nœuds (node locking)

Fichiers générés par `python tools/hrc/make_locks.py` dans `data/hrc/locks/` :
- `manifest.csv` : la liste des calculs, avec priorité ;
- un dossier par calcul, `<profil>/<table>_<stacks>/hero_<position>/`, qui contient `ranges.txt` (lisible, à coller dans HRC) et `locks.json` (même contenu, pour les scripts).

**135 calculs**, dont **45 en priorité P1** (12, 15 et 20 BB) ; la liste a été recalculée après réception de la base v2 :
- 3 profils : nit, fish, maniac. Le profil Shark est inutile : c'est la solution GTO.
- Chaque position du héros : BTN, SB, BB à 3 joueurs ; SB, BB en heads-up.
- Stacks égaux à partir de 10 BB. En dessous, les décisions sont surtout tout ou rien, et `exploit_engine` et `exp_hu_solver` couvrent déjà l'exploitant.

Procédure pour un calcul :
1. Ouvrir la main GTO indiquée en colonne `gto_source`.
2. Pour chaque bloc `=== Nœud ...` de `ranges.txt`, verrouiller ce nœud (joué par l'adversaire indiqué). Coller pour chaque action la range donnée : notation `main:poids`, poids entre 0 et 1, et une main seule vaut 1. Les nœuds du héros restent libres.
3. Recalculer, puis exporter dans un dossier nommé exactement comme `solve_id` (par exemple `nit_3w_15-15-15_heroBTN`).

**À tester d'abord sur un seul nœud :** si HRC refuse la notation `main:poids` ou attend des pourcentages, indiquez-moi le format accepté et je régénère les fichiers.

Ils couvrent maintenant toutes les profondeurs de 10 à 25 BB, à 3 joueurs comme en heads-up, base v2 comprise.

### Règles des profils (à valider)

| Profil | Agressivité (raise, all-in) | Passivité (limp, call) | Mains retirées de l'agressivité |
|---|---|---|---|
| nit | cotes × 0,5 | cotes × 0,5 | vont au fold |
| fish | cotes × 0,9 | cotes × 2,0 | deviennent limp ou call |
| maniac | cotes × 2,0 | cotes × 1,3 | vont au fold |

« Cotes × k » : une fréquence p devient k·p / (1 + (k − 1)·p). C'est la convention du moteur exploitant existant ; les facteurs sont ceux de `exploit_engine.PROFILES`.

Les mains ajoutées sont prises dans le fold (ou dans le check, quand checker est gratuit), des plus fortes aux plus faibles. Les mains retirées sont les plus faibles.

## 3. Livraison

Déposer chaque export (dossier `settings.json` + `nodes/`) dans une archive, comme les précédentes. Les exports seront importés dans `data/hrc/raw/` : `gto/` pour le §1, `locks/` pour le §2. Ils seront ensuite validés (arbre, stacks, normalisation, nœuds verrouillés bien respectés) et jamais embarqués dans l'application.

## 4. Arrondis

Les stratégies affichées dans l'application sont arrondies : action dominante, ou mélange au pas de 5 % ou 10 %, à fixer avec la maquette. La correction des réponses reste calculée sur les valeurs exactes, avant arrondi.

## 5. Précision des calculs (constat sur les exports reçus)

`docs/hrc/VALIDATION_HRC.md` compare l'EV exportée par HRC à l'EV exacte sur les calls d'all-in. En heads-up, le calcul est exact. L'écart moyen croît avec la profondeur :
- 7 mBB à 2 BB et 42 mBB à 8 BB ;
- 100 à 140 mBB à 12–14 BB ;
- 180 à 210 mBB à 15 BB ;
- plus de 300 mBB à 18 BB à 3 joueurs (calcul approché à 3 joueurs).

Le bruit vient du Monte-Carlo de HRC sur les nœuds peu fréquents : plus la range de shove adverse est étroite, plus il est fort. Il fausse aussi quelques décisions (J8s payé à 92 % à 15 BB alors que son EV exacte est de −0,22 BB).

Conséquences :
- **côté application** : les corrections de décisions tout ou rien utilisent l'EV exacte recalculée à partir des ranges HRC, pas l'EV HRC ;
- **côté HRC, si possible** : relancer les calculs P1 avec une précision plus élevée (temps de calcul ou nombre d'itérations plus grand, selon les réglages de convergence proposés par HRC) et exporter **tous les nœuds préflop**. Les exports v2 s'arrêtent encore à deux actions.
