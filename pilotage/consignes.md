---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (24/11) D-20261124-2 (glossaire « indice », « clôture ») confirmée ✅, ligne dans le tableau : continue. Réalise l'idée n° 77 (BCE 16-17/12 lue sur le site officiel ; ajoute la Fed seulement avec sa source) ou n° 71 (calendrier des résultats, 3,80), la plus petite d'abord. Un identifiant `D-AAAAMMJJ-n` est unique : `grep` avant de numéroter.
- (24/11) **Presse** : 🔁 3e fois. Ouvre le corps d'**un article entier** (Boursorama ou Investir, URL d'article) et note 2 chiffres du corps ; VIX 26,62 et Brent 88,87 $ lus sur une page de liste restent ❔ : ne les reprends pas.
- (24/11) Éligibilité : 21 « à vérifier » (23 hier) ; pour 3 titres allemands ou espagnols, cherche la deuxième source ailleurs que sur les sites qui répondent 403 (page investisseurs de l'émetteur via WebSearch).
- (06/11) Chaque amélioration suit `pilotage/decision.md` (identifiant `[D-…]` dans le commit) ; une nouveauté de CHANGELOG va **sous l'en-tête**.
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
- (16/11, propriétaire) Le défilement iPhone est corrigé côté Chromium (D-20261118-1), case ouverte jusqu'au retour du propriétaire : n'y touche plus.
1. (24/11, avis du chef) Pastille « Risque » 24 px : ✅ gardé (D-20261124-1, capture relue). **Ta décision va dans le tableau** de `pilotage/decisions.md` (3e fois en puce : le chef l'a recopiée) : écris la ligne `| D-… |` avant de pousser.
2. (24/11) Étude (a) faite ✅. Passe aux études (b) sites originaux et (c) pages faites avec Claude : 2 idées chacune, dans le journal.
3. (18/11) Lecture du graphique à **360 px** sur une fiche **ETF** avec historique (reportée 7 nuits : à faire avant toute autre amélioration), puis idée n° 76.

## Pour le vérificateur du code
1. (24/11) Ta correction de confidentialité (prénom dans mon rapport du 23/11) : ✅ bien vu, alerte « hors du rôle » vérifiée par le chef (`verifie.json`). Fais maintenant le test des échappements `esc()` (reporté 2 fois), puis n° 69, puis n° 65.
2. (24/11) Idée n° 80 (contrôle des décisions écrites en puce) : relis `scripts/controle.py` et dis si elle est faisable en 30 lignes ; ne change pas la règle seul.
3. (19/11) Confidentialité : chaque jour.
