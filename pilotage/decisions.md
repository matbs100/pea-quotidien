---
tags: [pea, agent, pilotage, decision]
---
# 🗳️ Journal des décisions

Une ligne par décision, prise avec la [[decision|méthode de décision]]. Tenu par le chef d'orchestre ;
l'agent de nuit y ajoute ses décisions provisoires. Le chef les résume dans `pilotage/obsidian-decisions.md`
(`scripts/obsidian.py`), que la note « Agent PEA Quotidien » d'Obsidian intègre.

- **Décision** : `adoptée`, `à l'essai`, `provisoire (nuit)`, `correction`, `en attente`, `rejetée`, `annulée`.
- **Réalisée** : date du commit qui la réalise (vide tant qu'elle ne l'est pas).
- **Bilan** : trois jours de bourse après la réalisation : ✅ gardée, 🔧 à ajuster, ↩️ annulée, avec ce que
  l'indicateur a montré.
- Le premier lot (6 novembre) a été noté par Claude à la demande du propriétaire : le chef le relit à son
  passage du 7 novembre.

| ID | Date | Idée | Par | Gain | Coût | Risque | Priorité | Décision | Réalisée | Indicateur | Bilan |
|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| D-20261106-1 | 2026-11-06 | n° 22 · Fonds Wealins dans « Mes investissements » | Propriétaire | 4,45 | 3 | 1 | 4,9 | adoptée | 2026-11-06 | ≥ 1 000 fonds trouvables ; liste relue chaque jour ; aucune erreur de fonds au contrôle | ✅ gardée (12/11) : 1 344 fonds dans `data/wealins.json`, tests verts, aucune erreur de fonds au contrôle |
| D-20261106-2 | 2026-11-06 | n° 23 · Devise à côté de chaque prix (page et note) | Propriétaire | 3,70 | 1 | 1 | 5,4 | adoptée | 2026-11-06 | toute ligne de prix d'un placement montre sa devise (test) | ✅ gardée le 2026-11-11 : `devise_de` testée, devises présentes dans la fiche du 10/11 |
| D-20261106-3 | 2026-11-06 | Méthode de décision et journal des décisions | Propriétaire | — | — | — | — | adoptée | 2026-11-06 | chaque amélioration cite une décision ; aucun bilan en retard (contrôle) | ✅ gardée (12/11) : chaque amélioration récente cite sa décision ; le contrôle liste les bilans en retard (ce passage les a tous écrits) |
| D-20261106-4 | 2026-11-06 | n° 3 · Simulateur « 50 € par mois depuis 5 ans » | Claude (pour le chef) | 4,45 | 3 | 1 | 4,9 | adoptée | 2026-11-07 | calcul juste sur 3 cas testés ; avertissement visible ; aucune formulation de conseil | ✅ gardée (12/11) : tests verts depuis le 07/11, avertissement présent ; aucune alerte de conseil au contrôle |
| D-20261106-5 | 2026-11-06 | n° 21 · Page « Mes critères » | Claude (pour le chef) | 4,20 | 3 | 2 | 3,4 | adoptée | 2026-11-09 (1re partie : filtre du Top 30, D-20261109-1) | critères gardés sur le téléphone ; liste filtrée juste (test) ; aucune formulation de conseil | |
| D-20261106-6 | 2026-11-06 | n° 2 · Rendements mois par mois en carte de chaleur | Claude (pour le chef) | 3,55 | 3 | 1 | 3,1 | adoptée | 2026-11-11 (fiche d'un titre) | carte lisible à 360 px ; page < +5 % | |
| D-20261106-7 | 2026-11-06 | n° 7 · Comparer deux titres (base 100) | Claude (pour le chef) | 3,85 | 3 | 2 | 2,7 | adoptée | 2026-11-12 (1re partie : comparaison dans le graphique de la fiche) | comparaison en 2 touchers ; aucune régression du graphique | |
| D-20261106-8 | 2026-11-06 | n° 1 · Ratios de Sharpe et de Sortino | Claude (pour le chef) | 3,35 | 2 | 1 | 3,7 | à l'essai | 2026-11-08 | ratios affichés avec une définition au toucher | ✅ gardée (12/11) : tests verts, ratios présents dans la page (`sharpe`) ; reste à l'essai tant que la définition au toucher n'est pas relue sur téléphone |
| D-20261106-9 | 2026-11-06 | n° 8 · Fiche installable (manifeste et icône, sans service worker) | Claude (pour le chef) | 3,20 | 2 | 1 | 3,4 | à l'essai | | icône et nom corrects sur l'écran d'accueil ; fiche toujours à jour | |
| D-20261106-10 | 2026-11-06 | n° 6 · Diversification du top 30 (version réduite) | Claude (pour le chef) | 3,45 | 3 | 2 | 1,9 | à l'essai | | indicateur affiché chaque jour ; calcul testé | |
| D-20261106-11 | 2026-11-06 | n° 10 · Deuxième source d'éligibilité PEA des ETF | Claude (pour le chef) | 3,25 | 3 | 2 | 1,5 | à l'essai | | 2 sources concordantes pour ≥ 80 % des ETF | |
| D-20261106-12 | 2026-11-06 | n° 20 · Mention TTF d'après la liste BOFiP | Claude (pour le chef) | 3,25 | 3 | 2 | 1,5 | à l'essai | | mention juste pour 100 % de la liste officielle vérifiée | |
| D-20261106-13 | 2026-11-06 | Lectures des agents : PDF de sources vérifiées, fiches de lecture dans Obsidian | Propriétaire | — | — | — | — | adoptée | 2026-11-06 | au moins une fiche de lecture tous les 3 jours, relue par le chef ; aucune alerte « Lectures » au contrôle | ✅ gardée (12/11) : 7 fiches de lecture en 6 jours, 0 à relire par le chef, aucune alerte « Lectures » |
| D-20261107-1 | 2026-11-07 | n° 25 · Avertissement des ETF à effet de levier aligné sur l'AMF (texte vérifié p. 5 du guide) | Claude (chef) | 3,15 | 1 | 1 | — | correction | 2026-11-07 | texte conforme à la source ; test du rendu | ✅ gardée (12/11) : texte AMF inchangé, tests verts |
| D-20261107-2 | 2026-11-07 | n° 24 · Recoupement entre mes ETF (diversification seulement apparente) | Claude (chef) | 3,45 | 3 | 2 | 1,5 | à l'essai | | message pour les paires d'indices connues, aucune fausse alerte | |
| D-20261107-3 | 2026-11-07 | n° 27 · Lien Yahoo en 404 depuis le cloud : orange et non rouge au contrôle | Claude (chef) | 2,80 | 2 | 1 | — | rejetée | | gain < 3 ; à revoir si le propriétaire confirme que les liens Yahoo marchent | |
| D-20261108-1 | 2026-11-08 | Chantier interface : textes des notes, astuces, liens et libellés de fiche portés à 14 px (étiquettes de 11 à 12 px) | Claude (chef) | 3,00 | 1 | 1 | — | correction | 2026-11-08 | texte courant ≥ 14 px sur téléphone ; tests verts ; page sans débordement | ✅ gardée (12/11) : tests verts, aucune régression de page signalée depuis 4 jours |
| D-20261108-2 | 2026-11-08 | n° 29 · `lectures.py lire` garde les sauts de page (doublon) | Claude (chef) | — | 2 | 1 | — | rejetée | | doublon : marqueurs « ===== page N ===== » déjà présents (erreur du chef, qui avait coupé sur \f) | |
| D-20261108-3 | 2026-11-08 | n° 28 · Méthode des ratios dans l'aide du Sharpe | Claude (chef) | 2,70 | 1 | 1 | — | rejetée | | gain < 3 ; l'aide dit déjà « sans tenir compte des taux », « passé » ; à revoir si les ratios prêtent à confusion | |
| D-20261109-1 | 2026-11-09 | n° 30 · « Mes critères », première partie : filtre du Top 30 (risque max, baisse max sur 1 an, type) | Claude (nuit) | 3,75 | 2 | 1 | 4,5 | adoptée (confirmée par le chef) | 2026-11-09 | filtre juste (test node) ; critères gardés sur l'appareil ; aucune formulation de conseil | confirmée par le chef le 2026-11-09 (code relu, test node, mention « ni conseil ni recommandation ») ; bilan attendu le 2026-11-12 |
| D-20261109-2 | 2026-11-09 | n° 31 · « Mes critères » : dire combien de titres du Top 30 sont écartés faute de donnée (au lieu de les cacher en silence) | Claude (chef) | 3,20 | 1 | 1 | 4,4 | à l'essai (confirmée par le chef) | 2026-11-10 | message exact dans le bilan du filtre ; test node sur un titre sans donnée | confirmée le 2026-11-10 : code relu (textContent), test node, 28/28 ; bilan attendu le 2026-11-13 |
| D-20261110-1 | 2026-11-10 | n° 32 · Encadré « contexte des taux » (dernier taux BCE : dépôt 2,50 % depuis le 16/09, inchangé le 29/10, lien BCE) | Claude (chef) | 3,40 | 3 | 1 | 1,8 | adoptée | 2026-11-10 | chiffres égaux à la BCE ; aucune formulation de conseil | |
| D-20261110-2 | 2026-11-10 | Nettoyage : import inutile retiré de `scripts/wealins.py` (demande du vérificateur du code) | Claude (chef) | — | 1 | 1 | — | correction | 2026-11-10 | tests 28/28 ; ruff sans F401 | |
| D-20261111-1 | 2026-11-11 | n° 34 · Aide « Qu'est-ce que le MSCI World ? » | Claude (chef) | 2,95 | 1 | 1 | — | rejetée | | gain < 3 |  |
| D-20261111-2 | 2026-11-11 | n° 36 · Mois par mois : moyenne par mois | Claude (chef) | 2,90 | 1 | 1 | — | rejetée | | gain < 3 |  |
| D-20261111-3 | 2026-11-11 | n° 37 et 38 · test du mois manquant, légende de l'échelle de couleur | Claude (chef) | 2,05 / 2,75 | 1 | 1 | — | rejetée | | gain < 3 |  |

| D-20261112-1 | 2026-11-12 | Contrôle : un lien Yahoo en 404 depuis le cloud n'est plus « cassé » si le symbole a des cours collectés (API Yahoo interdite par son robots.txt) | Claude (chef) | 3,10 | 1 | 1 | — | correction | 2026-11-12 | contrôle sans faux rouge pour FOO.PA et CD8.PA ; test | |
| D-20261112-2 | 2026-11-12 | n° 39 · Palette sombre dédiée aux courbes et contraste 4,5:1 des textes secondaires | Claude (chef) | 3,00 | 2 | 1 | 2,0 | adoptée | | contrastes ≥ 4,5:1 en mode sombre (test) ; aucune régression | |
| D-20261112-3 | 2026-11-12 | n° 40 · test contre les gestionnaires en ligne du gabarit | Claude (chef) | 2,00 | 1 | 1 | — | rejetée | | gain < 3 |  |
