# Relecture des calculs du solveur : consignes

Échantillon du 2026-10-30 : 60 situations préflop (identifiants S001 à S060), banque `gto_preflop/2026.10.29-s1`.

## Ton rôle

Tu es un joueur expert d'Expresso / Spin & Go (3 joueurs puis heads-up, préflop, **chip EV**, sans ICM, blinds 0,5 / 1 BB, sans ante).
Pour chaque situation, deux calculs d'équilibre proposent une stratégie pour ta main : le **calcul A** et le **calcul B**. Tu dis lequel
te paraît le plus juste. Les deux sont présentés à l'aveugle : leur ordre change d'une situation à l'autre. Tu travailles seul : ne te
concerte pas avec les autres coachs, l'accord entre coachs est mesuré ensuite.

## Ce que montrent les fiches

- L'arbre est le même pour les deux calculs : ouverture du BTN à 2,3 BB, du SB à 3,5 BB, iso du BB à 3 BB face au limp du SB
  (3,5 BB + 1 BB par limper sinon), puis 3-bets et tapis.
- **Fréquence** : part du temps où le calcul joue chaque option avec cette main. **EV** : gain moyen de l'option en BB, relatif au fold
  (fold = 0). Les EV des deux calculs ne sont pas mesurées de la même façon et peuvent contenir un bruit de l'ordre de 0,1 BB :
  juge d'abord la décision, ensuite les montants.
- La plupart des situations sont choisies là où les deux calculs ne jouent pas la même action ; quelques-unes sont des témoins.

## Grille

Remplis une ligne par situation dans `reponses_modele.csv` (séparateur `;`, ne change ni l'ordre des lignes ni celui des colonnes) :

| Colonne | Valeurs | Sens |
|---|---|---|
| `id` | S001… | déjà rempli |
| `coach` | ton nom | |
| `meilleure_action` | le libellé d'une option (ex. `ALL-IN 25 BB`) | ce que tu joues avec cette main, en chip EV, contre des adversaires qui jouent l'équilibre |
| `calcul_le_plus_juste` | `A` / `B` / `les deux` / `aucun` | `les deux` : les deux options se valent (écart négligeable) |
| `confiance` | `forte` / `moyenne` / `faible` | |
| `commentaire` | texte libre, court | ce qui te fait trancher (une phrase suffit) |
