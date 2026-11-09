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
   "answered_at": "2026-11-09T17:22:17+00:00"}]}
```

`cost_fr` est le texte à afficher ; `cost_bb` sert au tri ou à une mise en forme propre.

## « Les rejouer » : proposition (non codée)
**Le plus simple** : `POST /sessions` avec `{"mode": "gto", "plan": "replay", "tz": 60}`, **sans liste**. Le serveur recalcule lui-même les pires erreurs du jour (même fonction) et sert ces (situation, main), dans le même ordre. Rien à vérifier, puisque le client n'envoie aucune question ; pas de nouvelle table (`sessions.plan = 'replay'`, comme `review`). Aucune erreur aujourd'hui : 422 « Aucune erreur à rejouer aujourd'hui ».

Variante si Interface veut choisir les questions : `"items": [{"session_id": …, "question_index": …}]`, le serveur vérifiant que chaque réponse est du joueur, du jour local et du mode. Plus de code, pour un gain faible.

Points à trancher :
1. La série de rejeu compte-t-elle dans les statistiques et la révision ? Proposition : oui, ce sont de vraies décisions (comme une série de révision).
2. Après un rejeu réussi, l'erreur reste-t-elle dans les 3 pires du jour ? Proposition : elle reste (c'est l'historique du jour), avec un champ `replayed_ok: true` pour que l'interface la coche.
3. Taille de la série : 1 à 3 questions (pas de complément par d'autres mains).

Contrôles : `tests/test_worst.py` (sans pseudo, liste vide, tri des 3 pires, mode exploitant, lecture du vilain et test de placement exclus, fuseau).
