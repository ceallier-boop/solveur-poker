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
