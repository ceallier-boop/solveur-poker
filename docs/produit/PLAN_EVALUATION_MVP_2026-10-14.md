# Plan d'action : évaluation du MVP du 14 octobre 2026

Source : « SpinsAcademy — Évaluation du MVP » (@Charles, 14/10/2026), sur le commit `76ca428`, datasets `gto_preflop/2026.10.13-3` et `exploit_calls/2026.10.13-4`. Note globale 5,8/10 : bêta fermée oui, vente non.

## 1. Synthèse

| Axe (poids) | Note | En une phrase |
|---|---|---|
| A. Pédagogie (25 %) | 6,3 | Séries courtes et correction immédiate réussies ; le « pourquoi » décrit plus qu'il n'explique ; la progression donne trois diagnostics contradictoires |
| B. Fiabilité et couverture poker (30 %) | 5,0 | Juste et traçable sur son périmètre, mais ce périmètre n'est pas le jeu Expresso réel : 7 % de heads-up, décisions serrées filtrées, exploitant limité au call d'un tapis |
| C. Mobile (20 %) | 7,5 | Aucun défaut à 390 px, rapide (40 ms) ; bouton « Question suivante » à atteindre en défilant, grille ambiguë, `alert()` |
| D. Maturité technique (10 %) | 7,5 | Publication contrôlée, sauvegardes, tests ; tests en échec sans les exports bruts, script e2e périmé |
| E. Prêt pour la vente (15 %) | 3,3 | Droits HRC, comptes, paiement, confidentialité, rétention |

Le point commun des trois évaluateurs : **la fiabilité est réelle sur ce qui est couvert, mais ce qui est couvert ne correspond pas au jeu réel**.

Contrôles refaits le 14/10 sur les mêmes données (2 000 questions tirées) : heads-up 7,1 % ; EV exacte 2 % ; difficulté facile 27 %, moyen 59 %, difficile 14 % ; mains les plus tirées ATo 2,3 %, AA 2,2 %, AKo 2,2 %, KK 2,1 % ; le dataset contient déjà 159 situations et 11 542 questions heads-up tirables ; 304 calls sur 108 187 où la perte HRC dépasse le montant à payer (impossible en chip EV ; l'évaluation en compte 83 avec une définition plus étroite).

## 2. Toutes les remarques et leur traitement

Lot : **0** = immédiat (sans dépendance), **1** = avant la bêta ouverte, **2** = avant la vente. Dépendance : P = décision du porteur du projet, H = nouveaux exports HRC, E = expert externe, J = juridique.

| # | Remarque (évaluateur) | Action | Lot | Dép. |
|---|---|---|---|---|
| 1 | 8 tests échouent sans les exports bruts (mobile) | `pytest.mark.skipif` quand `data/hrc/raw` est absent, avec la raison affichée | 0 | — |
| 2 | `e2e_datasets.cjs` publie d'anciennes versions (mobile) | Lire les versions dans `PUBLICATIONS.md` / le catalogue au lieu de les coder en dur | 0 | — |
| 3 | « Question suivante » à atteindre en défilant (mobile) | Barre d'action fixée en bas de l'écran de correction (zone de sécurité iOS comprise) | 0 | — |
| 4 | Grille : légende sur toute la range, cases grisées non légendées ; « on croit que AQs se couche » (mobile, amateur) | Légende « part des mains qui arrivent à cette décision » ; case grise légendée « n'arrive pas ici (jouée autrement avant) » ; au toucher d'une case, la ligne de la main | 0 | — |
| 5 | Montants HRC aberrants (83 / 304 cas) (poker) | Perte d'un call bornée au montant à payer ; mains concernées retirées des questions et listées dans le rapport de contrôle | 0 | — |
| 6 | Trop de questions évidentes, AA trop fréquent (amateur) | Tirage pondéré par la difficulté (faciles ÷ 4 → ÷ 10), plafond par main dans une série, viser facile ≤ 15 % | 0 | P (cible) |
| 7 | Heads-up 7 % au lieu de 35-40 % (poker, amateur) | Rotation du tirage sur le format (heads-up / 3 joueurs) avant la position, cible 35 % de heads-up avec les 11 542 questions déjà disponibles ; puis nouveaux exports heads-up (profondeurs, tailles) | 0 puis 1 | P (cible), H |
| 8 | « Cette main après le flop » promet plus que le contenu (poker) | Renommer « Potentiel de la main au flop » ; le jeu postflop reste au lot 2 | 0 | — |
| 9 | Progression : trois diagnostics qui se contredisent, graphique sans axes (mobile, amateur) | Un seul bloc « À travailler maintenant » (une règle de priorité unique, appliquée aussi aux séries adaptées) ; axes et légende sur le graphique | 1 | — |
| 10 | `alert()` natives (mobile) | Bandeau d'erreur dans l'écran avec « Réessayer » | 1 | — |
| 11 | Impossible de mesurer la bêta (mobile) | Journal d'usage minimal et anonyme : temps de réponse par question, abandon de série, ouverture de « Pourquoi ? », de la grille, retour à J+1 / J+7 ; tableau dans l'administration | 1 | P (consentement) |
| 12 | « Pourquoi ? » décrit sans expliquer ; pas de règle à retenir (poker, amateur) | Après chaque erreur, une « règle à retenir » courte, tirée d'un catalogue de règles par famille, position et profondeur (ex. « BB face au tapis du BTN à 10 BB : paie toute paire et tout As ») ; les pourcentages de range descendent en détail | 1 | E (validation des règles) |
| 13 | Rôle des bloqueurs (grille, poker) | Une ligne « bloqueurs » quand la main retire des combinaisons clés de la range adverse (calculée avec la matrice des combos) | 2 | — |
| 14 | Relecture experte d'un échantillon, seuils 20 / 60 mBB et facteurs des profils non validés (poker : point critique) | Générer un échantillon stratifié de 300 questions (format, famille, position, profondeur, verdict, source d'EV) au format de relecture, avec un formulaire de retour ; intégrer les décisions | 1 | E |
| 15 | Décisions serrées filtrées par le seuil de bruit à 150 mBB (poker) | Exports HRC plus précis (plus d'itérations), puis baisse du seuil par profondeur, mesurée contre l'EV exacte | 1 | H |
| 16 | Une seule taille d'ouverture par arbre ; lignes courtes (poker) | Déjà 6 arbres importés ; ajouter des questions « quelle taille ? » quand deux arbres couvrent la même situation ; exports §7 | 2 | H |
| 17 | Exploitant : seulement le call d'un tapis au BB (poker, amateur) | Étendre sans HRC à l'open-shove contre un joueur qui paie trop (EV exacte avec `allin.shove_ev` et une range de call déformée) ; limps et relances avec des exports verrouillés | 1 puis 2 | H (limps, relances) |
| 18 | « Comment je repère un Nit ? » (amateur) | Fiche « reconnaître ce profil » : signes observables (fréquence de tapis sur N mains, mains montrées), taille d'échantillon nécessaire, avec prudence | 1 | E |
| 19 | Pas de postflop (poker, amateur) | Minimum : pots limpés heads-up à 15-25 BB à partir d'exports postflop HRC ; le solveur maison n'est pas assez précis | 2 | H |
| 20 | Pas d'ICM (poker) | Hors périmètre (décision chip EV) ; à rouvrir pour les gros multiplicateurs | 2 | P |
| 21 | Rétention : pas d'accueil, d'objectif du jour, de série de jours, de rappel (mobile, amateur) | Accueil d'un nouveau joueur (3 écrans) ; objectif quotidien ; série de jours ; révision espacée des erreurs (J+1, J+3, J+7) | 1 (révision) puis 2 | — |
| 22 | Pas de service worker (mobile) | Service worker : mode hors ligne pour l'interface et une série préchargée | 2 | — |
| 23 | Comptes liés à l'appareil (mobile : bloquant pour vendre) | Comptes (courriel ou fournisseur d'identité), rattachement de l'historique invité, synchronisation | 2 | P |
| 24 | Politique de confidentialité (mobile) | Rédiger la politique et les mentions (données traitées, durée, droits, export et effacement déjà présents) | 1 | J |
| 25 | Pas de limitation du nombre de requêtes (mobile) | Limitation par adresse et par joueur sur les routes publiques, au niveau de l'application et du proxy | 1 | — |
| 26 | Jeton d'administration partagé, comparaison non protégée (mobile) | `hmac.compare_digest` tout de suite ; comptes administrateurs nominatifs ensuite | 0 puis 2 | — |
| 27 | Droits HRC non vérifiés : blocage juridique (poker, synthèse) | Clarifier avec HoldemResources les droits sur les données dérivées (licence commerciale ou accord écrit) | dès maintenant | J, P |
| 28 | Paiement, différenciation face aux tableaux push/fold gratuits (amateur, synthèse) | Offre gratuite / payante (`docs/produit/OFFRE.md`) : le payant apporte le heads-up complet, l'exploitant étendu, la révision et les conseils ; paiement par un prestataire | 2 | P |

## 3. Calendrier proposé

**Lot 0, cette semaine (sans dépendance)** : remarques 1 à 8 et 26 (comparaison du jeton). Effet attendu : C à 8, B à 5,5 grâce au heads-up servi à 35 %, et une pédagogie plus juste (moins de questions évidentes, grille claire).

**Lot 1, avant la bêta ouverte (2 à 4 semaines)** : remarques 9 à 12, 14, 15, 17 (open-shove), 18, 21 (révision), 24, 25. Il dépend d'un expert (relecture, règles) et de nouveaux exports HRC (précision, heads-up).

**Lot 2, avant la vente** : remarques 13, 16, 17 (limps et relances), 19 à 23, 26 (comptes administrateurs), 28. Prérequis absolu : remarque 27 (droits HRC).

## 4. Décisions attendues du porteur du projet

1. Part de heads-up visée dans le tirage (proposé : 35 %).
2. Part maximale de questions faciles (proposé : 15 %).
3. Journal d'usage de la bêta : accord sur les événements collectés (anonymes, sans tiers) et sur leur mention dans la politique de confidentialité.
4. Choix de l'expert pour la relecture (300 questions, seuils, facteurs des profils, règles à retenir).
5. Démarche auprès de HoldemResources pour les droits sur les données dérivées.
6. Commande des exports HRC : heads-up à toutes les profondeurs et tailles, précision accrue, tapis direct au-delà de 16 BB (`docs/hrc/EXPORTS_A_PRODUIRE.md` §7 et §8).

## 5. Avancement

**Lot 0 réalisé le 14/10** (cibles validées par le porteur du projet : 35 % de heads-up, au plus 15 % de questions faciles).

| # | Fait | Mesure après correction |
|---|---|---|
| 1 | Tests qui exigent les exports bruts marqués `needs_raw` (`tests/conftest.py`) | sans `data/hrc/raw` : 61 réussis, 15 ignorés, 0 échec ; avec : 76 réussis |
| 2 | `e2e_datasets.cjs` lit les versions dans `PUBLICATIONS.md` | publie `gto_preflop/2026.10.13-3` et `exploit_calls/2026.10.13-4` sur une base neuve |
| 3 | « Question suivante » fixé en bas de l'écran de correction | — |
| 4 | Grille : légende « sur les mains qui arrivent à cette décision », case grise légendée, case touchée détaillée | — |
| 5 | Mains dont la perte HRC d'un call dépasse le montant à payer retirées du tirage (`quiz.impossible_ev`) | 135 551 questions tirables (135 853 avant) |
| 6 | Questions faciles tirées à dessein 6 % du temps, aucune main répétée dans une série, poids d'atteinte en racine carrée | faciles 11,8 % (27 % avant) ; AA 1,7 % (2,2 % avant) ; démo : 5 % |
| 7 | Rotation sur le format avant la position (`quiz.HU_SHARE` = 0,35), démo comprise | heads-up 34 % (7 % avant) ; démo : 36 % ; positions : BTN 21 %, SB 40 %, BB 39 % |
| 8 | Section renommée « Potentiel de la main au flop » | — |
| 26 | Jeton d'administration comparé à temps constant (`hmac.compare_digest`) | — |
