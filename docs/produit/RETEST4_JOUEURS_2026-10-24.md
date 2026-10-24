# Quatrième test joueurs (24/10/2026, table comme au client)

Version testée : lot 1 (table et actions comme au client de jeu, pastilles), progression hors connexion (commits `fb40a5d` à `849fa21`). Base de test séparée, aucun signalement envoyé.

## 1. Notes

| Joueur | Mode | Test 2 | Test 3 | Test 4 | Séries |
|---|---|---|---|---|---|
| Mamadou | GTO, téléphone | 4 | 4 | **4,5** | 100 %, 80 % |
| Léa | Exploitant, téléphone | 4 | 4 | 4 | 40 %, 60 % |
| Kevin | GTO HU < 10 BB, clavier | 4 | 4 | 4 | 90 %, 100 % |
| Nadia | GTO, téléphone, débutante | 4,5 | 4 | 4 | 60 %, 90 % |
| Jean-Pierre | Exploitant, face à un limp | 3,5 | 3,5 | 3,5 | 90 %, 100 % |
| Sofiane | Exploitant, puis lecture du vilain | — | 3 | **4** | 80 %, 100 % |

Moyenne des six : 3,75 → **4,0**.

## 2. Ce qui marche
- La table se lit d'un coup d'œil, « comme Winamax » : action sous les sièges, joueur couché grisé, bouton D, mises en jaune, Pot total, cartes en bas (tous).
- Les mots du client (FOLD, CALL, RAISE TO, ALL-IN) sont plus clairs que « Payer / Compléter », même pour la débutante ; le lexique les explique (Nadia).
- Montants, mises, Pot total et raccourcis clavier justes (Kevin).
- Progression hors connexion : affichée et datée chez les six.
- Pastilles claires ; le choix de couleur est gardé (Nadia, Sofiane, Mamadou).
- Le message essentiel parle maintenant du coup joué quand il est accepté (Mamadou).

## 3. Problèmes

### Table (petites corrections)
1. **Ta propre action n'est pas affichée sous ton siège** (« Tu limpes », « Tu relances à 2 BB ») ; on ne voit qu'un chiffre (Nadia, Sofiane).
2. **Ta mise est posée à gauche, pas devant toi** : on la croit au BTN couché (Jean-Pierre, Léa, Mamadou).
3. **Le tapis restant est en jaune comme les mises** (Sofiane, Nadia).
4. **Ligne de stats sous le siège** : elle déborde sur 3 ou 4 lignes avec deux stats ; ni théorie, ni échantillon ; arrondi 13 % contre 12 % dans l'énoncé (Léa, Jean-Pierre).
5. **Bouton D** : en heads-up, quand tu es SB, il flotte à droite du pot (Kevin).
6. **ALL-IN** : le bouton affiche le tapis effectif (4 BB) et non ton tapis (8 BB), contrairement au lexique ; un SB qui couvre est affiché ALL-IN avec 40 BB restants (Kevin, Nadia, Mamadou).
7. Cartes « 10 » contre « T » dans le texte ; pastille collée au mot (« SCalling station ») ; couleurs lues par leur code (« #30a46c ») par un lecteur d'écran (Sofiane, Nadia).

### Correction
8. **Libellés différents des boutons** : « Fold », « Call 14,5 BB », « raise to » contre FOLD, CALL, RAISE TO ; « Tu complètes », « limp » restent dans les textes (Mamadou, Léa, Nadia, Sofiane).
9. **Phrases toutes faites répétées** : « Inconnu = rec passif… Vole plus, paie plus serré » (5 fois sur 10 chez Jean-Pierre), « Il pousse peu : son tapis est fort… » (3 fois chez Léa).
10. **« À retenir » presque absent** : 1 main sur 10 (Kevin, Léa).
11. **Équité de la main absente** quand un joueur reste à parler (22 au SB, BB derrière) (Mamadou).
12. **« Autre option »** cite des coups perdants, parfois pires que l'erreur du joueur (Nadia).
13. **AA contre un vilain qui limpe peu** : « checke tes mains moyennes », et le plan postflop dit « il paie trop » alors qu'il a payé 2 tapis sur 22 (Jean-Pierre).
14. **Le fold face à l'iso, qui décide la main**, n'est visible que dans les précisions (Léa) ; « Sur quoi ça repose » toujours en dernier (Jean-Pierre).
15. « Action de référence » et « Référence : … (0,2 BB de moins) » dans le bilan restent obscurs (Nadia, Mamadou).

### Données (à vérifier)
16. **Même spot, deux versions** : BB face au limp du SB à 8/8 BB, relance à 3 BB une fois, à 2 BB l'autre, avec des pourcentages et des mains à la limite différents (Kevin). « Mains à la limite » qui changent d'un tirage à l'autre sur le même spot (Kevin). TT « à la limite » du tapis (Nadia).
17. SB à 25 BB sans limp ni tapis proposés (Sofiane).

### Divers
18. Sans réseau, « Série recommandée » affiche « Failed to fetch » en anglais (Mamadou).
19. Mode et filtre oubliés après rechargement (Jean-Pierre).
20. Peu de questions « Quelle pastille ? » (1 sur 5 en lecture du vilain) ; les « Défaut du vilain » sont trop faciles (Sofiane).
21. Raccourcis clavier vus sur téléphone par Sofiane ; Mamadou l'attribue à l'outil de test (émulation tactile perdue après rechargement) : à vérifier sur un vrai téléphone.

## 4. Proposition
- Lot court d'affichage : points 1 à 8, 18 et 19 (table, libellés, message hors ligne, mémoire du mode).
- Lot de textes : points 9 à 15 (phrases variées et ciblées, « À retenir » en exploitant, équité, « Autre option »).
- Vérification de données : points 16 et 17, avant toute correction.

## 5. Corrections faites (24/10/2026)

| Point | Correction |
|---|---|
| 1, 2 | Ton action s'affiche sous ton siège ; ta mise est posée devant toi, au-dessus de tes cartes. |
| 3 | Tapis restant en blanc, le jaune est réservé aux mises. |
| 4 | Ligne de stats : une ligne par stat, avec la théorie et l'échantillon (« Limp 13 % · th. 8 % · 10/80 »), arrondi identique à l'énoncé. |
| 5 | Bouton D placé à côté de ton siège quand tu as le bouton. |
| 6 | ALL-IN affiche ton tapis ; un adversaire qui te couvre est marqué « ALL-IN · te couvre ». |
| 7 | Pastille séparée du mot ; couleurs nommées en français pour les lecteurs d'écran ; mot souligné qui ne se coupe plus après l'apostrophe. Les cartes gardent « 10 », comme au client. |
| 8 | Mêmes libellés partout en capitales (FOLD, CALL 0,5 BB, RAISE TO 2,3 BB, ALL-IN 8 BB) ; un seul mot pour le limp dans les textes (« limper »). |
| 9, 13, 14 | Exploitant : le message essentiel donne le chiffre qui décide la main et le coup à jouer (« Face à ton tapis, il se couche 75 % du temps, et payé, T5o a 26 % d'équité. Pousse. ») ; 320 messages différents sur 381 mains tirées, contre 28 avant. Règles corrigées pour AA contre un vilain qui limpe peu ; plan postflop sans « il paie trop ». « Sur quoi ça repose » en tête des précisions. |
| 10 | « À retenir » sur chaque main, dans les deux modes. |
| 12 | « Autre option » seulement pour une vraie alternative (moins de 0,1 BB d'écart). |
| 15 | « Meilleur coup » au lieu de « Action de référence » ; bilan : « Ton coup : X (coûte 0,2 BB) · Meilleur coup : Y ». |
| 16 | GTO : une seule version par situation (arbre de référence, sinon le plus fréquent à ces tapis) ; 1458 situations servies au lieu de 1927 doublons compris. La démo passe à 6710 questions (2,6 Mo). |
| 18 | Sans réseau, « Série recommandée » dit « Pas de réseau… » au lieu de « Failed to fetch ». |
| 19 | Mode et thème gardés après un rechargement. |
| 20 | Lecture du vilain : « Quelle pastille ? » aussi souvent que « Défaut du vilain » (48 % contre 17 %). |

Non traités : équité de ta main quand un joueur reste à parler (11) ; SB à 25 BB sans limp ni tapis (17, limite des arbres de calcul) ; raccourcis vus sur téléphone (21, attribués à l'outil de test). Vérifié et sans erreur : l'équité élevée de T8s ou K7s contre un petit tapis du BTN à 18 BB (ses tapis sont surtout des mains moyennes, il relance ses grosses mains).
