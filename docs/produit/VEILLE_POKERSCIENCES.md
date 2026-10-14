# Veille concurrentielle : Poker Sciences (pokersciences.com)

Relevé du 14/10/2026 sur 62 pages publiques en anglais (sitemap : 237 URL) : accueil, cours gratuit (13 chapitres), Academy (49 leçons), page du Study Pack, bibliothèque de tableaux, Bankroll Challenge. L'application (`app.pokersciences.com`) et les contenus payants n'ont pas été consultés. Les chiffres cités sont ceux qu'affiche le concurrent, non vérifiés.

## 1. En bref

- **Positionnement** : « le nouveau standard du Spin & Go ». Un écosystème centré sur un **tracker spécialisé Spin** (Poker Spin Tracker), avec un **pack préflop payant** (Study Pack, 390 €) intégré dedans, et du contenu gratuit pour l'acquisition.
- **Entonnoir** : cours gratuit + articles SEO + ranges BTN gratuites → téléchargement du tracker (gratuit jusqu'à 2 000 Spins) → abonnement tracker + Study Pack.
- **Différence de fond avec SpinsAcademy** : ils **mesurent le jeu réel** (mains importées) et comparent à leurs ranges ; nous **entraînons des décisions** avec des EV HRC traçables. Ils annoncent un onglet « GTO » (solveur) « bientôt » et un postflop « en 2026 » : c'est notre terrain.
- **Ce qu'ils font très bien** : pédagogie (ton simple, simulations, définitions), gamification poussée (XP, flammes, divisions hebdomadaires, défis, Arena, univers médiéval-fantastique), boucle « mains réelles → erreurs → rejouer dans le Trainer ».

## 2. Entreprise et moyens

| Élément | Constat |
|---|---|
| Équipe visible | « Gandalf », joueur pro de Spin et cofondateur (auteur de tout le contenu) ; « Olivier », remercié avec Gandalf pour avoir « imaginé et créé » le tracker (probablement le cofondateur ingénieur) ; « Madspin » cité dans les témoignages |
| Contact | `support@pokerspintracker.com`, Discord FR et EN (salon réservé aux acheteurs du Study Pack) |
| Langues | FR, EN, ES |
| Technique du site | Next.js (App Router) sur Vercel, Sentry, mode sombre uniquement, Google Search Console et vérification Facebook (publicités Meta probables) |
| SEO | Schema.org `Article` rattaché à un `Course` (position du chapitre), `FAQPage` sur l'offre, Open Graph complet, mots-clés ciblés par page |
| Tracker | Application de bureau Mac, Windows, Linux ; base locale `~/.pst2/` (`pst2.sqlite` + `pst2.duckdb`) ; version 2 en cours |
| Rooms | Winamax, PokerStars, Betclic, GGPoker, iPoker, Unibet, PartyPoker, ACR ; import live pour Winamax, PokerStars, Unibet, iPoker ; lecture des exports PT4 et Hand2Note |
| Vidéo | Chaîne YouTube : surtout des shorts d'une minute (« Stop limp-folding », « GTO can make you lose! », « How long does a bad run last? ») |
| Réputation | Une trentaine d'avis Trustpilot positifs ; témoignages Discord sur la page de vente |

## 3. Offre et prix

| Produit | Contenu | Prix |
|---|---|---|
| Poker Spin Tracker | Tableau de bord, joueurs, revue de mains, Leak Finder, compétition, HUD, Copilot | Gratuit jusqu'à 2 000 Spins importés ; puis Standard 15 €/mois ou Pro 39 €/mois, facturés au semestre (relevés tiers) |
| Study Pack | 401 tableaux, Trainer, 18 Strategy Guides, liaison au tracker, salon Discord | **390 € en paiement unique**, accès et mises à jour à vie |
| Gratuit | Cours 13 chapitres, Academy, tableau BTN + son guide + son chapitre Trainer, articles | 0 € |
| Annoncé | Onglet « GTO » (solveur, calcul de solutions contre ses adversaires) ; Study Pack postflop | « Soon » / 2026 |

## 4. Le cours gratuit, chapitre par chapitre

Présenté comme « Getting started in Spins in 2026 », pour débutants à intermédiaires, environ 2 jours de lecture. Chaque chapitre : citation d'accroche, définitions encadrées, résumé final, lien vers le chapitre suivant.

| # | Titre | Contenu et chiffres clés | Vers quoi il renvoie |
|---|---|---|---|
| 1 | Peut-on gagner sur le long terme ? | Récit personnel (0,50 € Winamax, « 4x open au bouton »), définition de l'EV et du tapis effectif, courbes EV de Gandalf par profondeur (12-25, 6-12, < 6 BB) : 270 k jetons d'EV sur 65 k mains | — |
| 2 | Jackpots et rake | Tables de multiplicateurs Expresso 1 € (sur 10 M) et Spin & Rush Betclic 1 € (sur 1 M) ; rake 7 % sur les deux, contre environ 10 % en MTT | — |
| 3 | Quel ITM viser ? | Seuil 35,8 % à rake 7 % ; **rake effectif** sans les gros jackpots : Winamax 8,6 %, Betclic 7,17 % → ITM 36,5 % / 35,9 % | — |
| 4 | Le CEV | CEV mini = ITM × 1 500 − 500 → 38,5 sur Betclic ; simulations SwongSim (CEV réel 60) : sur 100 parties, 5 % sous 4,9 et 5 % au-dessus de 126,9 ; il faut au moins 1 000 parties | Tracker |
| 5 | Les courbes mentent | −500 € sur 1 400 Spins à 10 € avec un CEV > 60 ; trois profils simulés sur 200 parties (fish gagnant, breakeven, régulier perdant) | — |
| 6 | La variance | 100 joueurs CEV 65 à 1 € : 200 parties → 30 % perdants ; 1 000 → 10 % ; 10 000 → 0 %, 90 % entre +238 et +718 buy-ins, un joueur à −226 buy-ins après 2 000 parties | — |
| 7 | Le rakeback | 10 à 40 % du rake ; Betclic à 30 % : ITM requis 35,1 %, CEV 27,5 ; utile à partir de 2 € | — |
| 8 | Bankroll | CEV 59 à 2 €, 2 000 parties : 50 % de chances d'un downswing de 50 buy-ins, 30 % de 60+ ; 100 % de chances d'une période de 250 parties sans gain. Reco : débutant (CEV 45) 200 BI, moyen (59) 100-150 BI, confirmé (70+) 70 BI ; Nitro × 2 | Simulateur du tracker |
| 9 | Le tilt | 10 conseils : objectifs de progrès plutôt que financiers, pauses, cacher sa bankroll, moins de tables, analyser ses mains | Study Pack, simulateur, Discord |
| 10 | Par où commencer | Room (rake, rake effectif, rakeback), 0,25-0,50 €, bankroll, tracker, 1 à 2 tables, équilibre jeu et étude | Tracker |
| 11 | 3 stratégies de base | Préflop ≈ 70 % de l'EV ; jamais de limp BTN 3-max (min-raise, fold, shove sous 18 BB) ; SB : 3-bet shove plutôt que call ; contre un open-shove, payer serré (tableau de call HU BB vs SB par nombre de BB) | Study Pack |
| 12 | Punir 2 erreurs | Fréquences fish (1 M de mains) contre GTO (GTO Wizard), tableau ci-dessous | Study Pack |
| 13 | Stratégies avancées | GTO contre exploitant (pierre-feuille-ciseaux, marchands de glace et équilibre de Nash) ; approche hybride ; HRC cité comme l'outil des stratégies exploitantes | Study Pack, Bankroll Challenge |

Fréquences annoncées au chapitre 12 (25 BB sauf indication) :

| Situation | Fish | GTO |
|---|---|---|
| SB limp → BB isole 3x : call de la SB | 76 % | 35 % |
| SB min-raise → BB 3-bet tapis : call de la SB | 65 % | 26 % |
| Open-shove BTN 9 BB | 15 % | 30 % |
| Open-shove SB vs BB 11 BB | 11 % | 38 % |
| Open-shove HU SB 7 BB | 21 % | 52 % |
| HU BB vs limp SB 13 BB : shove | 11 % | 16 % |

## 5. L'Academy (documentation du tracker sous forme de cours)

8 modules, 49 leçons, avec un fil narratif (un mage et son apprenti cherchent « la Bible du Jeu » à travers le « Monde connu » ; quatre factions). Ce que la documentation révèle du produit :

| Module | Fonctions et idées |
|---|---|
| 1. Bienvenue | Les **3 piliers** : volume, qualité des tables (ratio fish/reg), niveau. Import live et manuel, détection automatique des rooms et des structures de multiplicateurs |
| 2. Premiers chiffres | 4 KPI (tournois, CEV, rakeback, profit) ; **4 modes de profit** : réel, **EV effective** (avec les multiplicateurs qu'on pouvait raisonnablement toucher à son volume, présentée comme une exclusivité), EV long terme, EV aux multiplicateurs obtenus. Rakeback par room et par période. €/h en EV effective présenté comme LA métrique (objectif 30 à 50 €/h) |
| 3. Courbes | Ligne de **CEV de rentabilité** propre à la room ; **intervalle de confiance à 90 %** sur le CEV (σ/√n × 1,645) ; événements (pic, creux, gros gain, downswing, plateau) ; filtres ; €/h par nombre de tables avec lissage ; **simulateur Monte-Carlo** inspiré de SwongSim (molette pour projeter, 100 tirages, percentiles 10/25/50/75/90) |
| 4. Variance | Ce que l'EV ajustée ne neutralise pas (cartes reçues, mains adverses au tapis, coups sans tapis) ; **badge Run Luck** (percentile de chance, à partir d'un volume minimal) |
| 5. Revue de mains | Replayer, filtres par **Action Lines** (séquence exacte, tailles), filtres rapides ; **détecteur d'erreurs préflop** (action à fréquence 0 dans le tableau de référence) ; résumé d'import avec précision préflop ; « Rejouer mes erreurs » dans le Trainer, combos regroupés |
| 6. Leak Finder | Onglet préflop (ta range contre la référence, contre les fish et contre les regs, score de précision, cible 85-90 %) ; tableaux personnalisés ; onglet postflop (arbre de décision, Hero contre fish et regs, composition des ranges) ; onglet **Global EV** (EV réalisée en bb par combo, comparée au GTO, incertitude par case) ; tableau de bord type Hand2Note ; plan de travail. Reconnaissent que « le tracker mesure, il ne construit pas la stratégie » : cela viendra avec le solveur |
| 7. Compétition | **Classement XP** (EV × coefficient de buy-in × √flammes ÷ aléa) ; **flammes** (jours d'activité consécutifs) ; **divisions hebdomadaires** de Bronze à Mythic (groupes de 10, promotions et relégations, Mythic limité à 12) ; **défis** publics ou privés (profit, EV €, volume pondéré par la durée des Spins) avec palmarès ; Arena quotidienne |
| 8. Adversaires | Classement fish/reg automatique (reg = 50 mains et limp BTN ≤ 5 %) ; tags, alias, HUD en jeu ; résultats par profil ; qualité des tables par jour et par créneau ; **CEV en fonction de la part de fish** (« quelques points de fish peuvent doubler le winrate ») |

## 6. Le Study Pack en détail

- **Tableaux** : 401 tableaux, 24 situations (3-max BTN, SB, BB : opens, limps, tapis, 3-bets, tapis asymétriques ; heads-up SB et BB), 10 tranches de tapis (0-4 jusqu'à 20+ BB), chacun en version **vs Reg (GTO)** et **vs Fish (Exploit)**. Mode comparaison, mode « redessine de mémoire », import et export texte, sauvegarde dans le cloud.
- **Construction** (FAQ) : plus d'1 million de mains de Spin donnent les tendances des récréatifs ; le solveur (HRC) calcule la meilleure réponse ; puis arbitrage entre 4 critères : meilleure EV, **tableau facile à mémoriser**, faible variance, lignes postflop. Les tableaux sont **simplifiés** par rapport au GTO brut.
- **Trainer** : 34 chapitres classés par importance, mode campagne (niveaux, XP) et mode libre, quiz d'introduction à certains chapitres, mode **Hardcore** (seulement les mains proches du seuil), **minuteur** (3 à 10 s), onglet erreurs, **Arena quotidienne** et classement.
- **18 Strategy Guides** : un mini-cours par situation importante, avec tableaux interactifs.
- **Liaison au tracker** : chaque main importée est comparée aux tableaux, avec un score de précision ; les erreurs deviennent des exercices.
- **Argument face aux solveurs** : « un solveur ne sait pas ce que vous jouez ; ici la référence et vos mains sont dans le même logiciel ».

## 7. Comparaison avec SpinsAcademy

| Axe | Poker Sciences | SpinsAcademy |
|---|---|---|
| Source des EV | Tableaux simplifiés et arrondis pour être mémorisés ; l'EV par main n'est pas exposée dans le Trainer | EV HRC exactes et traçables par question, écart chiffré de l'action choisie |
| Exploitant | Une version « vs Fish » par tableau, construite à partir d'1 M de mains | Profils d'exploitation limités (call d'un tapis au BB), extension prévue (plan MVP #17) |
| Support | Application de bureau, tracker local | Web mobile |
| Données réelles | Import des mains, détection d'erreurs, Leak Finder | Aucune |
| Rétention | Flammes, XP, divisions, défis, Arena, Discord, univers narratif | À construire (plan MVP #21) |
| Explications | 18 guides rédigés par un pro, ton pédagogique | « Pourquoi ? » jugé descriptif (plan MVP #12) |
| Postflop | Fréquences comparées aux regs ; théorie « à venir » | Prévu (lot 2) |
| Prix | 390 € une fois + abonnement tracker | À définir (`OFFRE.md`) |

## 8. Ce que SpinsAcademy peut en tirer

1. **Se placer sur la précision et le mobile.** Leur message est « des tableaux simples à retenir » ; le nôtre peut être « la vraie EV de chaque décision, en 2 minutes sur ton téléphone ». C'est complémentaire de leur tracker de bureau, sans l'affronter de face.
2. **Mode « seuil » (#6 du plan MVP).** Leur mode Hardcore (seulement les mains proches du seuil) confirme la demande. Nos EV exactes permettent un tirage pondéré par l'écart d'EV, ce qui est mieux qu'un seuil binaire.
3. **Minuteur.** Questions chronométrées de 3 à 10 secondes pour simuler le multi-tabling : peu coûteux à faire.
4. **Rétention (#21).** Série de jours (« flammes »), objectif quotidien, défi hebdomadaire. Leurs divisions demandent une communauté importante ; un classement privé ou entre amis suffit au départ.
5. **Règle à retenir (#12).** Les « Key takeaways » et les guides par situation montrent le format attendu : une règle par famille, position et profondeur, validée par un expert.
6. **Profils fish (#17, #18).** Leurs fréquences publiques (tableau du §4) peuvent servir d'**hypothèses de départ** pour les profils d'exploitation, à condition d'être citées comme telles et recoupées. Leur règle fish/reg (limp BTN ≤ 5 % sur 50 mains) répond à « comment repérer un profil ».
7. **Contenu gratuit et SEO.** Un cours structuré avec `Schema.org Course`, la page variance (chapitre 6) refaite sous forme de **simulateur interactif** (CEV, buy-in, nombre de parties, room), et des FAQ balisées.
8. **Rake effectif et multiplicateurs.** Leur notion d'EV effective est forte pour les joueurs. Un calculateur « ITM et CEV minimum par room » serait un bon produit d'appel gratuit, avec des calculs simples à vérifier.
9. **Risque à surveiller** : leur onglet GTO annoncé (« calculer ses propres solutions contre ses adversaires ») viendrait sur notre terrain. Il faut avoir sorti la bêta avant.
