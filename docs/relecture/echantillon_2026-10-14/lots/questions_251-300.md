# SpinsAcademy : questions Q251 à Q300

Consignes : `CONSIGNES.md`.

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

