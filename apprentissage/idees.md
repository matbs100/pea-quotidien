---
tags: [pea, agent, apprentissage]
---
# 💡 Idées d'amélioration

Chaque idée est notée avec la grille de la [[Finance/PEA Quotidien/pilotage/decision|méthode de décision]] (notes de 0 à 5) :
**U** utilité (30 %), **R** résultats attendus (25 %), **V** visuel et clarté (20 %), **N** avantage de la
nouveauté (15 %), **F** fiabilité des données (10 %) ; **Gain** = moyenne pondérée ; **C** coût et **Ri** risque
notés à part. Adoptée si Gain ≥ 3,5, Ri ≤ 2 et C ≤ 3 ; à l'essai si Gain ≥ 3 ; rejetée si Gain < 3.
Les décisions et leurs bilans sont dans le [[Finance/PEA Quotidien/pilotage/decisions|journal des décisions]].

Statuts : `proposée`, `adoptée D-…`, `à l'essai D-…`, `en attente : raison`, `fait le AAAA-MM-JJ`,
`rejetée : raison`, `échouée : raison`, `annulée : raison`. Notes passées à la grille le 2026-11-06 (Claude,
à revoir par le chef d'orchestre).

| # | Idée | Source | Indicateur de réussite | U | R | V | N | F | Gain | C | Ri | Statut |
|--:|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| 1 | Ratio de Sharpe et de Sortino dans la fiche détaillée, avec une explication simple | quantstats (Apache-2.0) | ratios affichés pour tous les titres à plus d'un an d'historique, avec une définition au toucher | 3 | 3 | 3 | 4 | 5 | 3,35 | 2 | 1 | à l'essai D-20261106-8 |
| 2 | Tableau des rendements mois par mois sur 5 ans, en carte de chaleur | quantstats (Apache-2.0) | carte lisible au téléphone (360 px) pour les titres à plus de 2 ans d'historique ; page < +5 % | 3 | 3 | 4 | 4 | 5 | 3,55 | 3 | 1 | adoptée D-20261106-6 |
| 3 | Simulateur d'investissement programmé : « 50 € par mois depuis 5 ans auraient donné… », calculé sur l'historique, avec un rappel que le passé ne prédit pas l'avenir | pédagogie, chapitre 6 du manuel | calcul juste sur 3 cas testés ; avertissement visible ; aucune formulation de conseil (contrôle) | 5 | 4 | 4 | 5 | 4 | 4,45 | 3 | 1 | adoptée D-20261106-4 |
| 4 | Alerte dans la notification en cas de forte variation d'un indice (plus de 3 % sur une séance) | idée interne | — | 4 | 3 | 2 | 3 | 5 | — | 1 | 1 | fait le 2026-11-05 (étape 8 de la consigne de la fiche) |
| 5 | Petites définitions au survol ou au toucher (RSI, PER, SRI, volatilité, bêta) | pédagogie, guides d'accessibilité (Penn State, GWU) | — | 4 | — | — | — | — | — | 2 | 1 | fait le 2026-11-05 |
| 6 | Diversification du top 30 en version réduite : les paires de titres les plus corrélées et un indicateur simple de diversification (pas de matrice 30 × 30 au téléphone) | Riskfolio-Lib (BSD-3), PyPortfolioOpt (MIT) | indicateur affiché chaque jour ; calcul vérifié par un test | 4 | 3 | 2 | 4 | 5 | 3,45 | 3 | 2 | à l'essai D-20261106-10 |
| 7 | Comparer deux titres sur le même graphique (base 100) | idée interne | comparaison possible depuis la fiche détaillée en 2 touchers ; aucune régression du graphique (tests) | 4 | 3 | 4 | 4 | 5 | 3,85 | 3 | 2 | adoptée D-20261106-7 |
| 8 | Fiche installable sur l'écran d'accueil du téléphone : manifeste et icône, **sans** service worker (pour ne jamais afficher une ancienne fiche) | bonnes pratiques web | icône et nom corrects une fois ajoutée à l'écran d'accueil ; la fiche reste toujours à jour | 3 | 3 | 3 | 3 | 5 | 3,20 | 2 | 1 | à l'essai D-20261106-9 |
| 9 | Bilan de la semaine le samedi : une fiche spéciale qui résume les 5 séances | idée interne | — | 4 | 3 | 3 | 4 | 5 | 3,65 | 4 | 2 | en attente : coût (une routine de plus sur le quota) ; à faire dans une routine existante |
| 10 | Deuxième source pour l'éligibilité PEA des ETF (page de l'émetteur ou liste Euronext) | contrôle des données | éligibilité confirmée par 2 sources pour au moins 80 % des ETF suivis | 4 | 4 | 1 | 3 | 4 | 3,25 | 3 | 2 | à l'essai D-20261106-11 |
| 11 | Exposition aux devises des ETF (part en dollars) et effet du taux euro/dollar | pédagogie | — | 3 | 3 | 3 | 2 | 3 | 2,85 | 3 | 2 | rejetée : gain < 3 (le risque de change est déjà expliqué dans chaque fiche ; pas de source fiable de la composition) |
| 12 | Backtest du classement : le top 30 d'il y a 3 mois a-t-il fait mieux que le Stoxx 600 ? Seulement avec assez de données accumulées | méthode, contrôle honnête | — | 5 | 5 | 3 | 5 | 4 | 4,50 | 4 | 2 | en attente : données insuffisantes avant le 2027-02-05 |
| 13 | Recherche d'un titre : ouvrir la fiche de n'importe quel titre suivi, pas seulement les affichés | idée interne | — | 3 | 3 | 3 | 3 | 5 | 3,20 | 4 | 2 | en attente : coût (poids de la page) ; à découper : fiches dans des fichiers séparés, chargés à la demande |
| 14 | Bouton clair / sombre manuel | bonnes pratiques web | — | 2 | 1 | 3 | 2 | 5 | 2,25 | 1 | 1 | rejetée : gain < 3 (la fiche suit déjà le mode clair ou sombre du téléphone) |
| 15 | Graphique accessible au clavier (flèches pour parcourir les jours) | accessibilité | — | 2 | 2 | 2 | 3 | 5 | 2,45 | 2 | 1 | rejetée : gain < 3 (le propriétaire consulte la fiche au téléphone) |
| 16 | Écart de suivi des ETF par rapport à leur indice | justETF, documentation des émetteurs | — | 3 | 3 | 2 | 4 | 3 | 2,95 | 4 | 2 | rejetée : gain < 3 tant qu'aucune source ouverte et fiable n'est trouvée |
| 17 | Remplacer le graphique maison par lightweight-charts | tradingview/lightweight-charts (Apache-2.0) | — | 2 | 1 | 3 | 2 | 5 | — | 3 | 3 | rejetée : ajoute une dépendance externe pour un gain faible ; le graphique actuel suffit |
| 18 | Graphiques lisibles par les daltoniens : style de trait en plus de la couleur (fait) ; étiquettes directes en fin de courbe | accessibility.psu.edu/guidelines/charts, nrennie.rbind.io | — | 2 | 2 | 4 | 2 | 5 | 2,70 | 2 | 1 | fait le 2026-11-06 (traits distincts) ; étiquettes : rejetée (gain < 3) |
| 19 | Badge de risque (SRI) sur chaque ligne de la page principale | consigne du chef (demande du propriétaire) | — | 5 | — | — | — | — | — | 2 | 1 | fait le 2026-11-06 |
| 20 | Mention « TTF 0,4 % » sur les actions françaises de la liste officielle BOFiP | Deloitte Avocats, BOFiP | mention juste pour 100 % des sociétés de la liste officielle (vérifiée) | 3 | 4 | 2 | 3 | 5 | 3,25 | 3 | 2 | à l'essai D-20261106-12 (après vérification de la liste officielle) |
| 21 | Page « Mes critères » : le propriétaire note ses critères (horizon, risque accepté, frais, simplicité) et la fiche montre chaque jour les titres qui les remplissent ; la décision reste à lui, sans conseil | idée du propriétaire (05/11) | critères gardés sur le téléphone ; liste filtrée juste (test) ; aucune formulation de conseil | 5 | 3 | 4 | 5 | 4 | 4,20 | 3 | 2 | adoptée D-20261106-5 |
| 22 | Fonds Wealins dans « Mes investissements » (recherche par ISIN ou nom, valeur liquidative datée) | demande du propriétaire (06/11) | ≥ 1 000 fonds trouvables ; liste relue chaque jour ; aucune erreur de fonds au contrôle | 5 | 4 | 4 | 5 | 4 | 4,45 | 3 | 1 | fait le 2026-11-06 (D-20261106-1) |
| 23 | Devise affichée à côté de chaque prix (fonds, ETF, actions), sur la page et dans la note Obsidian | demande du propriétaire (06/11) | toute ligne de prix d'un placement montre sa devise (test) | 4 | 3 | 4 | 3 | 5 | 3,70 | 1 | 1 | fait le 2026-11-06 (D-20261106-2) |
| 24 | Recoupement entre mes ETF : signaler dans « Mes investissements » quand deux ETF détenus suivent des indices qui se chevauchent (par exemple MSCI World et Nasdaq-100), diversification seulement apparente | lecture AMF du 2026-11-06 (p. 2 et 8) | message affiché pour les paires d'indices connues qui se recoupent ; aucune fausse alerte sur les cas testés | 4 | 3 | 3 | 4 | 3 | 3,45 | 3 | 2 | proposée |
| 25 | Correction : avertissement des ETF à effet de levier aligné sur l'AMF (placements très spéculatifs, conçus pour quelques jours ou semaines, pas pour un placement à moyen ou long terme) | lecture AMF du 2026-11-06 (p. 5) | texte de l'avertissement conforme à la source, test du rendu | 4 | 3 | 2 | 2 | 5 | 3,15 | 1 | 1 | proposée (correction) |
