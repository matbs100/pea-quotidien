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

## Le plus simple

Dans **Claude Code** (https://claude.ai/code), réglages de l'**environnement** des tâches planifiées →
**Accès réseau** : choisis l'accès **complet** (tous les domaines) s'il est proposé. Sinon « personnalisé »
avec toute la liste ci-dessous. Même chose pour les conversations : claude.ai → Paramètres → Capacités.

## Prix et données

```
query1.finance.yahoo.com
query2.finance.yahoo.com
fc.yahoo.com
finance.yahoo.com
guce.yahoo.com
consent.yahoo.com
www.boursorama.com
api.boursorama.com
markets.ft.com
www.ft.com
www.wealins.com
www.e-wealins.com
www.justetf.com
live.euronext.com
www.euronext.com
www.abcbourse.com
www.zonebourse.com
www.marketscreener.com
www.morningstar.fr
www.quantalys.com
pea.fr
www.amf-france.org
geco.amf-france.org
stooq.com
www.investing.com
```

## Presse et estimations

```
www.lesechos.fr
investir.lesechos.fr
www.lefigaro.fr
bourse.lefigaro.fr
www.capital.fr
www.bfmtv.com
www.latribune.fr
www.agefi.fr
www.lemonde.fr
www.boursier.com
www.reuters.com
www.bloomberg.com
www.cnbc.com
www.marketwatch.com
www.economist.com
www.wsj.com
www.ecb.europa.eu
www.banque-france.fr
www.insee.fr
www.federalreserve.gov
```

## Apprentissage (PDF, réglementation, fonds)

```
www.lafinancepourtous.com
www.esma.europa.eu
www.eiopa.europa.eu
www.bis.org
www.imf.org
www.oecd.org
www.stoxx.com
www.msci.com
www.spglobal.com
www.amundietf.fr
www.ishares.com
www.amundi.fr
www.legifrance.gouv.fr
www.service-public.gouv.fr
www.economie.gouv.fr
bofip.impots.gouv.fr
```

## Outils

```
pypi.org
files.pythonhosted.org
github.com
raw.githubusercontent.com
objects.githubusercontent.com
```

## Vérifier

Après l'ajout, dans une nouvelle conversation, demande à Claude de lancer
`curl -s -o /dev/null -w '%{http_code}' https://query1.finance.yahoo.com/v8/finance/chart/AI.PA` :
un code 200 veut dire que c'est bon.
