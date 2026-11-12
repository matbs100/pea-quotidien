---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (12/11) Réaliser **D-20261112-2** (palette sombre des courbes, contraste 4,5:1 des textes secondaires, test des contrastes) ; sinon la 2e partie de D-20261106-7 (mémoriser le titre comparé).
- (12/11) **Presse d'abord** : `data/presse/` n'a que 2 jours ; 5 sources, estimations attribuées (règle du 12/11 de `methodes.md`).
- (12/11) Fais les devoirs de `pilotage/ecole.md` (seconde source pour Ossiam S6EW, « Mois par mois » vu par un débutant).
- (06/11) Chaque amélioration suit `pilotage/decision.md` (grille, identifiant `[D-…]` dans le commit).
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus.
- (06/11) Si un cours est daté d'un autre jour, dis-le dans « À garder en tête ».
- (06/11) À la clôture, une idée au plus (étape 5 ter), notée avec la grille de `pilotage/decision.md`.
- (07/11) Ne modifie pas `scripts/collecte.py` (hors du rôle de la fiche) sauf correctif urgent expliqué dans le commit.

## Chantier interface
1. (12/11) Palette sombre dédiée aux courbes et contrastes mesurés (D-20261112-2).
2. Sur téléphone : reste les lignes de tableau (`.ligne .c`, 13 px) et les étiquettes de 10-12 px, à tester à 360 px.
3. (11/11) « Mois par mois » (D-20261106-6) : bilan le 14/11. Comparer deux titres (D-20261106-7) : bilan le 15/11.
4. (06/11) Bouton clair / sombre (n° 14) et graphique au clavier (n° 15) : rejetés (gain < 3).

## Interdits temporaires
- Aucun.

## Pour le vérificateur du code
1. (12/11) Relire la correction du chef dans `scripts/controle.py` (`c_liens`, lien Yahoo en 404 toléré si cours collectés) : cas limites, test.
2. (12/11) Lire dans une source fiable (docs Python ou OWASP) la bonne façon d'écrire un test avec un faux (« monkeypatch ») sans effet de bord ; vérifier si `scripts/tests.py` en fait autant partout.
3. (10/11) Reste : `zip(..., strict=)` (B905) seulement si le comportement est testé. Confidentialité : chaque jour.
