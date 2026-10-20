# Audit des coachs sur le moteur exploitant « field » et corrections v4.2 (20/10/2026)

## Ce qui a été reçu (`docs/audit/field_2026-10-20/`)

| Fichier | Contenu |
|---|---|
| `audit_coachs_v4_1.csv` | 258 questions de la banque v4.1 relues par Lucho, PA et Lucky : 240 ✅, 10 ⚠️, 8 ❌ ; 87 remarques de pédagogie |
| `audit_quiz_exploit_v3.csv` | 297 questions de la banque v3 : 256 ✅, 28 ⚠️, 13 ❌ (corrections déjà reprises par la v4 : option limp, pas de fold ni de limp exploitant à 4 BB, read d'au moins 40 occasions à 6 BB) |
| moteur v4.1 (archive) | porté dans `tools/field/` (code du moteur, générateur, vérification, grille des coachs) ; les exports HRC sont lus dans `data/hrc/raw` et ne sont jamais embarqués dans l'application |

## Constats de l'audit v4.1 et corrections

| # | Constat (coachs) | Cause dans le moteur | Correction v4.2 |
|---|---|---|---|
| 1 | 8 ❌ : heads-up à 8 BB contre un rec inconnu, le quiz demandait « Pousser » (J2s, 94s, 54o, T2s, 65o, 96o, T5s, J8o) ; Lucho et PA : « limper 100 %, même trash » | l'EV du limp était l'EV HRC contre un BB qui joue la théorie, prise comme borne basse : contre un rec qui iso peu, le limp était sous-évalué | `exploit_engine.limp_ev` : l'EV du limp est décomposée (check du BB / iso du BB) ; l'iso est évaluée par les équités (fold ou tapis payé), la valeur du check est calée sur l'EV HRC ; contre le vilain, la fréquence et la range d'iso changent. Contre un BB théorique, on retrouve l'EV HRC exactement. Exemple à 8 BB : J2s pousser +0,18 BB, limper +0,20 BB (HRC : +0,01). Quand l'estimation fait baisser le limp (mains fortes), un autre choix doit battre aussi l'EV HRC du limp |
| 2 | 8 ⚠️ (Lucky ❌) : la réponse « Rec passif ou reg (proche de la théorie) » réunit les deux joueurs dont la distinction rapporte le plus | les deux profils étaient indiscernables sur 40 à 80 occasions | deux réponses distinctes (« Rec passif », « Reg ») ; question gardée seulement si les fréquences observées séparent la bonne pastille (écart de χ² d'au moins 4) ; échantillon de 150 occasions ajouté quand 40 et 80 ne suffisent pas |
| 3 | 29 remarques « pas un piège : vilain à 0 à 5 points du GTO » | un piège était tiré même quand le vilain jouait presque la théorie | un piège (R9) exige un écart affiché d'au moins 5 points |
| 4 | 33 remarques « trivial : marge 11 à 34 × bruit » | aucune borne haute sur la marge d'un piège | marge d'un piège entre 3 et 10 × le bruit du moteur |
| 5 | « mix GTO : HRC joue déjà fold à 35 %… » (Lucky : déviation faible) | une main que HRC joue déjà en mixte devenait une « adaptation » | adaptation et « inconnu » exclues quand HRC joue déjà la réponse 30 % du temps ou plus |
| 6 | 2 ⚠️ : folder un call à 6 BB contre un nit (PA, Lucky : field proche de la théorie vers 5-6 BB) | read de 40 occasions accepté | à 6 BB et moins, payer moins (R2) exige 80 occasions |
| 7 | BvB à 3 joueurs : PA et Lucky « on limpe trop, l'agression prime » | — (la décomposition du limp augmentait aussi le limp en BvB) | estimation du limp réservée au heads-up ; en BvB l'EV HRC du limp reste une borne basse, dite comme telle dans la correction |
| 8 | BTN à 10 BB : PA « min-raise / fold du pack KT » | le min-raise est hors du domaine du moteur | pièges « fold au BTN » retirés à 10 BB et plus |
| 9 | règle R0 « pousse large » contredit le limp en heads-up | texte | « Vole plus (limp en heads-up, tapis en BvB et au BTN), paie plus serré (sauf à 4 BB ou moins) » |

## Résultat

Banque v4.2 (`exploit_field/2026.10.20-1`, graine 11) : 380 questions (258 en v4.1).

| Type | Nombre | Type | Nombre |
|---|---|---|---|
| adaptation | 136 | identification (« quel est son défaut ? ») | 23 |
| piège | 119 | quelle pastille ? | 19 |
| vilain inconnu | 69 | petit échantillon | 14 |

- Heads-up 185, 3 joueurs 195 ; 4 BB 49, 6 BB 125, 8 BB 128, 10 BB 35, 12 BB 43.
- Bonnes réponses : limp 107 (97 en heads-up, 10 en BvB contre la station), fold 103, tapis 80, payer 48.
- Contre un rec inconnu au SB en heads-up, la réponse est le limp dans plus de 80 % des questions.
- Vérification (`tools/field/verify_quiz.py`) : 0 échec ; recalcul indépendant 338 / 338 identiques ; simulation de parties réelles conforme.
- Grille des coachs (`tools/field/audit_quiz.py`, doctrine codée des trois skills) : 367 ✅, 13 ⚠️, 0 ❌ (`field_2026-10-20/grille_coachs_v4_2.csv`). Les 13 ⚠️ : 10 limps en BvB contre une calling station (« limp défendable, 2 coachs sur 3 ») et 3 folds à 6 BB contre un nit avec 80 occasions. Aucune des 18 questions contestées de la v4.1 n'est restée en l'état ; les 15 questions « pastille » de même identifiant ont désormais les cinq réponses séparées.
- La grille code la doctrine des coachs : elle ne remplace pas leur relecture de la banque v4.2.

## Intégration dans l'application

- Nouveau mode **Field** (accueil : GTO · Exploitant · Field), jeu de données `exploit_field`, contrôlé et publié comme les autres (`spinsacademy/catalog.py` : complétude, bonne réponse la plus rentable, aucun montant en mBB ni profil interne affiché, reconstruction depuis les exports HRC).
- Le joueur voit les statistiques observées du vilain (k sur n, observé contre théorie) ou « aucune information » (rec passif par défaut), jamais le profil interne.
- Questions de lecture (« quel est son défaut ? », « quelle pastille ? ») sans table ni cartes ; filtre « Lecture du vilain ».
- Correction : action contre ce vilain et gain par rapport à la théorie (en BB), action théorique HRC, EV de chaque option par rapport au fold, règle à retenir ; « Pourquoi ? » : nature de l'EV du limp, marge de précision du moteur, rappel que les profils sont des hypothèses de coachs.
- Notation : mêmes seuils que l'application (0,02 / 0,06 BB) ; une option dans la marge de précision du moteur reste au pire une imprécision.
- Séries de 5 : rotation heads-up / 3 joueurs, au plus 2 pièges ou échantillons et 1 question de lecture, jamais deux fois la même main. Pas de série adaptée en mode Field ; révision espacée, progression et signalements communs.
- Le mode Exploitant (profils fictifs, calcul exact) est conservé tel quel.

## Limites

- Les facteurs des profils (rec passif par défaut selon la profondeur, station, dégène, nit, reg) sont des hypothèses de coachs, non mesurées : à recaler avec `tools/field/calibrate_profiles.py` sur de vraies mains.
- L'estimation du limp en heads-up suppose que le SB, face à l'iso, se couche ou part à tapis, et corrige la valeur du check par l'équité contre la nouvelle range de check (pot de 2 BB) : c'est un modèle, pas un calcul HRC verrouillé. Les exports HRC « SB limp, BB iso, décision du SB » le remplaceraient.
- Domaine : stacks égaux de 4 à 12 BB, tout ou rien et limp du SB ; min-raise et iso non all-in exclus.
- Composition : la calling station pèse 31 % des questions (15 % du field), le rec passif 23 % (55 % du field) : le rec passif n'a que des questions « inconnu » et des pièges. Plafond actuel : 2 × la part du profil.
