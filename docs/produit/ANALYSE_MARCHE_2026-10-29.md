# Analyse de marché : inventaire et nom de l'application (29/10/2026)

Interface « Analyse de marché ». Ce document liste ce dont l'analyse a besoin, ce qui existe déjà dans le dépôt et les artéfacts, puis propose un nom.

## 1. Éléments nécessaires et état

| # | Élément | Existe déjà | Où | Manque |
|---|---|---|---|---|
| 1 | Public cible | Oui, en une phrase | Cahier des charges §1.2 : joueurs réguliers Spin / Expresso, francophones, connaissant ranges, profondeur et bases du GTO | Personas (récréatif qui progresse, régulier petites limites, régulier confirmé), part de chacun |
| 2 | Taille du marché | Non | — | Comptes poker actifs en France (rapports ANJ), part de l'Expresso dans le trafic Winamax, nombre de joueurs réguliers Expresso, même chose pour la Belgique, la Suisse et le Québec |
| 3 | Concurrents et prix | Quelques noms cités | Avis d'un joueur Expresso du 13/10 (HRC, ICMIZER) | Tableau complet : voir §2 pour un premier relevé |
| 4 | Positionnement | En creux | Cahier des charges §1.3 (exactitude avant quantité, explications traçables), mode Exploitant, séances courtes | Phrase de positionnement face aux concurrents |
| 5 | Disposition à payer | Oui, deux avis | Avis du 13/10 : « en l'état, je ne le paierais pas » (6,5/10) ; notes des tests joueurs 1 à 9 (3,5 à 4/5) | Question de prix posée aux testeurs (prix accepté, prix jugé cher), test de pages de prix |
| 6 | Modèle économique | Question ouverte | `OFFRE.md`, cahier des charges §19, action B4 | Contenu gratuit / payant, prix, essai, paiement |
| 7 | Canaux d'acquisition | Non | Coachs Lucho, PA, Lucky (déjà relecteurs) | Coachs et écoles spin, Twitch / YouTube, Discord, forums (Club Poker), partenariats d'affiliation |
| 8 | Rétention | En cours | Action D1 (indicateurs par cohortes), défis, objectifs, séance de 15 minutes | Repères du secteur (retour à J+1, J+7, J+30 des applis d'entraînement) |
| 9 | Contraintes légales du secteur | En partie | Politique de confidentialité (A14) ; droits sur la référence réglés (A13) | Publicité liée au jeu (encadrement ANJ), noms de formats déposés, règles des opérateurs sur les outils |
| 10 | Nom et marque | « SpinsAcademy » / « SpinAcademy », non tranché (I7) | Tableau de suivi | Voir §3 |

**Données à demander au porteur du projet** : estimation du nombre de joueurs Expresso réguliers (trafic observé, Sharkscope), prix envisagé, liste des coachs et communautés avec qui un partenariat est possible.

## 2. Premier relevé des concurrents

Prix relevés sur le web le 29/10/2026, à vérifier sur les sites des éditeurs.

| Outil | Ce qu'il fait pour le Spin | Prix relevé |
|---|---|---|
| GTO Wizard | Solutions et entraîneur Spin & Go préflop et postflop, en anglais | De 39 à 229 $ par mois selon les sources |
| Poker Academy (poker.academy) | Offre « Spin&Go with Solver » : préflop, entraîneur, solveur postflop jusqu'à 25 BB | 29 € par mois, 19 € par mois à l'année (annonce de 2023) |
| ICMIZER SNG Coach | Entraîneur push/fold et ICM, Spin compris | 37,99 $ par mois sur iOS |
| GTO Sensei | Pack Spin&Go sur mobile | 15,99 $ par mois |
| GTO Ranges+, Poker Preflop Trainer PRO, Poker Flight Simulator, ICM Trainer | Applis mobiles de ranges et de push/fold, Spin parmi d'autres formats | Gratuit avec achats intégrés |
| Poker Coaching (Jonathan Little) | Quiz push/fold par position et profondeur, cours | Gratuit avec achats intégrés |

**Ce qui en ressort** : les outils sérieux sont en anglais, chers et généralistes (tous formats) ; les applis mobiles bon marché sont des tableaux de ranges sans correction chiffrée. Aucune appli trouvée n'est en français, dédiée à l'Expresso, avec un mode exploitant contre le field. C'est la place à prendre.

## 3. Nom de l'application

### Pourquoi changer de « SpinsAcademy »

- **Les deux domaines `.com` sont déjà pris** (`spinacademy.com`, `spinsacademy.com`).
- **« Academy » rapproche d'un concurrent direct** : Poker Academy vend déjà une offre Spin&Go à 19-29 € par mois.
- **« Spin » renvoie au Spin & Go de PokerStars**, alors que le cœur du public joue l'Expresso de Winamax. Le nom ne parle ni aux uns ni aux autres en propre.
- Le pluriel ou non (« Spins » / « Spin ») crée déjà des fautes dans nos propres documents.

### Critères

Court, prononçable en français, sans nom de format d'opérateur (Expresso, Spin & Go, Twister), qui évoque la vitesse et le tapis court, domaine libre.

### Recommandation : **Ristretto**

Le ristretto est l'expresso serré : moins d'eau, plus concentré. Le nom dit exactement ce qu'est l'appli :

- **le format** : clin d'œil direct à l'Expresso, sans reprendre le nom de Winamax ;
- **le tapis court** : de 2 à 25 BB, le poker « serré » ;
- **la séance** : 15 minutes concentrées, un shot avant de jouer.

Accroche possible : **« Ristretto — le short stack, serré et intense. »** ou **« Court. Serré. Rentable. »**

Disponibilité vérifiée le 29/10 (registre RDAP) : `ristretto.poker`, `ristrettopoker.com`, `ristrettopoker.fr`, `ristretto.gg` et `ristrettoapp.com` sont libres ; `ristretto.fr` et `ristretto.app` sont pris. Aucune appli de poker trouvée sous ce nom.

Risque à lever : le mot est courant dans le café (Nespresso l'utilise comme nom de variété). Il reste descriptif pour le café, donc a priori libre pour une appli d'entraînement, mais une recherche INPI / EUIPO en classes 9 et 41 est nécessaire avant dépôt.

### Autres pistes

| Nom | Idée | Domaines libres | Limite |
|---|---|---|---|
| Tapis | Le mot français du all-in et du stack | `tapis.poker` | Très générique, difficile à déposer |
| TriMax | Le 3-max | `trimax.poker` | Ignore le heads-up, sonne technique |
| SpinLab | Laboratoire du spin | `spinlab.poker` | Garde « Spin » (PokerStars) |
| PushFold | Descriptif | `pushfold.app`, `pushfold.fr` | Réduit l'appli au push/fold, alors qu'elle va au-delà |

### Décision du porteur du projet (30/10) : **SpinPokerTraining**, à l'essai

Le 29/10, SpinLab avait été retenu ; une société « Spinlab » (spinlab.studio, logiciels de casino en marque blanche, créée en 2025) occupe déjà le nom dans le secteur des jeux d'argent. Le 30/10, le porteur du projet essaie **SpinPokerTraining**.

Disponibilité vérifiée le 30/10 (registre RDAP) : `spinpokertraining.com`, `.fr`, `.app`, `.io`, `.poker` et `spinpoker.training` sont tous libres. Aucun produit trouvé sous ce nom exact.

Points d'attention :

- **Proximité avec Advanced Poker Training** : cet éditeur exploite `pokertraining.com` et un entraîneur Spin & Go à `spinngo.pokertraining.com`. Notre nom contient le leur en entier : risque de confusion et d'opposition.
- **Nom descriptif** : « spin », « poker » et « training » sont des mots courants du secteur ; une marque purement descriptive se protège mal (dépôt fragile, copie difficile à empêcher). Un logo et une forme graphique propres aident.
- **« Spin Poker »** désigne aussi un jeu de vidéo-poker de casino (Action Gaming).
- **Anglais et long** (17 lettres) pour un public d'abord francophone ; en abrégé, « SPT » est plus facile à retenir.

Suite : recherche d'antériorité INPI / EUIPO (classes 9 et 41), achat de `spinpokertraining.com` et `spinpokertraining.fr`, réservation des comptes réseaux sociaux, puis renommage dans l'en-tête, le manifeste et les artéfacts (I7, interface « Interface »).

### Analyse des noms disponibles (30/10)

**Méthode.** 45 noms testés : domaines `.com`, `.fr`, `.app` et `.poker` (registre RDAP), puis recherche web d'un produit existant sous ce nom (poker, jeux d'argent, entraînement). Les registres de marques (TMview, INPI) refusent les accès automatiques depuis notre environnement : **aucun nom n'est garanti « libre de droits » tant que la recherche INPI / EUIPO n'est pas faite** (liens plus bas).

**Constat.** Presque tous les noms courts en `.com` sont pris (Spinto, Spinzo, Spinova, Spinflow, SpinCoach, SpinMind…). Le `.fr` et le `.app` suffisent pour une appli d'abord francophone.

#### Noms retenus

| Rang | Nom | Sens | `.com` | `.fr` | `.app` | `.poker` | Produit existant | Avis |
|---|---|---|---|---|---|---|---|---|
| 1 | **SpinDrill** | Spin + drill (exercice répété) | libre | libre | libre | libre | aucun trouvé | Seul nom court avec les quatre domaines libres. Dit ce que fait l'appli, garde « Spin ». « Drill » est connu des joueurs, moins du grand public. |
| 2 | **Spinkata** | Kata : geste répété jusqu'à l'automatisme | pris | libre | libre | — | aucun trouvé | Le plus distinctif, donc le plus facile à déposer. Image forte (routine, maîtrise). |
| 3 | **Ristretto** | L'expresso serré : tapis courts, séance courte | pris | pris | pris | libre | aucun en poker | La meilleure histoire, mais seul le `.poker` est libre. Mot courant du café. |
| 4 | **Shovio** | Mot inventé, de « shove » (tapis) | pris | libre | libre | — | aucun trouvé | Inventé, donc dépôt solide ; peu parlant au premier abord. |
| 5 | **Spinvo** | Mot inventé | pris | libre | libre | — | aucun trouvé | Court et déposable ; ne dit rien du produit. |

#### Noms possibles avec réserve

| Nom | Domaines libres | Réserve |
|---|---|---|
| SpinDojo | `.fr`, `.app` | Une appli « Poker Dojo » existe déjà |
| JamFold | les quatre | Jargon ; réduit l'appli au push/fold |
| SpinTuto | les quatre | Sonne débutant, pas assez premium pour un public confirmé |
| SpinPokerTraining | les quatre | Contient en entier le nom d'Advanced Poker Training, qui vend un entraîneur Spin-N-Go |

#### Noms écartés

SpinAcademy (domaines `.com` pris, proche de Poker Academy), SpinLab (société de logiciels de casino du même nom), SpinCoach, Spinto, Spinzo, Spinova, Spinflow, Spinoza, Trilo (domaines principaux pris).

#### À propos de « Spin »

PokerStars utilise « Spin & Go » ; « spin » seul est devenu le mot courant du format, ce qui limite le risque, mais empêche aussi de déposer « Spin » seul. La protection portera sur le nom entier (SpinDrill, Spinkata) et sur le logo.

#### Recommandation

**SpinDrill**, ou **Spinkata** si l'on préfère un nom plus distinctif. Avant de trancher : recherche gratuite sur [data.inpi.fr](https://data.inpi.fr) et [TMview](https://www.tmdn.org/tmview/) (classes 9 et 41), puis achat des domaines le jour même.

## 4. Prochaines étapes de l'analyse de marché

1. Taille du marché à partir des rapports annuels de l'ANJ et des données de trafic.
2. Tableau concurrentiel complet (fonctions, langue, prix, notes des stores).
3. Questionnaire prix et canaux auprès des testeurs (dixième test, P9).
4. Proposition d'offre gratuite / payante et de prix (B4), avec le positionnement.

## Sources

- [Poker Academy, offre Spin&Go with Solver](https://poker.academy/blog/post/introducing-the-new-spingo-with-solver-plan)
- [GTO Wizard, avis et prix (PokerListings)](https://www.pokerlistings.com/poker-tools/trackers/gto-wizard), [VIP-Grinders](https://www.vip-grinders.com/poker-tools/gto-wizard/)
- [ICMIZER SNG Coach (App Store)](https://apps.apple.com/us/app/id1212375605)
- [GTO Sensei (App Store)](https://apps.apple.com/us/app/id1523876570)
- [Poker Coaching (App Store)](https://apps.apple.com/app/id1444569705), [Poker Flight Simulator](https://apps.apple.com/app/id6786825538), [Poker Preflop Trainer PRO](https://mwm.ai/apps/poker-preflop-trainer-pro/1624849305)
- [Spinlab, logiciels de casino (Trustpilot)](https://ch.trustpilot.com/review/spinlab.studio), [SlotCatalog](https://slotcatalog.com/en/soft/spinlab)
- [Advanced Poker Training, entraîneur Spin-N-Go](https://www.pokertraining.com/poker/blog/spin-n-go-training-has-arrived/), [FAQ](https://spinngo.pokertraining.com/poker/faq.php)
- [Historique Expresso et Spin & Go (PokerNews)](https://www.pokernews.com/strategy/spin-and-go-poker-36231.htm)
