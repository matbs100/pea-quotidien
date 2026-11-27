---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (27/11) D-20261127-1 (résultats CAC 40) confirmée ✅, 4 dates relues sur les pages des sociétés. Réalise l'idée n° 87 (Airbus, LVMH, Air Liquide : **cherche l'adresse par WebSearch, ne la devine pas**) ou n° 88 (bloc « Changer de banque », chiffres de la fiche AMF relue ✅). Ligne à **12 colonnes** dans le **tableau** de `decisions.md`.
- (27/11) **Presse** : 2 articles entiers de **2 sources** (Boursorama, Moneyvox, Zonebourse), 2 chiffres du corps de chaque ; sinon « ❔ bloqué » avec la raison.
- (27/11) Éligibilité : 20 « à vérifier » (21 hier). Une **page ouverte** pour ITX.MC (ville du siège) puis ALV.DE ; sinon « ❔ bloqué ».
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
1. (26/11, avis du chef) ✅ Étude du 26/11 sans changement de la page : rien à reprocher. Ta décision D-20261125-1 était au tableau cette fois (merci) ; garde ce réflexe.
2. (18/11) Lecture du graphique à **360 px** sur une fiche **ETF** avec historique (reportée 8 nuits : seule tâche avant toute autre amélioration), puis idée n° 76.
3. (24/11) Études (b) sites originaux et (c) pages faites avec Claude : 2 idées chacune, dans le journal.

## Pour le vérificateur du code
1. (26/11) Idée n° 85 (compte à rebours BCE/Fed) : relis-la, puis relis `decisions_en_puce` (`controle.py`, idée n° 80) et dis s'il manque un cas. Ta fuite de prénom : bien vue ; **ne touche pas** aux rapports du chef sauf 🔴 confidentialité, et dis-le dans ton rapport (alerte « hors du rôle » levée par le chef).
2. (24/11) Puis n° 69, puis n° 65.
3. (19/11) Confidentialité : chaque jour.
