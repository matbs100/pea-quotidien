---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (11/11) Réaliser **D-20261106-7** (comparer deux titres, base 100), une première partie suffit ; sinon vérifier D-20261106-8 (Sharpe/Sortino) dans la fiche du jour.
- (11/11) Fais les devoirs de `pilotage/ecole.md` (3 nouveaux fonds d'un émetteur absent ; ne reviens plus sur MWRD, voir `methodes.md`).
- (06/11) Chaque amélioration suit `pilotage/decision.md` (grille, identifiant `[D-…]` dans le commit).
- (06/11) Ouvre au moins 3 sources par nuit, avec liens ; connaissances nouvelles en « ⏳ à vérifier ».
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.
- (11/11) `data/presse/` : 2 jours seulement ; vise 5 sources par jour de bourse, estimations attribuées.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus.
- (06/11) Si un cours est daté d'un autre jour, dis-le dans « À garder en tête ».
- (06/11) À la clôture, une idée au plus (étape 5 ter), notée avec la grille de `pilotage/decision.md`.
- (07/11) Ne modifie pas `scripts/collecte.py` (hors du rôle de la fiche) sauf correctif urgent expliqué dans le commit.

## Chantier interface
1. Sur téléphone : textes des notes et fiches passés à 14 px le 08/11 ; reste les lignes de tableau (`.ligne .c`, 13 px) et les étiquettes de 10-12 px, à tester à 360 px.
2. (11/11) Devise à côté des prix : bilan ✅. « Mois par mois » (D-20261106-6) : bilan le 14/11.
3. (06/11) Bouton clair / sombre (n° 14) et graphique au clavier (n° 15) : rejetés (gain < 3).

## Interdits temporaires
- Aucun.

## Pour le vérificateur du code
1. (11/11) Revoir `scripts/controle.py` : les 404 Yahoo (PLEM, CD8, PINR, TRV, INS, ALNOV) viennent-ils du cloud ou de symboles faux ? Teste un symbole depuis `collecte.py`, sans changer les données.
2. (11/11) Vérifier le ⏳ CSP (MDN) avec une seconde source fiable (OWASP).
3. (10/11) Reste : `zip(..., strict=)` (B905) seulement si le comportement est testé.
