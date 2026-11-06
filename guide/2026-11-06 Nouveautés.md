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

- **Tous les ETF éligibles au PEA cotés à Paris** : confié à une tâche ponctuelle qui vérifie chaque ETF
  (cours publiés par Yahoo, éligibilité PEA et ISIN sur Boursorama) avant de l'ajouter. Le premier essai
  (10 h 50) s'est arrêté sans rien publier ; relancé à 18 h 25 avec l'obligation d'écrire un rapport.
  Résultat : [[2026-11-06 Ajout des ETF - rapport]] et le commit « Univers : ajout de N ETF… ».
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
| Samedi à 4 h 20 | nouvelle tâche : recherche des nouveaux ETF éligibles au PEA et des actions entrées dans le CAC 40, le SBF 120 ou l'Euro Stoxx 50 (20 ajouts au plus, chacun vérifié) ; les titres qui ne cotent plus sont signalés, jamais supprimés |

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

- [ ] Vérifier le nombre d'ETF ajoutés par la tâche relancée le 6 novembre à 18 h 25
  ([[2026-11-06 Ajout des ETF - rapport]]).
- [ ] Fiche de clôture du 6 novembre : pas encore publiée à 18 h 15 (passage du chef d'orchestre, état
  rouge à cause d'un seul lien Yahoo, RS2K.PA, introuvable depuis le cloud). Plusieurs tâches ont été
  relancées vers 18 h 15 : vérifier qu'une seule notification de clôture est arrivée.
- [ ] Fiche d'ouverture du 6 novembre : 12 titres avec un cours du 4 novembre (vu par le chef
  d'orchestre de 12 h 30 ?). Les suggestions ignorent ces cours.
- [ ] Possible plus tard : un lien pour transférer tes achats vers un autre appareil (Mac).
- [ ] Wealins.com : écarté (le site ne publie pas les cours des titres de la fiche, et le réseau du
  cloud ne l'atteint pas).

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
