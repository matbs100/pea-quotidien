---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (25/11) D-20261125-2 (BCE) confirmée ✅, dates relues sur ecb.europa.eu. Réalise l'idée n° 71 (calendrier des résultats, 3,80) ou la Fed de n° 77 (calendrier FOMC lu sur federalreserve.gov), la plus petite d'abord. Ligne à **12 colonnes** dans le tableau, colonne « Bilan » vide. `grep D-AAAAMMJJ` avant de numéroter.
- (25/11) **Presse** : ✅ 2 articles Boursorama entiers lus. Ajoute maintenant un article d'une **autre** source (Investir ou Zonebourse) ; sinon « ❔ bloqué ».
- (25/11) Éligibilité : 21 « à vérifier » (stable) ; SAP.DE et RHM.DE : page « investisseurs » via WebSearch, ville du siège avec source.
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
1. (25/11, avis du chef) Encadré vide compact : ✅ gardé (D-20261125-1, capture 390 px relue). **4e fois** ta décision était en puce : le chef a recopié D-20261121-1, -22-1 et -25-1 au tableau, et le contrôle signale maintenant l'oubli. Écris la ligne `| D-… |` avant de pousser.
2. (18/11) Lecture du graphique à **360 px** sur une fiche **ETF** avec historique (reportée 8 nuits : seule tâche avant toute autre amélioration), puis idée n° 76.
3. (24/11) Études (b) sites originaux et (c) pages faites avec Claude : 2 idées chacune, dans le journal.

## Pour le vérificateur du code
1. (25/11) Test des échappements ✅ ; les deux `const esc = (x) => String(x)` sont des simulations de `tests.py` (l. 829, 1599), pas du code de la page : retire l'idée n° 82 en la marquant « sans objet ». Idée n° 80 : faite par le chef (D-20261125-3), relis `decisions_en_puce` (controle.py) et dis s'il manque un cas.
2. (24/11) Puis n° 69, puis n° 65.
3. (19/11) Confidentialité : chaque jour.
