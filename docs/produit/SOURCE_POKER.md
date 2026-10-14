# Source poker : Poker Académie (résumé de l'étude, 2026-10-14)

Résumé de l'étude de https://www.poker-academie.com (pages publiques, sans compte). Détail complet : [`CONCURRENCE.md`](CONCURRENCE.md) ; adresses Spin / Expresso : [`CONCURRENCE_URLS.md`](CONCURRENCE_URLS.md).

## Démarche

1. Page des tarifs, puis tout le site : accueil, vidéos, articles, ranges, coaching, replayer, boutique, e-books, offre Winamax, CGU.
2. Forum (Discourse) : 120 sujets de la catégorie « Sng & Expresso », 10 fils lus en entier. 10 autres sont restés inaccessibles (limite de débit du forum, respectée sans contournement).
3. Sitemap : 189 adresses Spin / Expresso, dont 13 pages clés lues (formation Spin Card, cours collectifs, quiz).
4. Comparaison des thèmes enseignés avec le périmètre du dataset `gto_preflop`.

## À retenir

**Droits.** CGU §10 : contenus réservés à un usage personnel, diffusion soumise à un accord écrit. **Aucun contenu n'est réutilisable** dans les datasets ou les explications. Rien n'y est d'ailleurs traçable à une source calculée (ni HRC, ni solveur). Usage retenu : étude de marché, thèmes à couvrir, repères de prix, experts à contacter.

**Modèle.** École généraliste créée en 2005, orientée cash game et MTT. Formules Gratuit, Silver à 19 €/mois et Gold à 49 €/mois. Le vrai moteur économique est **l'affiliation aux salles** : rakeback, bonus, points échangés en boutique. Coaching privé de 60 à 400 €/h, sans spécialiste Spin.

**Spin / Expresso.**
- Contenu riche entre 2021 et 2023 : formation gratuite « Spin Card » de 8 semaines (Spin 0,25-2 €), une cinquantaine de webinaires gratuits, quelques quiz.
- Ce contenu est aujourd'hui **à l'abandon** : aucune vidéo Spin depuis juillet 2025, et seulement 4 ranges sur le site, aucune en Spin.
- Les pages publiques ne sont que des annonces : le contenu réel est dans des replays réservés aux inscrits.
- **Aucun entraînement interactif** : les quiz ont été des opérations ponctuelles, corrigées par une vidéo la semaine suivante, sans source des ranges.

**Thèmes face au dataset.** Les thèmes préflop enseignés (push/fold, BTN contre BB à 25 BB, heads-up avec limp à 8 BB) sont **déjà couverts** par les familles du dataset. Les écarts sont pédagogiques et figurent déjà dans le plan MVP : règle à retenir (remarque 12), exploitant étendu (17), reconnaître un profil (18), après-flop (19).

**Ce que disent les joueurs (forum).**
- Ils mesurent leur jeu en **cEV** : environ 80 est correct, plus de 100 est un bon joueur, environ 40 est le seuil de rentabilité une fois le rake payé.
- La **variance** les angoisse : « combien de Spins pour savoir si je suis gagnant ? », jusqu'à un joueur toujours perdant après 20 000 Spins.
- Les débutants ne savent pas **où ils perdent**. Les erreurs citées : des tapis non faits, des fautes en BB.
- Ils veulent une stratégie simple, appliquée « sans réfléchir ». Les tables de ranges GTO brutes et sans source déçoivent.
- L'exploitation se pense en **profils** (VPIP / PFR).
- Ils cherchent à **progresser à plusieurs** : deux groupes de travail Expresso micro-limites montés en 2025 et 2026.

## Conséquences pour SpinsAcademy

1. **Créneau libre** : entraînement actif Spin / Expresso corrigé par l'EV, ce que personne ne propose en français.
2. **Cible** : Expresso Winamax et Spin de 0,25 à 2 €, débutants et intermédiaires, préflop et push/fold, sessions courtes.
3. **Argument** : juger son jeu décision par décision plutôt qu'au résultat, et traduire l'écart d'EV en cEV par partie, l'unité des joueurs.
4. **Différenciation** : traçabilité HRC et stratégies simplifiées, face aux tables de ranges sans source.
5. **Rétention** : objectif quotidien, série de jours, révision espacée des erreurs (remarque 21).
6. **Prix** : une offre payante autour de 9 à 15 €/mois paraît cohérente (`OFFRE.md`). L'affiliation à un opérateur agréé ANJ est une piste pour financer le gratuit.
7. **Expert** : coachs francophones Spin / Expresso repérés (Blagops, Nico, CallAuQQ, Mikepierce69) pour la relecture experte (remarque 14). Poker Académie est aussi un **partenaire possible** : sa boutique distribue déjà des trainers tiers.

## Suites possibles

- Relire plus tard les 10 fils du forum restés inaccessibles.
- Étudier la concurrence directe : trainers Spin / Expresso spécialisés.
