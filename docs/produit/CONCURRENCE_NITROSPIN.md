# Concurrence : NitroSpin (nitrospin.fr)

Analyse du 2026-10-14. L'espace membre (`/dashboard`) demande une connexion : il est reconstitué à partir des pages publiques (accueil, tarifs, Nitro Lab, Nitro Analytics, Nitro Campus) et du bundle JavaScript servi à tout visiteur. Le bundle peut contenir des fonctions pas encore ouvertes ou d'anciennes offres, signalées comme telles.

## 1. En bref

Plateforme française Spin & Go (Expresso Winamax, Nitro Betclic et PartyPoker) d'un coach unique, Clément (10+ ans de poker, anciennes écuries BitB et Spin Elite). Slogan : « Construis un edge durable. » Écosystème large : formation, entraînement préflop, analyse des mains, HUD Windows, coaching. Concurrent direct.

- **Technique** : application Lovable (React/Vite), Supabase (base et authentification), Stripe (paiement en comptant ou en 3 fois), Google Analytics 4, connexion Google.
- **Espace membre** : onglets Accueil, Campus, Lab, Analytics, Progrès (plus Formation et LeakFinder). L'accueil sert de tableau de bord : étape en cours du parcours, bouton « Continuer », encart « Ta priorité du moment » qui renvoie au Lab.

## 2. Les piliers

| Pilier | Contenu réel (d'après le code) |
|---|---|
| **Nitro Lab** (préflop) | Apprendre, Entraînement, Coloriage, Examen chronométré sans correction, Analyse ; multi-table jusqu'à 15 tables. Actions : Fold, Call/Limp/Check, Raise/Iso, All-in. Ranges « NitroSpin » 0-25 BB, heads-up, BvB et 3 joueurs, contre Reg et contre récréatif ; 193 situations, 48 798 lignes. |
| **Nitro Analytics** | Import serveur des historiques Winamax ; cEV « certifiée » ; analyse par catégorie (HU, BvB, 3 joueurs) et format (Flash 10, Nitro 15, Classique 25) ; adversaires classés Fish, Reg ou Inconnu ; replayer ; rakeback estimé. « Priorités » renvoie au Lab : « Rejoue cette situation dans le Nitro Lab jusqu'à ce que la bonne décision devienne automatique ». LeakFinder sur exports PokerTracker 4. Bouton « Coach IA », « bientôt disponible ». |
| **Nitro Campus** | Cours, vidéos, quiz, fiches PDF. Niveau Academy présent ; parcours Performance et Elite vides dans le code (« Structure prête — modules à venir »). |
| **NitroSpin PC** | Logiciel Windows : HUD Winamax, analyse, Lab hors ligne. Accès « par contact direct ». |

S'y ajoutent des guides gratuits pour le référencement (débuter, variance, bankroll), des tableaux de rakeback Winamax, Betclic et FDJ, et un Discord.

## 3. Tarifs

Absents des pages publiques, présents dans le code.

| Offre | Prix |
|---|---|
| Discovery | Gratuit, sans carte : Lab sur HU SB 9 BB contre Fish ; LeakFinder sur HU SB préflop et postflop ; Analytics limité à 9 BB |
| Range Lab | 9,99 €/mois, sans engagement : tous les outils, sur ses propres ranges |
| Nitro Lab | 129 € puis 11 × 9,90 €, soit 237,90 € pour 12 mois ; ranges acquises à la fin |
| Nitro Analytics | 19,99 €/mois, sans engagement |
| Academy, Performance, Elite | 399 €, 699 €, 999 € (en 3 fois), avec 2, 4 ou 8 h de coaching ; chaque niveau inclut le précédent |
| Continuity (anciens élèves) | 19,99 €/mois ou 199 €/an |
| Coaching à l'heure | 39 €/h, jusqu'à 29,95 €/h par 20 h |

Traces d'anciennes offres dans le code : « Preflop Lab 24 € », « HU BB + BvB + BTN — 39 € », « J'upgrade mon jeu — 179 € ». Le site mesure en interne l'entonnoir activation, tarifs, paiement.

## 4. Points forts

1. **Boucle diagnostic → priorité → exercice** : les mains du joueur font ressortir une fuite, puis la situation à rejouer dans le Lab. Correspond à notre remarque 9 (« À travailler maintenant »).
2. **Couverture proche du jeu réel** : heads-up, BvB et 3 joueurs sur 0-25 BB, contre Reg et contre récréatif. C'est le reproche fait à notre MVP (heads-up à 7 %, exploitant limité au call d'un tapis).
3. **Entrée gratuite efficace** : une situation complète, la plus jouée, et une analyse gratuite de ses propres statistiques.
4. **Multi-table et examen sans correction** pour travailler la vitesse d'exécution.
5. **Prix bas des outils** (10 à 20 €/mois) et ranges conservées.

## 5. Points faibles (nos angles)

1. **Source opaque** : aucun solveur cité. « Certifié » vient d'un registre interne : préflop classé « PRIMARY_SOLVER », références postflop tirées des fiches PDF de coaching, plusieurs sources « A_CLARIFIER ». Notre argument : chaque réponse vient de HRC, avec la perte en BB par décision.
2. **Correction juste/faux** : ni les pages ni le code visible ne chiffrent le coût d'une erreur. Notre écart en BB, « plusieurs bonnes décisions » et les fourchettes sont plus fins.
3. **Pas d'ICM** (seulement un texte marketing). Pareil chez nous.
4. **Offre plus large que le contenu** : Campus Performance et Elite vides, Coach IA et LeakFinder annoncés « en finalisation », témoignages anonymes sans résultats chiffrés.
5. **Offre complexe** : une dizaine de formules qui se recoupent, prix absents des pages publiques.
6. **Ordinateur nécessaire pour l'analyse** (PokerTracker 4, logiciel Windows). Notre application est pensée pour le mobile.

## 6. Conséquences pour SpinsAcademy

- **Priorités confirmées** : heads-up à 35 % (remarque 7 du plan d'évaluation) et exploitant étendu (remarque 17). Sur la couverture, NitroSpin est devant.
- **Différence à mettre en avant** : EV exacte et traçable, « règle à retenir » (remarque 12), mobile, révision espacée.
- **Piste nouvelle** : mode examen chronométré sans correction, peu coûteux avec notre moteur.
- **Pour `OFFRE.md`** : repères de prix d'environ 10-20 €/mois pour un outil seul et d'environ 240 €/an pour des ranges ; porte d'entrée gratuite sur une situation complète, à étudier.
