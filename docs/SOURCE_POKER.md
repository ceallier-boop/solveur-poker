# Sources poker : références pour fiabiliser les résultats

Synthèse de la recherche du 14 octobre 2026. But : trouver des références externes pour contrôler les modèles de SpinsAcademy (push/fold, HRC, chip EV, solveur postflop).

## 1. Point de départ : le fil Kill Tilt (sans valeur technique)

[« La stratégie réelle des expressos »](https://www.kill-tilt.fr/forums/topic/la-strategie-reelle-des-expressos/), forum Kill Tilt, 16 et 17 septembre 2016, 3 messages.

- Plasmaja présente les Expressos comme un accélérateur de trafic et de rake. Selon lui, ils rendent les joueurs impatients dans tous les formats (« le poker émotionnel tue le poker stratégique »).
- Pe4nuts lui objecte la responsabilité individuelle : on peut jouer ce format de façon raisonnée.
- L'auteur conclut que son post était écrit au second degré.

Le fil ne contient aucune range, aucun seuil en BB, aucun calcul de ROI ou de rake, aucune main commentée. **À ne pas citer comme référence.**

## 2. Contrôle réalisé : push/fold heads-up contre HoldemResources

Référence : équilibre Nash heads-up en push/fold publié par HoldemResources. Il est disponible en [tables](https://www.holdemresources.net/hune) et en [archive CSV](https://www.holdemresources.net/hrdata/holdemresources_hu_equilibrium.zip) (pas de 0,05 BB de 1 à 200 BB, fichiers datés de 2012, sans ante).

Comparaison avec `spinsacademy/pushfold.py` (`heads_up`) :

| BB | Push : SpinsAcademy / HRC (% des combos) | Call : SpinsAcademy / HRC | Classes qui diffèrent (écart de fréquence > 0,5) |
|---|---|---|---|
| 2 | 89,4 / 89,4 | 100,0 / 100,0 | aucune |
| 3 | 77,5 / 78,0 | 92,4 / 92,3 | 85o (push) |
| 4 | 73,8 / 73,8 | 73,8 / 74,1 | aucune |
| 5 | 71,5 / 71,5 | 62,1 / 62,1 | 95s (call) |
| 6 | 68,4 / 68,3 | 54,4 / 54,4 | aucune |
| 8 | 61,9 / 61,9 | 45,1 / 45,0 | aucune |
| 10 | 58,3 / 58,3 | 37,3 / 37,4 | aucune |
| 12 | 53,3 / 53,2 | 33,1 / 33,0 | aucune |
| 14 | 48,3 / 48,4 | 29,4 / 29,3 | aucune |
| 15 | 45,7 / 45,7 | 28,5 / 28,5 | aucune |
| 16 | 44,8 / 44,8 | 26,4 / 26,5 | aucune |
| 18 | 42,5 / 42,3 | 23,8 / 23,8 | aucune |
| 20 | 40,2 / 40,2 | 21,8 / 21,7 | aucune |
| 25 | 36,2 / 36,3 | 17,5 / 17,3 | K4s (push) |

**Conclusion : le moteur heads-up est validé.** Aucun écart ne dépasse 0,5 point, et les 3 classes qui diffèrent sont des mains à la limite de l'indifférence.

Remarques :
- `docs/audit/AUDIT_PHASE0.md` indique 57,8 % de push à 10 BB. Le moteur actuel et HRC donnent tous les deux 58,3 %. C'est probablement une ancienne valeur de `legacy/`.
- Ce contrôle peut devenir un test de non-régression. La licence des CSV HoldemResources est à vérifier avant de les mettre dans le dépôt (lien avec le point 27 du plan d'évaluation : droits HRC).

## 3. Références académiques

### Push/fold à 3 joueurs (`three_way_button`, mode exploitant)
- Ganzfried et Sandholm, *Computing an Approximate Jam/Fold Equilibrium for 3-player No-Limit Texas Hold'em Tournaments*, AAMAS 2008 ([PDF](https://aamas.csc.liv.ac.uk/Proceedings/aamas08/proceedings/pdf/paper/AAMAS08_0313.pdf), [CMU](https://kilthub.cmu.edu/articles/journal_contribution/Computing_an_Approximate_Jam_Fold_Equilibrium_for_3-player_No-Limit_Texas_Hold_em_Tournaments/6604343)). Même problème que le nôtre : 3 joueurs, jam/fold, résolu par jeu fictif.
- Ganzfried et Sandholm, *Computing Equilibria in Multiplayer Stochastic Games of Imperfect Information*, IJCAI 2009 ([résumé](https://www.ijcai.org/Abstract/09/034), [CMU](https://kilthub.cmu.edu/articles/journal_contribution/Computing_Equilibria_in_Multiplayer_Stochastic_Games_of_Imperfect_Information/6604361)). Ils montrent qu'à 3 joueurs, le jeu fictif peut converger vers un non-équilibre. Ils proposent un contrôle a posteriori : calculer ce que chaque joueur gagnerait à dévier (la meilleure réponse). Leur epsilon est de 0,5 % de la mise d'entrée. **Ce contrôle est à appliquer à notre moteur à 3 joueurs.**

### Validité du push/fold en heads-up
- Miltersen et Sørensen, *A Near-Optimal Strategy for a Heads-Up No-Limit Texas Hold'em Poker Tournament*, AAMAS 2007 ([PDF](https://www.itu.dk/~trbj/papers/poker.pdf)). Une stratégie jam/fold perd au plus 1,4 point de probabilité de victoire face à une stratégie optimale sans restriction. C'est une borne de l'erreur du module push/fold face à l'arbre HRC complet.

### Solveur postflop (`docs/solver/CONTROLE_ABSTRACTION.md`)
- Bowling, Burch, Johanson et Tammelin, *Heads-up Limit Hold'em Poker is Solved*, Science 2015 ([page](https://webdocs.cs.ualberta.ca/~bowling/publications/b2hd-15science.html)).
- Tammelin, Burch, Johanson et Bowling, *Solving Heads-up Limit Texas Hold'em*, IJCAI 2015 ([PDF](https://www.cs.ualberta.ca/~games/poker/publications/2015-ijcai-cfrplus.pdf)). C'est la référence de CFR+, l'algorithme du contrôle exact.
- Brown et Sandholm, *Solving Imperfect-Information Games via Discounted Regret Minimization*, AAAI 2019 ([arXiv 1809.04040](https://alphaxiv.org/abs/1809.04040)). Discounted CFR, qui fait mieux que CFR+.

### ICM (point 20 du plan d'évaluation)
- Kim, *Empirical Validation of the Independent Chip Model*, IEEE CoG 2025 ([arXiv 2506.00180](https://arxiv.org/abs/2506.00180v1)). Validation sur plus de 10 000 tournois réels, avec un jeu de données public sur Zenodo. L'ICM sous-estime les gros tapis et surestime les petits.

## 4. Hypothèses du format Expresso (Winamax)

### Distribution des multiplicateurs, Expresso à 1 €
Source : [pokersciences.com, chapitre « Jackpots et rake »](https://pokersciences.com/learn/spin/part-1/chapter-2) (source tierce, date de relevé non précisée).

| Multiplicateur | Probabilité |
|---|---|
| x2 | 5 938 688 / 10 M (59,4 %) |
| x3 | 2 674 208 / 10 M (26,7 %) |
| x4 | 825 000 / 10 M (8,25 %) |
| x5 | 400 000 / 10 M (4 %) |
| x10 | 150 000 / 10 M (1,5 %) |
| x50 | 10 000 / 10 M (0,1 %) |
| x100 | 2 000 / 10 M (0,02 %) |
| x1 000 | 100 / 10 M (0,001 %) |
| x100 000 | 4 / 10 M |

### Rake
Les jackpots redistribuent 27,9 M€ sur 30 M€ de mises, soit un **rake de 7 %**. Il est de 8 % aux buy-ins de 0,25 et 0,50 € ([pokersciences.com](https://pokersciences.com/articles/expresso-winimax-guide-complet), [Winamax Espagne](https://www.winamax.es/noticias_expresso-un-cambio-sutil-44283?param=expresso-un-cambio-sutil-44283)).

### Ce qui justifie le chip EV
Les multiplicateurs de x50 et plus ne représentent qu'environ **4,3 % de l'argent redistribué** (1,2 M€ sur 27,9 M€). Si seul le x100 000 paie plusieurs places, c'est 1,4 %. Les sources ne s'accordent pas sur le seuil de partage des gains : 80 / 12 / 8 selon [Winamax](https://www.winamax.fr/expresso) pour le jackpot maximal, à partir de x50 selon d'autres guides. Dans plus de 95 % de l'espérance de gain, le gagnant prend tout, ce qui justifie le chip EV. L'ICM ne concerne que les gros multiplicateurs, ce qui confirme la décision du point 20.

### Structure
500 jetons, blinds 10/20, donc 25 BB au départ. C'est cohérent avec les profondeurs calculées. Les sources ne s'accordent pas sur la durée des niveaux (1 min 30 d'après Winamax Espagne, 3 min ailleurs). Sans incidence sur le chip EV par main.

**À faire :** les pages officielles winamax.fr et winamax.es renvoient une erreur 403 aux requêtes automatiques. Relever et dater la table officielle sur [winamax.fr/expresso](https://www.winamax.fr/expresso) avant de citer ces chiffres comme référence. Winamax a modifié sa table plusieurs fois (par exemple, le x2 est passé de 74 % à 64,2 % d'après [PokerNews, 2014](https://fr.pokernews.com/news/2014/12/winamax-nouveaux-expressos-structure-gains-probabilite-stat-19725.htm)).

## 5. Ce qui reste sans référence externe

| Sujet | État | Contrôle possible |
|---|---|---|
| Ranges HRC à 3 joueurs avec limp et relances | aucune source publique pour les recouper | contrôles internes existants (bruit Monte-Carlo, EV exacte des calls, CFR+ exact), plus une meilleure réponse à la manière de Ganzfried et Sandholm |
| Push/fold à 3 joueurs | non comparé | [calculateur Nash de HoldemResources](https://www.holdemresources.net/nashicm) réglé sur 100 / 0 / 0 (l'ICM revient alors au chip EV) |
| Seuils de 20 et 60 mBB | aucune norme publiée | relecture experte (point 14 du plan d'évaluation) |
| Abstraction postflop de HRC | pas de documentation officielle trouvée, seulement des posts de forum ([fil de support HRC](https://www.pokerstrategy.com/forum/poker-tools-1361/official-support-thread-holdemresources-calculator-213128/paged/24/), [PokerNews](https://www.pokernews.com/strategy/holdemresources-calculator-simple-preflop-holdem-39096.htm)) | contrôle exact existant (`docs/solver/CONTROLE_ABSTRACTION.md`) |

## 6. Suites proposées

1. Ajouter la comparaison heads-up de la section 2 comme test de non-régression, après avoir vérifié la licence des CSV.
2. Comparer `three_way_button` (BTN tapis ou fold) au calculateur Nash de HoldemResources réglé sur 100 / 0 / 0.
3. Ajouter un calcul de meilleure réponse (gain à dévier) sur l'équilibre à 3 joueurs.
4. Relever et dater la table officielle des multiplicateurs Winamax.
5. Corriger la valeur de 57,8 % dans `docs/audit/AUDIT_PHASE0.md` (58,3 % mesuré).
