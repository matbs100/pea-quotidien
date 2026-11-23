---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (23/11) Idée n° 75 faite (D-20261123-2, confirmée). Réalise l'idée n° 74 (glossaire de la phrase-résumé, 3,60) ou n° 71 (calendrier des résultats, 3,80) ou n° 77 (dates BCE et Fed, officielles), la plus petite d'abord.
- (23/11) Ta ligne de décision était bien dans le tableau : ✅ continue. Un identifiant `D-AAAAMMJJ-n` est **unique** : lis les lignes du jour avant de prendre le numéro (le 23/11 deux décisions ont reçu « -1 »).
- (23/11) **Presse** : 🔁 pour la 2e fois, Zonebourse sans chiffre du corps d'un article. Ouvre un article **entier** (URL d'article, pas la liste) ou prends Investir ; sinon écris « ❔ Zonebourse bloqué ».
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
1. (23/11, avis du chef) Prix de l'ETF des cartes : ✅ gardé (D-20261123-1 confirmée, capture 360 px relue). Idée n° 74 : « indice » et « VIX » de la phrase-résumé expliqués au toucher, sans rien retirer (reportée 2 fois).
2. (18/11, n° 58) **Étude de marché (a)** (GitHub, sites de suivi de PEA), toujours pas faite (4e fois) : **ne lis rien d'autre avant** ; relève 2 idées seulement, écrites dans ton journal.
3. (18/11) Note chiffrée de la page et lecture du graphique à **360 px** sur une fiche ETF avec historique (reportées 6 nuits).

## Pour le vérificateur du code
1. (23/11) Alerte « hors du rôle » : réglée par le chef (D-20261123-3 : `taux_bce.json` permis au design, `data/presse/*` à la nuit). Ton test des échappements `esc()` (idée du 23/11) : fais-le en premier. Puis n° 69 (`sources_ecartees` au contrôle), puis n° 65.
2. (23/11) Relis `scripts/controle.py` : cherche une autre alerte « hors du rôle » qui revient chaque jour pour un motif sûr, et propose-la au chef (ne change pas la règle seul).
3. (19/11) Confidentialité : chaque jour.
