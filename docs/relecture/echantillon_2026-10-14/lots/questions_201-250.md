# SpinsAcademy : questions Q201 à Q250

Consignes : `CONSIGNES.md`.

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 12 / SB 12 / BB 12 · arbre 4d2f96f7

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 18 / SB 18 / BB 18 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 10 / SB 10 / BB 10 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis SB 22 / BB 22 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 40 / BB 15 · arbre daa9aaa0

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


## Q213 · GTO · 3-handed · BB face à un tapis · 10 BB · J5o

Type : décision nette · EV : la référence · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 30 / BB 25 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 4 / SB 8 / BB 8 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 15 / SB 20 / BB 40 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 4d2f96f7

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

Type : stratégie mixte · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 279f59f1

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

Type : décision nette · EV : la référence · tapis SB 30 / BB 20 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 14 / SB 14 / BB 14 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 35 / SB 25 / BB 15 · arbre daa9aaa0

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

Type : décision serrée (autre action à moins de 0,1 BB) · EV : la référence · tapis BTN 20 / SB 45 / BB 10 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 14 / BB 14 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 15 / SB 15 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 8 / SB 8 / BB 4 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 22 / BB 22 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis SB 22 / BB 22 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 8 / SB 4 / BB 8 · arbre daa9aaa0

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

Type : stratégie mixte · EV : la référence · tapis BTN 6 / SB 6 / BB 6 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 821ee345

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

Type : décision nette · EV : la référence · tapis SB 20 / BB 30 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 25 / SB 35 / BB 15 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 4 / SB 4 / BB 4 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre 4d2f96f7

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

Type : décision nette · EV : la référence · tapis BTN 20 / SB 20 / BB 20 · arbre daa9aaa0

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

Type : décision nette · EV : la référence · tapis BTN 16 / SB 16 / BB 16 · arbre 13f58826

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

