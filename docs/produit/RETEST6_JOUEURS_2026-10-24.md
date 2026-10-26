# Sixième test joueurs (24-26/10/2026) : corrections du test 5

Version testée : `22babea` (corrections du test 5). Base de test séparée, aucun signalement envoyé. Le test a d'abord été bloqué : la base de test neuve n'avait aucune banque publiée (voir problème 1) ; les deux banques y ont été contrôlées et publiées, puis le test a été refait en entier.

## 1. Notes

| Joueur | Test 5 | Test 6 | Séries | Ranges (mains bien classées) |
|---|---|---|---|---|
| Mamadou | 4 | 4 | 4 · 5 · 4 (chrono 15 s) | 97 · 97,3 · 98 · 82,7 % |
| Léa | 4 | **4,5** | 3 · 4 · 4 (chrono 8 s) | 76,3 · 90,6 · 83,3 · 89 % |
| Kevin | 3,5 | **4** | 4 · 5 · 4 (chrono 8 s) | 6 ranges, 77,7 à 92,8 % |
| Nadia | 4 | **4,5** | 4 · 4 · 2 (chrono 15 s) | 92,2 · 79,5 · 97 % |
| Jean-Pierre | 3,5 | **4** | 2 · 2 · 4 (chrono 8 s) | 87,6 · 85,8 · 95,9 · 93,5 % |
| Sofiane | 3 | **3,5** | GTO 4,5 ; exploitant au chrono 8 s joué par un script | 84,5 à 97,7 % |

Moyenne : 3,7 → **4,1**, la meilleure depuis le début. Personne ne baisse. Les corrections du test 5 tiennent presque toutes ; ce qui retient les réguliers, c'est la référence des ranges, jugée bruitée, et quelques incohérences de chiffres.

## 2. Corrections du test 5 vérifiées

| Correction | Verdict |
|---|---|
| Pourcentages de range identiques partout | **Tient** (recalculé case par case par Kevin sur 6 ranges, et par Léa) |
| Question qui dit ce que font les autres mains, coup de la référence pour chaque erreur | **Tient** (les six) |
| Situations de range variées | **Tient** (4 à 6 situations différentes par joueur) |
| Hachuré mixte, case touchée expliquée, plus de « 0 BB perdus » | **Tient** (Nadia, Mamadou, Jean-Pierre) |
| Coup joué au temps = erreur, mentionné dans le bilan et la progression ; chrono 15 s par défaut | **Tient** (les six) ; Mamadou : « 15 s m'oblige à connaître mes ranges » |
| BB perdus pour 100 décisions dans le bilan | **Tient**, mais « échantillon faible » n'est que dans « Ma progression » (problème 3) |
| Correction appuyée sur la pastille, alternance | **Tient** (Léa, Jean-Pierre) ; stats repliées plutôt que masquées (Léa) |
| KK / AA contre un vilain qui limpe peu : checker pour piéger | **Tient** (Jean-Pierre) |
| « Contre leurs ranges », lexique 22+ / A2s+ | **Tient** ; « A2+ » écrit dans « À retenir » absent du lexique (Nadia) |
| Plus de cases grisées à tort | **Pas tout à fait** : un cas trouvé par Kevin (problème 4) |

## 3. Problèmes

### Bloquant pour l'exploitation
1. **Message d'erreur trompeur** (les six) : quand aucune banque n'est publiée, l'application dit « Le serveur ne répond pas… réessaie dans un instant » alors que le serveur répond 503 avec la cause. « Construis ta range » ne réagit pas et « Ma progression » s'ouvre vide, sans message (Nadia).

### Ranges
2. **Référence jugée bruitée** (Sofiane, Jean-Pierre, Kevin) : AJs paie le tapis mais AJo pousse à 89 % ; 55 pousse et 77 paie ; en heads-up à 20 BB, 42s et 92o relancent mais KQs et JTs limpent ; 95s, 86o, 52s à jouer mais 76s, 87s à laisser ; K3o à tapis mais KJo sanctionnée. Aucune explication de la polarisation (relances avec des mains faibles, limps avec les fortes). À vérifier : défaut de l'arbre de référence, ou stratégie réelle à expliquer.
3. **« Mixte » hors de la règle 25-75 %** (Kevin, Nadia, Léa, Mamadou) : « K7o : mixte … 97 % », 66 à 10 %, ATo à 8 %, AA à 5 % ; à l'inverse QQ « jouée à tort » alors qu'AA, KK, JJ sont mixtes, et ATs en erreur à 19 % alors qu'A9s est mixte. Cause probable : la règle « erreur de moins de 0,01 BB comptée comme mixte » affiche « mixte » avec une fréquence qui contredit la légende.
4. **Case grisée à tort** (Kevin, SB limpe puis relance du BB) : ATs grisée alors que la SB la limpe environ 81 % du temps dans une autre range.
5. **« À retenir » contredit la grille** : « J9s+ (environ 7 %) » puis « A6s en fait partie » (Mamadou) ; « A2+ » mais A7s à la limite (Nadia) ; « 20 BB » au lieu de 10 BB effectifs (Nadia) ; des « mains à la limite pour FOLD » font partie de la range de jeu affichée juste au-dessus (Mamadou).
6. Textes : « 6 oubliées » mais 5 listées (Mamadou) ; « 22 : à laisser : bien vu. La référence la pousse à tapis » se lit comme « se coucher » (Nadia) ; « 97,7 % de mains bien classées » jugé flatteur avec 6 erreurs (Sofiane). Cases de 25,7 px sur téléphone (Mamadou).

### Chiffres et bilan
7. **« Échantillon faible » absent du bilan de série** (Mamadou, Jean-Pierre, Sofiane, Nadia, Kevin).
8. Arrondis : 0,36 + 0,17 affiché « 0,54 BB » (Léa) ; 0,35 BB en correction contre 0,36 BB au bilan (Mamadou) ; 75,0 % contre 75 % (Léa).
9. Verdict : 0,76 BB « Décision serrée » et 0,77 BB « Erreur » dans la même série (Kevin, effet du seuil « coup jouable ») ; « Plusieurs bonnes décisions : ALL-IN ou CALL » avec CALL à 0 % (Sofiane).

### Exploitant
10. « Il limpe beaucoup : son limp est faible, pousse plus large » sur 6 mains, y compris contre un vilain à 13 % de limp, alors que c'est son fold au tapis qui décide (Jean-Pierre).
11. « Son écart de stats » écrit alors qu'une pastille est posée (Jean-Pierre).
12. Pastille Dégène : se couche plus que la théorie face au tapis (81 % contre 78 %), posée sur un joueur qui limpe moins que la théorie (Jean-Pierre, Sofiane) ; énoncé 42 % contre 35 % en correction (Léa).
13. KK : « son limp est fort » contre « il se couche 69 % face à une iso » (Jean-Pierre).
14. Dénominateur : « Sur 120 occasions… 41 fois (45 %) » alors que 45 % = 41 sur 91 (Léa).
15. Textes hors situation : « trop petit pour checker » au BTN premier à parler ; « Piège » sur des relances standard ; « tout le monde se couche » en heads-up (Léa).

### Tirage des séries
16. Répétitions : 7♠6♠ deux fois en 15 mains (Léa), A9o face à un limp à 8 BB revenue à l'identique (Kevin), JJ en ouverture de deux séries recommandées de suite (Sofiane) ; 8 questions sur 15 face à un tapis (Kevin).
17. Explication de KQo relancée (bonne réponse) qui parle du limp (Nadia) ; un joueur à tapis affiche encore des jetons devant lui (Mamadou).

## 4. Proposition
- **Tout de suite** (1, 3, 5 à 9) : message d'erreur exact selon la réponse du serveur ; « mixte » réservé à 25-75 % et les erreurs bon marché dites « erreur sans coût réel » plutôt que « mixte » ; « À retenir » sans liste de mains ou avec la liste exacte ; tapis effectif dans « À retenir » ; « échantillon faible » dans le bilan ; une seule règle d'arrondi pour les BB.
- **À vérifier dans les données** (2, 4, 12) : bruit des ranges de référence (arbres à 20 BB heads-up, bluffs) ; reach de la case grisée ; calibration de la pastille Dégène.
- **Textes exploitants** (10, 11, 13 à 15) et **tirage** (16 : pas deux fois la même main dans une série, ni en ouverture de deux séries de suite ; plafonner les questions face à un tapis).
