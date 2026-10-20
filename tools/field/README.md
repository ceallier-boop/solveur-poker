# Moteur exploitant « field » (v4.2)

Porté du moteur exploitant v4.1 (stratégie exploitante v1, grilles Lucho / PA / Lucky) et corrigé après l'audit des coachs
du 20/10/2026 : `docs/audit/AUDIT_COACHS_FIELD_2026-10-20.md`. Outil de construction : rien de ce dossier n'est servi par
l'application, et les exports HRC lus ici (`data/hrc/raw`) ne sont jamais embarqués.

## Lancer (depuis ce dossier)

    python3 tests_exploit_v3.py                          # mécanique, monde synthétique (sans exports HRC)
    EXPRESSO_OUT=/tmp/x python3 quiz_generator.py         # banque quiz_field_v4_2.json / .csv
    EXPRESSO_QUIZ=/tmp/x/quiz_field_v4_2.json python3 verify_quiz.py
    python3 audit_quiz.py /tmp/x/quiz_field_v4_2.json /tmp/x/audit.csv   # grille des coachs (doctrine codée)

Jeu de données de l'application : `python -m spinsacademy.field --version <version>` (depuis la racine du dépôt), puis
contrôle et publication dans l'administration (`exploit_field`).

Données : `hrcdata.load` lit `data/hrc/raw/<dossier>/hand_<n>` (correspondance des clés `3w`, `hu`, `3wc`, `huc`, `c2` :
`data/hrc/README.md`) ; la matrice d'équités est celle de l'application (`spinsacademy/data/equity_169.npy`). La
variable `EXPRESSO_DATA` garde l'ancienne arborescence `hrc/x/<clé>/Hand_<n>` et `E3.npy`.

## Corrections v4.2

1. Limp du SB en heads-up : EV estimée contre le vilain (`exploit_engine.limp_ev`) au lieu de la borne basse HRC.
2. « Quelle pastille ? » : rec passif et reg séparés ; 40, 80 ou 150 occasions.
3. Pièges : vilain à 5 points ou plus du GTO, marge entre 3 et 10 × le bruit.
4. Pas d'adaptation sur une main que HRC joue déjà 30 % du temps.
5. R2 à 6 BB et moins : 80 occasions.
6. BvB : limp en borne basse ; pas de piège « fold au BTN » à 10 BB et plus ; texte de R0.
7. Chaque question porte les actions acceptées (moins de 1 × bruit), la fréquence HRC de la réponse et, au SB, la fréquence d'iso du BB.

`export_app.py` et `quiz_export_v2.schema.json` (export v2 de la v4.1) sont gardés pour mémoire : l'application lit le
format de `spinsacademy/field.py`.
