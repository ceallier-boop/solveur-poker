# Journal des publications de datasets

L'état de publication vit dans la base de l'application (`datasets`, journal `/admin/log`), pas dans le dépôt. Ce fichier garde la trace des publications décidées par le porteur du projet, pour les rejouer sur un autre serveur avec les mêmes routes (`POST /admin/datasets/<dataset>/<version>/validate`, puis `/publish`).

| Date | Dataset | Version | Contrôle | Décision | Remplace |
|---|---|---|---|---|---|
| 2026-10-13 | `gto_preflop` | `2026.10.13-3` | réussi | publication demandée par le porteur du projet (base HRC v3 : arbre complet, tapis déséquilibrés, tailles d'ouverture) | aucune version publiée sur ce serveur |
| 2026-10-13 | `exploit_calls` | `2026.10.13-4` | réussi (source GTO publiée) | idem (profils sur l'équilibre push/fold, générateur 2.0.0) | aucune version publiée sur ce serveur |
| 2026-10-14 | `exploit_calls` | `2026.10.14-1` | réussi (source GTO publiée, reconstruction identique) | lot 1 de l'évaluation du MVP : tapis du SB contre la Station d'appel (générateur 2.1.0, catalogue de profils 1.5.0) | `exploit_calls/2026.10.13-4` |
| 2026-10-20 | `exploit_field` | `2026.10.20-1` | réussi (reconstruction identique depuis les exports HRC) | mode Field : banque du moteur exploitant v4.2, corrigée après l'audit des coachs (`docs/audit/AUDIT_COACHS_FIELD_2026-10-20.md`) | aucune version publiée sur ce serveur |
| 2026-10-20 | `exploit_field` | `2026.10.20-2` | réussi (reconstruction identique depuis les exports HRC) | profils rééquilibrés selon leur part dans le field (rec passif 57 %, station 16 %, reg 11 %, dégène 10 %, nit 6 %) | `exploit_field/2026.10.20-1` |
| 2026-10-21 | `exploit_field` | `2026.10.20-4` | réussi (reconstruction identique depuis les exports HRC) | mode Exploitant principal : situations « BB face au limp du SB », 440 questions, théorie et postflop (la 2026.10.20-3, publiée puis remplacée le même jour, avait une faute dans un texte du moteur) | `exploit_field/2026.10.20-2` |
| 2026-10-21 | `exploit_field` | `2026.10.21-1` | réussi (reconstruction identique depuis les exports HRC) | banque agrandie (2173 questions, × 4,9) et corrections de la relecture des limps par les experts IA (`docs/relecture/limp_2026-10-21/SYNTHESE.md`), moteur v4.3 ; ancien mode exploitant (`exploit_calls`) retiré | `exploit_field/2026.10.20-4` |
| 2026-10-21 | `exploit_field` | `2026.10.21-2` | réussi (reconstruction identique depuis les exports HRC) | banque x 10 (4400 questions) : le volume prime sur les proportions (décision du porteur du projet), générateur 4.3.1 | `exploit_field/2026.10.21-1` |
| 2026-10-22 | `exploit_field` | `2026.10.22-1` | réussi (reconstruction identique depuis les exports HRC) | moteur v4.4 : corrections de l'audit complet des coachs (`docs/relecture/bilan_2026-10-21/SYNTHESE_AUDIT.md`, partie 6) | `exploit_field/2026.10.21-2` |

Serveur concerné : instance de travail de la session (`data/app/spinsacademy.sqlite`). Aucun serveur de production n'est encore en service ; au premier déploiement (`docs/exploitation/DEPLOIEMENT.md`), rejouer ces deux contrôles et publications depuis `/admin`.
