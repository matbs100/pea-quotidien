## 2026-11-13 · Contrastes des textes mesurés dans les deux thèmes
- Le vert, l'ambre et le gris « neutre » du thème clair sont légèrement assombris pour que tous les textes de couleur atteignent le contraste 4,5:1 (norme WCAG AA, W3C SC 1.4.3), sur le fond, la carte et leurs fonds doux. Le thème sombre était déjà conforme (5,3 au minimum). Un test vérifie désormais les deux thèmes à chaque modification. Aucune information changée. Décision D-20261112-2.

## 2026-11-13 · Glisser vers le bas pour fermer une fiche (Design, D-2026-11-13 sans tirets-1)
Fiche fermée au glissement sur téléphone (seuil 120 px ou geste rapide), poignée plus facile à saisir. Aucune information retirée.

---
tags: [pea, agent, apprentissage]
---
# 🛠 Nouveautés du programme

Du plus récent au plus ancien. Chaque entrée commence par `## AAAA-MM-JJ · titre` : la fiche du jour affiche la plus récente.

## 2026-11-12 · Contrôle qualité : le chef doit atteindre le vert
- Une alerte 🟠 « À surveiller » ne reste plus en suspens : le chef la corrige, ou la vérifie lui-même sur une source et l'inscrit avec sa preuve dans `pilotage/verifie.json` ; le contrôle la compte alors ✔ vérifiée. Une alerte non prouvée reste orange, un 🔴 ne peut jamais être levé. Le vérificateur du code relit ces preuves chaque jour. Le contrôle ne signale plus non plus la régénération de la dernière fiche existante au moment du commit (le chef la refait chaque matin pour vérifier le rendu) : seules les pages plus anciennes restent signalées. Décision du propriétaire.

## 2026-11-12 · Contrôle qualité : les liens Yahoo ne sont plus signalés à tort
- Depuis le cloud, la page HTML de Yahoo Finance répond « 404 » pour des symboles pourtant valides (FOO.PA, CD8.PA). Le contrôle quotidien ne les compte plus comme cassés quand le symbole a bien des cours collectés : plus de faux rouge. Aucun effet sur la fiche. Décision D-20261112-1.

## 2026-11-12 · Comparer deux titres (base 100) dans le graphique
- Dans la fiche d'un titre, sous « Historique du prix », un menu « Comparer avec… » ajoute la courbe d'un autre placement : les deux courbes partent de 100 au début de la période choisie (1 mois à 5 ans), pour voir lequel a le plus progressé. Touche le graphique pour les deux valeurs d'un jour. Comparaison du passé : ni prévision ni conseil. Inspiration : comparateurs base 100 des outils de suivi de portefeuille. Décision D-20261106-7.

## 2026-11-11 · Carte « Mois par mois » dans la fiche de chaque titre
- Dans la fiche d'un titre, nouveau bloc « Mois par mois » : le rendement de chaque mois des 5 dernières années, une ligne par année, en vert pour une hausse et en rouge pour une baisse (plus la couleur est foncée, plus l'écart est grand). Touche une case pour la valeur exacte. Calculé sur les clôtures hebdomadaires, donc approximatif ; le passé ne prédit pas l'avenir. Inspiration : tableaux de rendements mensuels des outils de suivi de portefeuille. Décision D-20261106-6.

## 2026-11-10 · Le contexte des taux de la BCE
- Nouvel encadré sous l'analyse du jour : les trois taux directeurs de la Banque centrale européenne (dépôt 2,50 %, refinancement 2,65 %, prêt marginal 2,90 %), avec leur date d'entrée en vigueur, le taux précédent et un lien vers la BCE. Les taux sont lus chaque jour à la source (`scripts/taux.py`), jamais écrits en dur ; sans réseau, le dernier relevé est affiché avec sa date. Information de contexte, pas un conseil. Inspiration : bulletin économique de la BCE n° 5/2026. Décision D-20261110-1.

## 2026-11-10 · Nettoyage d'un import inutile (D-20261110-2)

`scripts/wealins.py` n'importe plus `date` (inutilisé). Aucun effet sur la fiche.

## 2026-11-10 · « Mes critères » dit combien de titres sont écartés faute de donnée
- Quand tu règles un critère de risque ou de baisse sur 1 an, le bilan indique maintenant combien de titres du Top 30 sont écartés parce que cette donnée manque, au lieu de les cacher en silence. Ce n'est pas un conseil. Décision D-20261109-2.

## 2026-11-10 · Frais de chaque titre, devise de chaque cours, OPCVM éligibles au PEA, sécurité
- Frais : sur chaque ligne (Top 30, critères, recherche) et dans chaque fiche, frais de gestion annuels et frais de transaction (courtage BNP Paribas Bourse Start en ligne, plafonné à 0,5 % dans le PEA ; TTF 0,4 % ; droits de garde 0,4 % + 5 € par ligne), avec une simulation pour 100, 500 ou 1 000 € et le total sur un an. Demande du propriétaire.
- Devises : chaque cours affiche sa devise (EUR, USD, DKK…), et « pts » pour un indice.
- OPCVM : nouvelle section « OPCVM éligibles au PEA » (11 SICAV et FCP, `opcvm.json`), avec frais courants, droits d'entrée et de sortie, commission de surperformance, SRI ; valeur liquidative lue chaque jour (`scripts/opcvm.py`) ; un OPCVM se saisit aussi dans « Mes investissements » par son ISIN.
- Sécurité : politique de sécurité du contenu (seul le script de la page, repéré par son empreinte, peut s'exécuter), aucune fuite d'adresse vers les sites externes (no-referrer, noopener noreferrer), refus d'être affichée dans le cadre d'un autre site, liens externes limités au https, données de l'appareil relues et nettoyées.
 à côté des indices, filtre ETF / Actions corrigé
- Sur chaque carte d'indice (CAC 40, Euro Stoxx 50, Stoxx 600, DAX, S&P 500, Nasdaq 100), le prix d'une part d'un ETF éligible au PEA qui le suit s'affiche à droite des points ; dans la fiche de l'indice, un bouton ouvre la fiche de cet ETF. Demande du propriétaire.
- Top 30 : les boutons « ETF » et « Actions » masquent maintenant vraiment les autres lignes (le style des lignes l'empêchait), avec le nombre de titres affichés.
- Agents : revue de presse et estimations d'analystes chaque jour de bourse (`data/presse/`, nouvelle partie de l'analyse), presse économique chaque nuit, et une « ✨ Nouveauté » visible sur le site chaque fin de semaine. Lanceur Mac en double-clic (`Matin PEA.command`).
 : réduire le Top 30 à ce qui compte pour toi
- Nouvelle section avant le Top 30 : tu choisis un risque maximum (sur 7), la plus forte baisse acceptée sur 1 an et le type (ETF ou actions) ; la liste se réduit aux titres du Top 30 qui remplissent ces critères. Les critères restent sur ton appareil. Un titre dont la donnée manque n'est pas retenu. Ce n'est pas un conseil. Première partie : les critères de frais et d'horizon viendront ensuite.
- Inspiration : séparation préférence / capacité de risque (arXiv 2603.09303). Décisions D-20261106-5 et D-20261109-1.

## 2026-11-08 · Textes plus lisibles sur téléphone
- Notes, astuces, boutons de liens, libellés de formulaires : 14 px au lieu de 13 px ; étiquettes des chiffres clés : 12 px au lieu de 11. Décision D-20261108-1.

## 2026-11-08 · Ratios de Sharpe et de Sortino
- Dans le bloc « Risque » de la fiche détaillée, deux nouvelles lignes : ratio de Sharpe et ratio de Sortino, calculés sur l'historique hebdomadaire (au moins 2 ans), avec une définition au toucher. Ce sont des mesures du passé, pas des prévisions ni des conseils. Elles apparaîtront à la prochaine collecte des statistiques.
- Inspiration : quantstats (Apache-2.0), idée n° 1. Décision D-20261106-8.

## 2026-11-07 · Avertissement des ETF à effet de levier plus précis
- L'avertissement affiché sur les ETF à effet de levier reprend maintenant la formulation de l'AMF (guide du 11/06/2026, p. 5) : placements très spéculatifs, faits pour quelques jours ou semaines, pas pour investir à moyen ou long terme. Décision D-20261107-1.

## 2026-11-07 · Simulateur « et si j'avais investi régulièrement ? »
- Dans la fiche détaillée de chaque titre (hors fonds Wealins), un nouveau bloc montre ce qu'auraient donné 50 € investis chaque mois pendant 5 ans au plus : somme versée, valeur aujourd'hui et gain ou perte en pourcentage. Il apparaît seulement avec au moins 2 ans d'historique.
- Calcul sur l'historique hebdomadaire déjà suivi, sans frais ni impôts, avec des parts fractionnées ; l'avertissement « le passé ne prédit pas l'avenir, ni prévision ni conseil » est affiché dessous.
- Inspiration : pédagogie de l'investissement programmé. Décision D-20261106-4.

## 2026-11-06 · Les agents apprennent aussi dans des PDF de sources vérifiées
- Chaque nuit, l'agent de veille lit au moins un document PDF d'un site vérifié (AMF, Banque de France, BCE, ESMA, Euronext, fournisseurs d'indices, émetteurs d'ETF, recherche) et en écrit une fiche de lecture dans Obsidian : le lien, un résumé avec ses propres mots, les chiffres avec leur page et ce que la fiche peut en tirer.
- Le chef d'orchestre relit chaque fiche (le résumé est-il fidèle ?) et peut donner des lectures comme devoirs. La bibliothèque est dans `apprentissage/lectures/`.
- Les PDF ne sont jamais copiés dans le dépôt (droits d'auteur). Première fiche : le guide de l'AMF sur les ETF. Demandé par le propriétaire.

## 2026-11-06 · Fonds Wealins dans « Mes investissements »
- La barre de recherche trouve aussi les quelque 1 340 fonds de la liste Wealins (supports d'assurance vie), par ISIN ou par nom, même si les mots sont dans le désordre.
- Un fonds a pour prix sa dernière valeur liquidative, toujours affichée avec sa date : un fonds calcule sa valeur une fois par jour et Wealins la publie en général le lendemain. Les montants restent dans la devise du fonds (dollar, livre…).
- Pour un fonds noté dans `mes-investissements.md`, la fiche prend la valeur la plus récente entre Wealins et le Financial Times (règle du propriétaire : une source qui n'a que la veille est écartée), compare les deux quand elles ont la même date, et montre son historique et son risque estimé.
- Demandé par le propriétaire ; la liste est relue une fois par jour, une page par seconde (robots.txt de Wealins : tout est autorisé).

## 2026-11-06 · Moyennes mobiles distinguables sans la couleur
- Dans le graphique, la moyenne courte est en tirets et la longue en pointillés, avec le même style dans la légende : on les distingue même sans voir les couleurs.
- Inspiré des guides d'accessibilité des graphiques (Penn State) ; priorité du chef n° 3.

## 2026-11-06 · Recherche par ISIN dans « Mes investissements »
- Une barre de recherche en haut de « Mes investissements » : tape un ISIN, un nom ou un code, choisis le titre, puis la date, le prix d'une part et le nombre de parts. Le bouton « Ajouter à mes investissements » existe aussi dans chaque fiche détaillée.
- Ces achats restent sur ton téléphone (dans le navigateur) : rien n'est publié. Un ✕ retire un titre.
- La recherche couvre tous les ETF et actions suivis par la fiche ; leurs ISIN se complètent chaque jour. Tous les ETF éligibles au PEA cotés à Paris y sont ajoutés, plus 3 ou 4 ETF à effet de levier, signalés par un badge et un avertissement, et tenus hors du top 30 et des suggestions.
- Demandé par le propriétaire.

## 2026-11-06 · Suggestions du jour et suivi de mes investissements
- Nouvelle partie « Mes investissements » en haut de la fiche : prix du jour de chaque titre acheté, variation sur la séance, évolution depuis l'achat et, si la quantité est notée, valeur et plus-value en euros. Les achats se notent dans `mes-investissements.md` (Obsidian ou GitHub), ou en les donnant à Claude.
- Nouvelle partie « Suggestions du jour » : jusqu'à 5 actions à regarder de plus près, chacune avec la règle qui l'a choisie et une raison chiffrée (nouveau signal, entrée dans le top 30, plus haut sur un an, repli, gros mouvement). Ce n'est pas une liste d'achats.
- Les deux parties ont leur fiche détaillée au toucher, leurs prix contrôlés entre sources, et figurent dans la note Obsidian.
- Demandé par le propriétaire.

## 2026-11-06 · Textes un peu plus grands sur téléphone
- Chiffres des lignes à 13 px (au lieu de 12) et badge de risque à 12 px (au lieu de 11). Contrastes du gris vérifiés : 4,7:1 au minimum en clair, 6:1 en sombre.

## 2026-11-06 · Risque visible sur la page principale
- Chaque ligne du top 30 et des petits prix affiche un badge « Risque 4/7 » (officiel du DIC, ou « estimé » pour les actions), coloré du vert au rouge.
- Un toucher sur le badge affiche sa définition, sans ouvrir la fiche.
- Demandé par le propriétaire ; inspiré du SRI PRIIPs déjà utilisé dans les fiches.

## 2026-11-05 · Définitions au toucher
- Dans les fiches détaillées, les libellés volatilité, pire baisse, bêta, RSI, PER, rendement et moyennes ont une définition courte au toucher, au survol ou au clavier (Tab).
- Inspiré des guides d'accessibilité des graphiques et indicateurs (Penn State, GWU).

## 2026-11-05 · Agent qui apprend et s'améliore chaque nuit
- Nouvelle routine de nuit (3 h) : veille, notes dans ce dossier, une amélioration testée par nuit.
- Tests garde-fous (`scripts/tests.py`) obligatoires avant toute publication.

## 2026-11-05 · Fiches détaillées cliquables
- Un clic sur un titre ouvre sa fiche : graphique sur 5 ans, risque SRI de 1 à 7, frais, caractéristiques, éligibilité PEA selon Boursorama, historique des signaux.

## 2026-11-05 · Contrôle des prix
- Chaque prix affiché est comparé entre Yahoo Finance, Boursorama et le Financial Times.

## 2026-11-05 · Première version
- Fiche animée du matin : indices, euro/dollar, top 30 éligible PEA, 10 petits prix, signaux suivis dans le temps.
