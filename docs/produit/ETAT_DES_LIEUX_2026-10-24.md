# État des lieux de SpinsAcademy (24/10/2026)

Sources : plan en trois lots du 23/10 (`PLAN_LOTS_2026-10-23.md`), quatre tests joueurs (`RETEST*_JOUEURS_*.md`), lot 1 « table du client » (`LOT1_TABLE_CLIENT_2026-10-24.md`), plan d'évaluation du MVP (`PLAN_EVALUATION_MVP_2026-10-14.md`).

## 1. L'application aujourd'hui

| Domaine | Ce qui existe |
|---|---|
| **Mode GTO** | Banque `2026.10.13-3` : décisions préflop de 2 à 25 BB, heads-up et 3 joueurs, tapis égaux et inégaux. 1458 situations servies (une seule version par situation depuis le 24/10), mains mal résolues par la référence retirées. Séries tirées selon la fréquence réelle des situations. |
| **Mode exploitant** | Banque `2026.10.23-1` : 8000 questions de 4 à 25 BB, 12 situations (premier à parler, face à un limp, face à un open, face à un tapis, tapis après limp), relance non all-in, tapis inégaux en heads-up. Vilain inconnu, observé ou « pastille posée » (une question sur deux), questions « Défaut du vilain » et « Quelle pastille ? ». |
| **Correction** | Verdict en BB (bonne réponse < 0,02 BB, imprécision < 0,06 BB ou < 0,1 BB pour un coup jouable, erreur au-delà), coût du choix, message essentiel en une phrase chiffrée, « À retenir » sur chaque main, précisions repliées (barème, pourquoi, sur quoi ça repose, stratégie de référence), grille 13 × 13 en GTO, plan postflop quand le coup va au flop. Contre un inconnu, le coup théorique est au pire une imprécision. |
| **Table** | Comme au client de jeu : action sous chaque joueur, bouton D, mises en chiffres devant les joueurs, tapis restant, Pot total, tes cartes à ta place, barre d'actions FOLD / CHECK / CALL / RAISE TO / ALL-IN, stats du vilain en une ligne sous son siège, pastilles de couleur réglables (« Mes pastilles »). |
| **Progression** | Score global, évolution des séries, score par thème à partir de 10 questions, diagnostic « À travailler maintenant », séries adaptées aux erreurs (GTO), révision espacée à J+1, J+3, J+7. Accessible sans connexion (dernière progression gardée sur l'appareil, datée). |
| **Lexique** | Version 1.9.2, 78 termes, mots soulignés qui s'expliquent au toucher. |
| **Signalements et administration** | « Signaler cette main », relecture et clôture dans l'administration (jeton), catalogue des datasets avec validation, reconstruction et publication. |
| **Exploitation** | API FastAPI et SQLite, limitation de débit, préchargement des datasets au démarrage (un seul chargement par version, environ 600 Mo par processus), service worker (application ouverte hors ligne), procédures de déploiement, de retour arrière et de sauvegarde testées sur un serveur de test. |
| **Démo autonome** | Une page publiée (6710 questions, 2,7 Mo), progression gardée dans le navigateur, signalements dans une base partagée. |
| **Qualité** | 97 tests automatiques ; contrôles navigateur : parcours téléphone (clair et sombre), bêta (signalement, 4G, coupure réseau), hors ligne, démo avec données d'une ancienne version. |

**Notes des testeurs** (sur 5) :

| Test | Date | Moyenne | Commentaire principal |
|---|---|---|---|
| 1 | 23/10 | 3,5 (5 joueurs) | filtres perdus, seuils incohérents, jargon |
| 2 | 23/10 | 4,0 | contradictions dans les textes |
| 3 | 23/10 | 3,75 (6 joueurs) | réponses trop chargées, message essentiel générique |
| 4 | 24/10 | 4,0 | table « comme Winamax » ; textes répétitifs, petits défauts d'affichage |

Les corrections du test 4 et les pastilles à table n'ont pas encore été testées par les joueurs.

## 2. Ce qui était prévu, et ce qui a été fait

### Lot A (avant le MVP)

| # | Prévu | État |
|---|---|---|
| A1 à A12 | Corrections issues du premier test (filtres, ordre des actions, barème, un seul chiffre, stratégie mixte, pièges, vocabulaire, progression, « Sur quoi ça repose », signalement, 4G, coupure réseau) | **Fait** le 23/10, puis complété par trois séries de corrections (lot A', correction allégée, corrections du test 4). |
| A13 | Droits sur les données dérivées de la référence | **À faire, bloquant** (porteur du projet). Toutes les mentions du solveur et des coachs ont été retirées des textes servis et des documents ; les chemins techniques restent. |
| A14 | Politique de confidentialité, mentions légales, conditions d'utilisation, relecture d'un juriste | **Projet rédigé**, mis à jour pour la copie locale de la progression ; relecture à faire. |
| A15 | Hébergeur, installation de la production, sauvegardes externes chiffrées, surveillance | **Procédure prête et testée**, production non installée. |
| A16 | Mode invité ou comptes pour le MVP | **À trancher** (recommandation : invité). |
| A18 | Relecture experte de l'échantillon du 14/10 | **À trancher** (remplacée ou non par l'audit complet du 22/10). |

### Ajouts non prévus au plan, faits depuis

| Ajout | Origine |
|---|---|
| Suppression des mentions de la référence et des coachs (textes servis, documents, dossier `docs/reference`) | Demande du porteur du projet |
| Correction allégée : l'essentiel d'abord, précisions repliées | Demande du porteur du projet |
| Table et actions comme au client de jeu (lot 1 du plan « table ») | Captures du client fournies |
| Pastilles de couleur : réglage, à table, alternance avec la lecture des stats | Demande du porteur du projet |
| Message essentiel chiffré et propre à chaque main en exploitant | Test 4 |
| Une seule version par situation en GTO (452 doublons d'arbres retirés du tirage) | Test 4 (Kevin) |
| Panne mémoire du serveur sous charge corrigée (un seul chargement par version) | Test 1 |
| Démo robuste aux séries des anciennes versions | Retour du porteur du projet |

### Lot B (rapidement après le MVP)

| # | Prévu | État |
|---|---|---|
| B1 | Exports de référence priorité 1 (précision, 25 BB, heads-up open 2 / 2,5 / 3 BB, tapis inégaux), puis reconstruire les banques | **À faire** : calculs du porteur du projet. |
| B2 | Calibrer les profils sur un historique de mains réel | **À faire** : historique à fournir. |
| B3 | Comptes, synchronisation entre appareils, administrateurs nominatifs | **À faire** (après A16). |
| B4 | Offre gratuite / payante, paiement | **À faire** (après A13). |
| B5 | Accueil en trois écrans, objectif du jour, série de jours | **À faire**. |
| B6 | Mode hors ligne | **En partie** : l'application s'ouvre et la progression s'affiche sans réseau ; jouer une série demande encore le serveur. |
| B7 | Exploitant : open à 2 BB, SB face au limp du BTN, pots limpés à 3 | **À faire** (après B1). |
| B8 | Pastille « Nit » renforcée, pastilles hors heads-up | **En partie** : les pastilles s'affichent à 3 joueurs ; les questions « Quelle pastille ? » restent en heads-up. |
| B9 | Thème choisi dans l'application, deux colonnes sur grand écran, bilan cliquable | **À faire**. |
| B10 | Ligne « bloqueurs » dans la grille, questions « quelle taille ? » | **À faire**. |
| B11 | Audit d'accessibilité (RGAA) | **À faire** (quelques points traités : lecteur d'écran, couleurs nommées, lettres dans les pastilles). |

### Lot C (plus tard)

C1 postflop, C2 ICM, C3 tapis inégaux à 3 joueurs et 3-bet non all-in, C4 calculs verrouillés par profil, C5 EV exacte à 3 joueurs, C6 base serveur, C7 conseils payants : **rien de commencé**, comme prévu.

## 3. Ce qu'il reste à faire

### Avant la mise en ligne (bloquant)
1. **Droits sur les données de référence** (A13) : licence ou accord écrit ; à défaut, au moins l'accord pour une bêta fermée et gratuite.
2. **Juriste** (A14) : politique de confidentialité, mentions légales, conditions d'utilisation.
3. **Production** (A15) : choisir l'hébergeur (4 Go de mémoire recommandés), domaine en HTTPS, jeton d'administration, sauvegardes externes, surveillance.
4. **Décisions** : invité ou comptes (A16), relecture experte (A18), journal d'usage de la bêta (A17).

### Côté application, court terme
5. **Cinquième test joueurs** sur la version actuelle (corrections du test 4, pastilles à table et alternance).
6. **Points ouverts du test 4** :
   - équité de ta main quand un joueur reste à parler ;
   - raccourcis clavier vus sur téléphone, à vérifier sur un vrai appareil.
7. **Lot 2 « table du client »** : mode chrono au choix, correction affichée sur la même table, questions « pastille douteuse » (note posée sur peu de mains, contredite par les stats).
8. **Mots encore difficiles** pour une débutante : noms de mains (87o, Q9s), « Mains à la limite », « effectifs ».
9. **Questions « Défaut du vilain »** jugées trop faciles par un régulier : à durcir.

### Côté données
10. **Exports de référence priorité 1** (B1), puis reconstruction des deux banques. Cela réglera aussi le SB à 25 BB sans limp ni tapis, et les tapis toujours ronds (8 / 8 / 8).
11. **Historique de mains** pour calibrer les profils (B2) : aujourd'hui, le profil du rec passif est une hypothèse, ce que la correction dit franchement.
12. **Renommer les identifiants techniques** encore marqués du nom du solveur (`data/hrc`, `tools/hrc`, `ev_hrc`, valeur `hrc`) : à faire avec la prochaine version des banques, puisqu'une version publiée ne se modifie pas.

### Ensuite
13. Lot B restant (comptes, offre et paiement, accueil, interface grand écran, bloqueurs, accessibilité), puis lot C, à commencer par le postflop (C1).
