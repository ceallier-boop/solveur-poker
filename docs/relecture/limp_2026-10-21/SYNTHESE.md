# Relecture des questions « BB face au limp du SB » : synthèse et corrections (21/10/2026)

60 questions (`questions.md`, banque `exploit_field/2026.10.20-4`), relues par trois experts IA (Lucho, PA, Lucky).
Leurs grilles et remarques sont dans ce dossier (`reponses_*.csv`, `remarques_*.md`).

## Verdicts sur les décisions

| Expert | Validées | Contestées | Incertaines |
|---|---|---|---|
| Lucho | 59 | 0 | 1 (L35) |
| Lucky | 59 | 0 | 1 (L35) |
| PA | 56 | 1 (L21 : il fallait checker) | 3 (L01, L11, L43) |

Les décisions préflop tiennent. Les trois experts relèvent les mêmes défauts : la position est fausse en heads-up, la règle citée ne colle pas aux stats affichées, et les textes sont trop longs.

## Constats et corrections (banque `exploit_field/2026.10.21-1`, moteur v4.3)

| Constat (experts) | Gravité | Correction |
|---|---|---|
| En heads-up, les fiches disent « tu joues en position » alors que le SB est au bouton : le BB parle en premier après le flop (L31 à L60, les trois experts) | bloquant | Position calculée selon la table : en heads-up, le BB est hors de position et le SB en position ; à 3 (BvB), c'est l'inverse. Le « Pourquoi » dit maintenant : « Après un check, tu parles en premier au flop (il est au bouton) : ta main rapporte moins. D'où plus de tapis en heads-up. » L'EV du check vient de HRC, qui connaît la position : seul le texte était faux. |
| R12 « complète trop et se couche » affichée alors que le vilain complète moins que la théorie ou paie plus (L01, L02, L21, L34, L43, L59) ; R13 « paie ton tapis » alors qu'il se couche 69 % du temps (L13) | majeur | Quatre règles distinctes, choisies d'après les stats **affichées** : R12 (il complète beaucoup : tapis plus large), R13 (il se couche souvent face au tapis : tapis plus large), R14 (il paie souvent : tapis pour les bonnes mains, check pour les autres), R15 (il complète peu : son limp est fort, checke tes mains moyennes). Une question sans stat qui justifie sa réponse est retirée. |
| Stat de call lue sur 2 à 5 limps (L01, L02, L09, L17, L23, L40) | majeur | La stat de call après limp ne compte qu'à partir de 10 limps observés. |
| « Complété 0 fois » alors qu'il complète dans ce coup ; R10 « ne complète pas assez » alors que la stat affichée est au-dessus de la théorie | mineur | Plus de question à 0 limp observé ; le défaut cité (« il semble… ») est celui des stats affichées. |
| « Reg » sans preuve dans l'énoncé (L10, L14, L42) | mineur | R11 devient « Ses stats collent à la théorie : joue la théorie. » |
| Égalités ou écarts minimes présentés comme une seule bonne réponse (L29 à EV égales, L47 à 0,06 BB) | mineur | Pas de question notée sous 0,05 BB d'écart. Sous 0,1 BB, la correction ajoute « Écart faible : les deux options sont proches. » |
| Doublons : même main, mêmes EV (L45, L48, L58) | mineur | Une seule question par main, décision et EV (à 0,01 BB près), quel que soit l'échantillon affiché. |
| Les chiffres du « Pourquoi » (fold, équité) ne recomposent pas l'EV affichée (PA : plus de 0,08 BB d'écart sur une vingtaine de fiches) | mineur | L'EV vient de la solution HRC, ajustée à ce vilain ; les fréquences et l'équité expliquent la tendance. L'encadré des gains le dit : « Gain par rapport au fold (HRC, ajusté à ce vilain) », et l'EV n'est plus répétée dans le « Pourquoi ». Un calcul exact sans HRC s'écarterait de la décision HRC sur 15 à 50 % des mains : nous gardons HRC. |
| Postflop : des stats, pas de plan ; ligne « avantage de range 44-46 % » identique partout ; deux phrases contradictoires ; liste « ce qui avantage ta main » vide (L13, L18, L55, L56, L59) | majeur | Section réécrite : SPR, position, **plan en trois consignes** selon la position (par exemple « Il checke : mise environ 1 BB très souvent »), puis trois points au plus pour ta main et pour la sienne. La ligne d'avantage de range est supprimée et la liste n'est jamais vide. |
| Fiches trop longues (environ 25 lignes, EV répétée trois fois), jargon | majeur | Correction en trois blocs courts : décision, pourquoi (2 ou 3 lignes), postflop. La phrase générique sur les stats est supprimée. Règles R0 à R15 réécrites en une phrase. |
| Iso-relance non all-in absente (utile dès 10 BB, la norme à 12 BB) | limite | Pas encore proposée : le moteur ne sait pas l'ajuster au vilain. Les mains que HRC isole à 3 BB au moins 30 % du temps sont retirées, pour ne pas imposer « check ou tapis » quand la vraie réponse est l'iso. À ajouter dans une prochaine version. |
| L35 (K4s à 6 BB, check du moteur ; Lucho et Lucky : tapis) | à revérifier | La question disparaît : sa stat de call reposait sur moins de 10 limps. |

## Banque × 10

**Version 2026.10.21-1** : 2173 questions (× 4,9), proportions de la banque de référence gardées au plus près.

**Version 2026.10.21-2 (servie)** : 4400 questions (× 10). Le porteur du projet a tranché : le volume prime sur les proportions. Les parts de référence sont visées d'abord, puis la banque est complétée sans plafond. Le rec passif et le vilain inconnu manquent de candidats : il n'y a qu'une question par main et par décision une fois les doublons d'EV retirés. Leur part baisse donc dans la banque. En série, le tirage reste pondéré par la part de chaque profil dans le field, donc le rec passif reste majoritaire dans ce que voit le joueur.

| | Référence (440) | 2026.10.21-2 (4400) |
|---|---|---|
| Rec passif | 58,6 % | 33,4 % |
| Nit | 6,4 % | 20,3 % |
| Calling station | 12,0 % | 19,0 % |
| Adaptation | 36,4 % | 42,5 % |
| Piège | 32,0 % | 41,0 % |
| Vilain inconnu | 18,9 % | 6,0 % |
| BB face au limp du SB (deux situations) | 30 % | 32 % |
