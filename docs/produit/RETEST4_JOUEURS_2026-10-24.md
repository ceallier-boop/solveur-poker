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
