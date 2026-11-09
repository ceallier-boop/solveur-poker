# Les 3 pires erreurs de la journée (N2, 09/11/2026)

Décision du porteur : l'accueil montre les 3 erreurs les plus coûteuses du jour, avec un bouton pour les rejouer. Défis et rétention fait le calcul serveur, Interface le bloc.

## Calcul (codé : `spinsacademy/worst.py`)
- Réponses du **jour local** du joueur (`tz` de l'appareil), dans le mode demandé.
- Verdict « erreur » ou « imprécision », **regret strictement positif** : une réponse acceptée (référence ou experts) a un regret nul et n'y entre pas.
- **Exclus** : coups joués au temps (pas de choix du joueur), questions de lecture du vilain (sans EV, donc sans coût en BB), test de placement (hors statistiques).
- Tri par regret décroissant, au plus 3 ; moins s'il y en a moins ; **liste vide** sinon (l'interface dit « Aucune erreur coûteuse aujourd'hui »).
- Libellés et coût repris du résultat enregistré, comme le bilan de série : un seul chiffre de coût.

## Format
`GET /users/me/worst-today?mode=gto|exploit&tz=<minutes>`, en-tête `X-Player-Id` (400 sans, 422 mode inconnu). Réponse réelle (une série jouée par l'API) :

```json
{"mode": "gto", "date": "2026-11-09", "errors": [
  {"session_id": "999a05361b504809b0460c4b03209927", "question_index": 4, "spot_id": "hu-4-8-root-a519b5", "hand": "83o",
   "prompt_fr": "Heads-up, tapis 4 / 8 BB (SB / BB).\nPersonne n'a encore parlé.\nTu es au SB avec 8♠3♥. Que fais-tu ?",
   "chosen_fr": "ALL-IN 4 BB", "best_fr": "FOLD", "verdict": "erreur", "regret_mbb": 275.5, "cost_bb": 0.28, "cost_fr": "0,28 BB",
   "answered_at": "2026-11-09T17:22:17+00:00", "replayed_ok": false}]}
```

`cost_fr` est le texte à afficher ; `cost_bb` sert au tri ou à une mise en forme propre.

## Liste stable dans la journée (décision du 09/11)
La liste se remplit série après série jusqu'à compter 3 erreurs, puis ne change plus jusqu'à minuit, même si une erreur plus coûteuse arrive ensuite. Sans stockage : les séries du jour sont prises dans leur ordre de création, on s'arrête à celle qui porte le total à 3, et l'on garde les 3 plus coûteuses de ces séries. Les réponses d'un rejeu n'y entrent jamais. Chaque erreur porte `replayed_ok` : vrai si elle a été rejouée juste ce jour-là.

## « Les rejouer » (codé, décision du 09/11)
`POST /sessions` avec `{"mode": "gto", "plan": "replay", "tz": 60}`, **sans liste**, joueur identifié (400 sinon). Le serveur recalcule la liste du jour et sert ces (situation, main), dans le même ordre, de 1 à 3 questions, sans complément ; chaque question porte « Rejeu de ton erreur du jour (0,28 BB) ». Aucune erreur : 422 « Aucune erreur à rejouer aujourd'hui ».
- Compte dans les statistiques et la révision espacée, et comme un jour d'entraînement.
- Ne compte ni dans un défi, ni dans les étapes de la séance (plan `replay`, pas `theme`), ni dans le test de placement.
- Pas de nouvelle table : `sessions.plan = 'replay'`.

Contrôles : `tests/test_worst.py` (sans pseudo, liste vide, tri des 3 pires, mode exploitant, test de placement exclu, fuseau, rejeu : 400, 422, mêmes questions, `replayed_ok`, statistiques, ni défi ni séance ; erreurs du rejeu hors liste ; liste stable après de nouvelles erreurs).
