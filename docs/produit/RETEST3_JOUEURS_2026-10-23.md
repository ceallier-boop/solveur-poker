# Troisième test joueurs (23/10/2026, correction allégée)

Version testée : correction « l'essentiel d'abord » (commit `8903563`), `exploit_field/2026.10.23-1`, banque GTO `2026.10.13-3`. Base de test séparée, aucun signalement envoyé. Six joueurs : les cinq habituels et Sofiane, régulier gagnant, qui découvre l'application.

## 1. Notes

| Joueur | Mode | Test 1 | Test 2 | Test 3 | Séries | L'essentiel a suffi |
|---|---|---|---|---|---|---|
| Mamadou | GTO, téléphone | 4 | 4 | 4 | 80 %, 90 % | 7 sur 10 |
| Léa | Exploitant, téléphone | 3 | 4 | 4 | 80 %, 60 % | 7 sur 10 |
| Kevin | GTO HU < 10 BB, clavier | 3,5 | 4 | 4 | 80 %, 90 % | — |
| Nadia | GTO, téléphone, débutante | 4 | 4,5 | 4 | 100 %, 80 % | 8 sur 10 |
| Jean-Pierre | Exploitant, face à un limp | 3 | 3,5 | 3,5 | 70 %, 90 % | 7 sur 10 |
| Sofiane (nouveau) | Exploitant puis GTO premier à parler | — | — | 3 | 80 %, 50 % | 7 sur 10 |

Moyenne des cinq habituels : 3,5 → 4,0 → 3,9. Avec Sofiane : 3,75.

## 2. Ce qui marche
- Le nouvel écran se lit en quelques secondes : verdict, message essentiel et « À retenir » tiennent sans défiler (Sofiane, Nadia).
- Les reproches du test 2 sont réglés : seuils, « joueurs derrière », « 0 % », 3 décimales, raccourcis sur téléphone, lexique, double appui, définition sous la phrase, barre rouge, plafond Imprécision contre un inconnu.
- Montants et barème justes, filtres gardés (Kevin).

## 3. Problèmes, par priorité

### Le message essentiel (à corriger en premier)
1. **Il explique le coup de référence, pas celui du joueur** quand son choix est accepté (stratégie mixte, bons coups, imprécision). Exemples : A7s complété, « Bonne réponse », message « Face à ton tapis, l'adversaire se couche environ 62 % » (Mamadou) ; J3o complété, « Ton choix fait partie des bons coups » puis « cette main gagne trop rarement » (Nadia) ; KTo, A7o limpés (Kevin).
2. **Vilain inconnu : toujours la même phrase**, « Inconnu = rec passif… Vole plus, paie plus serré », parfois contraire au bandeau (KK, « Le bon coup : Check ») (Jean-Pierre, Léa).
3. **Petit échantillon** : « Trop peu de coups pour conclure : joue le profil par défaut » ne dit ni quoi faire ni pourquoi (Léa).
4. **L'argument décisif manque** : tapis justifié par la fréquence de limp alors que c'est le fold à 84 % face au tapis qui décide (Jean-Pierre) ; « Il se couche trop face à une relance » alors que seule une stat de call est affichée (Sofiane).
5. **« À retenir » absent en exploitant** sur les 30 mains jouées (Léa, Jean-Pierre, Sofiane).
6. **La base du conseil est cachée** : le plafond (« coup théorique contre un inconnu ») et « Sur quoi ça repose » ne sont visibles qu'en dépliant (Jean-Pierre).
7. **Équité absente face à deux adversaires** ou quand un joueur reste à parler : « ta main gagne assez souvent pour le prix à payer » sans chiffre (Mamadou, Kevin).

### Justesse à vérifier
8. 83o au SB en heads-up à 4 BB donné Fold, avec 53s « à la limite » (Sofiane). À contrôler dans les données.
9. « Rapporte 0,14 BB de plus que la théorie (fold) » pour T5o (6 BB HU) et 76s (BTN 4 BB) (Sofiane).
10. « À retenir » de A8o à 15 BB (« tapis avec KQo, J9s+ ») qui n'inclut pas A8o alors que les précisions disent qu'elle en fait partie (Sofiane).
11. « Mains à la limite » qui changent d'une fois à l'autre sur le même spot ; « Relancer à 2 BB » proposé une fois sur deux (Kevin).
12. Équités de K7s et KTs (44-45 % contre des ranges de 11-12 %) à vérifier (Léa).

### Détails
- « Décision serrée » pour 0,5-0,6 BB d'écart (Kevin, Mamadou) ; 0,29 BB dans le bandeau, 0,28 BB dans les précisions (Jean-Pierre).
- « Potentiel de la main au flop » sur des coups joués à tapis (Mamadou, Nadia) ; phrase pro-check dans les précisions quand on conseille le tapis (Léa, Jean-Pierre).
- « sa range » face à deux adversaires ; « Compléter » et « Limper » pour le même coup ; carte « 10 » contre « T » (Mamadou, Sofiane, Léa).
- Bilan : « Référence : Fold (0,59 BB de moins) » ambigu, « (un peu moins de 0,1 BB de moins) », « Ces mains reviendront » pour une seule main (Léa, Nadia, Mamadou).
- Mots : « Action de référence », « initiative », « effectifs », noms de mains (87o, Q9s) non expliqués (Nadia).
- Le bouton « Question suivante », collé en bas, cache du contenu (Nadia).

### Attentes d'un régulier (Sofiane)
Ranges heads-up courtes fiables, saisie de ses propres stats sur un vilain, spots contre des réguliers ; en premier à parler, l'EV de chaque option et le pourcentage de la stratégie mixte (Kevin).

## 4. Proposition
Un lot court sur le message essentiel (points 1 à 7) : il doit parler du coup du joueur quand il est accepté, donner l'argument décisif chiffré et ramener « À retenir » en exploitant. Les points 8 à 12 se vérifient dans les données avant toute correction.
