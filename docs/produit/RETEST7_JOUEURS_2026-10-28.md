# Septième test joueurs (28/10/2026) : conseiller préflop « Comment jouer ma main ? »

Version testée : `b0bc8de` (conseiller préflop `/conseil`, ajouté par le porteur du projet, sur la base des corrections du test 6). Base de test séparée, banques publiées, aucun signalement envoyé. Test interrompu une fois par la limite d'utilisation, puis repris.

## 1. Notes

| Joueur | Test 6 | Application | Conseiller seul | Consultations | Séries | Ranges |
|---|---|---|---|---|---|---|
| Mamadou | 4 | 4 | 3,5 | 11 | 3 · 4 (+ 2 en « face à un tapis ») | 76,3 · 82,5 % |
| Léa | 4,5 | 4 | 3 | 16 | 4 · 4 (exploitant) | 86,7 · 99,4 % |
| Kevin | 4 | 4 | 3 | 20 | 3 · 5 | 95,5 · 79,5 % |
| Nadia | 4,5 | 4 | 3,5 | 12 | 3,5 · 3 · 3,5 · 3 | 85,5 · 81,6 % |
| Jean-Pierre | 4 | 4 | 3,5 | 15 (+ 11 comparaisons) | 3 · 3 (exploitant) | 92,2 · 93,4 % |
| Sofiane | 3,5 | 4 | 3,5 | 27 | GTO 4 · exploitant 4,5 | 96,7 · 85,2 % |

Application : **4,0** (4,1 au test 6). Conseiller : **3,3**. Sofiane **paierait pour la première fois : 10 € par mois**, jusqu'à 15 € avec plus de tapis couverts et un mode contre un profil.

## 2. Le conseiller : ce qui plaît
- **Juste sur les situations simples** : push/fold heads-up connus (K7o au SB et A2o au BB à 10 BB, K2o à 4 BB, A5o à 15 BB, A9o paie à 8 BB) ; EV identiques au quiz et à l'exercice de range sur une quinzaine de situations comparées (Kevin, Mamadou, Sofiane, Jean-Pierre).
- **Repli sur les tapis calculés les plus proches** jugé intelligent quand il est signalé (« Écart important »).
- Page légère, sans débordement sur téléphone ; aide « Précise assortie ou dépareillée : AKs ou AKo » claire.
- Usage : **entre deux parties, pas pendant**. 2 à 7 touchers (8 s) avec des tapis égaux ou un préréglage, 9 à 13 touchers (15 s) avec des tapis inégaux.

## 3. Le conseiller : problèmes

### Justesse et cohérence
1. **« Jeu mixte : les deux sont justes » pour des options perdantes** (Kevin, Nadia, Jean-Pierre, Léa) : le conseiller appelle « mixte » toute action jouée au moins 10 % du temps, sans regarder l'EV. Q5s : shove −0,23 BB contre call +0,19 ; « CHECK 75 % · SHOVE 17 % » avec un shove à −0,08 contre +0,75. En heads-up à 10 BB ou moins, 172 des 836 « mixtes » affichés ont au moins 0,1 BB d'écart (Kevin). Trois seuils coexistent : conseiller 10 %, exercice de range 25-75 %, correction du quiz « de 20 à 80 % ».
2. **Tapis approchés sans avertissement** (les six) : l'avertissement n'apparaît qu'aux gros écarts. 9/30/13 devient 12/12/12 et affiche « 12 BB effectifs » ; 23/9/17 devient 18/12/18 ; 13/9/22 « 12 BB effectifs » ; 30/6/30 devient 35/15/25 et répond FOLD avec K8o, un tapis évident à 6 BB ; 3 → 4 ou 5 → 6 BB en heads-up. La cote affichée est celle des tapis calculés (« 7 BB pour 16 » au lieu de 5 pour 12).
3. **« Stratégie calculée pour ces tapis » faux en heads-up inégal** (Kevin, Léa) : la page lit le fichier 4/4 pour un 4/8 ; la situation « limp puis tapis du BB » ne peut pas être saisie, et la réponse vient pour le mauvais siège.
4. **Contradictions avec le quiz** (Léa, Jean-Pierre, Nadia) : A6s au BB face au tapis du BTN en 18/18/18, A8s face à un limp à 8 BB, 98s au BB après un limp du SB en 8/8/8, JTo au SB en heads-up 35/15. **Cause trouvée** pour les trois premiers : le « En théorie » du mode exploitant vient du moteur exploitant, pas des calculs de référence du quiz GTO et du conseiller. Le quatrième vient du repli sur des tapis approchés. Deux « théories » différentes dans la même application troublent les joueurs.
5. **Actions absentes des calculs sans message** (Kevin, Sofiane) : min-raise du SB, relance du BB à 2 BB ; après un limp à 6/6, « touche ce que le BB a fait : » sans aucun bouton, alors que le quiz pose cette situation.
6. Grille : mains atteintes 2 à 5 % du temps grisées (74o) ; le quiz cite K4o, Q5s, 76s « à la limite » quand le conseiller les grise (Kevin).

### Interface
7. **État gardé d'une visite à l'autre** : « Main non reconnue. » affichée avec le verdict de la main précédente (Nadia) ; le préréglage reste sélectionné après une saisie à la main (Sofiane).
8. **Réponse à plusieurs actions illisible** : texte noir sur fond bleu nuit (Sofiane).
9. **Sur téléphone, le verdict passe sous le clavier** quand on tape la main ; cases de grille à 23 px (Mamadou, Nadia).
10. Trop de touchers avec des tapis inégaux pour une décision en partie (les six).
11. Vocabulaire : shove / ALL-IN, limp / CALL selon l'écran ; pas de bouton Lexique ; « As Roi assortis » non reconnu (Nadia).
12. Rien ne dit que la réponse est **théorique, pas adaptée au vilain** (Jean-Pierre, Léa) ; pas de mode contre une pastille (Sofiane) ; pas d'équité (Mamadou).

## 4. Reste de l'application : corrections du test 6

| Correction | Verdict |
|---|---|
| « Échantillon faible » dans le bilan, un seul arrondi | **Tient** (les six) |
| Pas de main répétée d'une série à l'autre | **Tient** (les six) |
| « ALL-IN » sur un joueur à tapis ; plus de « Piège » ; « X fois sur Y » | **Tient** |
| Statut « écart négligeable » dans les ranges | **Tient** |
| Exceptions dans « À retenir » des ranges | **Tient** |
| Seuil « mixte » | **En partie** : 25-75 % dans les ranges, mais « de 20 à 80 % » dans la correction du quiz et « au moins 10 % » dans le lexique et le conseiller |
| Range polarisée signalée | **En partie** : dans l'exercice de range seulement, pas dans les corrections du quiz (heads-up 4 BB) |
| « Il limpe beaucoup… pousse plus large » remplacé quand le fold au tapis décide | **Ne tient pas** : 5 fois sur 10 chez Jean-Pierre |
| Pastille cohérente avec les stats | **En partie** : « Rec passif » qui se couche plus que la théorie |

Autres constats : KJo au SB en 18/18/12, « Bonne réponse » puis « Ton choix n'en fait pas partie » (Mamadou) ; un limp joué 15 % du temps noté « Bonne réponse » (Mamadou) ; « Construis ta range » caché en mode exploitant (Léa, Jean-Pierre) ; `#progress` vide à l'accueil après trois séries (Mamadou).

## 5. Proposition
- **Conseiller, justesse (1 à 5)** : « mixte » seulement entre 25 et 75 % et à moins de 0,1 BB du meilleur coup, sinon « Meilleur coup : X » ; avertissement dès que les tapis calculés diffèrent des tapis saisis (effectif, cote et tapis réels affichés) ; ne jamais écrire « calculée pour ces tapis » sur un repli ; message quand l'action saisie n'existe pas dans les calculs ; un seul seuil « mixte » dans toute l'application (conseiller, quiz, lexique).
- **Deux théories** : en mode exploitant, renommer « En théorie » en « Théorie du moteur exploitant » ou l'aligner sur la référence quand elle existe ; à trancher.
- **Conseiller, interface (7 à 12)** : remise à zéro à chaque visite, contraste du verdict, verdict au-dessus du clavier, tapis récents en un toucher, lexique et vocabulaire unifié, mention « théorie, pas exploitation ».
- **Quiz** : « Bonne réponse » et « n'en fait pas partie » ensemble (KJo) ; règle « limpe beaucoup » ; polarisation dans les corrections du quiz.
- La couverture des tapis (impairs, inégaux) dépend de la commande v4.
