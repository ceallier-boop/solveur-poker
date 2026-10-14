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

## 5. Complément : recherches « spin&go », « expresso », « range GTO », « range exploitant » (2026-10-14)

Deuxième passe en français et en anglais avec ces quatre mots-clés. Elle ajoute surtout des forums francophones, des vendeurs de ranges « GTO + exploitant » et deux jeux de données réels.

### 5.1 Forums et fils supplémentaires

| Forum | Fil | Date | Ce qu'on en tire |
|---|---|---|---|
| Poker Académie, section **« Sng & Expresso »** | [Ranges en Expresso / Spin](https://www.poker-academie.com/forum/t/ranges-en-expresso-spin/91657) | 2019 | Sources de ranges citées : Spinelite (réservées aux joueurs affiliés ou stakés), SpinForWin (gratuites, débutants), « PA BOOK ». Un membre juge les ranges GTO inutiles sous 20–25 € : l'exploitation suffit aux petites limites. Pas de chiffres. |
| Poker Académie, « Sng & Expresso » | [Spin&Go 5 $ – ranges de POF et ranges de call vs shove](https://www.poker-academie.com/forum/t/spin-go-5-ranges-de-pof-et-donc-ranges-de-call-vs-shove/115433) | janv. 2025 | Range de shove SB supposée à 9 BB (22+, A2s+, K2o+, Q6o+, J8o+, T7o+, 87o, 76o) ; « le field cbet trop ». Hypothèses individuelles. |
| Poker Académie, « Sng & Expresso » | [Analyse de mes stats en Expresso](https://www.poker-academie.com/forum/t/analyse-de-mes-stats-en-expresso/89570) | déc. 2018 | Stats d'une joueuse 1–5 € : VPIP 39, PFR 28, 3-bet 9, fold vs steal 76 % ; des regs à 15 % de 3-bet et 10 % de flat entre 15 et 20 BB. Conseil des intervenants : découper les stats par position et par stack. |
| Club Poker, « Sit'n Go » | [[Expresso] Range SB > 17 BB](https://www.clubpoker.net/forum-poker/topic/228492-expresso-range-sb-17bb/) | ≈ 2017 | Ancien ; un intervenant : contre les récréatifs et en micro, jouer équilibré fait perdre beaucoup d'EV. |
| **Kill-Tilt** (kill-tilt.fr) | [[spin petites limites] 3way, défense BB, fréquence vs minraise SB/BTN](https://www.kill-tilt.fr/forums/topic/spin-petites-limites-3way-range-de-defense-bb-frequence-vs-minraise-sbbtn/) ; [Expressos ou spin & go ?](https://www.kill-tilt.fr/forums/topic/expressos-ou-spin-go/) | ? | Forum FR non recensé en première passe ; lecture automatique refusée (HTTP 406). |

### 5.2 Outils et vendeurs de ranges supplémentaires

| Outil | Proximité | Ce qu'il fait | Notes |
|---|---|---|---|
| **Poker Sciences – Ranges Spin (bibliothèque)** ([page](https://pokersciences.com/bibliotheque-tableaux)) | ●●● | ≈ 300 ranges préflop, Expresso, Spin & Rush, Spin Gold, Spin & Go ; chaque table GTO a une version exploitante, une version simplifiée et un guide ; trainer gratuit | Confirme la méthode « HRC + plus d'un million de mains contre récréatifs ». Nitro non mentionné. |
| **Spinelite** (spinelite.fr) | ●● | Structure française de coaching et staking Spin/Nitro ; ranges gratuites, ranges GTO simplifiées et exploitantes réservées aux membres ; Discord | Distingue deux types de ranges exploitantes : contre un field (inconnus) et contre un profil précis. C'est exactement la distinction entre notre mode GTO et nos profils. |
| **Poker Toolkit** ([page](https://poker-toolkit.com/en/poker-ranges-charts)) | ●● | Éditeur de ranges Expresso / Nitro, ranges de départ par format et position, mémorisation par répétition espacée, coach intégré, accès mobile | Concurrent sur la mémorisation ; ranges construites par l'utilisateur, pas de correction EV. |
| **Poker Builder** ([formation Expresso](https://poker-builder.com/fr/formation/expresso-exploiter-recreatifs-strategies-de-base)) | ● | Formation française « exploiter les récréatifs en Expresso », tableau push/fold Nash interactif | Affirme que la moitié des adversaires en Expresso sont récréatifs, sans source. |
| **FreeBetRange** | ●● | Visionneuse et trainer de ranges en navigateur ; héberge les charts Team BAS et des charts GTO avec exercices | Plateforme de distribution de ranges tierces. |
| **bitB – charts Spin & Go** ([article](https://blog.freebetrange.com/article/spin-go-preflop-charts-by-bitb-poker-school)) | ● | Charts HU SB et SB vs BB 10–13 BB | Exemple d'écart exploitant chiffré en stack : min-raise HU SB maintenu jusqu'à 10 BB contre les récréatifs, là où le GTO s'arrête vers 12–13 BB. |
| **Poker Academy (poker.academy) – Spin charts** ([page](https://poker.academy/preflop-charts)) | ●● | Centaines de charts 3-max et HU, 5 à 25 BB | Payant. |
| **Simple Preflop**, **Range Manager**, **MasterRange**, **SpinForWin**, **Full Time Spinners** (Gumroad, 27 €/mois) | ● | Simulation ou vente de ranges, cités par Spinelite et Poker Académie | Pages produit introuvables ou vides pour MasterRange et SpinForWin. |
| Guides éditoriaux : PokerListings FR (top 20 / 30 / 40 % selon la phase), PokerNews FR, pokerenligne.com | — | Règles simplifiées | Pas de référence utilisable. |

### 5.3 Données supplémentaires

| Donnée | Source | Vérification | Usage possible |
|---|---|---|---|
| **Distribution réelle des multiplicateurs Nitro** sur 3 487 tournois 2023 (1 € et 2 € surtout) : x2 59,9 %, x3 26,0 %, x4 8,3 %, x5 4,3 %, x10 1,5 %, x50 0,06 % | `dataset.csv` de [NitroVariance](https://github.com/ThibaultDieudonne/NitroVariance) (colonnes buy-in, multiplicateur, place, résultat, cEV, cEV ajustée) | Recompté le 14/10 ; cohérent avec la table CardPlayer du §3.3 (59,4 / 26,7 / 8,25 / 4 / 1,5 %) | Valide la table de multiplicateurs pour un futur calcul ICM ; Nitro et Expresso classique semblent partager la même table |
| Historiques de mains Nitro (dossier `history` du même dépôt, ≈ 3 500 tournois selon Popoch39) | NitroVariance | Non ouvert | **Ne pas utiliser** : dépôt sans licence et mains d'autres joueurs (les CGU Winamax interdisent l'exploitation des mains d'autres comptes ; Popoch39 lui-même parle de « zone grise ») |
| Break-even Nitro ≈ 35,8 % de victoires à 1–5 € (gain moyen ≈ 2,79 buy-ins, rake 7 %) et ≈ 36,2 % à 0,25–0,50 € (rake 8 %) | [Spécification Popoch39](https://github.com/Popoch39/poker_solver/issues/1), d'après la page Winamax du 07/10/2026 | Non recalculé | Contexte pour la page d'accueil ou les textes pédagogiques |
| 320 000 décisions de joueurs experts sur 8 800 Spin & Go réels (PartyPoker.fr, 50 à 250 €, 2018–2020) ; un modèle reproduit le solveur dans 78 % des décisions | [SpinGPT, Maugin et Cazenave, ACG 2025](https://arxiv.org/abs/2509.22387) | Disponibilité des données non confirmée | Seul jeu de décisions réelles en Spin & Go trouvé ; haut niveau (regs), donc référence « reg » et pas « récréatif ». Contacter les auteurs (université Paris-Dauphine) si besoin. |
| Exemple GTO simplifié à 15 BB : A6o en BB contre open 2 BB du BTN → call 48,6 %, relance 26,2 %, tapis 25,1 % | [Spinelite](https://spinelite.fr/blog/limportance-des-ranges-en-spin) | Solveur non nommé | Contrôle ponctuel d'un export HRC |
| « La moitié des adversaires en Expresso sont récréatifs » ; ils limpent ou min-raisent au lieu de pousser et paient trop large | [Poker Builder](https://poker-builder.com/fr/formation/expresso-exploiter-recreatifs-strategies-de-base) | Sans source | Confirme qualitativement le §3.1 |

### 5.4 Ce que cette passe change

- Aucune nouvelle fréquence de population chiffrée : le tableau Poker Sciences du §3.1 reste la seule source quantitative publique trouvée.
- La table des multiplicateurs est maintenant recoupée par des résultats réels (NitroVariance).
- Le marché francophone des « ranges GTO + exploitantes » est plus large qu'en première passe (Poker Sciences, Spinelite, Poker Toolkit, bitB, Team BAS via FreeBetRange). Aucun de ces outils ne publie ses hypothèses de profil ni de correction chiffrée par main : nos profils versionnés et notre correction en EV restent des différenciateurs.

## 6. Vidéos YouTube (2026-10-14)

Méthode : recherche YouTube sur « spin&go », « expresso », « range GTO », « range exploitant » (et équivalents anglais), sélection de 28 vidéos sur le préflop, l'exploitation des récréatifs et la population, récupération des **sous-titres** (automatiques pour la plupart) avec `tools/veille/youtube_subs.sh`, puis lecture des passages qui parlent de tendances de population ou de chiffres. Les transcriptions ne sont pas versionnées (contenus protégés) : seuls la synthèse, les liens et les minutages le sont. Les ranges affichées à l'écran ne sont pas dans les sous-titres.

Limites : 4 vidéos sont réservées aux adultes (connexion YouTube requise) et 1 n'a pas de sous-titres ; les vidéos d'abord bloquées par la limite de débit de YouTube ont été récupérées en relançant plus lentement (§6.4). Toutes les affirmations ci-dessous sont celles des coachs, sans données publiées derrière, sauf mention contraire.

### 6.1 Chaînes et vidéos exploitées

| Chaîne | Vidéo | Date | Intérêt |
|---|---|---|---|
| **Kill Tilt** (FR) | [Les clés du jeu préflop en Expresso](https://www.youtube.com/watch?v=m6RyRKzR08A) (2 h 28) | 19/02/2026 | Le plus riche : tendances préflop des récréatifs par profondeur |
| Kill Tilt | [Stratégie simple et efficace pour gagner en Expresso petites limites](https://www.youtube.com/watch?v=Wkd0Uq0i2FE) | — | Calls face aux tapis courts, BTN vs SB |
| Kill Tilt | [Les 3 principes essentiels pour gagner en Expressos en 2026](https://www.youtube.com/watch?v=27YoUVv32Ag) | 09/02/2026 | Field trop serré à 8–9 BB, proche théorie à 5–6 BB |
| Kill Tilt | [Arrondir ses fins de mois en Expressos : la vérité en chiffres](https://www.youtube.com/watch?v=tLTEpJqn2jE) | 30/03/2026 | Repères de cEV Nitro |
| Kill Tilt | [5 principes fondamentaux… Expressos microlimites](https://www.youtube.com/watch?v=XIxCrh3PBKc) ; [Maîtriser les ranges préflop](https://www.youtube.com/watch?v=n_3_Zzc8hJw) | 2024–2025 | Limp SB, 5 paramètres d'adaptation des ranges |
| **Team Bas Poker** (EN/FR) | [Adjusting to GG Spin & Gold player pool](https://www.youtube.com/watch?v=8EgxqisVIu4) ; [$3 Spin & Gold – easy exploits](https://www.youtube.com/watch?v=YwUxeVIsOTU) ; [Stratégie gagnante à 25 €+ sur Expresso Nitro](https://www.youtube.com/watch?v=FLflTIdL2aE) | 2024–2026 | « Pas de charts GTO contre les récréatifs » ; signaux de profil |
| **Le Wojak Poker** (FR) | [Mes ranges de spin & go gratuites](https://www.youtube.com/watch?v=sdiLfKofaGc) | 20/04/2025 | Ranges gratuites + mémorisation par flashcards Anki |
| **SpinElite Poker** (FR) | [12 strats de pro pour dominer le format Nitro](https://www.youtube.com/watch?v=g1_kRGY5PAw) | 09/06/2025 | Limp vs reg, min-raise de récréatif = fort |
| **Poker Académie** (FR) | [Le préflop en Spin ! On vous dit tout !!](https://www.youtube.com/watch?v=sMoF9yNU6Ek) | 26/05/2021 | Open BTN 38 % théorique, 42–45 % en pratique |
| **HUSNG.com** (EN) | [Comparing Nash heads-up ranges versus the population](https://www.youtube.com/watch?v=xnBlnLLq8Ks) | 29/10/2012 | **Seule mesure de population chiffrée** (§6.2) |
| **IMEZRUSPIN Poker** (EN) | [PT4 stacksize filtering – Spin and go general population analysis](https://www.youtube.com/watch?v=DD_9PFkzf-c) | 14/03/2020 | Méthode de rapport de population par tranche de stack |
| **GTO Wizard** (EN) | [Turning fish into chips](https://www.youtube.com/watch?v=EvvQb3Kq7Yc) | 15/08/2024 | Taxonomie de 7 profils de fish sur 20 M de mains (cash) |
| **SOLVBET_FR** | [Poker GTO vs exploit : la stratégie parfaite](https://www.youtube.com/watch?v=TA--yWDvvtk) | 06/02/2022 | Méthode « fréquence du field verrouillée dans le solveur » |
| **GTO Poker Charts** (EN) | [Spin and Go GTO poker charts](https://www.youtube.com/watch?v=xrrFa68NrNU) | 27/12/2020 | Produit concurrent : charts par tranche de stack |
| **LUCKYSPIN – Poker FR** | [Spin ranges : le plan d'action pour devenir gagnant (Expressos, Twister)](https://www.youtube.com/watch?v=XoqBgf_J-Co) ; [Comment progresser en Expresso Nitro sur Winamax 5 €](https://www.youtube.com/watch?v=NKlxX_GB_SQ) | 2023–2024 | « Des ranges contre le limp sont obligatoires : en GTO le BTN ne limpe jamais, en pratique les récréatifs limpent beaucoup au BTN » ; un adversaire Nitro 5 € noté à ≥ 70 % de limp ; plan « 20 % des ranges = 80 % des résultats » + quiz |
| Team Bas Poker | [Most spin players misread HUD stats](https://www.youtube.com/watch?v=MW8XNNAokD4) | 11/02/2026 | Popup HUD : limp, iso, open shove globaux pour profiler un récréatif sur peu de mains ; tailles de mise favorites par street |
| **Club Poker** × SpinElite | [La vérité sur les expressos avec la Team SpinElite](https://www.youtube.com/watch?v=W3em_68xhSw) (2 h 14) | 15/06/2026 | Écosystème : staking, coaching, « EV pool » lancé en juin 2026 (plus de 100 joueurs) ; Expresso jusqu'à 500 € chez Winamax ; « ne pas folder contre un fish parce que la range théorique le dit » |
| **Best Fish Forever** (IT) | [SB 15 bb : stratégie préflop contre les fish passifs ou super agressifs](https://www.youtube.com/watch?v=APC80-cg_dg) | 01/04/2026 | Exploit par node-lock GTO Wizard contre deux profils : fish passif « linéaire » (tapis direct avec paires et Ax off, iso seulement avec broadways fortes, 3-bet surtout value, overfold léger) et fish agressif (iso ≈ 25–30 %, plutôt en bluff) ; contre le passif, pousser Ax off direct faute d'iso-bluffs adverses. Même démarche que nos profils fictifs |
| Jonathan Little | [Mastering Spin & Go strategy with Ryan O'Donnell](https://www.youtube.com/watch?v=bKIv1ZkbPJ8) | 18/03/2021 | Peu de contenu préflop exploitable |

### 6.2 Données chiffrées

**HUSNG.com, PokerStars heads-up hyper 100 $ (2012), à 7 BB** : modèle bayésien construit sur une base de mains de la population.

| Situation | Nash | Population | Facteur k équivalent (formule `EXPLOIT_CALLS.md`) | Push max-exploit du SB |
|---|---|---|---|---|
| BB paie le tapis du SB, moyenne de la population | 49 % | 45 % | ≈ 0,85 | 75 % (Nash : 66 %) |
| BB lue « serrée » | 49 % | ≤ 39 % | ≈ 0,67 | 95 % |
| BB lue « large » | 49 % | 51 % | ≈ 1,08 | 63 % |

Ancien, heads-up seul et à 100 $, mais c'est la seule mesure de population publiée en vidéo. Elle va dans le même sens que les coachs Expresso : la population **paie trop serré face aux tapis** (k < 1 sur le call), ce qui contredit en apparence Poker Sciences (§3.1, calls trop larges). En fait, les situations diffèrent : Poker Sciences mesure les calls face à une **relance ou un 3-bet** à 25 BB (les récréatifs paient trop), HUSNG et Kill Tilt parlent des calls face à un **open shove** court (la population paie un peu trop serré, et surtout pousse trop serré).

Autres chiffres :
- Kill Tilt : en heads-up à 10 BB, la théorie fait isoler la BB **45 %** face au limp du SB ; la population « n'y arrive jamais ».
- Poker Académie : open BTN 3 joueurs ≈ 38 % en théorie, 42–45 % en pratique ; SB à l'équilibre : 90–95 % des mains jouées.
- Kill Tilt : repères Nitro hors rakeback, break-even ≈ 23 cEV par partie, moyenne d'un groupe de joueurs qui partagent leurs résultats ≈ 25 cEV, bon joueur ≈ 50 cEV.
- GTO Wizard (cash, pas spins) : seuils de profils, baleine VPIP ≥ 60 % et PFR < 12 %, « clownfish » PFR ≥ 20 % ; un fish loose-agressif paie ≈ 66 % des 3-bets.

### 6.3 Tendances qualitatives convergentes (Expresso / Spin, petites limites)

| Tendance | Sources | Ce qu'elle implique pour nos profils |
|---|---|---|
| Les récréatifs **poussent trop serré** de 8 à 15 BB ; au-delà de 15 BB presque jamais d'open shove ; vers 5–6 BB leurs tapis se rapprochent de la théorie | Kill Tilt (3 vidéos), Team BAS, Poker Sciences (§3.1) | Le facteur de déformation devrait **dépendre de la profondeur** (k ≈ 0,2–0,4 à 9–11 BB selon §3.1, proche de 1 sous 6 BB), au lieu d'un k unique par profil |
| Face à un tapis du BTN, payer moins large que la théorie (bas de range de call, Kx off, A2o–A3o) ; au SB, coller davantage à la théorie | Kill Tilt | Le profil « Serré » est le plus réaliste pour le BTN ; c'est déjà ce que fait le dataset `exploit_calls`, mais il faudrait le décliner par position |
| La population **folde un peu trop face aux tapis** (« people tend to overfold slightly ») | Team BAS, HUSNG | Justifie un futur mode où le héros pousse face à un profil qui paie trop serré |
| Limp à ≤ 10 BB = mains faibles ou moyennes qui limp-foldent ; un limp du BTN signale presque toujours un récréatif (certains limpent ≥ 70 %) | Kill Tilt, Team BAS, LUCKYSPIN | Profil « récréatif passif » : limpe au lieu de pousser, tapis seulement avec les mains très fortes |
| La BB n'isole pas assez face au limp (alors que la théorie isole 45 % à 10 BB en HU) → limper 100 % au SB contre un récréatif passif jusqu'à ~7 BB | Kill Tilt, Le Wojak, Poker Académie | Situations limp à ajouter quand HRC verrouillé sera disponible (`EXPORTS_A_PRODUIRE.md` §2) |
| Min-raise d'un récréatif à faible profondeur = range forte, peu de bluffs | Kill Tilt, SpinElite | Indice à donner dans les textes de profil |
| Expresso = format avec la plus forte proportion de récréatifs ; Winamax en a « beaucoup plus » que GG | Kill Tilt, Team BAS, Poker Builder | Contexte marketing |
| « Pas de charts GTO contre les récréatifs » ; ranges anti-récréatifs gratuites (Team BAS, SpinElite, Le Wojak) | Team BAS, SpinElite, Le Wojak | Concurrence directe sur le gratuit ; notre différence reste la correction chiffrée et les profils explicites |

### 6.4 Vidéos non récupérées

| Vidéo | Raison |
|---|---|
| [50 mains pour maîtriser le jeu préflop en Expresso](https://www.youtube.com/watch?v=X6_sVBI0y7U) (Kill Tilt) | Réservée aux adultes |
| [Ces erreurs sont partout en Spin 5 €… voici comment les punir](https://www.youtube.com/watch?v=uyDkiYI_tCE) (SpinElite) | Réservée aux adultes |
| [How to use preflop charts on Winamax Nitro Expresso](https://www.youtube.com/watch?v=OTJBBsKQXCk) (bitB Spins) | Réservée aux adultes |
| [Spin & Go preflop strategy, 10 BB training with GTO Wizard](https://www.youtube.com/watch?v=45qHc44RJCY) (Leo Bell) | Réservée aux adultes |
| [Bien démarrer avec un tracker (Spin & Go, Expressos…)](https://www.youtube.com/watch?v=cXLFalql6Ik) (Poker Spin Tracker FR) | Pas de sous-titres |

Pour les vidéos réservées aux adultes : exporter les cookies d'un compte YouTube connecté et relancer `yt-dlp --cookies cookies.txt …` depuis ton ordinateur, ou me déposer les sous-titres.

## 7. Passages vidéo où une range est affichée à l'écran (2026-10-14)

**Repérage.** `tools/veille/reperes_ranges.py` cherche dans les transcriptions les minutes où l'orateur montre quelque chose (« tableau », « à l'écran », « en vert / en orange », « je vous affiche la range », « chart »…) en parlant de range ; 90 minutes candidates ont été relues à la main, en écartant les mentions sans image (« ne vous contentez pas de tableaux », publicités, cash game). Il en reste **23 passages** dans [`reperes_ranges_youtube.csv`](reperes_ranges_youtube.csv), classés par priorité : 1 = Spin/Expresso avec une situation identifiable, 2 = utile mais moins précis, 3 = MTT ou consultation rapide d'un tableau.

**Capture.** Les images ne peuvent pas être récupérées depuis cet environnement : YouTube le bloque désormais (« confirmez que vous n'êtes pas un robot »), et les miniatures de navigation (storyboards) sont trop petites pour lire une grille 13×13. Sur un ordinateur personnel :

```bash
pip install yt-dlp            # ffmpeg requis
tools/veille/captures_ranges.sh docs/produit/reperes_ranges_youtube.csv captures/ 1            # priorité 1
tools/veille/captures_ranges.sh docs/produit/reperes_ranges_youtube.csv captures/ 1 cookies.txt  # si YouTube demande une connexion
```

Le script ne télécharge que les portions listées, en 720p, et garde une image par changement d'écran. Les images restent hors du dépôt ; une fois déposées, chaque grille lisible peut être retranscrite (main par main, action, profondeur, position) et comparée aux exports HRC.

**Passages de priorité 1**

| Vidéo | Passage | Ce qui devrait être affiché |
|---|---|---|
| Kill Tilt, *Les clés du jeu préflop en Expresso* | [40–46 min](https://youtu.be/m6RyRKzR08A?t=2400) | Range d'open théorique du BTN à 3 joueurs, 15 BB (orange = min-raise, jaune = open shove), puis défense de la BB face au min-raise |
| | [70–72 min](https://youtu.be/m6RyRKzR08A?t=4200) | Simplification de range proposée par le coach (limp) |
| | [74–83 min](https://youtu.be/m6RyRKzR08A?t=4440) | Open shove au-delà de 15 BB contre récréatifs ; BB face à l'open shove à 10 BB (bas de range théorique) |
| | [89–92 min](https://youtu.be/m6RyRKzR08A?t=5340) | HU SB vs BB 25 BB : théorie (vert = limp, orange = relance) et adaptation |
| Kill Tilt, *Stratégie simple et efficace… petites limites* | [14–18 min](https://youtu.be/Wkd0Uq0i2FE?t=840) | BB à 15 BB ; ranges à 8–10 BB ; BB face au tapis du SB à 6–7 BB |
| | [30–39 min](https://youtu.be/Wkd0Uq0i2FE?t=1800) | BB face au limp du BTN ; call face au tapis du SB à 3–4 BB et du BTN (range à 4 BB) ; open shove à 3,2 BB ; range du BTN |
| | [69–72 min](https://youtu.be/Wkd0Uq0i2FE?t=4140) | HU 10 BB : call face au 3-bet tapis du SB (vert) ; SB limp contre relance |
| Kill Tilt, *Les 3 principes essentiels… 2026* | [39–41 min](https://youtu.be/27YoUVv32Ag?t=2340) | Range d'iso-shove à 3 joueurs (en haut à gauche de l'écran) |
| | [47–53 min](https://youtu.be/27YoUVv32Ag?t=2820) | Limp contre tapis ; BB face au tapis du BTN à 8–9 BB ; open shove à 5 BB ; call à 3 BB |
| Poker Académie, *Le préflop en Spin !* | [0–6 min](https://youtu.be/sMoF9yNU6Ek?t=0) | Range d'open du BTN à 3 joueurs (38 % théorique, 42–45 % en pratique) ; range du SB |
| | [11–16 min](https://youtu.be/sMoF9yNU6Ek?t=660) | Tableaux Nash push/fold du SB (~6–7 BB), récapitulatif en fin de vidéo |
| HUSNG.com, *Nash vs population* | [3–5 min](https://youtu.be/xnBlnLLq8Ks?t=180) | HU 7 BB : range Nash du SB et range max-exploit contre la population, côte à côte |

Intérêt pour le projet : les ranges « théoriques » affichées servent de contrôle croisé de nos exports HRC aux mêmes profondeurs (15 BB 3 joueurs, 10 BB HU, push/fold 3–7 BB) ; les ranges « adaptées » (Kill Tilt contre récréatifs, HUSNG contre la population) sont des exemples concrets de déformation à comparer à nos profils fictifs.
