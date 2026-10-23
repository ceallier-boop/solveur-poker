# SpinsAcademy : questions Q151 à Q200

Consignes : `CONSIGNES.md`.

## Q151 · GTO · 3-handed · BB face à un tapis · 18 BB · K7o

Type : décision nette · EV : la référence · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 35 / SB 25 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 18 / SB 12 / BB 18 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis SB 8 / BB 8 · arbre 100650d1

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis SB 40 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 12 / BB 12 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 22 / BB 22 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 15 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 14 / SB 18 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 13f58826

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 18 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 50 / SB 15 / BB 10 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 14 / SB 14 / BB 14 · arbre 821ee345

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

Type : stratégie mixte · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 4 / SB 4 / BB 4 · arbre 821ee345

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 13f58826

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

Type : décision nette · EV : la référence · tapis BTN 18 / SB 18 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : stratégie mixte · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 279f59f1

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

Type : stratégie mixte · EV : la référence · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

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

Type : stratégie mixte · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 13f58826

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

Type : décision nette · EV : la référence · tapis SB 8 / BB 8 · arbre 100650d1

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

Type : décision nette · EV : la référence · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

