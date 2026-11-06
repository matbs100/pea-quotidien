---
tags: [pea, agent, apprentissage]
---
# 🛠 Nouveautés du programme

Du plus récent au plus ancien. Chaque entrée commence par `## AAAA-MM-JJ · titre` : la fiche du jour affiche la plus récente.

## 2026-11-06 · Textes un peu plus grands sur téléphone
- Chiffres des lignes à 13 px (au lieu de 12) et badge de risque à 12 px (au lieu de 11). Contrastes du gris vérifiés : 4,7:1 au minimum en clair, 6:1 en sombre.

## 2026-11-06 · Risque visible sur la page principale
- Chaque ligne du top 30 et des petits prix affiche un badge « Risque 4/7 » (officiel du DIC, ou « estimé » pour les actions), coloré du vert au rouge.
- Un toucher sur le badge affiche sa définition, sans ouvrir la fiche.
- Demandé par Mathieu ; inspiré du SRI PRIIPs déjà utilisé dans les fiches.

## 2026-11-05 · Définitions au toucher
- Dans les fiches détaillées, les libellés volatilité, pire baisse, bêta, RSI, PER, rendement et moyennes ont une définition courte au toucher, au survol ou au clavier (Tab).
- Inspiré des guides d'accessibilité des graphiques et indicateurs (Penn State, GWU).

## 2026-11-05 · Agent qui apprend et s'améliore chaque nuit
- Nouvelle routine de nuit (3 h) : veille, notes dans ce dossier, une amélioration testée par nuit.
- Tests garde-fous (`scripts/tests.py`) obligatoires avant toute publication.

## 2026-11-05 · Fiches détaillées cliquables
- Un clic sur un titre ouvre sa fiche : graphique sur 5 ans, risque SRI de 1 à 7, frais, caractéristiques, éligibilité PEA selon Boursorama, historique des signaux.

## 2026-11-05 · Contrôle des prix
- Chaque prix affiché est comparé entre Yahoo Finance, Boursorama et le Financial Times.

## 2026-11-05 · Première version
- Fiche animée du matin : indices, euro/dollar, top 30 éligible PEA, 10 petits prix, signaux suivis dans le temps.
