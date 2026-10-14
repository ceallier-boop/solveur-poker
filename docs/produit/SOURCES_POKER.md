# Sources poker : synthèse de la veille du 2026-10-14

Résumé des principaux éléments de la veille sur les forums, vidéos et outils Spin & Go / Expresso. Détail, liens et minutages : [`VEILLE_FORUMS_2026-10-14.md`](VEILLE_FORUMS_2026-10-14.md). Tous les chiffres de coachs ou de vendeurs sont **non audités** et doivent être validés par l'expert poker avant usage (cahier des charges §1.3 et §7).

## 1. Où se trouve l'information

| Type | Sources principales | Accès depuis l'environnement cloud |
|---|---|---|
| Forums FR | Club Poker (« Outils et logiciels »), Poker Académie (« Sng & Expresso »), Kill-Tilt, PokerStrategy FR | Poker Académie lisible ; Club Poker et Kill-Tilt refusent la lecture automatique |
| Forums EN | Two Plus Two (« Heads Up SNG and Spin and Gos »), PokerStrategy, Run It Once, TournamentPokerEdge | Two Plus Two refuse la lecture automatique (extraits des moteurs seulement) |
| YouTube FR | **Kill Tilt** (le plus riche sur l'Expresso), **Lucho Poker FR** (Spin highstakes exploitant), SpinElite, LUCKYSPIN, Le Wojak, Poker Académie | Sous-titres seulement (limite de débit) ; vidéos et images bloquées |
| YouTube EN | Team BAS, HUSNG, GTO Wizard, IMEZRUSPIN | Idem |
| Twitch | Chaîne Winamax (reviews pédagogiques), SpinElite (formations 2017) | **Fonctionne** : vidéos et images en 1080p ; rediffusions de lives conservées quelques semaines seulement |
| Discord | Smart Spin, SpinElite, Poker Académie, Poker Spin Tracker, bitB DoJo, Lucho Family | Non indexés, à suivre à la main |

## 2. Outils concurrents

- **Concurrents directs** :
  - **Poker Sciences / Poker Spin Tracker** (FR) : environ 300–400 charts Spin en version « GTO » et « Exploit », trainer, tracker ; 390 € ; desktop.
  - **GTO Wizard** : Spins, trainer, profils Fish / station / maniac / nit depuis nov. 2025, calculés par incitations fixes et non calés sur des données.
  - **GTO Sensei** (mobile), **GTO Ranges+** (import de calculs HRC, même chaîne que nous).
  - **ICMIZER Coach** : seul quiz Expresso et Expresso Nitro nommé trouvé.
- **Ranges « GTO + exploitantes » en français** : Spinelite (distingue les ranges contre un field et contre un profil, comme nos modes GTO et profils), Poker Toolkit (mémorisation, mobile), bitB, Team BAS via FreeBetRange, Le Wojak (gratuit + flashcards).
- **À surveiller** :
  - SpinSensei (tracker annoncé sur Club Poker) ;
  - le solveur maison de Poker Sciences ;
  - GTOkiller (solveur exploitant alimenté par des fréquences réelles) ;
  - Popoch39/poker_solver (projet libre Expresso Nitro, avec un modèle de population et un bot de clics à ne pas reprendre).
- **Nos différenciateurs** : mobile, Expresso et Nitro nommés, correction chiffrée en EV, profils explicites et versionnés. Aucun concurrent ne publie ses hypothèses de profil.

## 3. Données chiffrées pour caler les profils

| Donnée | Source | Facteur k équivalent* |
|---|---|---|
| Open shove des récréatifs : BTN 9 BB 15 % (GTO 30 %), SB vs BB 11 BB 11 % (38 %), HU SB 7 BB 21 % (52 %) | Poker Sciences (> 1 M de mains annoncé) | ≈ 0,2 à 0,4 |
| Calls des récréatifs face à une relance à 25 BB : 76 % (GTO 35 %) sur iso, 65 % (26 %) sur 3-bet tapis | Poker Sciences | ≈ 5 à 6 |
| HU 7 BB, PokerStars 100 $ : la BB paie 45 % (Nash 49 %) ; push max-exploit du SB 75 % (Nash 66 %) | HUSNG (2012) | ≈ 0,85 |
| Isolation théorique face au limp : 45–46 % à 10–20 BB ; la population « n'y arrive jamais » | Kill Tilt, Lucho | — |
| Multiplicateurs Nitro réels sur 3 487 tournois : x2 59,9 %, x3 26,0 %, x4 8,3 %, x5 4,3 %, x10 1,5 % | NitroVariance (recompté) | — |
| cEV Expresso (Lucho, 11 911 parties) : > 100 jusqu'à 2 €, 64 en 5 €, 51 en 10 € ; Nitro (Kill Tilt) : break-even ≈ 23, moyenne ≈ 25 | Lucho, Kill Tilt | — |
| Rake effectif Spin hors gros jackpots : PokerStars 7,2 %, Unibet 7,3 %, Betclic 7,8 %, Party/PMU 8,3 %, Winamax 9,3 % | Lucho (≈ 2023) | — |

\* k selon la formule du générateur `exploit_calls` : q = k·p / (1 + (k − 1)·p).

**Jeux de mains bruts** :
- SpinGPT : 320 000 décisions de regs sur 8 800 Spin PartyPoker. Disponibilité à demander aux auteurs.
- Format PHH : pas de mains Spin.
- Historiques NitroVariance : à ne pas utiliser (pas de licence, mains d'autres comptes).
- La seule source auditable reste des historiques Winamax obtenus avec consentement.

## 4. Tendances de population sur lesquelles les sources s'accordent

1. Les récréatifs **poussent trop serré entre 8 et 15 BB**, ne poussent presque jamais d'emblée au-delà de 15 BB et se rapprochent de la théorie vers 5–6 BB. Le facteur de profil devrait donc **dépendre de la profondeur et de la position**, pas être unique.
2. Face au tapis du BTN, payer moins large que la théorie (pas les bas de range) ; face au SB, rester proche de la théorie.
3. Ils **limpent beaucoup** (y compris des mains qu'ils devraient pousser) et **n'isolent pas assez** : limper très large au SB contre eux, et des ranges contre le limp sont nécessaires.
4. Ils **paient trop leurs Ax/Kx** et ne jouent pas AA assez agressivement : open jam des Ax contre un récréatif jusqu'à 15–20 BB (Lucho).
5. Face aux open shoves courts, la population folde un peu trop (Team BAS, HUSNG).
6. Un min-raise de récréatif à faible profondeur signale une main forte.
7. Le consensus des coachs : pas de charts GTO bruts contre les récréatifs, mais des ranges simplifiées et un VPIP élevé en position. « En Spin, 80 % de l'EV vient du préflop » (Lucho).

## 5. Méthode retenue pour les tableaux de range par type de jeu

- On ne déduit pas des ranges complètes des mains vues en vidéo : trop peu de mains, rien de traçable.
- Les vidéos servent à trois choses :
  - les **grilles affichées**, pour le contrôle croisé avec HRC ;
  - les **décisions commentées**, comme points de contrôle ;
  - les **règles chiffrables**, pour définir les profils.
- Le tableau exploitant est **calculé** comme la meilleure réponse en EV contre la range déformée du profil.
- **Preuve** : avec `spinsacademy/pushfold.py`, sans modification, les chiffres HUSNG sont retrouvés (Nash 66,4 % / 48,6 % ; push max-exploit 76,8 % contre une BB qui paie 45 %, 93,7 % contre 39 %, 61,7 % contre 51 %).
- **Matrice cible** : format (Expresso, Nitro, Spin 25 BB, HU) × profondeur × situation (open shove, call de tapis, puis limp / iso / min-raise) × profil (récréatif passif, récréatif agressif, nit, reg).
  - Étape 1 : push/fold jusqu'à 15 BB avec le moteur existant.
  - Étape 2 : situations avec limp, via des calculs HRC verrouillés.

## 6. Vidéos : passages et outils

- **23 passages repérés** où une range est probablement affichée : [`reperes_ranges_youtube.csv`](reperes_ranges_youtube.csv). Priorité 1 : Kill Tilt *Les clés du jeu préflop en Expresso*, *Stratégie simple et efficace*, *Les 3 principes 2026* ; Poker Académie *Le préflop en Spin* ; HUSNG *Nash vs population*. Ajout : Lucho *Améliore ton préflop* (grilles GTO Wizard vers 3:40–5:30, 9:00–11:30, 13:30–17:00).
- **Scripts** (`tools/veille/`) :
  - `youtube_subs.sh` : récupère les sous-titres ;
  - `vtt2txt.py` : convertit en texte horodaté ;
  - `extraits.py` : extrait les passages sur la population ;
  - `reperes_ranges.py` : repère les ranges affichées ;
  - `captures_ranges.sh` : capture les passages listés, à lancer sur un ordinateur personnel ;
  - `images_cles.sh` : extrait une image par changement d'écran dans une vidéo complète.
- **Récupérer les vidéos** :
  - ordinateur : `yt-dlp` (cookies du navigateur si une connexion est demandée) ;
  - téléphone : captures d'écran en 1080p dans l'application YouTube, jointes à la conversation ;
  - le plus efficace : Claude Code installé en local.
- **Fiche par main commentée** (format dans la veille §8) : source, format, stacks, main, action, décision du coach, raisonnement, profil supposé, range affichée, comparaison avec l'export HRC.

## 7. Points d'attention et prochaines étapes

- **Droits** : transcriptions, vidéos et images restent hors du dépôt (analyse interne). Pour réutiliser un contenu dans l'application, il faut l'accord des créateurs.
- **Expert validateur** : Lucho Poker FR (pro Spin highstakes francophone, exploitant, partenaire GTO Wizard, coaching) ou un coach Kill Tilt / SpinElite, à contacter.
- **Prochaines étapes proposées** :
  1. Tableaux exploitants push/fold jusqu'à 15 BB avec un facteur k par profondeur et par position.
  2. Captures des grilles prioritaires (par toi ou par Claude Code en local), puis retranscription et comparaison avec HRC.
  3. Liste de streamers Twitch Spin / Expresso actifs à suivre, avec récupération régulière de leurs rediffusions.
  4. Contacter un expert pour valider les profils.
