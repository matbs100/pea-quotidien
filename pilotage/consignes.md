---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (16/11) D-20261116-2 (titre comparé mémorisé) confirmée. Réalise l'idée n° 46 (inflation de la zone euro dans le bloc « contexte des taux », source BCE p. 3-4 déjà relue) ; **une ligne dans le tableau** de `decisions.md`.
- (16/11) **Presse d'abord** : une source entière autre que Boursorama (WebSearch `site:` si bloquée), 2 chiffres attribués ; écris dans le journal que le fichier est demandé par le chef.
- (13/11) Fais les devoirs de `pilotage/ecole.md` (le fonds de la nuit : un seul, MWRD, CEM ou EQQQ).
- (06/11) Chaque amélioration suit `pilotage/decision.md` (identifiant `[D-…]` dans le commit) ; une nouveauté de CHANGELOG va **sous l'en-tête** du fichier.
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus.
- (06/11) Si un cours est daté d'un autre jour, dis-le dans « À garder en tête ».
- (06/11) À la clôture, une idée au plus (étape 5 ter), notée avec la grille de `pilotage/decision.md`.
- (07/11) Ne modifie pas `scripts/collecte.py` (hors du rôle de la fiche) sauf correctif urgent expliqué dans le commit.

## Chantier interface
1. (14/11) Bloc fiscalité du PEA fait (D-20261113-3) ; contrastes des deux thèmes faits (13/11).
2. Sur téléphone : reste les lignes de tableau (`.ligne .c`, 13 px) et les étiquettes de 10-12 px, à tester à 360 px.
3. (13/11) « Mois par mois » en 3 lettres fait (D-20261113-2). Bilans : D-20261106-6 (à mesurer avec une capture 360 px, reporté le 14/11) ; D-20261106-7 : 2 parties faites, bilan le 19/11 ; glisser pour fermer (D-20261113-1) le 17/11.
4. (06/11) Bouton clair / sombre (n° 14) et graphique au clavier (n° 15) : rejetés (gain < 3).

## Interdits temporaires
- Aucun.

## Pour l'agent design
0. (16/11) Unité du graphique ✅ (D-20261116-1). Reste : le regarder à **360 px** (pas 390) et sur une fiche ETF qui a un historique ; étude de marché (a) toujours non faite.
1. (13/11) Fais la note de la page et une étude de marché (a : GitHub, sites de suivi de PEA ou de bourse) : relève 2 idées concrètes pour rendre une fiche plus claire, sans rien retirer.
2. (16/11) Note ta décision dans le **tableau** de `decisions.md`, pas en puces. (13/11) Regarde les captures avant/après avant de pousser (`design.py rendre`) et écris l'identifiant de décision tel quel (D-20261113-1), jamais « sans tirets ».

## Pour le vérificateur du code
1. (13/11) Relire `scripts/modele.html` (glisser pour fermer, bloc `blocMois`) : un test node du seuil de glissement (120 px, geste rapide) serait-il simple ?
2. (13/11) Vérifier que les entrées de `CHANGELOG.md` sont toujours sous l'en-tête (le design l'avait collée au-dessus) : proposer un test.
3. (10/11) Reste : `zip(..., strict=)` (B905) seulement si le comportement est testé. Confidentialité : chaque jour.
