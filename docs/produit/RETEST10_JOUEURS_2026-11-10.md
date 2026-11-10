# Dixième test joueurs (10/11/2026) : navigation à cinq onglets (I9)

Version testée : `22f08d8` (barre Outils · GTO · Défis · Exploitant · Progression, démo version 17). Serveur de test sur une base jetable, servant la banque du test fermé `gto_preflop/2026.11.07-s2` (`SPINSACADEMY_DATASET`, feu vert du porteur le 10/11) ; démo reconstruite par `tools/web/build_offline.py` deux fois : avec la banque du test fermé, puis avec la banque de référence. Téléphone simulé 390 × 844. Les six profils sont joués par le responsable des tests : chaque tâche a été faite pour de vrai dans le navigateur (captures et relevés), le jugement par profil s'appuie sur ces relevés. Captures : `docs/produit/retest10_captures/` (arrivée, onglets, profil, bilan, abandon, placement bloqué).

## 1. Résultat en bref

La barre elle-même est comprise : les cinq onglets se lisent, Outils regroupe bien ce qu'on ouvre entre deux parties, la barre disparaît pendant une série et revient après, le cadenas Exploitant éteint est expliqué (« Offre payante, ouverte à tous pendant le test »). Mais **deux blocages sur la banque du test fermé** (séance du jour d'un débutant, test de placement d'un confirmé), tous deux **sans aucun message**, et plusieurs choses de l'ancien accueil ne se retrouvent plus depuis l'onglet d'arrivée.

| Joueur | Profil | Barre | Retrouver la séance | Trouver un outil | Sans se perdre (série) | Note |
|---|---|---|---|---|---|---|
| Mamadou | 58 ans, prudent, téléphone | 4 | 3 | 4 | 3 | 3,5 |
| Léa | régulière, Exploitant | 4 | 3 | 4 | 3 | 3,5 |
| Kevin | grinder, recompte tout | 3,5 | 3 | 4 | 2,5 | 3 |
| Nadia | débutante | 3 | 1 | 4 | 3 | 2 |
| Jean-Pierre | 67 ans, méfiant | 3 | 3 | 3,5 | 3 | 3 |
| Sofiane | confirmé, prêt à payer | 4 | 3,5 | 3 | 3 | 3 |

## 2. Défauts, par gravité

### Bloquants (test fermé)
1. **Séance du jour impossible pour un débutant (niveau 1)** sur la banque du test fermé. « Commencer la séance » envoie `POST /sessions` `{plan: "theme", filters: {family: "first_in", min_stack: 0, max_stack: 9.5}}` ; le serveur répond **422 « 3 spots disponibles pour ces filtres, 5 demandés »** (la banque n'a que 8 BB sous 10 BB). **Aucun message** : l'écran reste sur Défis, le bouton principal semble ne rien faire. La série rapide, elle, se replie et marche. Touche tous les testeurs débutants (Nadia). Un joueur confirmé (niveau 2, 10-16 BB) n'est pas touché. Même blocage dans une démo construite avec la banque du test fermé ; avec la banque de référence, la séance démarre.
2. **Test de placement impossible** sur la banque du test fermé : `POST /sessions {plan: "placement"}` → **422 « 0 spots disponibles pour ces filtres, 3 demandés »** (tranche 17-25 BB absente d'une banque 8-16 BB). Depuis le premier lancement, « Faire un test de 10 mains » ramène sur Défis **sans message** (Sofiane, Kevin). `e2e_placement_recette.cjs` échoue pour la même raison.

### Graves
3. **Échec silencieux d'un démarrage de série** : un refus 422 du serveur sur une séance ou un placement ne produit aucun message (cause commune des bloquants 1 et 2 côté interface). Il faut au moins « Cette séance n'est pas disponible avec la banque du test ; essaie une série rapide ».
4. **Série abandonnée introuvable** : après 2 mains d'une série rapide, toucher « SpinsAcademy » ramène sur Défis ; « Reprendre la série en cours » n'existe que dans l'onglet GTO, rien ne la signale ailleurs (pas de badge). Kevin et Mamadou recommencent une série au lieu de reprendre.
5. **Ouvrir l'onglet Exploitant change le niveau affiché** : une débutante qui jette un œil à Exploitant voit ensuite « Niveau 4 · Exploiter le field » sélectionné dans Progression ; revenir sur GTO le remet au niveau 1. Rien ne dit que la progression suit le dernier onglet visité (Nadia : « j'ai monté de niveau ? »).
6. **Les erreurs du jour (N2) ont quitté l'écran d'arrivée** : elles ne sont que dans l'onglet GTO, sans badge, alors que la décision du 09/11 les place sur l'accueil. Après une série fausse et « Retour à l'accueil », on les voit (on atterrit sur GTO) ; en rouvrant l'application, on arrive sur Défis et elles n'y sont pas (Léa, Kevin).

### Moyens
7. **L'onglet « Défis » est d'abord la séance du jour** : son titre est « Aujourd'hui », les défis viennent dessous. Pour « retrouver la séance du jour », quatre profils sur six cherchent d'abord dans GTO ; Jean-Pierre : « Défis, je pensais que c'était facultatif ». Et il y a **deux séances du jour** (GTO dans Défis, Exploitant dans l'onglet Exploitant), sans lien entre elles.
8. **« Retour à l'accueil » sans accueil** : bilan de série, séance, fiches et progression gardent ce lien. Il ramène à l'onglet d'où vient la série (Défis après la séance, GTO après une série rapide), ce qui est logique, mais le mot « accueil » ne correspond plus à rien (« Retour » ou le nom de l'onglet).
9. **Textes qui renvoient à l'ancien accueil** : « bouton « Revoir mes mains » sur l'accueil » (bilan ; le bouton est dans GTO) ; « relève le défi du jour depuis l'accueil » (Mes défis).
10. **Bilan de série en termes anglais au niveau 1** : « Ton coup : FOLD (coûte 1,26 BB) · Meilleur coup : ALL-IN 8 BB », alors que la correction de la même série parle français (AU8) (Nadia).
11. **Test de placement rangé sous le pli** de Progression (à 1 113 px, sous « Mon niveau ») : Sofiane ne le trouve qu'en faisant défiler, après être passé par Outils.
12. **Objectifs de la semaine** : plus visibles à l'arrivée, repliés au milieu de Progression (Kevin les cherche sur Défis).

### Mineurs
13. Profil : icône seule, sans libellé ; la feuille ne se ferme pas avec Échap (clavier) ; elle s'ouvre sur « Mes pastilles », que Nadia ne comprend pas, l'historique annoncé n'y est pas.
14. Lexique présent deux fois (en-tête et Outils) : pas gênant, à garder ou à choisir.
15. Le chrono de la série rapide est sur 15 s pour une débutante qui n'a rien réglé (Mamadou s'en étonne).

## 3. La barre jugée par les profils

| Tâche | Constat (mesuré) | Avis |
|---|---|---|
| Trouver les fiches, le conseiller | Outils, 1 toucher, quatre tuiles lisibles (« Comment jouer ma main ? », « Fiches à emporter », « Construis ta range », « Lexique ») | réussi par les six |
| Trouver la progression | onglet Progression, 1 toucher | réussi par les six |
| Trouver le test de placement | Progression, sous le pli (1 113 px) ; proposé au premier lancement aux confirmés | Sofiane le trouve en 3 essais ; Kevin passe d'abord par Outils |
| Comprendre le cadenas Exploitant | pas de cadenas affiché pendant le test, bandeau « Offre payante, ouverte à tous pendant le test » | compris par cinq sur six ; Jean-Pierre veut savoir combien ça coûtera |
| Retrouver la séance du jour | onglet Défis, titre « Aujourd'hui », bouton plein à 470 px | trouvé, mais après un détour par GTO pour quatre profils |
| Savoir où est le profil | icône en haut à droite, sans libellé | Mamadou et Jean-Pierre ne l'ouvrent pas d'eux-mêmes |
| Pendant une série | barre masquée (question, correction, bilan) | apprécié : rien ne distrait |
| Après une série | « Retour à l'accueil » → l'onglet d'où vient la série, barre revenue | compris ; le mot « accueil » gêne Jean-Pierre |
| Après un abandon | retour sur Défis, « Reprendre » seulement dans GTO | Kevin et Mamadou ne la retrouvent pas |

## 4. Ce qui était sur l'ancien accueil et où c'est maintenant

| Ancien accueil | Maintenant | Retrouvé par les profils ? |
|---|---|---|
| Séance du jour, série de jours, niveau, gains, carte « Ton but », défis | Défis | oui |
| Série rapide, chrono, « Choisir le thème », « Reprendre la série », « Revoir mes mains », recommandations, erreurs du jour | GTO (et Exploitant pour son mode) | en partie : « Reprendre » et les erreurs du jour ne sont plus à l'arrivée (défauts 4 et 6) |
| Objectifs de la semaine | Progression, replié | difficilement (défaut 12) |
| Fiches, « Construis ta range », conseiller | Outils | oui |
| Choix GTO / Exploitant | onglets GTO et Exploitant | oui, mais il change aussi le niveau affiché (défaut 5) |
| Mes pastilles | feuille du profil | non pour Nadia, oui pour Léa |
| Titre « Entraînement libre » | supprimé | sans manque |

## 5. Recettes habituelles (même `SPINSACADEMY_DATASET=2026.11.07-s2` que le serveur)

| Recette | Application | Démo |
|---|---|---|
| `e2e_audit_recette.cjs` (AU3, AU4, AU5, AU8) | 10 / 10 | — |
| `e2e_placement_recette.cjs` (AU7) | **arrêtée** : le test de placement ne démarre pas (défaut 2) | — |
| `e2e_test_ferme.cjs` (P15, 8-16 BB) | 7 / 7 | — |
| `e2e_rythme_recette.cjs` (N1, N2) | 13 / 13 | 10 / 10 |
| `e2e_fiches_recette.cjs` (N3) | 8 / 8 | 8 / 8 |

Toutes passent par `tools/web/nav_helper.cjs` (onglet ouvert au besoin) depuis I9. Parcours des profils dans la démo (banque de référence) : séance du débutant, barre masquée puis revenue, abandon et « Reprendre », profil : mêmes constats que dans l'application, sauf les blocages 1 et 2, propres à la banque du test fermé.

## 6. Ce qui plaît
- La barre : cinq mots simples, l'onglet central bien en vue, les badges (défi du jour) remarqués.
- Outils : « enfin un endroit pour le conseiller et les fiches » (Sofiane, Léa).
- La barre masquée pendant une série : plus de place pour la table (Mamadou).
- Le bandeau Exploitant, honnête sur l'offre payante.
- Aucune erreur JavaScript sur tout le parcours, application et démo.
