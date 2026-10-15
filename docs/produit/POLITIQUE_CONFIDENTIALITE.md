# Politique de confidentialité de SpinsAcademy (projet)

> **Projet à faire relire par un juriste avant toute mise en ligne publique** (évaluation du MVP, remarque 24). Les
> passages entre crochets sont à compléter par le porteur du projet. Ce texte décrit ce que fait le code au 14/10/2026
> (commit de cette version) ; toute évolution du traitement (comptes, paiement, journal d'usage) impose de le mettre à jour.

## 1. Qui est responsable

Responsable du traitement : [nom ou raison sociale, adresse, courriel de contact].
Hébergeur : [nom, adresse, pays du serveur].

## 2. Les données traitées

SpinsAcademy fonctionne **sans compte** : aucun nom, courriel, mot de passe ni moyen de paiement n'est demandé.

| Donnée | Pourquoi | Où | Durée |
|---|---|---|---|
| Identifiant aléatoire de l'appareil (créé par l'application, gardé dans le stockage local du navigateur) | relier tes séries entre elles pour ta progression | ton navigateur et le serveur | jusqu'à l'effacement, ou [24 mois] sans activité |
| Séries, questions posées, réponses, verdicts et dates | correction, bilan, progression, révision de tes erreurs (1, 3 et 7 jours) | serveur | idem |
| Préférences (séries adaptées activées ou non, date de réinitialisation) | adapter les séries à tes erreurs | serveur | idem |
| Signalements d'une question (motif et commentaire libre) | corriger les questions | serveur | [12 mois] après leur traitement |
| Adresse IP et identifiant de l'appareil, en mémoire vive | limiter le nombre de requêtes (protection contre les abus) | serveur, mémoire seulement | une minute, jamais écrits sur disque |
| Sauvegardes de la base | reprise après incident | serveur | 30 jours (au moins les 7 plus récentes) |

Ne mets pas de données personnelles dans le commentaire d'un signalement.

Aucune donnée sur de vrais adversaires : les profils de l'entraînement exploitant sont fictifs.

Pas de cookie publicitaire, pas de mesure d'audience, aucun service tiers ne reçoit tes données, pas de service d'IA.
Le temps de réponse aux questions n'est pas enregistré. [Si le journal d'usage de la bêta est mis en place : le décrire ici
(événements, durée, base légale) avant son activation ; il attend l'accord du porteur du projet.]

## 3. Base légale

Exécution du service que tu demandes (correction et suivi de ton entraînement) et intérêt légitime pour la sécurité
(limitation des requêtes, sauvegardes). [À confirmer par le juriste.]

## 4. Tes droits

- **Accès et portabilité** : « Ma progression », puis « Exporter mes données » (fichier JSON), ou route `GET /users/me/export`.
- **Effacement** : « Ma progression », puis « Effacer mes données » : toutes tes séries, réponses et préférences sont supprimées
  du serveur ; elles disparaissent des sauvegardes au plus tard 30 jours après.
- Effacer les données du site dans ton navigateur supprime l'identifiant : tes séries restent alors sur le serveur sans lien
  avec ton appareil ; demande-nous leur effacement avant, ou utilise le bouton.
- Rectification, opposition, limitation : [courriel de contact].
- Réclamation : Commission nationale de l'informatique et des libertés (CNIL), www.cnil.fr.

## 5. Sécurité

Connexion chiffrée (HTTPS), serveur à accès restreint, administration protégée par un jeton, sauvegardes vérifiées
(`docs/exploitation/SECURITE.md`, `docs/exploitation/SAUVEGARDES.md`).

## 6. Version de démonstration

La démonstration autonome (une page sans serveur) garde ta progression **dans ton navigateur uniquement**. Si tu y signales
une question, le signalement (question, réponse, motif, commentaire) est enregistré dans la base de la page de démonstration,
lisible par le porteur du projet, avec l'identifiant de ton compte sur la plateforme qui héberge la page.

## 7. Modifications

Date de cette version : [à la mise en ligne]. Toute modification importante sera signalée dans l'application.

---

Points ouverts pour le juriste :
1. Durées de conservation (proposées : 24 mois sans activité pour l'historique, 12 mois pour les signalements traités).
2. Mentions légales (éditeur, hébergeur) et conditions d'utilisation, à rédiger à part.
3. Données dérivées de HoldemResources Calculator (droits sur les EV affichées) : sujet distinct, bloquant avant la vente
   (évaluation du MVP, remarque 27).
4. Journal d'usage de la bêta (remarque 11) : information et, si nécessaire, consentement avant activation.
