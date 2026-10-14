# Veille forums Spin & Go / Expresso : outils concurrents et données de calage (2026-10-14)

Objet : recenser les forums qui parlent de Spin & Go et d'Expresso, en tirer (1) les outils concurrents de SpinsAcademy et (2) les données publiques utilisables comme référence pour caler le modèle des mains (ranges de référence, profils fictifs du mode exploitant, `docs/dataset/EXPLOIT_CALLS.md`).

Méthode : recherches web le 14/10/2026. Club Poker et Two Plus Two refusent la lecture automatique (HTTP 403) : pour ces forums, seuls les titres et extraits des moteurs de recherche ont été exploités. Les chiffres cités viennent pour la plupart de sites commerciaux et **ne sont pas audités** ; ils doivent être relus par l'expert poker avant tout usage (cahier des charges §1.3 et §7).

## 1. Forums et communautés recensés

| Forum / communauté | Langue | Fils pertinents trouvés | Intérêt |
|---|---|---|---|
| **Club Poker** (clubpoker.net), section « Outils et logiciels » | FR | [SpinSensei — tracker de Spin & Go](https://www.clubpoker.net/forum-poker/topic/246342-spinsensei-%E2%80%94-tracker-de-spin-go/) ; [Poker Sciences — tracker français spécialisé Spin et trainer préflop](https://www.clubpoker.net/forum-poker/topic/246315-poker-sciences-tracker-fran%C3%A7ais-sp%C3%A9cialis%C3%A9-en-spin-et-trainer-pr%C3%A9flop/) ; [PreflopHero lancement français](https://www.clubpoker.net/forum-poker/topic/235433-preflophero-lancement-fran%C3%A7ais/) ; [Les solvers](https://www.clubpoker.net/forum-poker/topic/226398-les-solvers/) ; [Quels logiciels pour bosser son jeu de MTT](https://www.clubpoker.net/forum-poker/topic/240943-quels-logiciels-pour-bosser-son-jeu-de-mtt/) | Annonces d'outils concurrents francophones, retours d'utilisateurs |
| Club Poker, autres sections | FR | [Théorie Spin&Go (Expresso Nitro)](https://www.clubpoker.net/forum-poker/topic/242743-th%C3%A9orie-spingo-expresso-nitro/) ; [Calculs simplifiés pour les expressos](https://www.clubpoker.net/forum-poker/topic/226699-calculs-simplifi%C3%A9s-pour-les-expressos/) ; [Impôt grindeur spin/expresso](https://www.clubpoker.net/forum-poker/topic/241008-imp%C3%B4t-grindeur-spinexpresso/) | Un membre y décrit vingt résolutions solveur 3 joueurs puis heads-up, contrôlées par un calcul push/fold maison : même démarche que notre `pushfold.py` |
| **Poker Académie** (poker-academie.com/forum) | FR | [Icmizer et Winamax](https://www.poker-academie.com/forum/t/icmizer-et-winamax/78028) (ancien : ICMizer n'importait pas les historiques Winamax) | Communauté FR avec vidéos Spin ; peu d'outillage spécifique Expresso |
| **PokerStrategy** (FR et EN) | FR/EN | [Comparaison d'un push sous PT4, ICM Trainer et SnG EGT](https://www.pokerstrategy.com/fr/forum/outils-de-poker-336/comparaison-dune-situation-de-push-sous-pt4-icm-trainer-et-sngegt-135327/) ; [Spin and go how to analyze](https://www.pokerstrategy.com/forum/sit-and-go-tournaments-1428/spin-and-go-how-to-analyze-473142/) | Désaccords entre outils push/fold selon les ranges de call supposées ; hypothèses qualitatives sur la population micro (pousse plus serré, paie un peu trop) |
| **Two Plus Two**, sous-forum « Heads Up SNG and Spin and Gos » | EN | [Gto solver for spins](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/gto-solver-spins-1778193/) ; [Population tendencies in Spins](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/population-tendencies-spins-1626102/) ; [Using PT4 to analyse population tendencies](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/help-using-pt4-analyse-population-tendencies-1208561/) ; [Spin and go HU calling ranges 5-12bb](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/spin-go-hu-calling-ranges-5-12bb-1779941/) ; [About GTO+](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/about-gto-1751890/) | Méthode de construction de stats de population ; HRC jugé meilleur solveur préflop pour les spins (2024) |
| Two Plus Two, « Poker Software » et « Poker Theory » | EN | [GTO Wizard all-in-one (p. 5)](https://forumserver.twoplustwo.com/167/poker-software/gto-wizard-ultimate-all-one-gto-tool-browse-solutions-practice-gto-analyze-hhs-1780811/index5.html) ; [Pourquoi GTO Wizard diffère de HRC sur ce spot](https://forumserver.twoplustwo.com/15/poker-theory-amp-gto/why-does-gto-wizards-preflop-strategy-spot-differ-so-dramatically-hrc-solve-1849913/) ; [1 million spin&go and math behind it](https://forumserver.twoplustwo.com/28/discussion-poker-sites/1-million-spin-amp-go-math-behind-1531529/) | Écarts HRC / GTO Wizard (utile pour expliquer nos écarts de référence) |
| **Run It Once** | EN | [ICMizer/HRC different results](https://www.runitonce.com/mtt/icmizerhrc-different-results/) | HRC 26 % de tapis contre ICMizer nettement plus serré : réglages FGS en cause |
| **TournamentPokerEdge** | EN | [Adjusting Nash ranges as exploits](https://www.tournamentpokeredge.com/forum/mtt-poker-strategy/adjusting-nash-ranges-as-exploits/) ; [How to assume opponents' shoving/calling range from data](https://tournamentpokeredge.com/forum/mtt-poker-strategy/how-to-assume-opponents-shovingcalling-range-from-the-data-i-have) | Thèse inverse : la population paie *trop serré* (hors spins) |
| PokerTracker forum | EN | [Spin&go stats](https://www.pokertracker.com/forums/viewtopic.php?f=61&p=283910) | Définition des stats spin dans PT4 |
| Discord | FR/EN | Smart Spin Official ; Discord Poker Académie ; canal privé Poker Spin Tracker ; bitB Spins DoJo | Non indexés : à suivre manuellement |

Aucun forum Winamax public actif dédié à l'Expresso n'a été trouvé : la discussion francophone passe par Club Poker, Poker Académie et les Discord des écoles.

## 2. Outils concurrents

Légende de proximité avec SpinsAcademy (trainer mobile préflop Spin & Go / Expresso, référence HRC, mode exploitant à profils fictifs) : ●●● concurrent direct, ●● partiel, ● voisin.

### 2.1 Trainers et packs de ranges Spin & Go

| Outil | Proximité | Ce qu'il fait | Points à noter |
|---|---|---|---|
| **Poker Sciences / Poker Spin Tracker – Study Pack** ([offre](https://app.pokersciences.com/en/offers/preflop-pack)) | ●●● | 401 charts sur 24 situations spin (3-max et HU), chacune en version « GTO » (contre regs) et « Exploit » (contre récréatifs) ; trainer en 34 chapitres (campagne, mode hardcore près des seuils, chronomètre, arène quotidienne, rejeu des erreurs) ; tracker qui compare les mains importées aux charts. 390 € à vie ; desktop. | Français, annoncé sur Club Poker ; charts exploit construits « avec HRC sur plus d'un million de mains contre des récréatifs » ; solveur GTO maison spécialisé spin annoncé. Le plus proche de notre offre, mais desktop et sans profils paramétrés. |
| **SpinSensei** (annonce Club Poker) | ●● | Tracker Spin & Go, solveur GTO intégré annoncé « prochainement » | Nouveau venu francophone, pas de site indexé : à surveiller. |
| **GTO Wizard** (Spins, Flash Spins, Spin + ante ; trainer ; *Player Profiles* depuis nov. 2025) | ●●● | Solutions 1–25 BB, symétriques et 600+ asymétriques, préflop et postflop, trainer, analyse d'historiques ; profils Fish, calling station, maniac, nit par incitations sur les actions ([PokerNews](https://www.pokernews.com/strategy/gto-wizard-player-profiles-49903.htm)). 39 à 229 $/mois. | Référence du marché ; ses profils ne sont pas calés sur des données de population (incitations fixes), comme nos profils fictifs. Préflop spin réputé calculé avec HRC (affirmation de forum). |
| **GTO Sensei** ([App Store](https://apps.apple.com/us/app/id1523876570)) | ●●● | Trainer mobile contre une IA solveur, pack Spin&Go payant (~16 $/mois) | Mobile comme nous ; pas d'Expresso ni de mode exploitant. |
| **GTO Ranges+** ([App Store](https://apps.apple.com/us/app/gto-ranges-poker-solver/id6458732631)) | ●●● | 60 spots spin 3-max, **import de sims HRC** pour s'entraîner dessus, hors ligne | Même chaîne que nous (HRC → trainer), gratuit. |
| **GTO Preflop** ([App Store](https://apps.apple.com/app/id1629141961)) | ●● | Spin 2–34 BB, stacks asymétriques, ELO | Mobile. |
| **Spin Ranges: Poker GTO+** ([Google Play](https://play.google.com/store/apps/details?id=com.spinranges.app)) | ●● | Ranges « vs Fish / vs Reg » | Mobile, dichotomie fish/reg simple. |
| **Spin Shadow Pro** ([site](https://spinshadowpro.com/)) | ●● | « Spin & Go Exploit Solver », coach IA low stakes, grille exploit 13×13 HU et 3-max, 7 profondeurs 5–25 BB | Positionné sur l'exploit, essai qui bascule en abonnement. |
| **PreflopHero Spin&Go** ([Poker Energy](https://pokerenergy.net/preflop-hero)) | ●● | Trainer de charts, choix de l'adversaire (reg/fish) et du stack | Ancien (≈ 5 ans). |
| **RangeConverter** ([spin trainer](https://rangeconverter.com/games/spin-and-go-range-viewer-and-gto-trainer)) | ●● | Visionneuse et trainer HU/3-way, rapports publics (ex. HU 10 BB limp pot) | Abonnement. |
| **FreeBetRange / charts Team BAS Poker** ([article](https://blog.freebetrange.com/article/dominate-spin-and-gos-with-tbps-premium-preflop-charts)) | ●● | Charts gratuits « basés sur les stats de population fish » et premium vs Fish / vs Reg, faits avec HRC et GTO Wizard | Affirme que les fish poussent bien plus serré que Nash. |
| **bitB Spins** (charts Nitro, Leakfinder, DoJo, Spin Academy) ([guide Nitro](https://bitb-spins.com/articles/winamax-expresso-nitro/)) | ●● | Charts Expresso Nitro maison (open 2,5x), leakfinder sur historiques, coaching | Orienté Winamax, affilié. |
| **Simple GTO**, **GTOSims**, **GTO Gecko** | ● | Packs de solutions spin (10 BB 3-max, SB vs BB 5–10 BB, 25 BB) | Contenu statique. |
| **Postflop+**, **Poker Academy** (poker.academy, import HRC, trainer « flashcards ») | ● | Trainers généralistes avec section spin | Poker Academy : spin annoncé « bientôt ». |
| **ICMIZER – MTT Coach** ([quiz Expresso Nitro](https://www.icmizer.com/quiz/winamax-expresso-nitro-3-max-hyper/)) | ●●● | Quiz push/fold avec gabarits **Winamax Expresso** et **Expresso Nitro**, classement des joueurs | Seul outil trouvé avec un quiz Expresso nommé ; push/fold ICM uniquement. |
| **SnapShove** | ● | Push/fold rapide (Nash), mobile | Simple, pas de spin 3-max avec limp. |
| **GTOkiller** ([Trustpilot](https://es.trustpilot.com/review/gtokiller.com)) | ●● | Solveur exploitant alimenté par des fréquences réelles de population (par room, limite, type de joueur) ; affiche exploit, GTO et fréquences de population côte à côte | Le modèle que notre mode exploitant pourrait viser si on obtient des données réelles. |
| **Popoch39/poker_solver** ([PR #15, 7–8 oct. 2026](https://github.com/Popoch39/poker_solver/pull/15)) | ●● | Projet libre : solveur push/fold Expresso Nitro HU et 3-max (DCFR), parseur d'historiques Winamax → Open Hand History, **modèle de population** (fréquences par nœud et tranche de stack, ranges abattues estimées par Bayes), node-locking, simulateur avec multiplicateurs 2026 | Concurrent technique très proche du mode exploitant ; contient aussi un « clicker bot » (risque CGU Winamax, ne rien en reprendre). |

### 2.2 Solveurs et calculateurs

| Outil | Rôle | Note |
|---|---|---|
| **HoldemResources Calculator (HRC)** | Notre référence. Jugé « meilleur solveur préflop » pour les spins sur 2+2 ; recommandé sur Club Poker pour son rapport utilité/prix | Écarts connus avec ICMizer (réglages FGS) et GTO Wizard (arbres) |
| **ICMIZER** | Push/fold Nash ICM, gabarits Expresso | Plus serré que HRC selon un fil Run It Once |
| **GTO+**, **PioSolver**, **Simple Postflop**, **Deepsolver**, **MonkerSolver** | Postflop | Hors périmètre actuel (préflop) |
| **SnG EGT**, **ICM Trainer** | Push/fold SNG anciens | Cités dans le fil PokerStrategy |

### 2.3 Trackers, HUD et analyse de population (sources de données potentielles plutôt que concurrents)

Hand2Note (rapports multi-joueurs, HUD SpinNGo), PokerTracker 4, MDA « End Boss » et HUD Xtreme (Team BAS), +EV Spin&Go HUD (PT4), Smart EV (popups H2N), Poker Spin Tracker (Poker Sciences), SpinSensei.

## 3. Données de référence pour caler le modèle des mains

### 3.1 Fréquences de population mesurées (les seules chiffrées trouvées)

Source : [Poker Sciences, *2 Common Beginner Mistakes at Spin & Go*](https://pokersciences.com/en/learn/spin/part-3/chapter-12). Échantillon annoncé : plus d'un million de mains jouées par l'auteur en spins sur plusieurs années (tableaux A) ; échantillon non précisé pour le tableau B. GTO = GTO Wizard (arbre avec limp).

**A. Calls des récréatifs face à une agression (25 BB)**

| Situation | Récréatifs | GTO | Facteur k équivalent* |
|---|---|---|---|
| SB limp → BB iso 3x, SB paie | 76 % | 35 % | ≈ 5,9 |
| SB minraise → BB 3-bet tapis, SB paie | 65 % | 26 % | ≈ 5,3 |

**B. Open shove des récréatifs**

| Situation | Récréatifs | GTO | Facteur k équivalent* |
|---|---|---|---|
| BTN 9 BB | 15 % | 30 % | ≈ 0,41 |
| SB vs BB (3 joueurs) 11 BB | 11 % | 38 % | ≈ 0,20 |
| HU SB 7 BB | 21 % | 52 % | ≈ 0,25 |
| HU BB face au limp du SB, 13 BB | 11 % | 16 % | ≈ 0,65 |

\* k calculé avec la formule de déformation du générateur 2.0.0 (`docs/dataset/EXPLOIT_CALLS.md`) : q = k·p / (1 + (k − 1)·p), soit k = q·(1 − p) / (p·(1 − q)).

Lecture pour le projet :
- Le récréatif type pousse **beaucoup moins** que la référence (k ≈ 0,2 à 0,4 sur les open shoves), plus loin que notre profil le plus serré (Serré, k = 0,5). Prudence : le GTO cité inclut le limp et la relance, et le récréatif limpe une partie des mains que le GTO pousse ; une part de l'écart vient donc de l'arbre, pas seulement de la tendance. À comparer avec notre référence `nash_pushfold`, qui ne limpe jamais, avant d'ajouter un profil.
- Il **paie beaucoup trop** face aux relances (k ≈ 5 à 6). C'est le profil « Station d'appel (Fish) », aujourd'hui non couvert : ces chiffres justifient de l'ajouter (situations où le héros pousse ou relance face à des calls trop larges).
- Concordance qualitative : Team BAS (« les fish poussent bien plus serré que Nash, donc payer plus serré que Nash ») et PokerStrategy (population micro « pousse plus serré, paie un peu trop »). Thèse contraire hors spins sur TournamentPokerEdge (la population paie trop serré face aux tapis).

### 3.2 Autres données chiffrées publiques

| Donnée | Source | Usage possible |
|---|---|---|
| VPIP de population ≈ 71 % (≈ 50 % en et hors position), Stars 3,50 $ | [2+2, plus de 10 ans](https://forumserver.twoplustwo.com/185/heads-up-sng-spin-gos/help-using-pt4-analyse-population-tendencies-1208561/) | Ordre de grandeur historique seulement |
| Repères HUD : reg TAG 18–22 % VPIP, fish ≥ 35 % (6-max) ; fish 40–100 % ; VPIP HU 42–59 % (low) et 47–63 % (high) | [Deepfold](https://deepfold.co/en/blog/hud-stats-guide), [Hand2Note](https://hand2note.com/Blog/Features/key-preflop-stats-player-profiling-and-basic-adjustments), [Smart Poker Study](https://smartpokerstudy.com/wp-content/uploads/2016/02/3.-Top-10-Poker-HUD-Stats.pdf) | Libellés des profils ; non spécifique spin |
| Taille d'échantillon : VPIP/PFR fiables vers 30–50 mains | Deepfold | Argument du niveau de confiance affiché dans la correction |
| Stats à découper par tranche de stack (10–15 BB, 7–9 BB) plutôt que globales | [VIP-Grinders](https://www.vip-grinders.com/mastering-spin-and-go-huds-5-essential-tips/) | Indexer les profils par tranche de stack |
| Fréquences d'équilibre GTO Wizard : 3 joueurs SB vs BB 15 BB (tapis 19,6 %, relance 2,5x 23,3 %, limp 19,5 %, fold 37,7 %) ; 13 BB sans limp (tapis 24,6 %, relance 2x 29,8 %, fold 45,6 %) ; HU SB 8,5 BB (tapis 36,2 %, limp 44,3 %, fold 19,5 %) | [bitB Spins](https://bitb-spins.com/articles/spin-and-go-strategy/) | Contrôle croisé de nos exports HRC aux mêmes profondeurs |
| BTN : le tapis remplace le limp vers 10 BB, limp disparu vers 8 BB (solveur) | [GTO Wizard, *Open-limping buttons*](https://blog.gtowizard.com/curious-case-of-open-limping-buttons/) | Contrôle de cohérence de l'arbre HRC |
| Écart HRC / ICMizer (26 % contre nettement moins) dû aux réglages FGS | [Run It Once](https://www.runitonce.com/mtt/icmizerhrc-different-results/) | À citer si un utilisateur compare avec ICMizer |
| Contrôle push/fold HU déjà fait dans le projet (SB 58 %, BB 37 % à 10 BB) | `docs/dataset/EXPLOIT_CALLS.md` ; charts Nash publiés (HoldemResources), vérifiés aussi par Popoch39 à 5, 8, 10, 12, 15 BB | Rien à ajouter |

### 3.3 Structure de gains Expresso (pour un futur calcul ICM)

Le projet reste en chip EV (`docs/hrc/EXPORTS_A_PRODUIRE.md` §6.5). Si l'ICM des gros multiplicateurs est rouvert : tirage d'un Expresso 5 € sur 10 000 000 parties, selon [CardPlayer](https://www.cardplayer.com/fr/poker-en-ligne/expresso-poker) (non daté, à vérifier sur [winamax.fr/expresso](https://www.winamax.fr/expresso)) : x2 59,4 %, x3 26,7 %, x4 8,25 %, x5 4 %, x10 1,5 %, x50 0,1 %, x100 0,02 %, x1 000 0,001 %, x200 000 2 sur 10 M. Jusqu'à x20 (ici x10), le vainqueur prend tout ; au-delà, partage 80 / 12 / 8 %. Expresso : 500 jetons ; Nitro : 300 jetons, niveaux d'une minute.

### 3.4 Sources de mains brutes (pour construire nos propres stats)

| Source | Contenu | Limite |
|---|---|---|
| Historiques Winamax du porteur du projet ou de testeurs volontaires | Mains réelles Expresso / Nitro | Consentement et anonymisation (RGPD) ; exclure le siège du héros comme le fait Popoch39 |
| Parseur Winamax → Open Hand History de Popoch39/poker_solver | Méthode de comptage par nœud et tranche de stack, estimation bayésienne des ranges abattues | Code tiers : vérifier la licence avant toute reprise |
| Format PHH et jeu de données ([phh-std](https://github.com/uoftcprg/phh-std), [Zenodo](https://zenodo.org/doi/10.5281/zenodo.10796885)) | Format d'historique ouvert, mains surtout de l'ACPC | Pas de mains Spin & Go |
| Rapports de population Hand2Note / PT4 / MDA | Fréquences réelles par limite et type de joueur | Licence d'outils payants ; données de l'utilisateur, pas redistribuables |

## 4. Recommandations

1. **Profils fictifs** : soumettre à l'expert les chiffres §3.1 pour (a) un profil « récréatif type » plus serré que Serré sur les tapis (k ≈ 0,3), en vérifiant d'abord l'effet de l'arbre avec limp, et (b) le profil Station d'appel (k ≈ 5) sur les décisions où le héros pousse ou relance. Les citer comme hypothèses de calage, avec leur source, jamais comme lecture d'un vrai joueur.
2. **Données propres** : le seul moyen d'avoir des fréquences auditables est de compter sur des historiques Winamax consentis, par nœud de l'arbre de référence et tranche de stack (méthode Popoch39 / GTOkiller).
3. **Différenciation** : face à Poker Sciences (desktop, 390 €) et GTO Wizard (généraliste, profils par incitations fixes), nos atouts sont le mobile, l'Expresso et le Nitro nommés, la correction traçable et des profils chiffrés et versionnés. ICMIZER Coach est le seul quiz Expresso nommé trouvé.
4. **À surveiller** : SpinSensei, le solveur maison de Poker Sciences, et les profils personnalisés annoncés par GTO Wizard.
