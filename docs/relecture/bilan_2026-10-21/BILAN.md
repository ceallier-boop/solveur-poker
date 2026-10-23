# Bilan des quizz (21/10/2026)

Outil : `tools/audit/bilan_quiz.py`. Les fichiers chiffrés sont dans ce dossier.

## 1. Les deux banques

| Mode | Version | Situations | Questions |
|---|---|---|---|
| GTO | `gto_preflop/2026.10.13-3` | 2528 spots, 2 à 25 BB (4 à 25 BB à 3 joueurs), dont 1 sur 3 en tapis inégaux | 145 975 couples spot × main proposables |
| Exploitant | `exploit_field/2026.10.21-2` | 9 situations, 4 à 12 BB, tapis égaux | 4400 questions fixes |

**Mode GTO, par famille de décision :**

| Table | Famille | Questions | Part servie | Part réelle des décisions |
|---|---|---|---|---|
| 3 joueurs | premier à parler (BTN, SB après fold du BTN) | 10 098 | 19 % | 55 % |
| 3 joueurs | face à un tapis | 66 948 | 30 % | 25 % |
| 3 joueurs | face à une relance | 35 749 | 30 % | 12 % |
| 3 joueurs | face à un limp | 19 497 | 20 % | 8 % |
| Heads-up | premier à parler (SB) | 2575 | 17 % | 48 % |
| Heads-up | face à un tapis | 6105 | 34 % | 21 % |
| Heads-up | face à une relance | 4157 | 33 % | 9 % |
| Heads-up | face à un limp (BB) | 846 | 17 % | 21 % |

« Part servie » : part des questions tirées sur 3000 séries simulées, pour chaque table. « Part réelle » : part des décisions prises dans cette famille sur une main jouée, d'après les stratégies de référence, en moyenne sur les quatre tranches de tapis.

**Mode exploitant, par situation :**

| Situation | Tapis couverts | Questions | Part servie |
|---|---|---|---|
| BB face au limp du SB (3 joueurs) | 6, 8 (2 à 10 BB, 0 à 12 BB) | 633 | 29 % |
| BB face au limp du SB (heads-up) | 6, 8 (2 à 10 BB, 0 à 12 BB) | 789 | 22 % |
| SB premier à parler (heads-up) | 4 à 12, surtout 6-8 | 555 | 8 % |
| SB après fold du BTN (3 joueurs) | 4 à 12, surtout 8 | 395 | 9 % |
| BTN premier à parler (3 joueurs) | 4 à 12, surtout 8 | 463 | 8 % |
| BB face au tapis du SB (3 joueurs) | 4 à 12 | 470 | 9 % |
| BB face au tapis du SB (heads-up) | 4 à 12 | 418 | 4 % |
| BB face au tapis du BTN, SB fold | 4 à 12 | 289 | 5 % |
| SB face au tapis du BTN | 4 à 12 | 335 | 5 % |
| Lecture du vilain (heads-up) | 4 à 12 | 53 | 1 % |

## 2. Constats du bilan (avant l'audit des coachs)

1. **Le tirage GTO ne suit pas la fréquence réelle.** Il fait tourner les familles et les positions à parts égales. Résultat : 42 % des questions servies portent sur des situations qui pèsent moins de 1 % des décisions de leur tranche de tapis (pots relancés puis relancés, sur-calls, squeezes). À l'inverse, les décisions les plus fréquentes sont sous-servies :

   | Situation | Part réelle | Part servie |
   |---|---|---|
   | BTN premier à parler (3 joueurs) | 22 % | 7 % |
   | SB premier à parler (heads-up) | 17 % | 6 % |
   | SB après fold du BTN | 14 % | 6 % |
   | BB face au tapis du SB, BTN fold | 4,8 % | 0,5 % |
   | SB face au tapis du BTN | 4,7 % | 0,4 % |

   (Les parts réelles supposent 35 % de mains en heads-up.)
2. **Le min-raise est presque absent.** Le BTN ouvre à 2,3 BB dans 43 spots, et à 2 BB dans 6 spots seulement (12-20 BB). En heads-up, le SB ouvre à 3,5 BB dans 13 spots et à 2 BB dans 5. Or le min-raise est l'ouverture la plus courante du field Expresso.
3. **Le mode exploitant ne couvre que 4 à 12 BB et la moitié des situations.**
   - Rien au-dessus de 12 BB, alors que les tranches 13-25 BB représentent une grande part des mains.
   - Aucune question sur le BTN qui limpe ou min-raise, ni sur le SB face au limp du BTN.
   - Rien sur le BB face au min-raise, ni sur les pots limpés à 3.
   - Pas d'iso non all-in, pas de tapis inégaux.
   - Le BB face au limp du SB n'a presque aucune question à 10 et 12 BB : la référence y isole à 3 BB, option que le moteur ne propose pas.
   - Même trou pour « premier à parler » à 10-12 BB : 29 questions en heads-up, 28 pour le SB et 77 pour le BTN à 3 joueurs. La référence y min-raise, ce que le moteur ne sait pas exploiter.
4. **Le mode exploitant sur-sert le limp à 6-8 BB.** Les deux situations « BB face au limp du SB » font 51 % des questions servies, dont 20 % pour la seule case 3 joueurs à 8 BB. Le tirage pondère par la part du profil dans le field ; or les questions de rec passif se concentrent sur ces cases.
5. **Le postflop n'est jamais une question.** C'est seulement une aide dans la correction, alors que les pots limpés (heads-up, BvB) et min-relancés sont fréquents dès 10 BB.

## 3. Audit des coachs (terminé)

Voir `audit_lucho.md`, `audit_pa.md`, `audit_lucky.md` et leurs grilles `audit_*.csv`. La consolidation est dans `SYNTHESE_AUDIT.md`.
