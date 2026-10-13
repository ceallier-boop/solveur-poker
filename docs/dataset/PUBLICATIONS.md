# Journal des publications de datasets

L'état de publication vit dans la base de l'application (`datasets`, journal `/admin/log`), pas dans le dépôt. Ce fichier garde la trace des publications décidées par le porteur du projet, pour les rejouer sur un autre serveur avec les mêmes routes (`POST /admin/datasets/<dataset>/<version>/validate`, puis `/publish`).

| Date | Dataset | Version | Contrôle | Décision | Remplace |
|---|---|---|---|---|---|
| 2026-10-13 | `gto_preflop` | `2026.10.13-3` | réussi | publication demandée par le porteur du projet (base HRC v3 : arbre complet, tapis déséquilibrés, tailles d'ouverture) | aucune version publiée sur ce serveur |
| 2026-10-13 | `exploit_calls` | `2026.10.13-4` | réussi (source GTO publiée) | idem (profils sur l'équilibre push/fold, générateur 2.0.0) | aucune version publiée sur ce serveur |

Serveur concerné : instance de travail de la session (`data/app/spinsacademy.sqlite`). Aucun serveur de production n'est encore en service ; au premier déploiement (`docs/exploitation/DEPLOIEMENT.md`), rejouer ces deux contrôles et publications depuis `/admin`.
