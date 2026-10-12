# Guide de comportement Expresso : stacks et profils adverses

Base : modèle push/fold à 3 joueurs en chip EV (gagnant prend tout), stacks égaux, sans ante. Les ranges exactes sont dans `ranges_3handed.md`. Les pourcentages ci-dessous sont des parts de mains (combos).

## 1. Selon la profondeur de stack (adversaires « équilibrés »)

| Stack | BTN push | SB open-shove (BTN fold) | SB call vs BTN | BB call vs SB | BB call vs BTN (SB fold) | BB call vs BTN+SB |
|---|---|---|---|---|---|---|
| 4 BB | 43 % | 74 % | 35 % | 73 % | 60 % | 51 % |
| 6 BB | 38 % | 68 % | 26 % | 54 % | 37 % | 25 % |
| 8 BB | 35 % | 62 % | 21 % | 44 % | 29 % | 14 % |
| 10 BB | 33 % | 58 % | 17 % | 37 % | 23 % | 12 % |
| 12 BB | 29 % | 52 % | 15 % | 33 % | 19 % | 9 % |
| 15 BB | 25 % | 46 % | 11 % | 27 % | 15 % | 6 % |

Règles de conduite :
- **Plus le stack baisse, plus on élargit** : chaque BB en moins ajoute environ 2 à 3 points de push au BTN et 3 à 4 points au SB.
- **Le SB est la position la plus agressive** : quand le BTN fold, il pousse 46 à 74 % de ses mains, car il ne reste qu'un adversaire.
- **Le BTN pousse nettement moins large que le SB** : il laisse deux joueurs derrière lui.
- **Contre un push, call plus serré qu'en heads-up** : à 10 BB, le BB call 37 % contre le SB, mais 23 % contre le BTN, et 12 % si un deuxième joueur est déjà all-in.
- **Face à deux all-in, ne call qu'avec de vraies mains** : à 10 BB, 44+, A9s+, KJs+, QTs+, JTs, ATo+.
- **Au-delà de 12 à 15 BB**, le push/fold pur sort du cadre du modèle : les raises de taille normale existent et ne sont pas modélisées.

## 2. Selon le profil de l'adversaire

On modélise un profil en changeant la largeur de son range par rapport à l'équilibre : « appelle ×0,6 » signifie qu'il call 40 % de mains en moins que l'équilibre. Ses mains retirées sont les plus faibles du range d'équilibre.

### Quand tu pousses : adversaires qui appellent plus ou moins que l'équilibre

| Stack | Équilibre BTN / SB | Adversaires nits (appellent ×0,6) | Adversaires larges (appellent ×1,5) |
|---|---|---|---|
| 6 BB | 38 % / 68 % | 100 % / 100 % | 31 % / 60 % |
| 8 BB | 35 % / 62 % | 100 % / 100 % | 29 % / 49 % |
| 10 BB | 33 % / 58 % | 100 % / 100 % | 24 % / 44 % |
| 12 BB | 29 % / 52 % | 100 % / 100 % | 22 % / 37 % |
| 15 BB | 25 % / 46 % | 100 % / 100 % | 18 % / 32 % |

- **Contre des nits** : pousse toutes tes mains au BTN et au SB (si les adversaires derrière appellent vraiment ×0,6). Le gain est d'environ 0,16 BB par fois que tu es dans le spot, sur tous les stacks testés.
- **Contre des adversaires qui appellent trop** : resserre (par exemple à 10 BB, BTN 33 → 24 %, SB 58 → 44 %) et pousse davantage pour la valeur. Le gain à exploiter va de 0,02 à 0,09 BB par spot.
- Un adversaire qui appelle ×2 donne des ranges comparables à ×1,5, avec un gain plus élevé (jusqu'à 0,09 à 0,10 BB par spot pour le SB à 12 et 15 BB).

### Quand tu appelles : adversaires qui poussent plus ou moins que l'équilibre

Part de mains à appeler, à 10 BB (équilibre entre parenthèses) :

| Situation | Adversaire serré (pousse ×0,6) | Équilibre | Adversaire large (pousse ×1,4) |
|---|---|---|---|
| BB face au SB | 22 % | 37 % | 52 % |
| BB face au BTN (SB fold) | 13 % | 23 % | 31 % |
| SB face au BTN | 10 % | 17 % | 27 % |

- **Contre un maniaque** (pousse beaucoup) : élargis tes calls d'environ 40 %. À 6 BB, le BB appelle jusqu'à 73 % de ses mains face à un SB qui pousse ×1,4.
- **Contre un joueur serré** : resserre d'environ 40 %. À 15 BB, le BB appelle 14 % face à un SB serré, contre 27 % à l'équilibre.

### Comment identifier le profil (règles de terrain, pas issues du modèle)

- **Nit** : fold presque toujours face à un push, ne défend pas ses blinds, ne pousse qu'avec de très bonnes mains.
- **Joueur qui appelle trop** : call des shoves avec des mains marginales (Kx, Qx offsuit), voit beaucoup de flops.
- **Maniac** : pousse presque toutes ses mains en position tardive.
- Il faut quelques mains d'observation avant de dévier : tant que tu n'as pas de lecture, reste à l'équilibre.

## 3. Limites

- Modèle chip EV à stacks égaux, sans ante : en pratique, les stacks deviennent vite inégaux, ce qui change les ranges.
- Les profils sont stylisés (range d'équilibre tronquée ou élargie), pas des joueurs réels.
- Les gains sont calculés par fois que le spot se présente, pas par main jouée.
- Ces chiffres n'ont pas été comparés à un solveur externe.
