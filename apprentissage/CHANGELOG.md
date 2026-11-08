---
tags: [pea, agent, apprentissage]
---
# 🛠 Nouveautés du programme

Du plus récent au plus ancien. Chaque entrée commence par `## AAAA-MM-JJ · titre` : la fiche du jour affiche la plus récente.

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
