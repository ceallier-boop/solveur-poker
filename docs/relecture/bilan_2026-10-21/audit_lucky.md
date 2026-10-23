# Audit Lucky : banques GTO et exploitant (22/10/2026)

Relecture façon Lucky (SpinPro) : la théorie comme référence, puis l'écart du field.
Détail ligne par ligne dans `audit_lucky.csv` (80 lignes : 1 bloquante, 55 majeures, 24 mineures).
Usage privé : rien ici n'est « validé par Lucky ».

## 1. Méthode et volume relu

**Exploitant (`exploit_field/2026.10.21-2`, 4400 questions).** J'ai tout analysé par script :
- bonne réponse = meilleure EV (oui pour les 4400) ; « gain » = EV de la réponse moins EV de la théorie (cohérent partout) ;
- règle citée comparée aux stats affichées (sens de l'écart, nombre de coups, écart-type) ;
- seuil d'équité du « pourquoi » comparé à la décision ;
- EV recalculée à partir du fold et de l'équité du « pourquoi » (écart moyen de 0,01 à 0,05 BB, cohérent) ;
- monotonie : la même main dans la même situation ne change jamais de décision dans le mauvais sens quand la stat bouge (0 cas) ;
- doublons, sens des adaptations, textes postflop.

J'ai lu en entier environ 170 fiches, sur toutes les strates (situation × tapis × type). J'ai commencé par les plus douteuses : petit écart d'EV, petit échantillon, R4, R12 et R13.

**GTO (`gto_preflop/2026.10.13-3`, 2528 spots).** La colonne de stratégie de `gto_spots.csv` est inutilisable (« None » pour toute range large). J'ai donc relu les ranges dans `data/datasets/gto_preflop/2026.10.13-3/spots.jsonl` :
- fréquences par action, par tapis et par arbre ;
- ranges push/fold comparées au Nash (moteur `pushfold`) ;
- premiums mal joués, nœuds non résolus ;
- lecture des 566 corrections.

**Bilans.** Pour chaque tranche de tapis, j'ai comparé la part servie dans les séries à la fréquence réelle.

**Ce qui tient.** Les ranges de référence sont propres. Elles évoluent régulièrement d'une profondeur à l'autre et collent au Nash. Exemples en HU, call du BB face au tapis : 73 % à 4 BB (Nash 74 %), 55 % à 6 BB (54 %), 37 % à 10 BB (37 %). Tapis du SB à 4 BB : 74 % (74 %).

En exploitant, les décisions préflop sont presque toutes justes en EV. Le mode « inconnu = rec passif » va dans le sens de Lucky : on paie plus serré à 10-12 BB, on vole plus.

Les problèmes viennent d'ailleurs :
- des arbres GTO (tailles, coupures) ;
- de la lecture des stats en exploitant ;
- des textes ;
- de l'équilibre des séries.

## 2. Erreurs systématiques

### Exploitant
1. **Reads sur des échantillons trop petits.**
   - R13 (« il se couche souvent face au tapis ») : 135 questions sur 253 reposent sur une stat de call après limp sous un écart-type. Exemple : 2 calls sur 10 (20 %, théorie 31 %).
   - La correction cite « 60 coups observés ». C'est le nombre d'occasions, pas le nombre de limps.
   - R12 : 259 questions ont un écart de limp sous 1,5 écart-type (4 limps sur 25).
   - La banque dit elle-même que 6 coups ne prouvent rien. 20 à 25 coups pour 5 à 8 points d'écart, ce n'est pas mieux.
2. **Identification (« quel est son défaut ? »).** 65 questions sur 226 annoncent un défaut avec un écart sous 1,5 écart-type. Exemple : 8 calls sur 20, soit 40 % contre 45 %. La correction affirme que « plusieurs dizaines de coups » suffisent. Ici, c'est faux.
3. **R12 contredite par la seconde stat.** Dans 170 questions, le vilain paie aussi le tapis après son limp, 10 points ou plus au-dessus de la théorie. La fiche ne parle que du limp large et dit « pousse plus large ». Un limp-call large, c'est une calling station : tapis avec les bonnes mains, pas avec Q4s ou J9o.
4. **R4 mal libellée (223 questions).** « Contre un joueur passif, limpe les mains trop faibles pour pousser. »
   - Dans 208 cas, le vilain « paie trop » et la théorie pousse déjà la main (86s, J6s).
   - Le limp gagne grâce à une fréquence d'iso du BB qui n'est jamais affichée.
   - Dans 15 cas, la stat dit « il ne paie pas assez » et la réponse est quand même le limp. C'est la leçon inverse.
5. **Aucune adaptation « il paie trop : pousse plus serré ».** Sur 1869 adaptations, 1589 élargissent et 280 resserrent (dont 178 limps R4). Aucune ne transforme un tapis théorique en fold. Le joueur retient « exploiter = pousser plus ». Or Lucky : contre une calling station, on n'ouvre que les bonnes mains.
6. **Postflop (946 fiches).** « S'il mise peu, paie avec un tirage, couche le reste » fait folder des paires face à une petite mise. Lucky : jamais de fold d'une paire face à moins de 50 % du pot.
7. **Petits défauts.**
   - La stat « il a payé k fois sur n » reste affichée avec n < 10 (379 questions).
   - 103 énoncés en double, dont 51 paires avec des EV différentes.
   - Le type « échantillon » calcule contre un vilain proche de la théorie, pas contre le rec passif annoncé.
   - En HU, le BB sans initiative « mise lui-même 1 BB » : c'est un donk, que Lucky déconseille. Je ne suis pas sûr que ce soit faux en EV contre un rec passif.

### GTO
1. **Ouverture à 3,5 BB en heads-up (bloquant).**
   - L'arbre principal fait relancer le SB à 3,5 BB de 10 à 25 BB.
   - Cela touche 41 spots (3802 questions) à 10-15 BB et 51 spots (3783 questions) à 16-25 BB. De 18 à 25 BB, c'est la seule taille de relance.
   - Résultat : limp à 70-82 %, et AA-JJ limpés jusqu'à 16 BB.
   - Lucky : en HU, open 2 BB obligatoire ; ouvrir à 3,5 BB est un signe de rec.
2. **Tailles hors norme et arbres mélangés.**
   - BTN à 2,3 BB (590 spots), SB à 3,5 BB (152 spots), iso du SB à 4,5 BB (301 spots).
   - À 12, 16 et 20 BB, cinq arbres de tailles différentes coexistent. La même main au même tapis change de réponse selon l'arbre tiré.
   - Exemple : AA au BTN à 18 BB, limp à 90 % avec un arbre, relance à 65 % avec l'autre.
3. **AA et KK limpés au BTN de 8 à 20 BB** (52 mains proposables). C'est un artefact d'indifférence. La range de limp du BTN est éparse : K7s, K4s, A3o, 54s. Lucky : jamais de limp BTN à 3 ; premiums ouverts à 2 BB au-dessus de 10 BB.
4. **Coupure du tapis à 16 BB.** L'option tapis disparaît d'un coup :
   - SB : 19 % à 15 BB, 0 à 16 BB ;
   - BB face au limp : 10,5 % puis 0 ;
   - SB HU : 7,7 % puis 0 ;
   - BB HU face au limp : 19 % puis 0.
5. **Textes des corrections.**
   - « Face à une relance à 25 BB » : 25 BB est le tapis, pas la relance.
   - Deux pourcentages différents dans la même fiche.
   - Montants comme 9,89, 15,11 ou 7,59 BB.
   - « Pourquoi » vide dans les 566 corrections.
   - 32o cité dans une range de valeur.

## 3. Erreurs ponctuelles notables
- **3w-12-12-12-…-5a95ea (GTO).** AKs face au tapis : 50/50 avec des EV nulles, nœud non résolu. Le fold d'AKs est noté correct. Même défaut :
  - 3w-4-4-4-…-b8b66b : A4s, T8s, 83s, 72s ;
  - f44fe6, 50abff, e18b59.
- **14 fiches où le texte contredit la réponse.** Exemples : 3w-4-5d01cd et 3w-8-00ebd9 (« 44 % d'équité pour 44 % requis : assez pour payer », réponse fold). Le texte oublie le BB qui parle derrière.
- **15 fiches R4 « il ne paie pas assez » avec réponse limp.** Exemples : hu-8-2a7d5c (42s), hu-8-004ee7 (32s), hu-8-286dfa (62s).
- **33 adaptations sous 0,1 BB de gain.** Exemples : 3w-4-c9b948 (J6o paie pour +0,099 BB), hu-4-f37773 (83s pousse pour +0,08 BB). La fiche dit elle-même « écart faible ».
- **hu-6-* inconnu.** La règle dit « il paie peu », mais le « pourquoi » donne un fold de 45 %, égal à la théorie. Seule l'iso faible justifie le limp.

## 4. Manques, du plus fréquent au plus rare en jeu
1. **BTN premier à parler avec open 2 BB contre les recs** (100 % des mains à 3). Exploitant : tapis ou fold seulement, 4-12 BB, 8 % des séries.
2. **SB après fold du BTN (BvB) : open 2 BB, limp, tapis** (60-65 % des mains). Exploitant : 28 questions à 10-12 BB, rien au-dessus.
3. **SB HU premier à parler au-dessus de 8 BB** : 29 questions à 10-12 BB.
4. **Profondeurs 13-25 BB** : aucune question exploitante.
5. **Tapis inégaux** : 0 en exploitant, alors que c'est la norme après le premier coup.
6. **SB face à l'iso ou au tapis du BB après son limp** (15-19 % des mains HU à 7-15 BB) : absent en exploitant. Lucky : limp-call seulement les bonnes mains.
7. **BB face au limp : iso non all-in à 10-15 BB** : 4 questions.
8. **BB face à l'open d'un rec (2 BB ou 3 BB)** : absent en exploitant.
9. **Iso du limp BTN d'un rec** : absent. C'est le signe n°1 du rec selon Lucky.
10. **Pots limpés à 3 / deux limps** : absents en exploitant.
11. **Face au 3-bet tapis après son open** (KQo à 15 BB).
12. **Postflop** : aucune question dans les deux modes.
13. **GTO** : seulement 162 spots HU. Pas d'arbre 2 BB au-dessus de 16 BB.

## 5. Équilibre des séries
- **GTO : premières décisions trop peu servies.** À 11-15 BB à 3 :
  - BTN premier à parler : 11,5 % servi contre 33,7 % en jeu réel ;
  - SB après fold : 8,4 % contre 22,2 % ;
  - en HU à 7-10 BB, SB premier à parler : 13 % contre 50 %.
- **GTO : lignes rares trop servies.** Les lignes de moins de 0,5 % du jeu prennent :
  - 35 % des séries à 11-15 BB (2 % en réel) ;
  - 48 % à 16-25 BB (3,6 % en réel).
- **GTO : face au tapis trop peu servi.** À 7-10 BB, ces situations font 26 % du jeu réel et 2,6 % des séries.
- **Exploitant : BB face au limp trop servi.** Il occupe 51 % des séries, contre environ 4 % des décisions à 3 et 20 % en HU. Le BTN premier à parler : 8 %. Les tapis 6 et 8 BB font 76 % des séries. À 10-12 BB, 85 % des questions sont des pièges.
- **Proposition.** Tirer d'abord selon la fréquence réelle. Plafonner les lignes rares à 10 %. Viser environ 60/40 entre adaptations qui élargissent et adaptations qui resserrent.

Je ne suis pas sûr de la part réelle des mains HU contre 3-way ni de la répartition par tapis en Expresso. J'ai utilisé les fréquences de référence du bilan, qui supposent un jeu théorique.

## 6. Top 10 des priorités
1. **GTO HU** : refaire l'arbre avec un open à 2 BB à toutes les profondeurs (bloquant).
2. **Exploitant** : seuils de significativité (au moins 30 coups et 1,5 écart-type) pour R12, R13 et l'identification ; sinon, type « échantillon ».
3. **Exploitant** : ajouter des adaptations « il paie trop : pousse plus serré » (calling station, environ 200 questions).
4. **Séries** : pondérer par la fréquence réelle (premières décisions, face au tapis) et plafonner les lignes rares.
5. **GTO** : un seul arbre par tapis (BTN 2 BB, SB 2,5-3 BB, iso 3 BB) ; ne plus noter le limp AA/KK du BTN comme seule bonne réponse.
6. **GTO** : garder l'option tapis jusqu'à 18-20 BB ; exclure les nœuds 50/50 à EV nulle (AKs).
7. **Exploitant** : réécrire R4 et R12 selon les deux stats ; retirer les 15 R4 incohérentes ; afficher la stat d'iso quand elle fonde le limp.
8. **Postflop** : remplacer « couche le reste » par « paie une paire face à une petite mise » ; revoir le donk du BB HU.
9. **Moteur exploitant** : min-raise, iso non all-in, 13-25 BB, tapis inégaux, SB face à l'iso après son limp.
10. **Textes** : corriger les 14 fiches au seuil d'équité faux, les doublons, « relance à 25 BB », les arrondis, le « pourquoi » GTO vide, la colonne stratégie à « None ».
