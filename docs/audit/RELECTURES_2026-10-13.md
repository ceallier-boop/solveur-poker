# Relectures croisées du 2026-10-13

Trois relecteurs indépendants, puis une discussion écrite entre eux :
- **A**, joueur d'Expresso, relecture des textes de correction : 6/10 ;
- **B**, spécialiste interface, sans connaître l'application : 6,5/10 ;
- **C**, coach de tournois courts, contenu poker, sans connaître l'application : 5/10.

Rapports complets et discussion : dossier de travail de la session (non versionné). Les points sont repris ici avec leur suite.

## Constats partagés par plusieurs relecteurs

| Constat | Relecteurs | Suite |
|---|---|---|
| L'action affichée, la grille et les parts contredisent l'EV exacte (100 mains), « à peine mieux que le fold » pour une action moins bonne que le fold (594 mains) | A, B, C | Corrigé : en EV exacte, la stratégie de référence est l'action la plus rentable (`grading.reference_freq`) ; une seule source par écran |
| Profils exploitants sur une range de tapis irréaliste (le SB de l'arbre de référence limpe AA à QQ) | C, A | Corrigé : générateur 2.0.0, référence à l'équilibre push/fold (`spinsacademy/pushfold.py`), dataset `exploit_calls/2026.10.13-3`, profils 1.4.0 |
| Notation fine (0,02 / 0,06 BB) sur une EV de référence bruitée (écart médian 58 mBB avec l'EV exacte) | C, A | Seuils inchangés (règle du porteur) ; les questions de référence dont la leçon coûte moins de 150 mBB ne sont plus tirées (`quiz.REF_NOISE_MBB`) : 27 364 questions restent |
| Tapis effectif faux à 3 joueurs (minimum de tous les tapis) | A, C | Corrigé à l'affichage (`quiz.hero_effective`) ; le champ `effective_stack_bb` des données, utilisé pour les filtres de profondeur, reste celui de l'importeur |
| « Pourquoi ? » donne des fréquences, pas de raison | A, C, B | Corrigé : une phrase de principe visible (fold equity tirée des spots suivants, piège avec une main très forte, cote du pot, joueur derrière) ; les chiffres restent dans « Pourquoi ? » |
| Correction : le choix du joueur n'apparaît pas face à la référence ; redites | B, A | Corrigé : bandeau « Tu as joué · Référence », toutes les options affichées avec la tienne marquée, redites retirées |
| Vert et rouge à double sens (verdicts et actions) | B | Corrigé : couleurs d'action neutres |
| « Et ensuite ? » creux ou contradictoire (après un fold, face à un tapis) | B, C, A | Corrigé : section masquée après un fold et face à un tapis sans joueur derrière ; comparaison aux mains du même type avec un seuil de 3 points ; renommée « Cette main après le flop » |

## Décisions du porteur du projet

1. Profils : refaire sans nouvel export de référence (équilibre push/fold). Fait.
2. Bruit de référence : filtrer le tirage, sans toucher aux seuils. Fait.
3. Vocabulaire : garder les termes des joueurs (fold, range, tapis, limp). Le lexique les explique.
4. Couverture : ajouter les situations manquantes à la liste d'exports (`docs/reference/EXPORTS_A_PRODUIRE.md` §7). Fait.

## Autres corrections

- Bornes 0,02 et 0,06 BB incluses comme dans la notation ; tout près d'une borne, « un peu plus / un peu moins de » ou 3 décimales ; le montant exploitant part de l'écart non arrondi.
- « Autre option » au lieu de « deuxième option » ; pourcentages cités = barres affichées ; « pile au seuil » ; deux décimales quand une main tombe sur le seuil affiché ; « décision serrée » convertie en BB.
- Historique à la 2e personne (« Tu relances à 3,5 BB ») ; tapis adverse affiché en BB effectifs ; heads-up : « l'adversaire ».
- Périmètre : situations sous 4 BB retirées du tirage ; exploitant : situations sans adaptation retirées, adaptations jamais tirées d'un call indifférent à l'équilibre.
- Interface : consigne visible, cartes dans la correction, filtres exploitants sans question masqués, message d'erreur visible, grille plus lisible avec la ligne de ta main, focus retenu dans le lexique, verdict annoncé aux lecteurs d'écran, cibles de 44 px, coquilles.
- Lexique 1.4.0 : kicker, station d'appel, cote du pot (rapport), tapis effectif, référence ; open-shove, iso-shove, sur-call, squeeze, piège, fold equity, Nash.

## Restent ouverts

- Calls heads-up face à un tapis après limp ou relance (`SB-call_BB-allin`, `SB-raise3.5_BB-allin`) : l'EV exacte est calculable mais demande une nouvelle importation du dataset GTO (ajout à `allin.CALL_NODES`).
- Couverture et arbre (tapis au-delà de 16 BB, BTN après sa première action, multiway, tailles d'ouverture) : nouveaux exports de référence (§7).
- Approximation à 3 joueurs (cartes du joueur couché non retirées) à mesurer.
- Interface : thème clair/sombre choisi dans l'application, deux colonnes sur grand écran, erreurs réseau sans `alert()`, bilan cliquable, barres de progression partielles.
- Fourchettes exploitantes : la fourchette 0,06 à 0,5 BB couvre beaucoup d'adaptations (palier à 0,2 BB suggéré par C) ; bornes fixées par le porteur, à rediscuter.
