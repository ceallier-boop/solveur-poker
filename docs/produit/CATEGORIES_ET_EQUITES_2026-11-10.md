# Catégories d'exercices et classe « Équités » (10/11/2026)

Demande du porteur du 10/11 : ranger proprement tous les exercices par catégorie ; constat que, avec les défis, la structure « 5 questions » est plus diluée ; nouvelle classe de questions « Équités ». Ce document propose, rien n'est codé.

## 1. Les catégories d'aujourd'hui

| # | Catégorie | Ce que fait le joueur | Où c'est dans l'application |
|---|---|---|---|
| 1 | Préflop GTO | choisit l'action de la banque du solveur | onglet GTO ; séance du jour, séries libres, thèmes |
| 2 | Préflop exploitant | choisit l'action contre un profil (mode Field) | onglet Exploitant |
| 3 | Profils joueurs | reconnaît un profil (« Quelle pastille ? », identification) | mode exploitant, défi « Lecteur de vilain » |
| 4 | Ranges | construit une range (« Construis ta range ») | Outils ; étape de la séance du jour |
| 5 | ? | le porteur en compte cinq : **à préciser** (candidats : le test de placement, ou la lecture du vilain séparée des profils) | |
| 6 | Équités (nouveau) | voir §3 | à créer |

Aujourd'hui ces exercices sont mélangés dans les séries : une série de 5 questions est tirée dans un seul type à la fois, mais les défis, les étapes de la séance du jour et les thèmes les enchaînent sans que le joueur sache dans quelle catégorie il est ni comment il progresse dans chacune.

## 2. Proposition de rangement

- **Une catégorie = une page propre** (liste de ses exercices, sa série libre, ses thèmes, son score et son niveau de maîtrise), dans l'onglet qui lui correspond : GTO et Exploitant gardent leurs onglets ; **Ranges**, **Profils** et **Équités** vivent sous un onglet « Exercices » ou dans Outils (à décider avec la maquette).
- **Progression par catégorie** : un score et un niveau par catégorie (les « thèmes » restent à l'intérieur de la catégorie GTO).
- **Étiquette de catégorie** affichée sur chaque question et dans le bilan de série (une icône et un mot).

### Les défis dilués

Le constat est juste : une série de 5 questions qui mélangerait les cinq catégories n'en donnerait qu'une chacune, donc aucune mesure fiable. Proposition :
- **Un défi = une catégorie** (5 questions dans la même catégorie), sauf le défi du jour ;
- **Défi du jour = un parcours mixte, une question par catégorie** (5 ou 6 questions), présenté comme tel : on y mesure la polyvalence, pas la maîtrise ;
- la séance du jour (10 ou 15 minutes) garde ses étapes, mais le bilan est découpé par catégorie.
Question au porteur : **défis par catégorie + défi du jour mixte (recommandé), ou autre ?**

## 3. Nouvelle classe « Équités »

Idée du porteur : on donne une main, la personne identifie ses forces et ses faiblesses et les chances de toucher paire, top paire, suite, carré, etc.

Proposition de format, à valider :
1. **Main seule (sans tableau).** « Tu as 9♠8♠. Quelle est la chance de toucher au moins une paire au flop ? une couleur ? une suite ? » Réponse en choisissant une tranche (par exemple 20 à 30 %) ; la correction donne la valeur exacte, calculée en énumérant tous les flops (19 600), jamais estimée.
2. **Forces et faiblesses.** Le joueur coche dans une liste ce qui est vrai de la main (« bonne pour les tirages couleur », « dominée par les As », « bloque les As », « fait rarement une top paire »…) ; liste générée par règles, pas à la main.
3. **Main contre une range.** Pour relier aux autres catégories : l'équité de la main contre la range de la banque (par exemple contre un tapis à 8 BB), avec les mêmes tranches de réponse.
4. **Plus tard** : mains avec tableau (flop), après la MVP comme décidé le 06/11.

Notation : points selon l'écart à la valeur exacte (tranche juste = 1 point, tranche voisine = demi-point) ; pas de « BB perdus » (pas de coût en BB).
Niveau 1 : vocabulaire simple (paire, couleur, suite), pas de pourcentages fins.
Calcul : le moteur existe déjà (équités du solveur et énumérations dans le dépôt) ; à confirmer par Moteur GTO.

## 4. Étapes proposées

| Étape | Qui | Contenu |
|---|---|---|
| CE1 | Plan | cette note, décisions du porteur (cinquième catégorie, défis, format équités) |
| CE2 | Moteur GTO | bibliothèque d'équités : chances de toucher chaque catégorie de main au flop, équité contre une range, étiquettes forces/faiblesses ; tests contre des valeurs connues |
| CE3 | Plan | classe de question « équités » dans le moteur de quiz (tirage, correction, points), démo comprise |
| CE4 | Interface | rangement par catégorie (maquette puis refonte), écran des questions d'équité |
| CE5 | Défis et rétention | défis par catégorie, défi du jour mixte, bilan par catégorie |
| CE6 | Tests | exactitude des équités, recette navigateur, test joueurs |
