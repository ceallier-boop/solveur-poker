# Défis avec publicité : note de conception (D8, 05/11/2026)

Demande du porteur (réponse du 05/11) : **diviser les défis en défis gratuits et défis avec publicité**. Le partage ci-dessous est la proposition de Plan (`DECISIONS_2026-11-05.md`, « Défis : partage gratuit / publicité »), **à valider par le porteur**. **Rien n'est codé** avant cette validation, la politique de confidentialité réécrite et relue (A14) et l'accord pour démarcher une régie. **Pendant le test fermé, tous les défis restent ouverts, sans publicité.**

## 1. Le partage et l'écran
| Zone de l'accueil | Défis | Accès |
|---|---|---|
| **Défis** | Défi du jour, Sous pression, Semaine pleine (« Semaine complète » dans les décisions) | gratuits, comme aujourd'hui |
| **Défis avec publicité** | Série parfaite, Range au cordeau | une publicité ouvre **les deux** pour la journée |
| Mode exploitant | Lecteur de vilain | payant, avec le mode exploitant |

Aucun niveau, objectif ni critère de séance ne dépend d'un défi : fermer un défi ne bloque jamais la progression.

**Zone « Défis avec publicité »**, sous les défis gratuits :
- **Verrouillée** : les deux cartes gardent leur titre et leur règle, avec un cadenas ; un seul bouton pour la zone : « Débloquer les deux défis du jour (courte publicité) ». Pas de bouton « Relever » sur les cartes.
- **Débloquée** : les cartes redeviennent normales (« Relever », résultat, réussite) jusqu'à minuit, heure de l'appareil ; la zone dit « Ouverts aujourd'hui ». Le lendemain, elle se reverrouille.
- **Abonné** (offre payante, P14) : pas de zone séparée, les deux cartes reviennent parmi les défis, sans cadenas.

Deux règles à ajouter au code, faute de quoi le cadenas se contourne :
1. **Range au cordeau** se gagne aujourd'hui avec n'importe quel exercice de range de la semaine. Défi verrouillé : seules comptent les ranges faites un jour où la zone était ouverte (sinon une range réussie en jeu libre valide le défi sans publicité).
2. **Série parfaite** : le serveur refuse la série (`POST /sessions` avec `challenge=perfect`) si la zone n'est pas ouverte ce jour-là pour ce joueur ; le déblocage est enregistré côté serveur (jour local et joueur invité).

## 2. Régie et consentement
- **Format** : publicité « récompensée » (le joueur choisit de la regarder, environ 15 à 30 s, puis le défi s'ouvre). Jamais de bandeau ni d'interstitiel imposé.
- **Régie pressentie** : Google Ad Manager, qui propose un format récompensé pour le web (l'application est une page web installable, pas une application native : AdMob ne s'applique pas). À confirmer : acceptation du site par la régie et conditions pour un contenu lié au poker.
- **Catégories bloquées** : jeux d'argent, casinos et paris, pour ne pas faire de publicité pour du jeu réel dans une application d'entraînement (et à cause des règles françaises de l'ANJ). À vérifier avec la régie avant de signer.
- **Consentement** : une plateforme de gestion du consentement certifiée par la régie (TCF 2.2), affichée seulement au premier toucher sur « Débloquer les deux défis du jour », jamais à l'ouverture de l'application. Refus = publicité non personnalisée si la régie le permet, sinon le repli du §3.
- **Politique de confidentialité** : la phrase « Pas de cookie publicitaire, pas de mesure d'audience, aucun service tiers ne reçoit tes données » (§2 « Les données traitées ») devient fausse ; réécriture et relecture juridique (A14) avant toute activation, en même temps que le journal d'usage anonyme (A17).
- Le script de la régie n'est chargé qu'après le toucher et le consentement : aucun appel à un tiers pour un joueur qui ne débloque rien.

## 3. Repli sans publicité
| Cas | Comportement |
|---|---|
| Test fermé | Les deux défis ouverts, sans publicité ni cadenas |
| Abonné (offre payante, P14) | Les deux défis ouverts, aucune publicité |
| Publicité vue jusqu'au bout | Les deux défis ouverts jusqu'à minuit |
| Pas de publicité disponible, erreur de la régie | Les deux défis ouverts quand même : le joueur a fait la démarche |
| Bloqueur de publicité, consentement refusé sans publicité possible | Zone fermée, message neutre : « Disponible avec une courte publicité ou avec l'offre payante. » Aucun reproche, aucune relance |
| Démo autonome (artéfact) | Pas de publicité (l'hébergeur bloque les scripts tiers) : les deux défis restent ouverts, comme dans le test fermé |

La fin de la publicité est déclarée par la page : la régie web ne fournit pas de confirmation côté serveur. Un joueur peut tricher ; c'est acceptable, puisque les défis ne changent ni la correction ni la progression.

## 4. Hors ligne
Une série demande déjà le serveur (le service worker ne met en cache que la page). Hors ligne, la zone affiche « Disponible en ligne » ; un déblocage obtenu reste valable jusqu'à minuit, même après une coupure.

## 5. Ce que ça change pour la séance et la série de jours
- **Rien d'obligatoire** : la séance du jour, la série de jours, les objectifs et les niveaux ne demandent jamais les défis avec publicité ; on peut tout tenir sans voir une publicité. La série de jours et Semaine pleine restent gratuites.
- Une série d'un défi avec publicité compte comme toute série finie (jour d'activité), sans être nécessaire.
- **Jamais de publicité pendant la séance**, ni avant le défi du jour : au plus une publicité par jour, proposée depuis la zone, jamais affichée d'office.
- Risque connu : deux défis aujourd'hui gratuits se ferment ; les testeurs aimaient les défis « sans contrainte ». À observer après le test fermé (taux de déblocage, retour à J+1).

## 6. À mesurer (journal d'usage anonyme, après A14)
Taux de joueurs qui touchent « Débloquer les deux défis du jour », part des publicités vues jusqu'au bout, effet sur le retour à J+1 et J+7 (comparé aux joueurs qui ne débloquent pas).

## Questions au porteur
1. Valides-tu le partage du §1 (gratuits : Défi du jour, Sous pression, Semaine pleine ; avec publicité : Série parfaite, Range au cordeau) ?
2. Accord pour démarcher Google Ad Manager, ou une autre régie à étudier ?
3. Range au cordeau verrouillé : d'accord pour ne compter que les ranges faites un jour où la zone est ouverte (§1, règle 1) ?
