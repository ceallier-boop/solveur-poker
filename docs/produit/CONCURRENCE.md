# Concurrence : Poker Académie (notes produit, 2026-10-14)

Analyse de https://www.poker-academie.com (pages publiques, sans compte) : tarifs, site, forum et contenus Spin / Expresso. Objectif : situer SpinsAcademy, pas réutiliser des contenus.

## Ce qu'on peut en faire (droits)

- CGU §10 : contenus réservés à un « usage personnel », toute diffusion soumise à un accord écrit de Poker Académie. Les messages du forum sont des contributions sous licence à la plateforme.
- **Aucun contenu (main, range, explication, question de quiz) n'est repris dans les datasets ni dans les explications.** De toute façon, rien n'y est traçable à une source calculée (cahier des charges §1.3 et §7 : EV issues de HRC, explications validées par un expert).
- Usage retenu : étude de marché, liste des thèmes à couvrir, repères de prix, experts à contacter. L'annexe liste des adresses, pas de contenu.
- Collecte : pages publiques autorisées par `robots.txt`, à faible cadence ; le forum (Discourse) limite le débit et cette limite a été respectée.

## 1. Offre et modèle économique

| Formule | Prix | Contenu |
|---|---|---|
| Gratuit | 0 € | 300+ vidéos, Replayer, Discord, articles, rakeback par affiliation |
| Silver | 19 €/mois | Coachings en direct sur Discord, 625+ vidéos, ranges partielles |
| Gold | 49 €/mois | Replays des lives, « 2 000+ » vidéos, toutes les ranges |

- Annuel annoncé à -25 % sans prix affiché (soit environ 171 € et 441 € par an).
- **Le moteur économique est l'affiliation** : rakeback et bonus PMU (+8 %, 500 €), Unibet (+7 %, 1 500 €), Winamax (250 €), points PPA échangés en boutique contre des cartes cadeaux ou des logiciels (Simple Preflop 1 000 PPA, Simple GTO Trainer 800 PPA, GTO+ 280 PPA), 2 semaines de Gold offertes à l'affiliation Winamax. Le contenu attire et retient ; les salles paient.
- Coaching privé : 14 coachs de 60 à 400 €/h (cash, MTT, mental), **aucun spécialiste Spin**.
- Revendiqué : 110 000+ membres, Trustpilot 4,3, depuis 2005. Audience mesurable : Discord 2 k, YouTube 6,6 k, Instagram 3,7 k.

## 2. Contenus et outils

| Rubrique | Volume | Remarque |
|---|---|---|
| Vidéos | 1 570 comptées (« 2 000+ » annoncées) | Cash 948, MTT 442, Sit & Go 152 ; vidéos Spin arrêtées depuis juillet 2025 |
| Articles | ~5 100, presque tous publics | Beaucoup d'actualité et de promotion des salles |
| Ranges | 4 | Cash NL10-NL50 et MTT, sans source (ni solveur ni HRC), rien en Spin |
| E-books | 10 | Cash et généralités |
| Replayer | gratuit, ~3 800 mains | Rejouer et commenter ; pas d'EV ni de solveur |
| Coachings hebdo | 5 lives par semaine | Annoncés « cash, MTT, Spin » ; planning sans Spin |

Incohérences relevées : nombre de vidéos, rakeback Winamax « jusqu'à +8 % » mais 0 % au récapitulatif, dépôt minimum 10 € ou 250 €, « 14 jours d'essai » sur l'offre gratuite. **Il n'existe aucun entraînement interactif** : l'entraînement est renvoyé à des logiciels tiers vendus en boutique.

## 3. Contenus Spin / Expresso (sitemap, 189 adresses)

Pages lues : programme de la Spin Card, TP n°1 et n°4, cours « push or fold », « concepts classés par buy-in », « spots faciles à abandonner », « HU limp 8 BB », « BTN vs BB 25 BB », « grand quiz Expresso », « bases d'un jeu gagnant en Expresso », « point de commitment », « initiation préflop », quiz Expresso et push/call HU.

**Constat principal : ces pages sont des annonces.** Le contenu réel (théorie, ranges, corrections) est dans des webinaires Livestorm (replays réservés aux inscrits) et des vidéos payantes. Le texte public ne contient ni ranges, ni chiffres, ni règles.

| Ensemble | Période | Ce qu'il montre |
|---|---|---|
| Formation « Spin Card » (17 pages) | sept.-nov. 2023 | Parcours gratuit de 8 semaines pour les Spin 0,25-2 € (coach CallAuQQ) : 8 cours théoriques (notions de base, GTO contre exploit, préflop « redless » et leaks du field récréatif, postflop, mindset, HUD Hand2Note, évaluation), 8 sessions de jeu commentées en Spin 2 €, missions, quiz final. Contrepartie : compte Betclic ou partypoker affilié contre 3 mois de Silver |
| Cours collectifs gratuits (37 pages) | 2021-2024 | Webinaires hebdomadaires de Blagops (70+ participants au 2ᵉ cours) : push or fold, BTN vs BB à 25 BB, HU limp à 8 BB, point de commitment, spots faciles à abandonner, concepts par buy-in, variance et SwongSim, pots 3-way, multitabling, bankroll challenge |
| Quiz (7 pages) | 2016-2023 | Quiz Expresso débutant / intermédiaire / difficile (10 questions sur 20, classement), push et call HU, delay c-bet HU. Source des ranges jamais indiquée ; correction par une vidéo la semaine suivante ; opérations ponctuelles |
| Fiches de coachs (19 pages) | 2016-2023 | Spécialistes francophones : Blagops (Expresso), Nico (Expresso), CallAuQQ (Spin low), Mikepierce69 (Spin high stakes), Lasz1 (Nitro), Muraille, Jojo-54 (Expresso et SNG HU) |
| Actualité (le reste) | 2016-2026 | Promotions des salles (Twister, Spins Ultra, Flash), répartition des multiplicateurs, bots sur les Expresso Winamax 100/250 € (2018) |

Repère chiffré utile (article de 2018 sur les bots) : avec GTO Database, l'erreur moyenne par décision des comptes soupçonnés valait environ -0,2 BB, contre -0,75 à -1 BB pour un très bon régulier selon l'auteur de l'outil. Ordre de grandeur pour présenter l'écart d'EV moyen d'un joueur, à valider (unité et périmètre de décisions non précisés).

### Thèmes cités face au périmètre du dataset

Périmètre actuel : préflop, 3-handed et heads-up, 4 à 25 BB, familles « premier à parler », « face à un limp », « face à une relance », « face à un tapis », modes GTO et exploitant (`docs/dataset/FORMAT_SPOT.md`).

| Thème travaillé chez Poker Académie | Couverture SpinsAcademy |
|---|---|
| Push or fold, push et call en HU | Couvert (premier à parler, face à un tapis ; EV exacte) |
| BTN vs BB à 25 BB | Couvert à 25 BB (3-handed : BTN premier à parler, BB face à une relance) |
| HU limp à 8 BB | Couvert (heads-up à 8 BB : SB premier à parler, BB face à un limp) |
| Stratégie préflop simplifiée, « redless » | Couvert par la stratégie de référence et la grille 13 × 13 ; manque une **règle à retenir** par spot (remarque 12 du plan MVP) |
| Leaks du field récréatif, exploits simples | Partiel : exploitant limité au call d'un tapis (remarque 17), fiche « reconnaître un profil » à faire (remarque 18) |
| Point de commitment | Implicite dans les tapis et relances à faible profondeur ; pas de notion nommée dans les explications |
| Concepts par buy-in | Absent : pas de parcours par limite ; idée de progression 0,25 → 2 € |
| Spots faciles à abandonner | Proche de la difficulté par question ; pas de vue « où je perds le plus d'EV » à ce jour |
| Variance, SwongSim, bankroll | Absent ; hors cœur de produit, mais c'est la question la plus posée sur le forum (§4) |
| Pots 3-way, postflop, delay c-bet, 2ᵉ barrel | Absent : postflop prévu au lot 2 (remarque 19) |
| Multitabling, HUD, prise de notes | Hors périmètre |

Aucun manque majeur sur le préflop : les thèmes préflop enseignés sont déjà dans les familles du dataset. Les écarts sont pédagogiques (règle à retenir, profil, parcours par limite) et le postflop.

## 4. Forum (Discourse)

Catégorie « Sng & Expresso » : 120 sujets depuis 2017, dont la moitié sont des annonces de vidéos ; un à deux sujets par mois en 2026.

Fils lus en entier : 10 (variance, groupes de travail, débutants, montée de limite, livre de ranges, « pool EV », range de call Expresso). 10 autres ciblés n'ont pas pu être lus : le forum a refusé les requêtes même à une par minute, et la limite n'a pas été contournée.

| Constat | Signes dans les fils | Pour SpinsAcademy |
|---|---|---|
| Le **cEV** (chips gagnés en EV par partie) est la mesure de référence des joueurs | « 80 de cEV c'est correct, les bons joueurs sont au-dessus de 100 » ; seuil de rentabilité estimé à ~40 de cEV avec 6,85 % de rake ; un joueur à 70 de cEV toujours perdant après 20 000 Spins | Parler le langage des joueurs : relier l'écart d'EV par décision à ce qu'il coûte en cEV par partie |
| La **variance** angoisse et personne ne sait la lire | « combien de Spins pour lisser la variance ? » ; réponses de 5 000 à plusieurs dizaines de milliers ; seul outil cité : SwongSim | Message produit : juger son jeu par décision, sans attendre 20 000 parties |
| Les débutants ne savent pas **où ils perdent** | « je push uniquement à moins de 8 BB » ; réponse : « un paquet de pushs corrects que tu rates » ; « encore quelques leaks en BB » selon PT4 | Le push/fold et la BB sont les premières sources d'erreur : vue « où je perds le plus » par famille et position |
| Besoin d'une **stratégie automatique** pour jouer vite | « une stratégie que tu appliques sur plus de 95 % de tes décisions sans réfléchir » ; « des ranges stables pour contrôler ce que je fais » | Règles à retenir courtes et ranges simplifiées (remarque 12 du plan MVP) |
| Les ranges GTO brutes déçoivent | Livre « Poker GTO Spin » (39 €) : « ranges arrondies, gratuites sur GTO Wizard », « aucune info sur le soft utilisé », « qu'il faudra encore simplifier » | La traçabilité (source HRC, version, contrôles) et la simplification sont des arguments ; une table de ranges seule ne se vend pas |
| L'exploitation se pense en **profils** | Expresso 15 BB face à un BB « VPIP 70 / PFR 10 » : « s'il est vraiment aussi nit, call ATo+ et 88+ » | Le mode exploitant parle le langage du forum ; à étendre au-delà du call d'un tapis (remarque 17) |
| L'EV « hors jackpot » est connue | « pool EV » (Hyperschool) : partage des gains hors gros multiplicateurs | Confirme le choix du chip EV pour juger les décisions, indépendamment des multiplicateurs |
| On cherche à **progresser ensemble** | Deux groupes de travail Expresso et Spin micro (déc. 2025, juin 2026) : ranges préflop, push/fold, leaks, sessions courtes | Cible et fonctions confirmées ; défis ou comparaison entre amis à étudier |

Autres sujets populaires (titres seulement) : « Bankroll pour expresso » (15 000 vues), « Tableaux de ranges pour les expressos (Winamax) », « Quels outils de travail pour débuter en spin », « Suite aux changements, quelle room choisir pour les SPIN », « Nitro 0,25 ».

## 5. Ce que cela implique pour SpinsAcademy

1. **Créneau libre** : entraînement actif Spin / Expresso corrigé par l'EV. Poker Académie a essayé le quiz (2016-2023) sans en faire un outil durable, et n'a plus de contenu Spin depuis 2025.
2. **Cible confirmée** : Expresso Winamax et Spin de 0,25 à 2 €, débutants et intermédiaires, préflop et push/fold, sessions courtes.
3. **Mesurer le jeu, pas les résultats** : la variance est la première inquiétude. Un indicateur d'écart d'EV par décision et son évolution répond à « suis-je un joueur gagnant ? » sans attendre 20 000 parties.
4. **Rétention** : les joueurs cherchent un « compagnon de route » ; objectif quotidien, série de jours et révision espacée (remarque 21) répondent au même besoin.
5. **Prix** : 19 et 49 €/mois pour regarder, 800 à 1 000 PPA pour un trainer tiers. Une offre payante autour de 9 à 15 €/mois est cohérente (`OFFRE.md`).
6. **Financement** : l'affiliation finance le gratuit chez Poker Académie ; à étudier avec un opérateur agréé ANJ, avec les règles de publicité et la mention 18+.
7. **Expert** : les coachs Spin / Expresso cités au §3 sont des candidats pour la relecture experte (remarque 14).
8. **Partenariat possible** : Poker Académie distribue déjà des trainers tiers dans sa boutique et n'a pas d'outil Spin.

## Annexe : adresses Spin / Expresso du site

[`CONCURRENCE_URLS.md`](CONCURRENCE_URLS.md) : 189 adresses issues du sitemap du 2026-10-14, classées par ensemble, sans contenu.
