---
tags: [pea, agent, pilotage, decision]
---
# ⚖️ Méthode de décision des améliorations

Lue par tous les agents. **Autorisation du propriétaire (6 novembre 2026)** : une amélioration jugée utile
selon cette méthode est réalisée et publiée **sans attendre sa validation**. En échange, chaque
décision est notée dans le [[decisions|journal des décisions]], mesurée après coup, et annulée si elle
n'apporte pas ce qu'elle promettait. Tout arrive dans Obsidian à la synchronisation suivante du Mac.

## 1. Proposer (tous les agents)

Une idée = une ligne de `apprentissage/idees.md` : ce qui change pour le propriétaire, sa source, l'**indicateur**
qui dira si elle a réussi, et les notes de la grille ci-dessous. Statut de départ : `proposée`.

| Agent | Ce qu'il propose |
|---|---|
| Agent de nuit (veille) | ce qu'il a appris : méthodes, design, sources de données, projets open source |
| Chef d'orchestre | ce que montrent les contrôles, la revue des commits et les bilans (au moins une idée par jour) |
| Fiche du jour (clôture) | ce qu'elle a remarqué en préparant la fiche : donnée absente, libellé peu clair, calcul douteux |
| Titres suivis (samedi) | ce qui manque dans les données des titres (ISIN, place, source) |

## 2. Noter : la grille

Chaque critère est noté de 0 à 5.

| Critère | Question | Poids |
|---|---|--:|
| **Utilité** | Aide-t-elle le propriétaire (débutant, PEA, téléphone) à comprendre ou à suivre ses placements ? | 30 % |
| **Résultats** | Quel gain mesurable : prix plus fiables, erreurs en moins, fiche plus rapide, données en plus ? Pour une idée proche d'une décision déjà mesurée, ce que le bilan a montré | 25 % |
| **Visuel et clarté** | Plus lisible, plus beau, plus simple au téléphone, cohérent avec le style de la fiche ? | 20 % |
| **Avantage de la nouveauté** | Qu'apporte-t-elle que la fiche n'a pas déjà ? (un doublon vaut 0) | 15 % |
| **Fiabilité des données** | Sources ouvertes, vérifiables, `robots.txt` respecté ? | 10 % |

- **Gain** = moyenne pondérée des cinq notes (de 0 à 5).
- **Coût** (0 à 5, à part) : temps de travail, lignes de code, poids de la page, requêtes, quota Claude.
- **Risque** (0 à 5, à part) : casser la fiche, afficher une information fausse, embrouiller un débutant.
- **Priorité** = Gain × 2 − Coût − Risque (la plus haute d'abord).

## 3. Décider

- **Veto** (rejet immédiat, quelle que soit la note) : conseil d'achat ou de vente, donnée personnelle
  publiée, protection anti-robot contournée, source non vérifiable, signaux ou score réglés pour coller
  au passé, donnée passée modifiée, dépendance externe lourde sans nécessité.
- **Adoptée** : Gain ≥ 3,5, Risque ≤ 2 et Coût ≤ 3. Réalisée dès que possible, sans validation.
- **À l'essai** : Gain ≥ 3, Risque ≤ 2 et Coût ≤ 3. Réalisée en version réduite ; le bilan décide de la suite.
- **En attente** : Gain ≥ 3 mais Coût ou Risque trop hauts, ou données insuffisantes. On cherche à la
  découper en plus petit ; on la renote quand un fait nouveau arrive.
- **Rejetée** : Gain < 3, ou veto. La raison est notée ; une idée rejetée peut revenir avec un fait nouveau.
- **Correction** : un bug, une information fausse ou un écart avec un fait vérifié est adopté d'office et
  passe avant tout le reste.
- **Qui décide** : le chef d'orchestre, chaque matin. L'agent de nuit peut appliquer seul la grille à une
  idée qui passe le seuil « adoptée » (**décision provisoire**) ; le chef la confirme ou l'annule le
  lendemain.

## 4. Réaliser

- Chaque décision a un identifiant `D-AAAAMMJJ-n` (date de la décision, numéro du jour).
- Le commit qui la réalise le cite : `Amélioration : <titre> [D-20261107-1]` ou
  `Chef : … ; <correction> [D-…]`. Tests obligatoires, ligne dans `ARCHITECTURE.md` pour toute fonction,
  entrée dans `apprentissage/CHANGELOG.md` pour tout changement visible (avec l'identifiant).
- Cadence : une amélioration par nuit (une seconde si elle fait moins de 80 lignes et que tout est au
  vert), une par jour pour le chef. Jamais plus de 300 lignes de code par commit.

## 5. Mesurer (par les résultats)

Trois jours de bourse après la réalisation, le chef fait le **bilan** avec l'indicateur annoncé (tests,
contrôle qualité, temps de collecte, erreurs, nombre de données, lisibilité constatée, retour de
Le propriétaire) :

- ✅ **gardée** : l'indicateur est atteint ;
- 🔧 **à ajuster** : utile mais incomplète ; une nouvelle idée est proposée ;
- ↩️ **annulée** : `git revert`, avec la raison ; l'idée passe en `annulée : raison`.

Les bilans servent à noter les idées suivantes (critère « Résultats ») : une famille d'idées qui
échoue souvent est notée plus bas.

## 6. Garder la trace

- `pilotage/decisions.md` : une ligne par décision (identifiant, notes, décision, réalisation, indicateur, bilan).
- `apprentissage/idees.md` : les idées et leurs notes ; `apprentissage/CHANGELOG.md` : ce qui change pour le propriétaire.
- Le relais du Mac (9 h 40 et 18 h 40, ou à la réouverture de l'appli Claude) rapatrie tout dans
  Obsidian, ajoute les nouvelles décisions à la note « Agent PEA Quotidien » et à la mémoire de Claude.
- `scripts/controle.py` vérifie chaque matin que toute amélioration du code cite une décision du journal
  et qu'aucun bilan n'est en retard.

## Historique de la méthode

Le chef peut affiner les poids ou les seuils une fois par semaine au plus, en expliquant pourquoi ici
et dans son rapport (bilans à l'appui).

- 2026-11-06 : première version (demande du propriétaire : décider par les résultats, le visuel et les
  avantages de la nouveauté ; adoption automatique de ce qui est utile).
