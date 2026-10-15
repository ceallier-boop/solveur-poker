# SpinsAcademy : questions Q101 à Q150

Consignes : `CONSIGNES.md`.

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

