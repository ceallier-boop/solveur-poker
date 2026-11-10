# Import de l'historique Winamax dans le navigateur (MM2)

Module : `spinsacademy/web/winamax.js`, portage de `tools/field/winamax_counts.py` (même version, mêmes situations, mêmes tapis, mêmes règles). JavaScript sans dépendance, chargé par `<script src="/static/winamax.js">`, qui expose `window.Winamax`. Le module n'écrit rien : ni stockage, ni réseau.

## API

```js
Winamax.VERSION                 // '1.0.1', celle de winamax_counts.py
Winamax.GRID                    // tapis du moteur : [2, 4, 6, 8, 10, 12, 15, 18, 20, 25]
Winamax.analyze(files, onProgress) -> Promise<résultat>
Winamax.toCsv(résultat)         -> {'comptages.csv': texte, 'volume.csv': texte}
```

- `files` : `[{name, text}]`, le texte d'un fichier `.txt` d'historique. Les autres noms et les résumés de tournoi (`…summary…`) sont ignorés et comptés dans `skipped_files`. Un BOM en tête est retiré.
- `analyze` rend la main au navigateur entre deux fichiers, et toutes les 2000 mains dans un gros fichier. `onProgress({done, total, hands})` est appelé après chaque fichier.
- La Promise n'est rejetée que si un pseudo se retrouverait dans le résultat : c'est une vérification interne, qui ne doit pas se déclencher.

Résultat :

| Champ | Contenu |
|---|---|
| `version`, `files`, `skipped_files` | version du lecteur, fichiers lus, fichiers ignorés |
| `hands`, `unreadable`, `ignored` | mains Expresso lues ; mains illisibles (structure, montants, héros absent) ; autres formats et parties fictives |
| `by_table` | `{hu, '3w'}` : mains lues par table |
| `months` | `['AAAA-MM', 'AAAA-MM']` (première et dernière), ou `null` |
| `counts` | `[{group, kind, decision, action, stack, n, k}]` : décisions des adversaires, comme `comptages.csv` |
| `volume` | `[{parameter, stack, n, status}]` : comme `volume.csv` (fiable, indicatif, insuffisant) |
| `hero_decisions` | une entrée par action du héros avant le flop, voir ci-dessous |

`hero_decisions` : `{table, position, stack_bb, history, decision, hero_hand, action, to_bb, month}`
- `table` : `hu` ou `3w` ; `position` : `BTN`, `SB` ou `BB` ; `stack_bb` : tapis effectif en BB, à 2 décimales ;
- `history` : actions précédentes dans le vocabulaire des situations (`BTN:fold SB:limp`, vide pour le premier à parler) ;
- `decision` : libellé de la situation (par exemple « BB face au limp du SB (BTN fold) »), ou `null` hors des 21 situations ;
- `hero_hand` : `AKs`, `77`, `92o` (`null` si les cartes sont illisibles) ; `action` : `fold`, `check`, `limp`, `paie`, `relance` ou `tapis` ; `to_bb` : montant total de la relance en BB, sinon `null` ;
- `month` : `AAAA-MM`.

## Vie privée

Les pseudos ne servent qu'en mémoire, pour séparer le héros (le joueur de « Dealt to ») de ses adversaires. Le résultat ne contient aucun pseudo, aucun numéro de main, de table ou de tournoi, et aucune date plus fine que le mois. Avant de rendre le résultat, une vérification cherche chaque pseudo et refuse s'il en trouve un. Sont exemptés les pseudos qui sont des mots des libellés (« fold ») ou des noms de mains (« AKs »), et les pseudos faits seulement de chiffres. `hero_decisions` reste en mémoire : c'est à l'écran « Mes mains » de décider de ce qu'il garde.

## Limites

- Format des mains : celui des historiques Winamax tel qu'on le connaît. Les 569 mains du porteur ont été lues sans main illisible par la version Python, mais les tests du module tournent sur des mains d'exemple (`tests/data/winamax`, pseudos inventés).
- Préflop seulement. Expresso et Expresso Nitro en argent réel ; pas d'option « tous formats » dans le navigateur.
- Les comptages des adversaires excluent un joueur dès qu'il a été héros dans une main déjà lue (même règle que la version Python). L'ordre des fichiers ne compte que pour un joueur qui a plusieurs comptes.
- `adversaires.csv` (répartition des adversaires par profil) reste dans l'outil Python tant que le volume est faible.

## Tests

`tests/test_winamax_js.py` lance le module sous Node (`tests/js/winamax_run.cjs`) sur `tests/data/winamax` (mains produites par `generer.py`). Il vérifie :
- des CSV identiques octet pour octet à ceux de la version Python ;
- les 21 situations couvertes ;
- un fichier illisible et un tournoi autre que l'Expresso ;
- des décisions du héros sans pseudo ;
- la vérification de vie privée.

Le test est sauté si Node est absent. Toute modification de `winamax_counts.py` doit être reportée dans `winamax.js` : le test de parité le signale.
