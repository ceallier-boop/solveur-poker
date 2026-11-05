# Décisions du porteur du projet, 05/11/2026

Source de vérité pour toutes les interfaces. Chaque règle dit qui la met en œuvre ; le suivi est dans le document de suivi (lignes P7 à P9, I8, D8, T8).

## Règles tranchées

| # | Sujet | Décision | Mise en œuvre |
|---|---|---|---|
| 1 | Mode exploitant | L'onboarding présente le mode exploitant. Il **reste payant**. | Interface (I8) pour l'écran ; Plan (P8) pour le droit d'accès |
| 2 | Désaccord entre coachs | Quand les coachs ne sont pas d'accord, l'application **présente les deux stratégies comme possibles**. Avec trois coachs, une stratégie est souvent portée par un seul et l'autre par les deux autres : cela peut servir à **recommander l'une plutôt que l'autre, en précisant la nuance** (par exemple « 2 coachs sur 3 »). Les mains sans consensus (par exemple le limp de AA à JJ entre 5 et 10 BB) ne sont donc plus exclues des questions. | Plan (P7) : règle et serveur ; Interface (I8) : affichage |
| 3 | Tests des coachs (T6) | On rejoue **toutes** les réponses des coachs, y compris celles où ils sont en désaccord. Pour un désaccord, les deux actions des coachs doivent être acceptées par la correction. | Tests (T8) |
| 4 | Banque du solveur | Utilisable en **test fermé** de 8 à 16 BB, en sachant que le moteur GTO va encore évoluer : chaque banque servie porte sa version et reste en staging tant que Plan ne l'a pas publiée. | Plan (P9) |
| 5 | Comptes (A16) | **Invité d'abord**, comptes ensuite. | voir « Conséquence à trancher » ci-dessous |
| 6 | Journal d'usage (A17) | **Oui, anonyme**, sans identifiant personnel. | Défis et rétention (D1), après la mise à jour de la politique de confidentialité |
| 7 | Rappels (D6) | **Plus tard**, avec les comptes. | rien avant les comptes |
| 8 | Offre (B4) | **Gratuit** : séance du jour, modes GTO, défis. **Payant** : mode exploitant complet, révision espacée, statistiques détaillées. **Dans les défis, le dernier est déblocable avec de la publicité.** | Défis (D8) pour les défis ; Plan (P8) pour le droit d'accès |
| 9 | Hébergeur (A15) | Cahier des charges demandé : `docs/exploitation/CAHIER_HEBERGEUR.md`. | Plan, fait |

## Conséquences que Plan a repérées (à trancher)

1. **Payant et invité ne vont pas ensemble tel quel.** Un achat lié à un appareil invité est perdu avec l'appareil. Proposition : **le compte n'est demandé qu'au moment d'acheter** (adresse de courriel et lien de connexion), le reste reste en invité.
2. **La publicité contredit la politique de confidentialité actuelle** (« aucun cookie publicitaire, aucun service tiers »). Il faut un bandeau de consentement et la réécriture de la politique, relues par un juriste (A14), avant d'activer quoi que ce soit.
3. **Quel est « le dernier défi » ?** La liste actuelle est : du jour, parfait ; de la semaine, pression, range, lecteur (exploitant) ; du mois, semaine complète. À préciser avant que Défis le code.
4. **Test fermé et mode exploitant** : tant que le paiement n'existe pas, le mode exploitant reste **ouvert** pendant le test fermé (hypothèse de Plan : on teste le produit, pas la caisse).
5. **Révision espacée et statistiques détaillées** sont aujourd'hui gratuites dans le code : Plan propose la frontière gratuit / payant (P8) avant que quiconque ne verrouille quoi que ce soit.

## Non encore tranché

T7 (tests automatiques sur GitHub, recommandé : oui), A18 (relecture de l'échantillon du 14/10, recommandé : la déclarer remplacée par l'audit du 22/10), achat des domaines SpinXpresso, format de l'historique de mains.
