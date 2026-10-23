# SpinsAcademy : audit de l'existant (phase 0)

Date : 12 octobre 2026. Périmètre : les cinq archives transmises (`tensor3.zip`, `flop_lines.zip`, et les trois archives d'exports de référence (complément 1, complément 2, min-raise à 3 joueurs et heads-up)) et le cahier des charges `Cahier_des_charges_SpinsAcademy.docx` v1.0.
La conversation partagée sur claude.ai n'a pas pu être lue, car la page est bloquée par une protection anti-robots. L'audit porte donc sur les fichiers seuls.

## 1. Inventaire

`flop_lines.zip` contient tous les fichiers de `tensor3.zip`, à l'identique (vérifié octet par octet), sauf `exploit_scenarios.csv`.

| Fichier | Rôle | État |
|---|---|---|
| `pushfold.py` | Évaluateur 7 cartes, matrice d'équité 169 × 169 (Monte-Carlo), push/fold heads-up | Exécuté. Retrouve l'équilibre de Nash connu (10 BB : SB 57,8 %, BB 37,3 %) |
| `pushfold_raise.py`, `solver2.py`, `solver3_iso.py` | Heads-up avec open 2 BB, limp et iso-raise. CFR+ | Postflop **approximé** (alpha = 0,35, beta = 0,03), open à 2 BB au lieu de 3,5 BB chez la référence : à abandonner au profit de la référence |
| `tensor3.py` | Tenseur d'équité à 3 mains (169³) | Correct. Fichier `T3.npy` non fourni, à recalculer |
| `solver3h.py`, `solver_uneq.py` | Push/fold à 3 joueurs, stacks égaux et inégaux (pots annexes) | Logique relue, cohérente. Utile sous 8 BB et comme repli |
| `hrc_surrogate.py` | Modèle « corrigé » : stratégies de référence interpolées entre profondeurs | **Ne tourne pas** : dépend de `hrcdata.py` et `E3.npy`, absents |
| `regret_stats.py`, `flop_lines.py`, `export_ranges.py` | Statistiques de regret contre la référence, lignes atteignant le flop, export des ranges | **Ne tournent pas** : `hrcdata.py`, `eval_vs_hrc.py` et `scorecard.py` sont absents |
| `scorecard.csv` | Comparaison chiffrée modèle / référence (MAE, accord, regret) | Données présentes |
| `spinsacademy_quiz_export.json` | 297 questions exploitantes (7 spots, 4 à 12 BB) | Recontrôlé contre la référence (voir §3) |
| `exploit_scenarios.csv` | 42 808 scénarios (169 mains × spots × 4 profils × 2 intensités) | Cohérence interne vérifiée (voir §3) |
| `postflop_package/` | Noyau postflop (1 326 combos, équité exacte, catégories, tirages, profils pédagogiques), tests | **Tests exécutés : 0 échec** |
| `ranges_*.md`, `fiche_*.pdf`, `guide_comportement_expresso.md` | Documents pédagogiques | Sources mélangées (voir §3) |
| Bases de référence (44 mains) | Exports de référence `settings.json` + `nodes/*.json` | Analysées (voir §2) |

**Scripts absents, indispensables pour reproduire ce qui a été produit :** `hrcdata.py`, `eval_vs_hrc.py`, `scorecard.py`, `quiz_generator.py`, `verify_quiz.py`, le « moteur exploitant v2 » (qui calcule `exploit_scenarios.csv` et les seuils de bruit) et `E3.npy`. Sans eux, le quiz et le CSV ne sont ni régénérables ni traçables, ce que le cahier des charges exige (§5.1 et §16).

## 2. Base de référence

- 44 mains exportées, 325 nœuds, toutes préflop. Configuration : chip EV, sans rake, blinds 0,5 / 1, ante à 0, moteur de référence Monte-Carlo (abstraction postflop à 256 buckets).
- Couverture à 3 joueurs : stacks égaux 4, 6, 8, 10, 12, 14, 15, 18, 20 et 25 BB, plus 18 répartitions inégales. Couverture heads-up : 2, 4, 6, 8, 10, 12, 15, 18, 20 et 25 BB, plus 3 répartitions inégales.
- Tailles d'arbre : open du BTN à 2,3 BB, open du SB à 3,5 BB, iso-raise du BB à 3 BB, puis all-in.
- **Deux arbres différents coexistent.** La base « Min-raise-3way » interdit le limp du BTN (`ALLOWED_FLATS_PER_RAISE[0] = 0`). Les bases « Complement » et « Complement2 » l'autorisent. Les deux existent à 12 BB × 3.
- **Exports partiels.** Beaucoup d'actions n'ont pas de nœud fils (par exemple la réponse du SB à un iso-raise). Les lignes plus profondes ne sont pas disponibles.
- **Précision.** Pour environ 10 % de la masse (main × nœud), les deux meilleures actions sont à moins de 20 mBB d'écart. Dans 108 cas, de référence joue une action à plus de 90 % alors que sa propre EV la place à plus de 50 mBB de la meilleure. Ce sont des traces de convergence Monte-Carlo, surtout aux nœuds de profondeur 2.

**Conséquence pour l'application :** corriger d'après l'EV (regret en mBB) avec une tolérance, et non d'après « l'action la plus fréquente ». Les nœuds peu fiables doivent être signalés ou exclus.

## 3. Constats et incompatibilités

1. **Trois sources « GTO » se côtoient.** Ce sont le push/fold maison, de référence brut et la référence interpolé (« modèle corrigé »). Les fiches PDF les mélangent dans un même tableau : la colonne BTN vient du modèle push/fold, la colonne SB de la référence. Le `guide_comportement_expresso.md` repose entièrement sur le push/fold maison. Or `scorecard.csv` montre qu'en heads-up, le modèle push/fold n'est d'accord avec la référence que dans 65 % des cas à 8 BB, 36 % à 10 BB et 22 % à 12 BB.
2. **La fiche v2 est périmée.** Elle dit que 4 et 6 BB à 3 joueurs, ainsi que 15 BB, ne sont pas couverts par la référence. Les bases « Complement » les couvrent pourtant.
3. **Le quiz est restreint au tout ou rien.** Les réponses GTO du quiz correspondent à l'action majoritaire de référence dans 216 questions sur 217. Mais entre 10 et 12 BB, 32 questions de type « pousse ou fold » portent sur des nœuds où la référence joue aussi le limp ou le raise. Dans 3 cas, une option non proposée a la meilleure EV (par exemple 43s au SB à 10 BB : limp +59 mBB, all-in +46 mBB). Cela contredit le §4.2 du cahier des charges : les options proposées ne sont pas les options réelles.
4. **Le profil « Shark (référence) » devrait donner zéro adaptation.** Il produit pourtant 156 changements d'action, dont 18 classés « légère ». La référence du moteur exploitant (les ranges d'équilibre qu'il utilise) n'est donc pas exactement celle du solveur de référence.
5. **Les seuils de bruit sont élevés** : 242 mBB à 10 BB et 332 mBB à 12 BB, contre 37 mBB à 4 BB. Ce sont ceux du moteur exploitant, non documentés en l'absence du script.
6. **`hrc_surrogate` fait la moyenne de deux arbres différents** à 12 BB (avec et sans limp du BTN). Il interpole aussi des stratégies entre profondeurs, ce qui est une heuristique et non un équilibre. C'est acceptable si c'est étiqueté comme approximation, jamais comme « la référence ».
7. **Postflop, deux défauts de définition.**
   - Sur board pairé ou brelan, la catégorie brute est comptée comme « mains fortes ». Exemples : 33 sur K-K-5 compte comme « deux paires » ; 23 sur 7-7-7 compte comme « brelan ». L'avantage de mains fortes est faussé sur ces boards.
   - L'« amélioration » compte une turn qui paire le board. Pour AK sur K-8-3, 6 des 11 cartes d'« amélioration » ne font que pairer le board. Le cahier des charges (§8.3) demande justement de définir ce terme.
8. **Performance postflop.** L'équité exacte prend 4 s pour deux ranges de 1 200 combos sur un flop. Il faudra un précalcul et un cache, pas de calcul à la demande.
9. **Modèle de gains.** Tout est en chip EV, ce qui n'est juste que si le gagnant prend tout. Pour les multiplicateurs qui paient plusieurs places, il faut l'ICM. À afficher comme hypothèse.
10. **Profondeurs de départ.** L'Expresso démarre vers 25 BB, mais le quiz ne couvre que 4 à 12 BB. Les données de référence de 14 à 25 BB existent sans être exploitées.
11. **Hygiène des scripts.** Chemins codés en dur (`/home/claude/...`), aucune dépendance déclarée (numpy, numba), pas de structure de package, code mort (`if False`).

## 4. Recommandations

| Élément | Décision |
|---|---|
| Bases de référence | **Conserver comme référence unique du mode GTO.** Normaliser vers un format de scénario versionné (identifiant d'arbre, empreinte des réglages, main de référence source) |
| Noyau postflop | **Conserver**, corriger les deux définitions (§3.7) et ajouter un précalcul |
| `pushfold.py`, `solver3h.py`, `solver_uneq.py`, `tensor3.py` | **Conserver** comme moteur de repli et d'exploitation sous 8 BB, après mise en package, tests et suppression des chemins en dur |
| `pushfold_raise.py`, `solver2.py`, `solver3_iso.py` | **Archiver** (postflop heuristique, tailles différentes de la référence) |
| `hrc_surrogate.py` | **Conserver après récupération de ses dépendances**, avec étiquetage « interpolé » |
| Quiz exporté | **Conserver comme jeu de démarrage**, après retrait ou correction des 32 questions de 10–12 BB à options incomplètes, et régénération traçable |
| Fiches et guide | **À régénérer** depuis la source unique |

---

## 5. Complément après réception de l'archive complète (`tout_le_travail_expresso.zip`)

Décisions du propriétaire :
- le GTO couvre 4 à 25 BB, avec limp et raise ;
- on reste en chip EV ;
- les exports de référence vont dans le dépôt (`data/hrc/raw/`) mais jamais dans l'application.

### 5.1 Ce qui a été reproduit

| Chaîne | Résultat |
|---|---|
| `hrcdata` → `hrc_surrogate` → `exploit_engine` | Tourne avec `E3.npy` recalculé. 42 808 lignes, dont 42 784 décisions exploitantes identiques à l'original. Les 24 écarts viennent du tirage Monte-Carlo de la matrice d'équité |
| `quiz_generator` → `verify_quiz` | **0 échec**. Il génère 287 questions. Les réponses sont identiques sur les 166 questions communes avec l'original ; le tirage aléatoire change avec les pools |
| `loo_eval` (stack retiré puis interpolé) | Perte nette de 8 à 64 mBB par main contre la référence, pour un plancher de référence de 0,4 à 19 mBB |
| `exp_hu_solver` (heads-up limp/raise, jeu après le flop calibré sur la référence) | Perte de 4 à 6 mBB à 6 BB et de 12 à 13 mBB à 8 BB, mais **30 à 50 mBB à 10–12 BB** |
| Paquet postflop v2 (avec `postflop_quiz`) | 181 questions. Seules **4 questions « mains fortes »** sont sur un board pairé (défaut §3.7). Aucune question « amélioration » n'est produite |

Le point 4 du §3 (profil Shark) est traité dans `quiz_generator` : les mains où Shark change la décision sont exclues des questions. Les seuils de bruit sont documentés dans `exploit_engine` : ce sont les gains parasites du profil Shark au 90ᵉ centile.

### 5.2 Ce qu'on garde, au vu des décisions

| Élément | Usage dans SpinsAcademy |
|---|---|
| **Exports de référence (44 mains)** | **Seule source du mode GTO**, limp et raise compris. On n'utilise que les profondeurs résolues. 3 joueurs : 4, 6, 8, 10, 12, 14, 15, 18, 20, 25 BB et 18 répartitions inégales. Heads-up : 2, 4, 6, 8, 10, 12, 15, 18, 20, 25 BB et 3 inégales. La correction se fait d'après l'EV de référence, avec une tolérance au moins égale au plancher de référence (≈ 20 mBB) |
| `hrcdata.py` | Logique de lecture à reprendre dans l'importeur (clés de nœud, étiquettes d'action, all-in) |
| `hrc_surrogate.fill_unreached` | À garder pour les mains non atteintes, mais **pas l'interpolation entre stacks** dans le mode GTO (perte de 8 à 64 mBB) |
| `exploit_engine.py`, `quiz_generator.py`, `verify_quiz.py`, `quiz_export.schema.json`, `spinsacademy_quiz.sqlite` | **Mode exploitant pour les décisions tout ou rien**, à toutes les profondeurs où la référence a la situation. La méthode différentielle (EV de référence + décalage calculé par les équités), les seuils de bruit, les pièges et la vérification sont bons. À étendre à 14–25 BB, et à afficher les options limp et raise avec leur EV GTO |
| `calibrate_profiles.py` + gabarit CSV | Calibration des profils sur des comptages observés, à garder pour plus tard |
| `crsolve.py`, `solver3h.py`, `solver_uneq.py`, `tensor3.py`, `pushfold.py` | Moteur push/fold avec bloqueurs : référence et contrôle sous 8 BB, module pédagogique « push/fold » distinct du GTO |
| `exp_hu_solver.py` + `solver_hu.py` | Exploitant heads-up limp/raise **jusqu'à 8 BB seulement**. Au-delà, l'erreur dépasse les écarts qu'on veut enseigner |
| Paquet postflop v2 (`postflop_core`, `postflop_quiz`, vérifications, tests exhaustifs) | À garder intégralement, avec les 2 corrections du §3.7. Les 4 questions sur board pairé sont à régénérer ensuite |
| `scorecard.csv`, `regret_stats`, `loo_*`, `eval_c2` | Rapports de validation historiques, à archiver |
| `Guide_final_Expresso.md`, fiches PDF v1 à v5, `ranges_*.md` | **Ne pas reprendre tels quels** : ils sont en push/fold pur ou mélangent les sources. À régénérer depuis la référence |
| `pushfold_raise.py`, `solver2.py`, `solver3_iso.py`, `model_pages.py` | À archiver |

### 5.3 Exploitant avec limp et raise de 10 à 25 BB

Aucun script fourni ne le fait de façon fiable : `exploit_engine` exclut volontairement ces lignes, et `exp_hu_solver` ne tient pas au-delà de 8 BB. La voie recommandée est le **verrouillage de nœuds dans la référence** : on fige la stratégie du vilain selon un profil, puis le solveur de référence calcule la meilleure réponse du héros. Ces exports « exploitants » suivraient le même import, la même validation et le même versionnage que les exports GTO.

### 5.4 Point juridique à confirmer

Les exports bruts restent hors de l'application. En revanche, les datasets publiés en contiendront des **dérivés** : fréquences, EV, ranges et questions. Il faut confirmer que la licence de référence autorise cette diffusion dérivée.
