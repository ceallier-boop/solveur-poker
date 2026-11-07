# Calibrage du field sur l'historique du porteur du projet (07/11/2026)

Données : `data/field/winamax/2026-11-07/` (winamax_counts 1.0.0) : 569 mains Expresso (243 en heads-up, 326 à 3 joueurs), 63 adversaires, mars 2025 à novembre 2026. Calcul : `python tools/field/calibrate_profiles.py data/field/winamax/2026-11-07/comptages.csv`. **Aucun facteur de profil n'a été modifié.**

Correction faite avant le calcul : une action jamais observée dans une case (par exemple aucun tapis du BTN à 10 BB) n'avait pas de ligne dans `comptages.csv`, et ses occasions étaient perdues pour le calibrage. Cela poussait le facteur de tapis vers le haut (0,50 au lieu de 0,38). Le calibrage lit désormais ces occasions avec k = 0, et le lecteur 1.0.1 écrit la ligne.

## 1. Ce que dit le calibrage

Facteur = multiplicateur des cotes de la fréquence de la référence (1 = la théorie ; moins de 1 = plus serré). Intervalle de confiance à 95 %.

| Paramètre | Mesuré, toutes profondeurs de 4 à 15 BB | Occasions | Hypothèse des coachs (rec passif) |
|---|---|---|---|
| shove (tapis en premier) | **0,38 (0,27 à 0,53)** | 270 | 1,0 à 4 BB, 0,8 à 8 BB, 0,6 à 12-15 BB |
| call (payer un tapis) | 0,66 (0,33 à 1,32) | 41 | 1,5 à 4 BB, 1,0 à 6 BB, 0,7 à 8 BB, 0,6 à 12 BB |

Par profondeur (cases d'au moins 5 occasions) : tapis 0,56 (0,24 à 1,30) à 4 BB, 0,30 (0,14 à 0,65) à 6 BB, 0,39 (0,20 à 0,77) à 8 BB, 0,22 (0,08 à 0,61) à 10 BB, 0,36 (0,14 à 0,91) à 12 BB, 0,72 (0,26 à 2,01) à 15 BB. Call : 0,42 (0,15 à 1,13) à 4 BB ; de 6 à 12 BB, 5 à 9 occasions par case, intervalles de 0,1 à 15.

Lecture :
- **Tapis en premier** : seul résultat net. Le field observé part à tapis en premier nettement moins que la théorie (cotes × 0,4 environ), et aussi moins que l'hypothèse des coachs à 4-10 BB. Le sens confirme la doctrine (« les recs jamment peu »), mais l'ampleur est plus forte. Aucune pente sur la profondeur ne se dégage (× 1,02 par 4 BB).
- **Payer un tapis** : rien de concluant. L'intervalle (0,33 à 1,32) contient la théorie et toute la plage des coachs. Le seul indice est à 4 BB : 0,42, alors que les coachs supposent 1,5 (« à 4 BB le field paie tout »). C'est à vérifier avec plus de mains, pas à appliquer.
- **Prudence** : les 270 occasions viennent de 63 adversaires, et un même joueur pèse plusieurs fois, donc les intervalles réels sont plus larges que ceux affichés. La référence est celle des exports actuels (ouvertures à 2,3 et 3,5 BB). Un field qui min-raise au lieu de pousser fait baisser le facteur de tapis : la colonne « open » des comptages le montre à 8-25 BB.

## 2. Ce qui reste de l'hypothèse des coachs

Tout, pour l'instant, dans le moteur. Aucun paramètre n'atteint « fiable » (200 occasions par profondeur) :
- shove : mesure nette, toutes profondeurs ensemble seulement. À confirmer avant de toucher `FIELD_REC`.
- call, limp_k, iso, call du tapis après limp (E3) : hypothèse des coachs, mesure inexploitable (12 à 147 occasions sur toutes les profondeurs).
- Parts des 5 profils : aucun adversaire assez observé (0 sur 63).
- Profils autres que le rec passif (station, dégène, nit, reg) : hypothèses, non mesurables avec des comptages de population.

## 3. Volume minimal réaliste

Estimé au rythme de cet historique (occasions par main pour chaque paramètre), pour 200 occasions :

| Paramètre | Un facteur commun de 4 à 15 BB | Un facteur par profondeur (profondeur médiane) | Toutes les profondeurs de 4 à 15 BB |
|---|---|---|---|
| shove, open | 500 mains | 2 500 | 5 000 |
| limp_k (limp du SB) | 800 | 4 000 | 9 000 |
| call (payer un tapis) | 3 000 | 25 000 | plus de 100 000 |
| iso (le BB isole un limp) | 3 000 | 15 000 | 30 000 |
| call du tapis après limp (E3) | 10 000 | 40 000 | plus de 200 000 |
| parts des profils | adversaires vus au moins 50 fois sur des tapis possibles : plusieurs dizaines de milliers de mains | | |

Objectif réaliste : **30 000 à 50 000 mains Expresso**. Avec ce volume, shove, open et limp sont fiables à chaque profondeur, call et iso le deviennent avec un facteur et une pente, et E3 est indicatif. Le « call à chaque profondeur » demanderait plus de 100 000 mains.

## 4. Obtenir plus de mains : les experts

Lucho, Lucky et PA ont probablement de grosses bases Expresso. Le lecteur ne sort que des comptages agrégés sans pseudo, et les comptages de plusieurs joueurs s'additionnent (même format, même version). Leur propre jeu n'est jamais compté : seuls leurs adversaires le sont.

Message à leur transmettre :

> Bonjour, on cale le comportement moyen du field Expresso (fréquences de tapis, de call, de limp selon la profondeur) pour l'entraînement de SpinAcademy. Si tu as un historique Winamax, un petit programme le lit chez toi et ne produit que des totaux anonymes : aucun pseudo, aucun numéro de main ni de tournoi, et ton propre jeu n'est pas compté. Tes fichiers ne quittent pas ton ordinateur ; seuls 5 petits fichiers de totaux nous sont envoyés. Merci !

Procédure (5 lignes) :

1. Installer Python 3.9 ou plus récent (python.org, cocher « Add python.exe to PATH »).
2. Enregistrer le fichier `winamax_counts.py` fourni dans un dossier.
3. Dans ce dossier, lancer : `py winamax_counts.py "C:/Users/<nom>/AppData/Roaming/winamax/documents/accounts" --sortie comptages` (ou le dossier d'historique indiqué dans les réglages du client Winamax).
4. Le terminal affiche un rapport. Le dossier `comptages` contient 5 fichiers sans aucun pseudo.
5. Envoyer ces 5 fichiers.

Le projet additionne les comptages reçus, puis relance le calibrage. Les calculs verrouillés (Moteur profil) attendent un volume fiable.
