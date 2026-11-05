# Décisions du porteur du projet, 05/11/2026

Source de vérité pour toutes les interfaces. Chaque règle dit qui la met en œuvre ; le suivi est dans le document de suivi (lignes P13 à P15, I8, D8, T9).

## Règles tranchées

| # | Sujet | Décision | Mise en œuvre |
|---|---|---|---|
| 1 | Mode exploitant | L'onboarding présente le mode exploitant. Il **reste payant**. | Interface (I8) pour l'écran ; Plan (P14) pour le droit d'accès |
| 2 | Désaccord entre coachs | Quand les coachs ne sont pas d'accord, l'application **présente les deux stratégies comme possibles**. Avec trois coachs, une stratégie est souvent portée par un seul et l'autre par les deux autres : cela peut servir à **recommander l'une plutôt que l'autre, en précisant la nuance** (par exemple « 2 coachs sur 3 »). Les mains sans consensus (par exemple le limp de AA à JJ entre 5 et 10 BB) ne sont donc plus exclues des questions. | Plan (P13) : règle et serveur ; Interface (I8) : affichage |
| 3 | Tests des coachs (T6) | On rejoue **toutes** les réponses des coachs, y compris celles où ils sont en désaccord. Pour un désaccord, les deux actions des coachs doivent être acceptées par la correction. | Tests (T9) |
| 4 | Banque du solveur | Utilisable en **test fermé** de 8 à 16 BB, en sachant que le moteur GTO va encore évoluer : chaque banque servie porte sa version et reste en staging tant que Plan ne l'a pas publiée. | Plan (P15) |
| 5 | Comptes (A16) | **Invité d'abord**, comptes ensuite. | voir « Conséquence à trancher » ci-dessous |
| 6 | Journal d'usage (A17) | **Oui, anonyme**, sans identifiant personnel. | Défis et rétention (D1), après la mise à jour de la politique de confidentialité |
| 7 | Rappels (D6) | **Plus tard**, avec les comptes. | rien avant les comptes |
| 8 | Offre (B4) | **Gratuit** : séance du jour, modes GTO, défis. **Payant** : mode exploitant complet, révision espacée, statistiques détaillées. **Dans les défis, le dernier est déblocable avec de la publicité.** | Défis (D8) pour les défis ; Plan (P14) pour le droit d'accès |
| 9 | Hébergeur (A15) | Cahier des charges demandé : `docs/exploitation/CAHIER_HEBERGEUR.md`. | Plan, fait |

## Conséquences que Plan a repérées (à trancher)

1. **Payant et invité ne vont pas ensemble tel quel.** Un achat lié à un appareil invité est perdu avec l'appareil. Proposition : **le compte n'est demandé qu'au moment d'acheter** (adresse de courriel et lien de connexion), le reste reste en invité.
2. **La publicité contredit la politique de confidentialité actuelle** (« aucun cookie publicitaire, aucun service tiers »). Il faut un bandeau de consentement et la réécriture de la politique, relues par un juriste (A14), avant d'activer quoi que ce soit.
3. **Quel est « le dernier défi » ?** La liste actuelle est : du jour, parfait ; de la semaine, pression, range, lecteur (exploitant) ; du mois, semaine complète. À préciser avant que Défis le code.
4. **Test fermé et mode exploitant** : tant que le paiement n'existe pas, le mode exploitant reste **ouvert** pendant le test fermé (hypothèse de Plan : on teste le produit, pas la caisse).
5. **Révision espacée et statistiques détaillées** sont aujourd'hui gratuites dans le code : Plan propose la frontière gratuit / payant (P14) avant que quiconque ne verrouille quoi que ce soit.

## Non encore tranché

T7 (tests automatiques sur GitHub, recommandé : oui), A18 (relecture de l'échantillon du 14/10, recommandé : la déclarer remplacée par l'audit du 22/10), achat des domaines SpinXpresso, format de l'historique de mains.

## Fiabilité des banques du solveur (Moteur GTO, 05/11)

| Banque | Arbre | Plage fiable | Remarques |
|---|---|---|---|
| `2026.10.29-s1` (pilote) | ouvertures 2,3 et 3,5 BB | 8 à 12 BB | calée sur la référence (12 mBB d'écart en heads-up 12 BB, 55 en heads-up 25 BB, 42 à 3 joueurs 12 BB, 100 à 3 joueurs 25 BB) ; ne correspond plus à l'arbre v5 |
| `2026.11.02-s2` (v5, sans correction G17) | v5, ouvertures à 2 BB | 8 à 16 BB pour les décisions qui finissent à tapis ou face à un tapis | fragile, à toute profondeur, sur les décisions qui mènent au flop dans un pot relancé (140 à 400 mBB par main) ; à 8 BB, les As de celui qui paie la relance sont sous-évalués d'environ 600 mBB ; non fiable au-delà de 16 BB ; calée sur aucune référence v5 |
| `2026.11.04-s3` (O7, avec g17-v1) | v5 | 8 à 25 BB attendus | meilleure que s2 sur les pots relancés dès 12 BB ; identique à s2 en dessous de 12 BB ; **à confirmer par comparaison avec s2** |

## Filtre anti-bruit des questions (`quiz.REF_NOISE_MBB` = 150 mBB), pour P15

Le filtre écarte les questions dont la leçon coûte moins de 150 mBB, parce que l'EV de la référence était bruitée. Une banque du solveur n'a pas ce bruit (pas de Monte-Carlo), mais elle a l'erreur d'abstraction de la ligne ci-dessus. Plan propose donc, sans le coder avant d'avoir la banque s3 :
- décisions qui finissent à tapis ou face à un tapis : seuil abaissé (de l'ordre de 20 mBB, `grading.TOLERANCE_MBB`), le solveur y est précis ;
- décisions qui mènent au flop : seuil de 150 mBB conservé tant que l'erreur d'abstraction mesurée est de cet ordre.
Le champ d'écart d'EV entre actions existe déjà dans chaque spot (`hands[h].ev_hrc`, dans l'ordre de `actions`) : pas de nouveau champ à ajouter.

## Réponses du 05/11 (suite) et propositions à valider

Acquis : compte demandé seulement à l'achat ; réécriture de la politique de confidentialité avec bandeau de consentement avant toute publicité ; mode exploitant ouvert pendant le test fermé ; filtre anti-bruit abaissé pour les décisions qui finissent à tapis (code après la banque s3) ; tests automatiques sur GitHub (T7) ; relecture de l'échantillon du 14/10 déclarée remplacée par l'audit du 22/10 (A18) ; format de l'historique de mains : **Winamax**.

### Défis : partage gratuit / publicité (demandé par le porteur, à valider)

Aucun niveau ni objectif ne dépend d'un défi : fermer un défi ne bloque jamais la progression.

| Catégorie | Défis | Raison |
|---|---|---|
| **Gratuits** | Défi du jour, Sous pression, Semaine complète | le défi du jour est le rendez-vous quotidien ; Semaine complète se gagne en s'entraînant et n'a pas de bouton |
| **Avec publicité** (une publicité = les deux défis du jour) | Série parfaite, Range au cordeau | deux défis optionnels et exigeants ; au plus une publicité par jour, jamais pendant la séance |
| **Payant** | Lecteur de vilain | fait partie du mode exploitant |

Repli : abonné sans publicité ; pas de publicité disponible = ouvert ; bloqueur ou refus de consentement = fermé avec un message neutre. Risque connu (note de Défis) : fermer un défi qui était gratuit peut mal passer auprès des testeurs ; pendant le test fermé, tout reste ouvert sans publicité.

### Frontière gratuit / payant (P14, à valider)

| | Gratuit | Payant |
|---|---|---|
| Séance du jour (15 min), modes GTO | oui, avec des nouvelles questions et le thème le plus faible | oui, avec en plus la révision espacée de tes erreurs (rappel à 1, 3 et 7 jours) |
| Progression | niveau, objectifs, série de jours, score par thème | statistiques détaillées : par famille de mains, position, profondeur, évolution dans le temps |
| Bilan de série | questions ratées de la série | idem |
| Mode exploitant | présenté à l'onboarding, verrouillé après le test fermé | oui |

Conséquence : la révision espacée est aujourd'hui intégrée à la séance du jour (`today.REVIEW_CAP`) ; pour un joueur gratuit, ces places passent à des nouvelles questions.
