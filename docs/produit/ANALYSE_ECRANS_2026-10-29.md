# Analyse des écrans de SpinsAcademy (29/10/2026)

Méthode : chaque écran capturé sur téléphone (390 × 844), en mode clair, version `db67ee7`, plus la page « Mes mains » de la démo publiée par une autre session (code non poussé). Pour chaque écran : est-il clair, facile à comprendre, et l'élément le plus important se repère-t-il tout de suite ?

## Synthèse

| Écran | Clarté (sur 5) | Élément le plus important | Repérable ? |
|---|---|---|---|
| Accueil | 4 | « Série recommandée » | **Oui** |
| Choisir le thème | 4 | « Lancer cette série » | **Oui** |
| Question (table) | 4,5 | Ta main et la barre d'actions | **Oui** |
| Correction | 4 | Verdict et bon coup | **Oui**, mais la suite est chargée |
| Bilan de série | 4,5 | Score « 2 / 5 » | **Oui** |
| Construis ta range, avant | 4,5 | La question | **Oui** |
| Construis ta range, après | 3 | Ta range trop serrée ou trop large | **Non** : le « 89,4 % » flatteur prend la place |
| Ma progression | 3 | Où tu en es, et quoi travailler | **En partie** : score visible, diagnostic vide |
| Lexique | 4 | La définition cherchée | **Oui** (« Sur cet écran ») |
| Conseiller « Comment jouer ma main ? » | 3 | La réponse | **Non** : sous la ligne de flottaison |
| Mes mains (démo publiée) | 3 | « Importer mes mains » | **Oui**, mais la démarche est technique |

Les écrans de jeu (accueil, question, correction, bilan) sont bons. Les trois écrans les plus faibles sont ceux où il faut **interpréter un résultat** (range corrigée, progression) ou **saisir une situation** (conseiller).

## 1. Accueil — 4/5
- **Bien** : titre et promesse en une phrase ; choix GTO / Exploitant expliqué ; « Série recommandée » seul bouton plein, impossible à manquer.
- **À améliorer** :
  - trois boutons secondaires de même poids (Construis ta range, Comment jouer ma main ?, Ma progression) : rien ne distingue l'entraînement de la consultation ;
  - « Ma progression » n'est qu'un bouton : un joueur qui revient ne voit ni son score ni ce qu'il doit travailler ;
  - « Choisir le thème » et « Mes pastilles » ont un espace vide sous leur titre, comme s'ils étaient cassés ;
  - aucun accueil pour un nouveau joueur (3 écrans prévus au lot B5).

## 2. Choisir le thème — 4/5
- **Bien** : quatre groupes nommés (Format, Situation, Position, Profondeur), choix actifs en vert, bouton « Lancer cette série » à la fin.
- **À améliorer** : long sur téléphone ; le nombre de questions disponibles pour le choix n'est pas indiqué.

## 3. Question (table) — 4,5/5
- **Bien** : la table ressemble au client de jeu ; tes cartes, ton tapis et la barre FOLD / CALL / ALL-IN sont l'essentiel de l'écran ; chrono en haut, discret.
- **À améliorer** :
  - les mises devant les joueurs sont des nombres sans unité (« 1 », « 0,5 ») ;
  - la moitié basse de l'écran est vide : la barre d'actions pourrait descendre, plus près du pouce ;
  - « Raccourcis clavier : touches 1 à 2 » et les chiffres sous les boutons s'affichent sur le téléphone simulé (à vérifier sur un vrai appareil, point ouvert depuis le test 4) ;
  - mode exploitant :
    - la pastille, information principale contre ce vilain, n'est qu'une lettre dans un petit rond ;
    - la pastille « Reg » est grise par défaut, donc proche du « ? » gris qui veut dire « pas de pastille » ;
    - la ligne de stats « Limp 22 · Call/limp 9 (100) » est cryptique, et le cadre déborde à droite de la table ;
    - la bande « Pastille posée · Stats du vilain · 80 mains » annonce des stats alors que la pastille les remplace.

## 4. Correction — 4/5
- **Bien** : verdict coloré en premier (« Erreur », « Bonne réponse »), bon coup et coût dans la même bande, message essentiel en gras, « À retenir » encadré, détails repliés.
- **À améliorer** :
  - la situation est redite en texte gris dense : on perd la table qu'on vient de voir ;
  - deux messages qui se répondent mal : la bande dit « Le bon coup : ALL-IN 8 BB », les précisions « Les coups les plus rentables : ALL-IN ou CALL 0,5 BB » ;
  - redites dans les précisions (« Plus de 0,1 BB d'écart : c'est une erreur » répète la bande) ; trois blocs repliables plus « Signaler » font une longue page ;
  - « À retenir » ajoute « les très grosses mains (AA, KK, QQ…) limpent plutôt » quand on joue J8o : utile, mais détourne de la leçon de la main ;
  - le bouton flottant « Question suivante » cache le texte quand on fait défiler.

## 5. Bilan de série — 4,5/5
- **Bien** : score énorme, trois compteurs (bonnes, imprécisions, erreurs), mains à revoir avec ton coup et le meilleur coup, révision annoncée.
- **À améliorer** : la phrase des BB perdus fait trois lignes ; la mention « échantillon faible » pourrait être une petite note sous le chiffre.

## 6. Construis ta range, avant — 4,5/5
- **Bien** : situation, question en gras, ce que font les autres mains, mode d'emploi de la grille, compteur « Ta range : x % », deux boutons clairs.
- **À améliorer** : « tapis 35 / 25 / 15 » puis, après la correction, « avec 25 BB de tapis » : le tapis effectif n'est pas annoncé avant.

## 7. Construis ta range, après — 3/5
- **Problème principal** : le premier chiffre est « 89,4 % des mains bien classées », alors que la range dessinée (6 %) fait le quart de la référence (25 %), avec 15 mains oubliées. Le message qui compte, « ta range est beaucoup trop serrée », est en petit sur la troisième ligne. Sofiane trouvait déjà ce score flatteur.
- **À améliorer** : grille très chargée (hachures sur une grande partie des cases) ; légende de cinq symboles en petit ; « Touche une case… » perdu sous la légende.
- **Proposition** : en tête, une phrase de diagnostic (« Trop serrée : 6 % des mains au lieu de 25 % ; 15 oubliées ») ; le pourcentage bien classé et les BB perdus en second.

## 8. Ma progression — 3/5
- **Bien** : score en grand, BB perdus pour 100 décisions, mention « échantillon faible ».
- **À améliorer** :
  - « À travailler maintenant : Rien à retravailler pour l'instant » à côté d'un score de 40 % : le joueur ne sait pas quoi faire ;
  - « Par thème » est un mur de « encore N questions pour un score » (cinq cartes, quinze lignes) qui ne dit rien à un nouveau joueur ;
  - graphique des séries sans valeurs ni dates ;
  - trois indicateurs (score, BB perdus, ranges) dans un paragraphe ;
  - réglage « Exercices adaptatifs » et liens de données en bas d'une page déjà longue.
- **Proposition** : en tête, un seul chiffre et une seule action (« Joue encore 8 questions face à un limp pour un premier diagnostic ») ; thèmes repliés tant qu'aucun n'a de score ; valeurs sur le graphique.

## 9. Lexique — 4/5
- **Bien** : recherche, rubrique « Sur cet écran » qui donne d'abord les mots de l'écran courant.
- **À améliorer** : définitions longues ; pas de lien direct depuis le conseiller.

## 10. Conseiller « Comment jouer ma main ? » — 3/5
- **Problème principal** : la réponse n'apparaît qu'au troisième bloc, sous la ligne de flottaison du téléphone. Le premier écran montre surtout les réglages de tapis.
- **À améliorer** :
  - la saisie du coup demande de comprendre l'arbre (« Au BTN de parler. C'est toi ? La réponse est ci-dessous. Sinon, touche ce que le BTN a fait… ») : on ne choisit pas directement sa position ;
  - douze préréglages de tapis : utiles, mais ils prennent deux lignes avant tout le reste ;
  - pas de lien retour clair vers l'entraînement (seulement « SpinsAcademy » en haut à droite).
- **Proposition** : en haut, position et main ; juste dessous, la réponse ; les tapis et les actions précédentes en réglages repliables, préremplis avec les derniers utilisés.

## 11. Mes mains (démo publiée par une autre session) — 3/5
- **Bien** : un seul bouton plein « Importer mes mains », étapes numérotées, confidentialité dite.
- **À améliorer** : la démarche est technique pour la plupart des joueurs (lancer `python winamax_hands.py import`, choisir un fichier `.json`) ; avant l'import, rien ne montre ce que l'analyse apporte (pas d'exemple).
- Hors de cette page, la démo affiche en tête un encadré technique (« datasets 2026.10.13-3… ») avant le titre.

## 12. Priorités proposées
1. **Conseiller** : réponse visible sans défiler (position et main en haut, réglages repliés).
2. **Range corrigée** : diagnostic « trop serrée / trop large » en tête, score en second, grille allégée.
3. **Progression** : un chiffre et une action en tête ; thèmes repliés tant qu'ils sont vides.
4. **Correction** : rappel compact de la situation (mini-table ou une ligne), redites retirées, une seule formulation du bon coup, marge sous le bouton flottant.
5. **Question** : unité sur les mises, pastille plus visible (couleur et nom), « Reg » dans une autre couleur que le gris, ligne de stats lisible et contenue dans son cadre.
6. **Accueil** : résumé de progression à la place du bouton, actions secondaires regroupées.
7. **Mes mains** : mode d'emploi pas à pas sans jargon, exemple d'analyse avant l'import.

## 13. Corrections faites (29/10/2026)

| Priorité | Fait |
|---|---|
| 1. Conseiller | Premier bloc « Ta position et ta main » : on touche BTN, SB ou BB, le coup se remplit avec le chemin le plus simple (tout le monde se couche avant toi ; au BB, le SB limpe), et la réponse s'affiche juste sous la position, sans défiler. Le verdict rappelle le coup supposé (« K9o au BB · après BTN fold, SB limp »). « Ce qui s'est passé avant toi » permet de le modifier. Table et tapis repliés, résumés en une ligne (« 3 joueurs · 20 / 20 / 20 BB · modifier »). Lien « ← Entraînement » en haut à gauche. |
| 2. Range corrigée | En tête, le diagnostic : « Trop serrée » ou « Trop large » (moins de 75 % ou plus de 133 % de la référence), sinon « Bonne taille » ; puis les mains oubliées et en trop ; le pourcentage bien classé et les BB perdus passent en second, en petit. |
| 3. Progression | Score en grand, puis des tuiles (BB perdus pour 100 décisions, ranges bien classées, coups au temps). Sans thème fiable, « À travailler maintenant » propose le thème le plus avancé avec un bouton (« Position : BB, 6 sur 10. Joue-le pour un premier diagnostic »). Thèmes repliés tant qu'aucun n'a de score. Valeurs et dates sur le graphique. |
| 4. Correction | Rappel de la situation en une ligne (« SB · heads-up · 20 BB effectifs / premier à parler »), énoncé complet en tête des précisions. Une seule formulation : la bande dit « Les bons coups : A ou B » quand plusieurs coups se valent, et les précisions ne répètent plus le verdict ni les bons coups. Marge sous le bouton flottant. |
| 5. Question | Mises en BB (« 1 BB », « 0,5 BB ») ; nom de la pastille sous le siège, dans sa couleur ; « Reg » violet par défaut (le gris reste « pas de pastille ») ; bande « Pastille posée · Reg · voir ses stats (40 mains) » ; ligne de stats qui revient à la ligne dans son cadre, « Call après limp » au lieu de « Call/limp ». |
| 6. Accueil | Le bouton « Ma progression » affiche le score, les BB perdus pour 100 décisions et le thème à travailler ; cadres « Choisir le thème » et « Mes pastilles » sans espace vide. |
| 7. Mes mains | **Non fait** : son code n'est dans aucune branche du dépôt (seulement dans la démo publiée par une autre session). |

Reste : raccourcis clavier affichés sur téléphone simulé (à vérifier sur un vrai appareil) ; accueil pour un nouveau joueur (lot B5).
