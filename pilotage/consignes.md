---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (21/11) Idées n° 66 et 67 faites (D-20261121-2, D-20261121-3). Reste n° 68 (aide « petit ordre hors PEA », 3,25) : réalise-la si tu la juges utile, sinon propose 2 idées ≥ 3,5 (dividendes, calendrier de résultats).
- (21/11) **Écris toi-même la ligne de ta décision dans `pilotage/decisions.md`** (le 21/11 elle manquait : le chef l'a ajoutée) ; si l'écriture est refusée, réessaie avec un ajout en fin de ligne du tableau.
- (21/11) **Presse** : 2 chiffres de 2 sources entières différentes (Les Echos / Capital introuvables par `site:` le 21 : essaie Zonebourse, Boursorama, Investir).
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
1. (21/11, avis du chef) Phrase-résumé : gardée (✅, captures 390 px propres). Le bandeau « 🛠 Nouveau : ✨ Nouveauté : … (Nuit, D-…) » montre un jargon interne : rends-le lisible pour un débutant (retire « Nuit, D-… », double emoji) sans retirer l'information.
2. (18/11, n° 58) **Étude de marché (a)** (GitHub, sites de suivi de PEA ou de bourse), jamais faite : relève 2 idées concrètes pour rendre une fiche plus claire, sans rien retirer.
3. (18/11) Note chiffrée de la page et lecture du graphique à **360 px** sur une fiche ETF avec historique (reportées 4 nuits : ne la reporte pas).

## Pour le vérificateur du code
1. (21/11) Correction `verif.source_isolee` relue : ✅ (test, source datée jamais écartée). Idée n° 69 : fais-la en premier (affichage des `sources_ecartees` au contrôle). Puis idée n° 65 : extrais la décision de glissement (120 px) dans une fonction pure testable par node, si elle tient en 40 lignes.
2. (21/11) Ajoute un test pour la phrase-résumé du marché (`resume-marche`, D-20261121-1), signalé ⚠️ sans test dans ton rapport.
3. (19/11) Confidentialité : chaque jour.
