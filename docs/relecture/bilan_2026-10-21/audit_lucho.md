# Audit Lucho : banques GTO et exploitant (22/10/2026)

Banques auditées : `gto_preflop/2026.10.13-3` (2528 spots) et `exploit_field/2026.10.21-2` (4400 questions).
Détail ligne par ligne : `audit_lucho.csv` (131 lignes : 44 bloquantes, 50 majeures, 37 mineures ; 27 lignes « SYSTEMATIQUE » donnent une règle d'erreur et le nombre de questions touchées).

En bref : **les décisions tiennent presque toutes**. Ce qui coince :
- des stats affichées fausses ou trop maigres ;
- des textes qui contredisent la réponse ;
- un mode exploitant qui n'apprend qu'à être plus agressif ;
- des séries qui servent mal les spots les plus joués.

---

## 1. Méthode et volume relu

**Exploitant (4400 questions, toutes passées au script)**
- Contrôles mécaniques :
  - bonne réponse = meilleure EV ;
  - gain = EV(bonne réponse) moins EV(action théorique) ;
  - écarts sous 0,05 BB ;
  - réponses acceptées.
- Cohérence entre la règle (R0 à R15), le sens de l'écart des stats affichées et le sens de la déviation.
- Calcul de la cote (« il te faut X % ») et cohérence « assez / pas assez » avec la réponse.
- Taille des échantillons : test binomial sur chaque stat affichée.
- Doublons d'EV, textes cassés, stats impossibles.
- Liste des mains par situation × tapis × décision, jugée avec la doctrine Lucho.
- **150 fiches lues en entier.** Chaque strate (situation × tapis × type) est couverte, puis j'ai pris les plus douteuses : écart faible, R13, inconnu, petit échantillon, gros gain.

**GTO (2528 spots)**
- Lecture du dataset complet par le chargeur de l'appli : 427 000 couples main × spot, avec fréquences, EV et regret HRC. Le CSV ne montre pas tout : « None » y veut dire « range trop longue ».
- Fréquences par action et par profondeur sur les nœuds clés (HU et 3-handed), et monotonie entre profondeurs voisines.
- Doublons visibles (même spot, deux réponses).
- Convergence HRC (regret).
- Contre-calcul indépendant de quelques overcalls à 3, avec la table d'équité à 3 joueurs.
- **566 corrections** : toutes contrôlées par script (chiffres, formulations). La liste compacte des 566 a été relue, et environ 40 corrections en entier.

**Manques et équilibre** : les deux fichiers de bilan, comparés à ma connaissance du field Expresso.

**Limite** : je n'ai pas de base de mains réelles du field. Les fréquences « réelles » viennent de HRC (des joueurs GTO), pas des recs. Quand je juge un facteur de profil (rec passif, etc.), c'est un avis de coach, pas une mesure.

---

## 2. Erreurs systématiques

### Exploitant

1. **Stat du BB fausse au BTN (445 questions, dont 44 impossibles : bloquant).**
   - « Le BB a payé ton tapis quand le SB s'était couché k fois » est divisé par toutes les occasions, pas par les folds du SB.
   - Dans 44 questions, le BB paie plus souvent que le SB ne s'est couché. Exemple 3w-4-185b6a : 25 occasions, le SB paie 11 fois, le BB paie 17 fois.
2. **R13 annonce un faux échantillon (253 questions).**
   - Le texte dit « il se couche souvent face au tapis (100 coups observés) ».
   - En réalité, la stat de fold repose sur 10 à 57 limps (médiane 16).
   - 248 de ces 253 questions n'ont pas d'écart significatif.
3. **La stat de call après limp est encore affichée sous 10 limps (396 questions).**
   - On voit par exemple « payé 0 fois sur 1 ».
   - La relecture du 21/10 disait ce point corrigé : il ne l'est que pour le choix de la règle.
4. **Les adaptations vont à sens unique (1869 questions).**
   - Premier à parler : 338 adaptations « fold → tapis », 0 « tapis → fold ».
   - Face au limp : 1066 « check → tapis », 5 dans l'autre sens.
   - Aucune question n'apprend à garder son tapis pour la value contre une calling station, alors que la station pèse 19 % de la banque.
5. **Le type de question se devine.**
   - Les 266 questions « inconnu » dévient toutes de la théorie.
   - Les 1806 « piège » et les 180 « échantillon » sont toutes à la théorie.
6. **Doublons d'EV entre types (222 groupes, 445 questions).**
   - Une adaptation a souvent exactement l'EV du vilain inconnu. Le read affiché ne change alors rien.
   - La leçon « il pousse peu : paie plus serré » est donc fausse : c'est le profil par défaut qui décide.
7. **Overfold à 10-12 BB face au tapis (50 questions R2 et 16 R0).**
   - On folde KQo, KJo, KTo, K9o et A2o-A4o contre un inconnu ou un « pousse peu » en HU et en BvB.
   - Le modèle suppose que le rec pousse le haut de la range théorique (9 % au lieu de 15 % en HU à 12 BB). Un rec ne joue pas comme ça : il limp ses monstres et pousse ses Ax faibles.
   - C'est exactement l'overfold que je combats. Je ne suis pas sûr du field réel à 12 BB, mais si on se trompe, c'est la fuite la plus chère.
8. **Textes de règle contraires aux stats.**
   - R4 « contre un joueur passif, limpe » alors que la stat montre un joueur qui paie trop (208 questions), ou qui paie peu (15 questions, où il faudrait pousser).
   - R12 « son limp est faible, pousse » alors qu'il paie au-dessus de la théorie (173 questions).
9. **Reads non prouvés.**
   - 129 questions d'identification sur 226 ont un écart non significatif.
   - 645 adaptations s'appuient sur un écart non significatif (p > 0,2).
10. **Le « Pourquoi » contredit la réponse (14 questions).**
    - Exemple : « assez pour payer », mais la réponse est fold.
    - Cause : au SB, le seuil de cote oublie que le BB est encore derrière.
11. **Textes mineurs.**
    - Phrase cassée dans les profils (« comme le GTO que le GTO ») : 14 questions.
    - « Ce vilain » au BTN alors qu'il y a deux joueurs.
    - « Tu gagnes 2 BB » au lieu du gain net de 1 BB.

### GTO

1. **Convergence HRC faible.**
   - 664 spots (26 %, 9303 questions) ont plus de la moitié des mains atteintes avec un regret au-dessus de 0,1 BB, jusqu'à 22 BB.
   - Ce sont surtout les arbres rares (limp, iso, call, squeeze).
   - Les mains proposées sont filtrées, mais leurs EV dépendent de stratégies mal résolues autour.
2. **Même spot visible, deux réponses de référence (544 couples main × spot).**
   - Cela vient d'arbres différents ou du bruit HRC.
   - Sur un overcall à 12 BB, l'EV de K9s va de -0,93 à +1,08 BB selon l'arbre.
3. **Actions manquantes.**
   - Pas de tapis au SB à partir de 16 BB (HU et BvB).
   - Pas de tapis pour le BB face au limp à partir de 16 BB.
4. **Tailles de relance peu réalistes.**
   - Le BTN ouvre à 2,3 BB dans la plupart des arbres, le SB à 3,3-3,5 BB.
   - En HU, une relance à 3,5 BB dès 10 BB.
   - Le field ouvre au clic (2 BB).
5. **Textes des corrections.**
   - « Face à une relance à 8 BB » alors que la relance est de 2,3 BB et que 8 BB est le tapis (environ 400 corrections ; 145 ont un chiffre qui n'est pas le tapis effectif).
   - Deux pourcentages différents dans la même correction (291 fiches).
   - Après deux tapis, le texte dit « face à un tapis » et « sa range » (142 fiches).
   - Jargon « règle simplifiée à 99 % » (93 fiches).
   - « Se couche 0 % du temps : tu prends le pot » (16 fiches).
6. **Ranges non monotones entre profondeurs voisines.** Exemples : KQo au BTN à 8 BB, AJo au SB à 10 BB. C'est souvent un mixte à EV égale, mais l'« À retenir » change sans raison de jeu.

Ce qui est bon :
- Les ranges de push/fold et de call aux profondeurs clés sont dans les clous. Exemples : en HU, le BB paie 74 / 55 / 44 / 37 / 31 / 25 % des mains à 4 / 6 / 8 / 10 / 12 / 15 BB ; le SB limp de plus en plus avec la profondeur.
- Les calls BB face au tapis sont monotones.
- Mon contre-calcul des overcalls à 6-10 BB colle à HRC à 0,1-0,3 BB près.

---

## 3. Erreurs ponctuelles notables

- **hu-12-8cabb3, hu-12-fb84a4** (KQo, BB face au tapis HU, 12 BB) : fold sur 3 tapis en 40 coups. L'écart n'est pas net, et folder KQo coûte cher si le vilain est un dégène. À passer en « payer » ou à retirer.
- **3w-12-2db655, 3w-12-35d880, 3w-12-a00fbf** (QJo, K9o, KJo, vilain inconnu, 12 BB) : fold d'un call théorique contre un inconnu.
- **3w-4-185b6a** et 43 autres : stats du BB impossibles (voir §2).
- **3w-8-4be606** (A6o), **3w-8-00ebd9** (A2s), **3w-4-4dcff2** (K4o) : le texte dit « assez pour payer », la réponse est fold.
- **hu-8-2a7d5c** (42s, SB HU 8 BB) : « il ne paie pas assez », et pourtant il faut limper. Sa vraie faiblesse, l'iso rare, n'est pas affichée.
- **hu-6-46a5ed** (83o) : « 100 coups observés » pour une stat de fold calculée sur 11 limps.
- **3w-10-5bfd1a, 3w-10-8bc886, 3w-10-e807c6** (type échantillon) : une 2e réponse est acceptée alors qu'elle perd 0,15 à 0,20 BB.
- **pf-4-96c452** et les autres profils à 4 BB : « dégène » pour un joueur qui pousse 85 % au lieu de 74 %. À 4 BB, c'est presque juste.
- **GTO 3w-8-8-8-BTN-raise2.3_SB-fold-e918b6** : « au BB face à une relance à 8 BB » pour un open à 2,3 BB.
- **GTO 3w-35-15-25-BTN-raise2.3_SB-call_BB-raise9.89** (KK) : spot rare et mal résolu. La règle donne « tapis avec 33+, A4s+, A9o+, 98s, 87s » et met AKo dans les mains limites : illisible.

---

## 4. Manques, classés par fréquence en jeu

Les fréquences viennent du bilan HRC et de mon estimation du field. Je ne suis pas sûr de l'ordre exact entre les points 3 et 5.

1. **SB premier à parler en HU, 10-25 BB** : limp 100 % vs rec, clic, jam. C'est la décision la plus fréquente d'un HU. Exploitant : 29 questions à 10-12 BB, rien au-delà. GTO : servi 13-15 % de la tranche pour 44-50 % réels.
2. **BTN premier à parler 3-handed, 11-25 BB, avec clic.** L'exploitant ne propose que fold ou tapis jusqu'à 12 BB ; le GTO ouvre à 2,3 BB. Il manque l'open loose au clic vs recs (K3, Q4, 82…).
3. **Face au tapis à 7-15 BB** (SB vs BTN, BB vs SB, BB vs BTN) : fréquent et cher (le punt classique). GTO : servi 0,08 à 0,26 fois sa fréquence réelle.
4. **BB face au limp du SB à 10-15 BB, avec iso non all-in** : exploitant 4 questions à 10 BB, 0 à 12. C'est là que l'iso 2,5-3 BB devient la norme.
5. **Tapis inégaux en exploitant** : 100 % des questions sont à tapis égaux, alors qu'en jeu ils sont presque toujours inégaux après le premier coup.
6. **Face au clic** (BB/SB contre un min-raise BTN ; BB contre le clic du SB en BvB) : absent de l'exploitant, rare en GTO (arbre à 2,3 BB).
7. **Limp du BTN et pots limpés à 3** : absents de l'exploitant, peu servis en GTO.
8. **Calling station** : aucune question « garde ton tapis pour la value ».
9. **Postflop** : aucune décision notée. Il faudrait des pots limpés HU et BvB avec un SPR de 2 à 5 : block bet, check des boards ratés, c-bet cher.
10. **Contexte jackpot** (x10 et plus, recs nits) : absent.

---

## 5. Équilibre des séries

**GTO**
- 78 situations quasi inexistantes en jeu (moins de 0,1 % de leur tranche) prennent 14,5 % des questions servies. Ce sont aussi les moins bien résolues.
- À l'inverse, face au tapis et premier à parler sont très sous-servis (voir §4).
- Par profondeur, en 3-handed, 7-10 BB n'a que 9,6 % des séries et ≤ 6 BB 5,4 %. C'est peu vu le temps passé short en hyper-turbo (mon estimation : 35-45 % des mains à 10 BB ou moins).
- HU : 34,9 % des séries pour 6 % des spots (162). Le volume de spots HU est trop faible pour cette part.

**Exploitant**
- 51 % des séries sont « BB face au limp du SB » (29 % en 3-handed, 22 % en HU).
- 50 % des séries sont à 8 BB ; 10 BB n'en a que 7,8 % et 12 BB 9,9 %.
- Le SB premier à parler (HU et BvB) n'a que 17 %, le BTN premier 8 %, face au tapis 23 %.
- Les profils : « Dégène » est la réponse de 55 % des questions de pastillage, « Nit » de 0 %, alors que le field est surtout passif.
- Cible proposée : 25 % de limp, 20 % SB premier à parler, 15 % BTN premier, 40 % face au tapis ; tapis répartis de 4 à 12 BB.

---

## 6. Top 10 des priorités

1. **Recalculer la stat du BB au BTN** sur les seuls folds du SB (445 questions, 44 impossibles).
2. **Corriger les échantillons affichés** : R13 doit citer le nombre de limps, la stat de call doit disparaître sous 10 limps, et il faut exiger un écart net pour les reads et les identifications.
3. **Arrêter l'overfold à 10-12 BB** : contre un inconnu, payer comme la théorie ; recaler le facteur du rec passif et la forme de sa range de tapis (66 questions).
4. **Ajouter des adaptations « plus serré »** (calling station : tapis pour la value) et des « inconnu » où la théorie tient. Le type ne doit plus se deviner.
5. **Dédoublonner tous types confondus**, et retirer les adaptations dont l'EV est celle du profil par défaut (445 questions).
6. **Rééquilibrer les séries** : face au tapis et premier à parler en hausse ; arbres rares plafonnés à 2 % (GTO) ; limp ramené à 25 % (exploitant).
7. **Nettoyer le GTO** : retirer ou recalculer les 664 spots mal convergés et fusionner les doublons visibles (544 conflits).
8. **Réécrire les « À retenir » GTO** : « tapis 8 BB » au lieu de « relance à 8 BB », un seul pourcentage, des formulations multiway, pas de jargon.
9. **Ajouter le clic et l'iso non all-in** (BTN, SB, BB face au limp à 10-15 BB), et le tapis au SB et au BB jusqu'à 20 BB dans les arbres HRC.
10. **Étendre l'exploitant** aux tapis inégaux, au limp BTN et pots limpés à 3, puis à 15-20 BB ; ensuite, un premier module postflop simple.
