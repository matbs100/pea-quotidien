---
tags: [pea, guide, nouveautes]
date: 2026-11-06
---
# 🆕 Nouveautés du 6 novembre 2026

Tout ce qui a été ajouté à Matin PEA ce jour-là, avec Claude, à la demande de Mathieu : comment
s'en servir, ce qui tourne tout seul, et ce qui reste à faire. Les détails techniques sont dans
[[ARCHITECTURE]] et la liste des changements dans [[apprentissage/CHANGELOG|les nouveautés]].

> [!warning] Information et apprentissage : rien sur la fiche n'est un conseil en investissement.

## 1. Mes investissements (en haut de la fiche)

**Ajouter un achat**
1. Ouvre la fiche du jour, partie « Mes investissements ».
2. Tape l'ISIN (par exemple `FR001400U5Q4`), le nom (« Air Liquide ») ou le code (`DCAM`) dans la barre de recherche.
3. Touche le bon titre, puis indique la date d'achat, le prix d'une part et le nombre de parts (facultatif).
4. Appuie sur « Ajouter à mes investissements ».

Autre chemin : chaque fiche détaillée (toucher une ligne du top 30, une suggestion…) a un bouton
« Ajouter à mes investissements ».

**Ce que la fiche affiche** : pour chaque titre, le prix du jour, la variation sur la séance,
l'évolution depuis l'achat et, si le nombre de parts est noté, la valeur et la plus-value en euros ;
en haut, le total (valeur, plus-value, variation de la séance). Plusieurs achats du même titre donnent
un prix d'achat moyen pondéré. Un achat du jour compte depuis son prix d'achat. Frais de courtage non
compris.

**Retirer un titre** : le ✕ de sa ligne (une confirmation est demandée).

**Où sont gardés tes achats** : seulement sur ton téléphone, dans le navigateur (rien n'est publié,
le site et le dépôt étant publics). Conséquence : ils n'apparaissent ni sur le Mac ni dans un autre
navigateur. Une fiche archivée n'affiche que les achats antérieurs à sa date.

**Autre façon de noter un achat** : le fichier [[mes-investissements]] (tableau : code ou ISIN, date,
prix, quantité, type). Ces achats apparaissent sur la fiche et dans la note Obsidian du jour, sur tous
les appareils, mais ils sont **publics**. Les agents ne modifient jamais ce fichier.

**Quels titres sont trouvables** : ceux que suit la fiche (liste `univers.json`). Les ISIN se
complètent tout seuls au fil des fiches (60 titres de plus par fiche) ; en attendant, la recherche par
nom marche pour tous. Pour un titre absent, donner son ISIN à Claude.

## 2. Suggestions du jour

Jusqu'à 5 actions à regarder de plus près, chacune choisie par une règle chiffrée, avec sa raison :
- nouveau signal « hausse » (le signal de la veille était neutre ou en baisse) ;
- entrée dans le top 30 ;
- au plus haut sur un an après une hausse sur 3 mois ;
- repli (RSI sous 40) alors que la tendance de fond monte (au-dessus de la moyenne 200 jours) ;
- gros mouvement du jour (au moins 3 % sur la séance).

Les titres suggérés les 3 jours précédents passent après les autres, pour varier. Seuls les titres
cotés à la dernière séance sont retenus. Ce sont des pistes à étudier (fiche, actualité, risque),
**pas une liste d'achats**.

## 3. Liste des titres suivis élargie

- **70 titres ajoutés le soir, depuis le Mac** (les deux essais dans le cloud, à 10 h 50 et 18 h 25, ne
  pouvaient rien vérifier : ils tournaient dans un environnement cloud qui bloque pypi.org, Yahoo et
  Boursorama). Chaque titre a passé deux vérifications : cours du jour sur Yahoo, « éligible PEA » et ISIN
  sur Boursorama. 25 ETF, 4 ETF à effet de levier et 41 actions ; la liste suivie compte maintenant
  42 ETF, 4 à effet de levier, 122 actions et 68 petites valeurs. Détail : [[2026-11-06 Ajout des ETF - rapport]].
- **ISIN** : 224 titres sur 236 ont leur ISIN. Les 70 nouveaux apparaissent dans la recherche dès la fiche
  de lundi 9 h 15 (il leur faut d'abord un cours).
- **3 ou 4 ETF à effet de levier** (×2 ou inverses), à la demande de Mathieu, dans une section à
  part (`etf_levier`) : trouvables dans la recherche, avec fiche et contrôle du prix, mais **hors du
  top 30 et des suggestions**. Badge rouge « Effet de levier » et avertissement : ils amplifient les
  variations de chaque jour et peuvent perdre de la valeur même si l'indice revient à son niveau de
  départ.

## 3 bis. Devise de chaque titre

- La devise de cotation (EUR pour Paris, Amsterdam, Francfort…, DKK pour Copenhague) est affichée à côté
  de chaque prix : top 30, petits prix, suggestions, mes investissements, recherche, fiche détaillée.
- Dans la fiche d'un ETF, une ligne « Risque de change » explique qu'un ETF coté en euros qui suit des
  actions étrangères bouge aussi avec leurs devises, sauf s'il est couvert (« Hedged »).
- Mes investissements : les montants d'un titre coté hors euros sont affichés dans sa devise et ne sont
  pas comptés dans le total en euros.

## 4. Ce qui se met à jour tout seul

| Quand | Quoi |
|---|---|
| 9 h 15 et 17 h 55, jours de bourse | prix de tous les titres suivis, suggestions, ISIN manquants (60 par fiche) ; tes investissements sont recalculés à l'ouverture de la fiche |
| Chaque nuit et chaque matin | **l'école des agents** : le chef corrige les devoirs, améliore le manuel des méthodes (`pilotage/methodes.md`), donne de nouveaux devoirs (`pilotage/ecole.md`) : nouveaux fonds, nouvelles données, nouvelles méthodes |
| Samedi à 4 h 20 | tâche « Titres suivis » (recréée le soir dans le bon environnement, consigne `UNIVERS.md`) : recherche des nouveaux ETF éligibles au PEA et des actions entrées dans le CAC 40, le SBF 120 ou l'Euro Stoxx 50 (20 ajouts au plus, chacun vérifié) ; les titres qui ne cotent plus sont signalés, jamais supprimés |

## 4 bis. Comparaison des prix : seulement les cours du jour

À la demande de Mathieu, une source qui ne donne que le cours de la veille n'est plus prise en compte
dans le contrôle des prix (fonction `source_perimee()` de `verif.py`) : elle est notée à part
(`sources_perimees`). Si un marché n'a pas encore ouvert (cours américains à 9 h 15), c'est la dernière
séance qui compte.

**Wealins** (www.wealins.com/funds-list/) : la liste publie des valeurs liquidatives de fonds d'assurance
vie, **datées de la veille** (le 6 novembre à 18 h 30, toutes au 5 novembre). Ce ne sont pas les titres de
la fiche, et la règle ci-dessus l'écarte : il n'est pas utilisé. Il ne servirait que pour suivre des fonds
Wealins dans « Mes investissements » ; il faudrait alors autoriser `www.wealins.com` dans le réseau du
cloud.

## 5. Garde-fous

- Une erreur dans les suggestions ou dans [[mes-investissements]] ne bloque jamais la fiche.
- Un code faux ou un ISIN inconnu dans le fichier est signalé sur la fiche (« À corriger ») et dans le
  contrôle du chef d'orchestre.
- `controle.py` alerte si un agent modifie [[mes-investissements]].
- Les prix des suggestions et de tes investissements sont contrôlés entre Yahoo, Boursorama et le
  Financial Times, comme le reste.
- 17 tests automatiques (`scripts/tests.py`), dont la lecture du fichier, les calculs, les règles des
  suggestions et le rendu de la page ; parcours de la recherche vérifié dans un navigateur de téléphone.

## 6. Points ouverts

- [x] ETF ajoutés (le soir, depuis le Mac) : voir [[2026-11-06 Ajout des ETF - rapport]].
- [x] Fiche de clôture du 6 novembre publiée (commits `6d2489e` et `e7ac7a5`, rendu régénéré après une
  fusion : une seule fiche).
- [ ] Fiche d'ouverture du 6 novembre : 12 titres avec un cours du 4 novembre. Les suggestions ignorent
  ces cours.
- [ ] Lundi 9 h 15 : vérifier que les 70 nouveaux titres sont dans la recherche et que la collecte reste
  assez rapide (236 titres).
- [ ] Possible plus tard : un lien pour transférer tes achats vers un autre appareil (Mac).
- [ ] Wealins : seulement si tu veux suivre des fonds Wealins (valeur de la veille) dans « Mes
  investissements ».

## 7. Détail technique (pour Claude et les agents)

- `collecte.py` : `lire_investissements`, `mes_investissements`, `suggestions`, `catalogue`,
  `nombre_fr`, `date_iso` ; nouvelles clés du JSON du jour : `suggestions`, `mes_investissements`,
  `catalogue`.
- `fiches.py` : `fichier_cache`, `isin_en_cache` ; ISIN ajouté au catalogue.
- `verif.py` et `fiches.py` : suggestions et investissements contrôlés et détaillés.
- `rendu.py` + `modele.html` : parties « Mes investissements » (barre de recherche, stockage
  `localStorage`, clé `matin-pea:investissements`) et « Suggestions du jour » ; note Obsidian.
- `controle.py` : `mes-investissements.md` hors du rôle de tous les agents ; codes à corriger signalés.
- Commits du 6 novembre préfixés « Mathieu : » (plus « Univers : » pour la liste des titres).
