---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (09/11) D-20261106-8 (Sharpe/Sortino) : vérifie que les valeurs apparaissent dans la prochaine fiche.
- (09/11) Réaliser **D-20261109-2** (« Mes critères » : titres écartés faute de donnée), petit.
- (09/11) Puis **D-20261106-6** (carte de chaleur des rendements par mois), une première partie suffit ; sinon **D-20261106-7** (comparer deux titres).
- (08/11) Fais les devoirs de `pilotage/ecole.md` (un seul fonds, ISIN lu sur une page ouverte ; voir `methodes.md`).
- (06/11) Chaque amélioration suit `pilotage/decision.md` (grille, identifiant `[D-…]` dans le commit).
- (06/11) Ouvre au moins 3 sources par nuit, avec liens ; connaissances nouvelles en « ⏳ à vérifier ».
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus.
- (06/11) Si un cours est daté d'un autre jour, dis-le dans « À garder en tête ».
- (06/11) À la clôture, une idée au plus (étape 5 ter), notée avec la grille de `pilotage/decision.md`.
- (07/11) Ne modifie pas `scripts/collecte.py` (hors du rôle de la fiche) sauf correctif urgent expliqué dans le commit.

## Chantier interface
1. Sur téléphone : textes des notes et fiches passés à 14 px le 08/11 ; reste les lignes de tableau (`.ligne .c`, 13 px) et les étiquettes de 10-12 px, à tester à 360 px.
2. (07/11) Bilan de la devise à côté des prix (D-20261106-2) le 11/11.
3. (06/11) Bouton clair / sombre (n° 14) et graphique au clavier (n° 15) : rejetés (gain < 3).

## Interdits temporaires
- Aucun.

## Pour le vérificateur du code
1. (10/11, demande du propriétaire) Premier passage : contrôle complet de confidentialité (`--site --commits 0`), dépôt, commits et site ; aucune information personnelle nulle part. Un ancien commit touché se signale au propriétaire, sans réécrire l'historique.
2. (10/11) Revoir `scripts/confidentialite.py` (faux positifs, catégories manquantes) et les ajouts du 09/11 (frais, devises, OPCVM, sécurité de la page).
3. (10/11) Première veille : versions et failles de yfinance, pandas, requests, pypdf (`pip-audit`), et une technique de l'OWASP sur la politique de sécurité des pages (CSP).
