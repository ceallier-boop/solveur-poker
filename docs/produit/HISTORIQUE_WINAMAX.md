# Historique de mains Winamax : récupération et calibrage du field (05/11/2026)

Débloque E3 (rec passif face au limp) et M4 (calibrage des facteurs et des parts du field). Outils : `tools/field/winamax_counts.py` (lecture des mains, chez le porteur du projet) et `tools/field/calibrate_profiles.py` (calibrage, dans le projet).

## 1. Ce que le porteur du projet récupère

| Élément | Précision |
|---|---|
| Dossier | L'historique des mains du client Winamax. Sous Windows, il est en général dans `C:/Users/<nom>/AppData/Roaming/winamax/documents/accounts/<compte>/history` (dossier caché : coller `%APPDATA%/winamax` dans la barre de l'explorateur). Si ce n'est pas là, le client indique le dossier dans ses réglages d'historique des mains. |
| Fichiers | Les `.txt` des tournois (un fichier par Expresso). Les fichiers `…_summary.txt` sont ignorés. On peut donner le dossier `accounts` entier ou une archive `.zip` : les sous-dossiers sont lus. |
| Période | Le plus récent possible, sur 6 à 12 mois : le field change avec le temps. Mélanger les buy-ins n'est pas gênant, le rapport donne les volumes. |
| Volume | Au moins **20 000 mains Expresso** (environ 1 000 tournois) pour les facteurs « tapis en premier » et « payer un tapis » de 6 à 12 BB ; **50 000 et plus** pour les cases rares (payer un tapis à 4 BB, isoler un limp, payer après son limp) et la répartition des adversaires. Le rapport dit, case par case, ce qui est atteint. |

Les fichiers bruts restent sur l'ordinateur du porteur du projet : ils ne sont ni envoyés ni versionnés.

## 2. Procédure (Windows)

1. Installer Python 3.9 ou plus récent depuis python.org (cocher « Add python.exe to PATH »). Aucune autre installation.
2. Depuis le dépôt cloné (à jour), ouvrir un terminal à sa racine. Sans le dépôt, le seul fichier `tools/field/winamax_counts.py` suffit.
3. Lancer :

   ```
   py tools/field/winamax_counts.py "C:/Users/<nom>/AppData/Roaming/winamax/documents/accounts" --sortie comptages_winamax
   ```

4. Le terminal affiche le rapport. Le dossier `comptages_winamax` contient 5 fichiers sans aucun pseudo : `comptages.csv`, `volume.csv`, `adversaires.csv`, `rapport.txt`, `rapport.json`. Les envoyer au projet.

## 3. Ce que fait le lecteur

- Ne lit que les Expresso (y compris Nitro) en argent réel ; `--tous-formats` lit les autres tournois.
- Repère le héros (« Dealt to ») et ne compte que ses adversaires : le field, jamais le joueur lui-même.
- Compte, pour chaque décision préflop (heads-up et 3 joueurs : premier à parler, face à un limp, à un open, à un tapis, après son limp) et chaque tapis effectif ramené aux cases du moteur (2, 4, 6, 8, 10, 12, 15, 18, 20, 25 BB), le nombre d'occasions et d'actions (fold, limp, check, paie, relance, tapis).
- **Confidentialité** : les pseudos ne servent qu'en mémoire. Aucun pseudo, numéro de main, de table ou de tournoi, aucune date plus fine que le mois n'est écrit, et le programme refuse d'écrire un fichier où un pseudo apparaîtrait. La répartition des adversaires est donnée par cases d'au moins 5 joueurs. Conforme à `docs/exploitation/SECURITE.md` : aucune donnée de vrais adversaires dans l'application ni dans le dépôt (seuls des comptages agrégés y entrent).
- Bibliothèque standard de Python seulement ; chemins en « / » ou « \ » ; aucun processus parallèle.

## 4. Contrôle de volume

`volume.csv` donne, pour chaque paramètre des profils et chaque tapis, les occasions et un statut :

| Statut | Occasions | Usage |
|---|---|---|
| fiable | 200 et plus | facteur mesuré à environ ± 15 % : remplace l'hypothèse des coachs |
| indicatif | 50 à 199 | tendance, combinée à l'hypothèse |
| insuffisant | moins de 50 | l'hypothèse des coachs reste |

| Paramètre (`profils_field.py`) | Décisions comptées | Calibrable |
|---|---|---|
| shove (tapis en premier) | BTN premier à parler, SB après fold du BTN, SB en heads-up | oui, de 4 à 15 BB (la référence n'a plus de tapis en premier à partir de 18 BB) |
| call (payer un tapis) | SB et BB face au tapis du BTN, BB face au tapis du SB | oui, de 4 à 15 BB (au-delà, les calls de la référence ne bougent plus) |
| limp_k (limp du SB) | SB premier à parler (heads-up, BvB) | comptage oui ; le facteur demande la fréquence de limp de la référence, à brancher |
| iso | BB face au limp du SB | idem |
| call du tapis après limp (E3) | SB face au tapis du BB après son limp | idem |
| parts du field (5 profils) | `adversaires.csv` | partiel : seuls les adversaires vus souvent (50 tapis possibles, 20 calls possibles) entrent ; les réguliers y sont surreprésentés |

## 5. Calibrage (dans le projet)

```
python tools/field/calibrate_profiles.py comptages_winamax/comptages.csv
```

Sortie : facteur mesuré du field par type et par tapis, avec intervalle de confiance, en face du rec passif supposé, puis une pente sur le tapis. Validé sur 18 000 mains simulées avec des facteurs connus (tapis 0,6 et call 0,7) : facteurs retrouvés dans l'intervalle à 6, 8 et 12 BB. Les comptages reçus (sans pseudo) peuvent être versionnés dans `data/field/comptages/<date>/`.
