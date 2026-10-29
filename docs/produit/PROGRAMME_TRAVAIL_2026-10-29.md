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
