# « Mes mains » : plan de réintégration (09/11/2026)

Demande du porteur du 09/11 : voir comment réintégrer la section « Mes mains », exclue de l'application le 29/10. Ce document dit ce qui existait, ce qu'on vise, dans quel ordre, et ce qui reste à décider. Aucun code n'est écrit à ce stade.

## 1. Ce qui existait (démo du 28/10)

Retrouvé dans l'artéfact publié `SpinsAcademy` du 28/10 (`https://claude.ai/artifact/DvmjQJpUvfUG3VWxT6iDi8`). Son code n'est dans aucune branche du dépôt.

- Le joueur lançait un script Python (`winamax_hands.py import`) sur son ordinateur ; il écrivait un fichier `mains_spinsacademy.json`.
- La page importait ce fichier. Tout restait **dans le navigateur** (`localStorage`, clé `spinsacademy_mains_v1`) : aucun envoi au serveur.
- Chaque décision réelle était **rapprochée de la situation de référence la plus proche** (historique des actions, tapis, main), puis notée : verdict comme dans l'entraînement, comparaison avec la stratégie de référence.
- Trois blocs : un bilan, des comparaisons de fréquences (le joueur contre la référence), des conseils avec un bouton pour s'entraîner sur la fuite.
- Limites relevées à l'analyse des écrans du 29/10 : démarche technique (installer Python), pas d'exemple avant l'import, banque de l'époque (export de référence, pas notre solveur).

## 2. Ce qu'on vise

Cinq principes.

1. **Tout reste chez le joueur.** Lecture et notation dans le navigateur ; rien n'est envoyé. Les pseudos des adversaires ne sont jamais conservés.
2. **Plus de Python.** Le joueur donne directement ses fichiers `.txt` d'historique Winamax. Moteur exploitant a déjà écrit un lecteur Python qui repère le héros et ses actions (`tools/field/winamax_counts.py`) : il se porte en JavaScript.
3. **Noté contre notre banque, avec sa fiabilité.** Les décisions « tapis » (2 à 16 BB) sont notées comme les questions. Les décisions qui mènent au flop sont affichées « approximation ». Les mains relues par les experts passent avant le solveur.
4. **Un écran en trois temps :** importer ; ce que disent tes mains (accord avec la référence, BB perdus pour 100 mains réelles, tes 3 plus grosses fuites) ; s'entraîner sur une fuite.
5. **Lien avec l'entraînement :** « Travailler cette fuite » lance une série filtrée sur la situation ; plus tard, les fuites réelles nourrissent le thème de la séance du jour.

## 3. Périmètre de la première version

- Avant le flop seulement, Expresso, heads-up et 3 joueurs, de 2 à 16 BB en priorité.
- Décisions sans situation de référence proche : comptées « non évaluées », jamais notées au hasard.
- Petits volumes : « échantillon faible » sous 100 décisions, comme dans la progression.
- Pas d'analyse après le flop, pas de suivi de gains, pas de tracker.

## 4. Données et vie privée

- Seul le jeu du héros est analysé. Les noms des adversaires servent en mémoire à l'analyse puis sont jetés.
- Stockage local sur l'appareil ; « Effacer mes mains » ; pas de synchronisation tant qu'il n'y a pas de comptes (A16).
- **Piste forte : contribution volontaire.** Chaque joueur peut, s'il le veut, offrir ses comptages anonymes (les mêmes que `winamax_counts.py`) pour caler le field. C'est exactement ce qui manque (569 mains aujourd'hui, 30 000 à 50 000 nécessaires). Case à cocher, désactivée par défaut, jamais obligatoire.
- La politique de confidentialité (A14) doit décrire l'import avant l'ouverture publique.

## 5. Offre (à valider, lié à P14)

Proposition : l'import et le bilan global sont gratuits (c'est ce qui donne envie de s'entraîner) ; le détail par famille de mains et par position, et le suivi dans le temps, font partie des statistiques détaillées payantes.

## 6. Étapes et responsables

| Étape | Qui | Contenu |
|---|---|---|
| MM1 | Plan | Cette note, puis récupération en lecture seule du code de la démo du 28/10 pour le réutiliser |
| MM2 | Moteur exploitant | Lecteur Winamax en JavaScript (héros, positions, tapis effectif, actions), format de sortie, tests sur des mains d'exemple sans pseudo |
| MM3 | Moteur GTO | Table de référence compacte pour le navigateur (situations « tapis » de 2 à 16 BB, EV par action, fiabilité), et règle d'appariement d'une main réelle à une situation |
| MM4 | Interface | Écran « Mes mains » : import, bilan, conseils, bouton d'entraînement |
| MM5 | Tests | Mains synthétiques, vie privée (aucun pseudo dans le stockage local ni sur le réseau), appariement |
| MM6 | Défis et rétention | Fuites réelles dans les objectifs et la séance du jour (après MM4) |

**Premier jalon (une semaine, MM2 + MM3) : essai sur les 569 mains Expresso du porteur.** Il dira quelle part des décisions réelles trouve une situation de référence, et donc si le produit tient.

## 7. Risques

- Le format Winamax est celui que lit Moteur exploitant, sans documentation officielle : 569 mains lues, 0 illisible, bon signe mais à confirmer sur plus de fichiers.
- L'appariement : si trop peu de décisions réelles trouvent une situation (tapis inégaux, limps multiples), le bilan sera maigre.
- Poids de la table de référence dans le navigateur : à mesurer (la démo complète pèse déjà 3 Mo).
- Usage de ses propres historiques Winamax : à vérifier avec le juriste (A14).
- Les décisions qui mènent au flop restent approximatives : l'écran doit le dire sans dramatiser.

## 8. À décider par le porteur

1. Offre : import et bilan gratuits, détail payant ?
2. Contribution volontaire des comptages anonymes : oui ?
3. Calendrier : lancer le jalon d'essai (MM2 + MM3) maintenant, en parallèle des trois chantiers de rythme (séance de 10 minutes, pires erreurs du jour, fiches), ou après ?
