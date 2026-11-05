# État des lieux de SpinsAcademy (29/10/2026)

Remplace l'état des lieux du 24/10. SpinsAcademy est une application d'entraînement complète en mode invité, avec un programme suivi (séance du jour, niveaux, objectifs, défis) ; elle n'est pas en ligne. Trois choses bloquent la suite : la mise en ligne (juriste, hébergeur), un historique de mains réel et les exports de référence v4.

Sources : `PLAN_LOTS_2026-10-23.md`, `PROGRAMME_TRAVAIL_2026-10-29.md`, les neuf tests joueurs (`RETEST*_JOUEURS_*.md`), `ANALYSE_ECRANS_2026-10-29.md`, les inventaires des interfaces du 29/10 (`docs/solver/INVENTAIRE_MOTEUR_GTO_2026-10-29.md`, `docs/exploitation/INVENTAIRE_TESTS_2026-10-29.md`, sur leurs branches) et le document de suivi partagé « SpinAcademy — suivi des actions et répartition ».

## 1. L'application aujourd'hui

| Domaine | Ce qui existe |
|---|---|
| **Mode GTO** | Banque `gto_preflop/2026.10.13-3` : décisions préflop de 2 à 25 BB, heads-up et 3 joueurs, tapis égaux et inégaux, une version par situation, mains mal résolues retirées. Séries tirées selon la fréquence réelle des situations. Les questions viennent des exports de la référence ; notre solveur ne produit encore aucune banque. |
| **Mode exploitant** | Banque `exploit_field/2026.10.23-1` (moteur v4.5) : 8000 questions de 4 à 25 BB, 12 situations, vilain inconnu, observé ou « pastille posée », questions « Défaut du vilain » et « Quelle pastille ? ». Profils : hypothèses des coachs, pas encore mesurées. |
| **Correction** | Verdict en BB, coût du choix, message essentiel, « À retenir », précisions repliées, grille 13 × 13, plan postflop, « Sur quoi ça repose » en exploitant, lien vers le conseiller. |
| **Table** | Comme au client de jeu : actions sous les joueurs, mises en BB, bouton D, pastilles de couleur réglables, stats du vilain sous son siège, chrono 15 s ou 8 s. |
| **Programme suivi** | Séance du jour de 15 minutes (révision, thème en 2 séries, range du jour), fixée pour la journée ; série de jours qui pardonne un jour par semaine ; recommandations (au plus 2) ; objectifs de la semaine modifiables ; 4 niveaux avec passage automatique et premier lancement en 3 écrans ; 6 défis et « Mes défis ». |
| **Outils** | « Construis ta range » (diagnostic trop serrée / trop large), conseiller préflop « Comment jouer ma main ? » (`/conseil`), « Ma progression » (score, BB perdus pour 100 décisions, thèmes, niveau, défis), révision espacée J+1 / J+3 / J+7, Lexique 1.12.2 (83 termes, mots expliqués au toucher). |
| **Signalements et administration** | « Signaler cette main », relecture et clôture dans `/admin` (jeton partagé), catalogue des datasets avec validation, reconstruction et publication. |
| **Exploitation** | API FastAPI et SQLite, limitation de débit, préchargement des banques, service worker (application ouverte hors ligne), déploiement, retour arrière et sauvegardes testés sur un serveur de test. Première question en 1 s en 4G simulée. |
| **Démo autonome** | Artefact [SpinAcademy v2](https://claude.ai/artifact/C5mfLsWqoeK55HEpKBYkHJ) : 6710 questions, progression dans le navigateur, mêmes règles que l'application (programme compris), signalements dans une base partagée. |
| **Qualité** | 141 tests automatiques ; 13 parcours navigateur (téléphone, bêta, hors ligne, séance, défis, objectifs, niveaux, recommandations, corrections du test 9). |

**Notes des testeurs** (sur 5) :

| Test | Date | Moyenne | Sujet principal |
|---|---|---|---|
| 1 | 23/10 | 3,5 | filtres perdus, seuils incohérents, jargon |
| 2 | 23/10 | 4,0 | après le lot A |
| 3 | 23/10 | 3,75 | correction allégée |
| 4 | 24/10 | 4,0 | table comme au client |
| 5 | 24/10 | 3,7 | ranges, chrono, BB perdus |
| 6 | 24-26/10 | 4,1 | corrections du test 5 |
| 7 | 28/10 | 4,0 | conseiller préflop |
| 8 | 29/10 | — | interrompu |
| 9 | 29/10 | 4,0 (accueil 3,2, défis 3,3) | programme de travail |

Les 24 problèmes du test 9 sont corrigés le 29/10, sauf un écart de pourcentages à reproduire (`RETEST9_JOUEURS_2026-10-29.md` §5). Ces corrections n'ont pas encore été testées par les joueurs.

## 2. Ce qui était prévu, et ce qui a été fait

### Lot A (avant le MVP)

| # | Prévu | État |
|---|---|---|
| A1 à A12 | Corrections du premier test (filtres, ordre des actions, barème, coût du choix, stratégie mixte, pièges, vocabulaire, progression, « Sur quoi ça repose », signalement, 4G, coupure réseau) | **Fait** le 23/10, puis complété par les corrections des tests 2 à 9. |
| A13 | Droits sur les données dérivées de la référence | **Réglé** le 26/10. |
| A14 | Politique de confidentialité, mentions légales, conditions d'utilisation, relecture d'un juriste | **Projet rédigé**, relecture à faire. |
| A15 | Hébergeur, production, sauvegardes externes, surveillance | **Procédure prête et testée**, production non installée. |
| A16 | Mode invité ou comptes | **À trancher** (recommandation : invité pour le MVP). |
| A17 | Journal d'usage anonyme de la bêta | **À trancher.** Sans lui, la rétention ne se mesure qu'à partir des tables existantes. |
| A18 | Relecture experte de l'échantillon du 14/10 | **À trancher.** |

### Lot B (rapidement après le MVP)

| # | Prévu | État |
|---|---|---|
| B1 | Exports de référence priorité 1, puis reconstruction des banques | **Commandés (v4), pas reçus.** La moyenne des exports répétés est en cours dans l'importeur (Moteur GTO). |
| B2 | Calibrer les profils sur un historique de mains réel | **Bloqué** : historique à fournir. |
| B3 | Comptes, synchronisation, administrateurs nominatifs | **À faire** (après A16). Le mode choisi est désormais gardé sur le serveur. |
| B4 | Offre gratuite / payante, paiement | **À faire** : contenu à définir. |
| B5 | Accueil en trois écrans, objectif du jour, série de jours | **Fait** (programme de travail, étapes 1 à 5, corrigé après le test 9). |
| B6 | Mode hors ligne | **En partie** : l'application s'ouvre et la progression s'affiche ; jouer une série demande le serveur. |
| B7 | Exploitant : open à 2 BB, SB face au limp du BTN, pots limpés à 3 | **Bloqué** par B1. |
| B8 | Pastille « Nit » renforcée, pastilles hors heads-up | **En partie** : pastilles à 3 joueurs à table ; « Quelle pastille ? » encore en heads-up. |
| B9 | Thème choisi dans l'application, deux colonnes sur grand écran, bilan cliquable | **À faire** (Interface, I5). |
| B10 | Ligne « bloqueurs », questions « quelle taille ? » | **À faire.** |
| B11 | Audit d'accessibilité (RGAA) | **À faire** (Interface, I6). |

### Lot C (plus tard)

C1 postflop, C2 ICM, C3 tapis inégaux à 3 joueurs et 3-bet non all-in, C4 calculs verrouillés par profil, C5 EV exacte à 3 joueurs, C6 base serveur, C7 conseils payants : **rien de commencé**. Le porteur du projet a décidé le 29/10 qu'à terme les banques GTO viendront de notre solveur, la référence servant à le caler : C3 et C5 deviennent des étapes de ce chantier (Moteur GTO, G4 et G5).

### Ajouts depuis le 24/10

| Ajout | Date |
|---|---|
| Corrections des tests 5 et 6 (ranges, chrono, BB perdus, pastilles) | 24-26/10 |
| Commande v4 des exports de référence (arbre unique, précision, tapis) | 26/10 |
| Conseiller préflop `/conseil`, puis corrections du test 7 | 28/10 |
| Analyse des écrans et écrans plus clairs (range corrigée, progression, correction, table, accueil) | 29/10 |
| Programme de travail, étapes 1 à 5 : séance du jour, recommandations, objectifs, niveaux, défis | 29/10 |
| Corrections du test 9 | 29/10 |
| Organisation en sept interfaces et document de suivi partagé | 29/10 |

## 3. Organisation du travail

Depuis le 29/10, sept interfaces Claude travaillent chacune sur son périmètre et sa branche. Le document de suivi partagé « SpinAcademy — suivi des actions et répartition » liste les 49 actions, leur responsable et leur état.

| Interface | Périmètre | Où elle en est (29/10) |
|---|---|---|
| Plan | Coordination, corrections des tests, démo, état des lieux | Corrections du test 9 faites |
| Moteur GTO | Notre solveur, qui doit produire les banques | Moyenne des exports répétés dans l'importeur |
| Moteur exploitant | Questions et corrections contre le field | Inventaire fait |
| Moteur profil | Profils adverses, pastilles, calibrage | Inventaire fait ; 3 incohérences à aligner |
| Défis et rétention | Mesure de la rétention, routine, partage, rappels | Inventaire fait |
| Interface | Écrans, style, accessibilité | Inventaire fait (23 éléments) |
| Tests | Stratégie de tests, non-régression, intégration continue | Inventaire fait ; la suite passe |

« Mes mains » (import de l'historique Winamax, démo du 28/10) reste hors de l'application jusqu'à nouvel ordre (décision du 29/10).

## 4. Ce qu'il reste à faire

### Avant la mise en ligne (bloquant)
1. **Juriste** (A14) : politique de confidentialité, mentions légales, conditions d'utilisation.
2. **Production** (A15) : hébergeur (4 Go de mémoire), domaine en HTTPS, jeton d'administration, sauvegardes externes, surveillance.
3. **Décisions** : invité ou comptes (A16), journal d'usage (A17), relecture experte (A18), nom définitif (SpinsAcademy ou SpinAcademy).

### Côté application, court terme
4. **Republier la démo** avec les corrections du test 9, puis **un dixième test joueurs** (Plan).
5. **Rétention** : indicateurs par cohortes, partage du défi du jour, séances de 5 et 30 minutes, test de placement (Défis et rétention).
6. **Interface** : remise à plat de `app.css`, écran « Profil et paramètres », grand écran, accessibilité, correction sur la table (Interface).
7. **Tests** : documentation à jour (`TESTS.md`, `ANOMALIES_CONNUES.md`), non-régression des bugs du lot 3, tests rapides / lents, tests automatiques sur GitHub (Tests).

### Côté données et moteurs
8. **Exports de référence v4** (choix A et B, pilote), puis reconstruction des banques ; ils débloquent B7 et la première banque issue du solveur.
9. **Notre solveur** : sortie au format des banques, écart sous le bruit de la référence sur deux situations, EV exacte à 3 joueurs (Moteur GTO).
10. **Historique de mains** pour calibrer les profils (B2) ; avant cela, aligner les profils des calculs verrouillés sur les 5 profils du moteur (Moteur profil) et durcir « Défaut du vilain » (Moteur exploitant).
11. **Relecture humaine** de la banque exploitante v4.5 par les coachs.
12. **Renommer les identifiants techniques** encore marqués du nom du solveur de référence (`data/hrc`, `tools/hrc`, `ev_hrc`), avec la prochaine version des banques.

### Ensuite
13. Lot B restant (comptes, offre et paiement, bloqueurs), puis lot C, à commencer par le postflop (C1).

## 5. Décisions attendues du porteur du projet

| Décision | Débloque |
|---|---|
| Historique de mains Expresso | calibrage des profils, rec passif face au limp, calculs verrouillés |
| Choix A et B de la commande v4, pilote | nouvelles banques, situations exploitantes manquantes, banque issue du solveur |
| A16 invité ou comptes | synchronisation entre appareils, classement du défi du jour |
| A17 journal d'usage | mesure propre de la rétention |
| Rappels (notification ou courriel) | rappels de séance |
| Mode exploitant dès le niveau 1 pour un joueur confirmé | parcours des niveaux |
| Limp des paires AA à JJ entre 5 et 10 BB | questions aujourd'hui exclues |
| Nom définitif | en-tête, manifeste, artefacts |
| Tests : réponses des coachs à rejouer, tests automatiques sur GitHub | non-régression |
| A14, A15, A18, B4 | mise en ligne et offre |
