# Matin PEA

Fiche boursière quotidienne et animée pour un PEA : euro/dollar, grands indices, top 30 éligible PEA
(actions européennes et ETF), 10 titres liquides à moins de 2 €, et signaux techniques dont la fiabilité
est mesurée dans le temps. Les prix viennent de Yahoo Finance et sont contrôlés avec Boursorama et le
Financial Times.

Générée chaque matin de semaine par un agent Claude (voir `ROUTINE.md`).
**Information et apprentissage uniquement : ce n'est pas un conseil en investissement.**

| Dossier | Contenu |
|---|---|
| `scripts/collecte.py` | prix, indicateurs, classements, suivi des signaux |
| `scripts/verif.py` | contrôle croisé Yahoo / Boursorama / FT |
| `scripts/rendu.py` + `modele.html` | fiche animée (`docs/`) et note Obsidian (`notes/`) |
| `data/` | une capture JSON par jour, historique CSV, signaux, analyses |
| `univers.json` | les titres suivis |

Relancer à la main : `pip install -r requirements.txt`, puis `python scripts/collecte.py`,
`python scripts/verif.py AAAA-MM-JJ`, `python scripts/rendu.py AAAA-MM-JJ`.
