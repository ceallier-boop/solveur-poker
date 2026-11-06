# Progression présentée en positif : indicateurs (AU5, 06/11/2026)

Chantier AU5 (audit de test, validé par le porteur) : Interface fait l'écran, Défis et rétention fournit les indicateurs. Cette note donne le calcul, les seuils minimaux d'échantillon et le format côté serveur. **Aucune route n'est codée avant la confirmation de Plan.**

## Règles communes
- **Jamais de chiffre négatif** : un indicateur qui ne montre pas de progrès n'est pas renvoyé (pas de « +0 », pas de « −3 »). Il reste toujours au moins l'indicateur d'effort (§5).
- **Pas de pourcentage sur un petit échantillon** : chaque indicateur a un minimum de décisions par fenêtre (tableau). En dessous, il n'est pas renvoyé.
- **Pas de bruit présenté comme un progrès** : un écart doit dépasser un seuil absolu **et** une erreur type (z ≥ 1, test volontairement indulgent : c'est un encouragement, pas une étude).
- Calcul par mode (GTO ou Exploitant), comme les objectifs ; journées dans le fuseau de l'appareil (`tz`). Les questions de lecture du vilain n'ont pas d'EV : elles ne comptent pas dans les BB, mais comptent dans les erreurs.
- Données existantes uniquement (`attempts`, `sessions`, `player_level`) : aucun stockage nouveau, rien qui dépende du journal d'usage (D1).

## Les indicateurs
| # | Indicateur | Calcul | Minimum d'échantillon | Seuil pour l'afficher |
|---|---|---|---|---|
| 1 | **BB récupérés** (semaine passée) | BB perdus pour 100 décisions (`progress.bb_per_100`) sur J−7 à J (B₀) et sur J−14 à J−7 (B₁) ; gain = B₁ − B₀ ; BB récupérés = gain × n₀ / 100 | 50 décisions chiffrées dans **chaque** fenêtre | gain ≥ 1 BB pour 100 **et** gain ≥ 10 % de B₁ **et** gain ≥ erreur type |
| 2 | **Erreurs en moins** (il y a 15 jours) | erreurs (verdict « erreur », imprécisions exclues) pour 100 décisions sur J−15 à J (E₀) et sur J−30 à J−15 (E₁) ; écart = E₁ − E₀ | 60 décisions dans **chaque** fenêtre | écart ≥ 2 pour 100 **et** écart ≥ 15 % de E₁ **et** z ≥ 1 |
| 3 | **Mains rattrapées en révision** | sur J−7 à J, avec la machine d'états de `review.items` : réussites qui font monter une main d'étape (J+1, J+3, J+7) ; mains passées « acquises » (les trois étapes) | aucun : ce sont des nombres, pas des taux | au moins 1 main acquise **ou** au moins 3 réussites |
| 4 | **Passage de niveau** | `player_level.promoted_at` dans les 7 derniers jours (passage automatique seulement : un changement manuel ne le remplit pas) | — | dès qu'il existe |
| 5 | **Effort** (toujours présent) | décisions jouées et jours d'entraînement sur J−7 à J | — | toujours renvoyé, même à zéro (« Ta première série t'attend ») |

Erreurs types (indicateurs 1 et 2) :
- 1 : SE = 100 × √(s₀²/n₀ + s₁²/n₁) / 1000, avec sᵢ l'écart type des regrets par décision (mbb) de la fenêtre ;
- 2 : avec p = taux commun des deux fenêtres, SE = 100 × √(p(1−p)(1/n₀ + 1/n₁)) ; z = écart / SE.

Limites connues :
- **Mélange des questions** : une semaine sur des tapis plus profonds (niveau 3) perd plus de BB qu'une semaine sur les tapis courts. Si le joueur a changé de niveau dans les 14 jours, l'indicateur 1 n'est calculé que sur les questions de son niveau actuel (même filtre que `levels.in_level`), avec les mêmes minimums.
- **Un seul passage gardé** : `promoted_at` est écrasé au passage suivant ; deux passages en 7 jours n'en montrent qu'un.
- **Révision payante** (frontière P14, à valider) : pour un joueur gratuit sans révision, l'indicateur 3 n'est pas renvoyé.

Ordre d'affichage proposé : passage de niveau, BB récupérés, erreurs en moins, mains rattrapées, effort. Interface en montre au plus deux sur l'accueil, tous dans « Ma progression ».

## Format côté serveur (proposition, route non codée)
`GET /users/me/wins?mode=gto&tz=60` (joueur identifié par `X-Player-Id`, comme les autres routes du programme). Réponse :

```json
{
  "mode": "gto",
  "as_of": "2026-11-06",
  "wins": [
    {"kind": "level_up", "from_level": 1, "to_level": 2, "level_name_fr": "Le jeu à 10-16 BB", "at": "2026-11-04T18:12:03+00:00",
     "text_fr": "Niveau 2 atteint : Le jeu à 10-16 BB."},
    {"kind": "bb_recovered", "window_days": 7, "bb_per_100_now": 8.4, "bb_per_100_before": 11.2, "gain_per_100": 2.8,
     "bb_recovered": 9.5, "decisions_now": 340, "decisions_before": 290,
     "text_fr": "Tu perds 2,8 BB de moins pour 100 décisions que la semaine passée : environ 9,5 BB récupérés sur tes 340 décisions."},
    {"kind": "fewer_errors", "window_days": 15, "errors_per_100_now": 9.0, "errors_per_100_before": 14.0, "fewer_per_100": 5.0,
     "decisions_now": 410, "decisions_before": 380,
     "text_fr": "5 erreurs de moins pour 100 décisions qu'il y a 15 jours."},
    {"kind": "review_recovered", "window_days": 7, "stage_ups": 6, "mastered": 2,
     "text_fr": "6 mains ratées réussies en révision cette semaine, dont 2 acquises pour de bon."}
  ],
  "effort": {"window_days": 7, "decisions": 340, "active_days": 5, "text_fr": "340 décisions sur 5 jours cette semaine."},
  "not_enough": [{"kind": "fewer_errors", "decisions_now": 41, "needed": 60}]
}
```

- `wins` : seulement les indicateurs qui passent leur seuil, dans l'ordre d'affichage ; liste vide possible.
- `not_enough` : indicateurs 1 et 2 sous leur minimum, pour un texte du type « Encore 19 décisions pour comparer tes erreurs » ; jamais d'indicateur en recul dans cette liste.
- `text_fr` : phrase prête à afficher (chiffres arrondis, virgule décimale) ; les champs chiffrés restent pour une mise en forme propre à Interface.
- Célébration du passage de niveau : une seule fois par appareil, côté page (clé locale avec la date `at`), sans écriture serveur.
- Démo autonome : même calcul dans le navigateur, comme les objectifs.

## Questions à Plan
1. Route séparée `GET /users/me/wins` (proposée), ou un bloc `wins` dans `GET /users/me/stats` ?
2. Fenêtres de 7 et 15 jours, minimums de 50 et 60 décisions : d'accord, ou à caler sur les données de la bêta ?

## Réalisé (06/11/2026, après accord de Plan)
- Route séparée `GET /users/me/wins?mode=&tz=` (`spinsacademy/wins.py`), fenêtres de 7 et 15 jours, minimums de 50 et 60 décisions, format ci-dessus.
- Révision rattrapée renvoyée à tous pendant le test fermé, avec `"paid_feature": true` pour pouvoir la masquer quand la frontière P14 sera décidée.
- Changement de niveau : passage automatique (`promoted_at`) ou changement manuel (`updated_at` différent d'`onboarded_at`, pour ne pas compter l'arrivée d'un ancien joueur au niveau 1).
- Tests : `tests/test_wins.py` (joueur sans historique, moins de 50 décisions, changement de niveau dans les 14 jours, recul sans chiffre négatif, bruit sous le seuil, révision, fuseau).
- Pas encore : la même logique dans la démo autonome (à faire avec l'écran d'Interface).
