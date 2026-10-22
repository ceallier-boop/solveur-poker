# Audit PA (Kill Tilt) – SpinsAcademy, banques du 21/10/2026

Regard de coach : la théorie d'abord, puis l'exploitation du field. Le détail ligne par ligne est dans `audit_pa.csv` (187 lignes : 1 bloquant, 103 majeurs, 83 mineurs). Montants en BB.

## 1. Méthode et volume relu

- **Exploitant, 4400 questions** passées au script : bonne réponse contre l'EV, gain affiché, cote et équité du « pourquoi », sens de l'écart des stats contre la règle (R0 à R15), taille des échantillons, doublons, profils.
- **Relecture fiche par fiche** : 184 fiches lues en entier, une ou deux par strate (situation × tapis × type), en commençant par les plus douteuses (petit écart d'EV, gros gain contre la théorie). Plus une vingtaine de fiches ouvertes pour vérifier un point.
- **GTO, 2528 spots** relus depuis la stratégie complète (`spots.jsonl`), car la colonne range du CSV est vide pour 1223 spots. J'ai comparé les fréquences par profondeur, la cohérence entre profondeurs voisines, les spots jumeaux et l'EV HRC contre l'EV exacte des nœuds de call (28 730 couples main-action).
- **566 corrections GTO** : lecture de 30 en entier, contrôle de longueur et de structure sur toutes.
- **Bilans** : part servie comparée à la fréquence réelle, tranche par tranche.

Ce que je n'ai pas pu vérifier : la vraie fréquence de fold du field après un limp (il faudrait des mains réelles), et si le moteur d'EV exploitant lit la stat du BB fausse décrite en 2.1.

## 2. Erreurs systématiques

### Exploitant

1. **Stat du BB fausse dans les 445 questions BTN (bloquant).** « Le BB a payé ton tapis quand le SB s'était couché 34 fois (42 %) » est calculé sur toutes les occasions (34/80) au lieu des fois où le SB s'est couché (34/62 = 55 %). On compare ensuite à la théorie conditionnelle (60 %). Le sens de l'écart est faux dans 60 questions. 71 questions R11 disent « ses stats collent à la théorie » alors que c'est faux.
2. **Face au limp du SB, 94 % des réponses sont « tapis » (majeur).** 1328 questions sur 1420. Sans info, c'est 100 %. Le rec passif par défaut limpe 27 % puis se couche 78 % face au tapis : c'est un profil limp-fold, pas le récréatif passif du field. On enseigne le tapis avec 32o, 72o, 83o à 8 BB, là où HRC checke. Pour PA, contre un récréatif qui ne folde pas, l'iso pour voler sans info est un mauvais concept, et le passif limpe aussi ses As. Je ne suis pas sûr de la vraie fréquence de fold du field : à mesurer avant de trancher.
3. **Adaptation sur trop peu de coups (majeur).** R12 conclut « il complète trop » sur 3 à 5 limps (148 questions). 290 questions affichent une stat de call lue sur moins de 10 limps, alors que la relecture précédente avait fixé 10 limps minimum. Les stats comptent à 10 % sous 10 occasions et à 90 % dès 11 : c'est une marche, pas un lissage. PA : 3 occurrences ne font pas une tendance.
4. **R13 cite le mauvais échantillon (majeur, 253 questions).** « 60 coups observés » désigne les occasions de limp, mais la règle repose sur 10 à 57 tapis subis (médiane 16).
5. **EV qui dépend d'un profil caché (majeur).** 51 paires d'énoncés identiques ont des EV différentes, jusqu'à 0,11 BB d'écart. R4 (223 questions) s'appuie sur une fréquence d'iso du BB qui n'est pas dans l'énoncé.
6. **Deux définitions du rec passif (majeur).** En R0 il « paie » ; dans les questions de pastille, le rec passif « pousse et paie moins » (c'est un nit), et la pastille « Nit » n'est jamais la bonne réponse.
7. **SB face au tapis du BTN (majeur, 316 fiches).** La cote est calculée comme en heads-up. Aucune fiche ne dit que le BB parle encore derrière. 13 fiches disent « assez pour payer » avec une réponse fold.
8. **Doublons (mineur).** 52 questions en trop (énoncé identique), 222 groupes avec la même EV alors que les stats diffèrent.
9. **Comptages irréalistes (mineur).** Le nombre de tapis subis est toujours égal au nombre de limps (1238 questions) ou d'occasions (questions de pastille).

### GTO

1. **Tailles d'open (majeur).** En HU, le SB ouvre en 3,5 BB dans 28 spots et en 2 BB dans 12 seulement (pas de 2 BB au-delà de 16 BB). HRC relance lui-même plus en 2 BB. À 3, le BTN ouvre surtout en 2,3 BB (43 spots contre 6 en 2 BB). PA min-raise sous 20 BB.
2. **Convergence HRC à 14-18 BB (mineur).** Aux nœuds de call, la stratégie HRC s'écarte de l'EV exacte de 0,2 à 0,3 BB en moyenne. La référence suit l'EV exacte, donc les réponses tiennent. Mais des spots jumeaux donnent des références opposées pour 10 à 11 mains limites à 12 et 16 BB.
3. **Textes des corrections (mineur).** 450 à 860 caractères, 8 phrases. Mains « à la limite » parfois absurdes (JJ en call, AKo en tapis). « Face à un tapis à 25 BB » quand le tapis subi est de 15 BB. « 91 % des mains » pour 91 % de la range qui arrive là.
4. **Iso à 3 BB à 8 BB (mineur).** Elle engage le tapis. PA pousse à 10 BB ou moins.

Sur le fond, les ranges GTO tiennent. Défense BB, calls contre tapis et open BTN (35-40 % au-delà de 20 BB) sont cohérents avec la théorie et avec PA. Je n'ai trouvé aucune range absurde, et les ranges de call rétrécissent bien quand le tapis grandit (1 seule exception par nœud, du bruit).

## 3. Erreurs ponctuelles notables

- **R4 en HU à 8 BB (15 questions, ex. hu-8-004ee7, hu-8-1fa84f).** Le texte dit « il paie trop / joueur passif » alors que le BB paie moins que la théorie (36-40 % contre 45 %). La réponse (limp de 32s, 74o, Q7o) va dans le sens de PA (limper large en HU contre un passif), mais rien dans l'énoncé ne le justifie.
- **3w-6-0d1a33 (Q6s, BB face au tapis BTN à 6 BB).** « 40 % d'équité : pas assez pour payer » pour une réponse « payer ».
- **13 fiches SB face au BTN** (ex. 3w-8-00ebd9 A2s, 3w-4-5d01cd K5o) : « assez pour payer » et réponse fold.
- **3w-8-2a295d (TT, SB à 8 BB)** : limp-trap contre un BB passif. C'est conforme à la théorie, mais PA réserve le limp-trap à ceux qui isolent tout. La fiche ne l'explique pas.
- **pf-10-21b809, pf-8-24d12e et 3 autres** : pastille « rec passif » pour un nit.
- **3w-25-35-15-BTN-raise2.3_SB-raise7.59_BB-allin-8ea0b3 (99)** et **3w-10-20-45-…-c0f9c3 (ATo)** : textes GTO trompeurs (mauvais tapis cité, mains limites absurdes).

## 4. Manques, du plus fréquent en jeu au moins fréquent

1. **HU, SB premier à parler et BB face au limp, toutes profondeurs.** C'est le spot le plus joué et le plus rentable (PA). En GTO : 162 spots HU sur 2528.
2. **Tapis inégaux en HU.** Le HU suit une élimination, donc les tapis sont souvent 2 pour 1 ou plus (30/15, 35/10). Il n'y a presque aucun spot de ce type.
3. **Exploitant au-dessus de 12 BB.** Le Nitro démarre à 15 BB et le Regular à 25 BB, et le mode n'a rien entre 15 et 25 BB.
4. **Min-raise et iso non all-in en exploitant.** C'est la norme à 10-15 BB (iso 2,5-3 BB pour PA) : 2 questions de limp à 10 BB, aucune à 12 BB.
5. **Limp et min-raise du BTN en exploitant.** C'est le signal de récréatif n° 1. Il manque SB face au limp BTN, BB face au limp BTN + SB, et BB face au min-raise.
6. **Tapis inégaux en exploitant** : tous les tapis sont égaux.
7. **Postflop.** Aucun exercice noté. PA gagne l'essentiel contre les récréatifs ici : value bet, cbet en HU, check-call contre des joueurs face up.
8. **Questions de pastille.** 53 seulement, toutes en HU.
9. **Pots limpés à 3 et lignes profondes (3-bet, squeeze).** Présents en GTO, voire trop (voir 5). Rares en jeu.

## 5. Équilibre des séries

- **GTO, sous-servi** (part servie / part réelle dans la tranche) :
  - BTN premier à parler : 0,23 à 0,34 ;
  - SB après fold du BTN : 0,35 à 0,38 ;
  - HU SB premier à parler : 0,26 à 0,56 ;
  - spots de tapis à 7-10 BB (SB face au BTN, BB face au SB ou au BTN) : 0,08 à 0,12.
- **GTO, sur-servi** :
  - HU BB face à l'open du SB 7-10 BB : × 8,5 ;
  - HU BB face au limp ≤ 6 BB : × 8 ;
  - HU SB limp puis relance du BB 7-10 BB : × 7 ;
  - SB face au limp du BTN 11-15 BB : × 3,5.

  L'arbre « BTN limp > SB limp » fait 18 % des spots pour moins de 1 % du jeu réel.
- **Exploitant** : les 4 situations de limp à 6-8 BB prennent 51 % de la part servie. Les tranches 10-12 BB n'en ont que 15 %. Dans ces questions de limp, la réponse est « tapis » 94 % du temps : un joueur peut cliquer « tapis » sans réfléchir.
- **Proposition** : tirer selon la fréquence réelle × l'enjeu en BB, avec un plancher et un plafond par famille (par exemple 2 % et 10 %), et viser 30 à 60 % pour chaque réponse dans une situation.

## 6. Top 10 des priorités

1. Corriger la stat du BB dans les 445 questions BTN (diviser par les folds du SB), puis reclasser R3/R9/R11.
2. Recaler le rec passif face au limp sur des données réelles. Sortir du « tapis 94 % » et garder le tapis large pour un profil limp-fold affiché.
3. Une seule taxonomie de profils (rec passif loose-passif, nit serré) dans R0, les fiches et les pastilles.
4. Seuils d'échantillon : au moins 8-10 limps pour R12, au moins 20 tapis subis pour R13, lissage continu. Citer le bon échantillon.
5. Calculer l'EV uniquement à partir des stats affichées (ou afficher la stat d'iso). Retirer les 52 doublons.
6. SB face au tapis du BTN : dire que le BB parle derrière et corriger les 14 verdicts « assez / pas assez » contradictoires.
7. Rééquilibrer les séries GTO vers BTN premier à parler, SB BvB, HU SB, et les tapis à 7-10 BB.
8. HU : faire du min-raise la taille par défaut et ajouter les tapis inégaux (10/35, 15/30, 20/25).
9. Exploitant : ajouter 15-25 BB, le min-raise, l'iso 2,5-3 BB, le limp du BTN et les tapis inégaux.
10. Raccourcir les corrections GTO à 3 blocs et filtrer les mains « à la limite » sur la fréquence. Puis lancer un premier module postflop (pots limpés HU et BvB).
