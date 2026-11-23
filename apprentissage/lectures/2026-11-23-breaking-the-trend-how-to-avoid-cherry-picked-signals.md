---
type: lecture
titre: "Breaking the Trend: How to Avoid Cherry-Picked Signals"
organisme: "arXiv (Valeyre)"
url: https://arxiv.org/pdf/2504.10914v11
publie_le: 2025-12-31
lu_le: 2026-11-23
lu_par: nuit
statut: ✅ relue le 2026-11-23
---
# 📄 Breaking the Trend: How to Avoid Cherry-Picked Signals

[Lire le PDF](https://arxiv.org/pdf/2504.10914v11) · arXiv (Valeyre) · publié le 2025-12-31 · lu le 2026-11-23 par l'agent de nuit

## Résumé
L'auteur (un gérant parisien) part d'un risque connu des stratégies de tendance : à force de tester des réglages sur le même passé, on finit par retenir celui qui a eu de la chance. Il compare le ratio de Sharpe mesuré sur des données réelles à celui que donne une formule théorique, selon la vitesse de la moyenne mobile choisie. L'ajustement est très bon, ce qui le conduit à penser qu'une seule moyenne mobile exponentielle suffit à capter la tendance à l'échelle des fonds de gestion de tendance (les CTA). Un panier d'indicateurs compliqués n'apporte pas de gain visible et ajoute le risque de choisir ses signaux après coup. Il rappelle aussi que la plupart de ces règles sont « ad hoc », sans justification théorique de leur optimalité. Limites : l'étude porte sur des contrats à terme de fonds de tendance, pas sur des ETF d'un épargnant ; un bon ajustement à la théorie ne promet pas un gain futur ; le document est une version de travail (v11) qui n'a pas été relue par un chef.

## Chiffres et faits clés
- L'auteur conclut qu'une seule moyenne mobile exponentielle semble optimale pour capter la tendance (résumé, p. 1).
- Optimiser les réglages sur le passé qui sert aussi à évaluer expose au sur-ajustement (p. 2).
- Les règles de tendance usuelles sont presque toutes « ad hoc » et sans justification théorique de leur optimalité (p. 5).

## Ce que Matin PEA peut en tirer
- Confirme la règle de la fiche : ne pas régler les signaux pour coller au passé. Idée n° 76 (afficher la période et le nombre de paramètres derrière chaque signal) dans `idees.md`.

## Vérification du chef
- ✅ 2026-11-23 : PDF ouvert (arxiv.org, 834 Ko) ; le texte dit bien qu'une seule moyenne mobile exponentielle semble optimale, que l'optimisation sur le même passé expose au sur-ajustement et que les règles usuelles sont « ad hoc » ; résumé en mots propres, aucune copie. arxiv.org est dans `pilotage/sources-verifiees.md`. Réserve : version de travail, contrats à terme de fonds de tendance, pas des ETF.
