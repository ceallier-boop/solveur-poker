# Analyse de la banque intermédiaire `gto_preflop/2026.11.02-s2` (03/11/2026)

Banque calculée par notre solveur sur l'ordinateur du porteur du projet (O5) : arbre v5 (ouvertures à 2 BB, tapis direct toujours proposé), réglage de regroupement `ehs2_texture`, grille P1 de 58 configurations (25 heads-up, 33 à 3 joueurs).

## Contrôles

| Contrôle | Résultat |
|---|---|
| Catalogue (`catalog.validate`) | réussi : 1 780 spots, 151 205 questions, contrôles du solveur des 58 configurations conformes, reconstruction à l'identique depuis `data/solver/runs/sf3dc2e6_48fa0906/` |
| Exploitabilité | 0,55 mBB par main au pire (seuil 5) |
| Dérive préflop / postflop | 0,6 mBB au pire (seuil 1) |
| Calage sur la référence | aucun : pas d'export v5 de la référence (O2, O4 non reçus) |
| Durée | heads-up 2 minutes en moyenne, 3 joueurs 35 minutes en moyenne (4 à 10 minutes sur la machine cloud de même nombre de cœurs) ; une configuration, 3 joueurs 20 / 40 / 15, a duré 7 h, sans doute une mise en veille |

## Comparaison avec le pilote `2026.10.29-s1` (arbre de la référence : ouvertures 2,3 et 3,5 BB)

Les deux banques n'ont pas le même arbre : les comparaisons portent sur les nœuds de même ligne, tailles de relance confondues. Fréquences globales (part des mains, pondérée par les combos et l'atteinte) :

| Nœud | Pilote (2,3 / 3,5 BB) | v5 (2 BB) |
|---|---|---|
| HU 25, SB premier de parole : fold / limp / relance | 6 / 70 / 24 | 9 / 52 / 39 |
| HU 25, BB face à la relance du SB : fold / call / 3-bet / tapis | 53 / 29 / 11 / 7 | 26 / 47 / 10 / 18 |
| HU 12, BB face à la relance du SB : fold / call / tapis | 60 / 13 / 27 | 27 / 41 / 32 |
| 3 joueurs 25, BTN premier de parole : fold / limp / relance | 61 / 5 / 34 | 62 / 0 / 38 |
| 3 joueurs 25, BB face à la relance du SB (BTN couché) : fold / call / 3-bet / tapis | 52 / 36 / 2 / 10 | 18 / 66 / 10 / 7 |
| 3 joueurs 12, décisions face à un tapis | — | identiques à 1 point près |

Les écarts viennent de l'arbre : une ouverture à 2 BB se défend beaucoup plus qu'une ouverture à 3,5 BB, et le SB relance plus souvent au lieu de limper. Les décisions face à un tapis, qui ne dépendent pas de la taille d'ouverture, ne bougent pas.

## Points de contrôle des coachs (échantillon G12)

Les 39 désaccords de l'échantillon, rejoués sur la ligne correspondante de l'arbre v5 :

| Avis majoritaire des coachs | Désaccords | v5 rejoint les coachs | v5 reste à l'opposé |
|---|---|---|---|
| Pour la référence | 21 | **6** : 96o et J8o checkés derrière le limp, K2o limpé au SB, ATs relancé, 76o et K6o payés face à l'open du BTN | 15 |
| Pour notre solveur | 16 | **11** gardés (pas de limp au BTN à 3 joueurs, tapis à 12 BB, AA relancé, etc.) | 5 changent (K7o, A3o checkés au lieu d'isoler ; K6s ouverte au lieu de tapis ; Q8o et J8o payés face à l'open) |

À lire avec deux réserves :
- une partie des changements tient à l'arbre et non au calcul : face à une ouverture à 2 BB au lieu de 3,5 BB, payer Q8o, J8o, 76o ou K6o devient normal ; ces situations ne sont plus celles que les coachs ont jugées ;
- **le défaut des pots relancés reste entier** sur les deux familles que les trois coachs donnaient à la référence : le SB qui a limpé se couche toujours face à l'iso à 25 BB avec K5o (89 %), K4o (90 %) et Q8o (58 %), et le BB isole toujours T9o (62 %), Q4o et Q5o (99 %) mais pas KJo à 12 BB. C'est le résidu mesuré par le calcul exact (paires et Kx faibles sous-évalués quand ils paient dans un pot relancé) : action G17.

## Avis sur la promotion

**Ne pas la publier comme banque GTO principale pour l'instant.** Elle est valide (contrôles réussis, stratégie convergée), mais :
1. elle n'est calée sur aucune référence v5 (O2, O4) ;
2. le défaut des pots relancés à 20-25 BB fausse des décisions que les joueurs rencontrent souvent (défense face à l'iso, composition de la range d'iso), et la correction (G17) refera toute la grille ;
3. côté application, les spots du solveur portent `ev_reference = hrc` : le filtre anti-bruit de 150 mBB (`quiz.REF_NOISE_MBB`), pensé pour le Monte-Carlo de la référence, écarterait les décisions serrées alors que le solveur n'a pas ce bruit. À régler avec la publication (hors du moteur).

Usage possible dès maintenant : la publier en test, à côté de la banque actuelle, pour une session de test joueurs sur les tapis courts (8 à 16 BB), où les pots relancés finissent surtout à tapis et où le défaut pèse peu.
