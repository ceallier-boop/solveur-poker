# Douzième test joueurs (16/11/2026) : la version complète

Version testée : `5ce7aec` (démo version 34). Application sur un serveur de test à base jetable servant la banque du test fermé `gto_preflop/2026.11.07-s2`, joueurs aux niveaux 1 et 2 ; démo reconstruite par `tools/web/build_offline.py` (banque de référence). Téléphone simulé 390 × 844. Les six profils sont joués par le responsable des tests : chaque parcours a été fait pour de vrai dans le navigateur (relevés chronométrés et captures dans `docs/produit/retest12_captures/`) ; le jugement par profil s'appuie sur ces relevés. Rien n'a été corrigé pendant le test.

Parcours couverts : premier lancement (« Ton but », proposition du test de placement), test de placement de 10 mains, onglets Quiz (GTO | Exploitant) et Exercices, séance du jour et défis par catégorie, défi du jour joué, main rejouée à la table, les huit sortes d'équités, « Construis ta range », lecture du vilain, import de mains (fichiers d'exemple synthétiques de `tests/data/winamax/`, pseudos inventés), fiches à emporter, Progression, profil et réglages.

## 1. Résultat en bref

La version complète tient debout : aucun incident, aucune erreur JavaScript, **aucun débordement horizontal à 390 px** sur aucun des écrans visités, application comme démo. Une débutante qui n'a jamais vu l'application répond à **sa première question 4 secondes** après l'ouverture. La main rejouée dure **1,2 à 2,9 s**. L'import est exemplaire sur la vie privée.

Les défauts restants sont du côté des **nouveaux exercices d'équités pour les débutants** (vocabulaire et grilles sans légende) et d'un chiffre de progression décourageant au tout début.

| Joueur | Profil | Prise en main | Quiz et séance | Équités | Import et fiches | Progression | Note |
|---|---|---|---|---|---|---|---|
| Mamadou | 58 ans, prudent, téléphone | 4,5 | 4 | 3 | 3 | 3,5 | 3,5 |
| Léa | régulière, Exploitant | 4,5 | 4,5 | 4 | 4 | 4 | 4 |
| Kevin | grinder, recompte tout | 4,5 | 4,5 | 4,5 | 3,5 | 4 | 4 |
| Nadia | débutante, niveau 1 | 4,5 | 4 | 2,5 | 3 | 3 | 3,5 |
| Jean-Pierre | 67 ans, méfiant | 4 | 4 | 3 | 4 | 3,5 | 3,5 |
| Sofiane | confirmé, niveau 2, prêt à payer | 4,5 | 4,5 | 4,5 | 3,5 | 4 | 4 |

## 2. Mesures

| Point observé | Mesure |
|---|---|
| Premières minutes (débutante) | 3 écrans de premier lancement, accueil à 3 s, première question à 4 s (bouton « Commencer la séance » visible sans défiler) |
| Main rejouée (séquence avant chaque question) | 1,2 à 2,9 s par question (séance, défi du jour, 10 mains de placement) |
| Lisibilité mobile 390 px | 0 débordement horizontal sur tous les écrans visités (application et démo) |
| Vocabulaire niveau 1, Préflop | énoncé, boutons, correction et bilan en mots français (« Se coucher (FOLD) », « Tapis 8 BB (ALL-IN) », « chances de gagner ») ; aucun terme de jargon relevé |
| Vocabulaire niveau 2 | termes habituels (FOLD, CALL, RAISE TO, ALL-IN, outs, range) : conforme au choix du niveau |
| Test de placement (confirmé) | proposé au premier lancement ; 10 mains ; résultat par profondeur de tapis ; sur la banque du test fermé, deux tranches (« 2 sur 4 », « 3 sur 6 »), la tranche 17-25 BB n'est pas montrée ; « Prendre ce niveau » / « Garder le niveau 2 » |
| Huit sortes d'équités | les huit se lancent depuis Exercices et se corrigent (application et démo) |
| Import de mains | 9 fichiers d'exemple : 138 mains lues, 2 ignorées, 30 en heads-up, 108 à 3 joueurs ; **aucune requête réseau** pendant l'import (application : seulement le chargement du lecteur `winamax.js` ; démo : aucune) ; case de contribution décochée et inactive (« bientôt ») ; « Effacer » vide le résultat |
| Séance du jour | en tête de Défis, avec le lien « Séance du jour Exploitant : ouvrir le Quiz Exploitant » ; sur la banque du test fermé, la série du thème d'une débutante a 3 questions (banque étroite) |

## 3. Défauts, par gravité

### Moyens
1. **Jargon dans les équités au niveau 1.** La règle du niveau 1 (« ni outs ni range dans l'énoncé ») n'est pas tenue par les nouvelles sortes :
   - titres des sortes affichés à une débutante : « Équité contre une range », « Tirages et outs », « Range contre range » ;
   - « Ce flop t'aide-t-il ? », « Range contre range », « Mains très fortes » : « Lui : SB, complète (limp) à 8 BB », « Toi, BB qui checke », et dans la correction « contre sa range », « de ta range ».
   Nadia : « une range, c'est quoi ? » ; Mamadou ne finit pas « Range contre range ». Captures `eq_range_help.png`, `eq_nut_help_correction.png`.
2. **Grilles de « Range contre range » sans légende.** Deux grilles 13 × 13 (bleue « Toi », verte « Lui ») avec des nuances, sans dire ce que veut dire une case foncée ou claire. Nadia et Jean-Pierre ne savent pas quoi regarder.
3. **Un chiffre décourageant au tout début.** Après 9 décisions, Progression affiche en tête « 108,89 BB perdus pour 100 décisions » (avec « échantillon faible » en petit). Nadia : « je perds plus de 100 BB ? ». Le chiffre est juste, mais sur 9 décisions il n'apprend rien ; proposition : ne pas le montrer avant un minimum de décisions (comme les objectifs, « au moins 30 décisions »), et sans décimales.
4. **Import : des chiffres, puis rien.** Le résultat donne 4 compteurs et un bouton « Enregistrer mes comptages » (deux fichiers CSV). Mamadou et Jean-Pierre : « et maintenant ? » ; Kevin ouvre les CSV mais aimerait le bilan dans l'application. C'est le périmètre de MM2 ; à annoncer (« le bilan de tes mains arrive ») pour ne pas décevoir pendant le test.

### Mineurs
5. Écran d'import : le titre « Importer mes mains » s'écrit sur deux lignes dans la barre du haut, serré contre « SpinsAcademy ».
6. Lecture du vilain : l'énoncé chiffré (« Sur 100 coups observés … le BB a payé ton tapis quand le SB s'était couché 27 fois sur 65 (42 % ; théorie : 28 %) ») est long sur téléphone ; Mamadou le lit deux fois. Les barres en dessous suffisent.
7. Test de placement d'un confirmé à 5 sur 10 : niveau 1 proposé, bouton plein « Prendre ce niveau ». Sofiane l'aurait pris par réflexe ; « Garder le niveau 2 » est moins visible. Rien de faux, mais un retour en arrière du niveau mériterait une phrase (« tu repars des tapis courts »).

## 4. Par profil

- **Mamadou** : prise en main rapide, la séance se lance seule ; l'animation de la main « montre bien qui a fait quoi » et ne le ralentit pas. Bloque sur « Range contre range » (défaut 1) et ne voit pas à quoi sert l'import (défaut 4).
- **Léa** : passe de GTO à Exploitant sans hésiter, trouve la séance Exploitant par le lien de Défis ; aime « Mains très fortes ». Demande une légende des grilles (défaut 2).
- **Kevin** : vérifie les chiffres : séance raccourcie à 3 questions sur la banque du test, placement par tranches, import (138 mains, 30 + 108) ; tout concorde. Voudrait le bilan de ses mains dans l'application (défaut 4).
- **Nadia** : la meilleure prise en main (première question à 4 s, mots français partout en Préflop) ; les équités avec tableau la perdent (défauts 1 et 2) ; le « 108,89 BB perdus » la décourage (défaut 3).
- **Jean-Pierre** : apprécie que l'import ne parte pas sur Internet (« Rien n'est envoyé », vérifié : aucune requête) et la case de contribution inactive ; trouve la lecture du vilain trop bavarde (défaut 6).
- **Sofiane** : niveau 2, vocabulaire du jeu, les huit sortes d'équités jouées sans peine ; hésite au résultat du placement (défaut 7) ; paierait pour le bilan des mains importées.

## 5. Recettes

Les recettes automatiques ont été rejouées sur la version testée, application et démo, avec les deux banques (contrôles passés / contrôles).

| Recette | Application, banque du test fermé | Application, banque de référence | Démo, banque du test fermé | Démo, banque de référence |
|---|---|---|---|---|
| `e2e_audit_recette.cjs` | 10/10 | 10/10 | — | — |
| `e2e_placement_recette.cjs` | 19/19 | 19/19 | 19/19 | 19/19 |
| `e2e_test_ferme.cjs` | 7/7 | — | — | — |
| `e2e_rythme_recette.cjs` | 13/13 | 13/13 | 10/10 | 10/10 |
| `e2e_fiches_recette.cjs` | 8/8 | 8/8 | 8/8 | 8/8 |
| `e2e_categories_recette.cjs` | 18/18 | 18/18 | 18/18 | 18/18 |
| `e2e_equites_recette.cjs` | 7/7 | 7/7 | 7/7 | 7/7 |
| `e2e_replay_recette.cjs` | 6/6 | 6/6 | 6/6 | 6/6 |
| `e2e_ui_categories_recette.cjs` | 11/11 | 11/11 | 11/11 | 10/11 puis 11/11 (×2) |

Seul écart : un contrôle de `e2e_ui_categories_recette.cjs` sur la démo exigeait une des sortes outs, équité sur tableau ou « Ce flop t'aide-t-il ? » ; une série tire 5 sortes sur 8 et peut n'en contenir aucune. C'était un défaut du test, pas de l'application : le contrôle compte désormais les cinq sortes avec tableau (toujours au moins 2 par série) et garde la vérification de chaque verdict par l'évaluateur indépendant ; rejoué deux fois sur la démo, 11/11.

## 6. Ce qui plaît
- La première séance en quelques secondes, sans explication.
- La main rejouée, courte (moins de 3 s) et utile.
- Les huit sortes d'équités, variées ; « Mains très fortes » et « Ce flop t'aide-t-il ? » plaisent aux joueurs confirmés.
- L'import : honnête sur la vie privée, et il tient ses promesses.
- Aucun écran qui déborde sur téléphone.
