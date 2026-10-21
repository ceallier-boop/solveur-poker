# Relecture Lucho : BB face au limp du SB (60 questions, 21/10/2026)

**Bilan.** 59 réponses validées, 0 fausse, 1 incertaine (L35). Le moteur prend les bonnes décisions. Ce qui coince, c'est le texte. Gravité : 1 bloquant, 32 majeurs, 16 mineurs, 11 sans remarque.

**(a) Doctrine face au limp du SB.**
- **6 BB (pot 2, il reste 5).** Pas d'iso intermédiaire : relancer à 2,5 BB t'engage déjà. Tapis très large contre un rec, car son limp est faible et le field se couche trop face au push : tous les Kx, les Qx, les suited, les connecteurs, les petites paires. On checke le vrai trash qui a de la jouabilité (en BvB), et AA/KK pour piéger.
- **8 BB.** Même logique. Le tapis reste l'arme principale, et on peut pousser de la poubelle (72o, 54o) contre un SB qui se couche à plus de 70 %. Contre une calling station, garde le tapis pour les mains qui battent ses calls, et checke le reste.
- **10-12 BB.** L'iso non all-in (2,5 à 3 BB) devient meilleure que le tapis avec les mains qui dominent (AK, AQ, KQ, AJ, 99+). On veut garder ses Ax et Kx dominés, et ce sont des mains qu'on peut payer face à un limp-jam. Le tapis reste pour les mains à fold equity (Ax faibles, Kx, petites paires) et pour les bluffs. On checke les mains jouables moyennes. L'appli ne propose pas l'iso : il faudrait l'ajouter au moins à partir de 10 BB (L47 QJs, L60 AKo).
- **HU contre BvB.** En BvB (BTN couché), le BB joue en position après le flop : checker les mains jouables est rentable. En HU, le SB est au bouton et le BB parle en premier après le flop : le check réalise mal, donc on pousse plus et on checke moins. Les fréquences théoriques de l'appli le reflètent bien : le SB limp 8-16 % en BvB contre 14-57 % en HU. Seuls les textes se trompent de position.

**(b) Erreurs du moteur.**
- Pas d'excès de tapis : les déviations vers le tapis sont cohérentes avec des fold à 70-80 %.
- Défaut systématique de justification : la règle R12 (« complète trop et se couche ») est collée sur des spots où :
  - il ne complète pas assez (L21, L43, L59) ;
  - il paie beaucoup (L01, L34, station en L02).
- Il faut une règle « il se couche trop face au tapis » et une règle « station : tapis pour la valeur ».
- Les « reads » reposent sur 2 ou 3 limps (L01, L10). Les écarts de moins de 0,15 BB sont présentés comme des réponses tranchées (L29 à EV égales, L47 à 0,06) : il faut écrire « quasi indifférent ».
- L35 est à vérifier : l'EV du check est-elle bien calculée hors de position ?
- Doublons : L45, L48 et L58 sont identiques.

**(c) Section postflop.**
- **Bloquant sur les 30 fiches HU** : « Tu joues en position, tu parles en dernier » est faux. Il faut écrire « Tu es hors de position : tu parles en premier ».
- La partie SPR est juste (2,5 : paire max = tapis ; 3,5-4,5 : paire max bon kicker).
- La section est peu utile : des stats, pas de plan. Ajouter une ligne concrète, par exemple « il checke = faible : mise 1 BB », « paire moyenne : block bet », « KK/AA : mise pour la valeur dès le flop ».
- 5 fiches ont une section « Ce qui avantage ta main » vide (L13, L18, L55, L56, L59).
- L36 dit « rarement (0 %) ».

**(d) Textes trop longs.** Il y a 12 puces par fiche, dont l'EV répétée, la phrase générique sur le check et le conseil générique sur les statistiques. Coupe à 3 puces : stat clé, équité, leçon.
- **Jargon à remplacer :**
  - « range plafonnée » → « il a peu de grosses mains » ;
  - « réalises plus d'équité » → « tu profites mieux de ta main » ;
  - « SPR » → « il reste 2,5 pots ».
- **Ce qui embrouille :**
  - les stats estimées (« son limp : 13 % ») données à côté de « 0 fois sur 3 » sans dire que c'est une estimation ;
  - « complété 0 fois » alors qu'il complète dans la main.
- **Les « À retenir » à réécrire :**
  - R9 → « Même contre lui, X reste le meilleur coup » ;
  - R0 → « Inconnu = rec passif : limp faible, se couche trop, donc tapis plus large ».
