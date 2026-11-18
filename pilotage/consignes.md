---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (18/11) **Idée n° 55** (efficacité du signal de tendance après frais) : trouve d'abord la **source primaire** (étude Zakamulin ou arXiv, PDF avec texte) et fais-en la fiche de lecture ; n'écris la phrase sur la fiche qu'avec elle. Ligne dans le tableau de `decisions.md`.
- (18/11) **Presse** : 2 chiffres attribués d'une source entière autre que Boursorama (MoneyVox : lire un article, pas la liste ; sinon WebSearch `site:`).
- (18/11) Idée n° 54 (source de l'inflation) est faite dans `taux.py` : ne la refais pas ; D-20261118-3 (`paris.py`) est fait par le chef.
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
- (16/11, propriétaire) La tâche « effet verre dépoli » est faite (D-20261117-1) ; le défilement iPhone est corrigé côté Chromium (D-20261118-1), case ouverte jusqu'au retour du propriétaire : n'y touche plus.
1. (18/11) **Étude de marché (a)** (GitHub, sites de suivi de PEA ou de bourse), jamais faite : relève 2 idées concrètes pour rendre une fiche plus claire, sans rien retirer.
2. (18/11) Note chiffrée de la page et lecture du graphique à **360 px** sur une fiche ETF avec historique (reportées 3 nuits).
3. (13/11) Décision dans le **tableau** de `decisions.md`, identifiant tel quel (D-20261118-1) ; regarde les captures avant de pousser.

## Pour le vérificateur du code
1. (18/11) Le test `date.today()` est fait (D-20261118-3) : vérifie qu'aucune autre date « du jour » sans fuseau ne traîne (`datetime.now()` nu, `time.localtime`).
2. (13/11) Un test node du seuil de glissement (120 px, geste rapide) de `modele.html` serait-il simple ?
3. (18/11) Relire `scripts/paris.py` et la dépendance `pypdf` (à justifier dans un journal). Confidentialité : chaque jour.
