# Neuvième test joueurs (29/10/2026) : programme de travail, étapes 1 à 5

Version testée : `f172b5e`. Accueil en programme : séance du jour, recommandations, objectifs de la semaine, défis, niveaux et écrans de premier lancement. Base de test séparée, banques publiées, aucun signalement envoyé. Le test de l'étape 1 (huitième test) avait été interrompu ; c'est le premier test complet du programme. Les six testeurs ont joué en même temps depuis la même adresse : les refus « Trop de requêtes » (429) viennent de là, pas d'un défaut de l'application.

## 1. Notes

| Joueur | Test 7 | Application | Accueil | Défis | Objectifs | Niveaux |
|---|---|---|---|---|---|---|
| Mamadou | 4 | 4 | 3 | 4 | 4 | 3 |
| Léa | 4 | 4 | 3 | 4 | 4 | 2 |
| Kevin | 4 | 4 | 4 | 3 | 4 | 4,5 |
| Nadia | 4 | 4 | 3 | 2,5 | 3 | 4 |
| Jean-Pierre | 4 | 4 | 3 | 3 | 3,5 | 3 |
| Sofiane | 4 | 4 | 3 | 3,5 | 3 | 3,5 |
| **Moyenne** | 4,0 | **4,0** | **3,2** | **3,3** | **3,6** | **3,3** |

Sofiane paierait toujours 10 € par mois, et 15 € avec un défi du jour comparé aux autres joueurs, des défis de la semaine plus durs et des niveaux qui filtrent vraiment la profondeur.

## 2. Ce qui plaît
- **Le bouton de la séance** : on comprend quoi faire en environ 5 s (les six). La séance va au bout, l'accueil se met à jour, et « Séance faite. Reviens demain » donne la routine que Mamadou cherchait.
- **Défi du jour** : deux joueurs reçoivent bien les mêmes 5 mains, avec les mêmes situations et les mêmes couleurs (Kevin). Le chrono de 15 s est imposé et le seuil de 4/5 est juste. Le chrono ne stresse pas Mamadou ; Sofiane le trouve exigeant, « c'est bien ».
- **Compteurs justes** quand Kevin les recalcule à la main : objectifs, critères de niveau, « Mes défis ».
- **Réglages à la main** : objectifs modifiables avec − / +, conservés après rechargement ; niveau changé en un toucher (Sofiane, Jean-Pierre).
- Les défis s'ignorent sans gêne (Jean-Pierre). Lecteur de vilain et Sous pression réussis avec plaisir (Léa).
- Les 3 écrans d'accueil d'un nouveau joueur sont clairs, en environ 25 s, et le niveau 1 convient à une débutante (Nadia).

## 3. Problèmes

### Défis
1. **« Seule la première tentative compte » se contourne** (Kevin, Jean-Pierre) :
   - une tentative abandonnée ne compte pas : « Relever » revient, avec les mêmes mains ;
   - finir plus tard une tentative abandonnée réécrit le résultat (une réussite à 5/5 devient « 0/5 » et disparaît de « Mes défis ») ;
   - le serveur accepte une deuxième tentative (201) ;
   - le défi se refait une fois par mode.
2. **Bilan trompeur** : « pas encore réussi » sur le défi du jour, qu'on ne peut pas retenter (Sofiane, Léa, Jean-Pierre, Kevin). Il faudrait « Défi du jour : 3/5. Nouveau défi demain. ».
3. **Série parfaite sur un autre thème que la séance** (les six) : « Premier à parler, 17 à 25 BB » contre « Face à un tapis, moins de 10 BB ». Ce thème est souvent hors du niveau du joueur : une débutante fait 1/5 sur du niveau 3, puis « À travailler » la renvoie vers ce thème (Nadia).
4. **Semaine pleine contre la série de jours** : « 5 jours de suite » en haut, « meilleure suite du mois : 3 jours » sur la carte (Kevin, Léa). La série de jours pardonne un jour manqué, la carte Semaine pleine non, et rien ne le dit.
5. **Range au cordeau validée sur une range jugée « Trop serrée »** (Kevin, Jean-Pierre) : 0,81 à 1,64 BB perdus pour 100, mais 82 % de justesse.
6. Sous pression trop facile avec un seuil à 3/5 (Sofiane). Lecteur de vilain trop facile : 8 questions sur 10 portent sur un « Défaut du vilain » qu'on lit sur les barres observé / théorie (Léa).
7. « Mes défis » ne montre que les réussites (Nadia, Léa).

### Thème du jour et séance
8. **Le thème du jour change dans la journée** (Kevin trois fois, Léa, Sofiane) : il est recalculé à chaque affichage à partir du diagnostic du moment. L'écran de fin affiche « Thème travaillé : … · BB » alors que tout a été joué en SB premier à parler. Une fois, le libellé était « Ton thème du jour » (Sofiane). La série « thème » a mélangé des tapis de 4 à 25 BB (Sofiane, Léa).
9. La range du jour a changé de situation entre deux affichages (Nadia).
10. **Révision contradictoire** : « Révision : 6 mains à revoir » cochée et barrée, alors que « Revoir mes mains (6 mains prêtes) » est encore proposé (Mamadou). Sofiane voit « rien à revoir aujourd'hui » et, au même moment, « Prochaine révision : jeudi 29 octobre (23 mains) ».
11. En mode Exploitant, la range du jour est corrigée sur la théorie juste après des séries exploitantes, et l'écran ne le dit pas (Léa).

### Niveaux et mode
12. **Le niveau ne suit pas le mode** (Léa, Jean-Pierre) :
    - « Ma progression » affiche « Niveau 1 · Tapis courts » en Exploitant et ne propose que les niveaux 1 à 3 ;
    - `#today-level` n'est pas rafraîchi au changement de mode, d'où « Niveau 4 » en GTO jusqu'au rechargement.
13. **Le compteur de décisions du niveau ne compte que les mains du palier, sans le dire** (Mamadou, Sofiane) : « 16/100 décisions » après beaucoup de mains jouées. Au niveau 3, des mains à 4-10 BB sont encore servies (Sofiane).
14. Le choix du mode est tout en bas et n'est gardé que dans le navigateur. Sur un nouvel appareil, un joueur qui a déjà joué voit « Première séance : c'est parti » (Léa, Jean-Pierre).

### Accueil et chiffres
15. **Accueil trop long** (les six) : 5 à 6 blocs sur environ 3 écrans de téléphone, avec 5 défis empilés. « Jouer librement » est trop bas.
16. **Trois chiffres « BB perdus » et deux cibles sur le même écran** (les six) : 7 jours, niveau (< 15) et objectif (< 20). Sofiane voit 63,05 / 5,6 / 63,05. « BB perdus / 100 » n'est pas compris sans aide (Nadia).

### Objectifs
17. **Cibles impossibles acceptées** : « 5 séances » ou « 7 séances » un jeudi avec « Encore 3 jours » (Nadia, Sofiane). « 3 ranges à 85 % » est trop dur pour une débutante (Nadia).
18. Le bilan de la semaine passée dit « objectifs reconduits plus faciles » alors qu'il n'y avait aucun objectif (Kevin).
19. Le jeu libre ne compte pas dans « Séances dans la semaine », et les objectifs sont séparés par mode sans que ce soit dit (Jean-Pierre).

### Divers
20. **Erreur 429** :
    - le chrono continue derrière le bandeau « Trop de requêtes… », et la main est comptée « Temps écoulé » (Jean-Pierre) ;
    - le bloc objectifs reste vide, sans message (Léa).
21. Un coup joué au temps qui tombait sur le meilleur coup compte en erreur (Kevin). C'est conforme à la règle, mais à expliquer.
22. Recommandation : « trop large » ou « trop serré » pour parler de la taille de la mise prête à confusion (Mamadou). Sens inversé une fois par rapport à la première erreur (Sofiane).
23. Écrans d'accueil : « Moins de / Plus de 3 mois » fait hésiter quelqu'un qui joue depuis 3 mois pile ; « Tapis courts » sans BB ; « field » absent du Lexique (Nadia).
24. Des pourcentages diffèrent entre l'énoncé et la correction (51 % contre 53 %, Jean-Pierre). A8s payé « avec 76 % des mains » face à un limp puis le tapis du BTN est jugé douteux (Sofiane).

### Demandes
- Classement ou taux de réussite du défi du jour, partage du résultat façon Wordle, badges (Léa, Sofiane).

## 4. Proposition de corrections
- **Défis (1-7)** :
  - tentative du défi du jour enregistrée dès la création de la série, une seule par jour tous modes confondus, refus serveur (409) ensuite ;
  - bilan « Nouveau défi demain » ;
  - série parfaite sur le thème de la séance du jour ;
  - Semaine pleine alignée sur la série de jours (ou règle écrite) ;
  - Range au cordeau à exiger aussi une justesse d'au moins 85 % ;
  - Sous pression à 4/5 ;
  - lecteur de vilain avec au moins 2 « Quelle pastille ? » ;
  - tentatives visibles dans « Mes défis ».
- **Thème (8-11)** :
  - thème et range du jour figés pour la journée (en base, au premier affichage) ;
  - libellé de fin = celui de la séance ;
  - révision barrée seulement quand toutes les mains dues ont été revues ;
  - mention « corrigée sur la théorie » sur la range en Exploitant.
- **Niveaux et mode (12-14)** :
  - niveau rafraîchi au changement de mode, niveau 4 affiché en Exploitant ;
  - « 16/100 décisions à moins de 10 BB » ;
  - niveaux 2 et 3 limités à leurs profondeurs dans la séance ;
  - mode remonté en haut et gardé côté serveur.
- **Accueil (15-16)** :
  - défis repliés en une ligne (« Défi du jour + 3 autres ») ;
  - un seul chiffre BB sur l'accueil, avec une seule cible ;
  - aide « BB perdus / 100 » au toucher.
- **Objectifs (17-19)** :
  - cible de séances plafonnée aux jours restants ;
  - cibles de départ plus basses pour un nouveau joueur ;
  - bilan de la semaine passée seulement si des objectifs existaient.
- **Divers (20-24)** : chrono en pause pendant une erreur réseau, message dans les blocs vides, textes des écrans d'accueil et du Lexique.
- **Plus tard** : classement du défi du jour et partage (avec les comptes).

## 5. Corrections faites (29/10/2026)

Branche `claude/eloquent-shannon-5afovj`. Contrôles : `tests/test_retest9.py` (13 tests), `tools/web/e2e_retest9.cjs`, parcours existants mis à jour (application et démo).

| N° | Correction |
|---|---|
| 1 | Défi du jour : une seule tentative par jour UTC, tous modes confondus, comptée dès la création de la série ; le serveur refuse la deuxième (409). Une tentative abandonnée se reprend (« Reprendre », chrono 15 s imposé de nouveau) mais ne se refait pas. |
| 2 | Bilan : « Défi du jour : 3/5. Nouveau défi demain. » ; les autres défis disent « Tu peux le retenter ». |
| 3 | Série parfaite sur le thème de la séance du jour du joueur. |
| 4 | Semaine pleine comptée comme la série de jours (un jour manqué par semaine pardonné), et la règle le dit ; la série de jours compte tous les modes. |
| 5 | Range au cordeau : moins de 2 BB perdus pour 100 mains et au moins 85 % de mains bien classées. |
| 6 | Sous pression à 4/5 ; Lecteur de vilain avec au moins 2 « Quelle pastille ? » par série. « Défaut du vilain » plus difficile : confié au Moteur exploitant (E1 du document de suivi). |
| 7 | « Mes défis » montre les tentatives (✓ réussie, ✗ pas réussie). |
| 8-9 | Thème et situation de la range fixés au premier affichage de la journée (table `daily_plan`) ; un thème tiré du diagnostic doit avoir une situation et une profondeur ; le libellé de fin est celui de la séance. Si le niveau change avant le début du thème, la séance est recalculée sur le nouveau niveau. |
| 10 | Révision cochée seulement quand plus aucune main n'est due ; « rien à revoir pour l'instant (23 mains à partir de 18 h 30) » quand des mains reviennent plus tard dans la journée. |
| 11 | En Exploitant, l'écran de range dit « corrigé sur la stratégie théorique (GTO), pas contre les joueurs du field ». |
| 12 | Niveau 4 affiché en Exploitant (accueil et progression), niveaux 1 à 4 proposés ; choisir le niveau 4 passe en Exploitant ; niveau rafraîchi au changement de mode. |
| 13 | « 16/100 décisions à moins de 10 BB » ; la révision de la séance est complétée dans la profondeur du niveau. |
| 14 | Mode en haut de l'accueil, gardé sur le serveur (repris sur un nouvel appareil du même joueur) ; « Pas encore de série aujourd'hui » au lieu de « Première séance » pour un joueur qui a déjà joué. |
| 15 | Défis repliés en une ligne (« Défi du jour : à relever · + 4 autres ») ; l'accueil passe d'environ 3 à 1,9 écran de téléphone. |
| 16 | Un seul chiffre BB sur l'accueil : l'objectif de précision de la semaine, avec sa cible et l'aide au toucher (Lexique). Les BB sur 7 jours restent sur l'écran de fin de séance, le critère BB du niveau dans « Ma progression ». |
| 17 | Cible de jours plafonnée aux jours restants (serveur et boutons − / +) ; nouveau joueur : 3 jours et 1 range à 85 %. |
| 18 | Bilan de la semaine passée seulement s'il y avait des objectifs. |
| 19 | « Jours d'entraînement » : séance, jeu libre et ranges comptent ; titre « Objectifs de la semaine · GTO / Exploitant ». |
| 20 | Chrono en pause tant que le message d'erreur est affiché, reprise du temps restant à la fermeture ; le coup joué au temps garde son statut au réessai ; messages « indisponibles pour l'instant, Réessayer » dans les blocs Objectifs et Défis. |
| 21 | « C'était le bon coup, mais il compte comme une erreur : à la table, laisser filer le temps n'est jamais un choix. » |
| 22 | Erreurs de taille nommées comme telles (« tu relances petit quand il fallait aller à tapis ») ; un sens n'est annoncé que s'il couvre au moins la moitié des erreurs. |
| 23 | « 3 mois ou plus » ; niveaux du premier lancement avec leur profondeur ; « Field » au Lexique (1.12.2, 83 termes). |
| 24 | Non traité : écarts de pourcentages énoncé / correction et A8s payé « avec 76 % des mains », à reproduire avec la main exacte. |

Reste pour plus tard : classement et partage du défi du jour (D2, D7 du document de suivi).
