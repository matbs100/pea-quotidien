# Matin PEA

Fiche boursière quotidienne et animée pour un PEA : suivi de mes investissements (notés dans
`mes-investissements.md`), euro/dollar, grands indices, suggestions du jour (actions à regarder, choisies
par des règles chiffrées), top 30 éligible PEA (actions européennes et ETF), 10 titres liquides à moins
de 2 €, et signaux techniques dont la fiabilité est mesurée dans le temps. Les prix viennent de Yahoo Finance et sont contrôlés avec Boursorama et le
Financial Times.

Quatre agents Claude travaillent dans le cloud, chacun avec sa consigne :
- **Fiche du jour** (`ROUTINE.md`), à 9 h 15 et 17 h 55 les jours de bourse : collecte, contrôle des prix, analyse, site, notification ;
- **Veille et amélioration** (`AMELIORATION.md`), chaque nuit à 3 h : apprend (marchés, méthodes, design, pédagogie, open source), note ce qu'il apprend dans `apprentissage/` avec ses sources, et améliore le programme par une petite modification testée ;
- **Vérificateur du code** (`VERIFICATION.md`), chaque jour à 4 h, sous la direction du chef : veille à la confidentialité du propriétaire (aucune information personnelle dans le dépôt ni sur le site), vérifie que le code est bien fait et marche, fait au plus une correction testée, apprend chaque jour une technique de code dans des sources fiables et propose des idées ;
- **Chef d'orchestre** (`CHEF.md`), chaque jour à 5 h : contrôle tout (`scripts/controle.py`), vérifie les faits appris, relit et peut annuler le travail des autres, corrige un bug ou embellit l'interface, et donne ses consignes dans `pilotage/`.

Le programme est expliqué fonction par fonction dans `ARCHITECTURE.md`.
**Information et apprentissage uniquement : ce n'est pas un conseil en investissement.**

| Dossier | Contenu |
|---|---|
| `scripts/collecte.py` | prix, indicateurs, classements, suivi des signaux |
| `scripts/verif.py` | contrôle croisé Yahoo / Boursorama / FT |
| `scripts/fiches.py` | fiches détaillées : historique 5 ans, risque SRI (DIC PRIIPs ou estimé), frais, caractéristiques, éligibilité PEA |
| `scripts/rendu.py` + `modele.html` | fiche animée (`docs/`) et note Obsidian (`notes/`) |
| `scripts/controle.py` | contrôle qualité du chef d'orchestre (écrit `pilotage/etat.json`) |
| `scripts/tests.py` | tests garde-fous, obligatoires avant toute publication |
| `scripts/confidentialite.py` | aucune information personnelle dans le dépôt public ni sur le site (termes protégés par empreinte) |
| `pilotage/` | consignes, état et rapports du chef d'orchestre |
| `apprentissage/` | journal de nuit, idées, connaissances vérifiées, nouveautés |
| `descriptions.json` | courtes descriptions rédigées par Claude (aucun texte copié) |
| `data/` | une capture JSON par jour, historique CSV, signaux, analyses |
| `univers.json` | les titres suivis |
| `mes-investissements.md` | mes achats (un par ligne), suivis à chaque fiche ; tenu par le propriétaire seul |

Sur le Mac : double-clic sur **`Matin PEA.command`** (prépare Python, fait la fiche du jour, copie les notes
dans Obsidian, lance le contrôle et propose de publier). Sites à autoriser pour le cloud :
[`guide/Domaines à autoriser.md`](guide/Domaines%20à%20autoriser.md).

Relancer à la main : `pip install -r requirements.txt`, puis `python scripts/collecte.py`,
`python scripts/verif.py AAAA-MM-JJ`, `python scripts/fiches.py AAAA-MM-JJ`, `python scripts/rendu.py AAAA-MM-JJ`.
Contrôler tout le projet : `python scripts/controle.py` (ou `--hors-ligne`), puis `python scripts/tests.py`.
