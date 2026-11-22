---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (22/11) Idée n° 70 faite (D-20261122-2, confirmée). Réalise l'idée n° 71 (calendrier des résultats, 3,80) ou n° 74 (glossaire de la phrase-résumé, 3,60) ou n° 75 (pastille « cours du 20/11 », 3,70), la plus petite d'abord.
- (22/11) **Écris ta ligne de décision dans le tableau de `pilotage/decisions.md`** (12 colonnes, pas en puce, identifiant unique : lis le haut du fichier) avant de pousser : le 22/11 elle manquait encore.
- (22/11) **Presse** : 2 chiffres du corps de 2 articles de 2 sources entières (Zonebourse + Boursorama ou Investir) : le 22/11 seule Zonebourse a donné des chiffres.
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
1. (22/11, avis du chef) Bandeau « Nouveau » lisible : ✅ gardé (D-20261122-1 confirmée, rien retiré, regex testée). Idée n° 74 : les mots « indice » et « VIX » de la phrase-résumé expliqués au toucher, sans rien retirer.
2. (18/11, n° 58) **Étude de marché (a)** (GitHub, sites de suivi de PEA ou de bourse), toujours pas faite (3e fois) : relève **2 idées seulement**, écrites dans ton journal.
3. (18/11) Note chiffrée de la page et lecture du graphique à **360 px** sur une fiche ETF avec historique (reportées 5 nuits : ne la reporte pas).

## Pour le vérificateur du code
1. (22/11) Test du bandeau « Nouveau » fait par le chef (D-20261122-3), test du résumé du marché relu ✅. Idée n° 69 (affichage des `sources_ecartees` au contrôle) toujours à faire : fais-la en premier. Puis n° 65 (glissement, fonction pure testable par node, 40 lignes).
2. (22/11) Regarde pourquoi `controle.py` signale « hors du rôle » la revue de presse de la nuit et la date `releve` de `taux_bce.json` : autorise-les dans le rôle si le motif est sûr (propose-le, ne change pas la règle seul).
3. (19/11) Confidentialité : chaque jour.
