---
tags: [pea, agent, pilotage, decision]
---
# 🗳️ Journal des décisions

Une ligne par décision, prise avec la [[decision|méthode de décision]]. Tenu par le chef d'orchestre ;
l'agent de nuit y ajoute ses décisions provisoires. Le relais du Mac recopie les nouvelles décisions dans
la note « Agent PEA Quotidien » et dans la mémoire de Claude.

- **Décision** : `adoptée`, `à l'essai`, `provisoire (nuit)`, `correction`, `en attente`, `rejetée`, `annulée`.
- **Réalisée** : date du commit qui la réalise (vide tant qu'elle ne l'est pas).
- **Bilan** : trois jours de bourse après la réalisation : ✅ gardée, 🔧 à ajuster, ↩️ annulée, avec ce que
  l'indicateur a montré.
- Le premier lot (6 novembre) a été noté par Claude à la demande de Mathieu : le chef le relit à son
  passage du 7 novembre.

| ID | Date | Idée | Par | Gain | Coût | Risque | Priorité | Décision | Réalisée | Indicateur | Bilan |
|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| D-20261106-1 | 2026-11-06 | n° 22 · Fonds Wealins dans « Mes investissements » | Mathieu | 4,45 | 3 | 1 | 4,9 | adoptée | 2026-11-06 | ≥ 1 000 fonds trouvables ; liste relue chaque jour ; aucune erreur de fonds au contrôle | |
| D-20261106-2 | 2026-11-06 | n° 23 · Devise à côté de chaque prix (page et note) | Mathieu | 3,70 | 1 | 1 | 5,4 | adoptée | 2026-11-06 | toute ligne de prix d'un placement montre sa devise (test) | |
| D-20261106-3 | 2026-11-06 | Méthode de décision et journal des décisions | Mathieu | — | — | — | — | adoptée | 2026-11-06 | chaque amélioration cite une décision ; aucun bilan en retard (contrôle) | |
| D-20261106-4 | 2026-11-06 | n° 3 · Simulateur « 50 € par mois depuis 5 ans » | Claude (pour le chef) | 4,45 | 3 | 1 | 4,9 | adoptée | 2026-11-07 | calcul juste sur 3 cas testés ; avertissement visible ; aucune formulation de conseil | |
| D-20261106-5 | 2026-11-06 | n° 21 · Page « Mes critères » | Claude (pour le chef) | 4,20 | 3 | 2 | 3,4 | adoptée | | critères gardés sur le téléphone ; liste filtrée juste (test) ; aucune formulation de conseil | |
| D-20261106-6 | 2026-11-06 | n° 2 · Rendements mois par mois en carte de chaleur | Claude (pour le chef) | 3,55 | 3 | 1 | 3,1 | adoptée | | carte lisible à 360 px ; page < +5 % | |
| D-20261106-7 | 2026-11-06 | n° 7 · Comparer deux titres (base 100) | Claude (pour le chef) | 3,85 | 3 | 2 | 2,7 | adoptée | | comparaison en 2 touchers ; aucune régression du graphique | |
| D-20261106-8 | 2026-11-06 | n° 1 · Ratios de Sharpe et de Sortino | Claude (pour le chef) | 3,35 | 2 | 1 | 3,7 | à l'essai | | ratios affichés avec une définition au toucher | |
| D-20261106-9 | 2026-11-06 | n° 8 · Fiche installable (manifeste et icône, sans service worker) | Claude (pour le chef) | 3,20 | 2 | 1 | 3,4 | à l'essai | | icône et nom corrects sur l'écran d'accueil ; fiche toujours à jour | |
| D-20261106-10 | 2026-11-06 | n° 6 · Diversification du top 30 (version réduite) | Claude (pour le chef) | 3,45 | 3 | 2 | 1,9 | à l'essai | | indicateur affiché chaque jour ; calcul testé | |
| D-20261106-11 | 2026-11-06 | n° 10 · Deuxième source d'éligibilité PEA des ETF | Claude (pour le chef) | 3,25 | 3 | 2 | 1,5 | à l'essai | | 2 sources concordantes pour ≥ 80 % des ETF | |
| D-20261106-12 | 2026-11-06 | n° 20 · Mention TTF d'après la liste BOFiP | Claude (pour le chef) | 3,25 | 3 | 2 | 1,5 | à l'essai | | mention juste pour 100 % de la liste officielle vérifiée | |
| D-20261106-13 | 2026-11-06 | Lectures des agents : PDF de sources vérifiées, fiches de lecture dans Obsidian | Mathieu | — | — | — | — | adoptée | 2026-11-06 | au moins une fiche de lecture tous les 3 jours, relue par le chef ; aucune alerte « Lectures » au contrôle | |
| D-20261107-1 | 2026-11-07 | n° 25 · Avertissement des ETF à effet de levier aligné sur l'AMF (texte vérifié p. 5 du guide) | Claude (chef) | 3,15 | 1 | 1 | — | correction | 2026-11-07 | texte conforme à la source ; test du rendu | |
| D-20261107-2 | 2026-11-07 | n° 24 · Recoupement entre mes ETF (diversification seulement apparente) | Claude (chef) | 3,45 | 3 | 2 | 1,5 | à l'essai | | message pour les paires d'indices connues, aucune fausse alerte | |
| D-20261107-3 | 2026-11-07 | n° 27 · Lien Yahoo en 404 depuis le cloud : orange et non rouge au contrôle | Claude (chef) | 2,80 | 2 | 1 | — | rejetée | | gain < 3 ; à revoir si Mathieu confirme que les liens Yahoo marchent | |
