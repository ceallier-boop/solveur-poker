# SpinsAcademy : questions Q001 à Q050

Consignes : `CONSIGNES.md`.

## Q001 · GTO · heads-up · BB face à un limp · 10 BB · A9o

Type : décision nette · EV : la référence · tapis SB 10 / BB 10 · arbre 100650d1

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 279f59f1

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

Type : décision nette · EV : la référence · tapis BTN 45 / SB 20 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 279f59f1

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis SB 18 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 20 / BB 30 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 35 / SB 15 / BB 25 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 4d2f96f7

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

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

Type : stratégie mixte · EV : la référence · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 35 / SB 15 / BB 25 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 22 / SB 22 / BB 22 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 22 / BB 22 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis SB 6 / BB 6 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 4 / BB 8 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 279f59f1

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 10 / SB 10 / BB 10 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 10 / SB 20 / BB 45 · arbre daa9aaa0

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

