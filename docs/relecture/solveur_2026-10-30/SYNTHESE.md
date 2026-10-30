# Relecture de l'échantillon du solveur par les trois coachs simulés (30/10/2026)

Échantillon : 60 situations de la banque pilote `gto_preflop/2026.10.29-s1` (39 désaccords entre notre solveur et la référence, 9 décisions serrées, 12 témoins), présentées à l'aveugle (calcul A / calcul B). Relecteurs : les skills Lucho, Lucky et PA, **simulés par l'IA**, l'un après l'autre. Réponses : `reponses_lucho.csv`, `reponses_lucky.csv`, `reponses_pa.csv` ; clé : `cle.csv`.

**À lire avec prudence.** Les trois avis viennent du même modèle, dans la même conversation : ils ne sont pas indépendants, et l'accord entre eux est surestimé. Leurs doctrines sont exploitantes (contre les récréatifs) alors que la consigne demandait l'équilibre ; certaines préférences (limper beaucoup en heads-up, ne jamais limper au BTN 3-way) pèsent sur les votes. Cette relecture sert à repérer des familles de situations à contrôler, pas à trancher. Une relecture par de vrais coachs reste nécessaire.

## Résultat global

| Mesure | Valeur |
|---|---|
| Désaccords donnés à la référence (au moins 2 coachs sur 3) | **21 sur 39** |
| Désaccords donnés à notre solveur | **16 sur 39** |
| Partagés | 2 |
| Témoins et décisions serrées | jugés « les deux » ou d'accord avec les deux calculs dans presque tous les cas |
| Accord entre coachs (kappa de Fleiss, 4 catégories) | 0,71 (surestimé, voir plus haut) |

| Coach | Pour le solveur | Pour la référence | Les deux / aucun |
|---|---|---|---|
| Lucho | 12 | 24 | 24 |
| Lucky | 18 | 18 | 24 |
| PA | 16 | 22 | 22 |

## Où notre solveur l'emporte (16)

- **BTN 3-way, ouverture plutôt que limp** (S004 A5s, S008 44, S039 A9s à 25 BB ; S019 K6s, S020 87s à 12 BB, en tapis) et AA en relance (S035) : la référence limpe beaucoup au BTN, les trois coachs non. Unanime sauf AA.
- **Tapis à 12 BB au SB contre le BB** (S014 Q8s, S041 76o, S052 Q5s) et contre le limp (S055 K8o, S023 88) : la référence limpe ou isole petit, les coachs préfèrent le tapis.
- **Iso avec des mains qui dominent le limp** (S010 K7o, S013 A3o).
- **Fold de Q8o et J8o face à l'open 3,5x en heads-up 25 BB** (S031, S032) : 2 coachs sur 3 (Lucho défend).

## Où la référence l'emporte (21)

1. **Le solveur folde trop face à l'iso après son limp en heads-up 25 BB** (S015 K5o, S037 Q8o, S048 K4o) : unanime, avec une cote de 25 % et la position. Écart d'EV important entre les deux calculs (le solveur donne au call −0,13 à −0,25 BB, la référence +0,11 à +0,22). Cohérent avec le défaut d'abstraction après le flop mesuré en G9 (mains spéculatives et moyennes sous-évaluées).
2. **Le solveur isole des mains faibles contre le limp** (S002 T9o, S006 96o, S009 J8o, S040 Q4o, S049 Q5o) et **n'isole pas KJo** (S026) : unanime. La composition de sa range d'iso paraît inversée par endroits, là aussi un effet probable de la valeur après le flop.
3. **Heads-up au SB : le solveur relance des mains faibles** (S043 94s, S050 83s) **et limpe ATs** (S046) : 2 à 3 coachs pour la référence.
4. **Heads-up 12 BB : le solveur part à tapis là où la référence limpe ou checke** (S007 54s, S051 98s, S060 Q6s au SB ; S054 98s, S059 85s au BB contre le limp). Attention : la préférence des coachs pour le limp en heads-up est une doctrine d'exploitation ; à vérifier par le calcul.
5. **Le solveur paie l'open du BTN au SB avec JTo** (S034) : unanime pour le fold (pas de flat hors de position avec le BB derrière).
6. **Le solveur folde 76o et K6o au BB face au min-raise du BTN** (S057, S058) : 2 coachs sur 3 pour la défense.
7. **KQo au BB contre le min-raise du BTN à 25 BB** : le solveur part à tapis à 98 % (S053) ; 2 coachs préfèrent call ou 3-bet non all-in.

## Ce qu'il faut en faire

- Les familles 1 et 2 (défense face à l'iso, composition de la range d'iso) concernent des pots qui vont au flop : elles sont à **remesurer après la correction du regroupement après le flop (G13)**, avec le calcul exact quand c'est possible. Si elles persistent, ce sont des défauts du solveur.
- Les familles 4 et 3 (limp contre tapis ou relance en heads-up) sont celles où la doctrine des coachs pèse le plus : à trancher par le calcul (exact à 8 BB et moins avec les exports `enumerated` de la v5), pas par les avis.
- Les points où le solveur l'emporte (pas de limp au BTN, tapis à 12 BB) concernent surtout l'arbre et la stratégie de la référence : rien à corriger chez nous.
- Relecture par de vrais coachs : reprendre le même échantillon après G13, pour mesurer les deux versions.
