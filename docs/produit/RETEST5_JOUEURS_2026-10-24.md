# Cinquième test joueurs (24/10/2026) : ranges, chrono, BB perdus

Version testée : chantiers 2 et 5 (`08fd6d8`), pastilles à table et alternance. Base de test séparée, aucun signalement envoyé.

## 1. Notes

| Joueur | Test 4 | Test 5 | Séries | Ranges (mains bien classées) |
|---|---|---|---|---|
| Mamadou | 4,5 | 4 | 4,5 · 5 · 4 (chrono 15 s) · 4 | 5 ranges, 94 % |
| Léa | 4 | 4 | 3 · 4 · 4 (chrono 8 s) | 66 → 86 → 93 → 96 % |
| Kevin | 4 | 3,5 | 3 · 5 · 5 (chrono 8 s) | 7 ranges, 95 % |
| Nadia | 4 | 4 | 3,5 · 5 · 4 (chrono 8 s) | 72 → 73 → 75 → 89 % |
| Jean-Pierre | 3,5 | 3,5 | 4 · 3 · 1,5 (chrono 8 s) | 96 · 88 · 95 · 100 % |
| Sofiane | 4 | 3 | 4 · 3 (chrono 8 s) · 3 | 92 · 85 · 84 · 78 · 100 % |

Moyenne : 4,0 → **3,7**. Les nouveautés plaisent dans leur principe, mais l'exercice de range a des défauts visibles qui font douter de la référence.

## 2. Ce qui plaît
- **BB perdus pour 100 décisions** : l'indicateur préféré de Jean-Pierre et de Léa (« le seul chiffre qui montre qu'une série à 4/5 a coûté plus que celle à 3/5 ») ; compris par la débutante grâce à « plus c'est bas, mieux c'est » ; calculs vérifiés (Kevin, Sofiane).
- **Ranges** : on voit tout de suite qu'on dessine trop large (Léa : « 53 mains en trop ») ; les coûts en BB par main classent les fautes (Jean-Pierre : « J9s 0,2 BB contre K6s 0,05 ») ; classement et coûts justes d'après le calcul de Kevin ; grille comprise en 10 secondes (Nadia) ; glisser au doigt et à la souris fluide.
- **Chrono** : bien réalisé (fold ou check automatique) ; Sofiane le valide.
- **Messages essentiels chiffrés**, base du conseil affichée, stats avec théorie et échantillon (Jean-Pierre) ; « Failed to fetch » disparu (Mamadou).

## 3. Problèmes

### Exercice de range (à corriger en premier)
1. **Cases grisées à tort** (les six) : « Main qui n'arrive pas à cette décision » sur des mains qui y arrivent (88, AQs, AA… au SB premier à parler). Ce sont les mains dont la référence change d'un arbre de calcul à l'autre, écartées des questions. Elles révèlent la réponse et faussent les pourcentages.
2. **Trois pourcentages qui ne concordent pas** : « Ta range » sous la grille et dans le résultat (49 % contre 53 %), « référence » et « À retenir » (62 % contre 60 %) (Kevin, Nadia, Léa, Mamadou).
3. **La question cache les autres coups** : « Avec quelles mains pousses-tu à tapis ? » alors que la référence limpe ou relance AA–TT ; « AA jouée à tort » sans dire quoi jouer à la place (Sofiane, Léa, Nadia, Mamadou).
4. **Peu de variété** : souvent la même situation (SB heads-up à 4 BB, 3 fois sur 4 chez Léa, 3 sur 5 chez Mamadou) ; « Nouvelle range » ressort la même ; environ 8 situations avec des filtres étroits (Kevin).
5. **Règle « À retenir » contredite par la grille** (« A2o+, 76s » alors que 22–55 sont à jouer et 76s mixte) (Jean-Pierre).
6. Hachuré « mixte » presque invisible sur téléphone ; main mixte choisie hors légende ; toucher une case après la correction n'affiche rien (Nadia). « 53s jouée à tort : 0 BB perdus » (Kevin). Cases d'environ 26 px (Mamadou).
7. À vérifier : références de Sofiane jugées fausses en pratique (« TT jouée à tort » à 10 BB, 74 % à 4 BB contre environ 90 % en push/fold pur) : effet du limp et de la petite relance disponibles dans l'arbre, à dire dans la question (point 3).

### Chrono
8. **Un fold automatique est compté « Bonne réponse »** quand il tombe sur le bon coup (les six).
9. Le bilan et la progression ne disent pas qu'un coup a été joué au temps (AA couché automatiquement chez Mamadou, qui fait l'essentiel de ses BB perdus). 8 s est trop court pour une débutante (Nadia).

### BB perdus
10. Le bilan de série dit « t'a coûté X BB », pas « pour 100 décisions » (Sofiane, Léa) ; sur 15 décisions, le chiffre est du bruit : mentionner l'échantillon faible (Kevin).

### Pastilles et textes
11. **La pastille ne sert pas dans la correction** : « Sur quoi ça repose » cite le profil par défaut alors qu'une pastille Nit ou Calling station est posée (Sofiane, Léa, Jean-Pierre).
12. Alternance peu visible (4 « Pastille posée » d'affilée) ; une question « Pastille posée » affiche quand même toutes les stats (Léa, Sofiane).
13. **KK contre un vilain qui limpe peu** : « checke tes mains moyennes » revient (la règle corrigée ne couvre pas tous les coups) ; « À retenir » contre un inconnu toujours identique (Jean-Pierre, Léa).
14. Arrondis : barres à 43,5 % contre 44 % dans le texte ; énoncé 38 % contre 36 % en correction (Léa, Sofiane).
15. Pot total de la table différent du pot de la correction quand un tapis couvre (46 BB contre 30 BB) ; bouton « ALL-IN 35 BB » pour 15 BB effectifs (Léa, Mamadou).
16. Équité de la main toujours absente quand un joueur reste à parler ; « Contre sa range » face à deux adversaires (Mamadou).
17. Notation « 22+, A2s+ » absente du lexique (Nadia).

## 4. Proposition
- **Ranges** (1 à 6) : ne plus griser (toutes les mains en jeu à classer, celles à référence instable comptées comme mixtes), un seul calcul de pourcentage partout, question qui annonce les autres coups (« Les autres mains limpent, relancent ou se couchent »), correction qui dit le bon coup de chaque erreur, tirage varié (pas deux fois la même situation, familles et tapis à parts égales), règle « À retenir » vérifiée contre la grille, hachuré plus marqué.
- **Chrono** (8, 9) : un coup joué au temps compte comme une erreur de temps (zéro point, sans BB perdus si c'était le bon coup ?) : décision à prendre ; mention dans le bilan ; 15 s par défaut.
- **Pastilles** (11, 12) : la correction s'appuie sur la pastille posée ; stats réduites quand la pastille est posée ; alternance équilibrée dans une série.
- **Textes et chiffres** (10, 13 à 17).
