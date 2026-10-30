# Exports de référence à produire

Ces calculs se lancent sur le poste où le solveur de référence est installé.
La session Claude dans le cloud ne peut pas piloter de référence : elle prépare les entrées, puis importe et valide les exports reçus.

## 0. Réglages communs (arbre de référence)

**Tous** les calculs utilisent les réglages des exports `complement` et `complement2`. C'est l'empreinte d'arbre `00a1dd91` dans `data/hrc/README.md`. Le plus simple : ouvrir l'une de ces mains dans la référence (par exemple 12 / 12 / 12 = `complement2/hand_7`) et ne changer que les stacks.

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

**Profondeur d'export :** si la référence propose de choisir les nœuds à exporter, exporter **tous les nœuds préflop**. Les exports actuels s'arrêtent souvent à deux actions ; par exemple, la réponse du SB à un iso-raise du BB manque.

## 1. Calculs GTO manquants (priorité 1) — **reçus le 12 octobre 2026** (`data/hrc/raw/v2/`)

Objectif : une solution de référence à chaque profondeur proposée dans les quiz (4 à 25 BB), toutes avec le même arbre. L'interpolation entre profondeurs coûte trop cher (8 à 64 mBB par main).

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
- un dossier par calcul, `<profil>/<table>_<stacks>/hero_<position>/`, qui contient `ranges.txt` (lisible, à coller dans la référence) et `locks.json` (même contenu, pour les scripts).

**180 calculs**, dont **60 en priorité P1** (12, 15 et 20 BB) ; liste recalculée le 29/10/2026 sur la base v3, avec les profils du moteur exploitant :
- 4 profils, ceux du mode exploitant (`tools/field/profils_field.py`) : rec passif (profil par défaut, 55 % du field), calling station, dégène, nit. Le reg est inutile : ses facteurs valent 1, c'est la solution GTO. Les anciens profils nit / fish / maniac (facteurs de l'ancien moteur) sont abandonnés : les calculs verrouillés jouent désormais contre les mêmes vilains que les questions de l'application.
- Chaque position du héros : BTN, SB, BB à 3 joueurs ; SB, BB en heads-up.
- Stacks égaux à partir de 10 BB. En dessous, les décisions sont surtout tout ou rien, et `exploit_engine` et `exp_hu_solver` couvrent déjà l'exploitant.

Procédure pour un calcul :
1. Ouvrir la main GTO indiquée en colonne `gto_source`.
2. Pour chaque bloc `=== Nœud ...` de `ranges.txt`, verrouiller ce nœud (joué par l'adversaire indiqué). Coller pour chaque action la range donnée : notation `main:poids`, poids entre 0 et 1, et une main seule vaut 1. Les nœuds du héros restent libres.
3. Recalculer, puis exporter dans un dossier nommé exactement comme `solve_id` (par exemple `nit_3w_15-15-15_heroBTN`).

**À tester d'abord sur un seul nœud :** si la référence refuse la notation `main:poids` ou attend des pourcentages, indiquez-moi le format accepté et je régénère les fichiers.

Ils couvrent maintenant toutes les profondeurs de 10 à 25 BB, à 3 joueurs comme en heads-up, base v2 comprise.

### Règles des profils (à valider)

Les facteurs sont lus dans `tools/field/profils_field.py` : changer un profil (par exemple après la calibration B2) et relancer `make_locks.py` suffit. Le facteur appliqué dépend de la situation du vilain, comme dans le moteur exploitant :

| Situation du vilain | Actions déformées | Facteur |
|---|---|---|
| premier à parler | relance et tapis / limp | `shove` / `limp_k` |
| face à un limp | iso (relance, tapis) / limp derrière | `iso` / `limp_k` |
| face à une relance ou un tapis | continuer (payer, relancer) | `call` |

| Profil | `shove` | `call` | `iso` | `limp_k` | Mains retirées de l'agressivité, premier à parler |
|---|---|---|---|---|---|
| rec passif | 0,6 | 0,6 | 0,4 | 2,0 | deviennent limp ; la moitié de la baisse sur ses mains fortes, As faibles gardés |
| calling station | 0,8 | 1,8 | 0,5 | 2,0 | idem |
| dégène | 2,0 | 1,3 | 2,0 | 0,6 | vont au fold |
| nit | 0,5 | 0,5 | 0,5 | 0,7 | vont au fold |

Rec passif : facteurs de 12 BB, valables jusqu'à 25 BB faute de mesure (le moteur fait de même) ; de 4 à 12 BB, ils suivent la profondeur.

« Cotes × k » : une fréquence p devient k·p / (1 + (k − 1)·p). C'est la convention du moteur exploitant.

Les mains ajoutées sont prises dans le fold (ou dans le check, quand checker est gratuit), des plus fortes aux plus faibles. Les mains retirées sont les plus faibles, sauf la part prise sur les mains fortes des récréatifs.

## 3. Livraison

Déposer chaque export (dossier `settings.json` + `nodes/`) dans une archive, comme les précédentes. Les exports seront importés dans `data/hrc/raw/` : `gto/` pour le §1, `locks/` pour le §2. Ils seront ensuite validés (arbre, stacks, normalisation, nœuds verrouillés bien respectés) et jamais embarqués dans l'application.

## 4. Arrondis

Les stratégies affichées dans l'application sont arrondies : action dominante, ou mélange au pas de 5 % ou 10 %, à fixer avec la maquette. La correction des réponses reste calculée sur les valeurs exactes, avant arrondi.

## 5. Précision des calculs (constat sur les exports reçus)

`docs/reference/VALIDATION_REFERENCE.md` compare l'EV exportée par la référence à l'EV exacte sur les calls d'all-in. En heads-up, le calcul est exact. L'écart moyen croît avec la profondeur :
- 7 mBB à 2 BB et 42 mBB à 8 BB ;
- 100 à 140 mBB à 12–14 BB ;
- 180 à 210 mBB à 15 BB ;
- plus de 300 mBB à 18 BB à 3 joueurs (calcul approché à 3 joueurs).

Le bruit vient du Monte-Carlo de la référence sur les nœuds peu fréquents : plus la range de shove adverse est étroite, plus il est fort. Il fausse aussi quelques décisions (J8s payé à 92 % à 15 BB alors que son EV exacte est de −0,22 BB).

Conséquences :
- **côté application** : les corrections de décisions tout ou rien utilisent l'EV exacte recalculée à partir des ranges de référence, pas l'EV de référence ;
- **côté de référence, si possible** : relancer les calculs P1 avec une précision plus élevée (temps de calcul ou nombre d'itérations plus grand, selon les réglages de convergence proposés par la référence) et exporter **tous les nœuds préflop**. Les exports v2 s'arrêtent encore à deux actions.

## 6. Calculs demandés après l'évaluation par un joueur (2026-10-13)

Constats : tapis presque toujours symétriques ou en motifs fixes ; peu de décisions au BTN ; une seule taille de relance ; mode exploitant limité au call d'un tapis ; pas de postflop. Ces points ne se corrigent pas sans nouveaux calculs : l'application n'invente aucune solution.

### 6.1 Tapis déséquilibrés (priorité 1)

Même arbre de référence (§0), chip EV, une sortie par configuration (BTN / SB / BB, en BB). Au total 75 BB à trois joueurs, configurations rencontrées en partie :

| 3 joueurs | | | | heads-up |
|---|---|---|---|---|
| 35 / 25 / 15 | 25 / 35 / 15 | 15 / 25 / 35 | 35 / 15 / 25 | 30 / 20 |
| 40 / 20 / 15 | 20 / 40 / 15 | 15 / 20 / 40 | 30 / 30 / 15 | 35 / 15 |
| 45 / 20 / 10 | 20 / 45 / 10 | 10 / 20 / 45 | 30 / 25 / 20 | 40 / 10 |
| 50 / 15 / 10 | 15 / 50 / 10 | 25 / 25 / 25 | 20 / 30 / 25 | 20 / 30 |

Chaque position occupe tour à tour le plus gros et le plus petit tapis, pour que le BTN ait autant de décisions que les blindes.

### 6.2 Plusieurs tailles de relance (priorité 2)

Sur 6 configurations (12, 16, 20 BB symétriques ; 35/25/15, 40/20/15, 30/20 HU) : ajouter à l'open du BTN 2 BB et 2,5 BB, à l'open du SB 2,5 BB et 3 BB, à l'iso du BB 2,5 BB et 4 BB. Les questions pourront alors porter sur le choix de taille.

### 6.3 Mode exploitant au-delà du call d'un tapis (priorité 2)

Les 180 calculs verrouillés du §2 couvrent les limps, les limp-relances et les opens. Ajouter, pour les profils de l'évaluation :
- BB qui se couche trop face aux opens et aux limps (défense réduite de 30 % et 50 %) ;
- joueur qui limp-relance trop (fréquence de limp-relance x 2) ;
- joueur qui ouvre en min-raise trop large (open x 1,5).

### 6.4 Postflop dans les pots limpés (priorité 3)

Pour 15 à 25 BB, pots limpés heads-up et à trois : exports postflop de référence (flop, avec les ranges d'entrée) sur une sélection de textures de board. Le solveur postflop maison n'est pas encore assez précis pour servir de référence (`docs/solver/CONTROLE_ABSTRACTION.md`).

### 6.5 ICM

Les calculs restent en chip EV (décision du porteur du projet). Pour les gros multiplicateurs, où plusieurs places sont payées, il faudrait des calculs ICM séparés : hors périmètre actuel.

## 7. Calculs demandés après les relectures croisées (2026-10-13, `docs/audit/RELECTURES_2026-10-13.md`)

Validé par le porteur du projet : ces situations sont à ajouter à la liste d'exports. Même arbre de référence (§0), chip EV.

### 7.1 Tapis à toutes les profondeurs (priorité 1)

L'arbre actuel retire le tapis direct trop tôt : le SB premier à parler (3 joueurs et heads-up) et le BB face à un limp n'ont plus l'option tapis à partir de 16 BB, le BTN premier à parler à partir de 20 BB. Garder l'option tapis de 4 à 25 BB pour chaque nœud (11 spots SB concernés aujourd'hui), pour que l'application n'enseigne pas une coupure artificielle.

### 7.2 Décisions après la première action (priorité 1)

- BTN face à l'iso-relance, à la sur-relance et au tapis du SB ou du BB après son open ou son limp ;
- SB face au BB après avoir complété à 3 joueurs (`BTN-fold_SB-call_BB-raise` et `BTN-fold_SB-call_BB-allin`) ;
- multiway : BB face à un limp du BTN puis un complément du SB, squeeze du SB ou du BB après open et call, sur-call d'un tapis.

### 7.3 Tailles d'ouverture (priorité 2)

Ouvertures à 2 et 2,5 BB en plus de 2,3 BB (BTN) et de 3,5 BB (SB), notamment en heads-up sous 12 BB, où une ouverture à 3,5 BB engage plus du tiers du tapis. Complète le §6.2.

### 7.4 Précision (priorité 2)

Sur les mains où l'EV exacte existe, l'EV de référence s'en écarte de 58 mBB en médiane et de 251 mBB au 90e centile (3 à 12 fois la tolérance de correction). En attendant des calculs plus précis, l'application ne tire plus les questions de référence dont la leçon coûte moins de 150 mBB (`quiz.REF_NOISE_MBB`). Des exports à précision plus élevée (plus d'itérations, mode postflop uniforme : certaines profondeurs viennent de `v2/general`, d'autres de `complement2/simple`) permettraient de baisser ce seuil.

## 8. Réception de la base v3 (13 octobre 2026)

| Demande | Statut |
|---|---|
| §6.1 tapis déséquilibrés (16 configurations à 3 joueurs, 4 en heads-up) | **reçu** |
| §6.2 / §7.3 tailles d'ouverture (BTN 2 / 2,3 / 2,5 BB ; SB 2,5 / 3 / 3,3 / 3,5 BB ; heads-up SB 2 BB) | **reçu** (5 arbres en plus de la référence) |
| §7.2 décisions après la première action, pots à trois, squeeze, sur-call | **reçu** (arbre complet) |
| §7.1 tapis direct du SB et du BB au-delà de 16 BB, du BTN au-delà de 20 BB | à produire : réglages d'arbre inchangés |
| §7.4 précision (plus d'itérations) | à produire : moteur et abstractions inchangés, écarts avec l'EV exacte identiques à v2 |
| §6.3 exploitant au-delà du call d'un tapis, §6.4 postflop | à produire |

## 9. Commande consolidée après la base v3 (14 octobre 2026)

Ce qui reste à produire pour terminer le plan de l'évaluation du MVP (`docs/produit/PLAN_EVALUATION_MVP_2026-10-14.md`). Réglages de l'arbre de référence (§0, empreinte préflop `daa9aaa0`), mode postflop « simple », **arbre complet** (tous les nœuds préflop, comme la base v3), chip EV.

### 9.1 Précision (priorité 1) : débloque les décisions serrées

Constat : l'EV de référence s'écarte de l'EV exacte de 35 mBB en médiane en heads-up et de 66 mBB à 3 joueurs (jusqu'à 200-300 mBB au 90e centile), à moteur et réglages identiques en v2 et v3. D'où le filtre qui écarte les questions dont la leçon coûte moins de 150 mBB.
1. **Test d'abord** sur deux mains : 12 / 12 / 12 et heads-up 12 / 12, en doublant puis en quadruplant le nombre d'itérations (ou la cible de convergence). Je mesure l'écart avec l'EV exacte et j'en déduis le réglage utile.
2. Puis refaire au réglage retenu toutes les profondeurs symétriques : 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25 BB, à 3 joueurs et en heads-up.

### 9.2 Tapis direct à toutes les profondeurs (priorité 1)

Dans l'arbre actuel, le tapis direct disparaît : pour le SB premier à parler et le BB face à un limp à partir de 16 BB, pour le BTN premier à parler à partir de 20 BB (`PREFLOP_ADD_ALLIN_SPR` 7, `PREFLOP_ALLIN_THRESHOLD` 40). Toujours proposer le tapis jusqu'à 25 BB effectifs : par exemple `PREFLOP_ADD_ALLIN_SPR` à 30 (à vérifier dans la référence). À combiner avec le 9.1 (mêmes mains : 16, 18, 20, 22, 25 BB, à 3 joueurs et en heads-up).

### 9.3 Heads-up (priorité 1) : cible de 35 % des questions

Déjà couverts sur l'arbre de référence : 2 à 25 BB symétriques, et 4/8, 8/4, 20/30, 30/20, 35/15, 40/10. Manque :
- **tailles d'ouverture du SB** : 2 BB (min-raise), 2,5 BB et 3 BB à 8, 10, 12, 14, 16, 18, 20, 25 BB (le SB 2 BB n'existe aujourd'hui que de 4 à 16 BB) ;
- **tapis déséquilibrés** : 10/20, 20/10, 12/18, 18/12, 15/25, 25/15 ;
- **arbre complet** pour 15/15, 20/20, 4/8, 8/4, 2/2, 4/4, 6/6, aujourd'hui issus d'exports anciens à deux actions au plus.

### 9.4 Arbre complet pour les configurations anciennes à 3 joueurs (priorité 2)

Encore servies depuis les bases `complement` et `complement2` (8 à 11 nœuds au lieu de 30 à 70) : 4/4/4, 6/6/6, 14/14/14, 15/15/15, 4/4/8, 4/8/4, 4/8/8, 8/4/4, 8/4/8, 8/8/4, 12/12/18, 12/18/12, 18/12/12, 18/12/18, 18/18/12, 14/18/18. Les refaire en arbre complet.

### 9.5 Tailles d'ouverture à 3 joueurs (priorité 2)

Les arbres BTN 2 BB / SB 3 BB, BTN 2 BB / SB 2,5 BB et BTN 2,5 BB / SB 3,5 BB n'existent qu'à 12, 16 et 20 BB. Ajouter 8, 10, 14, 18, 22 et 25 BB.

### 9.6 Mode exploitant au-delà du call d'un tapis (priorité 2)

Les 180 calculs verrouillés du §2 (dont 60 en P1 : 12, 15 et 20 BB) : profils rec passif, calling station, dégène, nit, sur les limps, les limp-relances et les opens. À tester d'abord sur un seul nœud pour valider la notation `main:poids`. (L'open-shove contre un joueur qui paie trop ne demande rien : je le calcule exactement.)

### 9.7 Postflop minimal (priorité 3)

Pots limpés à 15-25 BB, heads-up et à trois : exports postflop de référence au flop, avec les ranges d'entrée, sur environ 20 textures de board représentatives (sèche, assortie, connectée, paire, haute, basse). C'est la condition pour un contenu « après le flop » qui ne soit pas seulement statistique.

### 9.8 Hors périmètre sauf décision

ICM (gros multiplicateurs) : calculs séparés avec la structure de gains Expresso, seulement si le porteur du projet sort du chip EV.

### Livraison

Une archive par lot, comme la base v3 (dossier `settings.json` + `nodes/` par main). Je vérifie à chaque réception : arbre et réglages, précision contre l'EV exacte, couverture, et je publie un nouveau dataset après contrôle.

### 9.9 Résultat du test de précision (14/10)

Voir `docs/reference/TEST_PRECISION_2026-10-14.md` : les 4 exports reçus par configuration ne sont pas plus précis les uns que les autres, mais leur moyenne divise l'écart par 2 environ (bruit aléatoire). Ils utilisaient un arbre sans limp en premier de parole (`ALLOWED_FLATS_PER_RAISE` = `[0, 1, 1, 1, 0]`) : à refaire sur l'arbre de référence `[1, 1, 1, 1, 0]`.

## 10. Commande v4 (26 octobre 2026) : une base unique, précise et cohérente

Objectif : remplacer toutes les bases précédentes par **un seul arbre de référence**, refait à toutes les profondeurs, assez précis pour que les ranges ne paraissent plus bruitées. Constats des tests joueurs 4 à 6 à l'origine de cette commande :
- références jugées bruitées (bluffs isolés : 42s relance mais KQs limpe, 76s à laisser mais 95s à jouer) ;
- une même situation calculée dans plusieurs arbres (relance à 2 ou 3 BB), donc des mains en jeu qui ne suivent pas la stratégie servie au coup précédent ;
- tapis direct absent au-delà de 16 BB (SB, BB face à un limp) et de 20 BB (BTN) ;
- tapis presque toujours ronds et symétriques ;
- bruit des EV par main : 100 mBB en médiane, d'où le filtre `REF_NOISE_MBB` à 150 mBB qui écarte les décisions serrées.

### 10.1 Réglages de l'arbre (identiques pour tous les calculs)

| Réglage | Valeur | Changement par rapport à la base v3 |
|---|---|---|
| Modèle | chip EV, sans rake, ante 0, blinds 0,5 / 1 | — |
| Moteur | Monte-Carlo, abstractions 169 / 256 / 256 / 256 | — (le moteur « enumerated » ne joue pas le postflop : écarté) |
| Postflop | mode « simple » partout | v2 mélangeait « general » et « simple » |
| `ALLOWED_FLATS_PER_RAISE` | `[1, 1, 1, 1, 0]` (limp du BTN autorisé) | — (le test de précision du 14/10 l'avait à `[0, …]` : à ne pas reprendre) |
| `ALLOW_SB_COMPLETE` | oui | — |
| Tailles d'ouverture | **choix A** ci-dessous | un seul jeu de tailles pour toutes les profondeurs |
| 3-bets, 4-bets, 5-bets | comme au §0 | — |
| Tapis direct | toujours proposé jusqu'à 25 BB effectifs (par exemple `PREFLOP_ADD_ALLIN_SPR` à 30 ; à vérifier dans la référence) | nouveau (§7.1, §9.2) |
| Nœuds exportés | **tous les nœuds préflop** (arbre complet) | les bases `complement` s'arrêtaient à deux actions |

### 10.2 Configurations

| Lot | Configurations | Nombre |
|---|---|---|
| P1 symétriques, 3 joueurs | 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25 BB | 12 |
| P1 symétriques, heads-up | 2, 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25 BB | 13 |
| P1 inégaux, heads-up (SB / BB) | 4/8, 8/4, 10/20, 20/10, 12/18, 18/12, 15/25, 25/15, 20/30, 30/20, 35/15, 15/35 | 12 |
| P1 inégaux, 3 joueurs (BTN / SB / BB) | les 16 du §6.1, plus les 6 permutations de 6 / 10 / 14 | 22 |
| P2 tailles d'ouverture | si le choix A garde une seule taille : un arbre par taille alternative, à 12, 16 et 20 BB (3 joueurs et heads-up), pour de futures questions « quelle taille ? » | 6 par taille |
| P2 exploitant verrouillé | les 60 calculs P1 du §2 (`data/hrc/locks/manifest.csv`), après le choix E ; rec passif d'abord (15 calculs) s'il faut réduire | 60 |
| P3 postflop | §9.7 (pots limpés, environ 20 textures) | — |

Total P1 : 59 configurations, multipliées par le nombre de répétitions (choix B).

### 10.3 Choix à faire avant de lancer

- **A. Tailles d'ouverture.** Recommandé : BTN 2 BB ; SB 3 BB à 3 joueurs et 2 BB en heads-up ; iso du BB 3 BB face au limp du SB, 3,5 BB face au limp du BTN (+1 BB par limper en plus). Ce sont les tailles courantes en Expresso, et tout est refait de toute façon. Autre choix : garder BTN 2,3 BB / SB 3,5 BB, ce qui permet de réutiliser la base v3 comme une répétition de plus.
- **B. Précision.** Recommandé : 4 exports identiques par configuration P1 symétrique, 2 par configuration inégale ; l'importeur fait la moyenne des EV et des fréquences. Mesuré le 14/10 : l'écart avec l'EV exacte passe de 100 à 42 mBB en médiane (heads-up 12 BB) avec 4 exports. Si la référence propose un réglage de précision des EV par main (échantillons d'évaluation), le tester d'abord sur le pilote (10.4) : il peut remplacer les répétitions.
- **C. Périmètre des tapis.** Les 59 configurations P1, ou seulement les 25 symétriques dans un premier temps.
- **D. Modèle.** Recommandé : chip EV (décision du 13/10). L'ICM ne vaut que pour les gros multiplicateurs.
- **E. Exploitant verrouillé.** Recommandé : après l'historique de mains (B2), qui calibre les profils. Sans lui, les verrouillages reposent sur des profils supposés.
- **F. Postflop.** Recommandé : plus tard (lot C1).

### 10.4 Ordre de production

1. **Pilote** : 3 joueurs 12 / 12 / 12 et heads-up 12 / 12, sur l'arbre final, en 4 exports chacun. Je contrôle l'arbre (empreinte, tapis direct, nœuds complets), la précision contre l'EV exacte et la moyenne des répétitions, avant que tu lances le reste.
2. P1 symétriques, puis P1 inégaux.
3. P2 et P3 selon les choix.

### 10.5 Livraison

- Un dossier par export : `v4/<table>_<tapis>_r<n>/` avec `settings.json` et `nodes/`, par exemple `v4/3w_12-12-12_r1/` ou `v4/hu_10-20_r2/` (tapis dans l'ordre BTN / SB / BB, ou SB / BB en heads-up).
- Un fichier `NOTES.txt` par lot : version de la référence, réglage de précision ou nombre d'itérations, durée d'un calcul. Ces informations ne figurent pas dans `settings.json`.
- Les exports restent dans `data/hrc/raw/v4/` : jamais embarqués dans l'application.

### 10.6 Ce que je fais à réception

Moyenne des répétitions dans l'importeur, contrôle de chaque lot, reconstruction de la banque GTO sur ce seul arbre, baisse du filtre de bruit selon la précision mesurée, puis nouveau test joueurs.

Droits sur les données de référence (A13) : réglés le 26/10/2026, l'usage respecte les conditions de l'éditeur. Les exports bruts ne sont jamais embarqués dans l'application.
