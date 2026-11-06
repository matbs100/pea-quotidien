---
tags: [pea, guide, univers, etf]
date: 2026-11-06
---
# Ajout des ETF éligibles au PEA : rapport du 6 novembre 2026

Tâche relancée le 6 novembre vers 18 h 25 (heure de Paris) pour ajouter à `univers.json` les ETF
éligibles au PEA cotés à Paris, plus 3 ou 4 ETF à effet de levier (section `etf_levier`).

## Résultat : aucun ETF ajouté

`univers.json` n'a pas été modifié : ni la section `etf` ni la section `etf_levier` (pas créée).
La raison n'est pas l'absence de candidats. **Le réseau de cette session cloud ne pouvait pas faire
les deux vérifications obligatoires**, et la consigne dit de ne rien ajouter dans ce cas.

## Sites bloqués (réseau de la session)

| Site | Usage | Résultat |
|---|---|---|
| `query1.finance.yahoo.com` | vérification 4a (cours récents via yfinance) | refusé par le proxy du cloud (`CONNECT tunnel failed, response 403`) |
| `www.boursorama.com` | vérification 4b (`fiches.lire_bourso` : ISIN, éligibilité PEA) | refusé par le proxy du cloud (403) |
| `pypi.org` / `files.pythonhosted.org` | `pip install -r requirements.txt` | connexion refusée : **yfinance n'a pas pu être installé** |
| `www.justetf.com` | liste des ETF PEA | injoignable depuis le shell |

Conséquences :
- étape 4a impossible (pas de yfinance, et Yahoo bloqué de toute façon) ;
- étape 4b impossible (`lire_bourso` passe par `requests`, bloqué vers Boursorama) ;
- étape 7 : `scripts/tests.py` donne **5/18** (les 13 échecs viennent tous de
  `ModuleNotFoundError: No module named 'yfinance'`, pas des données). Selon la consigne, seul ce
  rapport est publié.

## Candidats examinés

Aucun candidat n'a pu passer les vérifications 4a et 4b : tous sont donc **écartés pour cette fois,
faute de vérification**, et non parce qu'ils seraient inéligibles.

Un seul a pu être consulté autrement (outil de lecture web Firecrawl, qui passe par un autre réseau) :

| Code | Ce que montre la page Boursorama `1rTPAASI` | Statut |
|---|---|---|
| PAASI | « Amundi PEA Asie Emergente (MSCI Emerging Asia) Screened UCITS ETF - EUR », ISIN `FR0013412012`, Euronext Paris, dernier cours 35,735 € le 6/11/2026 | non ajouté : la mention « PEA » de la rubrique Éligibilité n'a pas pu être lue, et `lire_bourso` n'a pas pu tourner |

Pistes non examinées (aucun moyen de les vérifier selon la procédure) : GPEA, CEU, CD8, MMS, SMC,
CACC, DAX, ESEE, TNO, HLT, BNK, AUT, INS, FOO, CHM, UTI, TRV, MDA, PMEH, PUSA, PINR, PAQ ; à effet
de levier : LVC, LQQ, CL2, BX4. Aucun code, ISIN ou nom n'a été inscrit sans vérification.

## Problèmes rencontrés

- La branche était en « HEAD détaché » au départ : remise sur `claude/pea` (`origin/claude/pea`, commit 19d41d3).
- Firecrawl a renvoyé « Service Unavailable » sur une demande de page HTML complète ; la version
  texte ne contient ni l'ISIN ni la rubrique « Éligibilité » au format attendu par `lire_bourso`.
  Remplacer la procédure de vérification par cet outil aurait été moins sûr : non fait.

## Pour que la prochaine tentative aboutisse

Les fiches quotidiennes atteignent normalement Yahoo depuis le cloud : la restriction semble propre à
cette session. Avant de relancer, vérifier dans claude.ai (Paramètres > Capacités, domaines autorisés)
que sont permis : `pypi.org`, `files.pythonhosted.org`, `query1.finance.yahoo.com`,
`query2.finance.yahoo.com`, `fc.yahoo.com`, `www.boursorama.com`. La tâche du samedi 4 h 20 (recherche
des nouveaux ETF éligibles) fera le même travail si son réseau le permet.
