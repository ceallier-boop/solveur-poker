# Audit complet des quizz par les coachs IA : synthèse (22/10/2026)

Banques auditées :
- GTO : `gto_preflop/2026.10.13-3`, 2528 spots ;
- exploitant : `exploit_field/2026.10.21-2`, 4400 questions.

Trois audits indépendants (Lucho, PA, Lucky), chacun sur l'ensemble des deux banques :
- les 4400 questions exploitantes passées au script, et 150 à 184 fiches lues en entier par coach ;
- les 2528 spots GTO relus, depuis la stratégie complète ;
- les 566 corrections GTO tirées dans toutes les situations.

| Coach | Constats | Bloquants | Majeurs | Mineurs |
|---|---|---|---|---|
| Lucho | 131 | 44 | 50 | 37 |
| PA | 187 | 1 | 103 | 83 |
| Lucky | 80 | 1 | 55 | 24 |

Les 44 bloquants de Lucho sont surtout les 44 questions à stat impossible du point 1 ci-dessous, comptées une par une ; les autres coachs les regroupent en une ligne.

Détail : `audit_lucho.md`, `audit_pa.md`, `audit_lucky.md` et les grilles `audit_*.csv`. Une erreur systématique y tient en une ligne, avec son ampleur et des exemples.

**Ce qui tient (les trois coachs).**
- En exploitant, la bonne réponse est toujours l'action la plus rentable en EV, et le gain affiché est cohérent.
- En GTO, les ranges collent à l'équilibre push/fold. En heads-up, le BB paie 73 % des mains à 4 BB (Nash : 74 %) et 37 % à 10 BB (Nash : 37 %).
- Les calls rétrécissent bien quand le tapis grandit. Aucune range absurde n'a été trouvée.

Les problèmes viennent de ce qui est **affiché**, de la **construction des questions**, des **arbres HRC** et de l'**équilibre des séries**.

« ✔ » : constat vérifié sur les données pendant cette synthèse.

## 1. Erreurs du mode exploitant

| # | Constat | Questions | Coachs | Gravité |
|---|---|---|---|---|
| 1 | ✔ **Stat du BB au BTN mal comptée.** « Le BB a payé ton tapis quand le SB s'était couché 20 fois » compte les calls sur toutes les occasions, pas sur les fois où le SB s'est couché. Le pourcentage affiché est le bon taux, mais le nombre de fois ne l'est pas. Dans 44 questions, le BB paie plus souvent que le SB ne s'est couché, ce qui est impossible. | 445 | les trois | bloquant |
| 2 | ✔ **Stat de call affichée sur moins de 10 limps** (« payé 1 fois sur 4 »). Le seuil de 10 limps fixé le 21/10 ne s'applique qu'au choix de la règle, pas à l'affichage. | 396 | les trois | majeur |
| 3 | ✔ **R13 cite le mauvais échantillon.** La fiche dit « 60 coups observés » (les occasions), alors que la stat de fold repose sur 10 à 57 limps (médiane 16). | 253 | les trois | majeur |
| 4 | **Reads non significatifs.** Écart plus petit que le bruit d'échantillon : R12 (148 à 259 questions selon le seuil), R13 (135 à 248), identification (65 à 129), adaptations (645 avec p > 0,2). | ~1000 | les trois | majeur |
| 5 | **Les adaptations ne vont que dans un sens.** 1589 élargissent, 280 resserrent, et aucune ne transforme un tapis en fold contre une calling station. Le joueur retient « exploiter = pousser plus ». | 1869 | les trois | majeur |
| 6 | **Le type de question se devine.** Les 266 « inconnu » s'écartent toutes de la théorie ; aucun « piège » ni « échantillon » ne s'en écarte. | 2252 | Lucho | majeur |
| 7 | **Face au limp du SB, la réponse est « tapis » 94 % du temps** (100 % sans info). Le rec passif par défaut se couche 78 % du temps face au tapis : c'est un profil qui complète puis se couche, pas le passif du field. À recaler sur des mains réelles. | 1328 | PA, Lucho | majeur |
| 8 | **Règles contredites par la 2e stat.** R12 « son limp est faible, pousse » alors qu'il paie aussi au-dessus de la théorie (170). R4 « limpe contre un passif » alors qu'il paie trop (208) ou pas assez (15). Le limp de R4 gagne grâce à une fréquence d'iso qui n'est jamais affichée. | ~390 | les trois | majeur |
| 9 | **L'EV dépend d'un profil caché.** 51 paires d'énoncés identiques ont des EV différentes (jusqu'à 0,11 BB). 222 groupes (445 questions) ont la même EV qu'une autre question alors que les stats affichées diffèrent : le read ne change rien. | ~550 | les trois | majeur |
| 10 | **SB face au tapis du BTN.** La cote est calculée comme en heads-up, sans dire que le BB parle encore derrière. Résultat : 14 fiches disent « assez pour payer » avec la réponse fold. | 316, dont 14 fausses | les trois | majeur |
| 11 | **Pastilles incohérentes.** Le « rec passif » des questions de pastille pousse et paie peu (c'est un nit). « Nit » n'est jamais la bonne réponse, « Dégène » l'est dans 55 % des cas. | 53 | PA, Lucho | majeur |
| 12 | **Conseils postflop.** « S'il mise peu, paie avec un tirage, couche le reste » fait folder des paires face à une petite mise. En heads-up, le BB qui « mise lui-même 1 BB » fait une donk bet, que Lucky déconseille. | 946 | Lucky | majeur |
| 13 | **Fold à 10-12 BB contre un inconnu** : KQo, KJo, A2o-A4o face au tapis. Lucho y voit l'overfold le plus cher si le modèle se trompe ; Lucky trouve que payer plus serré contre un rec est juste. **Les coachs sont en désaccord.** | 66 | Lucho | à trancher |
| 14 | Textes : phrase cassée « comme le GTO que le GTO » (14), « ce vilain » au BTN face à deux joueurs, « tu gagnes 2 BB » au lieu du gain net, 33 adaptations à moins de 0,1 BB présentées comme nettes. | ~50 | les trois | mineur |

## 2. Erreurs du mode GTO

| # | Constat | Ampleur | Coachs | Gravité |
|---|---|---|---|---|
| 1 | **Tailles d'ouverture irréalistes.** En heads-up, le SB ouvre à 3,5 BB de 10 à 25 BB (seule taille de 18 à 25 BB). À 3 joueurs, le BTN ouvre à 2,3 BB, le SB à 3,5 BB et l'iso fait 4,5 BB. Le field et les trois coachs ouvrent à 2 BB. Conséquence en heads-up : limp à 70-82 %, AA-JJ limpés jusqu'à 16 BB. | 92 spots HU, 7585 questions | les trois (bloquant pour Lucky) | bloquant |
| 2 | **Plusieurs arbres pour un même spot.** À 12, 16 et 20 BB, cinq arbres de tailles différentes coexistent. Le même spot à l'écran a deux réponses de référence selon l'arbre tiré. Exemple : AA au BTN à 18 BB, limp à 90 % dans un arbre, relance à 65 % dans l'autre. | 544 couples main × spot | Lucho, Lucky, PA | majeur |
| 3 | **Convergence HRC faible** sur les arbres rares (limp, iso, call, squeeze) : plus de la moitié des mains ont un regret au-dessus de 0,1 BB. Nœuds non résolus : AKs à 50/50 avec des EV nulles, fold noté correct (`…-5a95ea`, `…-b8b66b`). | 664 spots, 9303 questions | Lucho, Lucky | majeur |
| 4 | **Le tapis disparaît à 16 BB.** Pour le SB (19 % à 15 BB, 0 % à 16 BB) et pour le BB face au limp (10,5 % puis 0 %), en heads-up comme à 3. | arbres 16-25 BB | Lucho, Lucky | majeur |
| 5 | **AA et KK limpés au BTN de 8 à 20 BB** : artefact d'indifférence, présenté comme seule bonne réponse. | 52 mains | Lucky | majeur |
| 6 | **Textes des corrections.** « Face à une relance à 8 BB » désigne en fait le tapis (environ 400 corrections). Deux pourcentages différents dans une même fiche (291). Après deux tapis, le texte ne parle que d'un seul (142). Mains « à la limite » absurdes (JJ en call, AKo en tapis). Montants 9,89 ou 7,59 BB. Jargon « règle simplifiée à 99 % » (93). Fiches de 450 à 860 caractères. | ~800 | les trois | mineur à majeur |
| 7 | Ranges qui changent sans raison entre profondeurs voisines (KQo au BTN à 8 BB, AJo au SB à 10 BB) : souvent un mixte à EV égale, mais l'« À retenir » change. | quelques dizaines | Lucho, PA | mineur |

Deux remarques des coachs visaient mes fichiers d'export, pas l'application. Les ranges y apparaissaient en « None » quand elles étaient trop larges, et la colonne « pourquoi » des corrections GTO était vide. Les deux sont corrigés dans `tools/audit/bilan_quiz.py`.

## 3. Manques, classés par fréquence en jeu (consensus)

1. **Premières décisions avec open à 2 BB** : BTN premier à parler, SB après fold du BTN, SB en heads-up. C'est la majorité des décisions réelles. En exploitant, il n'y a que fold ou tapis jusqu'à 12 BB, et 29 à 77 questions seulement à 10-12 BB.
2. **Exploitant de 13 à 25 BB** : rien. Pourtant le Nitro démarre à 15 BB et le Regular à 25 BB (PA).
3. **Face au tapis de 7 à 15 BB** (SB face au BTN, BB face au SB ou au BTN) : fréquent et cher, mais servi 4 à 12 fois moins que sa fréquence en GTO.
4. **Iso non all-in face au limp à 10-15 BB** (2,5-3 BB) : 4 questions de limp à 10 BB, aucune à 12 BB.
5. **Tapis inégaux** : aucun en exploitant, et très peu en heads-up GTO (10/35, 15/30 BB), alors que c'est la norme après le premier coup.
6. **Situations des récréatifs absentes de l'exploitant** : limp du BTN et iso de ce limp, pots limpés à 3, BB face au min-raise d'un rec, SB face à l'iso ou au tapis du BB après son limp (15 à 19 % des mains en heads-up).
7. **Calling station** : aucune question « garde ton tapis pour tes bonnes mains ».
8. **Postflop** : aucune décision notée, alors que les pots limpés en heads-up et BvB (SPR de 2 à 5) font l'essentiel des gains contre les récréatifs (PA).
9. **Heads-up GTO** : 162 spots sur 2528 pour 35 % des séries. Pas d'arbre à 2 BB au-dessus de 16 BB.
10. Contexte jackpot (×10 et plus) et questions de pastille hors heads-up (Lucho, PA) : absents.

## 4. Équilibre des séries (consensus)

- **GTO.** Les lignes rares (moins de 0,5 % du jeu) prennent 35 à 48 % des séries à 11-25 BB. Les premières décisions sont servies 0,23 à 0,56 fois leur fréquence réelle, et face au tapis à 7-10 BB 0,08 à 0,12 fois. Cause : le tirage fait tourner positions et familles à parts égales.
- **Exploitant.** « BB face au limp du SB » prend 51 % des séries ; les tapis à 6 et 8 BB en prennent 76 %. À 10-12 BB, 85 % des questions sont des pièges.
- **Propositions des coachs :**
  - tirer selon la fréquence réelle × l'enjeu en BB, avec un plancher et un plafond par famille (par exemple 2 % et 10 %) ;
  - viser 30 à 60 % pour chaque réponse dans une situation, pour qu'on ne puisse pas cliquer « tapis » sans réfléchir ;
  - environ 60/40 entre adaptations qui élargissent et adaptations qui resserrent.

## 5. Priorités consolidées

1. **Corriger la stat du BB au BTN** (445 questions) : compter ses calls sur les folds du SB.
2. **Assainir les reads** :
   - retirer la stat de call sous 10 limps ;
   - faire citer à R13 le nombre de limps ;
   - exiger un écart significatif (au moins 1,5 écart-type) pour les adaptations, R12, R13 et l'identification ; sinon, la question devient « échantillon ».
3. **Rééquilibrer les séries GTO et exploitant** selon la fréquence réelle, avec planchers et plafonds.
4. **Refaire les arbres HRC** : open à 2 BB (BTN, SB, heads-up), un seul arbre par tapis, option tapis jusqu'à 20 BB. Retirer ou recalculer les 664 spots mal convergés et les nœuds à EV nulle.
5. **Questions exploitantes « plus serré »** : calling station (tapis pour la valeur), et des « inconnu » où la théorie tient, pour que le type ne se devine plus.
6. **Recaler le rec passif face au limp** sur des mains réelles du field (fin du « tapis 94 % »). Trancher le désaccord sur les folds à 10-12 BB.
7. **Rendre l'EV conforme à l'énoncé** : calculer à partir des seules stats affichées, ou afficher la stat d'iso. Réécrire R4 et R12 selon les deux stats, et dédoublonner tous types confondus.
8. **Corriger les textes** :
   - SB face au BTN : dire que le BB parle derrière (14 verdicts faux) ;
   - « relance à X BB » quand X est le tapis ;
   - pastilles (rec passif / nit) ;
   - postflop : payer une paire face à une petite mise, revoir la donk bet du BB en heads-up.
9. **Étendre l'exploitant** : open à 2 BB et iso non all-in, 13-25 BB, tapis inégaux, limp du BTN et pots limpés à 3, SB face à l'iso après son limp.
10. **Premier module postflop** : pots limpés en heads-up et BvB.

**Limite commune aux trois audits** : aucun coach n'avait de base de mains réelles du field. Les fréquences « réelles » viennent de HRC (joueurs théoriques), et les jugements sur les profils sont des avis de coach. Les priorités 3 et 6 gagneraient à être calées sur un historique de mains Expresso.

## 6. Corrections appliquées (22/10/2026)

Banque exploitante `exploit_field/2026.10.22-1` (moteur v4.4, 4400 questions) ; tirage GTO et exploitant revus ; nettoyage des spots GTO. Bilan après corrections : `apres_corrections/`.

| Priorité | Fait |
|---|---|
| 1. Stat du BB au BTN | Ses calls se comptent sur les folds du SB. La stat impossible a disparu (test). |
| 2. Reads | La stat de call après limp n'est plus affichée sous 10 limps. Les adaptations, R12, R13 et l'identification exigent un écart d'au moins 1,5 écart-type. La correction cite le bon échantillon (« 16 limps observés »). R12 n'est plus citée quand il paie aussi plus que la théorie. R4 ne s'applique qu'à un joueur qui paie trop. |
| 3. Équilibre des séries | GTO : tranches de tapis à parts égales, puis chaque situation selon sa fréquence réelle ; les situations rares se partagent 10 %. Exploitant : 33 % premier à parler, 38 % face au tapis, 24 % face au limp, 5 % lecture ; tapis puis bonne réponse tirés à parts égales. |
| 5. Adaptations « plus serré » | 110 adaptations : payer → fold (80), tapis théorique → fold (22), tapis → check (8), contre 0 avant. S'y ajoutent 341 « tapis théorique → limp », désormais réservées au joueur qui paie trop. Nouvelle règle R16 : « Il paie trop ton tapis : garde-le pour les mains qui battent ses calls. » |
| 6. Type caché | Avant la réponse, la question affiche seulement « Vilain inconnu » ou « Vilain observé ». Piège, adaptation et échantillon se découvrent à la correction. |
| 7. Doublons | Une adaptation qui a l'EV du vilain inconnu est retirée, ainsi que les énoncés identiques. |
| 8. Textes | SB face au tapis du BTN : « le BB parle encore derrière » au lieu d'un faux « assez pour payer ». « Tu prends le pot de 2 BB ». Postflop : « paie avec une paire ou un tirage ». « À retenir » GTO : « avec 8 BB de tapis » au lieu de « à 8 BB », et « face à deux joueurs à tapis ». La 2e ligne de pourcentage est supprimée. Profils : phrase cassée corrigée. |
| Pastilles | Le limp au SB est affiché en plus du tapis et du call : il sépare le rec passif du nit (« Nit » devient une bonne réponse possible, sur 2 questions seulement : à renforcer). |
| 4 (en partie). GTO | Les spots que HRC a mal résolus sont écartés : 581 spots dont plus de la moitié des mains ont un regret supérieur à 0,1 BB. Sont aussi retirées les mains dont la référence change d'un arbre à l'autre pour un même spot à l'écran, les nœuds à EV toutes nulles et AA ou KK limpés au BTN. Il reste 1946 spots et 134 577 questions. |

Effet mesuré (3000 séries simulées) :

| | Avant | Après | Jeu réel |
|---|---|---|---|
| GTO : situations rares (moins de 1 % de la tranche) | 42 % | 9 % | — |
| GTO : BTN premier à parler | 7 % | 22 % | 22 % |
| GTO : SB premier à parler en heads-up | 6 % | 15 % | 17 % |
| GTO : BB face au tapis du SB, BTN fold | 0,5 % | 4,4 % | 4,8 % |
| Exploitant : BB face au limp du SB | 51 % | 23 % | — |

**Reste à faire, hors de portée sans nouvelles données :**
- Refaire les arbres HRC : open à 2 BB, un seul arbre par tapis, tapis jusqu'à 20 BB. Il faut de nouveaux calculs HRC.
- Recaler le rec passif face au limp (la réponse « tapis » reste majoritaire dans la banque ; le tirage l'équilibre). Il faut un historique de mains du field.
- Trancher le fold à 10-12 BB contre un inconnu (désaccord Lucho / Lucky).
- Étendre l'exploitant (13-25 BB, open à 2 BB, iso non all-in, tapis inégaux, limp du BTN) et le postflop : il faut des développements du moteur et des calculs HRC.
