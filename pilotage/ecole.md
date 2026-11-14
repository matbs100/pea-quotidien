---
tags: [pea, agent, pilotage, ecole]
---
# 🎓 L'école des agents

Tenu par le chef d'orchestre (étape 8 bis de `CHEF.md`). Chaque matin, il corrige les devoirs de la
veille (✅ réussi, 🔁 à refaire, ❌ abandonné) et donne ceux du jour. L'agent de nuit les fait (étape
2 bis de `AMELIORATION.md`) et rend compte dans la partie `## Devoirs du chef` de son journal.

## Devoirs donnés le 2026-11-14 (pour la nuit du 15 novembre)
1. **Presse (nuit, petit).** Découpé : seulement 3 sources, une par nuit à ouvrir **entières** (Zonebourse, Moneyvox, puis une troisième trouvée par WebSearch `site:`), chacune avec un chiffre attribué. Écris les sources bloquées.
2. **Nouveaux fonds (nuit, petit).** Ne cherche plus par émetteur : prends les ETF **déjà écartés** par la tâche du samedi (`pilotage/univers/2026-11-14.md`, `pea_bourso: False`) et lis sur le site de l'émetteur si « éligible PEA » est écrit ; une ligne par fonds dans `candidats.md`.
3. **Lire (nuit).** Une fiche de lecture sur la page « Plan d'épargne en actions » de la Banque de France ou de l'Euronext (PDF), pages citées. Ajoute les cas d'exception au retrait avant 5 ans seulement si la source officielle les confirme (idée 44).
4. **Réviser (chef).** Ouverture des ETF à 9 h 04 (Euronext) : reporté deux fois, à faire d'abord demain.

## Résultats du 2026-11-14 (devoirs du 2026-11-13)
- 1 Nouveaux fonds : 🔁 aucune piste confirmée en 15 minutes (CEU : code Boursorama = action canadienne) ; la tâche du samedi a, elle, ajouté MFE, S6EW, ITP, CLARI (S6EW confirmé via Boursorama). Redonné autrement.
- 2 Presse : 🔁 deuxième fois de suite 2 sources sur 5 : découpé en plus petit (devoir 1).
- 3 Lire : ✅ fiche AMF relue, chiffres exacts à la page 1.
- 4 Euronext 9 h 04 (chef) : 🔁 reporté une deuxième fois (temps pris par le garde-fou de design).

## Archive : Devoirs donnés le 2026-11-13 (pour la nuit du 14 novembre)
1. **Nouveaux fonds (nuit, petit).** 1 ETF d'un émetteur absent de `univers.json` (pas Invesco, pas MWRD, pas Ossiam déjà noté) : ISIN lu, « éligible PEA » lu, ticker Paris ; note-le dans `candidats.md`. Si rien en 15 minutes, écris pourquoi.
2. **Presse (nuit).** 5 sources dans `data/presse/` ; si un site est bloqué, WebSearch `site:` puis « bloqué ». Estimations attribuées. Ne répète pas une rumeur de page d'accueil (ex. PDG de Nvidia) sans seconde source.
3. **Lire (nuit).** La lecture proposée : page « Plan d'épargne en actions » de l'AMF ou de la Banque de France en PDF, fiche de lecture avec pages.
4. **Réviser (chef).** Ouverture des ETF à 9 h 04 : relire la ligne du classeur Euronext (fait seulement en partie).

## Résultats du 2026-11-13 (devoirs du 2026-11-12)
- 1 Nouveaux fonds : 🔁 Ossiam S6EW : ticker « S6EW FP » vu (extrait), éligibilité PEA toujours sur une seule source ; autre émetteur non fait. Redonné en plus petit.
- 2 Comprendre l'utilisateur : ✅ initiales des mois ambiguës ; réalisé par le chef (D-20261113-2, mois en 3 lettres).
- 3 Presse : 🔁 2 sources sur 5 (Les Echos, BFM, MarketWatch bloqués) ; refait avec WebSearch.
- 4 Euronext 9 h 04 (chef) : 🔁 non refait ce matin (temps pris par la vérification de la fiscalité, ✅ relue sur service-public).

## Archive : Devoirs donnés le 2026-11-12
(voir le rapport du 13/11)

## Archive : Devoirs donnés le 2026-11-11 (pour la nuit du 12 novembre)
1. **Nouveaux fonds (nuit).** 3 ETF ou actions éligibles au PEA d'un émetteur **absent** de `univers.json` (vérifie la liste
   d'abord) : ISIN lu sur une page ouverte (Boursorama ou fiche de l'émetteur), mention « éligible PEA » lue, ticker Paris.
   Note-les dans `pilotage/candidats.md`. Ne reviens plus sur MWRD (voir ci-dessous).
2. **Comprendre l'utilisateur (nuit).** Relis la carte « Mois par mois » comme un débutant : une phrase d'explication ou un
   libellé à changer ? Écris la proposition (sans la réaliser) dans le journal.
3. **Réviser (chef).** Heure d'ouverture d'Euronext Paris : ouvrir le document « Cash markets trading hours » lié par la page officielle.

## Résultats du 2026-11-11 (devoirs du 2026-11-10)
- 1 MWRD : ❌ abandonné : page Boursorama sans mention PEA, extraits de recherche : assurance vie et PER ; fonds irlandais, probablement non éligible. Deux nuits passées dessus : on passe à d'autres fonds.
- 2 Lire : ✅ fiche arXiv relue (chiffres p. 1, 4, 15, 34 exacts) ; la fiche MSCI du 10/11 relue aussi (p. 13 et 24 exacts).
- 3 Horaires (chef) : ✅ 17 h 30 et 17 h 35 (avis officiels d'Euronext, extraits) ; 🔁 ouverture à 9 h confirmée seulement par une FAQ de 2017.

## Archive : Devoirs donnés le 2026-11-10 (pour la nuit du 11 novembre)
1. **Nouveaux fonds (nuit).** MWRD : lire sur Boursorama (ou une fiche amundietf.fr trouvée par WebSearch) la mention « éligible PEA » ; sinon noter « non lue » et passer à CEU.
2. **Lire (nuit).** Un PDF d'une source vérifiée : méthodologie de l'indice MSCI World ou publication de l'AMF sur l'épargne ; fiche de lecture avec pages.
3. **Réviser (chef).** Horaires de séance d'Euronext Paris : ouvrir le document « Cash markets trading hours » lié par la page officielle.

## Archive : Résultats du 2026-11-10 (devoirs du 2026-11-09)
- 1 Nouveaux fonds : ✅ MWRD, ISIN IE000BI8OT95 lu sur Finect ; éligibilité PEA non lue (devoir suivant).
- 2 Nouvelles données : 🔁 en partie : robots.txt noté, frais et encours trouvés sur Finect, pas d'adresse amundietf.fr ; abandonné au profit de Finect.
- 3 Réviser Euronext (chef) : ✅ jours de fermeture 2026 confirmés (page officielle) ; 🔁 horaires de séance (document séparé).
