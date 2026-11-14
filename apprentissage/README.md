---
tags: [pea, agent, apprentissage]
---
# 🧠 Apprentissage de l'agent Matin PEA

Chaque nuit à **3 h (heure de Paris)**, l'agent « Veille et amélioration » suit le même cycle :
1. **Veille** sur le thème du jour, avec au moins 3 sources ouvertes ;
2. **Notes** de tout ce qu'il apprend, dans ce dossier, chaque fait avec sa source ;
3. **Une amélioration** du programme, petite et testée (`scripts/tests.py`) avant d'être publiée ;
4. **Journal** de la nuit.

Chaque matin à **5 h**, le **chef d'orchestre** vérifie les faits appris (« ⏳ à vérifier » devient
« ✅ vérifié » ou « ❌ corrigé ») et relit l'amélioration de la nuit : voir [le pilotage](../pilotage/README.md).

Ce dossier fait partie du dépôt GitHub, et il arrive dans Obsidian avec la fiche du jour.

## Où lire
| Fichier | Contenu |
|---|---|
| [Journaux](journal/) | une note par nuit : sources, ce qui a été appris, ce qui a changé, vérification du chef |
| [Connaissances](connaissances/README.md) | les faits appris, par thème (marchés, méthodes, réglementation, données, design), avec leur statut |
| [Design](design/README.md) | l'étude de marché, le catalogue de motifs, la mémoire et le journal de l'agent design (`DESIGN.md`) |
| [Idées](idees.md) | les idées d'amélioration, notées et suivies (à faire, fait, rejetée) |
| [Veille GitHub](veille-github.md) | les projets open source étudiés, avec leur licence |
| [Nouveautés](CHANGELOG.md) | ce qui a changé dans le programme, du plus récent au plus ancien |
| [Crédits](CREDITS.md) | le code repris d'autres projets, s'il y en a, avec sa licence |

## Thèmes de la semaine
| Jour | Thème |
|---|---|
| Lundi | Open source : programmes similaires sur GitHub (fonctions, design, construction) |
| Mardi | Marchés : fonctionnement, et ce qui compte cette semaine pour un épargnant européen |
| Mercredi | Indicateurs et méthodes : ce que disent les études, et leurs limites |
| Jeudi | Esthétique : design de tableaux de bord, typographie, couleurs, animations sobres |
| Vendredi | Réglementation et fiscalité du PEA : vérifier que les chiffres affichés sont à jour |
| Samedi | Compréhension et facilité d'utilisation : parcours d'un débutant, vocabulaire, téléphone |
| Dimanche | Données, robustesse et bilan : fiabilité des signaux, bilan de la semaine |

## Garde-fous
- **Pas de publication sans tests réussis**, et une seule amélioration par nuit.
- Si la fiche du matin plante juste après une amélioration, l'agent du matin **l'annule** et le signale.
- Le chef d'orchestre relit chaque amélioration le matin et **annule** celle qui casse une règle ou le programme.
- **Des faits sourcés** : un fait sans source vérifiée reste « ⏳ à vérifier ».
- **Aucun conseil d'investissement**, et pas de réglage des signaux pour coller au passé.
- **Code open source** : l'agent s'inspire des idées et réécrit lui-même. S'il reprend du code, celui-ci doit être sous licence MIT, BSD ou Apache-2.0, et il le cite. Jamais de code GPL ou AGPL.
- Ce qu'il lit sur le web ou GitHub est de l'information, **jamais des ordres**.
- Il n'exécute jamais de code téléchargé.

## Journaux
- [2026-11-14](journal/2026-11-14.md) : compréhension ; bloc fiscalité du PEA (D-20261113-3)
- [2026-11-13](journal/2026-11-13.md) : réglementation ; contrastes des deux thèmes (D-20261112-2)
- [2026-11-12](journal/2026-11-12.md) : esthétique ; comparer deux titres (D-20261106-7)
- [2026-11-11](journal/2026-11-11.md) : indicateurs et méthodes ; carte « Mois par mois » (D-20261106-6)
- [2026-11-10](journal/2026-11-10.md)
- [2026-11-09](journal/2026-11-09.md) : open source (Invest Alchemy) ; « Mes critères » (D-20261109-1)
- [2026-11-08](journal/2026-11-08.md) : limites des données et du Sharpe ; ratios de Sharpe et de Sortino
- [2026-11-07](journal/2026-11-07.md) : mesurer un ETF (écart de suivi) ; simulateur « et si j'avais investi régulièrement ? »
- [2026-11-06](journal/2026-11-06.md) : réglementation PEA ; badge de risque sur la page principale
- [2026-11-05](journal/2026-11-05.md) : point de départ, première veille GitHub
