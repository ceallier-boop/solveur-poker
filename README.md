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
python -m spinsacademy.importer --version AAAA.MM.JJ-N  # publie un dataset en staging
python tools/hrc/make_locks.py                        # régénère data/hrc/locks/
python -m uvicorn spinsacademy.api:app --port 8000   # API du quiz + interface mobile sur http://localhost:8000/ (docs/api/API_QUIZ.md)
BASE_URL=http://localhost:8000/ node tools/web/e2e_mobile.cjs captures/   # parcours mobile complet (Playwright)
```
