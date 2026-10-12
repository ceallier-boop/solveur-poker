# API du quiz

Lancement : `python -m uvicorn spinsacademy.api:app --port 8000`. La documentation interactive est servie sur `/docs`.

Variables d'environnement :
- `SPINSACADEMY_DB` : base SQLite des sessions (par défaut `data/app/spinsacademy.sqlite`, hors dépôt) ;
- `SPINSACADEMY_DATASET` : version du dataset GTO servie (par défaut `2026.10.12-2`) ;
- `SPINSACADEMY_EXPLOIT` : dataset exploitant servi (par défaut `exploit_calls/2026.10.13-1`, voir `docs/dataset/EXPLOIT_CALLS.md`).

Mode invité au MVP : pas d'authentification. La question 22 du cahier des charges (comptes ou invité) reste à trancher. L'interface génère un identifiant anonyme d'appareil, envoyé dans l'en-tête `X-Player-Id`. Il relie les séries d'un même joueur ; une série créée sans cet en-tête n'entre dans aucune statistique.

| Route | Rôle |
|---|---|
| `GET /health` | état, version du dataset, nombre de spots |
| `POST /sessions` | crée une série : `{"mode": "gto" | "exploit", "size": 5, "seed": 12, "filters": {"table": "3-handed", "hero": "SB", "family": "vs_limp", "min_stack": 10, "max_stack": 25}}`, tous les champs étant facultatifs. Réponse : `session_id`, `dataset_version`, `size`. Erreur 422 si les filtres ne laissent pas assez de spots. |
| `GET /quiz/next?session_id=` | question suivante non répondue : énoncé (`prompt_fr`), état du jeu (tapis, historique, pot, montant à payer), options `{id, label_fr}`. **Aucune solution n'est envoyée.** `done: true` en fin de série. |
| `POST /attempts` | `{"session_id", "question_index", "action_id"}` → verdict, points, regret en mBB, meilleure action, stratégie arrondie, explication. Une réponse est définitive : renvoyer la même réponse rend la correction enregistrée (reprise après coupure réseau) ; une réponse différente donne 409. |
| `GET /users/me/stats` | progression du joueur (`X-Player-Id` obligatoire) : <br>• score global, verdicts, nombre de séries et de questions ; <br>• score par situation, position, format et profondeur, chaque ligne indiquant si son échantillon est suffisant (`reliable` : au moins 10 questions) ; <br>• évolution sur les 20 dernières séries ; <br>• les 3 erreurs récurrentes (thème avec au moins deux erreurs) ; <br>• point faible (`weakest`), seulement s'il existe un thème fiable. Chaque thème fournit les `filters` à passer à `POST /sessions` pour s'y entraîner. |
| `GET /users/me/export` | toutes les séries et réponses enregistrées pour ce joueur (droit d'accès et de portabilité) |
| `DELETE /users/me` | efface définitivement les séries et réponses de ce joueur (droit à l'effacement) |
| `GET /sessions/{id}/summary` | bilan : score, verdicts, résultats par famille de décision et position, erreurs triées par coût, énoncés à revoir |

Familles de décision : `first_in` (premier à parler), `vs_limp`, `vs_raise`, `vs_allin`.

## Tirage d'une série (`spinsacademy/quiz.py`)

- Chaque question tire une famille de décision (rotation aléatoire entre les familles disponibles), puis un spot de cette famille, puis une main proposable pondérée par sa fréquence naturelle (combos × atteinte).
- Jamais deux fois le même spot dans une série. Le tirage est reproductible avec `seed`.
- Une session reste liée à la version du dataset qui a servi à la corriger.

## Correction et explication

La notation est celle de `spinsacademy/grading.py` (`docs/dataset/FORMAT_SPOT.md`). L'explication est construite uniquement à partir des données du spot :
- la meilleure action et son gain par rapport au fold, ou au check quand rien n'est à payer ;
- l'écart de l'action choisie ;
- la raison d'une acceptation : stratégie mixte, ou écart non significatif ;
- la stratégie de référence arrondie à 5 % ;
- la source de l'EV.
