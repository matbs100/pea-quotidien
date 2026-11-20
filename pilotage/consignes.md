---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (20/11) Idées n° 61 et 64 faites (D-20261120-1, D-20261120-3) : n'y touche plus. **Pas de stock d'idées ≥ 3,5** : propose-en 2 nouvelles, utiles à un débutant, notées avec la grille (tirées de la veille du samedi : fonds, frais, dividendes).
- (20/11) **Presse** : les 4 sources habituelles (la nuit du 20 n'en a lu qu'une) ; 2 chiffres attribués de 2 sources différentes.
- (20/11) Une idée « faite » doit citer l'identifiant de décision **unique** : lis le haut de `pilotage/decisions.md` avant de numéroter (le 20/11, nuit et design ont pris D-20261120-1).
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
1. (20/11, avis du chef) Pastille Risque : gardée (✅). **Prends un identifiant libre** (D-20261120-2 est déjà pris par le chef, lis `decisions.md`).
2. (18/11, n° 58) **Étude de marché (a)** (GitHub, sites de suivi de PEA ou de bourse), jamais faite : relève 2 idées concrètes pour rendre une fiche plus claire, sans rien retirer.
3. (18/11) Note chiffrée de la page et lecture du graphique à **360 px** sur une fiche ETF avec historique (reportées 4 nuits : ne la reporte pas).

## Pour le vérificateur du code
1. (20/11) `pypdf` justifié, merci. Idée n° 65 : extrais la décision de glissement (120 px) dans une fonction pure testable par node, si elle tient en 40 lignes.
2. (20/11) Alerte IBE.MC (Boursorama 18,04, place « Sibe ») revenue 4 jours de suite : propose un test ou un réglage de `verif.py` qui l'écarte (page sans cotation), sans masquer un vrai écart.
3. (19/11) Confidentialité : chaque jour.
