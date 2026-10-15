# SpinsAcademy : 300 questions à relire

Consignes : `CONSIGNES.md`. Réponses : `reponses_modele.csv`.

## Q001 · GTO · heads-up · BB face à un limp · 10 BB · A9o

Type : décision nette · EV : HRC · tapis SB 10 / BB 10 · arbre 100650d1

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Le SB complète.
Tu es au BB avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.225 | 0 % | 0.402 | erreur |
| Relancer à 2 BB | +1.454 | 0 % | 0.172 | erreur |
| Tapis (10 BB) | +1.626 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (10 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (10 BB), +0,4 BB par rapport au check.
> Ton tapis met la pression maximale : l'adversaire se couche environ 71 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 36 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Autre option : relancer à 2 BB, 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (10 BB) » : K7s, Q6o, 86o, 83s, 75o.

**Correction affichée si le joueur joue « Relancer à 2 BB » (erreur la plus tentante)**

> Action de référence : Tapis (10 BB), +0,4 BB par rapport au check.
> Ton choix (relancer à 2 BB) rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 71 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à un limp à 10 BB (heads-up), on part à tapis avec environ 34 % des mains qui arrivent ici.
> Ici, on part à tapis avec 36 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (10 BB) » : K7s, Q6o, 86o, 83s, 75o.


## Q002 · GTO · 3-handed · BTN premier à parler · 20 BB · 62o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 6♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.325 | 0 % | 0.325 | erreur |
| Relancer à 2 BB | -0.341 | 0 % | 0.341 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; 62o en fait partie.
> Autre option : limper (1 BB), 0,33 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J4s, Q5s, 54s, A3o, 75s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,33 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 20 BB, on se couche avec environ 62 % des mains qui arrivent ici.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; 62o en fait partie.
> Autre option : relancer à 2 BB, 0,34 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J4s, Q5s, 54s, A3o, 75s.


## Q003 · GTO · 3-handed · BB face à un tapis · 10 BB · K9s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN part à tapis (15 BB, soit 10 BB effectifs).
Le SB se couche.
Tu es au BB avec K♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.090 | erreur |
| Payer le tapis (9 BB de plus) | +0.090 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (9 BB de plus), +0,09 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range de tapis, K9s a 44,3 % d'équité : marge de 0,4 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,09 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : A5o (44,4 %), A2s (44,6 %), JTs (44,7 %) ; se couchent déjà : KTo (43,7 %), T9s (43,4 %), A4o (43,1 %).
> Ici, on paie avec 22 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (9 BB de plus), +0,09 BB par rapport au fold.
> Ton choix (fold) rapporte 0,09 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 10 BB, on paie avec 22+, A2s+, A5o+, K9s+, KJo+, QTs+, JTs (environ 22 % des mains qui arrivent ici).
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range de tapis, K9s a 44,3 % d'équité : marge de 0,4 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,09 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : A5o (44,4 %), A2s (44,6 %), JTs (44,7 %) ; se couchent déjà : KTo (43,7 %), T9s (43,4 %), A4o (43,1 %).
> Ici, on paie avec 22 % des mains qui arrivent à cette décision.


## Q004 · GTO · 3-handed · BB face à un tapis · 10 BB · JTo

Type : décision nette · EV : HRC · tapis BTN 45 / SB 20 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 45 / 20 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB part à tapis (20 BB, soit 10 BB effectifs).
Tu es au BB avec J♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.919 | 0 % | 0.919 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; JTo en fait partie.
> Repère : il faut environ 40 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (9 BB de plus), 0,92 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A9s, J9s, 86s, T8s, K8s.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 0,92 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB, on ne joue que 33+, ATs+, AJo+, KTs+, KQo, QJs, 98s (environ 13 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; JTo en fait partie.
> Repère : il faut environ 40 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : A9s, J9s, 86s, T8s, K8s.


## Q005 · GTO · heads-up · BB face à un tapis · 4 BB · J6o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 4 / 8 BB (SB / BB).
Le SB part à tapis (4 BB).
Tu es au BB avec J♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.346 | erreur |
| Payer le tapis (3 BB de plus) | +0.346 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3 BB de plus), +0,35 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, J6o a 41,8 % d'équité : marge de 4,3 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,35 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T5o (37,6 %), 76o (37,7 %), 53s (37,8 %) ; se couchent déjà : 92s (37,3 %), 43s (37,1 %), T4o (37,1 %).
> Ici, on paie avec 74 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3 BB de plus), +0,35 BB par rapport au fold.
> Ton choix (fold) rapporte 0,35 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 4 BB (heads-up), on paie avec environ 74 % des mains qui arrivent ici.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, J6o a 41,8 % d'équité : marge de 4,3 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,35 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T5o (37,6 %), 76o (37,7 %), 53s (37,8 %) ; se couchent déjà : 92s (37,3 %), 43s (37,1 %), T4o (37,1 %).
> Ici, on paie avec 74 % des mains qui arrivent à cette décision.


## Q006 · GTO · heads-up · SB face à un tapis · 25 BB · 85o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 25 / BB 25 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 25 / 25 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB part à tapis (25 BB).
Tu es au SB avec 8♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (21,5 BB de plus) | -4.597 | 0 % | 4.597 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 21,5 BB à payer pour un pot final de 50 BB, il faut 43,0 % d'équité pour payer.
> Contre sa range de tapis, 85o a 33,8 % d'équité : 9,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 4,6 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 43,0 %, à 2 points près), paient encore : J8s (43,1 %), KTo (43,1 %), A7s (43,1 %) ; se couchent déjà : QTo (42,99 %), A9o (42,8 %), 33 (42,7 %).
> Ici, on paie avec 36 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (21,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (21,5 BB de plus) » rapporte 4,6 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 25 BB (heads-up), on ne joue que 44+, A8s+, ATo+, K9s+, KJo+, Q9s+ (environ 36 % des mains qui arrivent ici).
> Cote du pot : 21,5 BB à payer pour un pot final de 50 BB, il faut 43,0 % d'équité pour payer.
> Contre sa range de tapis, 85o a 33,8 % d'équité : 9,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 4,6 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 43,0 %, à 2 points près), paient encore : J8s (43,1 %), KTo (43,1 %), A7s (43,1 %) ; se couchent déjà : QTo (42,99 %), A9o (42,8 %), 33 (42,7 %).
> Ici, on paie avec 36 % des mains qui arrivent à cette décision.


## Q007 · GTO · heads-up · SB face à un tapis · 10 BB · T7s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 40 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB part à tapis (10 BB).
Tu es au SB avec T♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.173 | erreur |
| Payer le tapis (6,5 BB de plus) | +1.173 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (6,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (6,5 BB de plus), +1,17 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 6,5 BB à payer pour un pot final de 20 BB, il faut 32,5 % d'équité pour payer.
> Contre sa range de tapis, T7s a 38,4 % d'équité : marge de 5,9 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,17 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 32,5 %, à 2 points près), paient encore : J5o (32,8 %), J6o (32,9 %), 32s (33,3 %) ; se couchent déjà : Q3o (32,2 %), J4o (32,2 %).
> Ici, on paie avec 100 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (6,5 BB de plus), +1,17 BB par rapport au fold.
> Ton choix (fold) rapporte 1,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 10 BB (heads-up), on paie avec environ 100 % des mains qui arrivent ici.
> Cote du pot : 6,5 BB à payer pour un pot final de 20 BB, il faut 32,5 % d'équité pour payer.
> Contre sa range de tapis, T7s a 38,4 % d'équité : marge de 5,9 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,17 BB sur ce pot) : il fallait payer le tapis (6,5 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 32,5 %, à 2 points près), paient encore : J5o (32,8 %), J6o (32,9 %), 32s (33,3 %) ; se couchent déjà : Q3o (32,2 %), J4o (32,2 %).
> Ici, on paie avec 100 % des mains qui arrivent à cette décision.


## Q008 · GTO · 3-handed · BTN face à un tapis · 20 BB · K9o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Tu relances à 2 BB.
Le SB relance à 6,6 BB.
Le BB part à tapis (20 BB).
Tu es au BTN avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (18 BB de plus) | -4.686 | 0 % | 4.686 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (18 BB de plus), 4,69 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q4s, KTs, J7s, A3s, 95s.

**Correction affichée si le joueur joue « Payer le tapis (18 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (18 BB de plus) » rapporte 4,69 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BTN face à un tapis à 20 BB, on ne joue que 99+, ATs+, AJo+, KTs+, J9s+, 98s, 76s (environ 30 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : Q4s, KTs, J7s, A3s, 95s.


## Q009 · GTO · 3-handed · SB face à une relance · 8 BB · J8o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec J♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.186 | erreur |
| Payer (2 BB de plus) | +0.186 | 100 % | 0.000 | correct |
| Tapis (8 BB) | +0.117 | 0 % | 0.070 | imprécision |

**Référence de l'application** : Payer (2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (2 BB de plus), +0,19 BB par rapport au fold.
> Nuance : tapis (8 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 37 % des mains qui arrivent à cette décision ; J8o en fait partie.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : 53s, JTo, 54o, J6o, T9o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer (2 BB de plus), +0,19 BB par rapport au fold.
> Nuance : tapis (8 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 8 BB, on paie avec environ 32 % des mains qui arrivent ici.
> Ici, on paie avec 37 % des mains qui arrivent à cette décision ; J8o en fait partie.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : 53s, JTo, 54o, J6o, T9o.


## Q010 · GTO · heads-up · SB face à une relance · 18 BB · 94s

Type : stratégie mixte · EV : HRC · tapis SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 18 / 18 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec 9♠4♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 20 % | 0.042 | correct |
| Payer (2 BB de plus) | +0.042 | 80 % | 0.000 | correct |
| Tapis (18 BB) | -1.180 | 0 % | 1.221 | erreur |

**Référence de l'application** : Payer (2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (2 BB de plus), +0,04 BB par rapport au fold.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 59 % des mains qui arrivent à cette décision ; 94s en fait partie.
> Autre option : tapis (18 BB), 1,22 BB de moins.
> 94s est jouée de plusieurs façons (fold 20 %, payer (2 BB de plus) 80 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : A2s, 54o, 92s, A5s, Q5o.

**Correction affichée si le joueur joue « Tapis (18 BB) » (erreur la plus tentante)**

> Action de référence : Payer (2 BB de plus), +0,04 BB par rapport au fold.
> Ton choix « tapis (18 BB) » rapporte 1,22 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 18 BB (heads-up), on paie avec environ 62 % des mains qui arrivent ici.
> Ici, on paie avec 59 % des mains qui arrivent à cette décision ; 94s en fait partie.
> 94s est jouée de plusieurs façons (fold 20 %, payer (2 BB de plus) 80 %) : ces actions ont une valeur proche. Ton choix « tapis (18 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : A2s, 54o, 92s, A5s, Q5o.


## Q011 · GTO · heads-up · BB face à un limp · 20 BB · AQs

Type : décision nette · EV : HRC · tapis SB 20 / BB 30 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 20 / 30 BB (SB / BB).
Le SB complète.
Tu es au BB avec A♠Q♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.933 | 0 % | 0.510 | erreur |
| Relancer à 3 BB | +2.443 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,51 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 33 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 39 % des mains qui arrivent à cette décision ; AQs en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : 64s, T9o, 65o, T7o, K7s.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,51 BB par rapport au check.
> Ton choix (check) rapporte 0,51 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 33 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 20 BB (heads-up), on relance avec environ 39 % des mains qui arrivent ici.
> Ici, on relance avec 39 % des mains qui arrivent à cette décision ; AQs en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : 64s, T9o, 65o, T7o, K7s.


## Q012 · exploitant · 3-handed · SB premier à parler · 15 BB · K5o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 30 / SB 30 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 44,4 % de ses mains (équilibre push/fold : 28,5 %)

**Énoncé** : 3 joueurs, tapis 30 / 30 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 44,4 % de ses mains dans cette situation (équilibre push/fold : 28,5 %).
Tu joues en tapis ou fold.
Tu es au SB avec K♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (15 BB) | -0.090 | 0 % | 0.090 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,06 et 0,5 BB.
> Il se couche 57 % du temps face à ton tapis (équilibre push/fold : 72 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, K5o a 41,1 % d'équité contre sa range de call (équilibre push/fold : 35,0 %) et tout se joue à tapis (15 BB effectifs).
> Contre ce profil, on part à tapis avec 36 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 46 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (15 BB) » perd entre 0,06 et 0,5 BB.
> Il se couche 57 % du temps face à ton tapis (équilibre push/fold : 72 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, K5o a 41,1 % d'équité contre sa range de call (équilibre push/fold : 35,0 %) et tout se joue à tapis (15 BB effectifs).
> Contre ce profil, on part à tapis avec 36 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 46 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q013 · GTO · 3-handed · BTN premier à parler · 12 BB · K2o

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 18 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec K♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.178 | 0 % | 0.178 | erreur |
| Relancer à 2,3 BB | -0.185 | 0 % | 0.185 | erreur |
| Tapis (12 BB) | -0.536 | 0 % | 0.536 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; K2o en fait partie.
> Autre option : limper (1 BB), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J9o, K3s, Q9o, 76s, 97s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 12 BB, on ne joue que 22+, A2+, K5s+, K9o+, Q8s+, Q9o+, J8s+, JTo, T8s+, 97s+, 87s (environ 34 % des mains qui arrivent ici).
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; K2o en fait partie.
> Autre option : relancer à 2,3 BB, 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J9o, K3s, Q9o, 76s, 97s.


## Q014 · GTO · 3-handed · BB face à un limp · 20 BB · AJo

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec A♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.740 | 0 % | 0.678 | erreur |
| Relancer à 3 BB | +2.417 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,68 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 39 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 36 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : A6s, JTo, T7o, Q6o, T6o.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,68 BB par rapport au check.
> Ton choix (check) rapporte 0,68 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 39 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 20 BB, on relance avec environ 32 % des mains qui arrivent ici.
> Ici, on relance avec 36 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : A6s, JTo, T7o, Q6o, T6o.


## Q015 · GTO · 3-handed · BB face à un limp · 12 BB · A4o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec A♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.379 | 0 % | 0.154 | erreur |
| Relancer à 3 BB | +1.530 | 0 % | 0.003 | correct |
| Tapis (12 BB) | +1.533 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (12 BB) ou relancer à 3 BB (moins de 0,02 BB d'écart).
> Ton tapis met la pression maximale : l'adversaire se couche environ 78 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : Q5s, AJo, Q3o, K2s, K4o.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (12 BB) ou relancer à 3 BB (moins de 0,02 BB d'écart).
> Ton choix (check) rapporte 0,15 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 78 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à un limp à 12 BB, on part à tapis avec A2o+ (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 93 % d'entre elles).
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : Q5s, AJo, Q3o, K2s, K4o.


## Q016 · GTO · 3-handed · BB face à un tapis · 16 BB · QTs

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN part à tapis (16 BB).
Le SB se couche.
Tu es au BB avec Q♠T♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.071 | erreur |
| Payer le tapis (15 BB de plus) | +0.071 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15 BB de plus), +0,07 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 15 BB à payer pour un pot final de 32,5 BB, il faut 46,2 % d'équité pour payer.
> Contre sa range de tapis, QTs a 46,4 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,07 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,2 %, à 2 points près), paient encore : KTs (46,8 %), A5s (47,2 %), A6s (47,4 %) ; se couchent déjà : JTs (46,0 %), KJo (45,8 %), A4s (45,7 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15 BB de plus), +0,07 BB par rapport au fold.
> Ton choix (fold) rapporte 0,07 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 16 BB, on paie avec 33+, A5s+, A8o+, KTs+, KQo, QTs+ (environ 16 % des mains qui arrivent ici).
> Cote du pot : 15 BB à payer pour un pot final de 32,5 BB, il faut 46,2 % d'équité pour payer.
> Contre sa range de tapis, QTs a 46,4 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,07 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,2 %, à 2 points près), paient encore : KTs (46,8 %), A5s (47,2 %), A6s (47,4 %) ; se couchent déjà : JTs (46,0 %), KJo (45,8 %), A4s (45,7 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.


## Q017 · GTO · 3-handed · BTN premier à parler · 25 BB · Q4o

Type : décision nette · EV : HRC · tapis BTN 35 / SB 15 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 35 / 15 / 25 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec Q♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.181 | 0 % | 0.181 | erreur |
| Relancer à 2,3 BB | -0.211 | 0 % | 0.211 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; Q4o en fait partie.
> Autre option : limper (1 BB), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J6s, T6s, 54s, 86s, 65s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 25 BB, on se couche avec environ 65 % des mains qui arrivent ici.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; Q4o en fait partie.
> Autre option : relancer à 2,3 BB, 0,21 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J6s, T6s, 54s, 86s, 65s.


## Q018 · GTO · 3-handed · BB face à un limp · 16 BB · AKo

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec A♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +2.011 | 0 % | 0.690 | erreur |
| Relancer à 3 BB | +2.700 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,69 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 42 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 34 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : T3o, A6s, 96o, 95o, A6o.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,69 BB par rapport au check.
> Ton choix (check) rapporte 0,69 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 42 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 16 BB, on relance avec 22+, A5s+, A7o+, KTs+, KJo+, QJ, J9o+, 32o (environ 28 % des mains qui arrivent ici ; règle simplifiée, exacte pour 93 % d'entre elles).
> Ici, on relance avec 34 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : T3o, A6s, 96o, 95o, A6o.


## Q019 · exploitant · 3-handed · BB face à un tapis · 4 BB · 95o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 35,7 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 4 / 8 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Le SB se couche.
Profil fictif « Prudent » : ce BTN part à tapis avec 35,7 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec 9♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3 BB de plus) | -0.218 | 0 % | 0.218 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 95o a 32,7 % d'équité : 2,6 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 63s (35,33 %), K2o (35,4 %), T4s (35,4 %) ; se couchent déjà : 65o (35,1 %), 86o (35,0 %), T7o (34,9 %).
> Contre ce profil, on paie avec 58 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (3 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (3 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 95o a 32,7 % d'équité : 2,6 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 63s (35,33 %), K2o (35,4 %), T4s (35,4 %) ; se couchent déjà : 65o (35,1 %), 86o (35,0 %), T7o (34,9 %).
> Contre ce profil, on paie avec 58 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q020 · GTO · 3-handed · BB face à un limp · 8 BB · 87o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu es au BB avec 8♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | -0.243 | 100 % | 0.000 | correct |
| Tapis (8 BB) | -0.742 | 0 % | 0.499 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 78 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Autre option : tapis (8 BB), 0,5 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : Q9s, K4s, A7o, A4s, A6s.

**Correction affichée si le joueur joue « Tapis (8 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (8 BB) » rapporte 0,5 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 8 BB, on checke avec environ 79 % des mains qui arrivent ici.
> Ici, on checke avec 78 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : Q9s, K4s, A7o, A4s, A6s.


## Q021 · GTO · heads-up · BB face à un tapis · 4 BB · QTo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 4 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 4 / 4 BB (SB / BB).
Le SB part à tapis (4 BB).
Tu es au BB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.286 | erreur |
| Payer le tapis (3 BB de plus) | +1.286 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3 BB de plus), +1,29 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, QTo a 53,6 % d'équité : marge de 16,1 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 1,29 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T5o (37,53 %), 76o (37,7 %), 53s (37,7 %) ; se couchent déjà : 92s (37,3 %), 43s (37,1 %), T4o (37,0 %).
> Ici, on paie avec 74 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3 BB de plus), +1,29 BB par rapport au fold.
> Ton choix (fold) rapporte 1,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 4 BB (heads-up), on paie avec environ 74 % des mains qui arrivent ici.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, QTo a 53,6 % d'équité : marge de 16,1 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 1,29 BB sur ce pot) : erreur nette, il fallait payer le tapis (3 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T5o (37,53 %), 76o (37,7 %), 53s (37,7 %) ; se couchent déjà : 92s (37,3 %), 43s (37,1 %), T4o (37,0 %).
> Ici, on paie avec 74 % des mains qui arrivent à cette décision.


## Q022 · GTO · 3-handed · BTN face à un tapis · 6 BB · T9s

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Tu limpes.
Le SB part à tapis (6 BB).
Le BB paie le tapis.
Tu es au BTN avec T♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.375 | erreur |
| Payer le tapis (5 BB de plus) | +0.375 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5 BB de plus), +0,37 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 66 % des mains qui arrivent à cette décision ; T9s en fait partie.
> Repère : il faut 28 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : T8s, Q6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5 BB de plus), +0,37 BB par rapport au fold.
> Ton choix (fold) rapporte 0,37 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 6 BB, on paie avec QQ+, J7s+, T8s+ (environ 68 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on paie avec 66 % des mains qui arrivent à cette décision ; T9s en fait partie.
> Repère : il faut 28 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : T8s, Q6s.


## Q023 · GTO · 3-handed · SB face à un tapis · 15 BB · KK

Type : stratégie mixte · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB part à tapis (10 BB).
Le BTN paie le tapis.
Tu es au SB avec K♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 6.743 | erreur |
| Payer le tapis (9 BB de plus) | +6.743 | 90 % | 0.001 | correct |
| Tapis (15 BB) | +6.743 | 10 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : payer le tapis (9 BB de plus) ou tapis (15 BB) (moins de 0,02 BB d'écart).
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 12 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> KK est jouée de plusieurs façons (payer le tapis (9 BB de plus) 90 %, tapis (15 BB) 10 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « payer le tapis (9 BB de plus) » : A7s, 98s, AQs, QJo, JTs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : payer le tapis (9 BB de plus) ou tapis (15 BB) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 6,74 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 15 BB, on paie avec KK+, QJs (environ 3 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on paie avec 12 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> KK est jouée de plusieurs façons (payer le tapis (9 BB de plus) 90 %, tapis (15 BB) 10 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « payer le tapis (9 BB de plus) » : A7s, 98s, AQs, QJo, JTs.


## Q024 · exploitant · 3-handed · SB premier à parler · 8 BB · KJo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 62,2 % de ses mains (équilibre push/fold : 45,1 %)

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 62,2 % de ses mains dans cette situation (équilibre push/fold : 45,1 %).
Tu joues en tapis ou fold.
Tu es au SB avec K♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.548 | erreur |
| Tapis (8 BB) | +1.547 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (8 BB).
> Partir à tapis gagne entre 1 et 2 BB.
> Il se couche 40 % du temps face à ton tapis (équilibre push/fold : 57 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, KJo a 56,7 % d'équité contre sa range de call (équilibre push/fold : 53,0 %) et tout se joue à tapis (8 BB effectifs).
> Contre ce profil, on part à tapis avec 50 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 61 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (8 BB).
> Ton choix (fold) perd entre 1 et 2 BB.
> Il se couche 40 % du temps face à ton tapis (équilibre push/fold : 57 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, KJo a 56,7 % d'équité contre sa range de call (équilibre push/fold : 53,0 %) et tout se joue à tapis (8 BB effectifs).
> Contre ce profil, on part à tapis avec 50 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 61 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q025 · exploitant · 3-handed · BB face à un tapis · 18 BB · 22

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 43,7 % de ses mains (équilibre push/fold : 28 %)

**Énoncé** : 3 joueurs, tapis 18 / 12 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 43,7 % de ses mains dans cette situation (équilibre push/fold : 28 %).
Tu es au BB avec 2♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -0.061 | 0 % | 0.061 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, 22 a 46,4 % d'équité : 0,2 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : K7s (47,1 %), A3o (47,1 %), QTo (47,2 %) ; se couchent déjà : A2o (46,5 %), K6s (46,4 %), K5s (45,6 %).
> Contre ce profil, on paie avec 27 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 14 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (17 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, 22 a 46,4 % d'équité : 0,2 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : K7s (47,1 %), A3o (47,1 %), QTo (47,2 %) ; se couchent déjà : A2o (46,5 %), K6s (46,4 %), K5s (45,6 %).
> Contre ce profil, on paie avec 27 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 14 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q026 · GTO · 3-handed · SB face à une relance · 15 BB · K3s

Type : décision nette · EV : HRC · tapis BTN 35 / SB 15 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 35 / 15 / 25 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB relance à 9,9 BB.
Le BTN se couche.
Tu es au SB avec K♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (7,59 BB de plus) | -0.186 | 0 % | 0.186 | erreur |
| Tapis (15 BB) | -0.753 | 0 % | 0.753 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 34 % des mains qui arrivent à cette décision ; K3s en fait partie.
> Autre option : payer (7,59 BB de plus), 0,19 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A8o, KJo, QTo, QTs, K7s.

**Correction affichée si le joueur joue « Payer (7,59 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (7,59 BB de plus) » rapporte 0,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 15 BB, on se couche avec environ 33 % des mains qui arrivent ici.
> Ici, on se couche avec 34 % des mains qui arrivent à cette décision ; K3s en fait partie.
> Autre option : tapis (15 BB), 0,75 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A8o, KJo, QTo, QTs, K7s.


## Q027 · GTO · 3-handed · SB premier à parler · 22 BB · 72o

Type : décision nette · EV : HRC · tapis BTN 22 / SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 22 / 22 / 22 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec 7♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.171 | 0 % | 0.171 | erreur |
| Relancer à 3,5 BB | -0.247 | 0 % | 0.247 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 29 % des mains qui arrivent à cette décision ; 72o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 62s, 52s, 63s, 73s, T6o.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB premier à parler à 22 BB, on se couche avec environ 28 % des mains qui arrivent ici.
> Ici, on se couche avec 29 % des mains qui arrivent à cette décision ; 72o en fait partie.
> Autre option : relancer à 3,5 BB, 0,25 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 62s, 52s, 63s, 73s, T6o.


## Q028 · GTO · 3-handed · BTN face à un tapis · 20 BB · A6s

Type : décision nette · EV : HRC · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Tu limpes.
Le SB complète.
Le BB part à tapis (15 BB).
Tu paies le tapis.
Le SB part à tapis (20 BB).
Tu es au BTN avec A♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 15.753 | erreur |
| Payer le tapis (5 BB de plus) | +15.753 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5 BB de plus), +15,75 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A6s en fait partie.
> Repère : il faut 9 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5 BB de plus), +15,75 BB par rapport au fold.
> Ton choix (fold) rapporte 15,75 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 20 BB, on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A6s en fait partie.
> Repère : il faut 9 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q029 · GTO · heads-up · SB face à un tapis · 22 BB · 99

Type : décision nette · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu relances à 7,8 BB.
Le BB part à tapis (22 BB).
Tu es au SB avec 9♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 9.312 | erreur |
| Payer le tapis (14,2 BB de plus) | +9.312 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14,2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (14,2 BB de plus), +9,31 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Repère : il faut 32 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (14,2 BB de plus), +9,31 BB par rapport au fold.
> Ton choix (fold) rapporte 9,31 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 22 BB (heads-up), on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Repère : il faut 32 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q030 · GTO · 3-handed · BB face à un tapis · 8 BB · Q5s

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (8 BB).
Tu es au BB avec Q♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.700 | erreur |
| Payer le tapis (5 BB de plus) | +0.700 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5 BB de plus), +0,7 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 74 % des mains qui arrivent à cette décision ; Q5s en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : T9o, 74s, 86s, 55, Q5o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5 BB de plus), +0,7 BB par rapport au fold.
> Ton choix (fold) rapporte 0,7 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 8 BB, on paie avec 33+, A2+, K2s+, K3o+, Q3s+, Q6o+, J9s+, J8o+ (environ 74 % des mains qui arrivent ici).
> Ici, on paie avec 74 % des mains qui arrivent à cette décision ; Q5s en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : T9o, 74s, 86s, 55, Q5o.


## Q031 · exploitant · 3-handed · BB face à un tapis · 15 BB · J9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 30 / SB 30 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 62,8 % de ses mains (équilibre push/fold : 45,7 %)

**Énoncé** : 3 joueurs, tapis 30 / 30 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (30 BB, soit 15 BB effectifs).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 62,8 % de ses mains dans cette situation (équilibre push/fold : 45,7 %).
Tu es au BB avec J♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.062 | erreur |
| Payer le tapis (14 BB de plus) | +0.062 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (14 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, J9o a 46,9 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q6s (46,8 %), K2s (47,1 %), Q7s (47,5 %) ; se couchent déjà : Q8o (46,5 %), K5o (46,5 %), T8s (46,2 %).
> Contre ce profil, on paie avec 38 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (14 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, J9o a 46,9 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q6s (46,8 %), K2s (47,1 %), Q7s (47,5 %) ; se couchent déjà : Q8o (46,5 %), K5o (46,5 %), T8s (46,2 %).
> Contre ce profil, on paie avec 38 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q032 · GTO · heads-up · SB premier à parler · 6 BB · J9s

Type : stratégie mixte · EV : HRC · tapis SB 6 / BB 6 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec J♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.681 | erreur |
| Compléter (0,5 BB de plus) | +0.672 | 70 % | 0.009 | correct |
| Tapis (6 BB) | +0.681 | 30 % | 0.000 | correct |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : compléter (0,5 BB de plus) ou tapis (6 BB) (moins de 0,02 BB d'écart).
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 13 % des mains qui arrivent à cette décision ; J9s en fait partie.
> J9s est jouée de plusieurs façons (compléter (0,5 BB de plus) 70 %, tapis (6 BB) 30 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : QTs, T9s, 94s, 66, T3s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : compléter (0,5 BB de plus) ou tapis (6 BB) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,68 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 6 BB (heads-up), on complète avec environ 13 % des mains qui arrivent ici.
> Ici, on complète avec 13 % des mains qui arrivent à cette décision ; J9s en fait partie.
> J9s est jouée de plusieurs façons (compléter (0,5 BB de plus) 70 %, tapis (6 BB) 30 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : QTs, T9s, 94s, 66, T3s.


## Q033 · GTO · 3-handed · SB face à un limp · 15 BB · 66

Type : décision nette · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.624 | erreur |
| Compléter (0,5 BB de plus) | +0.624 | 100 % | 0.000 | correct |
| Relancer à 4,5 BB | +0.046 | 0 % | 0.578 | erreur |
| Tapis (15 BB) | +0.243 | 0 % | 0.381 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +0,62 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 17 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Autre option : tapis (15 BB), 0,38 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K3s, T7s, 64s, J9s, QJs.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +0,62 BB par rapport au fold.
> Ton choix « tapis (15 BB) » rapporte 0,38 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB face à un limp à 15 BB, on complète avec environ 17 % des mains qui arrivent ici.
> Ici, on complète avec 17 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Autre option : relancer à 4,5 BB, 0,58 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K3s, T7s, 64s, J9s, QJs.


## Q034 · GTO · heads-up · BB face à un limp · 4 BB · 42o

Type : décision nette · EV : HRC · tapis SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 4 / 8 BB (SB / BB).
Le SB complète.
Tu es au BB avec 4♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.108 | 100 % | 0.000 | correct |
| Tapis (4 BB) | -0.427 | 0 % | 0.534 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 44 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Autre option : tapis (4 BB), 0,53 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : 85s, 97s, AJs, T9s, 44.

**Correction affichée si le joueur joue « Tapis (4 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (4 BB) » rapporte 0,53 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 4 BB (heads-up), on checke avec environ 44 % des mains qui arrivent ici.
> Ici, on checke avec 44 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : 85s, 97s, AJs, T9s, 44.


## Q035 · GTO · 3-handed · SB premier à parler · 20 BB · KJo

Type : stratégie mixte · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec K♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.743 | erreur |
| Compléter (0,5 BB de plus) | +0.702 | 50 % | 0.041 | correct |
| Relancer à 3,5 BB | +0.743 | 50 % | 0.000 | correct |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), jouée 50 % du temps, +0,7 BB par rapport au fold.
> L'option (relancer à 3,5 BB) vaut presque autant : 0,04 BB de plus en EV ; les deux sont acceptés.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 44 % des mains qui arrivent à cette décision ; KJo en fait partie.
> KJo est jouée de plusieurs façons (compléter (0,5 BB de plus) 50 %, relancer à 3,5 BB 50 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K6o, AQo, 83s, 88, 44.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), jouée 50 % du temps, +0,7 BB par rapport au fold.
> L'option (relancer à 3,5 BB) vaut presque autant : 0,04 BB de plus en EV ; les deux sont acceptés.
> Ton choix (fold) rapporte 0,74 BB de moins que relancer à 3,5 BB, la plus rentable.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 20 BB, on complète avec environ 43 % des mains qui arrivent ici.
> Ici, on complète avec 44 % des mains qui arrivent à cette décision ; KJo en fait partie.
> KJo est jouée de plusieurs façons (compléter (0,5 BB de plus) 50 %, relancer à 3,5 BB 50 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K6o, AQo, 83s, 88, 44.


## Q036 · GTO · 3-handed · BB face à un tapis · 4 BB · J6o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 4 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (4 BB).
Tu es au BB avec J♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.336 | erreur |
| Payer le tapis (3 BB de plus) | +0.336 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3 BB de plus), +0,34 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, J6o a 41,7 % d'équité : marge de 4,2 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,34 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 76o (37,6 %), 53s (37,7 %), 86o (37,8 %) ; se couchent déjà : T5o (37,47 %), 92s (37,2 %), 43s (37,1 %).
> Ici, on paie avec 73 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3 BB de plus), +0,34 BB par rapport au fold.
> Ton choix (fold) rapporte 0,34 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 4 BB, on paie avec environ 73 % des mains qui arrivent ici.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, J6o a 41,7 % d'équité : marge de 4,2 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,34 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 76o (37,6 %), 53s (37,7 %), 86o (37,8 %) ; se couchent déjà : T5o (37,47 %), 92s (37,2 %), 43s (37,1 %).
> Ici, on paie avec 73 % des mains qui arrivent à cette décision.


## Q037 · GTO · 3-handed · SB premier à parler · 12 BB · AA

Type : décision nette · EV : HRC · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec A♠A♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 4.079 | erreur |
| Compléter (0,5 BB de plus) | +4.079 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +3.794 | 0 % | 0.286 | erreur |
| Tapis (12 BB) | +3.535 | 0 % | 0.544 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +4,08 BB par rapport au fold.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> Ici, on complète avec 29 % des mains qui arrivent à cette décision ; AA en fait partie.
> Autre option : relancer à 3,5 BB, 0,29 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : Q5o, AKs, KJs, 94s, K7o.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +4,08 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> À retenir : au SB premier à parler à 12 BB, on complète avec environ 28 % des mains qui arrivent ici.
> Ici, on complète avec 29 % des mains qui arrivent à cette décision ; AA en fait partie.
> Autre option : tapis (12 BB), 0,54 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : Q5o, AKs, KJs, 94s, K7o.


## Q038 · exploitant · 3-handed · BB face à un tapis · 15 BB · QQ

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Serré (Nit) : part à tapis avec 29,6 % de ses mains (équilibre push/fold : 45,7 %)

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (20 BB, soit 15 BB effectifs).
Profil fictif « Serré (Nit) » : ce SB part à tapis avec 29,6 % de ses mains dans cette situation (équilibre push/fold : 45,7 %).
Tu es au BB avec Q♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 7.321 | erreur |
| Payer le tapis (14 BB de plus) | +7.321 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (14 BB de plus).
> Payer gagne plus de 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, QQ a 71,1 % d'équité : marge de 24,4 points au-dessus du seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : A5s (47,1 %), 33 (47,2 %), KQo (47,2 %) ; se couchent déjà : A7o (46,4 %), KTs (46,1 %), A4s (46,0 %).
> Contre ce profil, on paie avec 15 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (14 BB de plus).
> Ton choix (fold) perd plus de 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, QQ a 71,1 % d'équité : marge de 24,4 points au-dessus du seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : erreur nette, il fallait payer le tapis (14 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : A5s (47,1 %), 33 (47,2 %), KQo (47,2 %) ; se couchent déjà : A7o (46,4 %), KTs (46,1 %), A4s (46,0 %).
> Contre ce profil, on paie avec 15 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q039 · GTO · 3-handed · BB face à une relance · 15 BB · 74o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 40 / 15 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec 7♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,3 BB de plus) | -0.154 | 0 % | 0.154 | erreur |
| Tapis (15 BB) | -0.798 | 0 % | 0.798 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Autre option : payer (1,3 BB de plus), 0,15 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 93s, 84s, 72s, 75o, 74s.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 0,15 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 15 BB, on se couche avec environ 37 % des mains qui arrivent ici.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Autre option : tapis (15 BB), 0,8 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 93s, 84s, 72s, 75o, 74s.


## Q040 · exploitant · heads-up · SB premier à parler · 14 BB · Q3o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 14 / BB 14 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 45,5 % de ses mains (équilibre push/fold : 29,4 %)

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 45,5 % de ses mains dans cette situation (équilibre push/fold : 29,4 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (14 BB) | -0.812 | 0 % | 0.812 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,5 et 1 BB.
> Il se couche 54 % du temps face à ton tapis (équilibre push/fold : 70 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q3o a 35,5 % d'équité contre sa range de call (équilibre push/fold : 31,6 %) et tout se joue à tapis (14 BB effectifs).
> Contre ce profil, on part à tapis avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 48 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (14 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (14 BB) » perd entre 0,5 et 1 BB.
> Il se couche 54 % du temps face à ton tapis (équilibre push/fold : 70 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q3o a 35,5 % d'équité contre sa range de call (équilibre push/fold : 31,6 %) et tout se joue à tapis (14 BB effectifs).
> Contre ce profil, on part à tapis avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 48 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q041 · exploitant · 3-handed · BB face à un tapis · 10 BB · K9o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 73,6 % de ses mains (équilibre push/fold : 58,3 %)

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (50 BB, soit 10 BB effectifs).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 73,6 % de ses mains dans cette situation (équilibre push/fold : 58,3 %).
Tu es au BB avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.909 | erreur |
| Payer le tapis (9 BB de plus) | +1.909 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (9 BB de plus).
> Payer gagne entre 1 et 2 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, K9o a 54,5 % d'équité : marge de 9,5 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 1 et 2 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (9 BB de plus).
> Ton choix (fold) perd entre 1 et 2 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, K9o a 54,5 % d'équité : marge de 9,5 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 1 et 2 BB sur ce pot) : il fallait payer le tapis (9 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q042 · GTO · 3-handed · BB face à un tapis · 12 BB · AJo

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (12 BB).
Tu es au BB avec A♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.514 | erreur |
| Payer le tapis (9 BB de plus) | +2.514 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (9 BB de plus), +2,51 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 55 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (9 BB de plus) » : Q6s, K8o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (9 BB de plus), +2,51 BB par rapport au fold.
> Ton choix (fold) rapporte 2,51 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 12 BB, on paie avec 66+, A3s+, A4o+, K2s+, K8o+, Q6s+, Q9o+, J7s+ (environ 57 % des mains qui arrivent ici).
> Ici, on paie avec 55 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (9 BB de plus) » : Q6s, K8o.


## Q043 · GTO · heads-up · SB face à un tapis · 20 BB · T7o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 30 / BB 20 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 30 / 20 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB part à tapis (20 BB).
Tu es au SB avec T♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (16,5 BB de plus) | -2.108 | 0 % | 2.108 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 16,5 BB à payer pour un pot final de 40 BB, il faut 41,2 % d'équité pour payer.
> Contre sa range de tapis, T7o a 36,0 % d'équité : 5,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 2,11 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 41,2 %, à 2 points près), paient encore : J8s (41,3 %), K7s (41,6 %), A3s (41,7 %) ; se couchent déjà : A2s (40,9 %), 98s (40,8 %), A5o (40,3 %).
> Ici, on paie avec 41 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (16,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (16,5 BB de plus) » rapporte 2,11 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 20 BB (heads-up), on ne joue que 44+, A7s+, A8o+, KQs, KJo+ (environ 42 % des mains qui arrivent ici).
> Cote du pot : 16,5 BB à payer pour un pot final de 40 BB, il faut 41,2 % d'équité pour payer.
> Contre sa range de tapis, T7o a 36,0 % d'équité : 5,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 2,11 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 41,2 %, à 2 points près), paient encore : J8s (41,3 %), K7s (41,6 %), A3s (41,7 %) ; se couchent déjà : A2s (40,9 %), 98s (40,8 %), A5o (40,3 %).
> Ici, on paie avec 41 % des mains qui arrivent à cette décision.


## Q044 · exploitant · heads-up · SB premier à parler · 4 BB · K3o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 84,9 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : Heads-up, tapis 4 / 4 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 84,9 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu joues en tapis ou fold.
Tu es au SB avec K♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.583 | erreur |
| Tapis (4 BB) | +0.583 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (4 BB).
> Partir à tapis gagne entre 0,5 et 1 BB.
> Il se couche 15 % du temps face à ton tapis (équilibre push/fold : 26 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, K3o a 49,1 % d'équité contre sa range de call (équilibre push/fold : 47,3 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (4 BB).
> Ton choix (fold) perd entre 0,5 et 1 BB.
> Il se couche 15 % du temps face à ton tapis (équilibre push/fold : 26 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, K3o a 49,1 % d'équité contre sa range de call (équilibre push/fold : 47,3 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q045 · GTO · 3-handed · BB face à un tapis · 20 BB · AA

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu relances à 5,3 BB.
Le BTN part à tapis (20 BB).
Le SB se couche.
Tu es au BB avec A♠A♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 22.368 | erreur |
| Payer le tapis (14,7 BB de plus) | +22.368 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (14,7 BB de plus), +22,37 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 91 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 36 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (14,7 BB de plus) » : A4o, A4s, A2s, K8o, Q9s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (14,7 BB de plus), +22,37 BB par rapport au fold.
> Ton choix (fold) rapporte 22,37 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 20 BB, on paie avec 55+, A2s+, A5o+, K7s+, K8o+, Q6s+, QJo, J7s+, T9o, 97s+, 86s+ (environ 95 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 91 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 36 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (14,7 BB de plus) » : A4o, A4s, A2s, K8o, Q9s.


## Q046 · GTO · 3-handed · SB face à une relance · 10 BB · K9o

Type : décision nette · EV : HRC · tapis BTN 10 / SB 10 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,8 BB de plus) | -0.424 | 0 % | 0.424 | erreur |
| Tapis (10 BB) | -0.814 | 0 % | 0.814 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 79 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Autre option : payer (1,8 BB de plus), 0,42 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KTo, A8o, A5o, JTs, 22.

**Correction affichée si le joueur joue « Payer (1,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,8 BB de plus) » rapporte 0,42 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 10 BB, on ne joue que 66+, A2s+, A7o+, KTs+, KJo+, QTs+ (environ 20 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 79 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Autre option : tapis (10 BB), 0,81 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KTo, A8o, A5o, JTs, 22.


## Q047 · exploitant · 3-handed · SB premier à parler · 14 BB · Q9o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 14 / SB 14 / BB 14 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 45,5 % de ses mains (équilibre push/fold : 29,4 %)

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 45,5 % de ses mains dans cette situation (équilibre push/fold : 29,4 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.132 | erreur |
| Tapis (14 BB) | +0.132 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (14 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (14 BB).
> Partir à tapis gagne entre 0,06 et 0,5 BB.
> Il se couche 55 % du temps face à ton tapis (équilibre push/fold : 71 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q9o a 42,6 % d'équité contre sa range de call (équilibre push/fold : 36,4 %) et tout se joue à tapis (14 BB effectifs).
> Contre ce profil, on part à tapis avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 48 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (14 BB).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Il se couche 55 % du temps face à ton tapis (équilibre push/fold : 71 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q9o a 42,6 % d'équité contre sa range de call (équilibre push/fold : 36,4 %) et tout se joue à tapis (14 BB effectifs).
> Contre ce profil, on part à tapis avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 48 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q048 · GTO · 3-handed · BB face à un limp · 18 BB · K9o

Type : stratégie mixte · EV : HRC · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu es au BB avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.651 | 55 % | 0.000 | correct |
| Relancer à 4,5 BB | +0.596 | 45 % | 0.055 | correct |
| Tapis (18 BB) | +0.337 | 0 % | 0.314 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 85 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Autre option : tapis (18 BB), 0,31 BB de moins.
> K9o est jouée de plusieurs façons (check 55 %, relancer à 4,5 BB 45 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « check » : JTs, T5s, A2s, Q9s, A9s.

**Correction affichée si le joueur joue « Tapis (18 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (18 BB) » rapporte 0,31 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 18 BB, on checke avec environ 88 % des mains qui arrivent ici.
> Ici, on checke avec 85 % des mains qui arrivent à cette décision ; K9o en fait partie.
> K9o est jouée de plusieurs façons (check 55 %, relancer à 4,5 BB 45 %) : ces actions ont une valeur proche. Ton choix « tapis (18 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « check » : JTs, T5s, A2s, Q9s, A9s.


## Q049 · GTO · 3-handed · SB face à un tapis · 20 BB · QJs

Type : décision nette · EV : HRC · tapis BTN 10 / SB 20 / BB 45 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 10 / 20 / 45 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB part à tapis (45 BB, soit 20 BB effectifs).
Le BTN se couche.
Tu es au SB avec Q♠J♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (19 BB de plus) | -1.007 | 0 % | 1.007 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; QJs en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (19 BB de plus), 1,01 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 44, KQo, QTs, 97s, Q8s.

**Correction affichée si le joueur joue « Payer le tapis (19 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (19 BB de plus) » rapporte 1,01 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 20 BB, on ne joue que 22+, A2s+, KJs+ (environ 23 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; QJs en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : 44, KQo, QTs, 97s, Q8s.


## Q050 · exploitant · heads-up · SB premier à parler · 10 BB · QTo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 10 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 54,4 % de ses mains (équilibre push/fold : 37,3 %)

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 54,4 % de ses mains dans cette situation (équilibre push/fold : 37,3 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.818 | erreur |
| Tapis (10 BB) | +0.818 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (10 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (10 BB).
> Partir à tapis gagne entre 0,5 et 1 BB.
> Il se couche 47 % du temps face à ton tapis (équilibre push/fold : 63 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, QTo a 48,6 % d'équité contre sa range de call (équilibre push/fold : 42,1 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (10 BB).
> Ton choix (fold) perd entre 0,5 et 1 BB.
> Il se couche 47 % du temps face à ton tapis (équilibre push/fold : 63 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, QTo a 48,6 % d'équité contre sa range de call (équilibre push/fold : 42,1 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q051 · exploitant · 3-handed · BB face à un tapis · 12 BB · Q6o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 24,2 % de ses mains (équilibre push/fold : 31,3 %)

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN part à tapis (12 BB).
Le SB se couche.
Profil fictif « Prudent » : ce BTN part à tapis avec 24,2 % de ses mains dans cette situation (équilibre push/fold : 31,3 %).
Tu es au BB avec Q♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -2.637 | 0 % | 2.637 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range, Q6o a 34,1 % d'équité : 10,8 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : KJs (45,2 %), 33 (45,4 %), A8o (45,9 %) ; se couchent déjà : KQo (44,5 %), A6s (44,4 %), A5s (44,2 %).
> Contre ce profil, on paie avec 14 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 20 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (11 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range, Q6o a 34,1 % d'équité : 10,8 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : KJs (45,2 %), 33 (45,4 %), A8o (45,9 %) ; se couchent déjà : KQo (44,5 %), A6s (44,4 %), A5s (44,2 %).
> Contre ce profil, on paie avec 14 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 20 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q052 · GTO · 3-handed · SB premier à parler · 16 BB · TT

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.631 | erreur |
| Compléter (0,5 BB de plus) | +2.463 | 0 % | 0.168 | erreur |
| Relancer à 3,5 BB | +2.631 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3,5 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3,5 BB, +2,63 BB par rapport au fold.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 51 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 27 % des mains qui arrivent à cette décision ; TT en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « relancer à 3,5 BB » : 33, 53s, 98o, T8o, A2o.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Relancer à 3,5 BB, +2,63 BB par rapport au fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 51 % du temps, et sinon tu gardes l'initiative.
> À retenir : au SB premier à parler à 16 BB, on relance avec environ 25 % des mains qui arrivent ici.
> Ici, on relance avec 27 % des mains qui arrivent à cette décision ; TT en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3,5 BB » : 33, 53s, 98o, T8o, A2o.


## Q053 · GTO · heads-up · BB face à une relance · 12 BB · A4o

Type : décision nette · EV : HRC · tapis SB 12 / BB 12 · arbre 100650d1

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Le SB relance à 2 BB.
Tu es au BB avec A♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.400 | erreur |
| Payer (1 BB de plus) | +0.914 | 0 % | 0.486 | erreur |
| Tapis (12 BB) | +1.400 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (12 BB), +1,4 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 52 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 33 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Autre option : payer (1 BB de plus), 0,49 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : K9o, K5s, Q2s, K7s, 75s.

**Correction affichée si le joueur joue « Payer (1 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (12 BB), +1,4 BB par rapport au fold.
> Ton choix « payer (1 BB de plus) » rapporte 0,49 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 52 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à une relance à 12 BB (heads-up), on part à tapis avec 22+, A2+, K9s+, K8o+, J4s+, T9s, 54s (environ 32 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on part à tapis avec 33 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : K9o, K5s, Q2s, K7s, 75s.


## Q054 · GTO · 3-handed · SB face à un tapis · 20 BB · 95s

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB part à tapis (20 BB).
Le BTN se couche.
Tu es au SB avec 9♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (19 BB de plus) | -2.770 | 0 % | 2.770 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 81 % des mains qui arrivent à cette décision ; 95s en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (19 BB de plus), 2,77 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T3s, A2o, T9s, T6s, T5s.

**Correction affichée si le joueur joue « Payer le tapis (19 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (19 BB de plus) » rapporte 2,77 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 20 BB, on ne joue que 33+, AKs, A7o+, K8s+, QJs, T9s, 54s (environ 15 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 81 % des mains qui arrivent à cette décision ; 95s en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : T3s, A2o, T9s, T6s, T5s.


## Q055 · GTO · 3-handed · BB face à un tapis · 8 BB · Q5s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB).
Tu es au BB avec Q♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.087 | erreur |
| Payer le tapis (7 BB de plus) | +0.087 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7 BB de plus), +0,09 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, Q5s a 44,3 % d'équité : marge de 0,5 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,09 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : T9o (43,77 %), J7s (43,79 %), K3o (44,1 %) ; se couchent déjà : Q4s (43,5 %), K2o (43,4 %), T7s (43,1 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7 BB de plus), +0,09 BB par rapport au fold.
> Ton choix (fold) rapporte 0,09 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 8 BB, on paie avec 22+, A2+, K2s+, K3o+, Q5s+, Q8o+, J7s+, J9o+, T8s+, T9o, 98s (environ 43 % des mains qui arrivent ici).
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, Q5s a 44,3 % d'équité : marge de 0,5 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,09 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : T9o (43,77 %), J7s (43,79 %), K3o (44,1 %) ; se couchent déjà : Q4s (43,5 %), K2o (43,4 %), T7s (43,1 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.


## Q056 · GTO · 3-handed · SB face à un tapis · 12 BB · QJo

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Tu relances à 4,3 BB.
Le BB part à tapis (12 BB).
Le BTN se couche.
Tu es au SB avec Q♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.725 | erreur |
| Payer le tapis (7,7 BB de plus) | +1.725 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7,7 BB de plus), +1,72 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 99 % des mains qui arrivent à cette décision ; QJo en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : Q5s, K4s, QTs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7,7 BB de plus), +1,72 BB par rapport au fold.
> Ton choix (fold) rapporte 1,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 12 BB, on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 99 % des mains qui arrivent à cette décision ; QJo en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : Q5s, K4s, QTs.


## Q057 · GTO · 3-handed · BB face à un tapis · 25 BB · QQ

Type : décision nette · EV : HRC · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 25 / 25 / 25 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB paie 2,3 BB.
Tu relances à 9,9 BB.
Le BTN se couche.
Le SB part à tapis (25 BB).
Tu es au BB avec Q♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 19.023 | erreur |
| Payer le tapis (15,11 BB de plus) | +19.023 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15,11 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15,11 BB de plus), +19,02 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 98 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 29 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15,11 BB de plus) » : A9s, T9s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15,11 BB de plus), +19,02 BB par rapport au fold.
> Ton choix (fold) rapporte 19,02 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 25 BB, on paie avec 22+, A2s+, A7o+, K6s+, KTo+, Q8s+, QJo, JTs, T9s, 75s+, 65s (environ 99 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on paie avec 98 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 29 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15,11 BB de plus) » : A9s, T9s.


## Q058 · GTO · 3-handed · BB face à une relance · 8 BB · 32o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 4 / 8 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec 3♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,3 BB de plus) | -0.380 | 0 % | 0.381 | erreur |
| Tapis (8 BB) | -2.321 | 0 % | 2.321 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 56 % des mains qui arrivent à cette décision ; 32o en fait partie.
> Autre option : payer (1,3 BB de plus), 0,38 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 74s, J3s, J9o, 97s, J8o.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 0,38 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 8 BB, on se couche avec environ 58 % des mains qui arrivent ici.
> Ici, on se couche avec 56 % des mains qui arrivent à cette décision ; 32o en fait partie.
> Autre option : tapis (8 BB), 2,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 74s, J3s, J9o, 97s, J8o.


## Q059 · GTO · heads-up · SB face à un tapis · 10 BB · T7s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis SB 10 / BB 10 · arbre 100650d1

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Tu complètes.
Le BB part à tapis (10 BB).
Tu es au SB avec T♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.064 | erreur |
| Payer le tapis (9 BB de plus) | +0.064 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (9 BB de plus), +0,064 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, T7s a 45,3 % d'équité : marge de 0,3 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,064 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : K4s (45,04 %), T9o (45,1 %), Q9o (45,3 %) ; se couchent déjà : J7s (44,7 %), Q6s (44,7 %), K6o (44,6 %).
> Ici, on paie avec 29 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (9 BB de plus), +0,064 BB par rapport au fold.
> Ton choix (fold) rapporte 0,064 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 10 BB (heads-up), on paie avec 55+, A2s+, A5o+, K5s+, K7o+, Q7s+, Q9o+, J8s+, JTo, T7s+, T9o (environ 29 % des mains qui arrivent ici).
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, T7s a 45,3 % d'équité : marge de 0,3 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,064 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : K4s (45,04 %), T9o (45,1 %), Q9o (45,3 %) ; se couchent déjà : J7s (44,7 %), Q6s (44,7 %), K6o (44,6 %).
> Ici, on paie avec 29 % des mains qui arrivent à cette décision.


## Q060 · GTO · 3-handed · SB face à une relance · 8 BB · Q9o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,8 BB de plus) | -0.704 | 0 % | 0.704 | erreur |
| Tapis (8 BB) | -1.229 | 0 % | 1.229 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 77 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Autre option : payer (1,8 BB de plus), 0,7 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A4o, K6s, 98s, Q9s, JTs.

**Correction affichée si le joueur joue « Payer (1,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,8 BB de plus) » rapporte 0,7 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 8 BB, on ne joue que 55+, A2s+, A4o+, K8s+, KTo+, QTs+, QJo, JTs (environ 22 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 77 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Autre option : tapis (8 BB), 1,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A4o, K6s, 98s, Q9s, JTs.


## Q061 · GTO · 3-handed · BB face à un limp · 4 BB · KQo

Type : décision nette · EV : HRC · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec K♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.175 | 0 % | 0.360 | erreur |
| Tapis (4 BB) | +1.535 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (4 BB), +0,36 BB par rapport au check.
> À 4 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> Ici, on part à tapis avec 50 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 43s, 84o, T2o, 86s, T7s.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Tapis (4 BB), +0,36 BB par rapport au check.
> Ton choix (check) rapporte 0,36 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> À 4 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> À retenir : au BB face à un limp à 4 BB, on part à tapis avec environ 51 % des mains qui arrivent ici.
> Ici, on part à tapis avec 50 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 43s, 84o, T2o, 86s, T7s.


## Q062 · GTO · 3-handed · BB face à un tapis · 25 BB · AA

Type : décision nette · EV : HRC · tapis BTN 25 / SB 25 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 25 / 25 / 25 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,5 BB.
Tu paies 4,5 BB.
Le BTN part à tapis (25 BB).
Le SB se couche.
Tu es au BB avec A♠A♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 27.340 | erreur |
| Payer le tapis (20,5 BB de plus) | +27.340 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (20,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (20,5 BB de plus), +27,34 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 77 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (20,5 BB de plus) » : AQs, K3s, 64s, 54s, 96s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (20,5 BB de plus), +27,34 BB par rapport au fold.
> Ton choix (fold) rapporte 27,34 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 25 BB, on paie avec environ 87 % des mains qui arrivent ici.
> Ici, on paie avec 77 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (20,5 BB de plus) » : AQs, K3s, 64s, 54s, 96s.


## Q063 · GTO · heads-up · SB face à une relance · 8 BB · Q3o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec Q♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.058 | 0 % | 0.058 | imprécision |
| Tapis (8 BB) | -0.479 | 0 % | 0.479 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; Q3o en fait partie.
> Autre option : tapis (8 BB), 0,48 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 93s, T3s, 52s, 97o, Q4o.

**Correction affichée si le joueur joue « Tapis (8 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (8 BB) » rapporte 0,48 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 8 BB (heads-up), on se couche avec environ 52 % des mains qui arrivent ici.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; Q3o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : 93s, T3s, 52s, 97o, Q4o.


## Q064 · GTO · 3-handed · BTN face à un tapis · 20 BB · TT

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 45 / SB 20 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 45 / 20 / 10 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB relance à 7,6 BB.
Le BB part à tapis (10 BB).
Tu es au BTN avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 5.467 | erreur |
| Payer le tapis (7,7 BB de plus) | +5.393 | 0 % | 0.074 | imprécision |
| Tapis (20 BB) | +5.467 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (20 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (20 BB), +5,47 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> Ici, on part à tapis avec 34 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut environ 28 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : ATo, KQs, KJs, 55, 99.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (20 BB), +5,47 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 5,47 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> À retenir : au BTN face à un tapis à 20 BB, on part à tapis avec 66+, AJs+, ATo+, KQs (environ 33 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on part à tapis avec 34 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut environ 28 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : ATo, KQs, KJs, 55, 99.


## Q065 · GTO · 3-handed · BTN premier à parler · 10 BB · QJo

Type : stratégie mixte · EV : HRC · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec Q♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.166 | erreur |
| Limper (1 BB) | +0.146 | 30 % | 0.020 | correct |
| Relancer à 2,3 BB | +0.148 | 0 % | 0.018 | correct |
| Tapis (10 BB) | +0.166 | 70 % | 0.000 | correct |

**Référence de l'application** : Tapis (10 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (10 BB), limper (1 BB) ou relancer à 2,3 BB (moins de 0,02 BB d'écart).
> Ton tapis met la pression maximale : tout le monde se couche environ 61 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 26 % des mains qui arrivent à cette décision ; QJo en fait partie.
> QJo est jouée de plusieurs façons (limper (1 BB) 30 %, tapis (10 BB) 70 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (10 BB) » : T7s, K6s, TT, Q9s, A4s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (10 BB), limper (1 BB) ou relancer à 2,3 BB (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 61 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BTN premier à parler à 10 BB, on part à tapis avec 22+, A2+, K6s+, KTo+, QTo+, J8s+, JTo, T8s+, 98s, 87s (environ 27 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on part à tapis avec 26 % des mains qui arrivent à cette décision ; QJo en fait partie.
> QJo est jouée de plusieurs façons (limper (1 BB) 30 %, tapis (10 BB) 70 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (10 BB) » : T7s, K6s, TT, Q9s, A4s.


## Q066 · GTO · 3-handed · SB face à un limp · 18 BB · 54o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 14 / SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 14 / 18 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 5♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.074 | 0 % | 0.074 | imprécision |
| Relancer à 4,5 BB | -0.504 | 0 % | 0.504 | erreur |
| Tapis (18 BB) | -0.878 | 0 % | 0.878 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Autre option : relancer à 4,5 BB, 0,5 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9s, Q6s, 86s, 75o, 92s.

**Correction affichée si le joueur joue « Relancer à 4,5 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (relancer à 4,5 BB) rapporte 0,5 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 18 BB, on ne joue que 22+, A2+, K5s+, K8o+, Q7s+, QTo+, J8s+, T8s+, 95s+, 84s+, 76s (environ 36 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Autre option : tapis (18 BB), 0,88 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9s, Q6s, 86s, 75o, 92s.


## Q067 · GTO · heads-up · BB face à un tapis · 25 BB · 54o

Type : décision nette · EV : HRC · tapis SB 25 / BB 25 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 25 / 25 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (25 BB).
Tu es au BB avec 5♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (22 BB de plus) | -6.419 | 0 % | 6.420 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 57 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Repère : il faut 44 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (22 BB de plus), 6,42 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9s, Q9s, JTo, KTs, K5s.

**Correction affichée si le joueur joue « Payer le tapis (22 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (22 BB de plus) » rapporte 6,42 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 25 BB (heads-up), on ne joue que 33+, A7s+, A9o+, KJs+, KQo, Q8s+, J8s+, 86s+ (environ 39 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 57 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Repère : il faut 44 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : T9s, Q9s, JTo, KTs, K5s.


## Q068 · GTO · 3-handed · BB face à un limp · 20 BB · 96o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu es au BB avec 9♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.517 | 100 % | 0.000 | correct |
| Relancer à 4,3 BB | +0.264 | 0 % | 0.253 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 83 % des mains qui arrivent à cette décision ; 96o en fait partie.
> Autre option : relancer à 4,3 BB, 0,25 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : 55, A7o, A6o, T9o, A4o.

**Correction affichée si le joueur joue « Relancer à 4,3 BB » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix (relancer à 4,3 BB) rapporte 0,25 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 20 BB, on checke avec environ 84 % des mains qui arrivent ici.
> Ici, on checke avec 83 % des mains qui arrivent à cette décision ; 96o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : 55, A7o, A6o, T9o, A4o.


## Q069 · GTO · 3-handed · SB face à un limp · 12 BB · 92o

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 9♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.386 | 0 % | 0.386 | erreur |
| Relancer à 4,5 BB | -0.494 | 0 % | 0.494 | erreur |
| Tapis (12 BB) | -1.160 | 0 % | 1.160 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 61 % des mains qui arrivent à cette décision ; 92o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,39 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 94s, 85s, T8s, Q7s, 63s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 12 BB, on ne joue que 22+, A2+, K2s+, K8o+, Q3s+, QTo+, J7s+, JTo, T7s+, 98s, 87s, 43s (environ 39 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on se couche avec 61 % des mains qui arrivent à cette décision ; 92o en fait partie.
> Autre option : relancer à 4,5 BB, 0,49 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 94s, 85s, T8s, Q7s, 63s.


## Q070 · exploitant · heads-up · BB face à un tapis · 4 BB · 86o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 66,3 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : Heads-up, tapis 4 / 8 BB (SB / BB).
Le SB part à tapis (4 BB).
Profil fictif « Prudent » : ce SB part à tapis avec 66,3 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu es au BB avec 8♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3 BB de plus) | -0.063 | 0 % | 0.063 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 86o a 36,7 % d'équité : 0,8 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> À l'équilibre push/fold, ce serait payer le tapis (3 BB de plus).
> Sa range de tapis est un peu plus forte : resserrer légèrement les calls limites.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (3 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (3 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 86o a 36,7 % d'équité : 0,8 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> À l'équilibre push/fold, ce serait payer le tapis (3 BB de plus).
> Sa range de tapis est un peu plus forte : resserrer légèrement les calls limites.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q071 · GTO · heads-up · SB face à un tapis · 6 BB · K4s

Type : décision nette · EV : HRC · tapis SB 6 / BB 6 · arbre 100650d1

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Tu relances à 2 BB.
Le BB part à tapis (6 BB).
Tu es au SB avec K♠4♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.395 | erreur |
| Payer le tapis (4 BB de plus) | +1.395 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (4 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (4 BB de plus), +1,39 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; K4s en fait partie.
> Repère : il faut 33 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (4 BB de plus), +1,39 BB par rapport au fold.
> Ton choix (fold) rapporte 1,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 6 BB (heads-up), on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; K4s en fait partie.
> Repère : il faut 33 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q072 · exploitant · heads-up · BB face à un tapis · 4 BB · Q2o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 84,9 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : Heads-up, tapis 4 / 4 BB (SB / BB).
Le SB part à tapis (4 BB).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 84,9 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu es au BB avec Q♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.561 | erreur |
| Payer le tapis (3 BB de plus) | +0.561 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Payer gagne entre 0,5 et 1 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, Q2o a 44,5 % d'équité : marge de 7,0 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 0,5 et 1 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 43s (37,6 %), 65o (37,7 %), 82s (37,7 %) ; se couchent déjà : 94o (37,0 %), 52s (36,6 %), 93o (36,5 %).
> Contre ce profil, on paie avec 82 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 0,5 et 1 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, Q2o a 44,5 % d'équité : marge de 7,0 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 0,5 et 1 BB sur ce pot) : il fallait payer le tapis (3 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 43s (37,6 %), 65o (37,7 %), 82s (37,7 %) ; se couchent déjà : 94o (37,0 %), 52s (36,6 %), 93o (36,5 %).
> Contre ce profil, on paie avec 82 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q073 · GTO · 3-handed · BTN face à une relance · 25 BB · J8s

Type : décision nette · EV : HRC · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 25 / 25 / 25 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB relance à 7,6 BB.
Le BB se couche.
Tu es au BTN avec J♠8♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (5,29 BB de plus) | -0.586 | 0 % | 0.586 | erreur |
| Tapis (25 BB) | -3.274 | 0 % | 3.274 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J8s en fait partie.
> Autre option : payer (5,29 BB de plus), 0,59 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 98s, A9s, A4s, 76s, Q6s.

**Correction affichée si le joueur joue « Payer (5,29 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (5,29 BB de plus) » rapporte 0,59 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 25 BB, on ne joue que 55+, A2s+, ATo+, K9s+, KQo, JTs, 97s+, 76s, 54s (environ 36 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J8s en fait partie.
> Autre option : tapis (25 BB), 3,27 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 98s, A9s, A4s, 76s, Q6s.


## Q074 · GTO · 3-handed · BB face à une relance · 12 BB · AQo

Type : décision nette · EV : HRC · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 12 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec A♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.048 | erreur |
| Payer (1,3 BB de plus) | +1.655 | 0 % | 0.393 | erreur |
| Tapis (12 BB) | +2.048 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (12 BB), +2,05 BB par rapport au fold.
> À 12 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> Ici, on part à tapis avec 19 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Autre option : payer (1,3 BB de plus), 0,39 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : Q5s, A6s, K9s, A4s, A4o.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (12 BB), +2,05 BB par rapport au fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 0,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> À 12 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> À retenir : au BB face à une relance à 12 BB, on part à tapis avec 22+, A4s+, A7o+, KQs, KJo+ (environ 17 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 19 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : Q5s, A6s, K9s, A4s, A4o.


## Q075 · GTO · 3-handed · BB face à un tapis · 25 BB · ATs

Type : stratégie mixte · EV : HRC · tapis BTN 15 / SB 25 / BB 35 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 25 / 35 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,5 BB.
Tu paies 4,5 BB.
Le BTN part à tapis (15 BB).
Le SB paie le tapis.
Tu es au BB avec A♠T♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 9.646 | erreur |
| Payer le tapis (10,5 BB de plus) | +9.625 | 10 % | 0.020 | correct |
| Tapis (25 BB) | +9.646 | 90 % | 0.000 | correct |

**Référence de l'application** : Tapis (25 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (25 BB), +9,65 BB par rapport au fold.
> Ton tapis met la pression maximale : tout le monde se couche environ 2 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 70 % des mains qui arrivent à cette décision ; ATs en fait partie.
> Repère : il faut 23 % d'équité pour payer (cote du pot).
> ATs est jouée de plusieurs façons (payer le tapis (10,5 BB de plus) 10 %, tapis (25 BB) 90 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : A9s, K9s, KQs, K4s, 64s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (25 BB), +9,65 BB par rapport au fold.
> Ton choix (fold) rapporte 9,65 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 2 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à un tapis à 25 BB, on part à tapis avec environ 74 % des mains qui arrivent ici.
> Ici, on part à tapis avec 70 % des mains qui arrivent à cette décision ; ATs en fait partie.
> Repère : il faut 23 % d'équité pour payer (cote du pot).
> ATs est jouée de plusieurs façons (payer le tapis (10,5 BB de plus) 10 %, tapis (25 BB) 90 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : A9s, K9s, KQs, K4s, 64s.


## Q076 · GTO · 3-handed · BTN face à un tapis · 20 BB · Q9o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 40 / 15 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB part à tapis (40 BB, soit 20 BB effectifs).
Le BB se couche.
Tu es au BTN avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17,7 BB de plus) | -2.324 | 0 % | 2.324 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 57 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Repère : il faut 43 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (17,7 BB de plus), 2,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KJs, A7s, QTs, JTs, 44.

**Correction affichée si le joueur joue « Payer le tapis (17,7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17,7 BB de plus) » rapporte 2,32 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BTN face à un tapis à 20 BB, on ne joue que 44+, A7s+, ATo+, KTs+, KQo (environ 41 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 57 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Repère : il faut 43 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : KJs, A7s, QTs, JTs, 44.


## Q077 · GTO · 3-handed · SB premier à parler · 25 BB · 86s

Type : stratégie mixte · EV : HRC · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 25 / 25 / 25 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec 8♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.389 | erreur |
| Compléter (0,5 BB de plus) | +0.389 | 75 % | 0.000 | correct |
| Relancer à 3,3 BB | +0.332 | 25 % | 0.057 | correct |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +0,39 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 42 % des mains qui arrivent à cette décision ; 86s en fait partie.
> 86s est jouée de plusieurs façons (compléter (0,5 BB de plus) 75 %, relancer à 3,3 BB 25 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 74s, 62s, 83s, 95s, QTs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +0,39 BB par rapport au fold.
> Ton choix (fold) rapporte 0,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 25 BB, on complète avec environ 44 % des mains qui arrivent ici.
> Ici, on complète avec 42 % des mains qui arrivent à cette décision ; 86s en fait partie.
> 86s est jouée de plusieurs façons (compléter (0,5 BB de plus) 75 %, relancer à 3,3 BB 25 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 74s, 62s, 83s, 95s, QTs.


## Q078 · GTO · 3-handed · SB face à un limp · 4 BB · J9o

Type : stratégie mixte · EV : HRC · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 4 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec J♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 55 % | 0.006 | correct |
| Compléter (0,5 BB de plus) | -0.175 | 0 % | 0.181 | erreur |
| Tapis (4 BB) | +0.006 | 45 % | 0.000 | correct |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou tapis (4 BB) (moins de 0,02 BB d'écart).
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 56 % des mains qui arrivent à cette décision ; J9o le fait 55 % du temps.
> Autre option : compléter (0,5 BB de plus), 0,18 BB de moins.
> J9o est jouée de plusieurs façons (fold 55 %, tapis (4 BB) 45 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « fold » : K5s, Q7s, K2o, Q2o, J4s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou tapis (4 BB) (moins de 0,02 BB d'écart).
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 4 BB, on ne joue que 22+, A2+, K2s+, K5o+, Q2s+, Q8o+, J8s+, J9o+, T5s+, T9o, 97s+, 65s (environ 43 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 56 % des mains qui arrivent à cette décision ; J9o le fait 55 % du temps.
> J9o est jouée de plusieurs façons (fold 55 %, tapis (4 BB) 45 %) : ces actions ont une valeur proche. Ton choix « compléter (0,5 BB de plus) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « fold » : K5s, Q7s, K2o, Q2o, J4s.


## Q079 · GTO · 3-handed · SB face à un tapis · 6 BB · A4o

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (6 BB).
Le BTN se couche.
Tu es au SB avec A♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.243 | erreur |
| Payer le tapis (3,7 BB de plus) | +3.243 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3,7 BB de plus), +3,24 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 84 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (3,7 BB de plus) » : Q6s, A2s, Q7s, J9s, JTs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3,7 BB de plus), +3,24 BB par rapport au fold.
> Ton choix (fold) rapporte 3,24 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 6 BB, on paie avec 55+, A2+, K4s+, Q7s+, QJo, J7s+, JTo, T9o, 76s (environ 97 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on paie avec 84 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (3,7 BB de plus) » : Q6s, A2s, Q7s, J9s, JTs.


## Q080 · GTO · 3-handed · SB face à un tapis · 15 BB · 66

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (10 BB).
Le BTN paie le tapis.
Tu es au SB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.716 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.632 | 0 % | 0.084 | imprécision |
| Tapis (15 BB) | +3.715 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 3,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à un tapis à 15 BB, on part à tapis avec 55+, A9s+, KTs+, KJo+ (environ 34 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.


## Q081 · exploitant · heads-up · BB face à un tapis · 8 BB · Q5o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 8 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 76,5 % de ses mains (équilibre push/fold : 61,9 %)

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB part à tapis (8 BB).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 76,5 % de ses mains dans cette situation (équilibre push/fold : 61,9 %).
Tu es au BB avec Q♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.257 | erreur |
| Payer le tapis (7 BB de plus) | +0.257 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (7 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, Q5o a 45,4 % d'équité : marge de 1,6 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : 98o (43,9 %), Q4o (44,2 %), J4s (44,2 %) ; se couchent déjà : J3s (43,5 %), Q3o (43,4 %), 96s (43,3 %).
> Contre ce profil, on paie avec 54 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (7 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, Q5o a 45,4 % d'équité : marge de 1,6 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : 98o (43,9 %), Q4o (44,2 %), J4s (44,2 %) ; se couchent déjà : J3s (43,5 %), Q3o (43,4 %), 96s (43,3 %).
> Contre ce profil, on paie avec 54 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q082 · GTO · 3-handed · BB face à un tapis · 8 BB · T3o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB part à tapis (8 BB).
Tu es au BB avec T♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -2.878 | 0 % | 2.878 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 82 % des mains qui arrivent à cette décision ; T3o en fait partie.
> Repère : il faut environ 38 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (7 BB de plus), 2,88 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KQo, K4s, QTs, Q8s, 66.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 2,88 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 8 BB, on ne joue que 44+, A3s+, AJo+, K8s+, KJo+, QTs+, T9s (environ 17 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 82 % des mains qui arrivent à cette décision ; T3o en fait partie.
> Repère : il faut environ 38 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : KQo, K4s, QTs, Q8s, 66.


## Q083 · GTO · 3-handed · BB face à un tapis · 15 BB · AKo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 15 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 15 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (15 BB).
Tu es au BB avec A♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 6.066 | erreur |
| Payer le tapis (14 BB de plus) | +6.065 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (14 BB de plus), +6,07 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, AKo a 66,9 % d'équité : marge de 20,2 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 6,07 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : K8s (46,9 %), A4o (47,1 %), J9s (47,3 %) ; se couchent déjà : QJo (46,6 %), Q8s (46,1 %), K7s (46,0 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (14 BB de plus), +6,07 BB par rapport au fold.
> Ton choix (fold) rapporte 6,07 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 15 BB, on paie avec 22+, A2s+, A4o+, K8s+, KTo+, Q9s+, J9s+, T9s (environ 25 % des mains qui arrivent ici).
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, AKo a 66,9 % d'équité : marge de 20,2 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 6,07 BB sur ce pot) : erreur nette, il fallait payer le tapis (14 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : K8s (46,9 %), A4o (47,1 %), J9s (47,3 %) ; se couchent déjà : QJo (46,6 %), Q8s (46,1 %), K7s (46,0 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.


## Q084 · exploitant · 3-handed · BB face à un tapis · 8 BB · Q3s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 76,5 % de ses mains (équilibre push/fold : 61,9 %)

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 76,5 % de ses mains dans cette situation (équilibre push/fold : 61,9 %).
Tu es au BB avec Q♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.437 | erreur |
| Payer le tapis (7 BB de plus) | +0.437 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (7 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, Q3s a 46,5 % d'équité : marge de 2,7 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : 98o (43,9 %), Q4o (44,2 %), J4s (44,2 %) ; se couchent déjà : J3s (43,5 %), Q3o (43,4 %), 96s (43,3 %).
> Contre ce profil, on paie avec 54 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (7 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, Q3s a 46,5 % d'équité : marge de 2,7 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : 98o (43,9 %), Q4o (44,2 %), J4s (44,2 %) ; se couchent déjà : J3s (43,5 %), Q3o (43,4 %), 96s (43,3 %).
> Contre ce profil, on paie avec 54 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q085 · GTO · 3-handed · BTN premier à parler · 6 BB · J2o

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec J♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.184 | 0 % | 0.184 | erreur |
| Relancer à 2,3 BB | -0.542 | 0 % | 0.542 | erreur |
| Tapis (6 BB) | -0.549 | 0 % | 0.549 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Autre option : limper (1 BB), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9o, Q6s, 76s, J7s, T7s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 6 BB, on ne joue que 22+, A2+, K2s+, K7o+, Q7s+, Q9o+, J7s+, JTo, T7s+, 97s+, 87s (environ 38 % des mains qui arrivent ici).
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Autre option : relancer à 2,3 BB, 0,54 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9o, Q6s, 76s, J7s, T7s.


## Q086 · GTO · heads-up · SB face à un tapis · 6 BB · J3o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 6 / BB 6 · arbre 100650d1

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Tu complètes.
Le BB part à tapis (6 BB).
Tu es au SB avec J♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (5 BB de plus) | -0.378 | 0 % | 0.378 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 5 BB à payer pour un pot final de 12 BB, il faut 41,7 % d'équité pour payer.
> Contre sa range de tapis, J3o a 38,5 % d'équité : 3,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,38 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 41,7 %, à 2 points près), paient encore : 75s (41,69 %), J3s (41,9 %), Q4o (42,2 %) ; se couchent déjà : 85s (41,4 %), Q3o (41,4 %), 87o (41,3 %).
> Ici, on paie avec 38 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (5 BB de plus) » rapporte 0,38 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 6 BB (heads-up), on ne joue que 66+, Q2s+, J8s+, T6s+, T8o+, 96s+, 87s (environ 38 % des mains qui arrivent ici).
> Cote du pot : 5 BB à payer pour un pot final de 12 BB, il faut 41,7 % d'équité pour payer.
> Contre sa range de tapis, J3o a 38,5 % d'équité : 3,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,38 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 41,7 %, à 2 points près), paient encore : 75s (41,69 %), J3s (41,9 %), Q4o (42,2 %) ; se couchent déjà : 85s (41,4 %), Q3o (41,4 %), 87o (41,3 %).
> Ici, on paie avec 38 % des mains qui arrivent à cette décision.


## Q087 · GTO · 3-handed · BB face à un tapis · 6 BB · 53o

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN part à tapis (6 BB).
Le SB paie le tapis.
Tu es au BB avec 5♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (5 BB de plus) | -0.753 | 0 % | 0.753 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 53o en fait partie.
> Repère : il faut 28 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (5 BB de plus), 0,75 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 86s, Q4s, K9o, A6o, 64s.

**Correction affichée si le joueur joue « Payer le tapis (5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (5 BB de plus) » rapporte 0,75 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 6 BB, on se couche avec environ 68 % des mains qui arrivent ici.
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 53o en fait partie.
> Repère : il faut 28 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : 86s, Q4s, K9o, A6o, 64s.


## Q088 · GTO · 3-handed · SB face à un tapis · 20 BB · KQo

Type : stratégie mixte · EV : HRC · tapis BTN 10 / SB 20 / BB 45 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 10 / 20 / 45 BB (BTN / SB / BB).
Le BTN part à tapis (10 BB).
Tu es au SB avec K♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.631 | erreur |
| Payer le tapis (9,5 BB de plus) | +0.616 | 50 % | 0.015 | correct |
| Tapis (20 BB) | +0.631 | 50 % | 0.000 | correct |

**Référence de l'application** : Tapis (20 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (20 BB) ou payer le tapis (9,5 BB de plus) (moins de 0,02 BB d'écart).
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> KQo est jouée de plusieurs façons (payer le tapis (9,5 BB de plus) 50 %, tapis (20 BB) 50 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : 77, AQo, AKs, KJs, AA.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (20 BB) ou payer le tapis (9,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,63 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> À retenir : au SB face à un tapis à 20 BB, on part à tapis avec 55+, A5s+, A8o+, KJ+ (environ 13 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> KQo est jouée de plusieurs façons (payer le tapis (9,5 BB de plus) 50 %, tapis (20 BB) 50 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : 77, AQo, AKs, KJs, AA.


## Q089 · exploitant · 3-handed · BB face à un tapis · 12 BB · TT

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 18 / BB 12 · arbre daa9aaa0

Profil adverse (fictif) : Serré (Nit) : part à tapis avec 36,3 % de ses mains (équilibre push/fold : 53,3 %)

**Énoncé** : 3 joueurs, tapis 12 / 18 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (18 BB, soit 12 BB effectifs).
Profil fictif « Serré (Nit) » : ce SB part à tapis avec 36,3 % de ses mains dans cette situation (équilibre push/fold : 53,3 %).
Tu es au BB avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 4.792 | erreur |
| Payer le tapis (11 BB de plus) | +4.792 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (11 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (11 BB de plus).
> Payer gagne entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range, TT a 65,8 % d'équité : marge de 20,0 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : 22 (45,9 %), A4o (46,0 %), K9s (46,8 %) ; se couchent déjà : QTs (45,4 %), A3o (45,3 %), A2o (44,7 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 33 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (11 BB de plus).
> Ton choix (fold) perd entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range, TT a 65,8 % d'équité : marge de 20,0 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait payer le tapis (11 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : 22 (45,9 %), A4o (46,0 %), K9s (46,8 %) ; se couchent déjà : QTs (45,4 %), A3o (45,3 %), A2o (44,7 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 33 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q090 · GTO · 3-handed · BTN premier à parler · 20 BB · A9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.262 | erreur |
| Limper (1 BB) | +0.236 | 0 % | 0.025 | imprécision |
| Relancer à 2,3 BB | +0.262 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 2,3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 2,3 BB, +0,26 BB par rapport au fold.
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 28 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 23 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 2,3 BB » : QTo, K9o, 98s, AA, Q8s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Relancer à 2,3 BB, +0,26 BB par rapport au fold.
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,26 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 28 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BTN premier à parler à 20 BB, on relance avec 44+, A2s+, A5o+, K7s+, KJo+, Q8s+, QJo, JT, T9s, 98s (environ 22 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on relance avec 23 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 2,3 BB » : QTo, K9o, 98s, AA, Q8s.


## Q091 · GTO · 3-handed · BB face à un limp · 10 BB · 96s

Type : décision nette · EV : HRC · tapis BTN 50 / SB 15 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 50 / 15 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec 9♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.828 | 100 % | 0.000 | correct |
| Relancer à 3 BB | +0.651 | 0 % | 0.177 | erreur |
| Tapis (10 BB) | +0.664 | 0 % | 0.164 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; 96s en fait partie.
> Autre option : tapis (10 BB), 0,16 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : 93o, A7s, K5s, T5o, K7o.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (10 BB) » rapporte 0,16 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 10 BB, on checke avec environ 65 % des mains qui arrivent ici.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; 96s en fait partie.
> Autre option : relancer à 3 BB, 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : 93o, A7s, K5s, T5o, K7o.


## Q092 · GTO · 3-handed · BTN face à une relance · 20 BB · J7s

Type : décision nette · EV : HRC · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB relance à 7,6 BB.
Le BB se couche.
Tu es au BTN avec J♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (5,29 BB de plus) | -1.959 | 0 % | 1.959 | erreur |
| Tapis (20 BB) | -5.315 | 0 % | 5.315 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 49 % des mains qui arrivent à cette décision ; J7s en fait partie.
> Autre option : payer (5,29 BB de plus), 1,96 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K9s, 44, A4s, A8s, JTs.

**Correction affichée si le joueur joue « Payer (5,29 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (5,29 BB de plus) » rapporte 1,96 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 20 BB, on ne joue que 33+, A2s+, ATo+, K7s+, KQo, QTs+, JTs (environ 53 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 49 % des mains qui arrivent à cette décision ; J7s en fait partie.
> Autre option : tapis (20 BB), 5,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K9s, 44, A4s, A8s, JTs.


## Q093 · GTO · heads-up · SB face à un tapis · 12 BB · ATo

Type : décision nette · EV : HRC · tapis SB 12 / BB 12 · arbre 100650d1

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Tu relances à 2 BB.
Le BB part à tapis (12 BB).
Tu es au SB avec A♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.542 | erreur |
| Payer le tapis (10 BB de plus) | +3.542 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (10 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (10 BB de plus), +3,54 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 48 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (10 BB de plus) » : 97s, Q7s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (10 BB de plus), +3,54 BB par rapport au fold.
> Ton choix (fold) rapporte 3,54 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 12 BB (heads-up), on paie avec 77+, A5s+, A7o+, K6s+, KJo+, Q9s+, QTo+, J8s+, JTo, T8s+ (environ 49 % des mains qui arrivent ici).
> Ici, on paie avec 48 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (10 BB de plus) » : 97s, Q7s.


## Q094 · GTO · 3-handed · SB face à une relance · 10 BB · 65o

Type : décision nette · EV : HRC · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec 6♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.160 | 0 % | 0.160 | erreur |
| Tapis (10 BB) | -0.346 | 0 % | 0.346 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 44 % des mains qui arrivent à cette décision ; 65o en fait partie.
> Autre option : payer (2 BB de plus), 0,16 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J2s, 64s, 74s, 76s, T5s.

**Correction affichée si le joueur joue « Payer (2 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (2 BB de plus) » rapporte 0,16 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 10 BB, on se couche avec environ 50 % des mains qui arrivent ici.
> Ici, on se couche avec 44 % des mains qui arrivent à cette décision ; 65o en fait partie.
> Autre option : tapis (10 BB), 0,35 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J2s, 64s, 74s, 76s, T5s.


## Q095 · GTO · heads-up · SB premier à parler · 15 BB · 22

Type : décision nette · EV : HRC · tapis SB 35 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 35 / 15 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec 2♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.726 | erreur |
| Compléter (0,5 BB de plus) | +0.464 | 0 % | 0.263 | erreur |
| Relancer à 3,5 BB | +0.552 | 0 % | 0.175 | erreur |
| Tapis (15 BB) | +0.726 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +0,73 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 74 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 9 % des mains qui arrivent à cette décision ; 22 en fait partie.
> Autre option : relancer à 3,5 BB, 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : 76s, A3s, Q9s, A2o, T8s.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +0,73 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 74 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 15 BB (heads-up), on part à tapis avec A2o+, 87s, 76s (environ 8 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on part à tapis avec 9 % des mains qui arrivent à cette décision ; 22 en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,26 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : 76s, A3s, Q9s, A2o, T8s.


## Q096 · GTO · 3-handed · BB face à une relance · 14 BB · A8o

Type : stratégie mixte · EV : HRC · tapis BTN 14 / SB 14 / BB 14 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec A♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.540 | erreur |
| Payer (1,3 BB de plus) | +0.540 | 15 % | 0.000 | correct |
| Tapis (14 BB) | +0.533 | 85 % | 0.007 | correct |

**Référence de l'application** : Tapis (14 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (14 BB) ou payer (1,3 BB de plus) (moins de 0,02 BB d'écart).
> À 14 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> Ici, on part à tapis avec 18 % des mains qui arrivent à cette décision ; A8o en fait partie.
> A8o est jouée de plusieurs façons (payer (1,3 BB de plus) 15 %, tapis (14 BB) 85 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (14 BB) » : A3s, K8s, A3o, KQo, AA.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (14 BB) ou payer (1,3 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,54 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> À 14 BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.
> À retenir : au BB face à une relance à 14 BB, on part à tapis avec 22+, A8+, KQs, J8s+ (environ 18 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on part à tapis avec 18 % des mains qui arrivent à cette décision ; A8o en fait partie.
> A8o est jouée de plusieurs façons (payer (1,3 BB de plus) 15 %, tapis (14 BB) 85 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (14 BB) » : A3s, K8s, A3o, KQo, AA.


## Q097 · exploitant · 3-handed · SB premier à parler · 12 BB · T9o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 18 / BB 12 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 49,7 % de ses mains (équilibre push/fold : 33,1 %)

**Énoncé** : 3 joueurs, tapis 18 / 18 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 49,7 % de ses mains dans cette situation (équilibre push/fold : 33,1 %).
Tu joues en tapis ou fold.
Tu es au SB avec T♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (12 BB) | -0.194 | 0 % | 0.194 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,06 et 0,5 BB.
> Il se couche 50 % du temps face à ton tapis (équilibre push/fold : 67 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, T9o a 40,0 % d'équité contre sa range de call (équilibre push/fold : 37,5 %) et tout se joue à tapis (12 BB effectifs).
> Contre ce profil, tu perds trop de folds : ton tapis vivait de ses abandons, et ta main est trop faible quand il paie.
> Contre ce profil, on part à tapis avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 53 %.
> À l'équilibre push/fold, ce serait tapis (12 BB).
> Il se couche moins souvent : tes tapis « de vol », qui vivaient de ses folds, rapportent moins ou perdent ; tes mains fortes gagnent plus, car il paie avec pire. Pousse moins de mains faibles, garde tes mains de valeur.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (12 BB) » perd entre 0,06 et 0,5 BB.
> Il se couche 50 % du temps face à ton tapis (équilibre push/fold : 67 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, T9o a 40,0 % d'équité contre sa range de call (équilibre push/fold : 37,5 %) et tout se joue à tapis (12 BB effectifs).
> Contre ce profil, tu perds trop de folds : ton tapis vivait de ses abandons, et ta main est trop faible quand il paie.
> Contre ce profil, on part à tapis avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 53 %.
> À l'équilibre push/fold, ce serait tapis (12 BB).
> Il se couche moins souvent : tes tapis « de vol », qui vivaient de ses folds, rapportent moins ou perdent ; tes mains fortes gagnent plus, car il paie avec pire. Pousse moins de mains faibles, garde tes mains de valeur.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q098 · GTO · heads-up · SB face à un tapis · 20 BB · 73s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 20 / BB 30 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 20 / 30 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB part à tapis (30 BB, soit 20 BB effectifs).
Tu es au SB avec 7♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (16,5 BB de plus) | -3.286 | 0 % | 3.286 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 16,5 BB à payer pour un pot final de 40 BB, il faut 41,2 % d'équité pour payer.
> Contre sa range de tapis, 73s a 33,0 % d'équité : 8,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 3,29 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 41,2 %, à 2 points près), paient encore : A4s (41,3 %), K7s (41,3 %), 22 (41,5 %) ; se couchent déjà : K8s (41,16 %), JTo (41,1 %), Q8s (40,8 %).
> Ici, on paie avec 42 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (16,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (16,5 BB de plus) » rapporte 3,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 20 BB (heads-up), on ne joue que 44+, A7s+, A8o+, K9s+, KQo, QJs (environ 42 % des mains qui arrivent ici).
> Cote du pot : 16,5 BB à payer pour un pot final de 40 BB, il faut 41,2 % d'équité pour payer.
> Contre sa range de tapis, 73s a 33,0 % d'équité : 8,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 3,29 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 41,2 %, à 2 points près), paient encore : A4s (41,3 %), K7s (41,3 %), 22 (41,5 %) ; se couchent déjà : K8s (41,16 %), JTo (41,1 %), Q8s (40,8 %).
> Ici, on paie avec 42 % des mains qui arrivent à cette décision.


## Q099 · GTO · 3-handed · SB face à un limp · 8 BB · 43o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 4 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 4♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.703 | 0 % | 0.703 | erreur |
| Tapis (8 BB) | -0.951 | 0 % | 0.951 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,7 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J8s, K8o, K6s, 63s, Q3s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,7 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 8 BB, on ne joue que 66+, A2+, K8s+, K9o+, QTs+, JTs, 54s (environ 28 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Autre option : tapis (8 BB), 0,95 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J8s, K8o, K6s, 63s, Q3s.


## Q100 · GTO · 3-handed · SB face à un tapis · 12 BB · KK

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Tu relances à 2,5 BB.
Le BB part à tapis (12 BB).
Tu es au SB avec K♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 8.654 | erreur |
| Payer le tapis (9,5 BB de plus) | +8.654 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (9,5 BB de plus), +8,65 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 52 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut 40 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (9,5 BB de plus) » : Q6s, 65s, Q7s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (9,5 BB de plus), +8,65 BB par rapport au fold.
> Ton choix (fold) rapporte 8,65 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 12 BB, on paie avec 66+, A5s+, AKo, K7s+, KTo+, Q8s+, QJo, J7s+, JTo, T8s+, T9o (environ 53 % des mains qui arrivent ici).
> Ici, on paie avec 52 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut 40 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (9,5 BB de plus) » : Q6s, 65s, Q7s.


## Q101 · GTO · heads-up · SB face à un tapis · 15 BB · J7o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 35 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 35 / 15 BB (SB / BB).
Tu complètes.
Le BB part à tapis (15 BB).
Tu es au SB avec J♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -1.633 | 0 % | 1.633 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, J7o a 41,2 % d'équité : 5,5 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,63 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : T8s (46,9 %), K8s (47,0 %), 98s (47,0 %) ; se couchent déjà : K7s (46,6 %), A2s (46,6 %), QJo (46,4 %).
> Ici, on paie avec 20 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (14 BB de plus) » rapporte 1,63 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 15 BB (heads-up), on ne joue que 44+, A3s+, A7o+, K8s+, KTo+, Q9s+, J9s+, T8s+, 98s (environ 20 % des mains qui arrivent ici).
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, J7o a 41,2 % d'équité : 5,5 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,63 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : T8s (46,9 %), K8s (47,0 %), 98s (47,0 %) ; se couchent déjà : K7s (46,6 %), A2s (46,6 %), QJo (46,4 %).
> Ici, on paie avec 20 % des mains qui arrivent à cette décision.


## Q102 · GTO · 3-handed · SB face à un limp · 8 BB · T2o

Type : décision nette · EV : HRC · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec T♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.210 | 0 % | 0.210 | erreur |
| Tapis (8 BB) | -1.183 | 0 % | 1.183 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,21 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 96s, K4s, T5s, J9o, J7s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,21 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 8 BB, on ne joue que 44+, A2+, K5s+, K7o+, Q7s+, Q9o+, JTs, J8o+, 98s (environ 37 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Autre option : tapis (8 BB), 1,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 96s, K4s, T5s, J9o, J7s.


## Q103 · exploitant · 3-handed · BB face à un tapis · 4 BB · A8o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Serré (Nit) : part à tapis avec 28,4 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 4 / 8 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Le SB se couche.
Profil fictif « Serré (Nit) » : ce BTN part à tapis avec 28,4 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec A♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.150 | erreur |
| Payer le tapis (3 BB de plus) | +1.150 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (3 BB de plus).
> Payer gagne entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, A8o a 48,8 % d'équité : marge de 13,5 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 97o (35,35 %), T5s (35,4 %), 76o (35,5 %) ; se couchent déjà : J8o (35,26 %), Q3s (35,2 %), J4s (35,2 %).
> Contre ce profil, on paie avec 49 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, A8o a 48,8 % d'équité : marge de 13,5 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : erreur nette, il fallait payer le tapis (3 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 97o (35,35 %), T5s (35,4 %), 76o (35,5 %) ; se couchent déjà : J8o (35,26 %), Q3s (35,2 %), J4s (35,2 %).
> Contre ce profil, on paie avec 49 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q104 · GTO · heads-up · SB face à une relance · 20 BB · 88

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 30 / BB 20 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 30 / 20 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec 8♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.334 | erreur |
| Payer (2 BB de plus) | +2.148 | 0 % | 1.186 | erreur |
| Relancer à 7,8 BB | +3.252 | 0 % | 0.082 | imprécision |
| Tapis (20 BB) | +3.334 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (20 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (20 BB), +3,33 BB par rapport au fold.
> Nuance : relancer à 7,8 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : l'adversaire se couche environ 51 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 6 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Autre option : payer (2 BB de plus), 1,19 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : A7s, KQo, A2s, TT, KQs.

**Correction affichée si le joueur joue « Payer (2 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (20 BB), +3,33 BB par rapport au fold.
> Nuance : relancer à 7,8 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « payer (2 BB de plus) » rapporte 1,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 51 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à une relance à 20 BB (heads-up), on part à tapis avec 33+, A9s+, A8o+ (environ 5 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 6 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : A7s, KQo, A2s, TT, KQs.


## Q105 · exploitant · heads-up · SB premier à parler · 10 BB · 99

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 40 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 54,4 % de ses mains (équilibre push/fold : 37,3 %)

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 54,4 % de ses mains dans cette situation (équilibre push/fold : 37,3 %).
Tu joues en tapis ou fold.
Tu es au SB avec 9♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.563 | erreur |
| Tapis (10 BB) | +2.564 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (10 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (10 BB).
> Partir à tapis gagne entre 2 et 5 BB.
> Il se couche 46 % du temps face à ton tapis (équilibre push/fold : 62 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 99 a 64,8 % d'équité contre sa range de call (équilibre push/fold : 62,0 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (10 BB).
> Ton choix (fold) perd entre 2 et 5 BB.
> Il se couche 46 % du temps face à ton tapis (équilibre push/fold : 62 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 99 a 64,8 % d'équité contre sa range de call (équilibre push/fold : 62,0 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q106 · GTO · 3-handed · BB face à un tapis · 4 BB · J5s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (8 BB, soit 4 BB effectifs).
Le SB se couche.
Tu es au BB avec J♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.134 | erreur |
| Payer le tapis (3 BB de plus) | +0.134 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3 BB de plus), +0,13 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range de tapis, J5s a 36,9 % d'équité : marge de 1,6 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,13 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : Q6o (35,32 %), 86o (35,4 %), 65o (35,5 %) ; se couchent déjà : Q7o (35,2 %), J2s (35,1 %), T3s (35,1 %).
> Ici, on paie avec 60 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3 BB de plus), +0,13 BB par rapport au fold.
> Ton choix (fold) rapporte 0,13 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 4 BB, on paie avec environ 60 % des mains qui arrivent ici.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range de tapis, J5s a 36,9 % d'équité : marge de 1,6 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,13 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : Q6o (35,32 %), 86o (35,4 %), 65o (35,5 %) ; se couchent déjà : Q7o (35,2 %), J2s (35,1 %), T3s (35,1 %).
> Ici, on paie avec 60 % des mains qui arrivent à cette décision.


## Q107 · GTO · heads-up · SB face à une relance · 16 BB · 88

Type : décision nette · EV : HRC · tapis SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 16 / 16 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec 8♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.086 | erreur |
| Payer (2 BB de plus) | +2.399 | 0 % | 0.687 | erreur |
| Tapis (16 BB) | +3.086 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (16 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (16 BB), +3,09 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 42 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 9 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Autre option : payer (2 BB de plus), 0,69 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (16 BB) » : A5s, A4s, KK, A2s, A6o.

**Correction affichée si le joueur joue « Payer (2 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (16 BB), +3,09 BB par rapport au fold.
> Ton choix « payer (2 BB de plus) » rapporte 0,69 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 42 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à une relance à 16 BB (heads-up), on part à tapis avec 22+, A5s+, A6o+, KQo (environ 9 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 9 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (16 BB) » : A5s, A4s, KK, A2s, A6o.


## Q108 · GTO · heads-up · BB face à une relance · 15 BB · J6o

Type : décision nette · EV : HRC · tapis SB 15 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 15 / 15 BB (SB / BB).
Le SB relance à 3,5 BB.
Tu es au BB avec J♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2,5 BB de plus) | -0.547 | 0 % | 0.547 | erreur |
| Tapis (15 BB) | -1.233 | 0 % | 1.232 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; J6o en fait partie.
> Autre option : payer (2,5 BB de plus), 0,55 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 72s, T9o, K8o, 84s, 93s.

**Correction affichée si le joueur joue « Payer (2,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (2,5 BB de plus) » rapporte 0,55 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 15 BB (heads-up), on se couche avec environ 55 % des mains qui arrivent ici.
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; J6o en fait partie.
> Autre option : tapis (15 BB), 1,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 72s, T9o, K8o, 84s, 93s.


## Q109 · GTO · heads-up · BB face à un tapis · 12 BB · 63s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Le SB part à tapis (12 BB).
Tu es au BB avec 6♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -1.738 | 0 % | 1.738 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range de tapis, 63s a 38,6 % d'équité : 7,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,74 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : JTo (46,0 %), QTo (46,0 %), K9o (46,0 %) ; se couchent déjà : A2o (45,7 %), K6s (45,7 %), J8s (45,7 %).
> Ici, on paie avec 30 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (11 BB de plus) » rapporte 1,74 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 12 BB (heads-up), on ne joue que 22+, A2s+, A3o+, K7s+, K9o+, Q9s+, QTo+, J9s+, JTo, T8s+, 98s (environ 30 % des mains qui arrivent ici).
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range de tapis, 63s a 38,6 % d'équité : 7,2 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,74 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : JTo (46,0 %), QTo (46,0 %), K9o (46,0 %) ; se couchent déjà : A2o (45,7 %), K6s (45,7 %), J8s (45,7 %).
> Ici, on paie avec 30 % des mains qui arrivent à cette décision.


## Q110 · GTO · 3-handed · BTN face à un tapis · 8 BB · 86s

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB part à tapis (8 BB).
Le BB paie le tapis.
Tu es au BTN avec 8♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.552 | erreur |
| Payer le tapis (5,7 BB de plus) | +0.552 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5,7 BB de plus), +0,55 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 91 % des mains qui arrivent à cette décision ; 86s en fait partie.
> Repère : il faut 24 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5,7 BB de plus) » : A5s, K7s, A2s, K3s, A5o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5,7 BB de plus), +0,55 BB par rapport au fold.
> Ton choix (fold) rapporte 0,55 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 8 BB, on paie avec environ 91 % des mains qui arrivent ici.
> Ici, on paie avec 91 % des mains qui arrivent à cette décision ; 86s en fait partie.
> Repère : il faut 24 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5,7 BB de plus) » : A5s, K7s, A2s, K3s, A5o.


## Q111 · GTO · 3-handed · BB face à un tapis · 16 BB · 43o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN relance à 2,5 BB.
Le SB part à tapis (16 BB).
Tu es au BB avec 4♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (15 BB de plus) | -4.882 | 0 % | 4.882 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 89 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (15 BB de plus), 4,88 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : ATs, KJs, A9s, QJs, J9s.

**Correction affichée si le joueur joue « Payer le tapis (15 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (15 BB de plus) » rapporte 4,88 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 16 BB, on ne joue que 55+, AJs+, ATo+, KJs+, JTs (environ 10 % des mains qui arrivent ici).
> Ici, on se couche avec 89 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : ATs, KJs, A9s, QJs, J9s.


## Q112 · exploitant · 3-handed · BB face à un tapis · 15 BB · 93o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 25 / BB 35 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 20,4 % de ses mains (équilibre push/fold : 26,8 %)

**Énoncé** : 3 joueurs, tapis 15 / 25 / 35 BB (BTN / SB / BB).
Le BTN part à tapis (15 BB).
Le SB se couche.
Profil fictif « Prudent » : ce BTN part à tapis avec 20,4 % de ses mains dans cette situation (équilibre push/fold : 26,8 %).
Tu es au BB avec 9♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -5.182 | 0 % | 5.182 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait plus de 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30,5 BB, il faut 45,9 % d'équité pour payer.
> Contre sa range, 93o a 28,9 % d'équité : 17,0 points sous le seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 45,9 %, à 2 points près), paient encore : 44 (46,3 %), KQs (46,9 %) ; se couchent déjà : A9o (45,8 %), A8s (45,7 %), KJs (44,2 %).
> Contre ce profil, on paie avec 10 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 16 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (14 BB de plus) » perd plus de 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30,5 BB, il faut 45,9 % d'équité pour payer.
> Contre sa range, 93o a 28,9 % d'équité : 17,0 points sous le seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 45,9 %, à 2 points près), paient encore : 44 (46,3 %), KQs (46,9 %) ; se couchent déjà : A9o (45,8 %), A8s (45,7 %), KJs (44,2 %).
> Contre ce profil, on paie avec 10 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 16 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q113 · exploitant · heads-up · BB face à un tapis · 10 BB · Q5o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis SB 40 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 73,6 % de ses mains (équilibre push/fold : 58,3 %)

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Le SB part à tapis (40 BB, soit 10 BB effectifs).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 73,6 % de ses mains dans cette situation (équilibre push/fold : 58,3 %).
Tu es au BB avec Q♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.067 | 0 % | 0.067 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, Q5o a 44,7 % d'équité : 0,3 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (9 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, Q5o a 44,7 % d'équité : 0,3 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q114 · GTO · 3-handed · BB face à un limp · 18 BB · A5o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu es au BB avec A♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.393 | 0 % | 0.339 | erreur |
| Relancer à 5,3 BB | +0.732 | 100 % | 0.000 | correct |
| Tapis (18 BB) | +0.680 | 0 % | 0.052 | imprécision |

**Référence de l'application** : Relancer à 5,3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 5,3 BB, +0,34 BB par rapport au check.
> Nuance : tapis (18 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 59 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 12 % des mains qui arrivent à cette décision ; A5o en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 5,3 BB » : 98s, A9s, A4s, 54s, K8s.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 5,3 BB, +0,34 BB par rapport au check.
> Nuance : tapis (18 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (check) rapporte 0,34 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 59 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 18 BB, on relance avec QQ+, A9s+, ATo+, KTo+ (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on relance avec 12 % des mains qui arrivent à cette décision ; A5o en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 5,3 BB » : 98s, A9s, A4s, 54s, K8s.


## Q115 · GTO · heads-up · BB face à une relance · 8 BB · K7o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB relance à 2 BB.
Tu es au BB avec K♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.632 | erreur |
| Payer (1 BB de plus) | +0.535 | 0 % | 0.098 | imprécision |
| Tapis (8 BB) | +0.632 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (8 BB), +0,63 BB par rapport au fold.
> Nuance : payer (1 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : l'adversaire se couche environ 22 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 40 % des mains qui arrivent à cette décision ; K7o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K5s, Q2s, J8s, JTo, QJs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (8 BB), +0,63 BB par rapport au fold.
> Nuance : payer (1 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,63 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 22 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à une relance à 8 BB (heads-up), on part à tapis avec 22+, A2+, K3s+, K2o+, Q7s+, Q8o+, J9s+, JTo, T9s (environ 42 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on part à tapis avec 40 % des mains qui arrivent à cette décision ; K7o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K5s, Q2s, J8s, JTo, QJs.


## Q116 · GTO · 3-handed · BB face à un limp · 20 BB · AA

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu es au BB avec A♠A♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +5.521 | 0 % | 5.972 | erreur |
| Relancer à 5,3 BB | +11.493 | 100 % | 0.000 | correct |
| Tapis (20 BB) | +9.945 | 0 % | 1.547 | erreur |

**Référence de l'application** : Relancer à 5,3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 5,3 BB, +5,97 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 50 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 11 % des mains qui arrivent à cette décision ; AA en fait partie.
> Autre option : tapis (20 BB), 1,55 BB de moins.
> Mains jouées en partie seulement pour l'action « relancer à 5,3 BB » : A2s, AQs, 99, A7o, A5o.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Relancer à 5,3 BB, +5,97 BB par rapport au check.
> Ton choix « tapis (20 BB) » rapporte 1,55 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 50 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 20 BB, on relance avec JJ+, KQ, QJo (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on relance avec 11 % des mains qui arrivent à cette décision ; AA en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 5,3 BB » : A2s, AQs, 99, A7o, A5o.


## Q117 · GTO · heads-up · BB face à une relance · 22 BB · J7o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB relance à 7,8 BB.
Tu es au BB avec J♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (4,8 BB de plus) | -0.051 | 0 % | 0.051 | imprécision |
| Tapis (22 BB) | -2.747 | 0 % | 2.747 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : payer (4,8 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; J7o en fait partie.
> Autre option : tapis (22 BB), 2,75 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K9o, J6s, 84s, 55, 87s.

**Correction affichée si le joueur joue « Tapis (22 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : payer (4,8 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (22 BB) » rapporte 2,75 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 22 BB (heads-up), on se couche avec environ 37 % des mains qui arrivent ici.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; J7o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : K9o, J6s, 84s, 55, 87s.


## Q118 · GTO · 3-handed · SB face à une relance · 16 BB · J9o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN se couche.
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec J♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.154 | erreur |
| Payer (2 BB de plus) | +0.154 | 100 % | 0.000 | correct |
| Tapis (16 BB) | -0.388 | 0 % | 0.542 | erreur |

**Référence de l'application** : Payer (2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (2 BB de plus), +0,15 BB par rapport au fold.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 51 % des mains qui arrivent à cette décision ; J9o en fait partie.
> Autre option : tapis (16 BB), 0,54 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : 74s, 87o, J8o, 64s, 52s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer (2 BB de plus), +0,15 BB par rapport au fold.
> Ton choix (fold) rapporte 0,15 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 16 BB, on paie avec environ 52 % des mains qui arrivent ici.
> Ici, on paie avec 51 % des mains qui arrivent à cette décision ; J9o en fait partie.
> Autre option : tapis (16 BB), 0,54 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : 74s, 87o, J8o, 64s, 52s.


## Q119 · GTO · 3-handed · BTN face à un tapis · 15 BB · T9s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB paie 2,3 BB.
Le BB part à tapis (10 BB).
Tu es au BTN avec T♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.353 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.353 | 100 % | 0.000 | correct |
| Tapis (15 BB) | +3.285 | 0 % | 0.069 | imprécision |

**Référence de l'application** : Payer le tapis (7,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7,7 BB de plus), +3,35 BB par rapport au fold.
> Nuance : tapis (15 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 34 % des mains qui arrivent à cette décision ; T9s en fait partie.
> Repère : il faut environ 35 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : QJo, KJo, AJo, AQs, AKo.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7,7 BB de plus), +3,35 BB par rapport au fold.
> Nuance : tapis (15 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 3,35 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 15 BB, on paie avec environ 27 % des mains qui arrivent ici.
> Ici, on paie avec 34 % des mains qui arrivent à cette décision ; T9s en fait partie.
> Repère : il faut environ 35 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : QJo, KJo, AJo, AQs, AKo.


## Q120 · GTO · heads-up · BB face à un tapis · 20 BB · 88

Type : décision nette · EV : HRC · tapis SB 30 / BB 20 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 30 / 20 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (30 BB, soit 20 BB effectifs).
Tu es au BB avec 8♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 9.322 | erreur |
| Payer le tapis (17 BB de plus) | +9.322 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (17 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (17 BB de plus), +9,32 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 49 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (17 BB de plus) » : T7s, T6s, 87s, KJs, A7o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (17 BB de plus), +9,32 BB par rapport au fold.
> Ton choix (fold) rapporte 9,32 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 20 BB (heads-up), on paie avec environ 49 % des mains qui arrivent ici.
> Ici, on paie avec 49 % des mains qui arrivent à cette décision ; 88 en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (17 BB de plus) » : T7s, T6s, 87s, KJs, A7o.


## Q121 · exploitant · heads-up · SB premier à parler · 4 BB · 95o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis SB 8 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 84,9 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : Heads-up, tapis 8 / 4 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 84,9 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu joues en tapis ou fold.
Tu es au SB avec 9♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (4 BB) | -0.097 | 0 % | 0.097 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,06 et 0,5 BB.
> Il se couche 15 % du temps face à ton tapis (équilibre push/fold : 26 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 95o a 39,0 % d'équité contre sa range de call (équilibre push/fold : 36,6 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (4 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (4 BB) » perd entre 0,06 et 0,5 BB.
> Il se couche 15 % du temps face à ton tapis (équilibre push/fold : 26 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 95o a 39,0 % d'équité contre sa range de call (équilibre push/fold : 36,6 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q122 · GTO · 3-handed · BB face à un tapis · 20 BB · 43o

Type : décision nette · EV : HRC · tapis BTN 10 / SB 20 / BB 45 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 10 / 20 / 45 BB (BTN / SB / BB).
Le BTN part à tapis (10 BB).
Le SB part à tapis (20 BB).
Tu es au BB avec 4♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (19 BB de plus) | -6.189 | 0 % | 6.189 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 89 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (19 BB de plus), 6,19 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : QJs, KQs, T9s, ATo, A8s.

**Correction affichée si le joueur joue « Payer le tapis (19 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (19 BB de plus) » rapporte 6,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 20 BB, on ne joue que 44+, ATs+, AJo+, KTs+, QJs (environ 10 % des mains qui arrivent ici).
> Ici, on se couche avec 89 % des mains qui arrivent à cette décision ; 43o en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : QJs, KQs, T9s, ATo, A8s.


## Q123 · exploitant · heads-up · BB face à un tapis · 15 BB · 75o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 15 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 54,1 % de ses mains (équilibre push/fold : 45,7 %)

**Énoncé** : Heads-up, tapis 15 / 15 BB (SB / BB).
Le SB part à tapis (15 BB).
Profil fictif « Agressif » : ce SB part à tapis avec 54,1 % de ses mains dans cette situation (équilibre push/fold : 45,7 %).
Tu es au BB avec 7♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -3.477 | 0 % | 3.477 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, 75o a 35,1 % d'équité : 11,6 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q9o (46,69 %), K7o (46,8 %), 22 (47,3 %) ; se couchent déjà : K4s (46,6 %), T9s (46,5 %), K3s (45,9 %).
> Contre ce profil, on paie avec 34 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Fold.
> Ton choix « payer le tapis (14 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, 75o a 35,1 % d'équité : 11,6 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q9o (46,69 %), K7o (46,8 %), 22 (47,3 %) ; se couchent déjà : K4s (46,6 %), T9s (46,5 %), K3s (45,9 %).
> Contre ce profil, on paie avec 34 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q124 · GTO · 3-handed · BB face à un tapis · 8 BB · A2o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB).
Tu es au BB avec A♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.135 | erreur |
| Payer le tapis (7 BB de plus) | +1.136 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7 BB de plus), +1,14 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, A2o a 50,8 % d'équité : marge de 7,0 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,14 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : J7s (44,0 %), T9o (44,1 %), K3o (44,2 %) ; se couchent déjà : K2o (43,4 %), T7s (43,4 %), Q4s (43,4 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7 BB de plus), +1,14 BB par rapport au fold.
> Ton choix (fold) rapporte 1,14 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 8 BB, on paie avec 22+, A2+, K2s+, K3o+, Q5s+, Q8o+, J7s+, J9o+, T8s+, T9o, 98s (environ 43 % des mains qui arrivent ici).
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, A2o a 50,8 % d'équité : marge de 7,0 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,14 BB sur ce pot) : il fallait payer le tapis (7 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : J7s (44,0 %), T9o (44,1 %), K3o (44,2 %) ; se couchent déjà : K2o (43,4 %), T7s (43,4 %), Q4s (43,4 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.


## Q125 · GTO · heads-up · SB premier à parler · 12 BB · TT

Type : décision nette · EV : HRC · tapis SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.784 | erreur |
| Compléter (0,5 BB de plus) | +2.784 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +2.434 | 0 % | 0.350 | erreur |
| Tapis (12 BB) | +2.219 | 0 % | 0.565 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +2,78 BB par rapport au fold.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> Ici, on complète avec 74 % des mains qui arrivent à cette décision ; TT en fait partie.
> Autre option : relancer à 3,5 BB, 0,35 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 76s, KTo, K2s, A7o, T2o.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +2,78 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,35 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> À retenir : au SB premier à parler à 12 BB (heads-up), on complète avec environ 77 % des mains qui arrivent ici.
> Ici, on complète avec 74 % des mains qui arrivent à cette décision ; TT en fait partie.
> Autre option : tapis (12 BB), 0,57 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 76s, KTo, K2s, A7o, T2o.


## Q126 · GTO · heads-up · SB premier à parler · 14 BB · JJ

Type : décision nette · EV : HRC · tapis SB 14 / BB 14 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec J♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.332 | erreur |
| Compléter (0,5 BB de plus) | +3.332 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +2.984 | 0 % | 0.348 | erreur |
| Tapis (14 BB) | +2.519 | 0 % | 0.813 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +3,33 BB par rapport au fold.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> Ici, on complète avec 78 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Autre option : relancer à 3,5 BB, 0,35 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K8s, J7s, 83o, KJs, 98s.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +3,33 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,35 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> À retenir : au SB premier à parler à 14 BB (heads-up), on complète avec environ 82 % des mains qui arrivent ici.
> Ici, on complète avec 78 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Autre option : tapis (14 BB), 0,81 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K8s, J7s, 83o, KJs, 98s.


## Q127 · GTO · 3-handed · SB face à un tapis · 25 BB · KQo

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 25 / BB 35 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 25 / 35 BB (BTN / SB / BB).
Le BTN limpe.
Tu relances à 4,5 BB.
Le BB paie 4,5 BB.
Le BTN part à tapis (15 BB).
Tu es au SB avec K♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.067 | imprécision |
| Payer le tapis (10,5 BB de plus) | -2.832 | 0 % | 2.900 | erreur |
| Tapis (25 BB) | +0.067 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (25 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (25 BB), +0,07 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> Ici, on part à tapis avec 51 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 30 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (10,5 BB de plus), 2,9 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : ATo, KQs, A2o, AQo, AKo.

**Correction affichée si le joueur joue « Payer le tapis (10,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (25 BB), +0,07 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « payer le tapis (10,5 BB de plus) » rapporte 2,9 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> À retenir : au SB face à un tapis à 25 BB, on part à tapis avec environ 51 % des mains qui arrivent ici.
> Ici, on part à tapis avec 51 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 30 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : ATo, KQs, A2o, AQo, AKo.


## Q128 · GTO · heads-up · SB face à un tapis · 8 BB · Q4o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Tu complètes.
Le BB part à tapis (8 BB).
Tu es au SB avec Q♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -0.507 | 0 % | 0.507 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, Q4o a 40,6 % d'équité : 3,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,51 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : Q4s (43,9 %), T9o (44,5 %), 97s (44,6 %) ; se couchent déjà : J8o (43,7 %), 76s (43,5 %), J6s (43,3 %).
> Ici, on paie avec 32 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 0,51 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 8 BB (heads-up), on ne joue que 55+, A4s+, K6s+, KQo, Q5s+, Q9o+, J7s+, J9o+, T8s+, 98s (environ 32 % des mains qui arrivent ici).
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, Q4o a 40,6 % d'équité : 3,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,51 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : Q4s (43,9 %), T9o (44,5 %), 97s (44,6 %) ; se couchent déjà : J8o (43,7 %), 76s (43,5 %), J6s (43,3 %).
> Ici, on paie avec 32 % des mains qui arrivent à cette décision.


## Q129 · GTO · 3-handed · BB face à un tapis · 18 BB · 43o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Tu es au BB avec 4♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -4.748 | 0 % | 4.748 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 43o a 33,6 % d'équité : 13,0 points sous le seuil.
> Écart large (plus de 10 points, soit environ 4,75 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : A5s (46,60 %), KJo (46,7 %), JTs (47,1 %) ; se couchent déjà : A6s (46,5 %), A8o (46,4 %), A7o (45,2 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17 BB de plus) » rapporte 4,75 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 18 BB, on ne joue que 33+, A7s+, A9o+, KTs+, KJo+, QTs+, JTs (environ 16 % des mains qui arrivent ici).
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 43o a 33,6 % d'équité : 13,0 points sous le seuil.
> Écart large (plus de 10 points, soit environ 4,75 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : A5s (46,60 %), KJo (46,7 %), JTs (47,1 %) ; se couchent déjà : A6s (46,5 %), A8o (46,4 %), A7o (45,2 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.


## Q130 · GTO · 3-handed · BTN face à un tapis · 10 BB · Q8s

Type : décision nette · EV : HRC · tapis BTN 10 / SB 10 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB paie 2,3 BB.
Le BB part à tapis (10 BB).
Tu es au BTN avec Q♠8♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.527 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.527 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7,7 BB de plus), +3,53 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 97 % des mains qui arrivent à cette décision ; Q8s en fait partie.
> Repère : il faut environ 35 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : 97s, T9s, K6s, J9o, 98s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7,7 BB de plus), +3,53 BB par rapport au fold.
> Ton choix (fold) rapporte 3,53 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 10 BB, on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 97 % des mains qui arrivent à cette décision ; Q8s en fait partie.
> Repère : il faut environ 35 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,7 BB de plus) » : 97s, T9s, K6s, J9o, 98s.


## Q131 · exploitant · heads-up · BB face à un tapis · 15 BB · J5o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 35 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 54,1 % de ses mains (équilibre push/fold : 45,7 %)

**Énoncé** : Heads-up, tapis 35 / 15 BB (SB / BB).
Le SB part à tapis (35 BB, soit 15 BB effectifs).
Profil fictif « Agressif » : ce SB part à tapis avec 54,1 % de ses mains dans cette situation (équilibre push/fold : 45,7 %).
Tu es au BB avec J♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -2.469 | 0 % | 2.469 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, J5o a 38,4 % d'équité : 8,3 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 2 et 5 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q9o (46,69 %), K7o (46,8 %), 22 (47,3 %) ; se couchent déjà : K4s (46,6 %), T9s (46,5 %), K3s (45,9 %).
> Contre ce profil, on paie avec 34 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Fold.
> Ton choix « payer le tapis (14 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, J5o a 38,4 % d'équité : 8,3 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 2 et 5 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : Q9o (46,69 %), K7o (46,8 %), 22 (47,3 %) ; se couchent déjà : K4s (46,6 %), T9s (46,5 %), K3s (45,9 %).
> Contre ce profil, on paie avec 34 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q132 · GTO · 3-handed · SB premier à parler · 12 BB · K9o

Type : stratégie mixte · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.562 | erreur |
| Compléter (0,5 BB de plus) | +0.465 | 0 % | 0.097 | imprécision |
| Relancer à 3,3 BB | +0.542 | 45 % | 0.020 | correct |
| Tapis (12 BB) | +0.562 | 55 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (12 BB) ou relancer à 3,3 BB (moins de 0,02 BB d'écart).
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : l'adversaire se couche environ 68 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 28 % des mains qui arrivent à cette décision ; K9o en fait partie.
> K9o est jouée de plusieurs façons (relancer à 3,3 BB 45 %, tapis (12 BB) 55 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : A5s, K7s, 65s, K2s, T8o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (12 BB) ou relancer à 3,3 BB (moins de 0,02 BB d'écart).
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,56 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 68 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 12 BB, on part à tapis avec environ 28 % des mains qui arrivent ici.
> Ici, on part à tapis avec 28 % des mains qui arrivent à cette décision ; K9o en fait partie.
> K9o est jouée de plusieurs façons (relancer à 3,3 BB 45 %, tapis (12 BB) 55 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : A5s, K7s, 65s, K2s, T8o.


## Q133 · GTO · 3-handed · BB face à une relance · 16 BB · Q4s

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,3 BB.
Tu es au BB avec Q♠4♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,3 BB de plus) | -1.834 | 0 % | 1.834 | erreur |
| Tapis (16 BB) | -3.912 | 0 % | 3.912 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; Q4s en fait partie.
> Autre option : payer (3,3 BB de plus), 1,83 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, 54s, A5s, QJo, K3s.

**Correction affichée si le joueur joue « Payer (3,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,3 BB de plus) » rapporte 1,83 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 16 BB, on ne joue que 77+, A7s+, ATo+ (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; Q4s en fait partie.
> Autre option : tapis (16 BB), 3,91 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, 54s, A5s, QJo, K3s.


## Q134 · GTO · 3-handed · BB face à une relance · 14 BB · 93o

Type : décision nette · EV : HRC · tapis BTN 14 / SB 14 / BB 14 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec 9♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,3 BB de plus) | -0.179 | 0 % | 0.179 | erreur |
| Tapis (14 BB) | -0.922 | 0 % | 0.922 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 44 % des mains qui arrivent à cette décision ; 93o en fait partie.
> Autre option : payer (1,3 BB de plus), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 43s, 97o, Q8o, K5o, K7o.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 14 BB, on se couche avec environ 44 % des mains qui arrivent ici.
> Ici, on se couche avec 44 % des mains qui arrivent à cette décision ; 93o en fait partie.
> Autre option : tapis (14 BB), 0,92 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 43s, 97o, Q8o, K5o, K7o.


## Q135 · exploitant · 3-handed · BB face à un tapis · 4 BB · Q4o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 52,6 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Le SB se couche.
Profil fictif « Agressif » : ce BTN part à tapis avec 52,6 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec Q♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.226 | erreur |
| Payer le tapis (3 BB de plus) | +0.226 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Payer le tapis (3 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, Q4o a 38,0 % d'équité : marge de 2,7 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 96o (35,30 %), 73s (35,32 %), 52s (35,4 %) ; se couchent déjà : 54o (35,2 %), 92s (35,0 %), 75o (35,0 %).
> Contre ce profil, on paie avec 73 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, Q4o a 38,0 % d'équité : marge de 2,7 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 96o (35,30 %), 73s (35,32 %), 52s (35,4 %) ; se couchent déjà : 54o (35,2 %), 92s (35,0 %), 75o (35,0 %).
> Contre ce profil, on paie avec 73 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q136 · GTO · 3-handed · BTN face à un tapis · 12 BB · QQ

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB part à tapis (12 BB).
Tu es au BTN avec Q♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 6.965 | erreur |
| Payer le tapis (11 BB de plus) | +6.965 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (11 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (11 BB de plus), +6,97 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 33 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 45 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (11 BB de plus) » : A2s, KJo, K9s, K8s, K6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (11 BB de plus), +6,97 BB par rapport au fold.
> Ton choix (fold) rapporte 6,97 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 12 BB, on paie avec 66+, A2s+, KTs+, KJo+, QTs+ (environ 29 % des mains qui arrivent ici).
> Ici, on paie avec 33 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 45 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (11 BB de plus) » : A2s, KJo, K9s, K8s, K6s.


## Q137 · GTO · 3-handed · SB face à un limp · 20 BB · A9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.655 | erreur |
| Compléter (0,5 BB de plus) | +0.322 | 0 % | 0.333 | erreur |
| Relancer à 4,5 BB | +0.624 | 0 % | 0.032 | imprécision |
| Tapis (20 BB) | +0.655 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (20 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (20 BB), +0,66 BB par rapport au fold.
> Nuance : relancer à 4,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 88 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,33 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : 98s, 96s, A9s, AKo, ATs.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (20 BB), +0,66 BB par rapport au fold.
> Nuance : relancer à 4,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,33 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 88 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à un limp à 20 BB, on part à tapis avec A9o+, KQo, 87s (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on part à tapis avec 12 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : 98s, 96s, A9s, AKo, ATs.


## Q138 · GTO · 3-handed · BTN face à un tapis · 20 BB · K2s

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Tu relances à 2,5 BB.
Le SB part à tapis (20 BB).
Le BB se couche.
Tu es au BTN avec K♠2♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17,5 BB de plus) | -3.201 | 0 % | 3.201 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 59 % des mains qui arrivent à cette décision ; K2s en fait partie.
> Repère : il faut 43 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (17,5 BB de plus), 3,2 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : QTs, KJs, 44, JTs, A9o.

**Correction affichée si le joueur joue « Payer le tapis (17,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17,5 BB de plus) » rapporte 3,2 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BTN face à un tapis à 20 BB, on ne joue que 44+, A6s+, ATo+, KTs+, KQo, QTs+, JTs (environ 42 % des mains qui arrivent ici).
> Ici, on se couche avec 59 % des mains qui arrivent à cette décision ; K2s en fait partie.
> Repère : il faut 43 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : QTs, KJs, 44, JTs, A9o.


## Q139 · exploitant · 3-handed · SB premier à parler · 4 BB · QQ

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 84,9 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 84,9 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.587 | erreur |
| Tapis (4 BB) | +2.587 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (4 BB).
> Partir à tapis gagne entre 2 et 5 BB.
> Il se couche 16 % du temps face à ton tapis (équilibre push/fold : 28 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, QQ a 78,7 % d'équité contre sa range de call (équilibre push/fold : 77,8 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (4 BB).
> Ton choix (fold) perd entre 2 et 5 BB.
> Il se couche 16 % du temps face à ton tapis (équilibre push/fold : 28 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, QQ a 78,7 % d'équité contre sa range de call (équilibre push/fold : 77,8 %) et tout se joue à tapis (4 BB effectifs).
> Contre ce profil, on part à tapis avec 70 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 74 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q140 · GTO · 3-handed · BB face à une relance · 20 BB · 85o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN se couche.
Le SB relance à 3 BB.
Tu es au BB avec 8♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.174 | 0 % | 0.174 | erreur |
| Relancer à 7,5 BB | -0.324 | 0 % | 0.325 | erreur |
| Tapis (20 BB) | -0.765 | 0 % | 0.765 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 39 % des mains qui arrivent à cette décision ; 85o en fait partie.
> Autre option : payer (2 BB de plus), 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 82s, 32s, 75o, T5s, 73s.

**Correction affichée si le joueur joue « Payer (2 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (2 BB de plus) » rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 20 BB, on se couche avec environ 39 % des mains qui arrivent ici.
> Ici, on se couche avec 39 % des mains qui arrivent à cette décision ; 85o en fait partie.
> Autre option : relancer à 7,5 BB, 0,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 82s, 32s, 75o, T5s, 73s.


## Q141 · exploitant · 3-handed · BB face à un tapis · 18 BB · T2s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 18 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 17,4 % de ses mains (équilibre push/fold : 23,1 %)

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Profil fictif « Prudent » : ce BTN part à tapis avec 17,4 % de ses mains dans cette situation (équilibre push/fold : 23,1 %).
Tu es au BB avec T♠2♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -5.446 | 0 % | 5.446 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait plus de 5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, T2s a 31,7 % d'équité : 14,9 points sous le seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : ATo (47,1 %), 55 (47,6 %) ; se couchent déjà : A9s (45,4 %), KQs (45,2 %), 44 (45,1 %).
> Contre ce profil, on paie avec 9 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 13 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (17 BB de plus) » perd plus de 5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, T2s a 31,7 % d'équité : 14,9 points sous le seuil.
> Écart large (plus de 10 points, soit plus de 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : ATo (47,1 %), 55 (47,6 %) ; se couchent déjà : A9s (45,4 %), KQs (45,2 %), 44 (45,1 %).
> Contre ce profil, on paie avec 9 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 13 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q142 · GTO · 3-handed · BTN face à un tapis · 16 BB · KK

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Tu limpes.
Le SB complète.
Le BB part à tapis (16 BB).
Tu es au BTN avec K♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 10.778 | erreur |
| Payer le tapis (15 BB de plus) | +10.778 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15 BB de plus), +10,78 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 32 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : QJo, J7s, J9s, A5s, QTs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15 BB de plus), +10,78 BB par rapport au fold.
> Ton choix (fold) rapporte 10,78 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 16 BB, on paie avec 33+, A6s+, A9o+, KTs+, QTs+, J9s+ (environ 29 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 32 % des mains qui arrivent à cette décision ; KK en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : QJo, J7s, J9s, A5s, QTs.


## Q143 · GTO · 3-handed · BTN premier à parler · 15 BB · 73o

Type : décision nette · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 7♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.243 | 0 % | 0.243 | erreur |
| Relancer à 2,3 BB | -0.265 | 0 % | 0.265 | erreur |
| Tapis (15 BB) | -0.966 | 0 % | 0.966 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Autre option : limper (1 BB), 0,24 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 76s, K4s, J9o, 65s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,24 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 15 BB, on se couche avec environ 65 % des mains qui arrivent ici.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Autre option : relancer à 2,3 BB, 0,26 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 76s, K4s, J9o, 65s.


## Q144 · GTO · 3-handed · SB premier à parler · 12 BB · Q9o

Type : stratégie mixte · EV : HRC · tapis BTN 18 / SB 18 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 18 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.221 | erreur |
| Compléter (0,5 BB de plus) | +0.221 | 65 % | 0.000 | correct |
| Relancer à 3,5 BB | +0.185 | 0 % | 0.035 | imprécision |
| Tapis (12 BB) | +0.208 | 35 % | 0.013 | correct |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : compléter (0,5 BB de plus) ou tapis (12 BB) (moins de 0,02 BB d'écart).
> Nuance : relancer à 3,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 31 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Q9o est jouée de plusieurs façons (compléter (0,5 BB de plus) 65 %, tapis (12 BB) 35 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : T8s, 83s, J5s, 92s, 97s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : compléter (0,5 BB de plus) ou tapis (12 BB) (moins de 0,02 BB d'écart).
> Nuance : relancer à 3,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,22 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 12 BB, on complète avec environ 32 % des mains qui arrivent ici.
> Ici, on complète avec 31 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Q9o est jouée de plusieurs façons (compléter (0,5 BB de plus) 65 %, tapis (12 BB) 35 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : T8s, 83s, J5s, 92s, 97s.


## Q145 · GTO · 3-handed · SB face à une relance · 25 BB · 77

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 30 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 30 / 25 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec 7♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.577 | erreur |
| Payer (1,8 BB de plus) | +0.897 | 0 % | 0.680 | erreur |
| Relancer à 7,6 BB | +1.539 | 0 % | 0.038 | imprécision |
| Tapis (25 BB) | +1.577 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (25 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (25 BB), +1,58 BB par rapport au fold.
> Nuance : relancer à 7,6 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 91 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 7 % des mains qui arrivent à cette décision ; 77 en fait partie.
> Autre option : payer (1,8 BB de plus), 0,68 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : KQo, Q8s, 44, KK, AJs.

**Correction affichée si le joueur joue « Payer (1,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (25 BB), +1,58 BB par rapport au fold.
> Nuance : relancer à 7,6 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « payer (1,8 BB de plus) » rapporte 0,68 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 91 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à une relance à 25 BB, on part à tapis avec QQ+, AKo, KQs, QJs (environ 5 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on part à tapis avec 7 % des mains qui arrivent à cette décision ; 77 en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : KQo, Q8s, 44, KK, AJs.


## Q146 · GTO · heads-up · SB face à un tapis · 8 BB · 55

Type : décision nette · EV : HRC · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Tu relances à 2 BB.
Le BB part à tapis (8 BB).
Tu es au SB avec 5♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.491 | erreur |
| Payer le tapis (6 BB de plus) | +2.491 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (6 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (6 BB de plus), +2,49 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 78 % des mains qui arrivent à cette décision ; 55 en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Aucune main n'est jouée en partie seulement pour l'action « payer le tapis (6 BB de plus) » : la frontière est nette.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (6 BB de plus), +2,49 BB par rapport au fold.
> Ton choix (fold) rapporte 2,49 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 8 BB (heads-up), on paie avec 55+, AJs+, K5s+, QTs+, QJo, J8s+, T7s+, 98s (environ 83 % des mains qui arrivent ici).
> Ici, on paie avec 78 % des mains qui arrivent à cette décision ; 55 en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Aucune main n'est jouée en partie seulement pour l'action « payer le tapis (6 BB de plus) » : la frontière est nette.


## Q147 · exploitant · heads-up · SB premier à parler · 6 BB · A3o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 6 / BB 6 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 70,5 % de ses mains (équilibre push/fold : 54,4 %)

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Personne n'a encore parlé.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 70,5 % de ses mains dans cette situation (équilibre push/fold : 54,4 %).
Tu joues en tapis ou fold.
Tu es au SB avec A♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.015 | erreur |
| Tapis (6 BB) | +1.015 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (6 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (6 BB).
> Partir à tapis gagne entre 1 et 2 BB.
> Il se couche 30 % du temps face à ton tapis (équilibre push/fold : 46 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, A3o a 52,6 % d'équité contre sa range de call (équilibre push/fold : 50,4 %) et tout se joue à tapis (6 BB effectifs).
> Contre ce profil, on part à tapis avec 59 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 68 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (6 BB).
> Ton choix (fold) perd entre 1 et 2 BB.
> Il se couche 30 % du temps face à ton tapis (équilibre push/fold : 46 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, A3o a 52,6 % d'équité contre sa range de call (équilibre push/fold : 50,4 %) et tout se joue à tapis (6 BB effectifs).
> Contre ce profil, on part à tapis avec 59 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 68 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q148 · exploitant · heads-up · BB face à un tapis · 8 BB · JJ

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 8 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Serré (Nit) : part à tapis avec 44,9 % de ses mains (équilibre push/fold : 61,9 %)

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB part à tapis (8 BB).
Profil fictif « Serré (Nit) » : ce SB part à tapis avec 44,9 % de ses mains dans cette situation (équilibre push/fold : 61,9 %).
Tu es au BB avec J♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 4.174 | erreur |
| Payer le tapis (7 BB de plus) | +4.174 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (7 BB de plus).
> Payer gagne entre 2 et 5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, JJ a 69,8 % d'équité : marge de 26,0 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : K5s (44,3 %), QTo (44,7 %), Q9s (45,0 %) ; se couchent déjà : K7o (43,6 %), K4s (43,4 %), J9s (43,1 %).
> Contre ce profil, on paie avec 30 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Serré (Nit) » : Payer le tapis (7 BB de plus).
> Ton choix (fold) perd entre 2 et 5 BB.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range, JJ a 69,8 % d'équité : marge de 26,0 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait payer le tapis (7 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : K5s (44,3 %), QTo (44,7 %), Q9s (45,0 %) ; se couchent déjà : K7o (43,6 %), K4s (43,4 %), J9s (43,1 %).
> Contre ce profil, on paie avec 30 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 45 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q149 · exploitant · heads-up · BB face à un tapis · 14 BB · 66

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 14 / BB 14 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 65,1 % de ses mains (équilibre push/fold : 48,3 %)

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Le SB part à tapis (14 BB).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 65,1 % de ses mains dans cette situation (équilibre push/fold : 48,3 %).
Tu es au BB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.097 | erreur |
| Payer le tapis (13 BB de plus) | +3.097 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (13 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (13 BB de plus).
> Payer gagne entre 2 et 5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, 66 a 57,5 % d'équité : marge de 11,1 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : T8s (46,45 %), J9o (47,0 %), K5o (47,0 %) ; se couchent déjà : Q5s (46,0 %), K4o (46,0 %), J7s (45,9 %).
> Contre ce profil, on paie avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (13 BB de plus).
> Ton choix (fold) perd entre 2 et 5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, 66 a 57,5 % d'équité : marge de 11,1 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait payer le tapis (13 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : T8s (46,45 %), J9o (47,0 %), K5o (47,0 %) ; se couchent déjà : Q5s (46,0 %), K4o (46,0 %), J7s (45,9 %).
> Contre ce profil, on paie avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q150 · GTO · 3-handed · BB face à un limp · 12 BB · KJs

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu es au BB avec K♠J♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.538 | 100 % | 0.000 | correct |
| Relancer à 4,5 BB | +1.472 | 0 % | 0.066 | imprécision |
| Tapis (12 BB) | +1.150 | 0 % | 0.388 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Nuance : relancer à 4,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 82 % des mains qui arrivent à cette décision ; KJs en fait partie.
> Autre option : tapis (12 BB), 0,39 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : Q2s, JTs, A6o, AJs, J8s.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Nuance : relancer à 4,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (12 BB) » rapporte 0,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 12 BB, on checke avec environ 86 % des mains qui arrivent ici.
> Ici, on checke avec 82 % des mains qui arrivent à cette décision ; KJs en fait partie.
> Mains jouées en partie seulement pour l'action « check » : Q2s, JTs, A6o, AJs, J8s.


## Q151 · GTO · 3-handed · BB face à un tapis · 18 BB · K7o

Type : décision nette · EV : HRC · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Le SB part à tapis (18 BB).
Tu es au BB avec K♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -3.645 | 0 % | 3.645 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; K7o en fait partie.
> Repère : il faut environ 46 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (17 BB de plus), 3,65 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A9o, KTs, KQo, K7s, Q9s.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17 BB de plus) » rapporte 3,65 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 18 BB, on ne joue que 44+, A9+, KJs+, KQo, 98s (environ 13 % des mains qui arrivent ici).
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; K7o en fait partie.
> Repère : il faut environ 46 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : A9o, KTs, KQo, K7s, Q9s.


## Q152 · GTO · 3-handed · BTN face à un tapis · 25 BB · AQo

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 35 / SB 25 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 35 / 25 / 15 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB paie 2,3 BB.
Le BB part à tapis (15 BB).
Tu es au BTN avec A♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 5.739 | erreur |
| Payer le tapis (12,7 BB de plus) | +5.675 | 0 % | 0.064 | imprécision |
| Tapis (25 BB) | +5.739 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (25 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (25 BB), +5,74 BB par rapport au fold.
> Nuance : payer le tapis (12,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> Ici, on part à tapis avec 32 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : JJ, K7s, 33, A4s, AQs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (25 BB), +5,74 BB par rapport au fold.
> Nuance : payer le tapis (12,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 5,74 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> À retenir : au BTN face à un tapis à 25 BB, on part à tapis avec environ 32 % des mains qui arrivent ici.
> Ici, on part à tapis avec 32 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (25 BB) » : JJ, K7s, 33, A4s, AQs.


## Q153 · GTO · 3-handed · SB face à un limp · 16 BB · J2o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec J♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.235 | 0 % | 0.235 | erreur |
| Relancer à 4,5 BB | -0.407 | 0 % | 0.407 | erreur |
| Tapis (16 BB) | -1.030 | 0 % | 1.030 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J7s, 32s, 52s, Q6s, Q9o.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,23 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 16 BB, on se couche avec environ 63 % des mains qui arrivent ici.
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Autre option : relancer à 4,5 BB, 0,41 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J7s, 32s, 52s, Q6s, Q9o.


## Q154 · GTO · 3-handed · BB face à un limp · 12 BB · Q9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.269 | 100 % | 0.000 | correct |
| Relancer à 3 BB | +1.187 | 0 % | 0.083 | imprécision |
| Tapis (12 BB) | +1.111 | 0 % | 0.159 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Nuance : relancer à 3 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Autre option : tapis (12 BB), 0,16 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : 44, Q3o, 86o, QTs, 94o.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Nuance : relancer à 3 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (12 BB) » rapporte 0,16 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 12 BB, on checke avec environ 64 % des mains qui arrivent ici.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : 44, Q3o, 86o, QTs, 94o.


## Q155 · GTO · heads-up · BB face à un limp · 8 BB · A8s

Type : stratégie mixte · EV : HRC · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB complète.
Tu es au BB avec A♠8♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.345 | 0 % | 0.179 | erreur |
| Relancer à 2 BB | +1.504 | 25 % | 0.021 | correct |
| Tapis (8 BB) | +1.524 | 75 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (8 BB), +0,18 BB par rapport au check.
> Ton tapis met la pression maximale : l'adversaire se couche environ 68 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; A8s en fait partie.
> A8s est jouée de plusieurs façons (relancer à 2 BB 25 %, tapis (8 BB) 75 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : Q9s, T2s, 65o, J3s, Q6o.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Tapis (8 BB), +0,18 BB par rapport au check.
> Ton choix (check) rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 68 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à un limp à 8 BB (heads-up), on part à tapis avec environ 36 % des mains qui arrivent ici.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; A8s en fait partie.
> A8s est jouée de plusieurs façons (relancer à 2 BB 25 %, tapis (8 BB) 75 %) : ces actions ont une valeur proche. Ton choix (check) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : Q9s, T2s, 65o, J3s, Q6o.


## Q156 · GTO · heads-up · BB face à une relance · 10 BB · 98o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 40 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Le SB relance à 3,5 BB.
Tu es au BB avec 9♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2,5 BB de plus) | -0.070 | 0 % | 0.070 | imprécision |
| Tapis (10 BB) | -0.830 | 0 % | 0.830 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : payer (2,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 55 % des mains qui arrivent à cette décision ; 98o en fait partie.
> Autre option : tapis (10 BB), 0,83 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T6s, Q6s, Q8o, K5o, 75s.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : payer (2,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (10 BB) » rapporte 0,83 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 10 BB (heads-up), on se couche avec environ 58 % des mains qui arrivent ici.
> Ici, on se couche avec 55 % des mains qui arrivent à cette décision ; 98o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : T6s, Q6s, Q8o, K5o, 75s.


## Q157 · GTO · heads-up · BB face à un tapis · 12 BB · 96o

Type : décision nette · EV : HRC · tapis SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (12 BB).
Tu es au BB avec 9♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.905 | 0 % | 0.905 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 46 % des mains qui arrivent à cette décision ; 96o en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (9 BB de plus), 0,91 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K6s, Q9o, 76s, K7s, K5s.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 0,91 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 12 BB (heads-up), on ne joue que 55+, A4s+, AKo, K5s+, K9o+, QTs+, J9s+, T8s+, T9o, 98s, 76s (environ 55 % des mains qui arrivent ici).
> Ici, on se couche avec 46 % des mains qui arrivent à cette décision ; 96o en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : K6s, Q9o, 76s, K7s, K5s.


## Q158 · GTO · 3-handed · BTN premier à parler · 12 BB · 72o

Type : décision nette · EV : HRC · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 12 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 7♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.279 | 0 % | 0.279 | erreur |
| Relancer à 2,3 BB | -0.234 | 0 % | 0.234 | erreur |
| Tapis (12 BB) | -1.025 | 0 % | 1.025 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 65 % des mains qui arrivent à cette décision ; 72o en fait partie.
> Autre option : relancer à 2,3 BB, 0,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J7s, 65s, 76s, 75s, 97s.

**Correction affichée si le joueur joue « Relancer à 2,3 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix (relancer à 2,3 BB) rapporte 0,23 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 12 BB, on se couche avec environ 66 % des mains qui arrivent ici.
> Ici, on se couche avec 65 % des mains qui arrivent à cette décision ; 72o en fait partie.
> Autre option : limper (1 BB), 0,28 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J7s, 65s, 76s, 75s, 97s.


## Q159 · exploitant · 3-handed · BB face à un tapis · 12 BB · 75o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 47,7 % de ses mains (équilibre push/fold : 31,3 %)

**Énoncé** : 3 joueurs, tapis 12 / 12 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (12 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 47,7 % de ses mains dans cette situation (équilibre push/fold : 31,3 %).
Tu es au BB avec 7♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -2.477 | 0 % | 2.477 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range, 75o a 34,8 % d'équité : 10,1 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : T9s (45,1 %), K7o (45,2 %), K3s (45,3 %) ; se couchent déjà : K2s (44,7 %), Q7s (44,6 %), K6o (44,4 %).
> Contre ce profil, on paie avec 35 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 20 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (11 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range, 75o a 34,8 % d'équité : 10,1 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : T9s (45,1 %), K7o (45,2 %), K3s (45,3 %) ; se couchent déjà : K2s (44,7 %), Q7s (44,6 %), K6o (44,4 %).
> Contre ce profil, on paie avec 35 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 20 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q160 · GTO · heads-up · BB face à une relance · 22 BB · T2o

Type : décision nette · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Le SB relance à 3,5 BB.
Tu es au BB avec T♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2,5 BB de plus) | -0.726 | 0 % | 0.727 | erreur |
| Relancer à 8,8 BB | -0.549 | 0 % | 0.549 | erreur |
| Tapis (22 BB) | -1.115 | 0 % | 1.115 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Autre option : relancer à 8,8 BB, 0,55 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T4s, T6s, T5s, K6o, J3s.

**Correction affichée si le joueur joue « Relancer à 8,8 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix (relancer à 8,8 BB) rapporte 0,55 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 22 BB (heads-up), on se couche avec environ 48 % des mains qui arrivent ici.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Autre option : payer (2,5 BB de plus), 0,73 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T4s, T6s, T5s, K6o, J3s.


## Q161 · GTO · heads-up · BB face à un limp · 15 BB · 99

Type : décision nette · EV : HRC · tapis SB 15 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 15 / 15 BB (SB / BB).
Le SB complète.
Tu es au BB avec 9♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.637 | 0 % | 0.621 | erreur |
| Relancer à 3 BB | +2.258 | 100 % | 0.000 | correct |
| Tapis (15 BB) | +2.077 | 0 % | 0.181 | erreur |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,62 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien, et garde l'initiative après le flop.
> Ici, on relance avec 20 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Autre option : tapis (15 BB), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : A9s, 84o, Q7o, A6s, QJs.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,62 BB par rapport au check.
> Ton choix « tapis (15 BB) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien, et garde l'initiative après le flop.
> À retenir : au BB face à un limp à 15 BB (heads-up), on relance avec 77+, A9s+, AKo, K9s+, KQo, Q9s+ (environ 14 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on relance avec 20 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : A9s, 84o, Q7o, A6s, QJs.


## Q162 · GTO · 3-handed · BB face à un tapis · 18 BB · 52o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 12 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Tu es au BB avec 5♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -5.361 | 0 % | 5.361 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 52o a 31,9 % d'équité : 14,7 points sous le seuil.
> Écart large (plus de 10 points, soit environ 5,36 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : QJs (46,8 %), A5s (46,9 %), A6s (47,0 %) ; se couchent déjà : QTs (46,2 %), A7o (45,8 %), KJo (45,7 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17 BB de plus) » rapporte 5,36 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 18 BB, on ne joue que 33+, A5s+, A8o+, KTs+, KQo, QJs (environ 16 % des mains qui arrivent ici).
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 52o a 31,9 % d'équité : 14,7 points sous le seuil.
> Écart large (plus de 10 points, soit environ 5,36 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : QJs (46,8 %), A5s (46,9 %), A6s (47,0 %) ; se couchent déjà : QTs (46,2 %), A7o (45,8 %), KJo (45,7 %).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision.


## Q163 · GTO · 3-handed · SB premier à parler · 18 BB · Q6s

Type : décision nette · EV : HRC · tapis BTN 14 / SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 14 / 18 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec Q♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.293 | erreur |
| Compléter (0,5 BB de plus) | +0.293 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +0.030 | 0 % | 0.264 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +0,29 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 45 % des mains qui arrivent à cette décision ; Q6s en fait partie.
> Autre option : relancer à 3,5 BB, 0,26 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K3s, A8s, 92s, QJs, 96o.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +0,29 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,26 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 18 BB, on complète avec environ 47 % des mains qui arrivent ici.
> Ici, on complète avec 45 % des mains qui arrivent à cette décision ; Q6s en fait partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K3s, A8s, 92s, QJs, 96o.


## Q164 · exploitant · 3-handed · BB face à un tapis · 4 BB · 65o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 61,3 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 8 / 4 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (8 BB, soit 4 BB effectifs).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 61,3 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec 6♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.063 | erreur |
| Payer le tapis (3 BB de plus) | +0.063 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 65o a 36,0 % d'équité : marge de 0,7 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 83s (35,30 %), 73s (35,6 %), T5o (35,7 %) ; se couchent déjà : 54o (35,28 %), 42s (35,2 %), 75o (35,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 65o a 36,0 % d'équité : marge de 0,7 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 83s (35,30 %), 73s (35,6 %), T5o (35,7 %) ; se couchent déjà : 54o (35,28 %), 42s (35,2 %), 75o (35,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q165 · GTO · 3-handed · BB face à une relance · 20 BB · AKo

Type : décision nette · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu relances à 3 BB.
Le SB relance à 7,8 BB.
Tu es au BB avec A♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 10.710 | erreur |
| Payer (4,8 BB de plus) | +9.977 | 0 % | 0.733 | erreur |
| Tapis (20 BB) | +10.710 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (20 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (20 BB), +10,71 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 37 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Autre option : payer (4,8 BB de plus), 0,73 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : A3s, 55, 33, KJo, KTs.

**Correction affichée si le joueur joue « Payer (4,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (20 BB), +10,71 BB par rapport au fold.
> Ton choix « payer (4,8 BB de plus) » rapporte 0,73 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à une relance à 20 BB, on part à tapis avec 44+, A9s+, A8o+, KTs+, KQo (environ 37 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 37 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (20 BB) » : A3s, 55, 33, KJo, KTs.


## Q166 · GTO · 3-handed · BB face à un limp · 15 BB · AJo

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu es au BB avec A♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.424 | 0 % | 0.395 | erreur |
| Relancer à 4,5 BB | +1.818 | 100 % | 0.000 | correct |
| Tapis (15 BB) | +1.723 | 0 % | 0.095 | imprécision |

**Référence de l'application** : Relancer à 4,5 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 4,5 BB, +0,39 BB par rapport au check.
> Nuance : tapis (15 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 54 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 11 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 4,5 BB » : AQo, T8s, KJo, 77, ATo.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 4,5 BB, +0,39 BB par rapport au check.
> Nuance : tapis (15 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (check) rapporte 0,39 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 54 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 15 BB, on relance avec 77+, AJs+, A9o+, 87s (environ 8 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on relance avec 11 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 4,5 BB » : AQo, T8s, KJo, 77, ATo.


## Q167 · GTO · 3-handed · SB face à un limp · 20 BB · K2o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec K♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.168 | 0 % | 0.168 | erreur |
| Relancer à 3,5 BB | -0.546 | 0 % | 0.546 | erreur |
| Tapis (20 BB) | -1.098 | 0 % | 1.098 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 59 % des mains qui arrivent à cette décision ; K2o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,17 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 64s, T3s, T8o, J5s, 52s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 20 BB, on se couche avec environ 59 % des mains qui arrivent ici.
> Ici, on se couche avec 59 % des mains qui arrivent à cette décision ; K2o en fait partie.
> Autre option : relancer à 3,5 BB, 0,55 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 64s, T3s, T8o, J5s, 52s.


## Q168 · GTO · 3-handed · SB face à une relance · 20 BB · 63s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN relance à 2,5 BB.
Tu es au SB avec 6♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.047 | 0 % | 0.047 | imprécision |
| Tapis (20 BB) | -0.673 | 0 % | 0.673 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 79 % des mains qui arrivent à cette décision ; 63s en fait partie.
> Autre option : tapis (20 BB), 0,67 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 97s, 76s, KTo, A6s, KJo.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (20 BB) » rapporte 0,67 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 20 BB, on ne joue que 22+, A2s+, A9o+, K9s+, KJo+, Q9s+, QJo, J9s+, T8s+ (environ 20 % des mains qui arrivent ici).
> Ici, on se couche avec 79 % des mains qui arrivent à cette décision ; 63s en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : 97s, 76s, KTo, A6s, KJo.


## Q169 · GTO · 3-handed · SB face à une relance · 20 BB · A9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.258 | erreur |
| Payer (1,8 BB de plus) | +0.258 | 100 % | 0.000 | correct |
| Relancer à 7,6 BB | +0.095 | 0 % | 0.163 | erreur |
| Tapis (20 BB) | +0.176 | 0 % | 0.082 | imprécision |

**Référence de l'application** : Payer (1,8 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (1,8 BB de plus), +0,26 BB par rapport au fold.
> Nuance : tapis (20 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Payer 1,8 BB pour un pot de 5,6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 6 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Autre option : relancer à 7,6 BB, 0,16 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (1,8 BB de plus) » : 87s, KTs, A7s, K8s, KQs.

**Correction affichée si le joueur joue « Relancer à 7,6 BB » (erreur la plus tentante)**

> Action de référence : Payer (1,8 BB de plus), +0,26 BB par rapport au fold.
> Nuance : tapis (20 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (relancer à 7,6 BB) rapporte 0,16 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 1,8 BB pour un pot de 5,6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 20 BB, on paie avec AA, KJs+, QJs, 87s, 54s (environ 3 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 6 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « payer (1,8 BB de plus) » : 87s, KTs, A7s, K8s, KQs.


## Q170 · GTO · 3-handed · BTN premier à parler · 8 BB · K9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 4 / 8 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec K♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.252 | erreur |
| Limper (1 BB) | +0.195 | 0 % | 0.058 | imprécision |
| Relancer à 2,3 BB | +0.243 | 0 % | 0.010 | correct |
| Tapis (8 BB) | +0.252 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (8 BB) ou relancer à 2,3 BB (moins de 0,02 BB d'écart).
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 45 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 32 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K7o, A2s, JJ, 97s, 76s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (8 BB) ou relancer à 2,3 BB (moins de 0,02 BB d'écart).
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,25 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 45 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BTN premier à parler à 8 BB, on part à tapis avec 22+, A3s+, A2o+, K2s+, K8o+, Q8s+, Q9o+, J7s+, JTo, T9s, 97s+, 76s (environ 34 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on part à tapis avec 32 % des mains qui arrivent à cette décision ; K9o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K7o, A2s, JJ, 97s, 76s.


## Q171 · GTO · heads-up · BB face à un tapis · 18 BB · ATo

Type : décision nette · EV : HRC · tapis SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 18 / 18 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (18 BB).
Tu es au BB avec A♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.491 | erreur |
| Payer le tapis (15 BB de plus) | +2.491 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15 BB de plus), +2,49 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 54 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : K9s, QJo, KTo, J8s, J9o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15 BB de plus), +2,49 BB par rapport au fold.
> Ton choix (fold) rapporte 2,49 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 18 BB (heads-up), on paie avec 33+, A5s+, A7o+, KJ+, Q9s+, QJo, J9s+, JTo, T7s+, 98s, 76s, 65s (environ 52 % des mains qui arrivent ici).
> Ici, on paie avec 54 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 42 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : K9s, QJo, KTo, J8s, J9o.


## Q172 · exploitant · 3-handed · BB face à un tapis · 4 BB · 66

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 52,6 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 4 / 8 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Le SB se couche.
Profil fictif « Agressif » : ce BTN part à tapis avec 52,6 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.760 | erreur |
| Payer le tapis (3 BB de plus) | +1.760 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Payer le tapis (3 BB de plus).
> Payer gagne entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 66 a 56,0 % d'équité : marge de 20,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 96o (35,30 %), 73s (35,32 %), 52s (35,4 %) ; se couchent déjà : 54o (35,2 %), 92s (35,0 %), 75o (35,0 %).
> Contre ce profil, on paie avec 73 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 66 a 56,0 % d'équité : marge de 20,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : erreur nette, il fallait payer le tapis (3 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 96o (35,30 %), 73s (35,32 %), 52s (35,4 %) ; se couchent déjà : 54o (35,2 %), 92s (35,0 %), 75o (35,0 %).
> Contre ce profil, on paie avec 73 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q173 · GTO · 3-handed · BB face à un tapis · 16 BB · QQ

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN part à tapis (16 BB).
Le SB paie le tapis.
Tu es au BB avec Q♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 12.810 | erreur |
| Payer le tapis (15 BB de plus) | +12.810 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15 BB de plus), +12,81 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 16 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : QJo, KJo, 76s, 97s, K6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15 BB de plus), +12,81 BB par rapport au fold.
> Ton choix (fold) rapporte 12,81 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 16 BB, on paie avec 44+, ATs+, AJo+, KJs+, KQo, Q8s+, J9s+, T8s+, 98s, 76s, 65s (environ 14 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on paie avec 16 % des mains qui arrivent à cette décision ; QQ en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : QJo, KJo, 76s, 97s, K6s.


## Q174 · GTO · 3-handed · BB face à un tapis · 18 BB · 32s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Tu es au BB avec 3♠2♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -5.399 | 0 % | 5.399 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 32s a 31,8 % d'équité : 14,8 points sous le seuil.
> Écart large (plus de 10 points, soit environ 5,4 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : QTs (47,2 %), A7s (47,4 %), A8o (47,5 %) ; se couchent déjà : KQo (46,3 %), A5s (46,1 %), T9s (45,9 %).
> Ici, on paie avec 15 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (17 BB de plus) » rapporte 5,4 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 18 BB, on ne joue que 33+, A7s+, A8o+, KTs+, QTs+, JTs (environ 15 % des mains qui arrivent ici).
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range de tapis, 32s a 31,8 % d'équité : 14,8 points sous le seuil.
> Écart large (plus de 10 points, soit environ 5,4 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : QTs (47,2 %), A7s (47,4 %), A8o (47,5 %) ; se couchent déjà : KQo (46,3 %), A5s (46,1 %), T9s (45,9 %).
> Ici, on paie avec 15 % des mains qui arrivent à cette décision.


## Q175 · GTO · 3-handed · BB face à un tapis · 8 BB · J6s

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN part à tapis (8 BB).
Le SB paie le tapis.
Tu es au BB avec J♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -0.821 | 0 % | 0.821 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 77 % des mains qui arrivent à cette décision ; J6s en fait partie.
> Repère : il faut 29 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (7 BB de plus), 0,82 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 86s, 22, KTo, K5s, K7s.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 0,82 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 8 BB, on ne joue que 22+, A6s+, A9o+, K7s+, KJo+, Q8s+, QTo+, J9s+, T7s+, 97s+, 87s (environ 22 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 77 % des mains qui arrivent à cette décision ; J6s en fait partie.
> Repère : il faut 29 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : 86s, 22, KTo, K5s, K7s.


## Q176 · GTO · 3-handed · BTN face à un tapis · 10 BB · QTo

Type : décision nette · EV : HRC · tapis BTN 50 / SB 15 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 50 / 15 / 10 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB part à tapis (10 BB).
Tu es au BTN avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.186 | 0 % | 0.186 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Repère : il faut 44 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (9 BB de plus), 0,19 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : QTs, A2s, K9s, KTo, Q9s.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 0,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BTN face à un tapis à 10 BB, on ne joue que 33+, A2s+, K9s+, KTo+, Q9s+ (environ 36 % des mains qui arrivent ici).
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Repère : il faut 44 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : QTs, A2s, K9s, KTo, Q9s.


## Q177 · GTO · 3-handed · SB face à un limp · 14 BB · 87o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 14 / SB 14 / BB 14 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 8♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.081 | 0 % | 0.081 | imprécision |
| Relancer à 4,3 BB | -0.264 | 0 % | 0.264 | erreur |
| Tapis (14 BB) | -0.463 | 0 % | 0.464 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Autre option : relancer à 4,3 BB, 0,26 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q7s, K2s, 76s, 97s, 86s.

**Correction affichée si le joueur joue « Relancer à 4,3 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (relancer à 4,3 BB) rapporte 0,26 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 14 BB, on ne joue que 22+, A2+, K2s+, K8o+, Q5s+, QTo+, J8s+, JTo, T7s+, 96s+, 85s+ (environ 37 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 63 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Autre option : tapis (14 BB), 0,46 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q7s, K2s, 76s, 97s, 86s.


## Q178 · GTO · 3-handed · BB face à un limp · 8 BB · Q8o

Type : stratégie mixte · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec Q♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.042 | 55 % | 0.000 | correct |
| Relancer à 3 BB | +1.027 | 45 % | 0.015 | correct |
| Tapis (8 BB) | +0.891 | 0 % | 0.151 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : check ou relancer à 3 BB (moins de 0,02 BB d'écart).
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; Q8o en fait partie.
> Autre option : tapis (8 BB), 0,15 BB de moins.
> Q8o est jouée de plusieurs façons (check 55 %, relancer à 3 BB 45 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « check » : 92o, 44, QTs, 33, Q4s.

**Correction affichée si le joueur joue « Tapis (8 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : check ou relancer à 3 BB (moins de 0,02 BB d'écart).
> Ton choix « tapis (8 BB) » rapporte 0,15 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 8 BB, on checke avec environ 65 % des mains qui arrivent ici.
> Ici, on checke avec 61 % des mains qui arrivent à cette décision ; Q8o en fait partie.
> Q8o est jouée de plusieurs façons (check 55 %, relancer à 3 BB 45 %) : ces actions ont une valeur proche. Ton choix « tapis (8 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « check » : 92o, 44, QTs, 33, Q4s.


## Q179 · GTO · 3-handed · BB face à un limp · 4 BB · A9s

Type : décision nette · EV : HRC · tapis BTN 4 / SB 4 / BB 4 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec A♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.191 | 0 % | 0.283 | erreur |
| Tapis (4 BB) | +1.475 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (4 BB), +0,28 BB par rapport au check.
> Ton tapis met la pression maximale : l'adversaire se couche environ 23 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 51 % des mains qui arrivent à cette décision ; A9s en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 53s, KJo, ATo, T5o, J3o.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Tapis (4 BB), +0,28 BB par rapport au check.
> Ton choix (check) rapporte 0,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 23 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à un limp à 4 BB, on part à tapis avec environ 51 % des mains qui arrivent ici.
> Ici, on part à tapis avec 51 % des mains qui arrivent à cette décision ; A9s en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 53s, KJo, ATo, T5o, J3o.


## Q180 · GTO · 3-handed · BTN face à une relance · 15 BB · KTs

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB relance à 4,5 BB.
Tu es au BTN avec K♠T♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.025 | imprécision |
| Payer (3,5 BB de plus) | +0.025 | 100 % | 0.000 | correct |
| Tapis (15 BB) | -0.190 | 0 % | 0.216 | erreur |

**Référence de l'application** : Payer (3,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (3,5 BB de plus), +0,03 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Payer 3,5 BB pour un pot de 9,5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 30 % des mains qui arrivent à cette décision ; KTs en fait partie.
> Autre option : tapis (15 BB), 0,22 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (3,5 BB de plus) » : KQs, QQ, KK, KJo, A8s.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Action de référence : Payer (3,5 BB de plus), +0,03 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (15 BB) » rapporte 0,22 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 3,5 BB pour un pot de 9,5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au BTN face à une relance à 15 BB, on paie avec environ 26 % des mains qui arrivent ici.
> Ici, on paie avec 30 % des mains qui arrivent à cette décision ; KTs en fait partie.
> Mains jouées en partie seulement pour l'action « payer (3,5 BB de plus) » : KQs, QQ, KK, KJo, A8s.


## Q181 · GTO · 3-handed · SB face à un tapis · 12 BB · TT

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Tu relances à 4,5 BB.
Le BB se couche.
Le BTN part à tapis (12 BB).
Tu es au SB avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.486 | erreur |
| Payer le tapis (7,5 BB de plus) | +2.486 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7,5 BB de plus), +2,49 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 84 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,5 BB de plus) » : QJo, K6s, K4s, T7s, T9s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7,5 BB de plus), +2,49 BB par rapport au fold.
> Ton choix (fold) rapporte 2,49 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 12 BB, on paie avec 55+, A2s+, A3o+, K2s+, K9o+, QJo, J8s+, T9s, 97s+, 65s (environ 87 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 84 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,5 BB de plus) » : QJo, K6s, K4s, T7s, T9s.


## Q182 · exploitant · heads-up · BB face à un tapis · 14 BB · A5o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 14 / BB 14 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 39,5 % de ses mains (équilibre push/fold : 48,3 %)

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Le SB part à tapis (14 BB).
Profil fictif « Prudent » : ce SB part à tapis avec 39,5 % de ses mains dans cette situation (équilibre push/fold : 48,3 %).
Tu es au BB avec A♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.418 | erreur |
| Payer le tapis (13 BB de plus) | +0.418 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (13 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Payer le tapis (13 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, A5o a 47,9 % d'équité : marge de 1,5 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : A4o (46,9 %), QTs (47,1 %), 33 (48,2 %) ; se couchent déjà : A3o (46,2 %), 22 (46,2 %), JTs (45,9 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Payer le tapis (13 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, A5o a 47,9 % d'équité : marge de 1,5 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : A4o (46,9 %), QTs (47,1 %), 33 (48,2 %) ; se couchent déjà : A3o (46,2 %), 22 (46,2 %), JTs (45,9 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q183 · GTO · 3-handed · SB face à un limp · 18 BB · J3o

Type : décision nette · EV : HRC · tapis BTN 18 / SB 18 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec J♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.211 | 0 % | 0.211 | erreur |
| Relancer à 4,5 BB | -0.516 | 0 % | 0.516 | erreur |
| Tapis (18 BB) | -0.821 | 0 % | 0.821 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J3o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,21 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K5s, K5o, 86s, 43s, K4s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,21 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 18 BB, on se couche avec environ 62 % des mains qui arrivent ici.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; J3o en fait partie.
> Autre option : relancer à 4,5 BB, 0,52 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K5s, K5o, 86s, 43s, K4s.


## Q184 · GTO · 3-handed · BTN face à une relance · 20 BB · A4o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Tu relances à 2 BB.
Le SB relance à 6,6 BB.
Le BB se couche.
Tu es au BTN avec A♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (4,6 BB de plus) | -0.420 | 0 % | 0.420 | erreur |
| Tapis (20 BB) | -1.413 | 0 % | 1.413 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Autre option : payer (4,6 BB de plus), 0,42 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, QTs, 55, 97s, K9s.

**Correction affichée si le joueur joue « Payer (4,6 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (4,6 BB de plus) » rapporte 0,42 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 20 BB, on ne joue que 44+, A2s+, ATo+, K3s+, KJo+, QTs+, J9s+, 75s+ (environ 46 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Autre option : tapis (20 BB), 1,41 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, QTs, 55, 97s, K9s.


## Q185 · GTO · 3-handed · SB face à une relance · 16 BB · 65s

Type : stratégie mixte · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB relance à 5 BB.
Le BTN paie 5 BB.
Tu es au SB avec 6♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 55 % | 0.000 | correct |
| Payer (4 BB de plus) | -0.049 | 45 % | 0.049 | correct |
| Tapis (16 BB) | -1.599 | 0 % | 1.599 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 58 % des mains qui arrivent à cette décision ; 65s en fait partie.
> Autre option : tapis (16 BB), 1,6 BB de moins.
> 65s est jouée de plusieurs façons (fold 55 %, payer (4 BB de plus) 45 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « fold » : A7s, 98s, KTo, Q5s, A6s.

**Correction affichée si le joueur joue « Tapis (16 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « tapis (16 BB) » rapporte 1,6 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 16 BB, on se couche avec environ 65 % des mains qui arrivent ici.
> Ici, on se couche avec 58 % des mains qui arrivent à cette décision ; 65s en fait partie.
> 65s est jouée de plusieurs façons (fold 55 %, payer (4 BB de plus) 45 %) : ces actions ont une valeur proche. Ton choix « tapis (16 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « fold » : A7s, 98s, KTo, Q5s, A6s.


## Q186 · GTO · 3-handed · BB face à une relance · 18 BB · 54o

Type : stratégie mixte · EV : HRC · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Le SB relance à 3,3 BB.
Tu es au BB avec 5♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 60 % | 0.003 | correct |
| Payer (2,3 BB de plus) | +0.003 | 40 % | 0.000 | correct |
| Tapis (18 BB) | -0.592 | 0 % | 0.594 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou payer (2,3 BB de plus) (moins de 0,02 BB d'écart).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 47 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Autre option : tapis (18 BB), 0,59 BB de moins.
> 54o est jouée de plusieurs façons (fold 60 %, payer (2,3 BB de plus) 40 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « fold » : K6o, 62s, K4o, 94s, K7o.

**Correction affichée si le joueur joue « Tapis (18 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou payer (2,3 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix « tapis (18 BB) » rapporte 0,59 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 18 BB, on se couche avec environ 47 % des mains qui arrivent ici.
> Ici, on se couche avec 47 % des mains qui arrivent à cette décision ; 54o en fait partie.
> 54o est jouée de plusieurs façons (fold 60 %, payer (2,3 BB de plus) 40 %) : ces actions ont une valeur proche. Ton choix « tapis (18 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « fold » : K6o, 62s, K4o, 94s, K7o.


## Q187 · exploitant · 3-handed · BB face à un tapis · 4 BB · 42o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 79,8 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : 3 joueurs, tapis 4 / 8 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB, soit 4 BB effectifs).
Profil fictif « Agressif » : ce SB part à tapis avec 79,8 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu es au BB avec 4♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3 BB de plus) | -0.434 | 0 % | 0.434 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 42o a 32,1 % d'équité : 5,4 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 0,06 et 0,5 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T3o (37,7 %), 53s (37,9 %), 95o (37,9 %) ; se couchent déjà : 83s (37,3 %), 43s (37,3 %), 63s (37,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (3 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Fold.
> Ton choix « payer le tapis (3 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 42o a 32,1 % d'équité : 5,4 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 0,06 et 0,5 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T3o (37,7 %), 53s (37,9 %), 95o (37,9 %) ; se couchent déjà : 83s (37,3 %), 43s (37,3 %), 63s (37,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q188 · GTO · 3-handed · BB face à un tapis · 4 BB · 88

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB, soit 4 BB effectifs).
Tu es au BB avec 8♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.180 | erreur |
| Payer le tapis (3 BB de plus) | +2.180 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (3 BB de plus), +2,18 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, 88 a 64,8 % d'équité : marge de 27,3 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 2,18 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 76o (37,7 %), 53s (37,8 %), 86o (37,8 %) ; se couchent déjà : T5o (37,4 %), 92s (37,2 %), 43s (37,1 %).
> Ici, on paie avec 73 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (3 BB de plus), +2,18 BB par rapport au fold.
> Ton choix (fold) rapporte 2,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 4 BB, on paie avec environ 73 % des mains qui arrivent ici.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range de tapis, 88 a 64,8 % d'équité : marge de 27,3 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 2,18 BB sur ce pot) : erreur nette, il fallait payer le tapis (3 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : 76o (37,7 %), 53s (37,8 %), 86o (37,8 %) ; se couchent déjà : T5o (37,4 %), 92s (37,2 %), 43s (37,1 %).
> Ici, on paie avec 73 % des mains qui arrivent à cette décision.


## Q189 · GTO · 3-handed · BTN face à une relance · 12 BB · T6s

Type : stratégie mixte · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB relance à 4,5 BB.
Tu es au BTN avec T♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 55 % | 0.059 | correct |
| Payer (3,5 BB de plus) | +0.059 | 45 % | 0.000 | correct |
| Tapis (12 BB) | -0.240 | 0 % | 0.299 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold, jouée 55 % du temps.
> L'option « payer (3,5 BB de plus) » vaut presque autant : 0,059 BB de plus en EV ; les deux sont acceptés.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 52 % des mains qui arrivent à cette décision ; T6s en fait partie.
> Autre option : tapis (12 BB), 0,24 BB de moins.
> T6s est jouée de plusieurs façons (fold 55 %, payer (3,5 BB de plus) 45 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « fold » : K5s, K3s, T7s, 65s, 86s.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Action de référence : Fold, jouée 55 % du temps.
> L'option « payer (3,5 BB de plus) » vaut presque autant : 0,059 BB de plus en EV ; les deux sont acceptés.
> Ton choix « tapis (12 BB) » rapporte 0,3 BB de moins que payer (3,5 BB de plus), la plus rentable.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 12 BB, on ne joue que 88+, A2s+, K4s+, KTo+, Q9s+, T7s+, 98s (environ 42 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 52 % des mains qui arrivent à cette décision ; T6s en fait partie.
> T6s est jouée de plusieurs façons (fold 55 %, payer (3,5 BB de plus) 45 %) : ces actions ont une valeur proche. Ton choix « tapis (12 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « fold » : K5s, K3s, T7s, 65s, 86s.


## Q190 · GTO · heads-up · BB face à un tapis · 15 BB · A5o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 15 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 15 / 15 BB (SB / BB).
Le SB part à tapis (15 BB).
Tu es au BB avec A♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.033 | erreur |
| Payer le tapis (14 BB de plus) | +1.033 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (14 BB de plus), +1,03 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, A5o a 50,1 % d'équité : marge de 3,4 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 1,03 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : QTo (46,8 %), T8s (46,8 %), QJo (47,0 %) ; se couchent déjà : KJo (46,66 %), KQo (46,6 %), J8s (46,6 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (14 BB de plus), +1,03 BB par rapport au fold.
> Ton choix (fold) rapporte 1,03 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 15 BB (heads-up), on paie avec 22+, A2s+, A4o+, K9s+, Q9s+, QTo+, J9s+, JTo, T8s+, 98s (environ 25 % des mains qui arrivent ici).
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, A5o a 50,1 % d'équité : marge de 3,4 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 1,03 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : QTo (46,8 %), T8s (46,8 %), QJo (47,0 %) ; se couchent déjà : KJo (46,66 %), KQo (46,6 %), J8s (46,6 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.


## Q191 · GTO · heads-up · BB face à un tapis · 8 BB · 93s

Type : décision nette · EV : HRC · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB complète.
Tu relances à 2 BB.
Le SB part à tapis (8 BB).
Tu es au BB avec 9♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (6 BB de plus) | -0.939 | 0 % | 0.939 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 41 % des mains qui arrivent à cette décision ; 93s en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (6 BB de plus), 0,94 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 98o, Q7s, Q8o, 97s, J8s.

**Correction affichée si le joueur joue « Payer le tapis (6 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (6 BB de plus) » rapporte 0,94 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 8 BB (heads-up), on ne joue que 77+, A4s+, K6s+, KQo, Q8s+, Q9o+, J8s+, JTo, T9s, T8o+, 97s+, 98o (environ 59 % des mains qui arrivent ici).
> Ici, on se couche avec 41 % des mains qui arrivent à cette décision ; 93s en fait partie.
> Repère : il faut 38 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : 98o, Q7s, Q8o, 97s, J8s.


## Q192 · GTO · 3-handed · BB face à un tapis · 12 BB · 75o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (12 BB).
Tu es au BB avec 7♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -2.133 | 0 % | 2.134 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range de tapis, 75o a 36,9 % d'équité : 8,9 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 2,13 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : T8s (45,9 %), Q8s (45,9 %), K8o (46,1 %) ; se couchent déjà : 98s (45,3 %), K5s (45,1 %), K7o (44,7 %).
> Ici, on paie avec 32 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (11 BB de plus) » rapporte 2,13 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 12 BB, on ne joue que 22+, A2+, K6s+, K8o+, Q8s+, QTo+, J8s+, JTo, T8s+ (environ 32 % des mains qui arrivent ici).
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range de tapis, 75o a 36,9 % d'équité : 8,9 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 2,13 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : T8s (45,9 %), Q8s (45,9 %), K8o (46,1 %) ; se couchent déjà : 98s (45,3 %), K5s (45,1 %), K7o (44,7 %).
> Ici, on paie avec 32 % des mains qui arrivent à cette décision.


## Q193 · GTO · 3-handed · BTN face à un tapis · 25 BB · AKo

Type : décision nette · EV : HRC · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 25 / 25 / 25 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB paie 2,3 BB.
Le BB part à tapis (25 BB).
Tu es au BTN avec A♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 7.276 | erreur |
| Payer le tapis (22,7 BB de plus) | +7.276 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (22,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (22,7 BB de plus), +7,28 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 41 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (22,7 BB de plus) » : A9o, JTs, 64s, KTs, A8o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (22,7 BB de plus), +7,28 BB par rapport au fold.
> Ton choix (fold) rapporte 7,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 25 BB, on paie avec 44+, A5s+, A9o+, KJo+, Q7s+, T8s+, 64s+ (environ 39 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 41 % des mains qui arrivent à cette décision ; AKo en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (22,7 BB de plus) » : A9o, JTs, 64s, KTs, A8o.


## Q194 · exploitant · heads-up · BB face à un tapis · 14 BB · 74o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 14 / BB 14 · arbre daa9aaa0

Profil adverse (fictif) : Serré (Nit) : part à tapis avec 31,8 % de ses mains (équilibre push/fold : 48,3 %)

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Le SB part à tapis (14 BB).
Profil fictif « Serré (Nit) » : ce SB part à tapis avec 31,8 % de ses mains dans cette situation (équilibre push/fold : 48,3 %).
Tu es au BB avec 7♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (13 BB de plus) | -3.928 | 0 % | 3.928 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Serré (Nit) » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, 74o a 32,4 % d'équité : 14,0 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : A3s (46,43 %), KJo (46,6 %), A4s (47,1 %) ; se couchent déjà : QJs (45,8 %), A2s (45,8 %), A6o (45,3 %).
> Contre ce profil, on paie avec 18 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (13 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Serré (Nit) » : Fold.
> Ton choix « payer le tapis (13 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range, 74o a 32,4 % d'équité : 14,0 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : A3s (46,43 %), KJo (46,6 %), A4s (47,1 %) ; se couchent déjà : QJs (45,8 %), A2s (45,8 %), A6o (45,3 %).
> Contre ce profil, on paie avec 18 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q195 · GTO · 3-handed · BB face à une relance · 20 BB · 87o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN se couche.
Le SB relance à 2,5 BB.
Tu es au BB avec 8♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.172 | erreur |
| Payer (1,5 BB de plus) | +0.172 | 100 % | 0.000 | correct |
| Relancer à 6,2 BB | -0.074 | 0 % | 0.246 | erreur |
| Tapis (20 BB) | -0.242 | 0 % | 0.413 | erreur |

**Référence de l'application** : Payer (1,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (1,5 BB de plus), +0,17 BB par rapport au fold.
> Payer 1,5 BB pour un pot de 5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 58 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Autre option : relancer à 6,2 BB, 0,25 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (1,5 BB de plus) » : A9o, A6o, A5s, A3o, AQs.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer (1,5 BB de plus), +0,17 BB par rapport au fold.
> Ton choix (fold) rapporte 0,17 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 1,5 BB pour un pot de 5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au BB face à une relance à 20 BB, on paie avec environ 60 % des mains qui arrivent ici.
> Ici, on paie avec 58 % des mains qui arrivent à cette décision ; 87o en fait partie.
> Autre option : relancer à 6,2 BB, 0,25 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (1,5 BB de plus) » : A9o, A6o, A5s, A3o, AQs.


## Q196 · GTO · heads-up · BB face à un tapis · 10 BB · 98o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 10 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Le SB part à tapis (10 BB).
Tu es au BB avec 9♠8♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.342 | 0 % | 0.342 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, 98o a 43,3 % d'équité : 1,7 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,34 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : 97s (45,05 %), 87s (45,2 %), Q9o (45,2 %) ; se couchent déjà : T9o (44,9 %), J7s (44,9 %), T7s (44,8 %).
> Ici, on paie avec 38 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 0,34 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB (heads-up), on ne joue que 22+, A2+, K3s+, K5o+, Q8s+, Q9o+, J8s+, JTo, T8s+, 97s+, 87s (environ 38 % des mains qui arrivent ici).
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, 98o a 43,3 % d'équité : 1,7 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,34 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : 97s (45,05 %), 87s (45,2 %), Q9o (45,2 %) ; se couchent déjà : T9o (44,9 %), J7s (44,9 %), T7s (44,8 %).
> Ici, on paie avec 38 % des mains qui arrivent à cette décision.


## Q197 · GTO · 3-handed · SB face à un limp · 20 BB · A3o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec A♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.074 | 0 % | 0.074 | imprécision |
| Relancer à 4,5 BB | -0.282 | 0 % | 0.282 | erreur |
| Tapis (20 BB) | -0.471 | 0 % | 0.471 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; A3o en fait partie.
> Autre option : relancer à 4,5 BB, 0,28 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J4s, T6s, Q4s, T7o, K5s.

**Correction affichée si le joueur joue « Relancer à 4,5 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (relancer à 4,5 BB) rapporte 0,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 20 BB, on se couche avec environ 63 % des mains qui arrivent ici.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; A3o en fait partie.
> Autre option : tapis (20 BB), 0,47 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J4s, T6s, Q4s, T7o, K5s.


## Q198 · GTO · 3-handed · BB face à un limp · 12 BB · J2o

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu es au BB avec J♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.101 | 100 % | 0.000 | correct |
| Tapis (12 BB) | -1.297 | 0 % | 1.398 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 76 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Autre option : tapis (12 BB), 1,4 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : Q8s, 93s, Q6s, KJs, K8s.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (12 BB) » rapporte 1,4 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 12 BB, on checke avec K4s+, K2o+, Q2+, J2+, T2+, 92+, 82+, 72+, 62+, 52+, 42+, 32 (environ 77 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on checke avec 76 % des mains qui arrivent à cette décision ; J2o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : Q8s, 93s, Q6s, KJs, K8s.


## Q199 · GTO · 3-handed · SB premier à parler · 8 BB · A9o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.471 | erreur |
| Compléter (0,5 BB de plus) | +1.231 | 0 % | 0.240 | erreur |
| Tapis (8 BB) | +1.471 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (8 BB), +1,47 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 57 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 53 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,24 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : 93s, T2s, T6s, 84s, T9s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (8 BB), +1,47 BB par rapport au fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,24 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 57 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 8 BB, on part à tapis avec environ 53 % des mains qui arrivent ici.
> Ici, on part à tapis avec 53 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : 93s, T2s, T6s, 84s, T9s.


## Q200 · GTO · 3-handed · BB face à un tapis · 10 BB · A2o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN part à tapis (15 BB, soit 10 BB effectifs).
Le SB se couche.
Tu es au BB avec A♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.522 | 0 % | 0.522 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range de tapis, A2o a 41,4 % d'équité : 2,5 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,52 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : K9s (44,3 %), A5o (44,4 %), A2s (44,6 %) ; se couchent déjà : KTo (43,7 %), T9s (43,4 %), A4o (43,1 %).
> Ici, on paie avec 22 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 0,52 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB, on ne joue que 22+, A2s+, A5o+, K9s+, KJo+, QTs+, JTs (environ 22 % des mains qui arrivent ici).
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range de tapis, A2o a 41,4 % d'équité : 2,5 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,52 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : K9s (44,3 %), A5o (44,4 %), A2s (44,6 %) ; se couchent déjà : KTo (43,7 %), T9s (43,4 %), A4o (43,1 %).
> Ici, on paie avec 22 % des mains qui arrivent à cette décision.


## Q201 · GTO · heads-up · BB face à un tapis · 6 BB · AKs

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 6 / BB 6 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Le SB part à tapis (6 BB).
Tu es au BB avec A♠K♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.207 | erreur |
| Payer le tapis (5 BB de plus) | +3.207 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5 BB de plus), +3,21 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 5 BB à payer pour un pot final de 12 BB, il faut 41,7 % d'équité pour payer.
> Contre sa range de tapis, AKs a 68,4 % d'équité : marge de 26,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 3,21 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 41,7 %, à 2 points près), paient encore : 86s (41,68 %), 76s (41,8 %), 96s (41,9 %) ; se couchent déjà : J3s (41,6 %), Q3o (41,6 %), T7o (41,0 %).
> Ici, on paie avec 55 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5 BB de plus), +3,21 BB par rapport au fold.
> Ton choix (fold) rapporte 3,21 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 6 BB (heads-up), on paie avec environ 55 % des mains qui arrivent ici.
> Cote du pot : 5 BB à payer pour un pot final de 12 BB, il faut 41,7 % d'équité pour payer.
> Contre sa range de tapis, AKs a 68,4 % d'équité : marge de 26,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit environ 3,21 BB sur ce pot) : erreur nette, il fallait payer le tapis (5 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 41,7 %, à 2 points près), paient encore : 86s (41,68 %), 76s (41,8 %), 96s (41,9 %) ; se couchent déjà : J3s (41,6 %), Q3o (41,6 %), T7o (41,0 %).
> Ici, on paie avec 55 % des mains qui arrivent à cette décision.


## Q202 · GTO · 3-handed · BTN face à un tapis · 8 BB · QJs

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Tu relances à 2,3 BB.
Le SB part à tapis (8 BB).
Le BB se couche.
Tu es au BTN avec Q♠J♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.283 | erreur |
| Payer le tapis (5,7 BB de plus) | +1.283 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5,7 BB de plus), +1,28 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; QJs en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5,7 BB de plus), +1,28 BB par rapport au fold.
> Ton choix (fold) rapporte 1,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 8 BB, on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; QJs en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q203 · exploitant · 3-handed · BB face à un tapis · 4 BB · 65s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 61,3 % de ses mains (équilibre push/fold : 44,2 %)

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 61,3 % de ses mains dans cette situation (équilibre push/fold : 44,2 %).
Tu es au BB avec 6♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.351 | erreur |
| Payer le tapis (3 BB de plus) | +0.352 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 65s a 39,4 % d'équité : marge de 4,1 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 83s (35,30 %), 73s (35,6 %), T5o (35,7 %) ; se couchent déjà : 54o (35,28 %), 42s (35,2 %), 75o (35,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8,5 BB, il faut 35,3 % d'équité pour payer.
> Contre sa range, 65s a 39,4 % d'équité : marge de 4,1 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,3 %, à 2 points près), paient encore : 83s (35,30 %), 73s (35,6 %), T5o (35,7 %) ; se couchent déjà : 54o (35,28 %), 42s (35,2 %), 75o (35,2 %).
> Contre ce profil, on paie avec 77 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 66 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q204 · GTO · 3-handed · BB face à une relance · 12 BB · QTo

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN relance à 2 BB.
Le SB se couche.
Tu es au BB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.472 | erreur |
| Payer (1 BB de plus) | +0.472 | 100 % | 0.000 | correct |
| Tapis (12 BB) | +0.314 | 0 % | 0.158 | erreur |

**Référence de l'application** : Payer (1 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (1 BB de plus), +0,47 BB par rapport au fold.
> Payer 1 BB pour un pot de 4,5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 45 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Autre option : tapis (12 BB), 0,16 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (1 BB de plus) » : QJs, 73s, 98o, 42s, 32s.

**Correction affichée si le joueur joue « Tapis (12 BB) » (erreur la plus tentante)**

> Action de référence : Payer (1 BB de plus), +0,47 BB par rapport au fold.
> Ton choix « tapis (12 BB) » rapporte 0,16 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 1 BB pour un pot de 4,5 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au BB face à une relance à 12 BB, on paie avec environ 49 % des mains qui arrivent ici.
> Ici, on paie avec 45 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Mains jouées en partie seulement pour l'action « payer (1 BB de plus) » : QJs, 73s, 98o, 42s, 32s.


## Q205 · GTO · 3-handed · BB face à une relance · 18 BB · KK

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,3 BB.
Tu es au BB avec K♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 11.325 | erreur |
| Payer (3,3 BB de plus) | +11.231 | 0 % | 0.094 | imprécision |
| Tapis (18 BB) | +11.325 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (18 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (18 BB), +11,32 BB par rapport au fold.
> Nuance : payer (3,3 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 78 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 10 % des mains qui arrivent à cette décision ; KK en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (18 BB) » : A6s, QTs, A4s, 88, 33.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (18 BB), +11,32 BB par rapport au fold.
> Nuance : payer (3,3 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 11,32 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 78 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à une relance à 18 BB, on part à tapis avec 77+, A9s+, ATo+ (environ 10 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 10 % des mains qui arrivent à cette décision ; KK en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (18 BB) » : A6s, QTs, A4s, 88, 33.


## Q206 · GTO · 3-handed · BB face à un tapis · 10 BB · 94o

Type : décision nette · EV : HRC · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN limpe.
Le SB part à tapis (10 BB).
Tu es au BB avec 9♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -3.010 | 0 % | 3.010 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 82 % des mains qui arrivent à cette décision ; 94o en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (9 BB de plus), 3,01 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9s, A3s, 22, 98s, QJs.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 3,01 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB, on ne joue que 44+, A5s+, A7o+, KJs+, KQo (environ 17 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 82 % des mains qui arrivent à cette décision ; 94o en fait partie.
> Repère : il faut environ 43 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : T9s, A3s, 22, 98s, QJs.


## Q207 · exploitant · 3-handed · BB face à un tapis · 15 BB · 65o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 15 / SB 15 / BB 15 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 37,1 % de ses mains (équilibre push/fold : 45,7 %)

**Énoncé** : 3 joueurs, tapis 15 / 15 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (15 BB).
Profil fictif « Prudent » : ce SB part à tapis avec 37,1 % de ses mains dans cette situation (équilibre push/fold : 45,7 %).
Tu es au BB avec 6♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -3.522 | 0 % | 3.522 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, 65o a 34,9 % d'équité : 11,8 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : QTs (46,9 %), A5o (47,0 %), K9s (47,2 %) ; se couchent déjà : A4o (45,9 %), 22 (45,8 %), JTs (45,6 %).
> Contre ce profil, on paie avec 22 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (14 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range, 65o a 34,9 % d'équité : 11,8 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : QTs (46,9 %), A5o (47,0 %), K9s (47,2 %) ; se couchent déjà : A4o (45,9 %), 22 (45,8 %), JTs (45,6 %).
> Contre ce profil, on paie avec 22 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 29 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q208 · GTO · heads-up · SB premier à parler · 22 BB · T7s

Type : décision nette · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec T♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.640 | erreur |
| Compléter (0,5 BB de plus) | +0.640 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +0.407 | 0 % | 0.233 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +0,64 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 71 % des mains qui arrivent à cette décision ; T7s en fait partie.
> Autre option : relancer à 3,5 BB, 0,23 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 85o, T3s, 83o, A2o, J8o.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +0,64 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,23 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 22 BB (heads-up), on complète avec environ 75 % des mains qui arrivent ici.
> Ici, on complète avec 71 % des mains qui arrivent à cette décision ; T7s en fait partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 85o, T3s, 83o, A2o, J8o.


## Q209 · exploitant · 3-handed · BB face à un tapis · 4 BB · 96o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 66,3 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : 3 joueurs, tapis 8 / 4 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (4 BB).
Profil fictif « Prudent » : ce SB part à tapis avec 66,3 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu es au BB avec 9♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3 BB de plus) | -0.061 | 0 % | 0.060 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 96o a 36,7 % d'équité : 0,8 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> À l'équilibre push/fold, ce serait payer le tapis (3 BB de plus).
> Sa range de tapis est un peu plus forte : resserrer légèrement les calls limites.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (3 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Fold.
> Ton choix « payer le tapis (3 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, 96o a 36,7 % d'équité : 0,8 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> À l'équilibre push/fold, ce serait payer le tapis (3 BB de plus).
> Sa range de tapis est un peu plus forte : resserrer légèrement les calls limites.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q210 · GTO · 3-handed · BB face à un limp · 20 BB · A4o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu es au BB avec A♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.501 | 100 % | 0.000 | correct |
| Relancer à 5,5 BB | +0.474 | 0 % | 0.027 | imprécision |
| Tapis (20 BB) | +0.090 | 0 % | 0.410 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Nuance : relancer à 5,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 75 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Autre option : tapis (20 BB), 0,41 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : A5s, J8s, QJs, JTo, Q7s.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Nuance : relancer à 5,5 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (20 BB) » rapporte 0,41 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 20 BB, on checke avec environ 75 % des mains qui arrivent ici.
> Ici, on checke avec 75 % des mains qui arrivent à cette décision ; A4o en fait partie.
> Mains jouées en partie seulement pour l'action « check » : A5s, J8s, QJs, JTo, Q7s.


## Q211 · GTO · 3-handed · SB face à un tapis · 20 BB · TT

Type : décision nette · EV : HRC · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 40 / 15 BB (BTN / SB / BB).
Le BTN limpe.
Tu relances à 4,5 BB.
Le BB part à tapis (15 BB).
Le BTN paie le tapis.
Tu es au SB avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 7.539 | erreur |
| Payer le tapis (10,5 BB de plus) | +7.539 | 100 % | 0.000 | correct |
| Tapis (20 BB) | +7.243 | 0 % | 0.296 | erreur |

**Référence de l'application** : Payer le tapis (10,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (10,5 BB de plus), +7,54 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 40 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut 23 % d'équité pour payer (cote du pot).
> Autre option : tapis (20 BB), 0,3 BB de moins.
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : K5s, QJo, 99, 76s, KJo.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Payer le tapis (10,5 BB de plus), +7,54 BB par rapport au fold.
> Ton choix « tapis (20 BB) » rapporte 0,3 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 20 BB, on paie avec environ 29 % des mains qui arrivent ici.
> Ici, on paie avec 40 % des mains qui arrivent à cette décision ; TT en fait partie.
> Repère : il faut 23 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : K5s, QJo, 99, 76s, KJo.


## Q212 · GTO · 3-handed · SB face à un tapis · 15 BB · 66

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (10 BB).
Le BTN paie le tapis.
Tu es au SB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.716 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.632 | 0 % | 0.084 | imprécision |
| Tapis (15 BB) | +3.715 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 3,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à un tapis à 15 BB, on part à tapis avec 55+, A9s+, KTs+, KJo+ (environ 34 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.


## Q213 · GTO · 3-handed · BB face à un tapis · 10 BB · J5o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (45 BB, soit 10 BB effectifs).
Tu es au BB avec J♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -0.776 | 0 % | 0.776 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 38 % des mains qui arrivent à cette décision ; J5o en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (7 BB de plus), 0,78 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q4s, Q3s, Q9s, T6s, T8o.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 0,78 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB, on ne joue que 55+, A2s+, A3o+, K3s+, K6o+, Q3s+, QJo, J8s+, JTo (environ 62 % des mains qui arrivent ici).
> Ici, on se couche avec 38 % des mains qui arrivent à cette décision ; J5o en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : Q4s, Q3s, Q9s, T6s, T8o.


## Q214 · GTO · 3-handed · BTN face à une relance · 20 BB · J9s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 30 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 30 / 25 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB relance à 4,5 BB.
Tu es au BTN avec J♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -0.018 | 0 % | 0.018 | correct |
| Tapis (20 BB) | -0.856 | 0 % | 0.856 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou payer (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; J9s en fait partie.
> Autre option : tapis (20 BB), 0,86 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q9s, T8s, A4s, 86s, 33.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou payer (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix « tapis (20 BB) » rapporte 0,86 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 20 BB, on se couche avec environ 30 % des mains qui arrivent ici.
> Ici, on se couche avec 36 % des mains qui arrivent à cette décision ; J9s en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : Q9s, T8s, A4s, 86s, 33.


## Q215 · GTO · 3-handed · SB face à un tapis · 8 BB · 62o

Type : décision nette · EV : HRC · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Tu es au SB avec 6♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3,5 BB de plus) | -1.276 | 0 % | 1.276 | erreur |
| Tapis (8 BB) | -1.325 | 0 % | 1.325 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 62o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (3,5 BB de plus), 1,28 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J8s, JTo, K3s.

**Correction affichée si le joueur joue « Payer le tapis (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (3,5 BB de plus) » rapporte 1,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 8 BB, on ne joue que 22+, A2+, K4s+, K8o+, Q8s+, QTo+, J9s+, JTo, T8s+ (environ 33 % des mains qui arrivent ici).
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 62o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : tapis (8 BB), 1,33 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J8s, JTo, K3s.


## Q216 · GTO · 3-handed · BB face à une relance · 20 BB · 97o

Type : décision nette · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,5 BB.
Tu es au BB avec 9♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -2.186 | 0 % | 2.186 | erreur |
| Tapis (20 BB) | -3.479 | 0 % | 3.479 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; 97o en fait partie.
> Autre option : payer (3,5 BB de plus), 2,19 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J3s, KTs, K2s, K6s, KJs.

**Correction affichée si le joueur joue « Payer (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,5 BB de plus) » rapporte 2,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 20 BB, on ne joue que 55+, AJs+, ATo+, KQs, 76s (environ 11 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; 97o en fait partie.
> Autre option : tapis (20 BB), 3,48 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : J3s, KTs, K2s, K6s, KJs.


## Q217 · GTO · 3-handed · SB face à un tapis · 20 BB · A9o

Type : décision nette · EV : HRC · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 20 / 40 BB (BTN / SB / BB).
Le BTN se couche.
Tu complètes.
Le BB relance à 3 BB.
Tu relances à 7,8 BB.
Le BB part à tapis (40 BB, soit 20 BB effectifs).
Tu es au SB avec A♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.451 | erreur |
| Payer le tapis (12,2 BB de plus) | +3.451 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (12,2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (12,2 BB de plus), +3,45 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (12,2 BB de plus), +3,45 BB par rapport au fold.
> Ton choix (fold) rapporte 3,45 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 20 BB, on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A9o en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q218 · GTO · 3-handed · BB face à un tapis · 15 BB · 82o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (20 BB, soit 15 BB effectifs).
Tu es au BB avec 8♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -4.211 | 0 % | 4.211 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, 82o a 32,6 % d'équité : 14,1 points sous le seuil.
> Écart large (plus de 10 points, soit environ 4,21 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : T9s (46,8 %), J9s (46,9 %), Q9s (46,9 %) ; se couchent déjà : QJo (46,5 %), K8s (46,3 %), A2o (46,1 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (14 BB de plus) » rapporte 4,21 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 15 BB, on ne joue que 22+, A2s+, A3o+, K9s+, KTo+, Q9s+, J9s+, T9s (environ 25 % des mains qui arrivent ici).
> Cote du pot : 14 BB à payer pour un pot final de 30 BB, il faut 46,7 % d'équité pour payer.
> Contre sa range de tapis, 82o a 32,6 % d'équité : 14,1 points sous le seuil.
> Écart large (plus de 10 points, soit environ 4,21 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,7 %, à 2 points près), paient encore : T9s (46,8 %), J9s (46,9 %), Q9s (46,9 %) ; se couchent déjà : QJo (46,5 %), K8s (46,3 %), A2o (46,1 %).
> Ici, on paie avec 25 % des mains qui arrivent à cette décision.


## Q219 · GTO · 3-handed · SB face à une relance · 20 BB · T7o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN se couche.
Tu relances à 2,5 BB.
Le BB relance à 6,2 BB.
Tu es au SB avec T♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,75 BB de plus) | -0.654 | 0 % | 0.653 | erreur |
| Tapis (20 BB) | -2.058 | 0 % | 2.058 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 45 % des mains qui arrivent à cette décision ; T7o en fait partie.
> Autre option : payer (3,75 BB de plus), 0,65 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A7o, K8s, Q7s, 75s, K8o.

**Correction affichée si le joueur joue « Payer (3,75 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,75 BB de plus) » rapporte 0,65 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 20 BB, on ne joue que 22+, A2s+, A9o+, K4s+, K8o+, Q7s+, QTo+, J2s+, T8s+, 97s+, 75s+ (environ 51 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 45 % des mains qui arrivent à cette décision ; T7o en fait partie.
> Autre option : tapis (20 BB), 2,06 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A7o, K8s, Q7s, 75s, K8o.


## Q220 · GTO · 3-handed · SB face à un limp · 16 BB · 74o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec 7♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.177 | 0 % | 0.177 | erreur |
| Relancer à 3,5 BB | -0.511 | 0 % | 0.511 | erreur |
| Tapis (16 BB) | -1.249 | 0 % | 1.249 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A3o, K6o, 87s, 98s, 86s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 16 BB, on ne joue que 22+, A2s+, A4o+, K2s+, K7o+, Q5s+, Q9o+, J8s+, J9o+, T8s+, 86s+, 54s (environ 38 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 62 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Autre option : relancer à 3,5 BB, 0,51 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A3o, K6o, 87s, 98s, 86s.


## Q221 · GTO · 3-handed · SB premier à parler · 6 BB · T7s

Type : stratégie mixte · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec T♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.249 | erreur |
| Compléter (0,5 BB de plus) | +0.248 | 20 % | 0.001 | correct |
| Tapis (6 BB) | +0.249 | 80 % | 0.000 | correct |

**Référence de l'application** : Tapis (6 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (6 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton tapis met la pression maximale : l'adversaire se couche environ 46 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 62 % des mains qui arrivent à cette décision ; T7s en fait partie.
> T7s est jouée de plusieurs façons (compléter (0,5 BB de plus) 20 %, tapis (6 BB) 80 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (6 BB) » : T6o, J9s, 97s, J6o, T3s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (6 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,25 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 46 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 6 BB, on part à tapis avec environ 63 % des mains qui arrivent ici.
> Ici, on part à tapis avec 62 % des mains qui arrivent à cette décision ; T7s en fait partie.
> T7s est jouée de plusieurs façons (compléter (0,5 BB de plus) 20 %, tapis (6 BB) 80 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (6 BB) » : T6o, J9s, 97s, J6o, T3s.


## Q222 · exploitant · 3-handed · BB face à un tapis · 18 BB · 87o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 43,7 % de ses mains (équilibre push/fold : 28 %)

**Énoncé** : 3 joueurs, tapis 18 / 12 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 43,7 % de ses mains dans cette situation (équilibre push/fold : 28 %).
Tu es au BB avec 8♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (17 BB de plus) | -3.413 | 0 % | 3.413 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, 87o a 37,2 % d'équité : 9,4 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 2 et 5 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : K7s (47,1 %), A3o (47,1 %), QTo (47,2 %) ; se couchent déjà : A2o (46,5 %), 22 (46,4 %), K6s (46,4 %).
> Contre ce profil, on paie avec 27 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 14 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (17 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (17 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, 87o a 37,2 % d'équité : 9,4 points sous le seuil.
> Écart moyen (5 à 10 points, soit entre 2 et 5 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : K7s (47,1 %), A3o (47,1 %), QTo (47,2 %) ; se couchent déjà : A2o (46,5 %), 22 (46,4 %), K6s (46,4 %).
> Contre ce profil, on paie avec 27 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 14 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q223 · GTO · 3-handed · BTN face à un tapis · 16 BB · ATo

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 279f59f1

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB part à tapis (16 BB).
Tu es au BTN avec A♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.813 | erreur |
| Payer le tapis (15 BB de plus) | +1.813 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15 BB de plus), +1,81 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 29 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : A7o, A8o, QJs, Q8s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15 BB de plus), +1,81 BB par rapport au fold.
> Ton choix (fold) rapporte 1,81 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BTN face à un tapis à 16 BB, on paie avec 55+, A9s+, A8o+, KTs+ (environ 28 % des mains qui arrivent ici).
> Ici, on paie avec 29 % des mains qui arrivent à cette décision ; ATo en fait partie.
> Repère : il faut 46 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (15 BB de plus) » : A7o, A8o, QJs, Q8s.


## Q224 · exploitant · 3-handed · BB face à un tapis · 10 BB · K2o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 45 / SB 20 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 66,2 % de ses mains (équilibre push/fold : 58,3 %)

**Énoncé** : 3 joueurs, tapis 45 / 20 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (20 BB, soit 10 BB effectifs).
Profil fictif « Agressif » : ce SB part à tapis avec 66,2 % de ses mains dans cette situation (équilibre push/fold : 58,3 %).
Tu es au BB avec K♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.062 | 0 % | 0.062 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, K2o a 44,7 % d'équité : 0,3 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q4s (45,2 %), 98s (45,2 %), T9o (45,4 %) ; se couchent déjà : Q7o (44,99 %), J8o (44,7 %), Q3s (44,6 %).
> Contre ce profil, on paie avec 44 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Fold.
> Ton choix « payer le tapis (9 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, K2o a 44,7 % d'équité : 0,3 point sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q4s (45,2 %), 98s (45,2 %), T9o (45,4 %) ; se couchent déjà : Q7o (44,99 %), J8o (44,7 %), Q3s (44,6 %).
> Contre ce profil, on paie avec 44 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q225 · GTO · heads-up · BB face à une relance · 20 BB · 84o

Type : décision nette · EV : HRC · tapis SB 30 / BB 20 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 30 / 20 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB relance à 7,8 BB.
Tu es au BB avec 8♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (4,8 BB de plus) | -1.897 | 0 % | 1.897 | erreur |
| Tapis (20 BB) | -4.683 | 0 % | 4.683 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 38 % des mains qui arrivent à cette décision ; 84o en fait partie.
> Autre option : payer (4,8 BB de plus), 1,9 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 53s, 98s, J9s, J2s, Q8s.

**Correction affichée si le joueur joue « Payer (4,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (4,8 BB de plus) » rapporte 1,9 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 20 BB (heads-up), on se couche avec environ 38 % des mains qui arrivent ici.
> Ici, on se couche avec 38 % des mains qui arrivent à cette décision ; 84o en fait partie.
> Autre option : tapis (20 BB), 4,68 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 53s, 98s, J9s, J2s, Q8s.


## Q226 · GTO · 3-handed · BTN premier à parler · 14 BB · 92o

Type : décision nette · EV : HRC · tapis BTN 14 / SB 14 / BB 14 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 9♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.282 | 0 % | 0.282 | erreur |
| Relancer à 2,3 BB | -0.289 | 0 % | 0.289 | erreur |
| Tapis (14 BB) | -0.928 | 0 % | 0.928 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 92o en fait partie.
> Autre option : limper (1 BB), 0,28 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, A3o, T7s, K5s, T9o.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 14 BB, on ne joue que 22+, A2s+, A4o+, K6s+, K9o+, Q7s+, Q9o+, J7s+, JTo, T8s+, 97s+ (environ 32 % des mains qui arrivent ici).
> Ici, on se couche avec 67 % des mains qui arrivent à cette décision ; 92o en fait partie.
> Autre option : relancer à 2,3 BB, 0,29 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 76s, A3o, T7s, K5s, T9o.


## Q227 · GTO · heads-up · BB face à un tapis · 14 BB · 52o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 14 / BB 14 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Le SB part à tapis (14 BB).
Tu es au BB avec 5♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (13 BB de plus) | -3.783 | 0 % | 3.783 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range de tapis, 52o a 32,9 % d'équité : 13,5 points sous le seuil.
> Écart large (plus de 10 points, soit environ 3,78 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : T8s (46,5 %), 98s (46,7 %), QJo (46,8 %) ; se couchent déjà : JTo (46,42 %), QTo (46,3 %), K8s (46,2 %).
> Ici, on paie avec 26 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (13 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (13 BB de plus) » rapporte 3,78 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 14 BB (heads-up), on ne joue que 22+, A2s+, A4o+, K9s+, KTo+, Q9s+, QJo, J9s+, T8s+, 98s (environ 26 % des mains qui arrivent ici).
> Cote du pot : 13 BB à payer pour un pot final de 28 BB, il faut 46,4 % d'équité pour payer.
> Contre sa range de tapis, 52o a 32,9 % d'équité : 13,5 points sous le seuil.
> Écart large (plus de 10 points, soit environ 3,78 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 46,4 %, à 2 points près), paient encore : T8s (46,5 %), 98s (46,7 %), QJo (46,8 %) ; se couchent déjà : JTo (46,42 %), QTo (46,3 %), K8s (46,2 %).
> Ici, on paie avec 26 % des mains qui arrivent à cette décision.


## Q228 · GTO · 3-handed · BB face à une relance · 15 BB · T3o

Type : décision nette · EV : HRC · tapis BTN 35 / SB 25 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 35 / 25 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB relance à 3,5 BB.
Tu es au BB avec T♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2,5 BB de plus) | -0.605 | 0 % | 0.605 | erreur |
| Tapis (15 BB) | -1.794 | 0 % | 1.794 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 55 % des mains qui arrivent à cette décision ; T3o en fait partie.
> Autre option : payer (2,5 BB de plus), 0,61 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 52s, 63s, 95s, 53s, Q2s.

**Correction affichée si le joueur joue « Payer (2,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (2,5 BB de plus) » rapporte 0,61 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 15 BB, on se couche avec environ 55 % des mains qui arrivent ici.
> Ici, on se couche avec 55 % des mains qui arrivent à cette décision ; T3o en fait partie.
> Autre option : tapis (15 BB), 1,79 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 52s, 63s, 95s, 53s, Q2s.


## Q229 · GTO · 3-handed · BTN face à une relance · 20 BB · Q9o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Tu limpes.
Le SB relance à 4,5 BB.
Le BB se couche.
Tu es au BTN avec Q♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -0.004 | 0 % | 0.004 | correct |
| Tapis (20 BB) | -1.571 | 0 % | 1.571 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou payer (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Autre option : tapis (20 BB), 1,57 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A2s, J8s, QJs, Q9s, A4o.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou payer (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix « tapis (20 BB) » rapporte 1,57 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 20 BB, on ne joue que 44+, A2s+, ATo+, K7s+, QJ, T8s+, 65s (environ 50 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; Q9o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : A2s, J8s, QJs, Q9s, A4o.


## Q230 · GTO · heads-up · BB face à un tapis · 14 BB · K5o

Type : décision nette · EV : HRC · tapis SB 14 / BB 14 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 14 / 14 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (14 BB).
Tu es au BB avec K♠5♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -1.720 | 0 % | 1.720 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 52 % des mains qui arrivent à cette décision ; K5o en fait partie.
> Repère : il faut 39 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (11 BB de plus), 1,72 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q9s, QTo, Q9o, K9o.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (11 BB de plus) » rapporte 1,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 14 BB (heads-up), on ne joue que 55+, A4s+, AQo+, K9s+, KTo+, Q9s+, J9s+, T8s+ (environ 47 % des mains qui arrivent ici).
> Ici, on se couche avec 52 % des mains qui arrivent à cette décision ; K5o en fait partie.
> Repère : il faut 39 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : Q9s, QTo, Q9o, K9o.


## Q231 · GTO · 3-handed · BB face à un limp · 15 BB · AKs

Type : décision nette · EV : HRC · tapis BTN 15 / SB 15 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 15 / 15 BB (BTN / SB / BB).
Le BTN se couche.
Le SB complète.
Tu es au BB avec A♠K♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +2.227 | 0 % | 0.384 | erreur |
| Relancer à 3 BB | +2.611 | 100 % | 0.000 | correct |
| Tapis (15 BB) | +2.393 | 0 % | 0.218 | erreur |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,38 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien, et garde l'initiative après le flop.
> Ici, on relance avec 27 % des mains qui arrivent à cette décision ; AKs en fait partie.
> Autre option : tapis (15 BB), 0,22 BB de moins.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : T6o, T8o, 84o, A3s, Q8o.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,38 BB par rapport au check.
> Ton choix « tapis (15 BB) » rapporte 0,22 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien, et garde l'initiative après le flop.
> À retenir : au BB face à un limp à 15 BB, on relance avec environ 22 % des mains qui arrivent ici.
> Ici, on relance avec 27 % des mains qui arrivent à cette décision ; AKs en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : T6o, T8o, 84o, A3s, Q8o.


## Q232 · GTO · 3-handed · SB premier à parler · 4 BB · K9s

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 4 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec K♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.187 | erreur |
| Compléter (0,5 BB de plus) | +1.009 | 0 % | 0.178 | erreur |
| Tapis (4 BB) | +1.187 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (4 BB), +1,19 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 27 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 73 % des mains qui arrivent à cette décision ; K9s en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,18 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 86o, 93s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (4 BB), +1,19 BB par rapport au fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,18 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 27 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 4 BB, on part à tapis avec environ 73 % des mains qui arrivent ici.
> Ici, on part à tapis avec 73 % des mains qui arrivent à cette décision ; K9s en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 86o, 93s.


## Q233 · GTO · heads-up · SB face à une relance · 22 BB · AKs

Type : décision nette · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB relance à 8,8 BB.
Tu es au SB avec A♠K♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 8.566 | erreur |
| Payer (5,25 BB de plus) | +7.799 | 0 % | 0.767 | erreur |
| Tapis (22 BB) | +8.566 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (22 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (22 BB), +8,57 BB par rapport au fold.
> Ton tapis met la pression maximale : l'adversaire se couche environ 10 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 35 % des mains qui arrivent à cette décision ; AKs en fait partie.
> Autre option : payer (5,25 BB de plus), 0,77 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (22 BB) » : KQo, ATs, 66, KQs, KJs.

**Correction affichée si le joueur joue « Payer (5,25 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (22 BB), +8,57 BB par rapport au fold.
> Ton choix « payer (5,25 BB de plus) » rapporte 0,77 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 10 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à une relance à 22 BB (heads-up), on part à tapis avec 44+, AQs+, A9o+, KQs (environ 35 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on part à tapis avec 35 % des mains qui arrivent à cette décision ; AKs en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (22 BB) » : KQo, ATs, 66, KQs, KJs.


## Q234 · GTO · heads-up · BB face à un limp · 22 BB · AJo

Type : décision nette · EV : HRC · tapis SB 22 / BB 22 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 22 / 22 BB (SB / BB).
Le SB complète.
Tu es au BB avec A♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +1.591 | 0 % | 0.353 | erreur |
| Relancer à 3 BB | +1.943 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3 BB, +0,35 BB par rapport au check.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 34 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 39 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : 75o, 74s, 87o, A3o, T9s.

**Correction affichée si le joueur joue « Check » (erreur la plus tentante)**

> Action de référence : Relancer à 3 BB, +0,35 BB par rapport au check.
> Ton choix (check) rapporte 0,35 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 34 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BB face à un limp à 22 BB (heads-up), on relance avec 44+, A5+, K8+, Q8+, J9s+, JTo, T8o+, 97s+, 65, 53s+ (environ 36 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on relance avec 39 % des mains qui arrivent à cette décision ; AJo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3 BB » : 75o, 74s, 87o, A3o, T9s.


## Q235 · GTO · 3-handed · SB premier à parler · 4 BB · JJ

Type : stratégie mixte · EV : HRC · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 4 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec J♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.086 | erreur |
| Compléter (0,5 BB de plus) | +2.067 | 15 % | 0.019 | correct |
| Tapis (4 BB) | +2.086 | 85 % | 0.000 | correct |

**Référence de l'application** : Tapis (4 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (4 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton tapis met la pression maximale : l'adversaire se couche environ 27 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 73 % des mains qui arrivent à cette décision ; JJ en fait partie.
> JJ est jouée de plusieurs façons (compléter (0,5 BB de plus) 15 %, tapis (4 BB) 85 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 53s, 86o, 73s, 84s, T5o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (4 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 2,09 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 27 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 4 BB, on part à tapis avec environ 73 % des mains qui arrivent ici.
> Ici, on part à tapis avec 73 % des mains qui arrivent à cette décision ; JJ en fait partie.
> JJ est jouée de plusieurs façons (compléter (0,5 BB de plus) 15 %, tapis (4 BB) 85 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (4 BB) » : 53s, 86o, 73s, 84s, T5o.


## Q236 · GTO · 3-handed · BB face à une relance · 6 BB · 84o

Type : stratégie mixte · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB paie 2,3 BB.
Tu es au BB avec 8♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 75 % | 0.000 | correct |
| Payer (1,3 BB de plus) | -0.018 | 25 % | 0.018 | correct |
| Tapis (6 BB) | -0.906 | 0 % | 0.906 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou payer (1,3 BB de plus) (moins de 0,02 BB d'écart).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 48 % des mains qui arrivent à cette décision ; 84o en fait partie.
> Autre option : tapis (6 BB), 0,91 BB de moins.
> 84o est jouée de plusieurs façons (fold 75 %, payer (1,3 BB de plus) 25 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « fold » : Q5s, 97o, K2o, 53s, J6o.

**Correction affichée si le joueur joue « Tapis (6 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou payer (1,3 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix « tapis (6 BB) » rapporte 0,91 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 6 BB, on se couche avec environ 48 % des mains qui arrivent ici.
> Ici, on se couche avec 48 % des mains qui arrivent à cette décision ; 84o en fait partie.
> 84o est jouée de plusieurs façons (fold 75 %, payer (1,3 BB de plus) 25 %) : ces actions ont une valeur proche. Ton choix « tapis (6 BB) » n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « fold » : Q5s, 97o, K2o, 53s, J6o.


## Q237 · GTO · 3-handed · BB face à une relance · 20 BB · T2o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB relance à 7,6 BB.
Tu es au BB avec T♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (20 BB) | -7.146 | 0 % | 7.146 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 91 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Autre option : tapis (20 BB), 7,15 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : ATo, 44, KQs, 77, 66.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « tapis (20 BB) » rapporte 7,15 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 20 BB, on ne joue que 66+, AJs+, ATo+, KQs (environ 9 % des mains qui arrivent ici).
> Ici, on se couche avec 91 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : ATo, 44, KQs, 77, 66.


## Q238 · GTO · heads-up · SB premier à parler · 20 BB · Q6s

Type : décision nette · EV : HRC · tapis SB 20 / BB 30 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 20 / 30 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec Q♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.592 | erreur |
| Compléter (0,5 BB de plus) | +0.592 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +0.397 | 0 % | 0.194 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +0,59 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 73 % des mains qui arrivent à cette décision ; Q6s en fait partie.
> Autre option : relancer à 3,5 BB, 0,19 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : A3o, A9s, 32s, 92o, T7o.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +0,59 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,19 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 20 BB (heads-up), on complète avec environ 74 % des mains qui arrivent ici.
> Ici, on complète avec 73 % des mains qui arrivent à cette décision ; Q6s en fait partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : A3o, A9s, 32s, 92o, T7o.


## Q239 · GTO · 3-handed · SB face à un tapis · 25 BB · Q4s

Type : décision nette · EV : HRC · tapis BTN 25 / SB 35 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 25 / 35 / 15 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (15 BB).
Le BTN part à tapis (25 BB).
Tu es au SB avec Q♠4♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (22,7 BB de plus) | -9.075 | 0 % | 9.075 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; Q4s en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (22,7 BB de plus), 9,08 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : JTs, J9s, 44, KQs, KTs.

**Correction affichée si le joueur joue « Payer le tapis (22,7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (22,7 BB de plus) » rapporte 9,08 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 25 BB, on ne joue que 44+, AJs+, ATo+, KJs+, QTs+, J9s+ (environ 32 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; Q4s en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « fold » : JTs, J9s, 44, KQs, KTs.


## Q240 · GTO · 3-handed · BTN premier à parler · 4 BB · 73o

Type : décision nette · EV : HRC · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 7♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.420 | 0 % | 0.420 | erreur |
| Tapis (4 BB) | -0.658 | 0 % | 0.658 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 58 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Autre option : limper (1 BB), 0,42 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 97s, T7s, Q5s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,42 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 4 BB, on ne joue que 22+, A2+, K2s+, K5o+, Q5s+, Q8o+, J7s+, J9o+, T8s+, T9o, 97s+, 87s (environ 42 % des mains qui arrivent ici).
> Ici, on se couche avec 58 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Autre option : tapis (4 BB), 0,66 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 97s, T7s, Q5s.


## Q241 · exploitant · heads-up · BB face à un tapis · 4 BB · QTo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 4 / BB 4 · arbre daa9aaa0

Profil adverse (fictif) : Prudent : part à tapis avec 66,3 % de ses mains (équilibre push/fold : 73,8 %)

**Énoncé** : Heads-up, tapis 4 / 4 BB (SB / BB).
Le SB part à tapis (4 BB).
Profil fictif « Prudent » : ce SB part à tapis avec 66,3 % de ses mains dans cette situation (équilibre push/fold : 73,8 %).
Tu es au BB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.162 | erreur |
| Payer le tapis (3 BB de plus) | +1.162 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (3 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Prudent » : Payer le tapis (3 BB de plus).
> Payer gagne entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, QTo a 52,0 % d'équité : marge de 14,5 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Prudent » : Payer le tapis (3 BB de plus).
> Ton choix (fold) perd entre 1 et 2 BB.
> Cote du pot : 3 BB à payer pour un pot final de 8 BB, il faut 37,5 % d'équité pour payer.
> Contre sa range, QTo a 52,0 % d'équité : marge de 14,5 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 1 et 2 BB sur ce pot) : erreur nette, il fallait payer le tapis (3 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 37,5 %, à 2 points près), paient encore : T6o (37,6 %), T2s (37,7 %), J4o (37,9 %) ; se couchent déjà : 53s (37,4 %), 74s (37,4 %), J3o (37,2 %).
> Contre ce profil, on paie avec 67 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 73 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q242 · exploitant · 3-handed · SB premier à parler · 10 BB · Q2s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 54,4 % de ses mains (équilibre push/fold : 37,3 %)

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 54,4 % de ses mains dans cette situation (équilibre push/fold : 37,3 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠2♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (10 BB) | -0.062 | 0 % | 0.062 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,06 et 0,5 BB.
> Il se couche 46 % du temps face à ton tapis (équilibre push/fold : 62 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q2s a 40,7 % d'équité contre sa range de call (équilibre push/fold : 36,3 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, tu perds trop de folds : ton tapis vivait de ses abandons, et ta main est trop faible quand il paie.
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> À l'équilibre push/fold, ce serait tapis (10 BB).
> Il se couche moins souvent : tes tapis « de vol », qui vivaient de ses folds, rapportent moins ou perdent ; tes mains fortes gagnent plus, car il paie avec pire. Pousse moins de mains faibles, garde tes mains de valeur.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (10 BB) » perd entre 0,06 et 0,5 BB.
> Il se couche 46 % du temps face à ton tapis (équilibre push/fold : 62 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q2s a 40,7 % d'équité contre sa range de call (équilibre push/fold : 36,3 %) et tout se joue à tapis (10 BB effectifs).
> Contre ce profil, tu perds trop de folds : ton tapis vivait de ses abandons, et ta main est trop faible quand il paie.
> Contre ce profil, on part à tapis avec 46 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 58 %.
> À l'équilibre push/fold, ce serait tapis (10 BB).
> Il se couche moins souvent : tes tapis « de vol », qui vivaient de ses folds, rapportent moins ou perdent ; tes mains fortes gagnent plus, car il paie avec pire. Pousse moins de mains faibles, garde tes mains de valeur.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q243 · GTO · 3-handed · BB face à une relance · 20 BB · 83o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB relance à 7,6 BB.
Tu es au BB avec 8♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (20 BB) | -7.528 | 0 % | 7.528 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 91 % des mains qui arrivent à cette décision ; 83o en fait partie.
> Autre option : tapis (20 BB), 7,53 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KQs, K9s, KTs, A4s, 77.

**Correction affichée si le joueur joue « Tapis (20 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « tapis (20 BB) » rapporte 7,53 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 20 BB, on ne joue que 66+, AJs+, AQo+, KQs (environ 8 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 91 % des mains qui arrivent à cette décision ; 83o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : KQs, K9s, KTs, A4s, 77.


## Q244 · exploitant · 3-handed · SB premier à parler · 12 BB · T9s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 49,7 % de ses mains (équilibre push/fold : 33,1 %)

**Énoncé** : 3 joueurs, tapis 12 / 12 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 49,7 % de ses mains dans cette situation (équilibre push/fold : 33,1 %).
Tu joues en tapis ou fold.
Tu es au SB avec T♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.184 | erreur |
| Tapis (12 BB) | +0.184 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (12 BB).
> Partir à tapis gagne entre 0,06 et 0,5 BB.
> Il se couche 50 % du temps face à ton tapis (équilibre push/fold : 67 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, T9s a 43,1 % d'équité contre sa range de call (équilibre push/fold : 40,8 %) et tout se joue à tapis (12 BB effectifs).
> Contre ce profil, on part à tapis avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 53 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (12 BB).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Il se couche 50 % du temps face à ton tapis (équilibre push/fold : 67 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, T9s a 43,1 % d'équité contre sa range de call (équilibre push/fold : 40,8 %) et tout se joue à tapis (12 BB effectifs).
> Contre ce profil, on part à tapis avec 40 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 53 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q245 · GTO · heads-up · BB face à un tapis · 8 BB · QTo

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB part à tapis (8 BB).
Tu es au BB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.019 | erreur |
| Payer le tapis (7 BB de plus) | +1.019 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7 BB de plus), +1,02 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, QTo a 50,1 % d'équité : marge de 6,3 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,02 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : Q4s (43,9 %), T9o (44,2 %), K3o (44,3 %) ; se couchent déjà : T7s (43,7 %), 97s (43,7 %), 87s (43,6 %).
> Ici, on paie avec 44 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7 BB de plus), +1,02 BB par rapport au fold.
> Ton choix (fold) rapporte 1,02 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 8 BB (heads-up), on paie avec 22+, A2+, K2s+, K3o+, Q4s+, Q8o+, J7s+, J9o+, T8s+, T9o, 98s (environ 44 % des mains qui arrivent ici).
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, QTo a 50,1 % d'équité : marge de 6,3 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit environ 1,02 BB sur ce pot) : il fallait payer le tapis (7 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : Q4s (43,9 %), T9o (44,2 %), K3o (44,3 %) ; se couchent déjà : T7s (43,7 %), 97s (43,7 %), 87s (43,6 %).
> Ici, on paie avec 44 % des mains qui arrivent à cette décision.


## Q246 · GTO · 3-handed · SB face à un tapis · 20 BB · AA

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN relance à 2 BB.
Tu paies 2 BB.
Le BB part à tapis (20 BB).
Le BTN paie le tapis.
Tu es au SB avec A♠A♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 23.962 | erreur |
| Payer le tapis (18 BB de plus) | +23.962 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (18 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (18 BB de plus), +23,96 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 24 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (18 BB de plus) » : A9s, A5s, T9s, Q8s, J9s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (18 BB de plus), +23,96 BB par rapport au fold.
> Ton choix (fold) rapporte 23,96 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 20 BB, on paie avec 66+, A9s+, KJs+, QTs+, JTs, T8s+ (environ 18 % des mains qui arrivent ici).
> Ici, on paie avec 24 % des mains qui arrivent à cette décision ; AA en fait partie.
> Repère : il faut 30 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (18 BB de plus) » : A9s, A5s, T9s, Q8s, J9s.


## Q247 · exploitant · 3-handed · SB premier à parler · 6 BB · Q6s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 6 / SB 6 / BB 6 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 70,5 % de ses mains (équilibre push/fold : 54,4 %)

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 70,5 % de ses mains dans cette situation (équilibre push/fold : 54,4 %).
Tu joues en tapis ou fold.
Tu es au SB avec Q♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.644 | erreur |
| Tapis (6 BB) | +0.644 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (6 BB)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (6 BB).
> Partir à tapis gagne entre 0,5 et 1 BB.
> Il se couche 30 % du temps face à ton tapis (équilibre push/fold : 46 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q6s a 48,1 % d'équité contre sa range de call (équilibre push/fold : 43,3 %) et tout se joue à tapis (6 BB effectifs).
> Contre ce profil, on part à tapis avec 59 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 68 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Tapis (6 BB).
> Ton choix (fold) perd entre 0,5 et 1 BB.
> Il se couche 30 % du temps face à ton tapis (équilibre push/fold : 46 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, Q6s a 48,1 % d'équité contre sa range de call (équilibre push/fold : 43,3 %) et tout se joue à tapis (6 BB effectifs).
> Contre ce profil, on part à tapis avec 59 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 68 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q248 · exploitant · 3-handed · BB face à un tapis · 12 BB · A5s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 69,5 % de ses mains (équilibre push/fold : 53,3 %)

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (12 BB).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 69,5 % de ses mains dans cette situation (équilibre push/fold : 53,3 %).
Tu es au BB avec A♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.563 | erreur |
| Payer le tapis (11 BB de plus) | +2.563 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (11 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (11 BB de plus).
> Payer gagne entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range, A5s a 56,5 % d'équité : marge de 10,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : Q7o (45,9 %), Q4s (46,0 %), K3o (46,1 %) ; se couchent déjà : J8o (45,7 %), T7s (45,5 %), Q3s (45,3 %).
> Contre ce profil, on paie avec 44 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 33 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (11 BB de plus).
> Ton choix (fold) perd entre 2 et 5 BB.
> Cote du pot : 11 BB à payer pour un pot final de 24 BB, il faut 45,8 % d'équité pour payer.
> Contre sa range, A5s a 56,5 % d'équité : marge de 10,7 points au-dessus du seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait payer le tapis (11 BB de plus) sans hésiter, la main est loin du seuil.
> À la limite (seuil 45,8 %, à 2 points près), paient encore : Q7o (45,9 %), Q4s (46,0 %), K3o (46,1 %) ; se couchent déjà : J8o (45,7 %), T7s (45,5 %), Q3s (45,3 %).
> Contre ce profil, on paie avec 44 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 33 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q249 · GTO · 3-handed · BB face à un tapis · 20 BB · KJo

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu relances à 5,5 BB.
Le BTN part à tapis (20 BB).
Le SB paie le tapis.
Tu es au BB avec K♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 6.491 | erreur |
| Payer le tapis (14,5 BB de plus) | +6.491 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (14,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (14,5 BB de plus), +6,49 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 88 % des mains qui arrivent à cette décision ; KJo en fait partie.
> Repère : il faut 24 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (14,5 BB de plus) » : 66, K5s, Q7s, A8o, K3s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (14,5 BB de plus), +6,49 BB par rapport au fold.
> Ton choix (fold) rapporte 6,49 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 20 BB, on paie avec 55+, A2s+, A3o+, KT+, JT, T7s+, 97o+, 64s+ (environ 92 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on paie avec 88 % des mains qui arrivent à cette décision ; KJo en fait partie.
> Repère : il faut 24 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (14,5 BB de plus) » : 66, K5s, Q7s, A8o, K3s.


## Q250 · GTO · 3-handed · BTN face à une relance · 16 BB · J8s

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Tu limpes.
Le SB relance à 4,5 BB.
Le BB paie 4,5 BB.
Tu es au BTN avec J♠8♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -1.110 | 0 % | 1.110 | erreur |
| Tapis (16 BB) | -1.308 | 0 % | 1.308 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 45 % des mains qui arrivent à cette décision ; J8s en fait partie.
> Autre option : payer (3,5 BB de plus), 1,11 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A3o, 86s, 76s, Q4s, K6s.

**Correction affichée si le joueur joue « Payer (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,5 BB de plus) » rapporte 1,11 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BTN face à une relance à 16 BB, on se couche avec environ 46 % des mains qui arrivent ici.
> Ici, on se couche avec 45 % des mains qui arrivent à cette décision ; J8s en fait partie.
> Autre option : tapis (16 BB), 1,31 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A3o, 86s, 76s, Q4s, K6s.


## Q251 · GTO · 3-handed · SB face à un tapis · 8 BB · KQo

Type : stratégie mixte · EV : HRC · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Tu es au SB avec K♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.058 | erreur |
| Payer le tapis (3,5 BB de plus) | +1.058 | 65 % | 0.000 | correct |
| Tapis (8 BB) | +1.050 | 35 % | 0.008 | correct |

**Référence de l'application** : Payer le tapis (3,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : payer le tapis (3,5 BB de plus) ou tapis (8 BB) (moins de 0,02 BB d'écart).
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 9 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> KQo est jouée de plusieurs façons (payer le tapis (3,5 BB de plus) 65 %, tapis (8 BB) 35 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « payer le tapis (3,5 BB de plus) » : Q8s, A2o, T8s, ATs, K5s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : payer le tapis (3,5 BB de plus) ou tapis (8 BB) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 1,06 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 8 BB, on paie avec QQ+, KQo, JTs, T9s (environ 6 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on paie avec 9 % des mains qui arrivent à cette décision ; KQo en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> KQo est jouée de plusieurs façons (payer le tapis (3,5 BB de plus) 65 %, tapis (8 BB) 35 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « payer le tapis (3,5 BB de plus) » : Q8s, A2o, T8s, ATs, K5s.


## Q252 · exploitant · 3-handed · BB face à un tapis · 10 BB · A7s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 10 / SB 10 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Agressif : part à tapis avec 40,2 % de ses mains (équilibre push/fold : 32,5 %)

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN part à tapis (10 BB).
Le SB se couche.
Profil fictif « Agressif » : ce BTN part à tapis avec 40,2 % de ses mains dans cette situation (équilibre push/fold : 32,5 %).
Tu es au BB avec A♠7♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.807 | erreur |
| Payer le tapis (9 BB de plus) | +1.807 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Agressif » : Payer le tapis (9 BB de plus).
> Payer gagne entre 1 et 2 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range, A7s a 52,7 % d'équité : marge de 8,8 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 1 et 2 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : J9s (44,0 %), K5s (44,3 %), K6s (45,1 %) ; se couchent déjà : Q8s (43,87 %), JTo (43,8 %), K4s (43,5 %).
> Contre ce profil, on paie avec 30 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 24 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Agressif » : Payer le tapis (9 BB de plus).
> Ton choix (fold) perd entre 1 et 2 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range, A7s a 52,7 % d'équité : marge de 8,8 points au-dessus du seuil.
> Écart moyen (5 à 10 points, soit entre 1 et 2 BB sur ce pot) : il fallait payer le tapis (9 BB de plus) ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : J9s (44,0 %), K5s (44,3 %), K6s (45,1 %) ; se couchent déjà : Q8s (43,87 %), JTo (43,8 %), K4s (43,5 %).
> Contre ce profil, on paie avec 30 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 24 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q253 · GTO · heads-up · BB face à une relance · 10 BB · 83o

Type : décision nette · EV : HRC · tapis SB 10 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Le SB relance à 3,5 BB.
Tu es au BB avec 8♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2,5 BB de plus) | -0.577 | 0 % | 0.577 | erreur |
| Tapis (10 BB) | -2.317 | 0 % | 2.317 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; 83o en fait partie.
> Autre option : payer (2,5 BB de plus), 0,58 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9o, Q9o, 53s, T2s, Q4s.

**Correction affichée si le joueur joue « Payer (2,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (2,5 BB de plus) » rapporte 0,58 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 10 BB (heads-up), on se couche avec environ 53 % des mains qui arrivent ici.
> Ici, on se couche avec 53 % des mains qui arrivent à cette décision ; 83o en fait partie.
> Autre option : tapis (10 BB), 2,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : T9o, Q9o, 53s, T2s, Q4s.


## Q254 · GTO · 3-handed · SB face à une relance · 16 BB · 76o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec 7♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,8 BB de plus) | -0.400 | 0 % | 0.400 | erreur |
| Tapis (16 BB) | -1.174 | 0 % | 1.175 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 78 % des mains qui arrivent à cette décision ; 76o en fait partie.
> Autre option : payer (1,8 BB de plus), 0,4 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KTo, 87s, Q5s, J8s, 75s.

**Correction affichée si le joueur joue « Payer (1,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,8 BB de plus) » rapporte 0,4 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 16 BB, on ne joue que 22+, A2s+, A8o+, K9s+, KJo+, QTs+, QJo, J9s+, T9s, 98s, 87s (environ 21 % des mains qui arrivent ici).
> Ici, on se couche avec 78 % des mains qui arrivent à cette décision ; 76o en fait partie.
> Autre option : tapis (16 BB), 1,17 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KTo, 87s, Q5s, J8s, 75s.


## Q255 · GTO · heads-up · SB face à un tapis · 16 BB · A9s

Type : décision nette · EV : HRC · tapis SB 16 / BB 16 · arbre 100650d1

**Énoncé** : Heads-up, tapis 16 / 16 BB (SB / BB).
Tu complètes.
Le BB relance à 2 BB.
Tu relances à 5,2 BB.
Le BB part à tapis (16 BB).
Tu es au SB avec A♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.475 | erreur |
| Payer le tapis (10,8 BB de plus) | +3.475 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (10,8 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (10,8 BB de plus), +3,48 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A9s en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (10,8 BB de plus), +3,48 BB par rapport au fold.
> Ton choix (fold) rapporte 3,48 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 16 BB (heads-up), on paie avec environ 100 % des mains qui arrivent ici.
> Ici, on paie avec 100 % des mains qui arrivent à cette décision ; A9s en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Toutes les mains le font ici : pas de frontière.


## Q256 · GTO · 3-handed · BTN face à une relance · 12 BB · KJs

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Tu limpes.
Le SB se couche.
Le BB relance à 4,5 BB.
Tu es au BTN avec K♠J♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.589 | erreur |
| Payer (3,5 BB de plus) | +0.492 | 0 % | 0.097 | imprécision |
| Tapis (12 BB) | +0.589 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (12 BB), +0,59 BB par rapport au fold.
> Nuance : payer (3,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : l'adversaire se couche environ 25 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 26 % des mains qui arrivent à cette décision ; KJs en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : QTo, T8s, KK, QJs, QQ.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (12 BB), +0,59 BB par rapport au fold.
> Nuance : payer (3,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,59 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 25 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BTN face à une relance à 12 BB, on part à tapis avec 66+, A8s+, AQo+ (environ 25 % des mains qui arrivent ici).
> Ici, on part à tapis avec 26 % des mains qui arrivent à cette décision ; KJs en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : QTo, T8s, KK, QJs, QQ.


## Q257 · GTO · 3-handed · BB face à un tapis · 12 BB · KTo

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu relances à 4,5 BB.
Le BTN paie 4,5 BB.
Le SB part à tapis (12 BB).
Tu es au BB avec K♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.690 | erreur |
| Payer le tapis (7,5 BB de plus) | +1.690 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (7,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (7,5 BB de plus), +1,69 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 86 % des mains qui arrivent à cette décision ; KTo en fait partie.
> Repère : il faut environ 26 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,5 BB de plus) » : A8s, K6s, 87s, 66, Q7s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (7,5 BB de plus), +1,69 BB par rapport au fold.
> Ton choix (fold) rapporte 1,69 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 12 BB, on paie avec 66+, A3s+, A2o+, K3s+, K4o+, QJs, J5s+, T8s+ (environ 93 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on paie avec 86 % des mains qui arrivent à cette décision ; KTo en fait partie.
> Repère : il faut environ 26 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (7,5 BB de plus) » : A8s, K6s, 87s, 66, Q7s.


## Q258 · GTO · 3-handed · SB face à une relance · 20 BB · K6o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB relance à 4,5 BB.
Le BTN paie 4,5 BB.
Tu es au SB avec K♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -1.322 | 0 % | 1.322 | erreur |
| Tapis (20 BB) | -3.891 | 0 % | 3.891 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; K6o en fait partie.
> Autre option : payer (3,5 BB de plus), 1,32 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : QJs, T3s, 85s, 64s, A4o.

**Correction affichée si le joueur joue « Payer (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,5 BB de plus) » rapporte 1,32 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 20 BB, on se couche avec environ 70 % des mains qui arrivent ici.
> Ici, on se couche avec 66 % des mains qui arrivent à cette décision ; K6o en fait partie.
> Autre option : tapis (20 BB), 3,89 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : QJs, T3s, 85s, 64s, A4o.


## Q259 · GTO · heads-up · SB face à une relance · 15 BB · QTo

Type : décision nette · EV : HRC · tapis SB 35 / BB 15 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 35 / 15 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec Q♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.058 | erreur |
| Payer (2 BB de plus) | +1.058 | 100 % | 0.000 | correct |
| Tapis (15 BB) | +0.630 | 0 % | 0.427 | erreur |

**Référence de l'application** : Payer (2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (2 BB de plus), +1,06 BB par rapport au fold.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 42 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Autre option : tapis (15 BB), 0,43 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : A7s, 52s, 62s, A5s, A8s.

**Correction affichée si le joueur joue « Tapis (15 BB) » (erreur la plus tentante)**

> Action de référence : Payer (2 BB de plus), +1,06 BB par rapport au fold.
> Ton choix « tapis (15 BB) » rapporte 0,43 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 15 BB (heads-up), on paie avec environ 42 % des mains qui arrivent ici.
> Ici, on paie avec 42 % des mains qui arrivent à cette décision ; QTo en fait partie.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : A7s, 52s, 62s, A5s, A8s.


## Q260 · GTO · 3-handed · BB face à un tapis · 8 BB · 52o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (8 BB).
Tu es au BB avec 5♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -1.743 | 0 % | 1.743 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, 52o a 32,9 % d'équité : 10,9 points sous le seuil.
> Écart large (plus de 10 points, soit environ 1,74 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : K3o (43,82 %), T9o (44,0 %), J7s (44,1 %) ; se couchent déjà : T7s (43,7 %), Q4s (43,5 %), 97s (43,3 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 1,74 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 8 BB, on ne joue que 22+, A2+, K2s+, K3o+, Q5s+, Q8o+, J7s+, J9o+, T8s+, T9o, 98s (environ 43 % des mains qui arrivent ici).
> Cote du pot : 7 BB à payer pour un pot final de 16 BB, il faut 43,8 % d'équité pour payer.
> Contre sa range de tapis, 52o a 32,9 % d'équité : 10,9 points sous le seuil.
> Écart large (plus de 10 points, soit environ 1,74 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 43,8 %, à 2 points près), paient encore : K3o (43,82 %), T9o (44,0 %), J7s (44,1 %) ; se couchent déjà : T7s (43,7 %), Q4s (43,5 %), 97s (43,3 %).
> Ici, on paie avec 43 % des mains qui arrivent à cette décision.


## Q261 · GTO · 3-handed · SB face à un limp · 4 BB · T7o

Type : décision nette · EV : HRC · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN limpe.
Tu es au SB avec T♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Compléter (0,5 BB de plus) | -0.563 | 0 % | 0.563 | erreur |
| Tapis (4 BB) | -0.771 | 0 % | 0.771 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 54 % des mains qui arrivent à cette décision ; T7o en fait partie.
> Autre option : compléter (0,5 BB de plus), 0,56 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 74s, 98s, Q8s, Q8o, 95s.

**Correction affichée si le joueur joue « Compléter (0,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « compléter (0,5 BB de plus) » rapporte 0,56 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au SB face à un limp à 4 BB, on ne joue que 22+, A2+, K2s+, K7o+, Q2s+, Q5o+, J5s+, JTo, T6s+, 98o (environ 45 % des mains qui arrivent ici ; règle simplifiée, exacte pour 94 % d'entre elles).
> Ici, on se couche avec 54 % des mains qui arrivent à cette décision ; T7o en fait partie.
> Autre option : tapis (4 BB), 0,77 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 74s, 98s, Q8s, Q8o, 95s.


## Q262 · GTO · 3-handed · BB face à un limp · 4 BB · T6s

Type : décision nette · EV : HRC · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu es au BB avec T♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Check | +0.507 | 100 % | 0.000 | correct |
| Tapis (4 BB) | +0.220 | 0 % | 0.287 | erreur |

**Référence de l'application** : Check

**Correction affichée si le joueur joue la référence**

> Action de référence : Check.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> Ici, on checke avec 63 % des mains qui arrivent à cette décision ; T6s en fait partie.
> Autre option : tapis (4 BB), 0,29 BB de moins.
> Mains jouées en partie seulement pour l'action « check » : K5o, JTs, K5s, K3o, Q6o.

**Correction affichée si le joueur joue « Tapis (4 BB) » (erreur la plus tentante)**

> Action de référence : Check.
> Ton choix « tapis (4 BB) » rapporte 0,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent.
> À retenir : au BB face à un limp à 4 BB, on checke avec environ 64 % des mains qui arrivent ici.
> Ici, on checke avec 63 % des mains qui arrivent à cette décision ; T6s en fait partie.
> Mains jouées en partie seulement pour l'action « check » : K5o, JTs, K5s, K3o, Q6o.


## Q263 · GTO · 3-handed · BB face à un tapis · 15 BB · 74o

Type : décision nette · EV : HRC · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Le BTN limpe.
Le SB part à tapis (20 BB, soit 15 BB effectifs).
Tu es au BB avec 7♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (14 BB de plus) | -3.943 | 0 % | 3.943 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 87 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (14 BB de plus), 3,94 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : A7s, A5s, K2s, JTs, A9s.

**Correction affichée si le joueur joue « Payer le tapis (14 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (14 BB de plus) » rapporte 3,94 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 15 BB, on ne joue que 55+, A7s+, AJo+, KJs+, KQo, JTs (environ 11 % des mains qui arrivent ici).
> Ici, on se couche avec 87 % des mains qui arrivent à cette décision ; 74o en fait partie.
> Repère : il faut environ 45 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : A7s, A5s, K2s, JTs, A9s.


## Q264 · GTO · 3-handed · BTN premier à parler · 8 BB · 63o

Type : décision nette · EV : HRC · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 8 / 8 / 4 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec 6♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Limper (1 BB) | -0.289 | 0 % | 0.289 | erreur |
| Relancer à 2,3 BB | -0.480 | 0 % | 0.480 | erreur |
| Tapis (8 BB) | -0.772 | 0 % | 0.772 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 63o en fait partie.
> Autre option : limper (1 BB), 0,29 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 98s, Q6s, K3s, 97s.

**Correction affichée si le joueur joue « Limper (1 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « limper (1 BB) » rapporte 0,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé.
> À retenir : au BTN premier à parler à 8 BB, on ne joue que 22+, A2+, K4s+, K7o+, Q7s+, Q9o+, J8s+, JTo, T8s+, 87s (environ 35 % des mains qui arrivent ici).
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 63o en fait partie.
> Autre option : relancer à 2,3 BB, 0,48 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 87s, 98s, Q6s, K3s, 97s.


## Q265 · GTO · 3-handed · BB face à une relance · 10 BB · 73o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB relance à 7,6 BB.
Tu es au BB avec 7♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (10 BB) | -2.909 | 0 % | 2.909 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 85 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Autre option : tapis (10 BB), 2,91 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 44, T8s, 86s, A4s, K9s.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « tapis (10 BB) » rapporte 2,91 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 10 BB, on ne joue que 55+, A2s+, AJo+, KTs+, KQo, QTs+ (environ 13 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 85 % des mains qui arrivent à cette décision ; 73o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : 44, T8s, 86s, A4s, K9s.


## Q266 · GTO · heads-up · SB face à une relance · 10 BB · T3s

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 10 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 10 / 10 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec T♠3♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.095 | imprécision |
| Payer (2 BB de plus) | +0.095 | 100 % | 0.000 | correct |
| Tapis (10 BB) | -0.206 | 0 % | 0.301 | erreur |

**Référence de l'application** : Payer (2 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (2 BB de plus), +0,095 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 33 % des mains qui arrivent à cette décision ; T3s en fait partie.
> Autre option : tapis (10 BB), 0,3 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : K2o, 76o, J2s, Q5o, 88.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Action de référence : Payer (2 BB de plus), +0,095 BB par rapport au fold.
> Nuance : fold est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix « tapis (10 BB) » rapporte 0,3 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 2 BB pour un pot de 6 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 10 BB (heads-up), on paie avec environ 34 % des mains qui arrivent ici.
> Ici, on paie avec 33 % des mains qui arrivent à cette décision ; T3s en fait partie.
> Mains jouées en partie seulement pour l'action « payer (2 BB de plus) » : K2o, 76o, J2s, Q5o, 88.


## Q267 · GTO · 3-handed · SB face à une relance · 20 BB · K6o

Type : décision nette · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Tu complètes.
Le BB relance à 5,3 BB.
Le BTN se couche.
Tu es au SB avec K♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (4,3 BB de plus) | -0.845 | 0 % | 0.845 | erreur |
| Tapis (20 BB) | -3.572 | 0 % | 3.572 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 72 % des mains qui arrivent à cette décision ; K6o en fait partie.
> Autre option : payer (4,3 BB de plus), 0,84 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q7s, J2s, JTs, A5o, K4s.

**Correction affichée si le joueur joue « Payer (4,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (4,3 BB de plus) » rapporte 0,84 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 20 BB, on ne joue que 22+, A6s+, A8o+, K5s+, KQo, Q8s+, J9s+, 76s (environ 19 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 72 % des mains qui arrivent à cette décision ; K6o en fait partie.
> Autre option : tapis (20 BB), 3,57 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q7s, J2s, JTs, A5o, K4s.


## Q268 · GTO · 3-handed · BB face à un tapis · 20 BB · AQo

Type : décision nette · EV : HRC · tapis BTN 30 / SB 25 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 30 / 25 / 20 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,5 BB.
Tu paies 4,5 BB.
Le BTN part à tapis (30 BB, soit 20 BB effectifs).
Le SB paie le tapis.
Tu es au BB avec A♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.775 | erreur |
| Payer le tapis (15,5 BB de plus) | +3.775 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (15,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (15,5 BB de plus), +3,77 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 72 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Repère : il faut environ 24 % d'équité pour payer (cote du pot ; approximatif, car le tapis adverse te couvre).
> Mains jouées en partie seulement pour l'action « payer le tapis (15,5 BB de plus) » : K6s, J4s, Q5s, QTs, T9s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (15,5 BB de plus), +3,77 BB par rapport au fold.
> Ton choix (fold) rapporte 3,77 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 20 BB, on paie avec environ 75 % des mains qui arrivent ici.
> Ici, on paie avec 72 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Repère : il faut environ 24 % d'équité pour payer (cote du pot ; approximatif, car le tapis adverse te couvre).
> Mains jouées en partie seulement pour l'action « payer le tapis (15,5 BB de plus) » : K6s, J4s, Q5s, QTs, T9s.


## Q269 · GTO · 3-handed · BB face à un tapis · 10 BB · 52o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (10 BB).
Tu es au BB avec 5♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -2.373 | 0 % | 2.373 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, 52o a 33,1 % d'équité : 11,9 points sous le seuil.
> Écart large (plus de 10 points, soit environ 2,37 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : T8s (45,3 %), K3s (45,3 %), K6o (45,5 %) ; se couchent déjà : J9o (44,9 %), 98s (44,9 %), Q7s (44,8 %).
> Ici, on paie avec 36 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (9 BB de plus) » rapporte 2,37 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB, on ne joue que 22+, A2+, K3s+, K6o+, Q8s+, Q9o+, J8s+, JTo, T8s+ (environ 36 % des mains qui arrivent ici).
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range de tapis, 52o a 33,1 % d'équité : 11,9 points sous le seuil.
> Écart large (plus de 10 points, soit environ 2,37 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : T8s (45,3 %), K3s (45,3 %), K6o (45,5 %) ; se couchent déjà : J9o (44,9 %), 98s (44,9 %), Q7s (44,8 %).
> Ici, on paie avec 36 % des mains qui arrivent à cette décision.


## Q270 · exploitant · 3-handed · BB face à un tapis · 18 BB · QJo

Type : décision serrée (autre action à moins de 0,1 BB) · EV : exacte (tout le monde à tapis) · tapis BTN 18 / SB 18 / BB 18 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 37,5 % de ses mains (équilibre push/fold : 23,1 %)

**Énoncé** : 3 joueurs, tapis 18 / 18 / 18 BB (BTN / SB / BB).
Le BTN part à tapis (18 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 37,5 % de ses mains dans cette situation (équilibre push/fold : 23,1 %).
Tu es au BB avec Q♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.081 | erreur |
| Payer le tapis (17 BB de plus) | +0.081 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (17 BB de plus)

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (17 BB de plus).
> Payer gagne entre 0,06 et 0,5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, QJo a 46,8 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : A5o (47,0 %), A6o (47,4 %), KTo (47,6 %) ; se couchent déjà : A4o (46,0 %), JTs (45,9 %), K8s (45,8 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 13 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Payer le tapis (17 BB de plus).
> Ton choix (fold) perd entre 0,06 et 0,5 BB.
> Cote du pot : 17 BB à payer pour un pot final de 36,5 BB, il faut 46,6 % d'équité pour payer.
> Contre sa range, QJo a 46,8 % d'équité : marge de 0,2 point au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 46,6 %, à 2 points près), paient encore : A5o (47,0 %), A6o (47,4 %), KTo (47,6 %) ; se couchent déjà : A4o (46,0 %), JTs (45,9 %), K8s (45,8 %).
> Contre ce profil, on paie avec 23 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 13 %.
> À l'équilibre push/fold, ce serait fold.
> Sa range de tapis est nettement plus faible : payer beaucoup plus large qu'à l'équilibre.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q271 · GTO · 3-handed · SB face à un tapis · 15 BB · 66

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (10 BB).
Le BTN paie le tapis.
Tu es au SB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.716 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.632 | 0 % | 0.084 | imprécision |
| Tapis (15 BB) | +3.715 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 3,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à un tapis à 15 BB, on part à tapis avec 55+, A9s+, KTs+, KJo+ (environ 34 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.


## Q272 · GTO · 3-handed · BB face à un tapis · 16 BB · A3o

Type : décision nette · EV : HRC · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 16 / 16 / 16 BB (BTN / SB / BB).
Le BTN limpe.
Le SB complète.
Tu relances à 5,5 BB.
Le BTN paie 5,5 BB.
Le SB part à tapis (16 BB).
Tu es au BB avec A♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.286 | erreur |
| Payer le tapis (10,5 BB de plus) | +2.286 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (10,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (10,5 BB de plus), +2,29 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 85 % des mains qui arrivent à cette décision ; A3o en fait partie.
> Repère : il faut environ 28 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : K7s, J9s, K5s, T5s, JTo.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (10,5 BB de plus), +2,29 BB par rapport au fold.
> Ton choix (fold) rapporte 2,29 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 16 BB, on paie avec 22+, A2+, K5s+, KJo+, Q5s+, QTo+, J9s+, T5s+, T8o+, 65s (environ 93 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on paie avec 85 % des mains qui arrivent à cette décision ; A3o en fait partie.
> Repère : il faut environ 28 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : K7s, J9s, K5s, T5s, JTo.


## Q273 · GTO · 3-handed · SB face à une relance · 15 BB · J9s

Type : décision nette · EV : HRC · tapis BTN 35 / SB 15 / BB 25 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 35 / 15 / 25 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB relance à 9,9 BB.
Le BTN paie 9,89 BB.
Tu es au SB avec J♠9♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.980 | erreur |
| Payer (7,59 BB de plus) | +0.439 | 0 % | 2.541 | erreur |
| Tapis (15 BB) | +2.980 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +2,98 BB par rapport au fold.
> Ton tapis met la pression maximale : tout le monde se couche environ 4 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 50 % des mains qui arrivent à cette décision ; J9s en fait partie.
> Autre option : payer (7,59 BB de plus), 2,54 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : K7s, 76s, A5o, 86s, 65s.

**Correction affichée si le joueur joue « Payer (7,59 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +2,98 BB par rapport au fold.
> Ton choix « payer (7,59 BB de plus) » rapporte 2,54 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 4 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à une relance à 15 BB, on part à tapis avec environ 52 % des mains qui arrivent ici.
> Ici, on part à tapis avec 50 % des mains qui arrivent à cette décision ; J9s en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : K7s, 76s, A5o, 86s, 65s.


## Q274 · GTO · 3-handed · BTN face à un tapis · 12 BB · JTo

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Tu limpes.
Le SB complète.
Le BB part à tapis (12 BB).
Tu es au BTN avec J♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -0.743 | 0 % | 0.743 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 72 % des mains qui arrivent à cette décision ; JTo en fait partie.
> Repère : il faut environ 44 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (11 BB de plus), 0,74 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : Q9s, A3s, JTs, 97s.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (11 BB de plus) » rapporte 0,74 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BTN face à un tapis à 12 BB, on ne joue que 88+, A8s+, KQs, Q9s+, JTs (environ 27 % des mains qui arrivent ici).
> Ici, on se couche avec 72 % des mains qui arrivent à cette décision ; JTo en fait partie.
> Repère : il faut environ 44 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : Q9s, A3s, JTs, 97s.


## Q275 · GTO · heads-up · SB premier à parler · 8 BB · K6s

Type : stratégie mixte · EV : HRC · tapis SB 8 / BB 8 · arbre 100650d1

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec K♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.778 | erreur |
| Compléter (0,5 BB de plus) | +0.770 | 15 % | 0.008 | correct |
| Relancer à 2 BB | +0.706 | 0 % | 0.073 | imprécision |
| Tapis (8 BB) | +0.778 | 85 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (8 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Nuance : relancer à 2 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : l'adversaire se couche environ 56 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 44 % des mains qui arrivent à cette décision ; K6s en fait partie.
> K6s est jouée de plusieurs façons (compléter (0,5 BB de plus) 15 %, tapis (8 BB) 85 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : A5s, KTs, 63s, 55, Q5o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (8 BB) ou compléter (0,5 BB de plus) (moins de 0,02 BB d'écart).
> Nuance : relancer à 2 BB est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 0,78 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : l'adversaire se couche environ 56 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB premier à parler à 8 BB (heads-up), on part à tapis avec environ 45 % des mains qui arrivent ici.
> Ici, on part à tapis avec 44 % des mains qui arrivent à cette décision ; K6s en fait partie.
> K6s est jouée de plusieurs façons (compléter (0,5 BB de plus) 15 %, tapis (8 BB) 85 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : A5s, KTs, 63s, 55, Q5o.


## Q276 · GTO · heads-up · SB premier à parler · 10 BB · JJ

Type : décision nette · EV : HRC · tapis SB 40 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec J♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.139 | erreur |
| Compléter (0,5 BB de plus) | +3.139 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +2.561 | 0 % | 0.578 | erreur |
| Tapis (10 BB) | +2.456 | 0 % | 0.683 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +3,14 BB par rapport au fold.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> Ici, on complète avec 56 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Autre option : relancer à 3,5 BB, 0,58 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : Q6s, T8s, 84o, J8s, KTo.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +3,14 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,58 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> À retenir : au SB premier à parler à 10 BB (heads-up), on complète avec environ 59 % des mains qui arrivent ici.
> Ici, on complète avec 56 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Autre option : tapis (10 BB), 0,68 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : Q6s, T8s, 84o, J8s, KTo.


## Q277 · GTO · heads-up · SB premier à parler · 20 BB · AQo

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 30 / BB 20 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 30 / 20 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec A♠Q♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.026 | erreur |
| Compléter (0,5 BB de plus) | +1.995 | 0 % | 0.031 | imprécision |
| Relancer à 3,5 BB | +2.027 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 3,5 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 3,5 BB, +2,03 BB par rapport au fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 53 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 23 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3,5 BB » : 52s, Q4o, A6o, Q6o, A8o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Relancer à 3,5 BB, +2,03 BB par rapport au fold.
> Nuance : compléter (0,5 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 2,03 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : l'adversaire se couche environ 53 % du temps, et sinon tu gardes l'initiative.
> À retenir : au SB premier à parler à 20 BB (heads-up), on relance avec environ 19 % des mains qui arrivent ici.
> Ici, on relance avec 23 % des mains qui arrivent à cette décision ; AQo en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 3,5 BB » : 52s, Q4o, A6o, Q6o, A8o.


## Q278 · GTO · 3-handed · BB face à un tapis · 15 BB · 77

Type : décision nette · EV : HRC · tapis BTN 25 / SB 35 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 25 / 35 / 15 BB (BTN / SB / BB).
Le BTN limpe.
Le SB se couche.
Tu relances à 4,5 BB.
Le BTN part à tapis (25 BB, soit 15 BB effectifs).
Tu es au BB avec 7♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 5.856 | erreur |
| Payer le tapis (10,5 BB de plus) | +5.856 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (10,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (10,5 BB de plus), +5,86 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 87 % des mains qui arrivent à cette décision ; 77 en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : 63s, A6o, JTo, K3s, K8s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (10,5 BB de plus), +5,86 BB par rapport au fold.
> Ton choix (fold) rapporte 5,86 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 15 BB, on paie avec environ 91 % des mains qui arrivent ici.
> Ici, on paie avec 87 % des mains qui arrivent à cette décision ; 77 en fait partie.
> Repère : il faut 34 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (10,5 BB de plus) » : 63s, A6o, JTo, K3s, K8s.


## Q279 · GTO · heads-up · SB premier à parler · 8 BB · ATs

Type : stratégie mixte · EV : HRC · tapis SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Personne n'a encore parlé.
Tu es au SB avec A♠T♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 1.854 | erreur |
| Compléter (0,5 BB de plus) | +1.854 | 80 % | 0.000 | correct |
| Tapis (8 BB) | +1.806 | 20 % | 0.049 | correct |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +1,85 BB par rapport au fold.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> Ici, on complète avec 33 % des mains qui arrivent à cette décision ; ATs en fait partie.
> ATs est jouée de plusieurs façons (compléter (0,5 BB de plus) 80 %, tapis (8 BB) 20 %) : ces actions ont une valeur proche, chacune est acceptée.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 76o, KTs, 43s, 82s, Q5o.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +1,85 BB par rapport au fold.
> Ton choix (fold) rapporte 1,85 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère.
> À retenir : au SB premier à parler à 8 BB (heads-up), on complète avec environ 32 % des mains qui arrivent ici.
> Ici, on complète avec 33 % des mains qui arrivent à cette décision ; ATs en fait partie.
> ATs est jouée de plusieurs façons (compléter (0,5 BB de plus) 80 %, tapis (8 BB) 20 %) : ces actions ont une valeur proche. Ton choix (fold) n'en fait pas partie.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : 76o, KTs, 43s, 82s, Q5o.


## Q280 · GTO · 3-handed · SB face à une relance · 25 BB · J7o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 25 / BB 35 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 25 / 35 BB (BTN / SB / BB).
Le BTN se couche.
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec J♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.096 | 0 % | 0.096 | imprécision |
| Relancer à 7,8 BB | -0.523 | 0 % | 0.523 | erreur |
| Tapis (25 BB) | -1.130 | 0 % | 1.130 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 37 % des mains qui arrivent à cette décision ; J7o en fait partie.
> Autre option : relancer à 7,8 BB, 0,52 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 64s, 86o, Q8o, T4s, 63s.

**Correction affichée si le joueur joue « Relancer à 7,8 BB » (erreur la plus tentante)**

> Action de référence : Fold.
> Nuance : payer (2 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (relancer à 7,8 BB) rapporte 0,52 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 25 BB, on se couche avec environ 37 % des mains qui arrivent ici.
> Ici, on se couche avec 37 % des mains qui arrivent à cette décision ; J7o en fait partie.
> Autre option : tapis (25 BB), 1,13 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 64s, 86o, Q8o, T4s, 63s.


## Q281 · GTO · heads-up · SB face à un tapis · 12 BB · K6s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 12 / 12 BB (SB / BB).
Tu relances à 3,5 BB.
Le BB part à tapis (12 BB).
Tu es au SB avec K♠6♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.925 | erreur |
| Payer le tapis (8,5 BB de plus) | +0.925 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (8,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (8,5 BB de plus), +0,92 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Cote du pot : 8,5 BB à payer pour un pot final de 24 BB, il faut 35,4 % d'équité pour payer.
> Contre sa range de tapis, K6s a 39,3 % d'équité : marge de 3,9 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,92 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 35,4 %, à 2 points près), paient encore : Q8o (35,43 %), T5s (35,6 %), J4s (35,6 %) ; se couchent déjà : 84s (35,3 %), T4s (35,2 %), K5o (35,0 %).
> Ici, on paie avec 99 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (8,5 BB de plus), +0,92 BB par rapport au fold.
> Ton choix (fold) rapporte 0,92 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 12 BB (heads-up), on paie avec environ 100 % des mains qui arrivent ici.
> Cote du pot : 8,5 BB à payer pour un pot final de 24 BB, il faut 35,4 % d'équité pour payer.
> Contre sa range de tapis, K6s a 39,3 % d'équité : marge de 3,9 points au-dessus du seuil.
> Décision serrée (moins de 5 points d'équité, soit environ 0,92 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 35,4 %, à 2 points près), paient encore : Q8o (35,43 %), T5s (35,6 %), J4s (35,6 %) ; se couchent déjà : 84s (35,3 %), T4s (35,2 %), K5o (35,0 %).
> Ici, on paie avec 99 % des mains qui arrivent à cette décision.


## Q282 · GTO · 3-handed · SB face à un tapis · 8 BB · A7o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 8 / 8 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Tu es au SB avec A♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.731 | erreur |
| Payer le tapis (3,5 BB de plus) | +0.713 | 0 % | 0.018 | correct |
| Tapis (8 BB) | +0.731 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (8 BB)

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : tapis (8 BB) ou payer le tapis (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> Ici, on part à tapis avec 24 % des mains qui arrivent à cette décision ; A7o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K4s, Q8s, A2o, ATs, JTo.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Plusieurs bonnes décisions : tapis (8 BB) ou payer le tapis (3,5 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix (fold) rapporte 0,73 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus.
> À retenir : au SB face à un tapis à 8 BB, on part à tapis avec 22+, A8s+, A3o+, K8+, QJs, QTo+, JTo (environ 26 % des mains qui arrivent ici ; règle simplifiée, exacte pour 95 % d'entre elles).
> Ici, on part à tapis avec 24 % des mains qui arrivent à cette décision ; A7o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « tapis (8 BB) » : K4s, Q8s, A2o, ATs, JTo.


## Q283 · GTO · heads-up · BB face à une relance · 6 BB · 42o

Type : décision nette · EV : HRC · tapis SB 6 / BB 6 · arbre 100650d1

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Le SB relance à 2 BB.
Tu es au BB avec 4♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1 BB de plus) | -0.359 | 0 % | 0.359 | erreur |
| Tapis (6 BB) | -1.786 | 0 % | 1.786 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 31 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Autre option : payer (1 BB de plus), 0,36 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 72s, J3o, T3s, 74s, 84s.

**Correction affichée si le joueur joue « Payer (1 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1 BB de plus) » rapporte 0,36 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 6 BB (heads-up), on se couche avec environ 32 % des mains qui arrivent ici.
> Ici, on se couche avec 31 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Autre option : tapis (6 BB), 1,79 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 72s, J3o, T3s, 74s, 84s.


## Q284 · GTO · heads-up · SB face à une relance · 10 BB · 54o

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis SB 40 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Tu complètes.
Le BB relance à 3 BB.
Tu es au SB avec 5♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (2 BB de plus) | -0.011 | 0 % | 0.011 | correct |
| Tapis (10 BB) | -0.569 | 0 % | 0.569 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Plusieurs bonnes décisions : fold ou payer (2 BB de plus) (moins de 0,02 BB d'écart).
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Autre option : tapis (10 BB), 0,57 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 93s, 43s, Q7o, J2s, T2s.

**Correction affichée si le joueur joue « Tapis (10 BB) » (erreur la plus tentante)**

> Plusieurs bonnes décisions : fold ou payer (2 BB de plus) (moins de 0,02 BB d'écart).
> Ton choix « tapis (10 BB) » rapporte 0,57 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 10 BB (heads-up), on se couche avec environ 52 % des mains qui arrivent ici.
> Ici, on se couche avec 50 % des mains qui arrivent à cette décision ; 54o en fait partie.
> Mains jouées en partie seulement pour l'action « fold » : 93s, 43s, Q7o, J2s, T2s.


## Q285 · exploitant · 3-handed · SB premier à parler · 8 BB · 94o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

Profil adverse (fictif) : Station d'appel (Fish) : part à tapis avec 62,2 % de ses mains (équilibre push/fold : 45,1 %)

**Énoncé** : 3 joueurs, tapis 8 / 8 / 8 BB (BTN / SB / BB).
Le BTN se couche.
Profil fictif « Station d'appel (Fish) » : ce BB paie un tapis avec 62,2 % de ses mains dans cette situation (équilibre push/fold : 45,1 %).
Tu joues en tapis ou fold.
Tu es au SB avec 9♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Tapis (8 BB) | -0.850 | 0 % | 0.850 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Partir à tapis perdrait entre 0,5 et 1 BB.
> Il se couche 37 % du temps face à ton tapis (équilibre push/fold : 54 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 94o a 33,0 % d'équité contre sa range de call (équilibre push/fold : 31,5 %) et tout se joue à tapis (8 BB effectifs).
> Contre ce profil, on part à tapis avec 50 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 61 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Tapis (8 BB) » (erreur la plus tentante)**

> Contre ce type de profil « Station d'appel (Fish) » : Fold.
> Ton choix « tapis (8 BB) » perd entre 0,5 et 1 BB.
> Il se couche 37 % du temps face à ton tapis (équilibre push/fold : 54 %) : tu gagnes alors sa blinde (1 BB).
> Quand il paie, 94o a 33,0 % d'équité contre sa range de call (équilibre push/fold : 31,5 %) et tout se joue à tapis (8 BB effectifs).
> Contre ce profil, on part à tapis avec 50 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 61 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q286 · GTO · heads-up · BB face à un tapis · 10 BB · T2o

Type : décision nette · EV : HRC · tapis SB 40 / BB 10 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 40 / 10 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (40 BB, soit 10 BB effectifs).
Tu es au BB avec T♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (7 BB de plus) | -0.910 | 0 % | 0.910 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 34 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Autre option : payer le tapis (7 BB de plus), 0,91 BB de moins.
> Aucune main n'est jouée en partie seulement pour l'action « fold » : la frontière est nette.

**Correction affichée si le joueur joue « Payer le tapis (7 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (7 BB de plus) » rapporte 0,91 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 10 BB (heads-up), on se couche avec environ 33 % des mains qui arrivent ici.
> Ici, on se couche avec 34 % des mains qui arrivent à cette décision ; T2o en fait partie.
> Repère : il faut 35 % d'équité pour payer (cote du pot).
> Aucune main n'est jouée en partie seulement pour l'action « fold » : la frontière est nette.


## Q287 · GTO · 3-handed · SB face à un tapis · 14 BB · KJo

Type : décision nette · EV : HRC · tapis BTN 14 / SB 14 / BB 14 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 14 / 14 / 14 BB (BTN / SB / BB).
Le BTN limpe.
Tu relances à 4,3 BB.
Le BB paie 4,3 BB.
Le BTN part à tapis (14 BB).
Tu es au SB avec K♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.094 | erreur |
| Payer le tapis (9,7 BB de plus) | +3.094 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (9,7 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (9,7 BB de plus), +3,09 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 94 % des mains qui arrivent à cette décision ; KJo en fait partie.
> Repère : il faut environ 30 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (9,7 BB de plus) » : K3s, A2s, T9s, K8s, A7s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (9,7 BB de plus), +3,09 BB par rapport au fold.
> Ton choix (fold) rapporte 3,09 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au SB face à un tapis à 14 BB, on paie avec 44+, A3s+, A2o+, K2s+, KTo+, Q2s+, QTo+, J8s+, JTo, T9s (environ 96 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on paie avec 94 % des mains qui arrivent à cette décision ; KJo en fait partie.
> Repère : il faut environ 30 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « payer le tapis (9,7 BB de plus) » : K3s, A2s, T9s, K8s, A7s.


## Q288 · GTO · 3-handed · SB premier à parler · 12 BB · KK

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 18 BB (BTN / SB / BB).
Le BTN se couche.
Tu es au SB avec K♠K♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.495 | erreur |
| Compléter (0,5 BB de plus) | +3.496 | 100 % | 0.000 | correct |
| Relancer à 3,5 BB | +3.216 | 0 % | 0.279 | erreur |
| Tapis (12 BB) | +3.021 | 0 % | 0.474 | erreur |

**Référence de l'application** : Compléter (0,5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Compléter (0,5 BB de plus), +3,5 BB par rapport au fold.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> Ici, on complète avec 31 % des mains qui arrivent à cette décision ; KK en fait partie.
> Autre option : relancer à 3,5 BB, 0,28 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K4s, 88, T9s, K2o, T5s.

**Correction affichée si le joueur joue « Relancer à 3,5 BB » (erreur la plus tentante)**

> Action de référence : Compléter (0,5 BB de plus), +3,5 BB par rapport au fold.
> Ton choix (relancer à 3,5 BB) rapporte 0,28 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes.
> À retenir : au SB premier à parler à 12 BB, on complète avec environ 30 % des mains qui arrivent ici.
> Ici, on complète avec 31 % des mains qui arrivent à cette décision ; KK en fait partie.
> Autre option : tapis (12 BB), 0,47 BB de moins.
> Mains jouées en partie seulement pour l'action « compléter (0,5 BB de plus) » : K4s, 88, T9s, K2o, T5s.


## Q289 · exploitant · 3-handed · BB face à un tapis · 10 BB · 74o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 10 / SB 10 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 49 % de ses mains (équilibre push/fold : 32,5 %)

**Énoncé** : 3 joueurs, tapis 10 / 10 / 10 BB (BTN / SB / BB).
Le BTN part à tapis (10 BB).
Le SB se couche.
Profil fictif « Maniaque (Maniac) » : ce BTN part à tapis avec 49 % de ses mains dans cette situation (équilibre push/fold : 32,5 %).
Tu es au BB avec 7♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -2.196 | 0 % | 2.196 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 2 et 5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range, 74o a 33,2 % d'équité : 10,7 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : c'est une décision de principe, à prendre sans hésiter.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : Q6s (44,0 %), K6o (44,2 %), J8s (44,3 %) ; se couchent déjà : J9o (43,5 %), K5o (43,5 %), Q8o (43,4 %).
> Contre ce profil, on paie avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 24 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (9 BB de plus) » perd entre 2 et 5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20,5 BB, il faut 43,9 % d'équité pour payer.
> Contre sa range, 74o a 33,2 % d'équité : 10,7 points sous le seuil.
> Écart large (plus de 10 points, soit entre 2 et 5 BB sur ce pot) : erreur nette, il fallait te coucher sans hésiter, la main est loin du seuil.
> À la limite (seuil 43,9 %, à 2 points près), paient encore : Q6s (44,0 %), K6o (44,2 %), J8s (44,3 %) ; se couchent déjà : J9o (43,5 %), K5o (43,5 %), Q8o (43,4 %).
> Contre ce profil, on paie avec 37 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 24 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.


## Q290 · GTO · 3-handed · BB face à une relance · 6 BB · 64o

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB se couche.
Tu es au BB avec 6♠4♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,3 BB de plus) | -0.242 | 0 % | 0.242 | erreur |
| Tapis (6 BB) | -1.231 | 0 % | 1.231 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 51 % des mains qui arrivent à cette décision ; 64o en fait partie.
> Autre option : payer (1,3 BB de plus), 0,24 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 52s, J2s, 72s, 75s, 87s.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 0,24 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 6 BB, on se couche avec environ 51 % des mains qui arrivent ici.
> Ici, on se couche avec 51 % des mains qui arrivent à cette décision ; 64o en fait partie.
> Autre option : tapis (6 BB), 1,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : 52s, J2s, 72s, 75s, 87s.


## Q291 · GTO · 3-handed · BTN premier à parler · 20 BB · TT

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 20 / 20 / 20 BB (BTN / SB / BB).
Personne n'a encore parlé.
Tu es au BTN avec T♠T♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 2.676 | erreur |
| Limper (1 BB) | +2.586 | 0 % | 0.090 | imprécision |
| Relancer à 2,3 BB | +2.676 | 100 % | 0.000 | correct |

**Référence de l'application** : Relancer à 2,3 BB

**Correction affichée si le joueur joue la référence**

> Action de référence : Relancer à 2,3 BB, +2,68 BB par rapport au fold.
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 34 % du temps, et sinon tu gardes l'initiative.
> Ici, on relance avec 25 % des mains qui arrivent à cette décision ; TT en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 2,3 BB » : 66, A3o, A5s, K4s, A2s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Relancer à 2,3 BB, +2,68 BB par rapport au fold.
> Nuance : limper (1 BB) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 2,68 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Relancer construit le pot avec une main qui joue bien : tout le monde se couche environ 34 % du temps, et sinon tu gardes l'initiative.
> À retenir : au BTN premier à parler à 20 BB, on relance avec 77+, A7s+, A4o+, KQs, K9o+, Q8s+, Q9o+, J9o+, T8s+, 98s (environ 27 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on relance avec 25 % des mains qui arrivent à cette décision ; TT en fait partie.
> Mains jouées en partie seulement pour l'action « relancer à 2,3 BB » : 66, A3o, A5s, K4s, A2s.


## Q292 · GTO · 3-handed · BB face à une relance · 15 BB · J5s

Type : décision nette · EV : HRC · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 40 / 20 / 15 BB (BTN / SB / BB).
Le BTN limpe.
Le SB relance à 4,5 BB.
Tu es au BB avec J♠5♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (3,5 BB de plus) | -1.660 | 0 % | 1.660 | erreur |
| Tapis (15 BB) | -4.233 | 0 % | 4.233 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; J5s en fait partie.
> Autre option : payer (3,5 BB de plus), 1,66 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KQo, 33, J9s, A3s, 87s.

**Correction affichée si le joueur joue « Payer (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (3,5 BB de plus) » rapporte 1,66 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au BB face à une relance à 15 BB, on ne joue que 55+, A9s+, ATo+, KQo, QJs, 87s (environ 13 % des mains qui arrivent ici ; règle simplifiée, exacte pour 98 % d'entre elles).
> Ici, on se couche avec 86 % des mains qui arrivent à cette décision ; J5s en fait partie.
> Autre option : tapis (15 BB), 4,23 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : KQo, 33, J9s, A3s, 87s.


## Q293 · GTO · heads-up · BB face à un tapis · 8 BB · 99

Type : décision nette · EV : HRC · tapis SB 8 / BB 8 · arbre daa9aaa0

**Énoncé** : Heads-up, tapis 8 / 8 BB (SB / BB).
Le SB complète.
Tu relances à 3 BB.
Le SB part à tapis (8 BB).
Tu es au BB avec 9♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 4.447 | erreur |
| Payer le tapis (5 BB de plus) | +4.448 | 100 % | 0.000 | correct |

**Référence de l'application** : Payer le tapis (5 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer le tapis (5 BB de plus), +4,45 BB par rapport au fold.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> Ici, on paie avec 79 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : 97o, 84s, T7s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Payer le tapis (5 BB de plus), +4,45 BB par rapport au fold.
> Ton choix (fold) rapporte 4,45 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher.
> À retenir : au BB face à un tapis à 8 BB (heads-up), on paie avec environ 79 % des mains qui arrivent ici.
> Ici, on paie avec 79 % des mains qui arrivent à cette décision ; 99 en fait partie.
> Repère : il faut 31 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « payer le tapis (5 BB de plus) » : 97o, 84s, T7s.


## Q294 · GTO · 3-handed · BB face à une relance · 12 BB · JJ

Type : décision nette · EV : HRC · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 12 / 12 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Le SB paie 2,3 BB.
Tu es au BB avec J♠J♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 7.014 | erreur |
| Payer (1,3 BB de plus) | +3.334 | 0 % | 3.680 | erreur |
| Tapis (12 BB) | +7.014 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (12 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (12 BB), +7,01 BB par rapport au fold.
> Ton tapis met la pression maximale : tout le monde se couche environ 12 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 20 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Autre option : payer (1,3 BB de plus), 3,68 BB de moins.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : 87s, 44, 53s, A2o, 62s.

**Correction affichée si le joueur joue « Payer (1,3 BB de plus) » (erreur la plus tentante)**

> Action de référence : Tapis (12 BB), +7,01 BB par rapport au fold.
> Ton choix « payer (1,3 BB de plus) » rapporte 3,68 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 12 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au BB face à une relance à 12 BB, on part à tapis avec 33+, A2s+, ATo+, KTo+, QJs, 87s (environ 18 % des mains qui arrivent ici ; règle simplifiée, exacte pour 97 % d'entre elles).
> Ici, on part à tapis avec 20 % des mains qui arrivent à cette décision ; JJ en fait partie.
> Mains jouées en partie seulement pour l'action « tapis (12 BB) » : 87s, 44, 53s, A2o, 62s.


## Q295 · GTO · 3-handed · BB face à un tapis · 12 BB · 84s

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 12 / SB 18 / BB 12 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 12 / 18 / 12 BB (BTN / SB / BB).
Le BTN part à tapis (12 BB).
Le SB se couche.
Tu es au BB avec 8♠4♠. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (11 BB de plus) | -1.834 | 0 % | 1.833 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range de tapis, 84s a 37,4 % d'équité : 7,5 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,83 BB sur ce pot) : la décision est claire dès que tu estimes bien la range adverse.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : A2s (45,0 %), A6o (45,7 %), A3s (45,8 %) ; se couchent déjà : A5o (44,87 %), K9s (44,6 %), T9s (44,3 %).
> Ici, on paie avec 20 % des mains qui arrivent à cette décision.

**Correction affichée si le joueur joue « Payer le tapis (11 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (11 BB de plus) » rapporte 1,83 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au BB face à un tapis à 12 BB, on ne joue que 22+, A2s+, A6o+, KTs+, KJo+, QTs+, JTs (environ 20 % des mains qui arrivent ici).
> Cote du pot : 11 BB à payer pour un pot final de 24,5 BB, il faut 44,9 % d'équité pour payer.
> Contre sa range de tapis, 84s a 37,4 % d'équité : 7,5 points sous le seuil.
> Écart moyen (5 à 10 points, soit environ 1,83 BB sur ce pot) : il fallait te coucher ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse.
> À la limite (seuil 44,9 %, à 2 points près), paient encore : A2s (45,0 %), A6o (45,7 %), A3s (45,8 %) ; se couchent déjà : A5o (44,87 %), K9s (44,6 %), T9s (44,3 %).
> Ici, on paie avec 20 % des mains qui arrivent à cette décision.


## Q296 · GTO · heads-up · SB face à une relance · 6 BB · T9o

Type : décision nette · EV : HRC · tapis SB 6 / BB 6 · arbre 100650d1

**Énoncé** : Heads-up, tapis 6 / 6 BB (SB / BB).
Tu complètes.
Le BB relance à 2 BB.
Tu es au SB avec T♠9♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 0.514 | erreur |
| Payer (1 BB de plus) | +0.514 | 100 % | 0.000 | correct |
| Tapis (6 BB) | +0.258 | 0 % | 0.256 | erreur |

**Référence de l'application** : Payer (1 BB de plus)

**Correction affichée si le joueur joue la référence**

> Action de référence : Payer (1 BB de plus), +0,51 BB par rapport au fold.
> Payer 1 BB pour un pot de 4 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> Ici, on paie avec 68 % des mains qui arrivent à cette décision ; T9o en fait partie.
> Autre option : tapis (6 BB), 0,26 BB de moins.
> Mains jouées en partie seulement pour l'action « payer (1 BB de plus) » : 86o, J8s, 83s, 66, T5o.

**Correction affichée si le joueur joue « Tapis (6 BB) » (erreur la plus tentante)**

> Action de référence : Payer (1 BB de plus), +0,51 BB par rapport au fold.
> Ton choix « tapis (6 BB) » rapporte 0,26 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Payer 1 BB pour un pot de 4 BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant.
> À retenir : au SB face à une relance à 6 BB (heads-up), on paie avec environ 69 % des mains qui arrivent ici.
> Ici, on paie avec 68 % des mains qui arrivent à cette décision ; T9o en fait partie.
> Mains jouées en partie seulement pour l'action « payer (1 BB de plus) » : 86o, J8s, 83s, 66, T5o.


## Q297 · GTO · 3-handed · SB face à un tapis · 4 BB · 97o

Type : décision nette · EV : HRC · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 4 / 4 / 4 BB (BTN / SB / BB).
Le BTN part à tapis (4 BB).
Tu es au SB avec 9♠7♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (3,5 BB de plus) | -0.423 | 0 % | 0.423 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 97o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Autre option : payer le tapis (3,5 BB de plus), 0,42 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K7o, 76s, Q6s, J8s, K2s.

**Correction affichée si le joueur joue « Payer le tapis (3,5 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer le tapis (3,5 BB de plus) » rapporte 0,42 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme.
> À retenir : au SB face à un tapis à 4 BB, on ne joue que 22+, A2+, K2s+, K8o+, Q7s+, Q9o+, J8s+, JTo, T8s+, 98s, 87s (environ 35 % des mains qui arrivent ici).
> Ici, on se couche avec 64 % des mains qui arrivent à cette décision ; 97o en fait partie.
> Repère : il faut environ 39 % d'équité pour payer (cote du pot ; approximatif, car un joueur reste à parler).
> Mains jouées en partie seulement pour l'action « fold » : K7o, 76s, Q6s, J8s, K2s.


## Q298 · GTO · 3-handed · SB face à une relance · 6 BB · 42o

Type : décision nette · EV : HRC · tapis BTN 6 / SB 6 / BB 6 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 6 / 6 / 6 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu es au SB avec 4♠2♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer (1,8 BB de plus) | -1.063 | 0 % | 1.063 | erreur |
| Tapis (6 BB) | -2.068 | 0 % | 2.068 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Action de référence : Fold.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Autre option : payer (1,8 BB de plus), 1,06 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K5s, J8s, JTo, Q8s, K4s.

**Correction affichée si le joueur joue « Payer (1,8 BB de plus) » (erreur la plus tentante)**

> Action de référence : Fold.
> Ton choix « payer (1,8 BB de plus) » rapporte 1,06 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage.
> À retenir : au SB face à une relance à 6 BB, on ne joue que 44+, A2+, K8s+, K9o+, Q8s+, QTo+, J9s+ (environ 29 % des mains qui arrivent ici ; règle simplifiée, exacte pour 99 % d'entre elles).
> Ici, on se couche avec 70 % des mains qui arrivent à cette décision ; 42o en fait partie.
> Autre option : tapis (6 BB), 2,07 BB de moins.
> Mains jouées en partie seulement pour l'action « fold » : K5s, J8s, JTo, Q8s, K4s.


## Q299 · GTO · 3-handed · SB face à un tapis · 15 BB · 66

Type : décision serrée (autre action à moins de 0,1 BB) · EV : HRC · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

**Énoncé** : 3 joueurs, tapis 15 / 50 / 10 BB (BTN / SB / BB).
Le BTN relance à 2,3 BB.
Tu paies 2,3 BB.
Le BB part à tapis (10 BB).
Le BTN paie le tapis.
Tu es au SB avec 6♠6♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 0 % | 3.716 | erreur |
| Payer le tapis (7,7 BB de plus) | +3.632 | 0 % | 0.084 | imprécision |
| Tapis (15 BB) | +3.715 | 100 % | 0.000 | correct |

**Référence de l'application** : Tapis (15 BB)

**Correction affichée si le joueur joue la référence**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.

**Correction affichée si le joueur joue « Fold » (erreur la plus tentante)**

> Action de référence : Tapis (15 BB), +3,72 BB par rapport au fold.
> Nuance : payer le tapis (7,7 BB de plus) est aussi pertinente (moins de 0,1 BB d'écart, dans la marge d'incertitude du calcul).
> Ton choix (fold) rapporte 3,72 BB de moins.
> Écart au-delà de 0,06 BB : erreur.
> Ton tapis met la pression maximale : tout le monde se couche environ 0 % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité.
> À retenir : au SB face à un tapis à 15 BB, on part à tapis avec 55+, A9s+, KTs+, KJo+ (environ 34 % des mains qui arrivent ici ; règle simplifiée, exacte pour 96 % d'entre elles).
> Ici, on part à tapis avec 39 % des mains qui arrivent à cette décision ; 66 en fait partie.
> Repère : il faut 26 % d'équité pour payer (cote du pot).
> Mains jouées en partie seulement pour l'action « tapis (15 BB) » : KJs, K5s, KTs, QJs, Q6s.


## Q300 · exploitant · 3-handed · BB face à un tapis · 10 BB · Q3o

Type : décision nette · EV : exacte (tout le monde à tapis) · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

Profil adverse (fictif) : Maniaque (Maniac) : part à tapis avec 73,6 % de ses mains (équilibre push/fold : 58,3 %)

**Énoncé** : 3 joueurs, tapis 20 / 45 / 10 BB (BTN / SB / BB).
Le BTN se couche.
Le SB part à tapis (45 BB, soit 10 BB effectifs).
Profil fictif « Maniaque (Maniac) » : ce SB part à tapis avec 73,6 % de ses mains dans cette situation (équilibre push/fold : 58,3 %).
Tu es au BB avec Q♠3♥. Que fais-tu ?

| Option | EV (BB) | Fréquence de référence | Écart (BB) | Verdict de l'application |
|---|---|---|---|---|
| Fold | +0.000 | 100 % | 0.000 | correct |
| Payer le tapis (9 BB de plus) | -0.431 | 0 % | 0.431 | erreur |

**Référence de l'application** : Fold

**Correction affichée si le joueur joue la référence**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Payer perdrait entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, Q3o a 42,8 % d'équité : 2,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : bien vu, mais un petit changement de range adverse ou de tapis peut la renverser.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

**Correction affichée si le joueur joue « Payer le tapis (9 BB de plus) » (erreur la plus tentante)**

> Contre ce type de profil « Maniaque (Maniac) » : Fold.
> Ton choix « payer le tapis (9 BB de plus) » perd entre 0,06 et 0,5 BB.
> Cote du pot : 9 BB à payer pour un pot final de 20 BB, il faut 45,0 % d'équité pour payer.
> Contre sa range, Q3o a 42,8 % d'équité : 2,2 points sous le seuil.
> Décision serrée (moins de 5 points d'équité, soit entre 0,06 et 0,5 BB sur ce pot) : retiens surtout le seuil d'équité, c'est lui qui tranche.
> À la limite (seuil 45,0 %, à 2 points près), paient encore : Q2s (45,3 %), J6s (45,5 %), Q6o (45,9 %) ; se couchent déjà : T8o (44,9 %), J5s (44,8 %), 97s (44,8 %).
> Contre ce profil, on paie avec 48 % des mains qui arrivent à cette décision ; contre un joueur équilibré en push/fold, avec 37 %.
> Même décision qu'à l'équilibre push/fold : l'écart de range ne suffit pas à la changer.
> Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.

