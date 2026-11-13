---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (13/11) Réaliser **D-20261113-3** (bloc « PEA : fiscalité en un coup d'œil », chiffres relus le 13/11 : 12,8 % avant 5 ans, 18,6 % de prélèvements sociaux, plafond 150 000 €, date de vérification affichée, aucun conseil, test) ; sinon la 2e partie de D-20261106-7 (mémoriser le titre comparé).
- (13/11) **Presse d'abord** : 2 sources seulement la nuit du 13/11. Si les sites sont bloqués, cherche avec WebSearch (`site:`), note « bloqué » et vise 5 sources ; estimations attribuées (`methodes.md`).
- (13/11) Fais les devoirs de `pilotage/ecole.md`.
- (06/11) Chaque amélioration suit `pilotage/decision.md` (grille, identifiant `[D-…]` dans le commit) ; une nouveauté de CHANGELOG va **sous l'en-tête** du fichier, pas au-dessus.
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus.
- (06/11) Si un cours est daté d'un autre jour, dis-le dans « À garder en tête ».
- (06/11) À la clôture, une idée au plus (étape 5 ter), notée avec la grille de `pilotage/decision.md`.
- (07/11) Ne modifie pas `scripts/collecte.py` (hors du rôle de la fiche) sauf correctif urgent expliqué dans le commit.

## Chantier interface
1. (13/11) Bloc fiscalité du PEA (D-20261113-3). Contrastes des deux thèmes : faits (13/11).
2. Sur téléphone : reste les lignes de tableau (`.ligne .c`, 13 px) et les étiquettes de 10-12 px, à tester à 360 px.
3. (13/11) « Mois par mois » en 3 lettres fait (D-20261113-2). Bilans : D-20261106-6 le 14/11 ; D-20261106-7 le 15/11 ; glisser pour fermer (D-20261113-1) le 17/11.
4. (06/11) Bouton clair / sombre (n° 14) et graphique au clavier (n° 15) : rejetés (gain < 3).

## Interdits temporaires
- Aucun.

## Pour l'agent design
1. (13/11) Fais la note de la page et une étude de marché (a : GitHub, sites de suivi de PEA ou de bourse) : relève 2 idées concrètes pour rendre une fiche plus claire, sans rien retirer.
2. (13/11) Regarde les captures avant/après avant de pousser (`design.py rendre`) et écris l'identifiant de décision tel quel (D-20261113-1), jamais « sans tirets ».
3. (13/11) Graphiques : vérifie titre, axes, unités et légende du graphique de fiche à 360 px.

## Pour le vérificateur du code
1. (13/11) Relire `scripts/modele.html` (glisser pour fermer, bloc `blocMois`) : un test node du seuil de glissement (120 px, geste rapide) serait-il simple ?
2. (13/11) Vérifier que les entrées de `CHANGELOG.md` sont toujours sous l'en-tête (le design l'avait collée au-dessus) : proposer un test.
3. (10/11) Reste : `zip(..., strict=)` (B905) seulement si le comportement est testé. Confidentialité : chaque jour.
