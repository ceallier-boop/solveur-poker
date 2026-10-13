# SpinsAcademy

Application d'entraînement au Spin & Go / Expresso. Cahier des charges : `docs/cahier_des_charges/` ; format des données : `docs/dataset/FORMAT_SPOT.md` ; audit de l'existant : `docs/audit/AUDIT_PHASE0.md`.

## Arborescence

| Dossier | Contenu |
|---|---|
| `spinsacademy/` | moteur : lecture HRC, EV exactes des all-in, import des spots, correction |
| `data/hrc/raw/` | exports HRC de référence (**jamais embarqués dans l'application**) |
| `data/hrc/locks/` | stratégies à verrouiller dans HRC pour le mode exploitant |
| `data/datasets/` | datasets publiés, versionnés et immuables |
| `tools/hrc/` | validation des exports, génération des verrouillages |
| `legacy/` | travaux antérieurs, en lecture seule |

## Commandes

```bash
pip install -r requirements.txt
python -m pytest -q                                   # tests
python tools/hrc/validate.py                          # rapport docs/hrc/VALIDATION_HRC.md
python -m spinsacademy.importer --version AAAA.MM.JJ-N  # produit un dataset en staging (à contrôler puis publier dans /admin)
python -m spinsacademy.catalog gto_preflop/AAAA.MM.JJ-N  # contrôles de publication, hors application
python tools/hrc/make_locks.py                        # régénère data/hrc/locks/
SPINSACADEMY_ADMIN_TOKEN=... python -m uvicorn spinsacademy.api:app --port 8000   # API + interface mobile sur http://localhost:8000/, administration sur /admin (docs/api/API_QUIZ.md)
SPINSACADEMY_ALLOW_STAGING=1 python -m uvicorn spinsacademy.api:app --port 8000   # développement : sert les versions par défaut tant que rien n'est publié
BASE_URL=http://localhost:8000/ ADMIN_TOKEN=... node tools/web/e2e_datasets.cjs captures/   # publication des datasets depuis /admin (base neuve)
BASE_URL=http://localhost:8000/ node tools/web/e2e_mobile.cjs captures/   # parcours mobile complet (Playwright)
```
