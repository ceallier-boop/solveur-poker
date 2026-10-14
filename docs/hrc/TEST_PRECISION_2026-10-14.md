# Test de précision HRC (14 octobre 2026)

Exports reçus : `Test_HRC_v1.zip`, rangés dans `data/hrc/tests/precision_v1/` (hors de `data/hrc/raw` : jamais importés dans un dataset). Mesures : `python tools/hrc/precision_test.py data/hrc/tests/precision_v1`.

## Ce qui a été reçu

| Mains | Table | Tapis | Nœuds | Arbre |
|---|---|---|---|---|
| `hand_1` à `hand_4` | heads-up | 12 / 12 | 8 | `16c57008` |
| `hand_5` à `hand_8` | 3 joueurs | 12 / 12 / 12 | 22 | `16c57008` |

- Les quatre exports de chaque groupe ont des `settings.json` **strictement identiques** : le nombre d'itérations (ou la précision demandée) n'est pas enregistré dans l'export. On ne peut donc pas savoir, d'après les fichiers, lequel a tourné le plus longtemps.
- **L'arbre n'est pas celui de référence.** Seule différence avec `v3/hand_13` et `v3/hand_3` : `ALLOWED_FLATS_PER_RAISE` vaut `[0, 1, 1, 1, 0]` au lieu de `[1, 1, 1, 1, 0]`. Le limp en premier de parole est interdit (22 nœuds à 3 joueurs au lieu de 44) ; le SB peut toujours compléter en heads-up.

## Résultats (mains atteintes à 5 % au moins, pire action, sur les nœuds où l'EV exacte existe)

| | Heads-up 12 BB | 3 joueurs 12 BB |
|---|---|---|
| Base v3 actuelle (une main) | médiane 104 mBB, 90e centile 274 | médiane 116 mBB, 90e centile 304 |
| Chaque export du test | médiane 92 à 103 mBB | médiane 101 à 118 mBB |
| Moyenne de 2 exports | médiane 60, 90e centile 187 | médiane 83, 90e centile 196 |
| Moyenne de 4 exports | **médiane 42, 90e centile 122** | **médiane 66, 90e centile 154** |
| Dispersion des EV entre les 4 exports | médiane 97 mBB | médiane 143 mBB |
| Dispersion des fréquences entre les 4 exports | médiane 1,7 point (90e centile 25) | médiane 1,0 point (90e centile 25) |
| Biais moyen HRC − exact (nœud de call de tapis) | +3,5 mBB | −21 mBB |

## Ce qu'on en conclut

1. **Aucun des quatre exports n'est plus précis que les autres** : si ce sont des réglages de précision croissants, ils n'améliorent pas les EV par main.
2. **L'écart est un bruit aléatoire, pas un biais** : le biais moyen est presque nul, la dispersion entre exports identiques est du même ordre que l'écart avec l'EV exacte, et la moyenne de n exports réduit l'écart à peu près comme 1/√n (heads-up : 100 → 60 → 42 mBB). À 3 joueurs, la baisse est plus lente : une partie de l'écart vient de l'approximation de notre calcul exact (cartes du joueur couché non retirées).
3. **Les fréquences sont stables** (1 à 2 points d'écart en médiane) : c'est l'EV par main exportée qui est bruitée, pas la stratégie.

## Suite proposée

- **Demander à HRC** s'il existe un réglage distinct pour la précision des EV par main (échantillonnage de l'évaluation), et confirmer ce qui différait entre les quatre exports.
- **À défaut, répéter les calculs** : 4 exports identiques par configuration, et l'importeur fait la moyenne des EV (et des fréquences). Écart attendu en heads-up : environ 40 mBB au lieu de 100, ce qui permettrait de baisser le filtre de bruit de 150 à environ 75 mBB et de rendre les décisions serrées.
- **Refaire le test sur l'arbre de référence** (`ALLOWED_FLATS_PER_RAISE` = `[1, 1, 1, 1, 0]`), pour que les exports soient utilisables tels quels.
