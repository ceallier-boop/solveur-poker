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

### Convergence préflop / postflop : amortissement fixe ou moyenne des tours (29/10/2026)

Heads-up 25 BB, 10 tours. Dérive = exploitabilité de la stratégie du tour précédent dans le modèle du nouveau tour (mBB par main) ; elle comprend l'exploitabilité propre du préflop, environ 0,45 mBB à 1 500 itérations.

| Tour | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|
| Amortissement 0,5 : variation (points) / dérive (mBB) | 5,3 / 4,4 | 1,9 / 1,0 | 2,1 / 0,9 | 3,2 / 3,4 | 2,8 / 1,8 | 1,9 / 1,4 |
| Moyenne des tours (`linear`) | 4,6 / 3,1 | 1,8 / 0,8 | 1,7 / 0,6 | 0,4 / 0,4 | 0,4 / 0,5 | 0,3 / 0,5 |

L'amortissement fixe oscille ; la moyenne des corrections postflop sur tous les tours (le tour k pèse k) converge. Réglage retenu : `linear`, arrêt dès que la dérive passe sous 0,6 mBB, 12 tours au plus ; contrôle bloquant à 1 mBB.

### Pilote `gto_preflop/2026.10.29-s1` (29/10/2026)

| Configuration | Calcul | Tours | Exploitabilité (mBB, pire joueur) | Dérive (mBB) | Spots | Perte / plancher de la référence (mBB) | Accord | TV |
|---|---|---|---|---|---|---|---|---|
| HU 12 / 12 | 169 s | 4 | 0,08 | 0,37 | 7 | 12,3 / 6,9 | 88 % | 13 % |
| HU 25 / 25 | 459 s | 7 | 0,45 | 0,55 | 9 | 54,4 / 33,5 | 81 % | 20 % |
| 3 joueurs 12 / 12 / 12 | 930 s | 6 | 0,13 | 0,38 | 44 | 41,7 / 34,7 | 87 % | 14 % |
| 3 joueurs 25 / 25 / 25 | 1 025 s | 5 | 0,23 | 0,43 | 63 | 100,2 / 114,4 | 86 % | 17 % |

123 spots, 9 378 questions ; tous les contrôles du catalogue réussis. Sur 4 cœurs, compter 3 à 8 minutes par configuration heads-up et 15 à 20 minutes à 3 joueurs : environ 12 heures pour les 58 configurations P1.

À 3 joueurs, la perte reste proche du plancher de la référence (sous le plancher à 25 BB) : l'écart y est du même ordre que le bruit de la référence. Le heads-up 25 BB est le plus éloigné.

### Heads-up 25 BB : l'écart vient du sous-jeu postflop des pots relancés (29/10/2026)

Protocole : le sous-jeu postflop seul, résolu avec les ranges exactes de la référence à l'entrée du flop, sans boucle préflop. Le gain postflop G de l'appelant est comparé à celui qu'implique la référence (EV du call + mise engagée − blind perdue au fold). Écart moyen pondéré par la range de l'appelant, en mBB :

| Variante du solveur postflop | Pot limpé (BB) | Iso payé (SB en position) | Relance payée (BB hors de position) |
|---|---|---|---|
| Production (16 groupes, 24 tirages, mise 66 %) | −35 | −145 | −49 |
| Tapis seulement si SPR ≤ 5 (règle de la référence) | −30 | −145 | −49 |
| Groupes selon le potentiel (`ehs2`) | −23 | −58 | −51 |
| 32 groupes, 48 tirages | −27 | −127 | −50 |
| Mise 50 % | −34 | −108 | −100 |
| Abattage forcé après 2 rues | +21 | −130 | −81 |

- Dans les pots relancés, les valeurs sont plus étalées que chez la référence : grosses paires +200 à +1 100 mBB, petites paires −400 à −1 000 mBB, connecteurs assortis −150 à −300 mBB, broadways +100 à +190 mBB.
- Aucune variante d'abstraction ni de taille de mise ne corrige les petites paires : ce n'est pas la finesse des groupes. L'abattage forcé après 2 rues (lecture possible de `POSTFLOP_FORCE_CHECKDOWN_AFTER` de la référence) n'explique pas non plus l'écart : l'option n'est pas gardée.
- Effet sur la stratégie servie : faible pour les petites paires, qui vont à tapis chez nous comme chez la référence (EV du tapis proches). Visible pour des mains faibles dépareillées face à une relance : J8o se couche chez nous, la référence la paie (+0,13 BB).
- `ehs2` divise par 2,5 l'écart de l'iso payé : piste à confirmer sur la configuration complète.

Rappel du principe : la référence sert à caler, pas à dicter. Son postflop est lui-même simplifié (« simple », 256 groupes Monte-Carlo) et ses EV par main sont bruitées. Un écart avec elle n'est pas forcément une erreur du solveur ; l'arbitre final est la résolution exacte de sous-jeux (`postflop/exact.py`), à étendre au flop pour trancher.

### Résolution exacte à partir du flop : relance payée, heads-up 25 BB (G9, 30/10/2026)

Outil : `tools/solver/exact_flop_check.py --spot raise --flops 5 --iters 100` (moteur `spinsacademy/postflop/exact_flop.py`). Le SB relance à 3,5 BB, le BB paie (hors de position) : pot 7 BB, 21,5 BB derrière ; ranges d'entrée de la référence (`v3/hand_18`). Sur chaque flop : résolution exacte combo par combo (100 itérations de CFR+ alterné, 15 minutes), et stratégie du solveur de production rejouée sur le même flop. Détail : `exact_flop_hu25_raise.json`.

| Flop | Exploitabilité exacte | Exploitabilité de la stratégie de production sur ce flop | G de l'appelant : exact / production (BB) |
|---|---|---|---|
| 7♠ 8♥ J♠ | 0,61 % du pot | 13,4 % | 3,995 / 4,137 |
| 3♠ Q♦ A♦ | 0,59 % | 11,9 % | 3,225 / 3,263 |
| 5♥ 7♦ Q♠ | 0,62 % | 10,9 % | 3,050 / 2,990 |
| 7♣ 9♣ T♣ | 0,60 % | 12,6 % | 3,679 / 3,760 |
| J♥ Q♠ A♠ | 0,65 % | 16,9 % | 3,672 / 3,916 |

Exact − production, mêmes flops (comparaison appariée, sans bruit d'échantillon), en mBB, pondéré par la range de l'appelant :

| Global | Paires | Connecteurs assortis | Autres assorties | Autres dépareillées | As assortis | As dépareillés | Broadways assortis | Broadways dépareillés |
|---|---|---|---|---|---|---|---|---|
| −41 | **+751** | +308 | +85 | +3 | −231 | −180 | −309 | −338 |

Lecture :
- **Le défaut est bien dans notre abstraction postflop**, pas dans la référence : sur les mêmes flops, la stratégie de production sous-évalue les paires (+751 mBB à l'exact) et les connecteurs assortis (+308), et surévalue As et broadways (−180 à −338). C'est le sens de l'écart mesuré contre la référence (paires −480 à −550, broadways +100 à +140) : la référence avait raison sur ce point. Sur la moyenne de la range, l'abstraction ne se trompe que de 41 mBB : elle déplace la valeur entre familles de mains plus qu'elle ne la crée ou la détruit.
- La stratégie de production, partagée entre tous les flops par groupes de force, est exploitable de 11 à 17 % du pot sur un flop donné ; l'exacte de 0,6 %.
- Les mains citées (J8o, 22, 44) ne se comparent à la référence qu'en moyenne sur beaucoup de flops : 5 flops (dont 3 avec une dame et 2 avec un as) ne suffisent pas, l'écart type du G moyen entre flops est de 170 mBB et bien plus par main. Comparaison appariée sur ces flops : production − exact = +331 mBB pour J8o, −746 pour 22, −864 pour 44.
- Suite : corriger l'abstraction là où elle se trompe (groupes selon le potentiel `ehs2`, qui réduisait déjà l'écart avec la référence sur l'iso payé ; stratégie par famille de flops), puis remesurer avec cet outil sur les mêmes flops.

### Résolution exacte à partir du flop : iso payé, heads-up 25 BB (G9, 30/10/2026)

Le SB limpe, le BB relance à 3 BB, le SB paie (en position) : pot 6 BB, 22 BB derrière ; mêmes 5 flops, même protocole (33 minutes par flop). Détail : `exact_flop_hu25_iso.json`.

| Flop | Exploitabilité exacte | Exploitabilité de la stratégie de production | G de l'appelant : exact / production (BB) |
|---|---|---|---|
| 7♠ 8♥ J♠ | 0,62 % du pot | 14,7 % | 3,285 / 3,456 |
| 3♠ Q♦ A♦ | 0,69 % | 17,5 % | 2,620 / 2,515 |
| 5♥ 7♦ Q♠ | 0,62 % | 13,0 % | 2,994 / 2,974 |
| 7♣ 9♣ T♣ | 0,83 % | 14,9 % | 3,046 / 3,224 |
| J♥ Q♠ A♠ | 0,68 % | 18,7 % | 2,386 / 2,333 |

Exact − production, mêmes flops, mBB :

| Global | Paires | Connecteurs assortis | Autres assorties | Autres dépareillées | As assortis | As dépareillés | Broadways assortis | Broadways dépareillés |
|---|---|---|---|---|---|---|---|---|
| +34 | **+713** | +131 | +225 | +165 | −494 | −286 | −359 | −381 |

Même constat que pour la relance payée, en position cette fois : l'abstraction se trompe peu sur la moyenne (+34 mBB) mais sous-évalue les paires (+713 mBB : 66 à −0,07 BB en production contre +1,35 en exact) et les mains spéculatives, et surévalue As et broadways de 290 à 490 mBB. Les deux pots relancés donnent la même signature : **c'est notre abstraction postflop qu'il faut corriger**, la référence avait raison sur le sens de l'écart. (Dans le fichier, 88, TT et QQ valent 0 : elles ne sont pas dans la range qui paie l'iso.)

### Conclusion de G9

La résolution exacte au flop tranche les désaccords : les écarts entre notre solveur et la référence dans les pots relancés viennent de notre abstraction postflop (groupes de force partagés entre tous les flops), qui déplace la valeur des paires et des mains spéculatives vers les As et les broadways. Correction à faire, mesurée avec cet outil sur les mêmes flops : groupes selon le potentiel (`ehs2`), plus de groupes au flop, stratégie par famille de flops.

### Correction du regroupement après le flop : réglages à mesurer (G13, 30/10/2026)

Réglages nommés (`spinsacademy/postflop/hu_solver.py`, `PRESETS`), tous disponibles pour le solveur de production et pour la mesure exacte :

| Réglage | Groupes au flop | Groupes turn / river | Force | Texture du board |
|---|---|---|---|---|
| `production` (actuel) | 16 | 16 | moyenne (EHS) | non |
| `ehs2` | 16 | 16 | potentiel (EHS², groupes d'effectifs égaux) | non |
| `ehs2_flop32` | 32 | 16 | potentiel | non |
| `ehs2_texture` | 16 × 8 | 16 × 8 | potentiel | oui : stratégie par famille de boards (couleur possible, board pairé, quinte possible) |
| `ehs2_flop32_texture` | 32 × 8 | 16 × 8 | potentiel | oui |

Nouveau réglage `PostflopConfig.flop_buckets` (nombre de groupes au flop, le reste inchangé) ; le calcul des groupes est commun au solveur et à la mesure exacte (`fast.groups`).

Mesure : `tools/solver/exact_flop_check.py --variants all` résout chaque flop exactement une seule fois et y rejoue la stratégie de chaque réglage, sur les 5 flops de G9 (graine 1). Critères de choix (G16) : l'écart moyen avec l'exact, le **transfert entre familles** (dispersion des écarts par famille de mains autour de leur moyenne : c'est le défaut constaté en G9), et l'exploitabilité de la stratégie sur chaque flop. La mesure (environ 4 h 15) se lance sur l'ordinateur du porteur du projet : `docs/solver/PROCEDURE_ORDINATEUR.md`, action O3. Le réglage de production ne change qu'après cette mesure.

La grille peut tourner sur l'arbre v5 (G14) : `python -m spinsacademy.solver.dataset --grid p1 --tree v5 --postflop <réglage>` (ouvertures à 2 BB, tapis direct toujours proposé).

Contrôles après le choix du réglage (G16), à partir de la relecture simulée des coachs (`docs/relecture/solveur_2026-10-30/SYNTHESE.md`) :
- O3 affiche le gain postflop des mains signalées, pour les deux joueurs de l'iso payé : celles qui paient l'iso (K5o, Q8o, K4o : le solveur les couche, les trois coachs les défendent) et celles qui isolent (T9o, 96o, J8o, Q4o, Q5o isolées par le solveur, KJo non isolée : les trois coachs contre) ;
- la banque pilote est refaite avec le réglage retenu (4 configurations, environ 45 minutes), puis `python tools/solver/control_spots.py --after gto_preflop/<version>` met côte à côte, pour les 60 situations de l'échantillon, la décision du solveur avant et après, celle de la référence et l'avis majoritaire des coachs. Les familles qui vont au flop (défense face à l'iso, composition de la range d'iso) doivent bouger ; celles où le solveur l'emporte (pas de limp au BTN à 3 joueurs, tapis du SB à 12 BB) ne doivent pas bouger.

### Choix du réglage de regroupement (G16, 02/11/2026)

Mesure O3 (ordinateur du porteur du projet, `exact_flop_hu25_raise_g13.json`, `exact_flop_hu25_iso_g13.json`), mêmes 5 flops que G9, exact − réglage en mBB ; « transfert » = dispersion des écarts entre familles de mains, le défaut de G9 :

| Réglage | Relance payée : moyenne / transfert / exploitabilité | Iso payé : moyenne / transfert / exploitabilité |
|---|---|---|
| `production` | −41 / 199 / 13,1 % | +31 / 282 / 15,8 % |
| `ehs2` | +10 / 179 / 12,4 % | +55 / 190 / 15,2 % |
| `ehs2_flop32` | +33 / 170 / 12,3 % | +60 / 192 / 15,1 % |
| **`ehs2_texture`** | +12 / **156** / **11,5 %** | +55 / **150** / **14,9 %** |
| `ehs2_flop32_texture` | +13 / 152 / 11,6 % | +55 / 149 / 14,8 % |

**Réglage retenu : `ehs2_texture`** (groupes selon le potentiel, croisés avec la texture du board). Il réduit le transfert de 22 % (relance payée) et 47 % (iso payé) ; 32 groupes au flop n'apportent presque rien de plus pour un calcul plus lourd.

Ce qui reste : les paires (+550 à +680 mBB) et les Kx faibles qui paient l'iso (K5o : 1,03 BB exact contre 0,45 ; K4o : 0,70 contre −0,07) restent sous-évalués, As et broadways surévalués (−50 à −250 mBB). Ce résidu ne vient ni du nombre de groupes ni de la mesure de force : il est commun à tous les réglages.

Pilote heads-up refait avec `ehs2_texture` (`gto_preflop/2026.11.02-s1`, arbre de la référence) :

| Configuration | Perte / plancher de la référence (mBB), production | Idem, `ehs2_texture` |
|---|---|---|
| HU 12 / 12 | 12,3 / 6,9 | **10,4** / 6,9 |
| HU 25 / 25 | **54,4** / 33,5 | 65,7 / 33,5 |

`tools/solver/control_spots.py` sur les situations relevées par les coachs : aucune décision ne change en heads-up 25 BB (K5o, Q8o, K4o se couchent toujours face à l'iso ; T9o et J8o sont toujours isolées). Le résidu des pots relancés porte donc sur des décisions réelles à 25 BB ; à 12 BB, où les pots relancés finissent surtout à tapis, le réglage améliore le calage.

Calage sur la v5 : impossible pour l'instant, les exports v5 de la référence (O2, O4) ne sont pas reçus. À faire à leur réception (`REFERENCE_TREES`).

Grille O5 : `--postflop ehs2_texture --tree v5`. Sous Windows, les sous-jeux postflop démarrent leurs processus par `spawn` (pas de `fork`), corrigé le 02/11/2026 (`solver/pipeline.py`).

### Accélération de la grille (02/11/2026)

Mesuré avant tout calcul de la grille v5, sur les 4 configurations du pilote (arbre de la référence, réglage `production`, 4 cœurs, calculs seuls sur la machine) :

| Configuration | Avant | Après | Exploitabilité (mBB) | Écart de stratégie | Perte / plancher de la référence (mBB) |
|---|---|---|---|---|---|
| HU 12 / 12 | 169 s | **73 s** | 0,08 → 0,07 | 0,9 point | 12,3 → 12,3 / 6,9 |
| HU 25 / 25 | 459 s | **140 s** | 0,45 → 0,54 | 2,8 points | 54,4 → 54,9 / 33,5 |
| 3 joueurs 12 | 930 s | **240 s** | 0,13 → 0,12 | 1,4 point | 41,7 → 42,3 / 34,7 |
| 3 joueurs 25 | 1 025 s | **570 s** | 0,23 → 0,22 | 1,5 point | 100,2 → 101,9 / 114,4 |

Total 2,5 fois plus rapide (2 583 s → 1 023 s) ; la grille O5 passe d'environ 12 h à environ 5 h sur 4 cœurs. Mémoire maximale : 0,2 Go pour le processus principal, 0,25 Go par processus de sous-jeux.

Ce qui a changé (`solver/pipeline.py`, réglages enregistrés dans chaque résultat) :
- à partir du 2e tour, chaque sous-jeu postflop repart des regrets du même sous-jeu au tour précédent, avec 1 000 itérations au lieu de 3 000 ; sa stratégie moyenne repart de zéro ;
- un sous-jeu qui pèse moins de 0,1 % de la masse des sous-jeux (lignes rares à 3 joueurs : 19 sur 32 à 25 BB, 12 sur 18 à 12 BB) reçoit au plus 500 itérations ;
- un sous-jeu dont une range est vide est sauté (sa correction du tour précédent est gardée) ;
- le réservoir de boards est calculé une seule fois par jeu de réglages, puis relu par chaque processus.

Essayé et écarté : reprendre aussi le préflop d'un tour à l'autre. Plus rapide, mais les nœuds peu joués (calls de tapis en fin de ligne à 3 joueurs, le BB qui part à tapis sur une relance) n'apprenaient plus rien et gardaient des fréquences sans valeur (perte de 300 à 750 mBB sur ces nœuds). Le préflop reste résolu depuis zéro à chaque tour.

Les banques calculées avant ces accélérations se recalculent toujours à l'identique (`--check`) : les réglages absents de leur manifeste sont ceux d'avant (`dataset.params_of`).

### G17 : paires et Kx faibles sous-évalués dans les pots relancés, diagnostic (03/11/2026)

Outil : `tools/solver/exact_check.py` (sous-jeu résolu exactement à partir de la turn ou de la river, comparé à la stratégie abstraite rejouée sur les mêmes boards). Pot relancé heads-up 25 BB (le SB relance à 3,5 BB, le BB paie : pot 7 BB, 21,5 BB derrière), ranges de la référence (`v3/hand_18`), réglage `ehs2_texture`. Écart abstrait − exact pour l'appelant (BB, hors de position), en mBB :

| Variante | Rue de départ | Exploitabilité abstraite | Paires | Connecteurs assortis | As dépareillés | Broadways dépareillés |
|---|---|---|---|---|---|---|
| `ehs2_texture` | river (200 boards) | 4,9 % du pot | −124 | −36 | +4 | +49 |
| `ehs2_texture` | turn (40 boards) | 8,7 % | **−387** | −148 | −78 | +96 |
| 48 groupes au lieu de 16 | turn | 8,8 % | −390 | −158 | −83 | +83 |
| 30 000 itérations au lieu de 3 000 | turn | 10,2 % | −356 | −148 | −57 | +57 |
| groupes par joueur contre la range adverse (`strength_vs`) | turn | **6,8 %** | −356 | −131 | −198 | +70 |

Lecture :
- le défaut existe dès la turn (presque pas à la river) ; ce n'est ni la finesse des groupes, ni la convergence, ni la mesure de force (contre une main au hasard ou contre la range adverse) ;
- il touche les mains qui attrapent les bluffs (paires, y compris JJ et 99) et les petites mains assorties de l'appelant ; le relanceur, lui, gagne avec ses As et broadways non appariés. C'est la signature d'une stratégie partagée entre des boards différents : ces mains ont besoin de décisions propres au board (payer ici, se coucher là), qu'un groupe de force commun à tous les boards ne peut pas prendre ;
- les groupes contre la range adverse rendent la stratégie nettement moins exploitable (−22 %) sans corriger les paires : l'option reste disponible (`board_pool(ranges=...)`, `exact_check.py --range-aware`), non branchée dans la grille.

Options pour la suite (décision à prendre) :
1. **Correction apprise du calcul exact** : estimer, sur un échantillon de flops résolus exactement, l'écart exact − abstrait du gain postflop par classe de mains et type de pot (limpé, iso payé, relance payée ; profondeur), et l'ajouter aux gains avant le modèle de réalisation. Coût de calcul : des mesures exactes une fois pour toutes (quelques heures sur l'ordinateur), rien de plus par grille. Limite : la correction dépend un peu des ranges.
2. **Sous-jeux résolus board par board** pour les pots relancés à 16 BB et plus (calcul exact par flop sur un échantillon de flops pondéré) : le plus juste, mais la grille passerait de 5 h à plusieurs jours.
3. **Garder le défaut**, documenté, pour la banque v5 : il pèse sur les décisions qui vont au flop dans les pots relancés à 20-25 BB.

### G17 : correction apprise du calcul exact (option 1 retenue, 03/11/2026)

- Code : `spinsacademy/solver/correction.py` (table par rôle dans le duel — agresseur ou appelant, en position ou non — et par SPR, en fraction du pot ; nulle à SPR 0, interpolée linéairement, constante au-delà du dernier SPR appris), appliquée dans `pipeline._subgame` aux gains des duels qui ont un agresseur préflop, avant `fit_offsets`. Pots limpés inchangés.
- Désactivable : `SolveParams.correction` (option `--correction <nom>` de `spinsacademy.solver.dataset`). Sans correction, l'empreinte des résultats est celle d'avant (la banque `2026.11.02-s2` garde `sf3dc2e6_48fa0906`) ; avec, elle change : les deux grilles se comparent côte à côte.
- Apprentissage : `tools/solver/learn_correction.py`. Sous-jeux tirés de la banque v5 (ranges réelles d'arrivée au flop) : relance payée (`SB-raise2_BB-call`) et iso payé (`SB-call_BB-raise3_SB-call`). Jeu d'apprentissage HU 25, 18, 12 (8 flops par pot) ; jeu de contrôle HU 22, 15, 8 (6 flops par pot, autre graine) : tapis et flops jamais vus à l'apprentissage. Écart par classe rapproché de la moyenne de sa famille selon la masse observée (classes peu jouées).
- Coût mesuré : 1 308 s par flop pour la relance payée à 25 BB, 1 354 s pour l'iso payé (4 cœurs), mémoire 3,2 Go (`--low-memory`). Apprentissage 12 à 15 h : action O6 sur l'ordinateur du porteur ; contrôle dans la session cloud.
- Premier flop (sonde, non retenu) : l'écart d'un flop isolé atteint 1,5 BB sur une famille (Kx de l'appelant sur un flop à roi) : la correction n'a de sens qu'en moyenne sur de nombreux flops, d'où le contrôle hors échantillon avant toute grille.

### G17 : table `g17-v1` et contrôle hors échantillon (04/11/2026)

Apprentissage : O6 (HU 25, 18, 12 ; relance payée et iso payé ; 8 flops chacun, 48 flops, 100 itérations, exploitabilité exacte ≤ 1,1 % du pot). Contrôle : HU 22, 15, 8, 6 flops chacun, autre graine (calcul cloud). Écart quadratique exact − abstrait par classe (mBB, pondéré par la range du joueur), **jeu de contrôle seul**, sans correction → avec :

| Configuration | Pot | Rôle | Sans | Avec (min 0 BB) | Avec `g17-v1` (≥ 12 BB) |
|---|---|---|---|---|---|
| HU 22 | relance payée | OOP appelant | 252 | 144 | 144 |
| HU 22 | relance payée | IP relanceur | 266 | 202 | 202 |
| HU 22 | iso payé | OOP relanceur | 235 | 154 | 154 |
| HU 22 | iso payé | IP appelant | 280 | 251 | 251 |
| HU 15 | relance payée | OOP appelant | 144 | 141 | 141 |
| HU 15 | relance payée | IP relanceur | 195 | 139 | 139 |
| HU 15 | iso payé | OOP relanceur | 405 | 277 | 277 |
| HU 15 | iso payé | IP appelant | 227 | 202 | 202 |
| HU 8 | relance payée | OOP appelant | 400 | 351 | 400 |
| HU 8 | relance payée | IP relanceur | **66** | **107** | 66 |
| HU 8 | iso payé | OOP relanceur | 168 | 142 | 168 |
| HU 8 | iso payé | IP appelant | **81** | **106** | 81 |

- 15 et 22 BB : l'écart baisse dans les 8 cas (−2 % à −43 %). Le reste (140 à 280 mBB) comprend le bruit du contrôle lui-même (6 flops ; un flop isolé s'écarte de plus d'1 BB sur une famille), à comparer aux 47 à 89 mBB sur l'échantillon d'apprentissage.
- 8 BB : deux rôles sur quatre se dégradent, et le plus gros défaut (l'appelant de la relance, As +600 mBB) n'est pas corrigé, faute d'As dans les ranges apprises à ce SPR. D'où `min_stack = 12` dans `g17-v1` : la correction ne s'applique qu'aux duels dont le plus petit tapis de départ atteint 12 BB. Le défaut à 8 BB reste ouvert.
- Choix du lissage (`shrink`, équivalent flops vers la moyenne de la famille) : 4, 8, 20, 60 donnent des écarts de contrôle voisins (15-22 BB : 189 à 210) ; 8 retenu.
- L'exploitabilité postflop abstraite (5,5 à 15,6 % du pot) ne change pas : la correction agit sur les valeurs transmises au préflop, pas sur le jeu postflop. Son effet se mesure en comparant les grilles 2026.11.02-s2 (sans) et 2026.11.04-s3 (avec, O7).
- Essai rapide (HU 15, réglages réduits) : face à l'ouverture du SB, le BB passe de 58 % de fold à 88 % de call avec K5o, dans le sens des coachs.

### G17 : table `g17-v2`, tapis courts (06/11/2026)

Apprentissage ajouté : HU 10 (relance payée et iso payé) et HU 6 (relance payée ; pas d'iso à 6 BB dans la banque), 8 flops chacun, 5 minutes par flop, calculés dans la session cloud (`learn_correction.py --set short`). 8 BB reste en contrôle, jamais appris. Table `g17-v2` : apprentissage `learn` + `short`, appliquée dès 6 BB de tapis effectif (`min_stack = 6`). Contrôle seul, écart quadratique sans correction → `g17-v2` (mBB) :

| Configuration | Pot | Rôle | Sans | `g17-v1` (≥ 12 BB) | `g17-v2` |
|---|---|---|---|---|---|
| HU 8 | relance payée | OOP appelant | 400 | 400 | **322** |
| HU 8 | relance payée | IP relanceur | 66 | 66 | **57** |
| HU 8 | iso payé | OOP relanceur | 168 | 168 | **131** |
| HU 8 | iso payé | IP appelant | 81 | 81 | **71** |
| HU 15, 22 | tous | tous | | | identique à `g17-v1` |

- À 8 BB, les quatre rôles s'améliorent (−9 % à −22 %) au lieu de deux qui se dégradaient avec une correction appliquée partout.
- Reste : l'appelant d'une relance à 8 BB garde des As sous-évalués (As assortis +513, As dépareillés +533 mBB, contre +589 et +623 sans correction) et les broadways dépareillés (+450). Les ranges apprises à 6 et 10 BB ne contiennent pas ces mains comme le fait la range à 8 BB ; un apprentissage supplémentaire à 7 ou 9 BB, ou une mesure à 8 BB elle-même, les corrigerait, au prix d'un contrôle de moins.

### G17 : effet de `g17-v1` sur la stratégie préflop (O7 partielle, 07/11/2026)

43 configurations sur 58 (dossier `sf3dc2e6_eed23e4e`, sans les 15 configurations à 3 joueurs aux tapis inégaux), comparées à `2026.11.02-s2` avec `tools/solver/compare_runs.py`. Exploitabilité ≤ 0,61 mBB et dérive ≤ 0,65 mBB partout : la résolution a convergé.

- Sans effet là où prévu : tous les tapis effectifs sous 12 BB (HU 2 à 10, 3 joueurs 4 à 10), identiques à s2.
- Décalage moyen de stratégie : 10 à 12 points en HU 12 à 22, 24 points en HU 25 ; 6 à 9 points à 3 joueurs 12 à 25.
- Fréquences globales : le SB relance plus (HU 15 : 17 → 25 %, HU 22 : 32 → 44 %, HU 25 : 39 → 65 %) et limpe moins ; le SB paie plus l'iso (fold 50 → 44 % en HU 15).
- Mains suivies, SB limpé face à l'iso (fold, sans → avec) : K5o 99 → 0 (HU 22), 89 → 13 (HU 25), 99 → 46 (HU 18) ; K4o 97 → 44 (HU 15), 96 → 1 (HU 18) : le défaut recule. Mais Q8o 58 → 100 (HU 25) et 78 → 91 (HU 22) : il se creuse. Et, face à l'ouverture à 2 BB, le BB se couche avec K5o 0 → 96 % et K4o 0 → 99 % à HU 25, 0 → 44 % et 0 → 26 % à HU 22 : nouveau défaut.
- Cause identifiée : la correction apprise des Kx de l'appelant hors de position change de signe entre 12 BB (+407 mBB) et 25 BB (−298 mBB), et sur le jeu de contrôle elle dégrade ces mains (HU 15 : Kx assortis −41 → −240 ; HU 22 : +4 → +167). Huit flops par cas ne la fixent pas.

### G17 : table `g17-v3a` (07/11/2026), conclusion

`g17-v3a` : apprentissage `learn` + `short`, lissage fort vers la moyenne de la famille de mains (`--shrink 60`), amplitude divisée par deux (`--scale 0.5`), appliquée dès 6 BB. Essais complets (HU 6, 8, 10, 12, 15, 18, 22, 25 ; 3 joueurs 12 et 25) avec `tools/solver/try_correction.py` ; coachs rejoués avec `tools/solver/score_coaches.py` (verdict du solveur seul : `quiz.correct` accepte de force toute action d'un coach, ce qui donne 100 % par construction).

| Mesure | s2 (sans) | `g17-v1` | `g17-v3a` |
|---|---|---|---|
| Actions de coachs acceptées par le solveur seul | 43 / 56 | 43 / 57 | 43 / 56 |
| Action recommandée acceptée (situations) | 39 / 48 | 39 / 49 | 38 / 48 |
| BB face à l'open à 2 BB, fold de K5o, K4o à HU 22 et 25 | 0 % | 44 / 26 % (HU 22), 96 / 99 % (HU 25) | 0 % |
| SB limpé face à l'iso, fold de Q8o à HU 22 / 25 | 78 / 58 % | 91 / 100 % | **19 / 17 %** |
| SB limpé face à l'iso, fold de K5o, K4o à HU 25 | 89 / 90 % | 13 / 55 % | 87 / 94 % |
| Décalage de stratégie à HU 25 | | 24 points | 11 points |
| Contrôle hors échantillon, 8 / 15 / 22 BB, 12 rôles | | 8 sur 12 mieux | 12 sur 12 mieux (écart quadratique −5 à −24 %) |
| Sous 12 BB (HU 6, 8, 10) | | identique à s2 | décalage de 0,7 à 2,7 points |

- Les actions de coachs refusées changent peu : 5 s'ajoutent (J8o check, K7o isolement et 83s, 98s limpés à HU 25, K2o), 5 se corrigent (KJo, KJs, Q4o, A2s, K2o) ; ce sont presque toutes des « imprécisions » (écart à la limite de la tolérance).
- Aucun nouveau défaut sur les trois points demandés (K5o, K4o face à l'open ; Q8o face à l'iso), et Q8o face à l'iso est corrigé. Mais le défaut d'origine, K5o et K4o couchés face à l'iso à 22-25 BB, n'est pas corrigé, et le nombre de situations des coachs acceptées ne monte pas.
- Décision : l'effet ne justifie pas 5 h de calcul sur l'ordinateur du porteur. Le défaut des pots relancés est une limite connue de la banque `2026.11.02-s2` (fiable de 8 à 16 BB sur les décisions à tapis ou face à un tapis ; moins sûre sur les décisions qui mènent au flop dans un pot relancé). Les tables `g17-v1`, `g17-v2` et `g17-v3a` et les outils restent dans le dépôt, la correction est désactivée par défaut.
- Piste si le sujet revient : sous-jeux exacts par flop pour les pots relancés (option 2 de G17), ou davantage de flops par cas pour l'apprentissage (48 flops ne suffisent pas à fixer le signe des Kx de l'appelant hors de position).

### G18 : champ `reliability` (07/11/2026)

Version `gto_preflop/2026.11.07-s2` : mêmes résultats enregistrés que `2026.11.02-s2` (`sf3dc2e6_48fa0906`, 1 780 spots, 151 205 questions, aucun recalcul ; les spots sont identiques hors deux champs ajoutés), avec par spot :
- `reliability` : `'tapis'` (aucun nœud « flop » atteignable depuis la décision : payer ou pousser un tapis, se coucher face à un tapis…) ou `'flop'` (au moins une action peut mener au flop : l'EV dépend du modèle postflop) ;
- `flop_pot` : `None` pour `'tapis'` ; pour `'flop'`, `'relance'` si un des flops atteignables est celui d'un pot relancé, `'limp'` si tous sont limpés.
Calculés depuis l'arbre (`dataset.reliability_of`). Répartition : 1 151 spots « tapis », 629 « flop » (572 « relance », 57 « limp »).

Le manifeste porte `reliability` (`dataset.RELIABILITY`) : plage fiable des décisions « tapis » 8 à 16 BB ; pour « flop », aucune plage fiable, avec l'écart mesuré par rapport au calcul exact (66 à 400 mBB par main à 8 BB, 144 à 405 à 15 BB, 235 à 280 à 22 BB). La reconstruction du catalogue lit ce champ dans le manifeste : les anciennes versions (sans `reliability`) restent reproductibles à l'identique.

### G19 : calage sur le pilote des exports de référence v5 (07/11/2026)

Exports reçus : `data/hrc/raw/v5/` (HU 12/12 ×5 Monte-Carlo, HU 8/8 ×1 Monte-Carlo). Outil : `tools/solver/calibrate_v5.py` (`--families`, `--repeats`).
- Arbre : empreinte préflop `d0fd39a7` pour les six exports ; mêmes nœuds et mêmes actions que notre arbre v5 (`sf3dc2e6`, ouvertures à 2 BB, iso 3 BB, tapis direct). Correspondance déclarée dans `dataset.REFERENCE_PREFLOP` (l'identifiant de nos arbres, donc les empreintes de résultats, ne change pas). Les 5 répétitions HU 12/12 sont moyennées par l'importeur (`reference_nodes`, 1.5.0) : même base `v5`, même empreinte de réglages.
- HU 12/12, solveur de la banque `2026.11.02-s2` / `2026.11.07-s2` contre la moyenne des 5 répétitions : perte 6,6 mBB par main (plancher de la référence, son propre regret : 5,9), accord des actions dominantes 88 %, TV 14,5 %, aucune action hors de l'arbre de la référence. Contre chaque répétition prise seule : TV 14,6 à 15,8 %, perte 8,7 à 10,6 mBB (plancher 5,4 à 5,8). Les répétitions entre elles s'écartent de 11 à 17 % (TV, un export contre la moyenne des 4 autres) : à 12 BB, le solveur est dans le bruit de la référence.
- Écarts qui dépassent ce bruit (fréquences globales, référence / solveur) : le SB relance à 2 BB plus souvent dans la référence (11,4 % contre 3,8 %) ; le BB isole plus après un limp (16,0 % contre 10,8 %) ; le BB se couche moins face à l'ouverture (21,1 % contre 27,2 %). Même sens qu'au contrôle exact (G17) : les pots relancés sont sous-évalués dans notre modèle.
- Par famille de mains (perte du solveur contre plancher, mBB), seuls écarts nets : BB face à l'ouverture, Kx dépareillés 60 (plancher 10) et connecteurs assortis 33 (25) ; SB face à l'iso, autres dépareillées 16 (6). Partout ailleurs, au plancher.
- HU 8/8 (une seule répétition Monte-Carlo, pas d'export « enumerated ») : perte 8,1 mBB (plancher 6,0), accord 86,5 %, TV 14,3 %. Mêmes écarts de sens : SB relance 1,6 % contre 0 % ; BB isole 21,2 % contre 13,7 % ; BB se couche 24,5 % contre 29,5 % face à l'ouverture.
- Décisions face à un tapis : TV 1 à 2 %, accord 97 à 100 %, perte au niveau du plancher (0,4 à 8 mBB) : les « décisions à tapis » de la banque sont celles de la référence.

### G19 (suite) : export HU 8/8 « enumerated » du 07/11/2026 (`data/hrc/raw/v5/hu_8-8_enum`)

Export exact (moteur enumerated, arbre personnalisé `ui`, mêmes ouvertures et mêmes réglages préflop que les Monte-Carlo ; empreinte préflop `98433a9d`, car elle contient le moteur). 7 nœuds au lieu de 8 : la branche `SB-raise2` (le SB ouvre à 2 BB) n'est pas développée (l'action R2 n'a pas de nœud fils) ; un nœud `SB-fold` s'ajoute. Les EV sont absolues (le fold vaut le tapis restant) : comparées à celles des Monte-Carlo après retrait de l'EV du fold.

Contre l'exact, sur les 6 nœuds communs :

| | TV | accord | perte (plancher de l'exact 8,3 mBB) |
|---|---|---|---|
| solveur (s2) | 20,3 % | 79,8 % | 36,0 mBB |
| Monte-Carlo, 1 répétition | 22,6 % | 77,2 % | 34,2 mBB |
| solveur contre Monte-Carlo (G19) | 14,3 % | 86,5 % | 8,1 mBB |

Le solveur et le Monte-Carlo sont proches l'un de l'autre et s'écartent ensemble de l'exact (SB face à l'iso : fold 47,5 % dans l'exact, 69,9 % solveur, 68,2 % Monte-Carlo ; BB face au tapis du SB après l'iso : fold 37,4 % exact, 4,3 % solveur, 3,3 % Monte-Carlo). Le solveur et le Monte-Carlo ont aussi le même écart d'EV avec l'exact sur des nœuds sans jeu après le flop (call du tapis après iso : +1,8 et +1,9 BB par rapport au fold), ce qu'aucune abstraction postflop ne peut expliquer : arbre différent (branche `SB-raise2` absente) ou convention d'EV différente. **Aucune conclusion sur la justesse du solveur ou de la référence tant que cet export n'est pas recoupé par un cas sans jeu postflop** (HU 4/4 enumerated, où le jeu est un pur calcul d'équité : nos résultats doivent y coïncider presque exactement, sinon c'est une convention).

### G19 (suite 2) : deuxième envoi de référence v5 et contrôle d'équité pur (08/11/2026)

**Rectificatif sur le HU 8/8 enumerated (ci-dessus).** Les EV d'un nœud sans jeu postflop dépendent de la range adverse, qui diffère d'un équilibre à l'autre : l'écart de +1,8 BB sur le call du tapis ne prouvait donc pas une convention d'EV différente. Le contrôle des conventions est le HU 4/4 ci-dessous.

- **HU 4/4 enumerated (jeu d'équité pur au tapis)** : racine du SB (fold, limp, tapis) exact 25,9 / 0,4 / 73,8 %, solveur 26,2 / 0 / 73,8 % (TV 0,4 %) ; décision face au tapis du SB : exact 25,9 / 74,1 %, solveur 26,3 / 73,7 % (TV 0,4 %). EV du call relative au fold : biais 0,3 mBB, écart quadratique 0,8 mBB. **Les conventions d'EV sont les mêmes** (EV de l'export absolue : le fold vaut le tapis restant ; mêmes équités, mêmes blindes). Aux nœuds qui passent par le flop (BB après un limp), l'écart d'EV est de 67 à 98 mBB (limp du SB : −28 mBB de biais), du même ordre que les écarts au calcul exact de G17 (exact et solveur diffèrent par leur modèle postflop) ; le regret de l'export exact lui-même y atteint 435 mBB, ce qui limite ce qu'on peut lui demander.
- **Empreintes acceptées** (`dataset.REFERENCE_PREFLOP`) : `ed8fc281` (SPR 40, HU et 3 joueurs) et `d0fd39a7` (SPR 7). Les répétitions de nœuds et d'actions identiques sont moyennées ensemble, quelle que soit l'empreinte (`reference_nodes`) : à HU 8/8, r1 (SPR 7) et r2 (SPR 40) ont les mêmes 8 nœuds et les mêmes actions, et leur écart (TV 14 à 25 %) est celui de deux répétitions du même réglage (HU 12, 14 à 21 %). Les répétitions HU 12/12 à SPR 7 restent utilisables telles quelles, avec les nôtres : mêmes nœuds et mêmes actions que notre arbre. Les exports enumerated, d'une autre empreinte (le moteur y entre), ne sont jamais moyennés avec le Monte-Carlo.
- **3 joueurs 12/12/12 (5 répétitions)** : 34 nœuds comparés, TV 14,1 %, accord 88,7 %, perte 20,3 mBB (plancher de la référence 26,0), 0,2 % hors référence. Contre une répétition seule : TV 14,4 à 14,8 %, perte 31 à 36 mBB (plancher 24 à 27). Écarts de fréquence à noter, le BB face à l'ouverture du BTN : après un call du SB, il paie 30,2 % chez nous contre 17,1 % dans la référence (et se couche 52,2 % contre 63,3 %) ; quand le SB a couché, il se couche 52,6 % chez nous contre 39,7 % (et paie 26,1 % contre 42,7 %). Détail par nœud : `tools/solver/calibrate_v5.py`.
- **3 joueurs 8/8/8 (3 répétitions)** : 32 nœuds, TV 13,1 %, accord 90,3 %, perte 30,6 mBB (plancher 38,8), 0 % hors référence.
- **HU 20/20 (1 répétition, SPR 40)** : le solveur voit les mêmes 12 nœuds et les mêmes actions (tapis direct à la racine inclus), 0 % hors référence ; TV 17,7 %, accord 83,5 %, perte 23,1 mBB (plancher 15,7).

### G19 (suite 3) : courbe de calage profondeur par profondeur (08/11/2026)

Outil : `tools/solver/calibration_curve.py` (résultat : `data/solver/g17/courbe_calage_s2.json`). Solveur de `2026.11.02-s2` (sans correction) contre les exports de référence v5 à tapis égaux, 27 configurations ; perte et plancher en mBB par main, séparées selon `reliability` (nœuds « tapis » / « flop »). Les exports aux mêmes nœuds et actions sont moyennés ensemble (HU 12 : les 5 à SPR 7 et celui à SPR 40, qui s'écarte de leur moyenne de 9 à 17 % de TV, comme un SPR 7 s'écarte de la moyenne des quatre autres, 11 à 17 %).

| Tapis | Exports | Décisions « tapis » : TV / accord / perte (plancher) | Décisions « flop » : TV / accord / perte (plancher) | Bruit de la référence (TV, perte) |
|---|---|---|---|---|
| HU 2 | 1 | 0,1 / 99,8 / 0,7 (0,0) | 7,8 / 92,8 / 0,9 (0,3) | |
| HU 4 | 1 | 1,4 / 97,9 / 0,2 (0,3) | 9,6 / 91,4 / 19,2 (8,6) | |
| HU 6 | 1 | 0,8 / 99,4 / 0,5 (0,3) | 15,7 / 86,8 / 8,6 (6,1) | |
| HU 8 | 3 | 1,4 / 99,2 / 1,4 (1,1) | 20,0 / 86,3 / 7,3 (8,6) | 11,9 %, 8,8 |
| HU 10 | 1 | 2,0 / 98,6 / 2,4 (2,0) | 22,0 / 80,2 / 12,1 (6,7) | |
| HU 12 | 6 | 2,0 / 98,3 / 2,3 (3,2) | 21,2 / 83,4 / 8,4 (7,4) | 10,1 %, 7,2 |
| HU 14 | 1 | 2,4 / 97,0 / 5,2 (4,5) | 23,9 / 78,2 / 15,3 (8,4) | |
| HU 16 | 4 | 4,1 / 96,1 / 6,1 (7,3) | 23,2 / 83,0 / 12,2 (9,2) | 11,8 %, 11,6 |
| HU 18 | 1 | 3,8 / 97,4 / 9,1 (14,0) | 24,1 / 77,5 / 19,6 (10,1) | |
| HU 20 | 4 | 5,0 / 95,1 / 15,7 (20,1) | 23,5 / 81,4 / 18,4 (15,2) | 12,8 %, 22,8 |
| HU 22 | 1 | 6,0 / 94,8 / 49,5 (33,9) | 27,6 / 72,5 / 28,9 (16,1) | |
| HU 25 | 4 | 4,9 / 97,1 / 42,8 (50,9) | 26,4 / 75,1 / 24,7 (18,8) | 14,1 %, 39,6 |
| 3 j. 8 | 4 | 5,2 / 97,6 / 7,8 (29,8) | 18,2 / 86,4 / 45,0 (47,1) | 10,8 %, 68,5 |
| 3 j. 12 | 6 | 4,6 / 97,4 / 10,4 (27,7) | 21,3 / 81,6 / 27,8 (25,1) | 9,9 %, 49,0 |
| 3 j. 16 | 5 | 5,8 / 96,8 / 16,9 (61,4) | 22,3 / 82,6 / 31,3 (35,6) | 11,5 %, 93,4 |
| 3 j. 25 | 4 | 8,1 / 95,5 / 83,9 (226,7) | 21,9 / 82,6 / 55,8 (59,9) | 13,6 %, 256,9 |

Lecture :
- Décisions « tapis » : TV 0,1 à 2 % jusqu'à HU 12, 4 à 6 % de HU 16 à 25, accord 93 à 100 %, perte au niveau du plancher partout. Plage fiable confirmée : HU jusqu'à 16 BB (perte ≤ 10 mBB), 3 joueurs jusqu'à 16 BB ; au-delà, la perte monte avec le bruit de la référence lui-même (plancher de 34 à 44 mBB à HU 22-25, 150 à 190 à 3 joueurs 22-25) et on ne peut plus la distinguer du plancher.
- Décisions « flop » : TV de 8 % (HU 2) à 28 % (HU 25), accord de 93 à 72 % ; perte au-dessus du plancher de 0 à 1 mBB jusqu'à HU 8, de 1 à 5 mBB à HU 10-12, de 7 à 13 mBB à HU 14-25. L'écart avec la référence croît avec la profondeur, et il est du sens du défaut des pots relancés.
- Bruit d'un export isolé contre la moyenne des autres : HU 8 et 12, perte de 7 à 9 mBB ; HU 20, 33 mBB ; 3 joueurs, 49 à 69 mBB. C'est le seuil à retenir pour les configurations à une seule répétition (et non 100 mBB) : HU jusqu'à 18 BB, plancher + 15 mBB ; HU 20 à 25, plancher + 35 ; 3 joueurs, plancher + 70.

### G19 (suite 4) : mesure du défaut des pots relancés avec 4 répétitions, ancrages exacts, 3 joueurs profonds (09/11/2026)

Exports reçus : HU 16, 20, 25 à 4 répétitions chacun (SPR 40), 3 joueurs 16 (5) et 25 (4), `hu_6-6_enum` et `3w_4-4-4_enum` (exacts, mode `ui`). Le HU 8/8 enumerated est identique à `hu_8-8_enum` (7 nœuds : ce moteur ne développe pas la branche `SB-raise2`). `3w_25-25-25_r3` omet les 3 nœuds du tapis direct du BTN (mêmes réglages) : `reference_nodes` moyenne désormais chaque nœud sur les exports qui l'ont, à condition que leurs actions concordent.

**Défaut G17 avec 4 répétitions (solveur de s2, sans correction), décisions « flop » :**

| Tapis | Perte moins plancher | TV solveur / bruit | BB se couche face à l'ouverture (référence, écart type entre exports → solveur) | BB se couche face à l'iso | SB relance à 2 BB |
|---|---|---|---|---|---|
| HU 16 | +3,0 mBB | 23,2 % / 11,8 % | 19,2 % (0,3) → 27,4 % | 46,2 → 50,8 % | 27,3 → 17,9 % |
| HU 20 | +3,2 mBB | 23,5 % / 12,8 % | 19,0 % (0,8) → 28,1 % | 44,5 → 48,1 % | 31,8 → 27,9 % |
| HU 25 | +5,9 mBB | 26,4 % / 14,1 % | 17,2 % (0,4) → 26,4 % | 42,5 → 48,2 % | 36,8 → 39,4 % |

- Le défaut est réel et systématique : le BB se couche 8 à 9 points de plus que la référence face à l'ouverture, aux trois profondeurs, soit 10 à 25 écarts types entre exports ; face à l'iso, 4 à 6 points de plus. La TV des décisions « flop » est le double du bruit d'un export.
- Il coûte peu en EV : 3 à 6 mBB par main au-dessus du plancher, contre un bruit d'un export de 12 à 40 mBB. Les mains concernées sont marginales. À HU 25, par famille (perte, plancher) : As assortis face à l'ouverture 84 (31), connecteurs assortis face à l'iso 41 (14), autres dépareillées face à l'ouverture 21 (9) ; tout le reste au plancher.
- Les décisions « tapis » restent au plancher (perte de 6 à 43 mBB, plancher de 7 à 51).

**Ancrages exacts (`tools/solver/compare_exact.py`) :**
- HU 6/6 : décisions « tapis » (2 nœuds) TV 1,3 %, accord 99 %, perte 0,7 mBB (plancher 0,4) ; décisions « flop » (2 nœuds) TV 22 % : le SB limpe 12,8 % chez nous contre 0,6 % dans l'exact, le BB après un limp pousse 49,6 % contre 54,1 %. Branche `SB-raise2` non développée dans l'exact.
- 3 joueurs 4/4/4 : décisions « tapis » (5 nœuds) TV 2,0 %, accord 98 %, perte 0,4 mBB (plancher 0,0) ; racine du BTN et du SB (fold, tapis) à moins de 0,5 % ; décisions « flop » TV 8,9 % (le BB après deux limps : push 48,9 % contre 56,5 %). La branche du BTN qui limpe (10 nœuds) n'est pas développée dans l'exact.
- Avec HU 4/4 : les décisions sans flop coïncident avec l'exact aux profondeurs 4 et 6 (TV 0,4 à 2 %) et à 3 joueurs 4 ; les écarts apparaissent aux nœuds qui passent par le flop, du même ordre que le calcul exact au flop de G17.

**3 joueurs profonds :** 16/16/16 (5 répétitions) : TV 14,8 %, accord 89,0 %, perte 24,7 mBB (plancher 47,3), 0,2 % hors référence ; 25/25/25 (4) : TV 15,6 %, accord 88,5 %, perte 68,5 mBB (plancher 135,6), 0,3 % hors. Dans le bruit (bruit d'un export : 93 mBB à 16 BB, 257 mBB à 25 BB) : un calage à 3 joueurs ne peut pas distinguer le solveur de la référence à ces profondeurs.
