# Note juridique préparatoire : SpinXpresso (24/11/2026)

**Ce document n'est pas un avis d'avocat.** Il est rédigé par Plan (une IA) à la demande du porteur, à partir de recherches web du 24/11/2026 (sources en fin de document). Il sert à trois choses : (1) donner au porteur une lecture claire des sujets juridiques ; (2) fixer des règles prudentes à appliquer d'ici là ; (3) préparer une consultation d'une à deux heures avec un avocat (droit du numérique, données personnelles, jeux d'argent) ou un conseil en propriété industrielle. Les articles de loi cités sont à vérifier sur Légifrance (plusieurs sources ne donnent pas le texte consolidé actuel).

## 1. Résumé en dix lignes

| # | Sujet | Niveau de risque estimé | Ce qui est sûr / prudent | Ce qu'un professionnel doit trancher |
|---|---|---|---|---|
| 1 | Données personnelles des formulaires et du Discord | **Moyen** (facile à réduire) | Informer à la collecte (art. 13 RGPD), durée courte, outil dans l'UE avec contrat de sous-traitance | Texte final de la mention ; choix de l'outil |
| 2 | Données de mains Winamax | **Faible** si le fonctionnement actuel est conservé | Lecture dans le navigateur ; seuls des comptages anonymes sortent, et seulement si le joueur les envoie | Conformité aux conditions de Winamax (voir 3) |
| 3 | Règles de Winamax sur les outils tiers et les historiques | **Inconnu : à lire** | Aucune aide en temps réel ; aucune affiliation ; aucun logo | Lecture des conditions de Winamax ; question écrite à Winamax |
| 4 | Publicité du poker et jeu responsable | **Moyen** | Rester dans le registre « outil d'entraînement » ; 18+ ; aucun lien vers une room ; message d'aide | Si la communication de SpinXpresso peut être rangée comme communication commerciale de jeu d'argent |
| 5 | Influenceurs et collaborations | **Moyen** | Accès gratuit = avantage en nature : signaler la collaboration | Formulation exacte de la mention |
| 6 | Marque SpinXpresso | **Moyen** | Votre vérification INPI/EUIPO est un bon début, pas une garantie | Recherche d'antériorités approfondie ; dépôt |
| 7 | Avis des coachs dans l'application | **Moyen** | Aucune mention de leurs noms ; accord écrit pour toute utilisation | Contrat de collaboration ou de cession |
| 8 | Mineurs | **Moyen** | 18+ affiché partout ; majorité demandée | Valeur d'une simple case à cocher |
| 9 | Statut de l'éditeur (vous) | **À décider** | Une activité gratuite de test peut rester en nom propre ; l'offre payante demande une structure | Choix de la structure avant la phase payante |
| 10 | Cookies et mesure d'audience | **Faible** | Aucun traceur : aucun bandeau nécessaire ; journaux techniques de l'hébergeur à mentionner | Rien de plus tant qu'aucun traceur n'est ajouté |

## 2. D10 expliqué simplement
Le formulaire de candidature récolte des données personnelles (pseudo, moyen de contact, habitudes de jeu). Le droit européen (RGPD) impose trois choix, que D10 désigne :
1. **Le responsable des données** : la personne qui décide de recueillir ces données et pourquoi. **C'est vous**, tant qu'il n'y a pas de société ou d'association. Son nom apparaît dans la mention d'information. Recommandation : votre nom (ou votre pseudo professionnel si vous en avez un), plus l'adresse de contact. Dès que vous créez une société ou une association (avant la phase payante), le responsable devient cette structure.
2. **L'outil de formulaire** : un service qui stocke les réponses pour vous (un « sous-traitant »). Il faut un contrat de sous-traitance (DPA) et savoir où les données sont hébergées. Options :
   - **Tally** (société belge, hébergement annoncé dans l'UE, DPA proposé, gratuit) : recommandé, **mais vérifiez sa liste de sous-traitants avant de l'utiliser**, car je n'ai pas pu la lire ([tally.so/help/gdpr](https://tally.so/help/gdpr)).
   - **Framaforms** (association française Framasoft, logiciel libre) : plus simple et sans pistage ; ses conditions et son lieu d'hébergement sont à confirmer sur le site ([framaforms.org](https://framaforms.org)).
   - **Google Forms** : à éviter, société américaine, transferts de données hors UE.
3. **L'adresse de contact** : une adresse dédiée (par exemple `contact@spinxpresso.fr` une fois le domaine acheté, sinon une messagerie gratuite) où les personnes exercent leurs droits (accès, correction, suppression). Elle doit figurer dans la mention d'information et dans les mentions légales de la page.
Quatre autres éléments à fixer : la **durée de conservation** (proposition : fin du test + 3 mois pour les testeurs, suppression immédiate des candidatures non retenues à la fin de la phase 1a), le **service tiers** utilisé, les **journaux techniques** de l'outil, et la présence de **Discord** (service américain).

## 3. Analyse par sujet

### 3.1 Données personnelles (RGPD)
- **Information à la collecte.** Un formulaire doit afficher : qui collecte, pourquoi, quelles réponses sont obligatoires, qui reçoit les données, combien de temps on les garde, quels droits et comment les exercer. La CNIL le précise pour les formulaires de candidature ([guide du recrutement](https://www.cnil.fr/le-guide-du-recrutement)). La mention de `docs/marketing/FORMULAIRES_TESTEURS_v0.3_2026-11-23.md` couvre ces points ; elle manque seulement du nom du responsable et de l'adresse de contact.
- **Durée.** La CNIL rappelle de ne garder les données de candidats que le temps nécessaire. Garder des candidatures en réserve demande le consentement de la personne et est en principe limité à deux ans pour le recrutement ; pour un test de produit, une durée courte (3 mois après la fin du test) est prudente.
- **Liste de contacts de partenaires.** C'est un traitement de données (des personnes identifiables, même sous pseudo) : informations publiques et professionnelles seulement, durée courte, information de la personne dès le premier message (source, droits).
- **Discord** : service américain ; les messages y sont conservés selon ses conditions. L'indiquer ; ne jamais demander d'historiques de mains dans les salons.
- **Mains Winamax** : les historiques peuvent contenir les pseudos des adversaires. Le fonctionnement actuel les traite uniquement sur l'appareil du joueur et n'en exporte que des comptages sans pseudo (vérifié par des tests). Tant que l'application ne reçoit que ces comptages, le risque est faible. Toute future transmission de mains complètes changerait cette analyse.
- **Politique de confidentialité de l'application** : à réécrire avant la bêta ouverte (import local, signalements, Discord, formulaires, hébergeur OVHcloud, journal d'usage anonyme prévu, contribution de comptages, durées). L'actuelle dit « aucun cookie publicitaire, aucun service tiers » : à corriger dès qu'un service tiers est utilisé.

### 3.2 Règles de Winamax (le point le plus important à clarifier)
Je n'ai **pas pu lire** les conditions de Winamax sur les logiciels tiers, les historiques de mains et l'assistance en jeu : mes recherches ne les ont pas retrouvées ([conditions générales](https://api-sesame.cashlib.com/cgu/winamax/cgu-winamax-sesame.pdf) : copie tierce). À faire par le porteur : lire les conditions et le règlement poker sur winamax.fr (rubriques « logiciels tiers », « historique de mains », « assistance »), puis, si le texte n'est pas clair, **poser la question par écrit au support de Winamax** : « un outil d'entraînement qui analyse, hors partie, les fichiers d'historique que le joueur a lui-même exportés, est-il autorisé ? ». Garder la réponse. En attendant, règles prudentes : aucune aide pendant une partie, aucune lecture de l'écran du joueur, aucun lien avec Winamax, nom cité de manière descriptive seulement.

### 3.3 Publicité du jeu et jeu responsable
- Le poker est un jeu d'argent autorisé en ligne en France ; la publicité des jeux d'argent est encadrée (protection des mineurs, interdiction d'inciter à un jeu excessif, message renvoyant à l'aide aux joueurs), et l'ANJ publie des lignes directrices ([ANJ, lignes directrices 2022-C-001](https://anj.fr/sites/default/files/2022-02/Communication%202022-C-001_Lignes%20directrices%20PUB.pdf)). Ces règles visent d'abord **les opérateurs agréés** et leur communication commerciale. SpinXpresso est un outil d'entraînement, sans mise d'argent ; la prudence consiste à ne pas en faire une promotion déguisée de jeu : 18+, aucun lien vers une room, aucune promesse de gains, aucune incitation à jouer plus.
- **Mention d'aide :** le numéro de Joueurs Info Service est bien **09 74 75 13 13** (appel anonyme et non surtaxé, 7 jours sur 7, de 8 h à 2 h du matin, selon les sources consultées) ([findahelpline](https://findahelpline.com/organizations/joueurs-info-service)) ; à reconfirmer sur [joueurs-info-service.fr](https://www.joueurs-info-service.fr) avant publication. Le ⚠ des textes peut être retiré à ce moment-là.
- **À demander à l'avocat :** SpinXpresso entre-t-il, par son contenu ou ses canaux, dans le régime des communications commerciales de jeux d'argent ? Mon analyse : probablement non, mais je ne peux pas l'affirmer.

### 3.4 Influenceurs et collaborations
- La loi du 9 juin 2023 sur les influenceurs, modifiée par l'ordonnance du 6 novembre 2024, encadre l'influence commerciale, y compris pour les jeux d'argent (qui n'y sont pas interdits en tant que tels) ([Dalloz actualité](https://www.dalloz-actualite.fr/document/loi-n-2023-451-9-juin-2023-jo-10-juin), [ordonnance 2024-978](https://www.dalloz-actualite.fr/document/ord-n-2024-978-6-nov-2024-jo-7-nov)). Un streamer qui reçoit un avantage (même un accès gratuit) en échange d'une promotion est dans une collaboration commerciale : prévoir la mention « Collaboration avec SpinXpresso » et un écrit simple décrivant la contrepartie. Texte exact à valider par l'avocat.

### 3.5 Marque
- La vérification INPI/EUIPO du porteur (« libre ») est un bon premier filtre. Elle ne garantit pas l'absence de risque : une marque proche (orthographe, son, classe voisine) ou un nom utilisé sans dépôt peut poser problème. Compléments déjà prévus : TMview, base de l'OMPI, pseudos, recherche web.
- **Dépôt :** INPI 190 € pour une classe et 40 € par classe supplémentaire (grille officielle d'avril 2023 ; tarif à reconfirmer sur [inpi.fr](https://www.inpi.fr/realiser-demarches/propriete-intellectuelle/deposant-et-cout-dune-marque)) ; marque de l'Union européenne environ 850 € pour une classe (source : cabinet d'avocats, à confirmer). Proposition : déposer en France classes 9, 41 et 42 avant l'ouverture publique (environ 270 € au total d'après le tarif INPI de 2023) ; décision du porteur.
- Le nom du domaine ne donne pas de droit de marque ; l'achat des domaines `.fr` et `.com` reste conseillé.

### 3.6 Avis des coachs
- L'application affiche « N experts sur 3 » sur 60 situations : c'est une mention anonyme, mais elle repose sur le travail de trois personnes. Prévoir un **accord écrit** (même court) précisant : leur contribution, l'usage dans l'application, l'absence de nom, la durée, la possibilité de retrait. Aucune mention externe « relu par des experts » tant que cet accord n'existe pas (décision du porteur).

### 3.7 Mineurs
- Interdire aux moins de 18 ans est la règle prudente. Une case à cocher n'est pas une vérification d'âge ; elle sert de déclaration. Discord impose lui-même un âge minimum. À demander à l'avocat : suffit-il pour un outil d'entraînement sans mise d'argent ?

### 3.8 Statut de l'éditeur et mentions légales
- Un site ou une application publiés par un particulier agissant à titre non professionnel peuvent n'indiquer que les coordonnées de l'hébergeur ; **dès qu'il y a une activité professionnelle ou un prix, l'éditeur doit s'identifier**. Avant la phase payante : choisir une structure (micro-entreprise, société ou association), rédiger mentions légales, conditions générales d'utilisation et de vente, politique de confidentialité.

### 3.9 Cookies et audience
- Aucune mesure d'audience, aucun pixel, aucune publicité : aucun bandeau de consentement n'est nécessaire. L'hébergeur enregistre des journaux techniques (adresse IP) : à mentionner. Tout ajout ultérieur (mesure, publicité récompensée) déclenche un bandeau et la mise à jour de la politique.

## 4. Questions à poser à un avocat (liste de consultation)
1. La mention d'information des formulaires (D10) est-elle suffisante ? Le choix de l'outil (Tally ou Framaforms) convient-il ?
2. Les conditions de Winamax permettent-elles l'analyse locale de fichiers d'historique par un outil tiers ? Faut-il une autorisation écrite ?
3. La communication de SpinXpresso relève-t-elle du régime des communications commerciales de jeux d'argent (ANJ) ? Quelles mentions obligatoires ?
4. Mention de collaboration pour un streamer qui reçoit un accès gratuit : formulation, contenu minimal de l'écrit.
5. Marque : la vérification faite suffit-elle ? Quelles classes déposer ? Risque lié au mot « Xpresso » / « Expresso » (format de Winamax) ?
6. Contrat avec les trois coachs : contenu minimal.
7. Mineurs : suffit-il d'une déclaration de majorité ?
8. Structure à créer avant la phase payante ; mentions légales, CGU et CGV.
9. Publicité récompensée dans l'application (étude de fin de bêta) : régie, bandeau de consentement, politique.
10. Liste de contacts de partenaires : conformité (information, durée).

## 5. Règles prudentes à appliquer dès maintenant (sans attendre l'avocat)
- Aucun envoi, aucune publication, aucune réservation publique ne contient : nom de coach, « relu par des experts », promesse de gains, lien vers une room, logo de Winamax.
- 18+ et message d'aide à chaque point de contact public.
- Aucun envoi des formulaires tant que le responsable, l'outil, l'adresse et la durée ne sont pas renseignés et que la mention n'a pas été relue.
- Aucun contact de partenaire tant que D1 (fait), D10, la liste validée et la confirmation de non-lien avec les coachs ne sont pas réunis.
- Conserver les preuves : captures et dates des recherches de marque, réponse de Winamax si elle est demandée.

## Sources (recherches du 24/11/2026)
- [Joueurs Info Service (findahelpline)](https://findahelpline.com/organizations/joueurs-info-service) ; [ANJ, lignes directrices 2022-C-001](https://anj.fr/sites/default/files/2022-02/Communication%202022-C-001_Lignes%20directrices%20PUB.pdf) ; [OFDT, note sur la réglementation des jeux d'argent](https://www.ofdt.fr/sites/ofdt/files/2025-03/note_reglementation_jah_0.pdf)
- [Loi n° 2023-451 (Dalloz actualité)](https://www.dalloz-actualite.fr/document/loi-n-2023-451-9-juin-2023-jo-10-juin) ; [Ordonnance n° 2024-978](https://www.dalloz-actualite.fr/document/ord-n-2024-978-6-nov-2024-jo-7-nov) ; [Vie publique, loi influenceurs](https://www.vie-publique.fr/loi/288793-loi-influenceurs-proposition-de-loi-delaporte-vojetta)
- [CNIL, guide du recrutement](https://www.cnil.fr/le-guide-du-recrutement) ; [Tally et le RGPD](https://tally.so/help/gdpr) ; [Framaforms](https://framaforms.org)
- [INPI, coût d'une marque](https://www.inpi.fr/realiser-demarches/propriete-intellectuelle/deposant-et-cout-dune-marque) ; [tarifs INPI au 1er avril 2023](https://www.inpi.fr/sites/default/files/TARIFS%20APPLICABLES%20AU%201er%20AVRIL%202023.pdf)
- [Conditions générales Winamax (copie tierce)](https://api-sesame.cashlib.com/cgu/winamax/cgu-winamax-sesame.pdf)
