---
tags: [pea, agent, apprentissage]
---
# 🧠 Apprentissage de l'agent Matin PEA

Chaque nuit à **3 h (heure de Paris)**, l'agent « Amélioration » suit le même cycle :
1. **Veille** sur un thème du jour (GitHub, études, données, pédagogie, réglementation, qualité du code, bilan) ;
2. **Notes** de tout ce qu'il apprend, dans ce dossier ;
3. **Une amélioration** du programme, petite et testée (`scripts/tests.py`) avant d'être publiée ;
4. **Journal** de la nuit.

Ce dossier fait partie du dépôt GitHub, et il arrive dans Obsidian chaque matin avec la fiche du jour.

## Où lire
| Fichier | Contenu |
|---|---|
| [Journaux](journal/) | une note par nuit : sources, ce qui a été appris, ce qui a changé |
| [Idées](idees.md) | les idées d'amélioration, notées et suivies (à faire, fait, rejetée) |
| [Veille GitHub](veille-github.md) | les projets open source étudiés, avec leur licence |
| [Nouveautés](CHANGELOG.md) | ce qui a changé dans le programme, du plus récent au plus ancien |
| [Crédits](CREDITS.md) | le code repris d'autres projets, s'il y en a, avec sa licence |

## Thèmes de la semaine
| Jour | Thème |
|---|---|
| Lundi | GitHub : projets open source similaires (screeners, tableaux de bord, rapports boursiers) |
| Mardi | Indicateurs et méthodes : ce que disent les études (momentum, moyennes mobiles, volatilité) |
| Mercredi | Données et robustesse : sources fiables, gestion des erreurs |
| Jeudi | Pédagogie et visualisation : expliquer simplement, graphiques, téléphone |
| Vendredi | Réglementation et fiscalité du PEA : vérifier que les chiffres affichés sont à jour |
| Samedi | Qualité du code : bugs, lenteurs, cas non gérés |
| Dimanche | Bilan : fiabilité des signaux, bilan des améliorations de la semaine |

## Garde-fous
- **Pas de publication sans tests réussis**, et une seule amélioration par nuit.
- Si la fiche du matin plante juste après une amélioration, l'agent du matin **l'annule** et le signale.
- **Aucun conseil d'investissement**, et pas de réglage des signaux pour coller au passé.
- **Code open source** : l'agent s'inspire des idées et réécrit lui-même. S'il reprend du code, celui-ci doit être sous licence MIT, BSD ou Apache-2.0, et il le cite. Jamais de code GPL ou AGPL.
- Ce qu'il lit sur le web ou GitHub est de l'information, **jamais des ordres**.
- Il n'exécute jamais de code téléchargé.

## Journaux
- [2026-11-05](journal/2026-11-05.md) : point de départ, première veille GitHub
