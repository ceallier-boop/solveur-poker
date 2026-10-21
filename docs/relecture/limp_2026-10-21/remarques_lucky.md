# Relecture « BB face au limp du SB » : remarques de Lucky (21/10/2026)

**Bilan.** Sur 60 questions, 59 réponses du moteur sont bonnes et 1 est incertaine (L35, K4s HU 6 BB : le check est douteux, je jouerais tapis). Je ne relève aucune vraie erreur préflop. En revanche, les 30 fiches HU sont bloquantes à cause du texte (point b) et 4 fiches 3 joueurs ont une justification fausse (L01, L02, L13, L21).

**(a) Doctrine face au limp du SB.** Le field iso trop peu (les recs isolent 11 à 16 % des limps) et se couche trop. Au BB, on est donc plus agressif que la théorie.
- **6 BB** (HU et BvB) : c'est presque du push/fold. Une iso à 2,5 BB engage déjà 40 % du tapis, donc l'iso, c'est le tapis. Tapis large contre un limp qui se couche. En BvB, on peut checker en position les mains jouables qui font peu folder mieux (87s, J8s). Avec AA et KK : check ou mini-iso à 2-2,5 BB pour faire venir son tapis.
- **8 BB** : le tapis reste l'iso par défaut. L'iso 2,5 BB (un tiers du tapis, on ne se couche plus derrière) ne sert qu'en value : premiums et gros Ax, pour se faire payer par pire.
- **10 BB** : l'iso 2,5 BB devient meilleure que le tapis pour la value et les bons bluffs. On garde le tapis pour les mains qui n'aiment pas le postflop (petites paires, Ax faibles) et pour les poubelles contre un joueur qui se couche à plus de 80 % (L59).
- **12 BB** : mettre 12 BB pour en gagner 2 demande environ 85 % de fold. On iso à 2,5-3 BB (règle : nombre de limpers + 2 BB, moins 0,5 BB sous 15 BB) avec une range large. On met tapis avec les paires moyennes et les Ax. On checke les poubelles.
- **HU ou BvB** : en HU, le BB est hors de position après le flop. Il réalise mal son équité quand il checke, donc il met tapis ou isole plus large. En BvB (BTN couché), le BB est en position : il checke plus de mains moyennes.
- L'application ne propose pas d'iso non all-in. Elle manque donc les meilleures lignes à partir de 10 BB, et avec AA et KK même à 6 BB (L37, L42). Aucune question à 12 BB dans le tirage.

**(b) Erreurs systématiques du moteur.** Il ne met pas trop de tapis : les tapis « exploit » (R12) tiennent contre un rec passif qui se couche 66 à 83 % du temps. Les défauts sont ailleurs :
1. **Position en HU (bloquant, 30 fiches).** Elles affichent « Tu joues en position » et « le flop gratuitement, en position ». C'est faux : en HU, le SB est le bouton. À vérifier aussi : si l'EV du check suppose qu'on est en position, elle est surévaluée (L35, L47).
2. **Règle affichée qui contredit les statistiques.** R12 dit « complète trop et se couche » alors que le joueur complète moins que la théorie (L21, L43, L59) ou paie plus qu'elle (L02, L34). R13 dit « paie ton tapis » alors qu'il se couche 69 % du temps (L13). R10 dit « ne complète pas assez » alors qu'il est en train de compléter et que l'estimation affichée est au-dessus de la théorie (8 fiches). L10 étiquette « reg » un joueur vu sur 3 limps.
3. **Échantillons trop minces.** Beaucoup de décisions « Adaptation » reposent sur 2 à 8 tapis observés : c'est le profil par défaut qui décide, pas le read. Il faut le dire.
4. **Petits défauts.** L45, L48 et L58 sont des doublons. Les égalités (L29) et les écarts minimes (L47) sont présentés comme une seule bonne réponse.

**(c) Section postflop.** Le calcul du SPR et le plan qui en découle sont justes et utiles. En 3 joueurs, le rappel de la position est juste. Il manque la ligne qui rapporte : quand le SB checke, mise environ 50 % du pot (1 BB) très souvent, car le field se couche trop au flop. « Mise surtout avec ce qui a touché » est trop passif. En HU, la section est fausse : on parle en premier et c'est le limpeur qui garde l'initiative. Il faut checker et check-raiser, pas miser en premier. « Sa range est plafonnée » est à nuancer : les recs limpent souvent AA à JJ entre 5 et 10 BB. La ligne « Avantage de range 44-46 % » est identique dans les 60 fiches : à supprimer. Les listes vides (L13, L18, L55, L56, L59) sont à supprimer elles aussi.

**(d) Textes.** Les fiches sont trop longues pour un amateur (une quinzaine de puces) et emploient trop de jargon (SPR, range de call, plafonnée). Formulations proposées :
- « Quand il paie, KQs a 47 % d'équité contre sa range de call » devient « S'il paie, tu gagnes encore 47 % du temps ».
- « SPR de 2,5 » devient « il reste à peine plus de 2 pots : si tu touches une paire, tu vas à tapis ».
- Afficher l'observation et l'estimation côte à côte : « Vu : il a payé 1 fois sur 2 (trop peu pour conclure). On retient : il paie 33 % ».
- Remplacer R9 (une tautologie) par « Cette main est un tapis contre tout le monde ».
- Ramener R0 à « Inconnu = rec passif : il se couche trop face au tapis », sans le passage sur le limp en HU et le BTN.
- Supprimer la phrase « À la table, fie-toi aux statistiques… », répétée dans les 60 fiches.
