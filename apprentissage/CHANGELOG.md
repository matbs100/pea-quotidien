---
tags: [pea, agent, apprentissage]
---
# 🛠 Nouveautés du programme

Du plus récent au plus ancien. Chaque entrée commence par `## AAAA-MM-JJ · titre` : la fiche du jour affiche la plus récente.

## 2026-11-25 · Prochaine réunion de la BCE affichée sous les taux (Nuit, D-20261125-2)

Sous l'encadré des taux, la note indique « Prochaine réunion de la BCE : décision le … » avec un lien vers le calendrier officiel ; la date change toute seule après chaque réunion. Rien n'est retiré. Inspiré de l'idée n° 77 (presse du 23/11) ; calendrier lu sur ecb.europa.eu. La Fed n'est pas ajoutée.

## 2026-11-25 · Encadré « Aucun investissement » compact sur téléphone (Design, D-20261125-1)

CSS seul (≤ 480 px) : marge et taille réduites, texte inchangé ; « Les marchés » apparaît dans le premier écran à 390×844. comparer 🟢, 61/61 tests.

## 2026-11-24 · Les mots « indice » et « clôture » expliqués au toucher (Nuit, D-20261124-2)
Dans la phrase-résumé sous la date, « indice » et « clôture » sont soulignés en pointillés : un toucher affiche leur définition en une phrase, un second la referme. Rien n'est retiré. Inspiré de l'idée n° 74 (revue du chef du 22/11, jargon pour un débutant).

## 2026-11-24 · Pastille « Risque » plus facile à toucher (Design, D-20261124-1)
La pastille Risque mesure au moins 24 px de haut (norme WCAG 2.5.8). Rien n'est retiré de la page.

## 2026-11-23 · La carte du monde des titres suivis (D-20261123-4)

- En bas de la fiche, un globe à faire tourner du doigt ou à la souris : les pays où se trouvent les titres suivis sont en orange. Toucher un pays rapproche la vue et ouvre sa fiche : son drapeau, quelques clins d'œil, les chiffres de la séance et ses titres, du plus au moins performant. Actions : pays du siège ; ETF : pays de création, sauf ceux qui investissent aux États-Unis, au Japon ou en Inde, et les 4 ETF émergents et Asie, placés dans chaque pays couvert. Tracé des pays : Natural Earth (domaine public).
- Avec la carte, l'éligibilité au PEA de chaque titre suivi est contrôlée chaque nuit (D-20261123-5) : un titre non éligible ou à vérifier le dit sur la carte et dans sa fiche.
- Premier contrôle : Unibail-Rodamco-Westfield, foncière au régime SIIC, n'est pas éligible au PEA ; il ne fait plus partie des titres suivis (D-20261123-6).

## 2026-11-23 · Un cours ancien le dit sous le prix de la ligne (Nuit, D-20261123-2)

- Dans les listes (Top 30, valeurs connues, petites valeurs), le mot « prix » devient « cours du 20 nov. » quand le cours date d'un autre jour que la fiche (« valeur du … » pour un fonds). Aucune ligne plus haute. Source : alerte « cours ancien » du contrôle, idée n° 75.

## 2026-11-23 · Cartes des marchés : prix de l'ETF plus coupé à 320–390 px (Design, D-20261123-1)

- Le prix d'une part d'ETF et « 1 part d'ETF » passent sous le prix de l'indice quand la place manque, au lieu de dépasser de la carte. Rien retiré.

## 2026-11-23 · Un ETF non éligible au PEA retiré (D-20261123-1)
L'ETF BNP Paribas Easy MSCI Emerging (EEMK) n'est pas éligible au PEA : il ne fait plus partie des titres suivis.

## 2026-11-22 · Le résumé du marché sépare l'Europe et New York (D-20261122-4)
La phrase en haut de page ne compte plus ensemble des marchés qui n'ont pas les mêmes heures. Elle donne d'abord l'Europe du jour, puis le S&P 500 à part, en disant si New York est encore ouverte ou de quel jour date sa clôture. L'accord « 1 montent » est corrigé. Les cartes des indices ne changent pas.

## 2026-11-22 · Repère de l'ESMA sur 10 ans dans le bloc Frais (Nuit, D-20261122-2)
Le bloc Frais ajoute un repère : selon le régulateur européen (ESMA, rapport 2023), 10 000 € placés 10 ans dans un portefeuille type de fonds européens valent 14 850 € après 2 000 € de frais, environ 13 500 € après inflation. Exemple passé (2013-2022), pas une prévision ni un conseil. Inspiration : lecture du rapport ESMA. Idée n° 70. Test `repere_esma_dix_ans`.

## 2026-11-22 · Bandeau « Nouveau » lisible pour un débutant (Design, D-20261122-1)

Le bandeau n'affiche plus les étiquettes internes ; le texte complet reste ici.

## 2026-11-21 · Repère des frais moyens dans le bloc Frais d'un ETF (D-20261121-3)

Le bloc Frais d'un ETF montre le repère de l'AMF : 0,38 % par an en moyenne pour les ETF indiciels actions, 1,33 % pour les fonds d'actions français (2024). Pour comparer, pas pour choisir.

## 2026-11-21 · ✨ Nouveauté : frais sur 10 ans dans la fiche d'un titre (Nuit, D-20261121-2)
Le bloc Frais ajoute une ligne « Sur 10 ans » : achat, 10 ans de gestion et de droits de garde, revente, pour 100, 500 ou 1 000 €. Calcul simple, valeur supposée constante et frais d'aujourd'hui : ce n'est pas une prévision. Inspiration : lecture de la lettre AMF n° 61 sur les frais. Idée n° 66 ; aucun conseil. Test `frais_sur_dix_ans`.

## 2026-11-21 · Une phrase en haut de page résume le marché (Design, D-20261121-1)
- Sous la date : combien d'indices montent ou baissent, avec le CAC 40 et le S&P 500.

## 2026-11-20 · Transfert de PEA : un délai à prévoir (Chef, D-20261120-3)
Le bloc fiscalité ajoute une phrase : dans l'échantillon de grands teneurs de compte du rapport de l'AMF (2023, p. 8), 80 % des transferts de PEA étaient faits en moins d'un mois, mais aucun délai n'est garanti. Information, pas un conseil.

## 2026-11-20 · Inflation : date de mise à jour d'Eurostat sur la carte (Nuit, D-20261120-1)
La carte d'inflation de la zone euro indique maintenant « chiffre mis à jour par Eurostat le 18 nov. 2026 », pour que le lecteur sache si la valeur a été revue. Eurostat ne dit pas « estimation rapide » ou « finale » dans ses données : seule la date est affichée, rien n'est supposé. Chiffre inchangé (octobre : 4,0 %). Idée n° 61 ; aucun conseil. Test `taux_bce` étendu.

## 2026-11-20 · Toucher sur la pastille Risque ouvre la fiche (Design, D-20261120-1)

Un toucher n'importe où sur une ligne, pastille « Risque » comprise, ouvre la fiche ; l'explication du risque y figure.

## 2026-11-19 · Note d'étude du signal : « la meilleure règle » (Chef, D-20261119-2)
La note sous le signal de tendance dit maintenant que la **meilleure règle testée** bat la détention avant frais (et non « les règles »), comme l'étude arXiv 1504.04254 (PDF relu par le chef). Aucun conseil.

## 2026-11-19 · Ce que dit une étude sur le signal de tendance (Nuit, D-20261119-1)
Sous le signal technique de chaque fiche, une note cite une étude (Zhu et al., arXiv 1504.04254) : sur les indices de Shanghai et de Shenzhen (1991-2013), les moyennes mobiles battent la simple détention avant frais, mais plus après. La note précise que c'est une seule étude, sur des marchés chinois. Idée n° 55 ; aucun conseil. Test `aide_signal_etude_tendance`.

## 2026-11-18 · Transfert de PEA dans le bloc fiscalité (Nuit, D-20261118-2)
Une ligne ajoutée sous le bloc « PEA : fiscalité en un coup d'œil » : changer de banque en transférant tout son PEA n'est pas un retrait, et les avantages fiscaux sont conservés. Source : AMF, FAQ PEA et PEA PME-ETI (p. 1). Aucun conseil. Test `bloc_fiscalite_pea` étendu.

## 2026-11-18 · Défilement au doigt sur les lignes (Design, D-20261118-1)

Le propriétaire ne pouvait pas faire défiler la page en glissant sur une ligne (iPhone). Corrections de causes probables : `overflow-x: clip` sur `body`, fiche et voile fermés en `display: none`, `touch-action: manipulation` sur les lignes, effet de pression réservé à la souris. Test tactile ajouté.

## 2026-11-17 · Verre dépoli sur la fiche détaillée (Design, D-20261117-1)
En-tête de fiche et info-bulle de risque en verre dépoli (repli opaque). Aucune information retirée.

## 2026-11-17 · ✨ Nouveauté : l'inflation de la zone euro dans « Le contexte des taux » (Nuit, D-20261117-2)
Une quatrième carte donne l'inflation sur un an de la zone euro (octobre 2026 : 4,0 %, après 3,8 % en septembre), à côté des taux de la BCE, pour situer le taux de dépôt. Le chiffre est lu chaque jour sur Eurostat (la série de la BCE n'a plus de données après 2025), avec un lien vers la source ; information, pas un conseil. Idée n° 46.

## 2026-11-17 · ✨ Nouveauté : chercher un ISIN non suivi sur Boursorama, justETF ou Fundsquare (Chef, D-20261117-1)
Quand la recherche « Mes investissements » ne connaît pas un ISIN valide, des liens ouvrent sa page chez Boursorama et justETF (et Fundsquare pour un fonds luxembourgeois), dans un nouvel onglet. Aucun appel depuis la page ; Euronext n'est pas proposé, sa recherche n'a pas pu être vérifiée.

## 2026-11-16 · ✨ Nouveauté : 30 valeurs connues, et risque et frais lus dans le DIC officiel (Propriétaire, D-20261116-3 et D-20261116-4)
Nouveau bloc « 30 valeurs connues » sous le Top 30 : grandes actions européennes cotées depuis longtemps et ETF répandus (Monde, Nasdaq-100, Japon, Asie, émergents, Inde), la même liste chaque jour. Le risque (SRI) et les frais courants de chaque ETF sont maintenant lus dans son DIC officiel (Fundsquare, sinon Amundi ETF) plutôt que sur Boursorama, qui donnait les frais maximum du prospectus ; la fiche affiche aussi les coûts de transaction du fonds et des liens vers Fundsquare et Quantalys.

## 2026-11-16 · Comparaison de deux titres : le choix est mémorisé (Nuit, D-20261116-2)
Le titre choisi dans « Comparer avec… » est gardé sur l'appareil (jamais publié) et repris à l'ouverture d'une fiche s'il est encore proposé ; choisir « Comparer avec… » efface la comparaison. Source : idée n° 7, 2e partie (D-20261106-7).

## 2026-11-16 · Unité (devise) sur le graphique de fiche (Design, D-20261116-1)
Le résumé du graphique de fiche indique « Prix en EUR · axe de droite » et le libellé lu par les lecteurs d'écran contient la devise et la variation. Aucune information retirée.


## 2026-11-15 · ✨ Nouveauté : exceptions au retrait avant 5 ans dans le bloc fiscalité
Une note sous les 4 cartes dit que licenciement, invalidité (2e ou 3e catégorie) et mise à la retraite par l'employeur évitent la clôture du PEA, pour le titulaire ou son conjoint. Source : service-public.gouv.fr F22449 (page vérifiée le 15/04/2026). Décision D-20261115-2.

## 2026-11-15 · Lignes du Top 30 sans chevauchement sur petit téléphone (Design, D-20261115-1)
À 360 px, les variations (1 jour, 1 mois, 3 mois) passaient sous la pastille de signal ; elles tiennent maintenant jusqu'à 320 px.

## 2026-11-14 · ✨ Nouveauté : « PEA : fiscalité en un coup d'œil »
- Un nouveau bloc, avant les suggestions, résume en 4 cartes les chiffres du PEA : plafond de 150 000 €, 12,8 % d'impôt avant 5 ans, 18,6 % de prélèvements sociaux, 0 % d'impôt sur le revenu après 5 ans. Date de relecture affichée (13/11/2026) et liens vers service-public.gouv.fr ; information générale, ni conseil fiscal ni conseil d'investissement. Décision D-20261113-3.

## 2026-11-14 · Cartes marchés sans point orphelin sur téléphone (Design, D-20261114-1)
Le séparateur « · » est masqué sous 600 px (il commençait la 2e ligne). Aucune information retirée.

## 2026-11-13 · « Mois par mois » : mois en trois lettres
- Les initiales J, F, M, A… se répétaient (J trois fois, M deux fois) : la carte affiche maintenant jan, fév, mar, avr, mai, jun, jul, aoû, sep, oct, nov, déc. Aucun chiffre changé. Décision D-20261113-2.

## 2026-11-13 · Glisser vers le bas pour fermer une fiche (Design, D-20261113-1)
Fiche fermée au glissement sur téléphone (seuil 120 px ou geste rapide), poignée plus facile à saisir. Aucune information retirée.

## 2026-11-13 · Contrastes des textes mesurés dans les deux thèmes
- Le vert, l'ambre et le gris « neutre » du thème clair sont légèrement assombris pour que tous les textes de couleur atteignent le contraste 4,5:1 (norme WCAG AA, W3C SC 1.4.3), sur le fond, la carte et leurs fonds doux. Le thème sombre était déjà conforme (5,3 au minimum). Un test vérifie désormais les deux thèmes à chaque modification. Aucune information changée. Décision D-20261112-2.

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
