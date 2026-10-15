# API du quiz

Lancement : `python -m uvicorn spinsacademy.api:app --port 8000`. La documentation interactive est servie sur `/docs`.

Variables d'environnement :
- `SPINSACADEMY_DB` : base SQLite des sessions (par défaut `data/app/spinsacademy.sqlite`, hors dépôt) ;
- `SPINSACADEMY_DATASET` : version du dataset GTO servie (par défaut `2026.10.13-2`) ;
- `SPINSACADEMY_EXPLOIT` : dataset exploitant servi (par défaut `exploit_calls/2026.10.13-3`, voir `docs/dataset/EXPLOIT_CALLS.md`).

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

Mode exploitant : `GET /profiles` donne le catalogue des profils fictifs ; le filtre `profile` (`nit`, `prudent`, `agressif`, `maniac`) restreint la série à un profil. Chaque question exploitante porte `profile` (sans conseil), et la correction un objet `exploit` : `reference_fr` (contre ce profil, montant en fourchette), `comparison_fr` (par rapport au GTO), `tendency_fr`, `confidence` (`élevée` ou `moyenne`), `confidence_fr` (« enjeu net » à partir de 0,06 BB d'écart d'EV, « enjeu faible » en dessous), `note_fr`, `choice_loss_fr`, `profile` (avec la version du catalogue). Détails : `docs/dataset/EXPLOIT_CALLS.md`.

## Tirage d'une série (`spinsacademy/quiz.py`)

- Chaque question tire une famille de décision (rotation aléatoire entre les familles disponibles), puis un spot de cette famille, puis une main proposable pondérée par sa fréquence naturelle (combos × atteinte).
- Jamais deux fois le même spot dans une série. Le tirage est reproductible avec `seed`.
- Une session reste liée à la version du dataset qui a servi à la corriger.
- Les spots désactivés par l'administration (voir ci-dessous) ne sont plus tirés. Désactiver un spot GTO retire aussi les spots exploitants qui en dérivent (`base_spot_id`). Les séries déjà tirées ne sont pas modifiées.

## Correction et explication

La notation est celle de `spinsacademy/grading.py` (`docs/dataset/FORMAT_SPOT.md`). L'explication est construite uniquement à partir des données du spot :
- la meilleure action et son gain par rapport au fold, ou au check quand rien n'est à payer ;
- l'écart de l'action choisie ;
- la raison du verdict, avec son seuil (bruit de calcul sous 0,02 BB, imprécision jusqu'à 0,06 BB, erreur au-delà, action mixte jouée au moins 10 % du temps) ; pour une EV HRC, une action à moins de 0,1 BB de la meilleure reste « pertinente » : au pire une imprécision, et la correction de la référence ajoute « Nuance : … est aussi pertinente » (décision du porteur du projet, 2026-10-14) ;
- après une erreur ou une imprécision (mode GTO), une ligne « À retenir » : la range de la référence en règle à seuils (« 22+, A2+, K7s+ »), affichée seulement si elle classe bien au moins 93 % des mains pondérées, sinon la part des mains ;
- la stratégie de référence : actions jouées au moins 10 % du temps, arrondies à 5 % ;
- la source de l'EV.

## Révision espacée des erreurs (`spinsacademy/review.py`, évaluation du MVP, remarque 21)

Une main ratée (erreur ou imprécision) revient 1 jour, puis 3 jours, puis 7 jours après ; une bonne réponse à l'échéance la fait avancer, une réussite avant l'échéance ne compte pas, une nouvelle erreur la fait repartir à 1 jour. Après la révision à 7 jours, la main est acquise. Seules les mains dont la situation existe dans le dataset servi (même `spot_id`) et y reste proposable sont révisées.

| Route | Rôle |
|---|---|
| `GET /users/me/reviews?mode=gto` | règle, nombre de mains prêtes (`due`) et à venir (`pending`), date de la prochaine, mains prêtes (20 au plus) |
| `POST /sessions` avec `review: true` | série qui commence par les mains prêtes, complétée par un tirage normal ; `purpose: "spaced"`, `purpose_fr` « Révision de ton erreur du 14/10 (étape 1 sur 3) » ; exige `X-Player-Id` |

Accueil : bouton « Revoir mes erreurs (N mains prêtes) », ou date de la prochaine révision ; le bilan d'une série avec des erreurs le rappelle. La démo applique la même règle dans le navigateur.

## Limitation du nombre de requêtes (`spinsacademy/ratelimit.py`, remarque 25)

Plafonds par minute : 300 par adresse IP, 120 par joueur, 30 créations de série et 10 signalements par joueur ; au-delà, 429 avec `Retry-After` et un message en français (l'interface propose « Réessayer »). Détails et réglages : `docs/exploitation/SECURITE.md`.

## Signalement d'une erreur (cahier des charges §7 et §14)

Sur l'écran de correction, le joueur peut signaler la question : motif obligatoire, commentaire facultatif (1 000 caractères au plus).

| Route | Rôle |
|---|---|
| `POST /reports` | `{session_id, question_index, reason, comment?}` → `201 {report_id, status: "open"}`. `reason` : `wrong_answer`, `unclear`, `illegal_action` ou `other`. `409` si la question n'a pas encore reçu de réponse (pas de signalement avant la correction) ou si elle a déjà été signalée. |

Le signalement enregistre la version du dataset, le spot, la main et l'action choisie : l'expert retrouve exactement la question vue.

### Administration

Page d'administration : `/admin` (mobile et ordinateur). L'expert saisit le jeton et son nom (inscrit au journal), puis traite les signalements : énoncé, réponse du joueur, correction qu'il a vue, commentaire, décision motivée, retrait éventuel du spot. Le jeton reste dans l'onglet (sessionStorage) ; la page elle-même ne contient aucune donnée.

Les routes `/admin/*` exigent l'en-tête `X-Admin-Token`, égal à la variable d'environnement `SPINSACADEMY_ADMIN_TOKEN`. Si la variable n'est pas définie, l'administration est fermée (`403`).

| Route | Rôle |
|---|---|
| `GET /admin/reports?status=open` | signalements (`open`, `accepted` ou `rejected`), avec le motif en français, l'énoncé, la correction affichée au joueur (`correction`) et le nombre de signalements sur le même spot |
| `POST /admin/reports/{id}/resolve` | `{status: accepted\|rejected, resolution, disable_spot?, actor?}`. Avec `disable_spot`, le spot n'est plus tiré. `409` si le signalement est déjà traité. |
| `GET /admin/disabled` | spots désactivés, avec le motif et le signalement d'origine |
| `DELETE /admin/disabled/{spot_id}?reason=...&actor=...` | réactive un spot (motif obligatoire) |
| `GET /admin/log` | journal de toutes les décisions d'administration (qui, quand, quoi) |

Le dataset publié n'est jamais modifié : une correction de fond passe par une nouvelle version. La désactivation sert à retirer tout de suite une question douteuse, en attendant cette nouvelle version.

## Publication des datasets (cahier des charges §2, §13.1 et §16)

L'application ne sert que des versions **publiées**. Tant qu'aucune version n'est publiée pour un mode, `POST /sessions` répond `503`. En développement et dans les tests, `SPINSACADEMY_ALLOW_STAGING=1` sert les versions par défaut (`SPINSACADEMY_DATASET`, `SPINSACADEMY_EXPLOIT`) quand rien n'est publié ; cette variable ne doit pas être définie en production.

Cycle de vie (`spinsacademy/catalog.py`), statut enregistré dans la base de l'application :

| Statut | Sens |
|---|---|
| `staging` (À contrôler) | dossier présent sur le serveur, jamais contrôlé |
| `rejected` (Refusé au contrôle) | au moins un contrôle bloquant en échec ; publication impossible |
| `validated` (Contrôlé) | tous les contrôles bloquants réussis |
| `published` (Publié) | version servie aux nouvelles séries ; une seule par dataset |
| `retired` (Remplacé) | ancienne version publiée, remplacée par une nouvelle ; peut être republiée (retour arrière) |
| `disabled` (Retiré) | retrait en urgence : plus de nouvelles séries, et les séries en cours s'arrêtent (`410`) ; peut être republiée |

Contrôles (rapport lisible dans `/admin`, onglet Datasets) :
- bloquants : manifeste cohérent avec le dossier ; empreinte SHA-256 du fichier des spots identique au manifeste ; nombre de spots et de questions conformes ; aucun doublon ; chaque spot complet et légal (héros présent et non couché, actions distinctes, pas de check face à une mise ni de fold gratuit, pas de mise au-delà des tapis, 169 mains, fréquences normalisées, EV de référence complète pour chaque main proposable, règles d'éligibilité du manifeste respectées) ; pour l'exploitant, chaque spot renvoie à un spot du dataset GTO source ;
- test de référence : chaque spot est reconstruit depuis ses sources (exports HRC pour le GTO, dataset GTO source pour l'exploitant) et doit être identique. Si la reconstruction n'est pas comparable (version d'importeur différente, exports absents de ce poste), c'est un avertissement affiché, pas un échec ;
- avertissement : dataset GTO source non publié (exploitant).

Règles : publier exige un contrôle réussi sur des fichiers inchangés depuis le contrôle ; un dataset exploitant ne peut être publié que si son dataset GTO source l'est ; retirer un dataset GTO retire aussi les datasets exploitants publiés qui en dérivent. Publier, retirer et contrôler sont inscrits au journal (acteur, date, motif). Le contrôle est aussi disponible hors application : `python -m spinsacademy.catalog gto_preflop/2026.10.12-2`.

L'import reste hors ligne : `python -m spinsacademy.importer --version X` (GTO, depuis les exports HRC du dépôt) et `python -m spinsacademy.exploit --version X --gto Y` produisent un dossier immuable en `staging`, livré au serveur avec le code. Les exports HRC bruts ne sont jamais servis par l'application.

| Route (en-tête `X-Admin-Token`) | Rôle |
|---|---|
| `GET /admin/datasets` | versions connues, statut, volumes, résumé du dernier contrôle, dernière décision |
| `POST /admin/datasets/{dataset}/{version}/validate` | `{actor}` → rapport ; statut `validated` ou `rejected` |
| `GET /admin/datasets/{dataset}/{version}/report` | dernier rapport de contrôle |
| `POST /admin/datasets/{dataset}/{version}/publish` | `{reason, actor}` → publie ; l'ancienne version publiée passe en `retired` |
| `POST /admin/datasets/{dataset}/{version}/disable` | `{reason, actor}` → retire (et les exploitants dérivés) |

`GET /health` indique les versions publiées. Les refus du cycle de vie répondent `409` avec la raison.

## Exercices adaptatifs (cahier des charges §9.3, `spinsacademy/adaptive.py`)

Règle affichée au joueur (`rule_fr`) :
- thème = famille de décision × position × profondeur, dans le mode de la série ;
- difficulté d'un thème = (erreurs + 0,5 × imprécisions + 1) / (réponses + 3), taux lissé qui ne conclut pas sur quelques réponses ;
- thème à retravailler : au moins 3 réponses, au moins 2 erreurs et une difficulté ≥ 40 % ;
- thème acquis : au moins 5 réponses et une difficulté < 25 % ;
- une série adaptée : 60 % de questions sur les thèmes à retravailler (tirés au prorata de leur difficulté), 20 % de révision (thèmes acquis les moins récemment travaillés), le reste en découverte (thèmes jamais travaillés, sinon les moins travaillés) ;
- sans thème à retravailler, la série est tirée normalement.

L'adaptation s'applique à la « série recommandée » d'un joueur identifié (`X-Player-Id`), sans filtre : un thème choisi par le joueur est toujours respecté. Elle ne modifie jamais la correction. Chaque question indique son objectif (`purpose` : `weak`, `review`, `discovery`, `complement` ; `purpose_fr`).

| Route | Rôle |
|---|---|
| `POST /sessions` | champ facultatif `adaptive` (sinon : préférence du joueur) ; la réponse contient `adaptive` : `active`, `reason_fr`, `rule_fr` |
| `GET /users/me/adaptation?mode=gto` | règle, thèmes à retravailler, thèmes en révision, état de la préférence, date de réinitialisation |
| `GET /users/me/preferences`, `PUT /users/me/preferences` | `{adaptive: true \| false}` (activée par défaut) |
| `POST /users/me/adaptation/reset` | l'adaptation ne compte plus que les réponses postérieures ; l'historique et les statistiques sont conservés |

Les préférences sont incluses dans `GET /users/me/export` et effacées par `DELETE /users/me`.


## Lexique

`spinsacademy/web/lexique.json` (servi en `/static/lexique.json`, version 1.0.0) : 68 termes techniques en 5 catégories (table et format, actions, calcul et stratégie, profils exploitants, application). Le bouton « Lexique » de la barre du haut ouvre un panneau : d'abord les termes repérés sur l'écran affiché (sigles BB, SB, BTN, GTO, EV, ICM, mBB repérés en respectant la casse), puis tout le lexique par catégorie, avec une recherche. Les définitions sont à faire relire par un expert poker.
