# Défi débloqué par une publicité : note de conception (D8, 05/11/2026)

Décision du porteur (`DECISIONS_2026-11-05.md`, règle 8) : les défis sont gratuits, et « le dernier est déblocable avec de la publicité ». **Rien n'est codé** tant que trois points restent ouverts : quel défi (question posée au porteur), politique de confidentialité réécrite et relue (A14), offre payante définie (P8).

## 1. Quel défi : recommandation
Ordre actuel des cartes : défi du jour, série parfaite ; sous pression, range au cordeau, lecteur de vilain (exploitant) ; semaine pleine.

| Option | Pour | Contre |
|---|---|---|
| **A. Un défi bonus du jour, en plus** (recommandé) | La publicité ajoute quelque chose ; aucun défi gratuit aujourd'hui ne se ferme | Un défi de plus à concevoir (par exemple une série de 5 au chrono 8 s sur le thème de la veille) |
| B. Range au cordeau (le dernier défi jouable en GTO) | Rien à créer | Un défi gratuit devient payant en temps : mal reçu par les testeurs, qui aimaient les défis « sans contrainte » |
| C. Une deuxième tentative du défi du jour | Simple | Contredit la règle d'une seule tentative, tout juste corrigée (test 9), et rend le défi commun inéquitable |

Semaine pleine n'a pas de bouton « Relever » (elle se gagne en s'entraînant) ; Lecteur de vilain est dans le mode exploitant, payant : aucun des deux ne convient.

## 2. Régie et consentement
- **Format** : publicité « récompensée » (le joueur choisit de la regarder, environ 15 à 30 s, puis le défi s'ouvre). Jamais de bandeau ni d'interstitiel imposé.
- **Régie pressentie** : Google Ad Manager, qui propose un format récompensé pour le web (l'application est une page web installable, pas une application native : AdMob ne s'applique pas). À confirmer : acceptation du site par la régie et conditions pour un contenu lié au poker.
- **Catégories bloquées** : jeux d'argent, casinos et paris, pour ne pas faire de publicité pour du jeu réel dans une application d'entraînement (et à cause des règles françaises de l'ANJ). À vérifier avec la régie avant de signer.
- **Consentement** : une plateforme de gestion du consentement certifiée par la régie (TCF 2.2), affichée seulement au premier toucher sur « Débloquer avec une publicité », jamais à l'ouverture de l'application. Refus = publicité non personnalisée si la régie le permet, sinon le repli du §3.
- **Politique de confidentialité** : la phrase « Pas de cookie publicitaire, pas de mesure d'audience, aucun service tiers ne reçoit tes données » (§2 « Les données traitées ») devient fausse ; réécriture et relecture juridique (A14) avant toute activation, en même temps que le journal d'usage anonyme (A17).
- Le script de la régie n'est chargé qu'après le toucher et le consentement : aucun appel à un tiers pour un joueur qui ne débloque rien.

## 3. Repli sans publicité
| Cas | Comportement |
|---|---|
| Abonné (offre payante, P8) | Défi ouvert, aucune publicité |
| Publicité vue jusqu'au bout | Défi ouvert pour la journée |
| Pas de publicité disponible, erreur de la régie | Défi ouvert quand même : le joueur a fait la démarche |
| Bloqueur de publicité, consentement refusé sans publicité possible | Défi fermé, message neutre : « Disponible avec une courte publicité ou avec l'offre payante. » Aucun reproche, aucune relance |
| Démo autonome (artéfact) | Pas de publicité (l'hébergeur bloque les scripts tiers) : défi bonus absent |

Le déblocage est déclaré par la page : la régie web ne fournit pas de confirmation côté serveur. Un joueur peut tricher ; c'est acceptable, puisque les défis ne changent ni la correction ni la progression.

## 4. Hors ligne
Une série demande déjà le serveur (le service worker ne met en cache que la page). Hors ligne, la carte affiche « Disponible en ligne » ; un déblocage obtenu reste valable jusqu'à la fin de la journée locale, même après une coupure.

## 5. Ce que ça change pour la séance et la série de jours
- **Rien d'obligatoire** : la séance du jour, la série de jours, les objectifs et les niveaux ne demandent jamais le défi débloqué ; on peut tout tenir sans voir une publicité.
- Une série du défi débloqué compte comme toute série finie (jour d'activité), sans être nécessaire.
- **Jamais de publicité pendant la séance**, ni avant le défi du jour : au plus une publicité par jour, proposée depuis la carte du défi, une fois la séance faite ou ignorée.

## 6. À mesurer (journal d'usage anonyme, après A14)
Taux de joueurs qui touchent « Débloquer », part des publicités vues jusqu'au bout, effet sur le retour à J+1 et J+7 (comparé aux joueurs qui ne débloquent pas).

## Questions au porteur
1. Option A, B ou C (§1) ?
2. Accord pour démarcher Google Ad Manager, ou une autre régie à étudier ?
3. Le défi bonus est-il offert pendant le test fermé, sans publicité, comme le mode exploitant (conséquence 4 des décisions) ?
