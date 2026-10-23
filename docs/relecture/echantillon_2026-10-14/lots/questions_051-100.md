# SpinsAcademy : questions Q051 à Q100

Consignes : `CONSIGNES.md`.

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 12 / BB 12 · arbre 100650d1

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 25 / SB 25 / BB 25 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis SB 8 / BB 8 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 45 / SB 20 / BB 10 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 14 / SB 18 / BB 18 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 25 / BB 25 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 6 / BB 6 · arbre 100650d1

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

Type : décision nette · EV : la référence · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 18 / SB 12 / BB 12 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 15 / SB 25 / BB 35 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 25 / SB 25 / BB 25 · arbre 821ee345

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

Type : stratégie mixte · EV : la référence · tapis BTN 4 / SB 8 / BB 4 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 15 / SB 50 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

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

Type : stratégie mixte · EV : la référence · tapis BTN 10 / SB 20 / BB 45 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 40 / SB 20 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 50 / SB 15 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 12 / BB 12 · arbre 100650d1

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

Type : décision nette · EV : la référence · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis SB 35 / BB 15 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 14 / SB 14 / BB 14 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 4d2f96f7

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

