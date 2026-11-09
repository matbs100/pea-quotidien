---
tags: [pea, guide, reseau]
date: 2026-11-09
---
# 🌐 Sites à autoriser pour les agents du cloud

Les agents de Matin PEA tournent dans le cloud d'Anthropic, dont le réseau ne laisse passer que les sites
autorisés. Sans eux, la fiche ne peut pas lire les prix depuis le cloud, et les agents ne peuvent pas lire
la presse ni les PDF. **À faire par le propriétaire**, sur claude.ai dans un navigateur : **Paramètres →
Capacités** (domaines autorisés). Les nouvelles conversations et les prochaines tâches planifiées en
profitent ; une conversation déjà ouverte peut ne pas les voir.

Si le réglage propose d'autoriser **tous les domaines**, c'est le plus simple. Sinon, ajoute cette liste.

## Prix et données (indispensables)

| Domaine | Pour quoi |
|---|---|
| `query1.finance.yahoo.com`, `query2.finance.yahoo.com`, `fc.yahoo.com`, `finance.yahoo.com` | cours, historiques (yfinance) |
| `www.boursorama.com` | contrôle des prix, éligibilité PEA, ISIN, actualités |
| `markets.ft.com`, `www.ft.com` | contrôle des prix, fonds, presse internationale |
| `www.wealins.com`, `www.e-wealins.com` | valeurs des fonds d'assurance vie |
| `www.justetf.com` | caractéristiques des ETF |
| `live.euronext.com`, `www.euronext.com` | fiches des titres, indices CAC, calendrier |
| `pypi.org`, `files.pythonhosted.org` | installer yfinance, pandas… |

## Presse et estimations (revue de presse du jour)

`www.lesechos.fr`, `investir.lesechos.fr`, `www.zonebourse.com`, `www.marketscreener.com`,
`www.abcbourse.com`, `www.bfmtv.com`, `bourse.lefigaro.fr`, `www.lefigaro.fr`, `www.capital.fr`,
`www.agefi.fr`, `www.reuters.com`, `www.bloomberg.com`, `www.economist.com`, `www.cnbc.com`,
`www.marketwatch.com`

## Lectures et réglementation (PDF)

Voir la colonne « Réseau du cloud » de `pilotage/sources-verifiees.md` : les lignes « à autoriser »
(`www.esma.europa.eu`, `www.eiopa.europa.eu`, `www.bis.org`, `www.lafinancepourtous.com`,
`www.stoxx.com`, etc.).

## Vérifier

Après l'ajout, dans une nouvelle conversation, demande à Claude de lancer
`curl -s -o /dev/null -w '%{http_code}' https://query1.finance.yahoo.com/v8/finance/chart/AI.PA` :
un code 200 veut dire que c'est bon.
