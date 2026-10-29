# Programme de travail SpinsAcademy (proposition du 29/10/2026)

Objectif : transformer la boîte à outils actuelle (séries, ranges, conseiller, progression) en un **programme suivi** : le joueur ouvre l'application, sait quoi faire aujourd'hui, voit pourquoi, et mesure ce qu'il gagne. Ce document reprend et précise le lot B5 du plan (« accueil en trois écrans, objectif du jour, série de jours »).

## 1. Principes

1. **Peu, souvent** : une séance de 15 minutes par jour vaut mieux qu'une heure le dimanche. Variantes de 5 et 30 minutes.
2. **Une mesure qui compte** : les BB perdus pour 100 décisions, sur 7 jours glissants, comparés à la semaine précédente. Le score en % reste affiché, mais c'est lui qui guide.
3. **Du plus simple au plus fin** : tapis courts et tout ou rien d'abord, puis le jeu à 10-16 BB, puis 17-25 BB, puis l'exploitation.
4. **Revoir ses erreurs** : la révision espacée (J+1, J+3, J+7) passe toujours en premier.
5. **Relier l'entraînement au jeu réel** : le conseiller sert entre deux parties ; « Mes mains » ramène les vraies erreurs dans l'entraînement quand cette fonction sera intégrée.
6. **Jamais de culpabilisation** : pas de compteur rouge, une série de jours qui pardonne un jour manqué par semaine.

## 2. Le parcours en quatre niveaux

Chaque niveau dure environ deux semaines pour un joueur régulier. Il se débloque par des critères mesurés, jamais par le temps passé. Un joueur peut toujours jouer librement hors du parcours.

| Niveau | Contenu (filtres existants) | Outils mis en avant | Pour passer au niveau suivant |
|---|---|---|---|
| **1. Tapis courts** | Moins de 10 BB, heads-up puis 3 joueurs : premier à parler, face à un tapis | Séries GTO, ranges « pousses-tu », « paies-tu le tapis », chrono 15 s | 100 décisions à moins de 15 BB perdus pour 100 ; 3 ranges du niveau à 85 % ou plus |
| **2. Le jeu à 10-16 BB** | 10 à 16 BB : limp, iso, face à un limp, face à une relance | Séries adaptées, ranges « limpes-tu », « relances-tu » | 150 décisions à moins de 12 BB pour 100 ; aucun thème du niveau marqué « fragile » |
| **3. Le jeu à 17-25 BB** | 17 à 25 BB, 3 joueurs : ouvertures, défense, BTN | Séries, ranges, conseiller sur les spots ratés | 150 décisions à moins de 10 BB pour 100 |
| **4. Exploiter le field** | Mode exploitant : pastilles, vilain observé, « Défaut du vilain », « Quelle pastille ? » | Séries exploitantes, pastilles, chrono 8 s | Niveau ouvert en continu : objectifs hebdomadaires |

Le niveau de départ se choisit au premier lancement (trois questions, voir §4.1) ou se déduit d'un test de placement de 10 décisions.

## 3. La séance du jour

Construite automatiquement à partir de ce que l'application sait déjà (révisions dues, thèmes fragiles, niveau en cours). Elle s'affiche sur l'accueil sous forme de 3 ou 4 étapes à cocher.

| Étape | Durée | Contenu | Source |
|---|---|---|---|
| 1. Révision | 2-3 min | Les mains ratées dont la date de révision est arrivée | Révision espacée existante |
| 2. Le thème du jour | 6-8 min | Deux séries de 5 sur le thème à travailler (le plus fragile, sinon le prochain thème du niveau) | Séries adaptées existantes |
| 3. La range du jour | 3 min | Un exercice « Construis ta range » sur la situation du thème | Exercice de range existant |
| 4. Le défi (facultatif) | 2 min | Le défi du jour (§6) | Nouveau |

Variantes, au choix sur l'accueil :
- **5 minutes** : révision et une série du thème ;
- **30 minutes** : la séance, plus une série au chrono 8 s et deux ranges.

Fin de séance : un écran court « Ta séance » qui donne les BB perdus de la séance, le thème travaillé, ce qui revient demain, et l'effet sur les objectifs de la semaine.

## 4. L'accueil réorganisé

### 4.1 Premier lancement (trois écrans, lot B5)
1. « Tu joues en Expresso depuis… » (moins de 3 mois / plus / je joue beaucoup) et « Ton but » (comprendre les bases / gagner plus contre les récréatifs / affûter mes ranges).
2. Le niveau de départ proposé (ou le test de placement de 10 décisions), et le mode : GTO d'abord, exploitant à partir du niveau 2 pour un joueur confirmé.
3. Le temps par jour (5, 15 ou 30 minutes), et un rappel facultatif.

### 4.2 Accueil des jours suivants (de haut en bas)

```
┌──────────────────────────────────────────────┐
│ Bonjour · Niveau 2 « Le jeu à 10-16 BB »      │
│ 🔥 6 jours de suite      BB perdus / 100 : 9,8 │
│                          ▼ 2,1 sur 7 jours    │
├──────────────────────────────────────────────┤
│ TA SÉANCE DU JOUR · 15 min                    │
│ ☐ Révision : 4 mains                          │
│ ☐ Thème : BB face au limp du SB, 10-16 BB     │
│ ☐ Range : « Avec quelles mains isoles-tu ? »  │
│ ☐ Défi du jour                                │
│ [        Commencer la séance        ]         │
│ 5 min · 30 min · Jouer librement              │
├──────────────────────────────────────────────┤
│ RECOMMANDÉ POUR TOI                           │
│ • Tu paies trop large face au tapis du SB à   │
│   4-6 BB (5 erreurs sur 8). → 1 série ciblée  │
│ • Ta range de limp au SB est trop serrée      │
│   (18 % au lieu de 35 %). → refaire la range  │
├──────────────────────────────────────────────┤
│ OBJECTIFS DE LA SEMAINE                       │
│ 5 séances            ▓▓▓▓▓▓░░░░ 3/5          │
│ < 10 BB/100 au BB    ▓▓▓▓▓▓▓░░░ 11,2 → 10    │
│ 3 ranges à 85 %      ▓▓▓▓▓▓▓▓▓░ 2/3          │
├──────────────────────────────────────────────┤
│ DÉFIS                                         │
│ Aujourd'hui : « Série parfaite au BTN »       │
│ Semaine : « 50 décisions au chrono 8 s »      │
├──────────────────────────────────────────────┤
│ OUTILS                                        │
│ Jouer librement · Construis ta range ·        │
│ Comment jouer ma main ? · Mes mains ·         │
│ Ma progression · Mes pastilles · Lexique      │
└──────────────────────────────────────────────┘
```

Règles d'affichage :
- un seul bouton plein sur l'écran : « Commencer la séance » (ou « Continuer la séance » si elle est entamée) ;
- séance terminée : le bloc devient « Séance faite ✓ — Demain : 3 révisions, thème suivant… » et le bouton plein passe à « Une série en plus » ;
- le choix GTO / Exploitant et le chrono descendent dans « Jouer librement » : la séance les fixe selon le niveau ;
- sur grand écran : séance et recommandations à gauche, objectifs et défis à droite (lot B9).

## 5. Les recommandations

Au plus deux à la fois, chacune avec **un constat chiffré** et **une action en un toucher**. Ordre de priorité :

| Priorité | Déclencheur (données existantes) | Message type | Action |
|---|---|---|---|
| 1 | Révisions en retard de plus de 2 jours | « 6 mains attendent leur révision depuis lundi. » | Série de révision |
| 2 | Thème fragile (règle des séries adaptées : au moins 3 réponses dont 2 erreurs) | « Tu paies trop large face au tapis du SB à 4-6 BB (5 erreurs sur 8). » | Série ciblée sur ce thème |
| 3 | Range du thème sous 80 % ou diagnostic « trop serrée / trop large » | « Ta range de limp au SB est trop serrée (18 % au lieu de 35 %). » | Refaire cette range |
| 4 | Erreurs répétées sur la même famille de décision au chrono | « Au chrono, tu te couches trop souvent au BB. » | Série au chrono sur ce thème |
| 5 | Mains réelles importées (quand « Mes mains » sera intégré) | « Sur tes 120 dernières mains, 3 erreurs coûteuses au SB face au limp du BTN. » | Rejouer ces mains |
| 6 | Niveau presque validé | « Plus que 30 décisions sous 12 BB pour 100 pour passer au niveau 3. » | Séance du niveau |
| 7 | Rien de tout ça | « Découvre un thème que tu n'as jamais joué : BTN à 17-25 BB. » | Série découverte |

Le conseiller s'y intègre de deux façons :
- depuis une correction ou une recommandation : « Voir cette situation dans le conseiller » ouvre `/conseil` préréglé (tapis, position, coup) ;
- les situations consultées dans le conseiller alimentent la recommandation 7 : « Tu as consulté 4 fois BB face au limp à 12 BB : entraîne-toi dessus. »

## 6. Les objectifs

Trois objectifs par semaine, proposés le lundi, modifiables :

| Type | Exemple | Adapté au joueur |
|---|---|---|
| **Régularité** | 5 séances dans la semaine | selon le temps choisi (3, 5 ou 7) |
| **Précision** | Moins de 10 BB perdus pour 100 sur le thème du niveau | cible = moyenne des 4 dernières semaines moins 10 % |
| **Ranges** | 3 ranges à 85 % ou plus | situations du niveau |

En option, un objectif « Vitesse » (50 décisions au chrono 8 s à moins de 15 BB pour 100) pour un joueur du niveau 3 ou 4.

Bilan du dimanche : objectifs tenus ou non, évolution des BB perdus, thème le plus progressé, thème à surveiller. Un objectif manqué est reconduit plus facile, jamais affiché en échec.

## 7. Les défis

Courts, facultatifs, pour donner du rythme. Ils ne changent ni la correction ni la progression.

| Défi | Règle | Fréquence |
|---|---|---|
| **Défi du jour** | Les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date), au chrono 15 s | Quotidien |
| **Série parfaite** | 5 bonnes réponses sur un thème donné | Quotidien, thème tournant |
| **Sous pression** | Une série au chrono 8 s sans coup joué au temps | Hebdomadaire |
| **Range au cordeau** | Une range à moins de 2 BB perdus pour 100 mains | Hebdomadaire |
| **Lecteur de vilain** | 5 « Quelle pastille ? » justes d'affilée | Hebdomadaire (niveau 4) |
| **Semaine pleine** | 7 jours de suite | Mensuel |

Récompenses : une marque sur la carte du défi et un historique « Mes défis » dans la progression. Classement entre joueurs : seulement après la mise en place des comptes (B3), sur le défi du jour, et facultatif.

Série de jours : un jour compte dès qu'une séance (même de 5 minutes) est faite ; un jour manqué par semaine est pardonné automatiquement.

## 8. Ce qu'il faut construire

| Élément | Réutilise | Nouveau |
|---|---|---|
| Séance du jour | révision, séries adaptées, range, filtres | `GET /users/me/today` (plan du jour), suivi des étapes |
| Niveaux | progression par thème, BB perdus | table `player_level`, critères de passage, test de placement |
| Recommandations | diagnostic « À travailler maintenant », révision, ranges | règles du §5 dans `progress.py`, `GET /users/me/recommendations` |
| Objectifs | stats existantes | table `goals` (semaine, type, cible, valeur) |
| Défis | tirage à graine fixe (comme les tests) | table `challenges`, tirage du jour par date |
| Accueil | écran actuel | nouvel ordre de l'accueil (§4), premier lancement en 3 écrans |
| Conseiller relié | `/conseil` | paramètres d'URL (tapis, position, coup) pour l'ouvrir préréglé |
| Démo autonome | shim existant | même logique en local (navigateur), sans classement |

## 9. Ordre de réalisation proposé

1. **Séance du jour et accueil réorganisé** (le plus visible) : plan du jour, étapes à cocher, écran de fin de séance, série de jours.
2. **Recommandations** (priorités 1 à 4 et 6-7) et lien vers le conseiller préréglé.
3. **Objectifs de la semaine** et bilan du dimanche.
4. **Niveaux** et premier lancement en trois écrans.
5. **Défis**.
6. Recommandation 5 (mains réelles), quand « Mes mains » sera intégré au dépôt.

Après les étapes 1 et 2 : un test joueurs centré sur « sais-tu quoi faire en ouvrant l'application, et pourquoi ? ».

## 10. Points à trancher

1. Durée par défaut de la séance : 15 minutes (recommandé) ou 10.
2. Le mode exploitant dès le niveau 1 pour un joueur confirmé, ou seulement au niveau 4.
3. Rappels (notification ou courriel) : oui, non, ou plus tard avec les comptes.
4. Défi du jour commun à tous : à garder anonyme tant qu'il n'y a pas de comptes.
5. Seuils de passage des niveaux (§2) : à caler sur les données des premiers joueurs.

## 11. Étape 1 réalisée (29/10/2026) : séance du jour et accueil

Décision du porteur du projet : séance de 15 minutes.

- **Accueil** : en tête, la carte « Ta séance du jour · 15 min » avec la série de jours, les BB perdus pour 100 décisions sur 7 jours (et l'écart avec la semaine précédente), trois étapes à cocher et le seul bouton plein de l'écran (« Commencer la séance », « Continuer la séance », puis « Une série en plus »). Dessous, « Jouer librement » regroupe le mode, le chrono, la série rapide, l'exercice de range, le conseiller et la progression.
- **Étapes** (`spinsacademy/today.py`, `GET /users/me/today?mode=&tz=`) :
  1. révision des mains arrivées à échéance (faite d'office s'il n'y a rien à revoir) ;
  2. thème du jour en 2 séries de 5 : le thème à travailler du diagnostic, sinon un cycle de 8 thèmes qui commence par les tapis courts pour un nouveau joueur ; le thème reste le même toute la journée ;
  3. range du jour sur la situation du thème (filtres élargis si l'exercice n'a pas de situation pour ce thème).
- **Enchaînement** : à la fin de chaque série ou range, « Suite de la séance » lance l'étape suivante ; à la fin, l'écran « Séance du jour faite » (thème, BB perdus sur 7 jours, série de jours, ce qui revient demain).
- **Série de jours** : un jour compte dès qu'une série est finie ou qu'une range est faite ; un jour manqué par période de 7 jours est pardonné. La journée suit le fuseau de l'appareil.
- Les séries de la séance sont marquées en base (`sessions.plan` : `review` ou `theme`) ; la démo autonome refait le même calcul dans le navigateur.
- Contrôles : `tests/test_today.py`, `tools/web/e2e_today.cjs` (application et démo).

Hors étape 1, prévu ensuite : variantes 5 et 30 minutes, défi du jour dans la séance (étape 5), recommandations (étape 2).

## 12. Étape 2 réalisée (29/10/2026) : recommandations et conseiller relié

- **Accueil** : bloc « Recommandé pour toi » entre la séance du jour et « Jouer librement » ; au plus deux cartes, chacune avec un constat chiffré et un bouton qui lance l'action.
- **Règles** (`spinsacademy/recommend.py`, `GET /users/me/recommendations?mode=&tz=`), par priorité :
  1. révisions en retard de plus de 2 jours → « Revoir mes mains » ;
  2. thème fragile (au moins 2 erreurs), autre que le thème de la séance, avec le sens des erreurs (« surtout en jouant trop serré : tu te couches ou tu paies quand il fallait engager plus » / « trop large ») → « Une série ciblée » ;
  3. dernière range trop serrée, trop large ou sous 80 % → « Refaire cette range » (la même situation, `GET /ranges/next?spot=`) ;
  4. au moins 2 coups joués au temps sur 7 jours → « Série au chrono 15 s » ;
  5. découverte d'une situation jamais jouée dans le mode (jamais celle de la séance) → « Découvrir ».
- **Conseiller relié** : chaque correction du mode GTO propose « Voir cette situation dans le conseiller », qui ouvre `/conseil` sur la même table, les mêmes tapis, le même coup et la même main. Pas dans la démo autonome (le conseiller n'y est pas).
- Sens des erreurs : `progress.direction` compare le coup joué au meilleur coup (moins de jetons engagés : trop serré ; plus : trop large).
- La démo refait les mêmes règles dans le navigateur, sans le sens des erreurs.
- Contrôles : `tests/test_recommend.py`, `tools/web/e2e_recs.cjs` (application et démo).

Pas encore : recommandation « niveau presque validé » (avec les niveaux, étape 4), mains réelles (avec « Mes mains »), situations consultées dans le conseiller (le conseiller ne garde pas d'historique côté serveur).

## 13. Étape 3 réalisée (29/10/2026) : objectifs de la semaine

- **Accueil** : bloc « Objectifs de la semaine » sous les recommandations, trois objectifs avec leur barre et « encore N jours cette semaine » ; « modifier » affiche des boutons − / + pour changer chaque cible.
- **Objectifs** (`spinsacademy/goals.py`, `GET` et `PUT /users/me/goals`), semaine du lundi au dimanche dans le fuseau de l'appareil :
  - séances dans la semaine : jours avec au moins une série du thème de la séance finie (cible 5, de 1 à 7) ;
  - BB perdus pour 100 décisions de la semaine sous la cible, sur au moins 30 décisions (cible : moyenne des 4 dernières semaines moins 10 %, sinon 20) ;
  - ranges à 85 % ou plus (cible 3, de 1 à 10).
- Les cibles sont fixées à la première visite de la semaine (table `goals`), puis gardées ; un objectif manqué est reconduit un peu plus facile la semaine suivante, jamais affiché en échec.
- **Bilan de la semaine passée** en début de semaine : objectifs tenus, séances, BB perdus pour 100 décisions comparés à la semaine d'avant ; « OK » le range. L'écran de fin de séance rappelle où en sont les objectifs.
- Les objectifs sont exportés et effacés avec les autres données du joueur ; la démo refait les mêmes calculs dans le navigateur.
- Contrôles : `tests/test_goals.py`, `tools/web/e2e_goals.cjs` (application et démo).

Pas encore : objectif « vitesse » au chrono (avec les niveaux 3 et 4), bilan détaillé par thème (plus progressé, à surveiller).

## 14. Étape 4 réalisée (29/10/2026) : niveaux et premier lancement

- **Premier lancement** (nouveau joueur sans historique) en trois écrans : expérience et but ; niveau de départ proposé (moins de 3 mois → niveau 1, plus de 3 mois ou gros volume → niveau 2), modifiable ; présentation de la séance de 15 minutes et des objectifs. « Passer » démarre au niveau 1. Un joueur qui avait déjà joué n'y passe pas : il part du niveau 1 et monte d'après ses résultats.
- **Niveaux** (`spinsacademy/levels.py`, `GET` et `PUT /users/me/level`, `POST /users/me/onboarding`, table `player_level`) :
  1. Tapis courts (moins de 10 BB) : 100 décisions du niveau à moins de 15 BB perdus pour 100, et 3 ranges du niveau à 85 % ;
  2. Le jeu à 10-16 BB : 150 décisions à moins de 12, et aucun thème du niveau fragile ;
  3. Le jeu à 17-25 BB : 150 décisions à moins de 10 ;
  4. Exploiter le field : le mode exploitant, ouvert en continu.
  Mesure sur les 300 dernières décisions du niveau ; passage automatique (message « Bravo : tu passes au niveau 2… ») ; le joueur peut choisir son niveau de 1 à 3.
- **Séance du jour** : le thème vient du niveau (cycle de ses thèmes) ; un thème fragile hors du niveau n'est pas imposé. En mode exploitant, les thèmes du niveau 4.
- **Accueil** : la carte de la séance affiche le niveau et l'avancement (« 40/100 décisions · 33,9 BB/100 (cible < 15) · 0/3 ranges à 85 % ») ; un toucher ouvre « Mon niveau » dans la progression (critères cochés, changement de niveau).
- **Recommandation « niveau presque validé »** (application) : « Plus que 20 décisions pour passer au niveau 2. »
- Le niveau est exporté et effacé avec les autres données ; la démo refait les mêmes calculs dans le navigateur (sans la recommandation de niveau).
- Contrôles : `tests/test_levels.py`, `tools/web/e2e_onboard.cjs` ; les autres parcours passent le premier lancement par « Passer ».

Pas encore : test de placement de 10 décisions, choix du temps par jour (5 / 15 / 30 minutes), objectif « vitesse » des niveaux 3 et 4.

## 15. Étape 5 réalisée (29/10/2026) : défis

- **Accueil** : bloc « Défis » sous les objectifs ; chaque défi a sa période (aujourd'hui, cette semaine, ce mois-ci), sa règle, ton résultat et un bouton « Relever ».
- **Défis** (`spinsacademy/challenges.py`, `GET /users/me/challenges`, `POST /sessions` avec `challenge`) :
  - défi du jour : les mêmes 5 mains pour tous les joueurs du jour (tirage fixé par la date UTC), au chrono 15 s imposé ; réussi à 4 sur 5 ; seule la première tentative compte (le bouton disparaît ensuite) ;
  - série parfaite : 5 sur 5 sur le thème du jour, le même pour tous ;
  - sous pression (semaine) : une série au chrono 8 s imposé, sans coup joué au temps, à 3 sur 5 ou plus ;
  - range au cordeau (semaine) : une range à moins de 2 BB perdus pour 100 mains ;
  - lecteur de vilain (semaine, mode exploitant) : 5 lectures justes sur 5 ;
  - semaine pleine (mois) : 7 jours de suite d'entraînement dans le mois.
- Le bilan de série dit si le défi est réussi ; la progression a une section « Mes défis » (réussites des 60 derniers jours).
- Les défis ne changent ni la correction ni la progression ; pas de classement entre joueurs (après les comptes, B3).
- La démo refait les mêmes règles ; son défi du jour donne aussi les mêmes mains à tous les joueurs de la démo (tirage à graine fixe).
- Contrôles : `tests/test_challenges.py`, `tools/web/e2e_challenges.cjs` (application et démo).

Le programme de travail (étapes 1 à 5) est en place. Restent : variantes de séance de 5 et 30 minutes, test de placement, objectif « vitesse », bilan détaillé par thème, mains réelles (« Mes mains »), classements (avec les comptes).

## 16. Corrections du neuvième test joueurs (29/10/2026)

Détail dans `RETEST9_JOUEURS_2026-10-29.md` §5. Changements de règles par rapport aux §11 à §15 :
- défi du jour : une seule tentative par jour, tous modes confondus, comptée dès la création de la série ; une tentative abandonnée se reprend ;
- série parfaite : thème de la séance du jour du joueur (et non plus le même pour tous) ; sous pression à 4/5 ; range au cordeau avec au moins 85 % de mains bien classées ; lecteur de vilain avec au moins 2 « Quelle pastille ? » ;
- thème et range du jour figés pour la journée (table `day_plan`) ; étape de révision cochée seulement quand il ne reste rien à revoir ; échéances de révision en jours du joueur ;
- série de jours et semaine pleine comptées sur les mêmes jours, tous modes confondus ;
- objectifs : séances plafonnées aux jours restants, cibles de départ plus basses pour un nouveau joueur, bilan seulement s'il y avait des objectifs ;
- accueil : mode en haut (gardé côté serveur), « Jouer librement » avant les objectifs et les défis, défis repliés, un seul chiffre BB.
