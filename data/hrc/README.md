# Exports HRC de référence

**Ces fichiers ne doivent jamais être embarqués dans l'application** (frontend, API publique, bundle, datasets publiés). Ils servent uniquement de source pour générer, valider et documenter les datasets. Ils ont été obtenus légalement par le propriétaire du projet.

## Contenu

Ce dossier contient 44 mains exportées depuis HRC, toutes préflop. Chaque main a un fichier `settings.json` (configuration) et un dossier `nodes/*.json` (un fichier par nœud, avec la stratégie et les EV par classe de main).

Configuration commune :
- modèle : chip EV, sans rake ;
- blinds 0,5 / 1, ante à 0 ;
- moteur HRC Monte-Carlo ;
- tailles : open du BTN à 2,3 BB, open du SB à 3,5 BB, iso-raise du BB à 3 BB, puis all-in.

Seule différence d'arbre entre les dossiers : `min_raise_3way` interdit le limp du BTN.

La colonne « Clé `hrcdata` » donne la correspondance avec les scripts de `legacy/conversation/` (`hrcdata.load(kind, hand)`).

| Dossier | Main | Table | Stacks (BB) | Limp BTN autorisé | Nœuds | Empreinte arbre | Clé `hrcdata` |
|---|---|---|---|---|---|---|---|
| `complement/hand_1` | 1 | 3 joueurs | 4 / 4 / 4 | oui | 8 | `58407ad7` | `3wc/1` |
| `complement/hand_2` | 2 | 3 joueurs | 6 / 6 / 6 | oui | 10 | `58407ad7` | `3wc/2` |
| `complement/hand_3` | 3 | 3 joueurs | 15 / 15 / 15 | oui | 11 | `58407ad7` | `3wc/3` |
| `complement/hand_4` | 4 | heads-up | 15 / 15 | — | 4 | `58407ad7` | `huc/4` |
| `complement2/hand_1` | 1 | 3 joueurs | 4 / 8 / 8 | oui | 8 | `58407ad7` | `c2/1` |
| `complement2/hand_2` | 2 | 3 joueurs | 8 / 4 / 8 | oui | 10 | `58407ad7` | `c2/2` |
| `complement2/hand_3` | 3 | 3 joueurs | 8 / 8 / 4 | oui | 10 | `58407ad7` | `c2/3` |
| `complement2/hand_4` | 4 | 3 joueurs | 8 / 4 / 4 | oui | 8 | `58407ad7` | `c2/4` |
| `complement2/hand_5` | 5 | 3 joueurs | 4 / 8 / 4 | oui | 8 | `58407ad7` | `c2/5` |
| `complement2/hand_6` | 6 | 3 joueurs | 4 / 4 / 8 | oui | 8 | `58407ad7` | `c2/6` |
| `complement2/hand_7` | 7 | 3 joueurs | 12 / 12 / 12 | oui | 11 | `58407ad7` | `c2/7` |
| `complement2/hand_8` | 8 | heads-up | 4 / 8 | — | 3 | `58407ad7` | `c2/8` |
| `complement2/hand_9` | 9 | heads-up | 8 / 4 | — | 3 | `58407ad7` | `c2/9` |
| `complement2/hand_10` | 10 | heads-up | 4 / 8 | — | 3 | `58407ad7` | `c2/10` |
| `complement2/hand_11` | 11 | heads-up | 15 / 15 | — | 4 | `58407ad7` | `c2/11` |
| `complement2/hand_12` | 12 | heads-up | 12 / 12 | — | 4 | `58407ad7` | `c2/12` |
| `complement2/hand_13` | 13 | heads-up | 20 / 20 | — | 3 | `58407ad7` | `c2/13` |
| `complement2/hand_14` | 14 | 3 joueurs | 20 / 20 / 20 | oui | 8 | `58407ad7` | `c2/14` |
| `complement2/hand_15` | 15 | 3 joueurs | 14 / 14 / 14 | oui | 11 | `58407ad7` | `c2/15` |
| `complement2/hand_16` | 16 | 3 joueurs | 14 / 18 / 18 | oui | 10 | `58407ad7` | `c2/16` |
| `complement2/hand_17` | 17 | 3 joueurs | 18 / 12 / 18 | oui | 11 | `58407ad7` | `c2/17` |
| `complement2/hand_18` | 18 | 3 joueurs | 18 / 18 / 12 | oui | 11 | `58407ad7` | `c2/18` |
| `complement2/hand_19` | 19 | 3 joueurs | 18 / 12 / 12 | oui | 11 | `58407ad7` | `c2/19` |
| `complement2/hand_20` | 20 | 3 joueurs | 12 / 18 / 12 | oui | 11 | `58407ad7` | `c2/20` |
| `complement2/hand_21` | 21 | 3 joueurs | 12 / 12 / 18 | oui | 11 | `58407ad7` | `c2/21` |
| `min_raise_3way/hand_4` | 4 | 3 joueurs | 25 / 25 / 25 | non | 6 | `c22b0ad6` | `3w/4` |
| `min_raise_3way/hand_5` | 5 | 3 joueurs | 18 / 18 / 18 | non | 15 | `c22b0ad6` | `3w/5` |
| `min_raise_3way/hand_6` | 6 | 3 joueurs | 12 / 12 / 12 | non | 9 | `c22b0ad6` | `3w/6` |
| `min_raise_3way/hand_7` | 7 | 3 joueurs | 10 / 10 / 10 | non | 9 | `c22b0ad6` | `3w/7` |
| `min_raise_3way/hand_8` | 8 | 3 joueurs | 8 / 8 / 8 | non | 8 | `c22b0ad6` | `3w/8` |
| `min_raise_3way/hand_9` | 9 | 3 joueurs | 12 / 21 / 21 | non | 8 | `c22b0ad6` | `3w/9` |
| `min_raise_3way/hand_10` | 10 | 3 joueurs | 21 / 12 / 21 | non | 7 | `c22b0ad6` | `3w/10` |
| `min_raise_3way/hand_11` | 11 | 3 joueurs | 21 / 21 / 12 | non | 7 | `c22b0ad6` | `3w/11` |
| `min_raise_3way/hand_12` | 12 | 3 joueurs | 8 / 14 / 14 | non | 9 | `c22b0ad6` | `3w/12` |
| `min_raise_3way/hand_13` | 13 | 3 joueurs | 14 / 8 / 14 | non | 8 | `c22b0ad6` | `3w/13` |
| `min_raise_3way/hand_14` | 14 | 3 joueurs | 14 / 14 / 8 | non | 8 | `c22b0ad6` | `3w/14` |
| `min_raise_hu/hand_15` | 15 | heads-up | 25 / 25 | — | 3 | `58407ad7` | `hu/15` |
| `min_raise_hu/hand_16` | 16 | heads-up | 18 / 18 | — | 5 | `58407ad7` | `hu/16` |
| `min_raise_hu/hand_17` | 17 | heads-up | 12 / 12 | — | 4 | `58407ad7` | `hu/17` |
| `min_raise_hu/hand_18` | 18 | heads-up | 10 / 10 | — | 7 | `58407ad7` | `hu/18` |
| `min_raise_hu/hand_19` | 19 | heads-up | 8 / 8 | — | 3 | `58407ad7` | `hu/19` |
| `min_raise_hu/hand_20` | 20 | heads-up | 6 / 6 | — | 3 | `58407ad7` | `hu/20` |
| `min_raise_hu/hand_21` | 21 | heads-up | 4 / 4 | — | 3 | `58407ad7` | `hu/21` |
| `min_raise_hu/hand_22` | 22 | heads-up | 2 / 2 | — | 3 | `58407ad7` | `hu/22` |
