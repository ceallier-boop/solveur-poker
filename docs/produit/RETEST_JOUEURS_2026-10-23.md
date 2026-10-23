# Second test des 5 joueurs (23/10/2026, après le lot A1–A12)

Version testée : `exploit_field/2026.10.23-1` (moteur 4.5) et la banque GTO nettoyée. Base de test séparée : aucun signalement n'a été écrit dans la vraie base.

## 1. Notes

| Joueur | Profil | Mode | Note avant | Note après | Scores des séries |
|---|---|---|---|---|---|
| Mamadou | 58 ans, prudent, téléphone | GTO | 4 | 4 | 80 % puis 70 % |
| Léa | joueuse régulière | Exploitant | 3 | 4 | 80 % puis 100 % |
| Kevin | grinder | Exploitant / GTO | 3,5 | 4 | 80 % puis 80 % |
| Nadia | débutante | GTO | 4 | 4,5 | 60 % puis 40 % |
| Jean-Pierre | 67 ans, ancien du live, méfiant | Exploitant, « Face à un limp » | 3 | 3,5 | 40 % puis 60 % |

Moyenne : 3,5 → 4,0.

## 2. Ce qui est réglé (constaté par les joueurs)
- Imprécision au lieu d'Erreur pour les petits écarts ; la phrase « au-delà de 0,06 BB : erreur » a disparu (Mamadou).
- « Nouvelle série » garde le filtre choisi (Jean-Pierre).
- « Taux lissé » a disparu de la Progression ; « encore N questions pour un score » est compris (Jean-Pierre, Mamadou).
- « Sur quoi ça repose » dit franchement que le profil par défaut n'est pas encore mesuré sur des mains réelles (Jean-Pierre).
- Le « Pourquoi ? » chiffré face à un tapis (équité contre équité requise) est apprécié de tous.
- Les mots expliqués au toucher et le lexique sont utilisés (Nadia, Mamadou).

## 3. Incident pendant le test
Le serveur a été tué par manque de mémoire (13 Go) quand plusieurs joueurs ont démarré en même temps : chaque requête chargeait le dataset en parallèle. Corrigé et poussé : un seul chargement par version (verrou) et préchargement au démarrage. Mesure : 566 Mo en pointe pour 10 sessions simultanées à froid. L'app a alors affiché « Connexion perdue … vérifie ta connexion », ce qui met la faute sur le joueur alors que le serveur était en cause.

## 4. Nouveaux problèmes, par priorité

### Contradictions dans la correction (à corriger avant la MVP)
1. **La leçon contredit le verdict** : 75s à 8 BB en HU, « À retenir : pousse plus large » alors que le tapis est noté Erreur et que le meilleur coup est Relancer à 3 BB (Jean-Pierre). « D'où plus d'agressivité » avec Check comme réponse (Jean-Pierre).
2. **« Aussi pertinente » à côté de « 0 % » dans la stratégie**, avec deux seuils (0,06 et 0,1 BB) dans la même boîte (Mamadou). Un coup « aussi pertinent » noté Imprécision et envoyé en révision (Kevin).
3. **La phrase générique « Des joueurs parlent encore derrière : payée, la main gagne trop rarement »** apparaît au BTN premier à parler, au SB face au BB seul et en HU (Mamadou, Kevin).
4. **La ligne postflop ne suit pas le coup** : « tu checkes son limp » quand il faut relancer ou pousser, « il checke derrière ton limp » après une relance (Léa, Jean-Pierre).
5. **Pourcentages différents dans une même correction** (32 % puis 33 %) et montants à 3 décimales (Mamadou, Kevin, Léa).
6. **Grammaire des lectures** : « Il semble ouvre trop souvent », avec un chiffre qui dit l'inverse (Léa). « Il se couche environ 0 % : tu prends le pot » (Kevin).
7. **« Écart de stats trop petit pour changer de taille »** alors qu'une seule taille est proposée (Jean-Pierre).

### Confiance dans le mode exploitant
8. Des écarts de 0,26 à 0,34 BB, venant seulement du profil par défaut non mesuré, sont notés Erreur alors que le joueur a joué le coup théorique (Jean-Pierre). Piste : contre un vilain inconnu, plafonner à Imprécision quand le coup joué est le coup HRC.
9. « Sur quoi ça repose » cite le total d'occasions (150) au lieu de l'échantillon décisif (« 7 sur 40 »), et ne dit pas quand une stat vient seulement du profil (fold face à l'iso) (Jean-Pierre). Le bloc revient sur presque toutes les mains (Léa).
10. Un même spot change d'arbre : l'option « Relancer à 2 BB » est présente ou absente (Kevin).

### Interface
11. Raccourcis clavier affichés sur téléphone dès la 2e question (Mamadou, Léa).
12. Note interne visible en pied du lexique : « À faire relire par un expert poker », « chip EV » (Mamadou, Nadia).
13. La définition s'insère au milieu de la phrase et la coupe (Mamadou, Nadia).
14. Un double appui pendant le redémarrage a mélangé deux séries (question K9o, correction KJs) (Léa).
15. L'accueil annonce « révision de tes erreurs (4 mains) » quand il y a 1 Erreur et 3 Imprécisions (Mamadou). Une série notée « Erreur » commence par « Plusieurs bonnes décisions » ; la barre est rouge à 50 % (Nadia).
16. La Progression désigne un « thème le plus fragile » sur 4 questions (Jean-Pierre) ou propose le heads-up quand tous les thèmes sont à 80 % (Kevin).
17. « Connexion perdue » pour une erreur serveur : distinguer réseau et serveur.
18. Mots encore difficiles : « Action de référence », « 12 BB effectifs », « règle simplifiée à 99 % », « A5s+/Jx », « abattage », règles « R9 / R12 » affichées (Nadia, Jean-Pierre).

### À faire vérifier par les coachs
- K8o au BTN à 15 BB à 3 joueurs (SB 50, BB 10) donné Fold 100 % (Mamadou).
- 66 à 6 BB en HU, BB face au limp : HRC check à 89 % (Jean-Pierre).
- La question d'identification du vilain n'est jamais sortie en 20 mains (Léa) : c'est attendu avec MAX_READ = 1 et 5 % de part, mais à revoir.

## 5. Proposition
Un lot A' (avant la MVP) pour les points 1 à 7, 11 à 15 et 17 : surtout des textes et de petites corrections d'interface. Les points 8 à 10 touchent le barème exploitant et demandent une décision : plafonner à Imprécision quand le coup joué est le coup HRC contre un vilain inconnu.

## 6. Lot A' (fait le 23/10/2026)

Décision du porteur du projet : contre un vilain inconnu, le coup théorique est au pire une Imprécision. Demande ajoutée : aucune mention de HRC ni des coachs dans ce que voit le joueur.

| Point | Correction |
|---|---|
| 1 | La leçon suit le meilleur coup (R13 + relance : « une petite relance suffit ») ; « D'où plus d'agressivité » seulement si le meilleur coup attaque. |
| 2 | Nuance : « coûte moins de 0,1 BB : coup jouable, même si la théorie ne le choisit pas ». Une seule limite du barème par correction (0,06 ou 0,1 BB selon le coup), y compris pour l'Erreur (« Plus de X BB d'écart : c'est une erreur »). |
| 3 | Fold : « Avec le BB / deux joueurs encore à parler… », selon la situation (premier à parler, face à un limp, face à une mise). |
| 4 | « Gérer le postflop » seulement quand le meilleur coup mène au flop (check, limp, call) ; textes propres à l'ouverture du BTN ; plan sans « AA ou KK » avec une autre main. |
| 5 | « À retenir » reprend le même pourcentage que le pourquoi ; jamais 3 décimales (« un peu plus de 0,06 BB » près d'une limite). |
| 6 | Petit échantillon décrit à partir de la stat affichée (sens et chiffres) ; « il ne se couche presque jamais » au lieu de « 0 % : tu prends le pot » (exploitant et GTO). |
| 7 | Piège avec relance : « trop petit pour checker ou pousser à la place ». |
| 8 | Plafond Imprécision pour le coup théorique contre un inconnu, avec la phrase « l'écart vient du profil supposé ». |
| 11 | Raccourcis clavier masqués sur écran tactile. |
| 12 | Pied du lexique sans note interne ; lexique 1.8.0. |
| 13 | La définition s'affiche sous la phrase, chaque phrase de l'explication sur sa ligne. |
| 14 | Un double appui sur « Nouvelle série » ne crée qu'une série. |
| 15 | « Revoir mes mains » ; le bilan marque chaque main « Erreur » ou « Imprécision » ; « Les bons coups ici : … Ton choix n'en fait pas partie » quand le choix est mauvais ; barre rouge sous 40 %, orange de 40 à 60 %. |
| 17 | Panne serveur (5xx) : « Le serveur ne répond pas… Ce n'est pas ta connexion », avec « Réessayer » ; hors ligne : « Pas de réseau ». |
| HRC, coachs | « En théorie », « Gain par rapport au fold (ajusté à ce vilain) », lexique « Solveur » sans marque, « profil de départ » au lieu de « établi avec des joueurs professionnels », `ev_source` servi : `solveur`. Contrôle : `tests/test_lot_a_prime.py` et la démo autonome (0 occurrence). |

Restent internes (non servis au joueur) : noms de fichiers et de champs du code (`ev_hrc`, `data/hrc`), documentation, pages d'administration, champs internes des datasets publiés (immuables ; une prochaine version du moteur pourra les renommer).
Non traités dans ce lot : points 9, 10, 16 et 18, et les trois vérifications des coachs.

## 7. Correction allégée (retour du porteur du projet, 23/10/2026)

« Les réponses sont encore trop chargées » : l'écran de correction montre d'abord l'essentiel, puis les précisions, repliées.

1. **Bandeau** : le verdict et une seule ligne, « Le bon coup : Check. Ton choix coûte 0,17 BB. »
2. **Message essentiel** : une phrase en gras. En GTO, le principe du coup ; pour payer un tapis, « Il te faut 45 % d'équité pour payer, et Q5o en a 40,5 % : couche-toi. » En exploitant, la leçon contre ce vilain (« Il pousse trop : paie plus large. »).
3. **À retenir** (GTO, après une erreur ou une imprécision ; questions de lecture) : la règle, dans un encadré.
4. **Précisions** (replié) : gain par rapport au fold, barème, nuance, chiffres du pourquoi, sur quoi ça repose, stratégie de référence ou tableau du vilain.

L'API ajoute `essential_fr`, `remember_fr` et `details_fr` ; `explanation_fr` reste complet (administration, signalements). Les chiffres estimés du vilain sont dits comme tels (« Estimation retenue (ses coups et le profil) »), pour ne pas les confondre avec sa stat observée. Le numéro de règle (R12…) n'est plus affiché.
