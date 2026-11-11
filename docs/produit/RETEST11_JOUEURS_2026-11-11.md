# Onzième test joueurs (11/11/2026) : onglets Quiz (GTO | Exploitant), Exercices, Défis, Progression, Outils

Version testée : `86a235a` (démo version 28). Serveur de test sur une base jetable servant la banque du test fermé `gto_preflop/2026.11.07-s2`. Téléphone simulé 390 × 844. Les six profils sont joués par le responsable des tests : chaque tâche a été faite pour de vrai dans le navigateur (relevés et captures dans `docs/produit/retest11_captures/`), le jugement par profil s'appuie sur ces relevés.

## 1. Résultat en bref

La nouvelle navigation tient ses promesses : chaque tâche demandée se fait en un ou deux touchers, et tous les défauts graves du dixième test sont corrigés. Il reste surtout des **textes qui parlent encore d'« onglet » GTO ou Exploitant**, et **deux séances du jour** dont une seule est en tête de Défis.

| Joueur | Profil | Trouver Ranges / Équités / Profils | GTO → Exploitant | Cadenas | Séance du jour | Note |
|---|---|---|---|---|---|---|
| Mamadou | 58 ans, prudent, téléphone | 4 | 4 | 4 | 4,5 | 4 |
| Léa | régulière, Exploitant | 4,5 | 4,5 | 4 | 3,5 | 4 |
| Kevin | grinder, recompte tout | 4 | 4 | 4 | 3,5 | 4 |
| Nadia | débutante | 4 | 4 | 4 | 4,5 | 4 |
| Jean-Pierre | 67 ans, méfiant | 3,5 | 4 | 3,5 | 4 | 3,5 |
| Sofiane | confirmé, prêt à payer | 4,5 | 4,5 | 4 | 3,5 | 4 |

## 2. Les tâches, mesurées

| Tâche | Constat | Avis des profils |
|---|---|---|
| Trouver Ranges | Exercices → « Construire une range » : l'écran de la range s'ouvre (1 toucher après l'onglet) | trouvé par les six |
| Trouver Équités | Exercices → « Une série de 5 questions » (ou une seule sorte) : question d'équités, étiquette « Équités » | trouvé par les six ; Kevin aime choisir une seule sorte |
| Trouver Profils | Exercices → « Quelle pastille ? Une série de lecture » : question « Défaut du vilain », étiquette « Profils » | trouvé par les six ; Jean-Pierre cherchait d'abord dans Quiz → Exploitant |
| Passer de GTO à Exploitant | Quiz, deux boutons en haut (GTO pressé par défaut) ; le choix est gardé après rechargement | compris immédiatement ; Léa apprécie de retrouver Exploitant à la réouverture |
| Comprendre le cadenas | pendant le test, aucun cadenas affiché ; bandeau « Offre payante, ouverte à tous pendant le test. » (Exploitant), « Offre payante, ouverte pendant le test. » (Équités) | compris par les six ; Jean-Pierre veut connaître le prix |
| Retrouver la séance du jour | en tête de Défis (onglet d'arrivée), titre « Défis », phrase « Ta séance du jour d'abord » ; bouton plein à 530 px | trouvé par les six ; mais c'est la séance GTO (défaut 1) |
| Pendant et après une série | barre masquée pendant la série ; pendant une séance, le bilan propose « Suite de la séance » et « Retour aux défis » | clair |
| Série abandonnée | retour sur Défis : « Reprendre la série en cours » visible, badge sur Défis | corrigé depuis le dixième test |
| Erreurs du jour | sur Défis | corrigé |
| Test de placement (confirmé) | Progression, visible sans défiler (495 px) | corrigé |
| Profil | icône avec le libellé « Profil » | corrigé |

## 3. Défauts, par gravité

### Moyens
1. **Deux séances du jour, une seule en tête de Défis.** Défis montre la séance GTO (« Ta séance du jour · GTO ») et annonce « Ta séance du jour d'abord » ; la séance Exploitant n'existe que dans Quiz → Exploitant. Léa et Sofiane, qui jouent surtout l'Exploitant, ouvrent Défis et y trouvent une séance qui n'est pas la leur. Proposition : une seule séance (celle du mode choisi), ou les deux en tête de Défis.
2. **« Reprendre la série en cours » du mauvais côté** : une série GTO abandonnée se propose aussi dans Quiz → Exploitant (Kevin : « je reprends quoi, là ? »).
3. **Équités annoncée payante** (« Offre payante, ouverte pendant le test ») alors que la décision du 10/11 laisse l'accès d'Équités à trancher : à confirmer avant que les testeurs ne le lisent comme acquis.

### Mineurs
4. **Textes qui parlent d'« onglet » GTO ou Exploitant**, qui n'en sont plus :
   - bilan de série : « bouton « Revoir mes mains » dans l'onglet GTO ou Exploitant » ;
   - Progression : « Niveau 4 · Exploiter le field : l'onglet Exploitant, ouvert en continu » et le lien « Ouvrir l'onglet Exploitant ».
5. Le libellé de la carte Préflop GTO « X % de bonnes réponses » compte les points (une imprécision = 1/2) : 90 % affichés pour 4 bonnes réponses sur 5 (déjà signalé le 11/11).
6. Profils : la série de lecture ne s'annonce pas dans Quiz → Exploitant, où Jean-Pierre l'a cherchée d'abord ; un renvoi « Lecture du vilain : onglet Exercices » suffirait.

## 4. Ce qui était sur l'ancienne navigation et où c'est maintenant

| Avant (I9) | Maintenant |
|---|---|
| Onglets GTO et Exploitant | onglet Quiz, deux boutons |
| Construis ta range (Outils) | Exercices → Ranges |
| Équités (onglet GTO) | Exercices → Équités |
| Lecture du vilain (Exploitant) | Exercices → Profils |
| Conseiller, fiches, lexique, importer mes mains | Outils |
| Séance du jour, défis, erreurs du jour, reprise | Défis |

Rien de ce que les profils utilisaient n'a disparu.

## 5. Recettes

| Recette | Application, banque du test fermé | Application, banque de référence | Démo, banque du test fermé | Démo, banque de référence |
|---|---|---|---|---|
| `e2e_audit_recette.cjs` | 10/10 | 10/10 | — | — |
| `e2e_placement_recette.cjs` | 19/19 | 19/19 | 19/19 | 19/19 |
| `e2e_test_ferme.cjs` | 7/7 | — | — | — |
| `e2e_rythme_recette.cjs` | 13/13 | 13/13 | 10/10 | 10/10 |
| `e2e_fiches_recette.cjs` | 8/8 | 8/8 | 8/8 | 8/8 |
| `e2e_categories_recette.cjs` | 18/18 | 18/18 | 18/18 | 18/18 |
| `e2e_equites_recette.cjs` | 6/6 | 6/6 | 6/6 | 6/6 |
| `e2e_replay_recette.cjs` | 6/6 | 6/6 | 6/6 | 6/6 |
| `e2e_ui_categories_recette.cjs` | 11/11 | 11/11 | 11/11 | 11/11 |

31 passages sur 31, une base neuve par passage, même `SPINSACADEMY_DATASET` que le serveur ou la démo. Toutes passent par `tools/web/nav_helper.cjs` (onglet Quiz puis bouton GTO ou Exploitant). Le contrôle AU3 de `e2e_audit_recette` n'exige plus un nombre de situations distinctes (échec aléatoire sur la banque étroite) mais les 10 questions dans la tranche.

## 6. Ce qui plaît
- Exercices : « enfin rangé » (Sofiane) ; les trois formats en une page.
- Les deux boutons GTO | Exploitant, plus clairs que deux onglets (Mamadou, Nadia).
- Défis qui commence par la séance, puis les défis avec leur catégorie.
- Aucune erreur JavaScript sur tout le parcours.
