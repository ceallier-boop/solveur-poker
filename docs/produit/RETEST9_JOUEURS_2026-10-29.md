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

Mêmes règles dans l'application et dans la démo autonome. Contrôles : `tests/test_challenges.py`, `test_today.py`, `test_goals.py`, `test_recommend.py`, `test_review.py` ; `tools/web/e2e_retest9.cjs` (20 vérifications sur l'application, 17 sur la démo).

| # | Problème | Fait |
|---|---|---|
| 1 | Défi du jour contournable | La tentative compte dès la création de la série, une seule par jour UTC, tous modes confondus ; une deuxième série est refusée (409). Une tentative abandonnée se **reprend** (« Reprendre », même série, chrono 15 s), elle ne se recommence pas. |
| 2 | Bilan trompeur | « Défi du jour : 3/5. Nouveau défi demain. » ; la carte de l'accueil dit la même chose. Les autres défis : « pas encore réussi. Tu peux le retenter. » |
| 3 | Série parfaite hors du thème | Elle se joue sur le thème de la séance du jour du joueur, donc dans son niveau. |
| 4 | Semaine pleine contre série de jours | Les deux comptent maintenant les mêmes jours (tous modes confondus, ranges comprises). La règle est écrite sur la carte : « 7 jours d'affilée, sans jour manqué ; la série de jours de l'accueil, elle, pardonne un jour par semaine » ; résultat : « meilleure suite sans jour manqué ce mois-ci ». |
| 5 | Range au cordeau sur une range « trop serrée » | Il faut aussi au moins 85 % de mains bien classées. |
| 6 | Défis trop faciles | Sous pression à 4/5 ; Lecteur de vilain avec au moins 2 « Quelle pastille ? » dans la série. |
| 7 | « Mes défis » | Toutes les tentatives finies, réussies (✓) ou non. |
| 8 | Thème du jour qui change | Thème et range du jour figés au premier affichage (table `day_plan`), sauf changement de niveau ; seul un thème fragile ou à surveiller (situation, position et profondeur) peut devenir le thème, jamais un score par dimension (« Position : SB ») qui mélangeait les tapis de 4 à 25 BB. L'écran de fin reprend le libellé de la séance. |
| 9 | Range du jour qui change | Même situation toute la journée (`spot_id` dans la séance du jour). |
| 10 | Révision contradictoire | L'étape n'est cochée que quand il ne reste plus de main à revoir aujourd'hui (« Révision : faite ») ; les échéances se comptent en jours du joueur, donc « Prochaine révision : aujourd'hui » n'arrive plus à côté de « rien à revoir ». |
| 11 | Range en exploitant | Mention « Exercice corrigé sur la stratégie théorique (GTO), même en mode Exploitant ». |
| 12 | Niveau et mode | La ligne de niveau de l'accueil et « Mon niveau » suivent le mode (niveau 4 en Exploitant, avec le niveau GTO rappelé). |
| 13 | Compteur du niveau | « 16/100 décisions à moins de 10 BB » ; les séances des niveaux 2 et 3 restent dans leur profondeur (voir 8). |
| 14 | Mode tout en bas, gardé dans le navigateur | Le choix GTO / Exploitant est en haut de l'accueil et gardé côté serveur (`PUT /users/me/preferences`). Un autre appareil reste un nouveau joueur tant qu'il n'y a pas de comptes (lot B3). |
| 15 | Accueil trop long | Ordre : mode, séance, recommandations, « Jouer librement », objectifs, défis. Seul le défi du jour est visible ; les autres sont repliés en une ligne (« 4 autres défis · 1 réussi »). |
| 16 | Trois chiffres BB | Un seul chiffre BB sur l'accueil : celui de l'objectif de la semaine, avec sa cible ; « BB perdus pour 100 décisions » s'explique au toucher. Le niveau garde son critère BB dans « Ma progression ». |
| 17 | Cibles impossibles | Séances plafonnées à ce qui reste possible dans la semaine (le « + » se bloque, le serveur refuse au-delà) ; nouveau joueur : 3 séances et 1 range à 85 %. |
| 18 | Bilan sans objectifs | Le bilan de la semaine passée ne s'affiche que s'il y avait des objectifs. |
| 19 | Jeu libre et modes | Dit sous les objectifs : « objectifs du mode GTO ; les séances comptées sont celles de la séance du jour ». |
| 20 | Erreur 429 | Le chrono se met en pause pendant l'envoi et tant que le message d'erreur reste affiché, puis reprend ; « Réessayer » garde le coup joué (et le « temps écoulé » s'il y en avait un). Séance, objectifs et défis affichent un message et « Réessayer » au lieu d'un cadre vide. L'accueil ne s'affiche plus avant de savoir s'il faut le premier lancement, ce qui évite aussi une rafale de requêtes en double au démarrage. |
| 21 | Coup au temps sur le bon coup | La correction le dit : « C'était le bon coup, mais il compte comme une erreur : à la table, laisser filer le temps n'est jamais un choix. » |
| 22 | « Trop large / trop serré » | Recommandation reformulée en jetons : « le plus souvent en mettant moins (plus) de jetons qu'il ne fallait : tu te couches ou tu paies quand il fallait relancer ou pousser ». |
| 23 | Textes du premier lancement et Lexique | « 3 mois ou plus » ; chaque niveau avec sa profondeur (« Tapis courts · à moins de 10 BB ») ; terme « Field » ajouté au Lexique (1.12.2). |
| 24 | Pourcentages énoncé / correction, A8s | **Non traité** : il faut les mains exactes pour vérifier (données, pas interface). |

Pas fait, comme prévu : classement et partage du défi du jour (avec les comptes).
