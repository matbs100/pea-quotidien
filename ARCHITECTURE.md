---
tags: [pea, agent, architecture]
---
# 🏗 Comment Matin PEA est construit

Ce document explique comment le programme fonctionne, fichier par fichier et fonction par
fonction. **Il doit rester exact** : chaque agent qui ajoute ou change une fonction le met à jour
dans le même commit, et le chef d'orchestre vérifie chaque matin que toutes les fonctions y sont
décrites (`scripts/controle.py`).

## Le trajet d'une fiche

```
Yahoo Finance ──► collecte.py ──► data/jours/AAAA-MM-JJ.json ◄── verif.py (Boursorama, FT)
                                         │      ▲
                                         │      └── fiches.py (Boursorama, Yahoo : historique, SRI, frais)
                                         ▼
                  Claude écrit data/analyses/AAAA-MM-JJ.md (6 parties, 350 mots au plus)
                                         ▼
                rendu.py + modele.html ──► docs/ (site GitHub Pages)  et  notes/ (Obsidian)
                                         ▼
                 git push ──► GitHub Pages (≈ 1 min) ──► notification ntfy sur le téléphone
```

`collecte.py` lit aussi `mes-investissements.md` (les achats notés par Mathieu) pour la partie « Mes
investissements », et choisit les « Suggestions du jour » par des règles chiffrées.

Tout tourne dans le cloud (routines Claude Code) : le Mac peut être éteint. Le dépôt est rangé
dans le coffre Obsidian, donc un `git pull` sur le Mac suffit à tout y amener.

## L'équipe d'agents

| Heure (Paris) | Agent | Consigne | Rôle |
|---|---|---|---|
| 3 h, chaque nuit | **Veille et amélioration** | `AMELIORATION.md` | apprend (marchés, design, pédagogie, open source), note ce qu'il apprend dans `apprentissage/`, fait une amélioration testée |
| 5 h, chaque jour | **Chef d'orchestre** | `CHEF.md` | contrôle tout (`controle.py`), vérifie les faits appris, relit les commits des autres, annule ce qui casse, corrige un bug ou embellit l'interface, écrit `pilotage/` |
| 12 h 30, jours de bourse | **Chef d'orchestre, passage de mi-journée** | routine dédiée (lit `CHEF.md`) | vérifie la fiche d'ouverture, la refait et corrige le programme si besoin, s'assure que la clôture pourra tourner ; pas d'embellissement |
| 9 h 15 et 17 h 55, jours de bourse | **Fiche du jour** | `ROUTINE.md` | collecte, contrôle des prix, fiches détaillées, analyse, site, notification |
| 9 h 40 et 18 h 40, si le Mac est allumé | **Relais du Mac** | tâche planifiée de l'appli Claude | `git pull` dans Obsidian, vérifie le site en ligne, recopie l'essentiel dans les notes |

Les agents ne se parlent pas directement : ils communiquent par des fichiers du dépôt.
- `pilotage/consignes.md` : les consignes du chef, que les autres agents lisent en premier ;
- `pilotage/etat.json` : le dernier contrôle, affiché en bas de la fiche ;
- `pilotage/rapports/` : un rapport du chef par jour ;
- `apprentissage/` : ce que l'agent de nuit apprend (journal, idées, connaissances).

Les consignes des routines sont recopiées dans `ROUTINE.md`, `AMELIORATION.md` et `CHEF.md`. Les
agents ne modifient jamais ces trois fichiers : seul Mathieu (avec Claude sur le Mac) les change, en
même temps que la routine correspondante sur claude.ai.

## Les fichiers

| Chemin | Contenu |
|---|---|
| `univers.json` | les titres suivis, par catégorie (indices, devises, matières, ETF, actions, petits prix) |
| `descriptions.json` | courtes descriptions des titres, rédigées sans copier de site |
| `mes-investissements.md` | les achats de Mathieu (code Yahoo, date, prix, quantité, type), un par ligne de tableau. Tenu par Mathieu seul : les agents le lisent mais ne le modifient jamais (`controle.py` le signale). Public, comme tout le dépôt |
| `config.json` | adresse du site et du dépôt (ne pas changer) |
| `data/jours/` | une capture JSON par jour (écrasée à la clôture) |
| `data/analyses/` | l'analyse écrite par Claude, une par jour |
| `data/historique.csv`, `data/signaux.csv` | historique des cours de clôture et des signaux, jugés 5 séances plus tard |
| `data/correspondances.json`, `data/fiches/` | caches : codes Boursorama / FT trouvés, caractéristiques des titres (7 jours) |
| `docs/` | le site : `index.html` (dernière fiche) et `archives/` |
| `notes/` | une note Obsidian par jour |
| `apprentissage/` | journal de nuit, idées, connaissances, veille GitHub, nouveautés, crédits |
| `pilotage/` | consignes, état et rapports du chef d'orchestre |
| `scripts/` | le programme (ci-dessous) |

## Les scripts, fonction par fonction

### `collecte.py` : cours, indicateurs, classement, signaux, suggestions, mes investissements
Usage : `python scripts/collecte.py [AAAA-MM-JJ] [ouverture|cloture]`. Codes de sortie : 0 OK,
3 cours du jour (ou clôture définitive) pas encore publiés, 4 Bourse fermée.

| Fonction | Rôle |
|---|---|
| `telecharger(tickers)` | télécharge 14 mois de cours quotidiens pour tous les titres en un seul appel Yahoo |
| `rsi(s, n)` | RSI sur 14 séances (100 s'il n'y a eu que des hausses) |
| `var(s, n)` | variation en % sur n séances |
| `r(x, n)` | arrondi qui renvoie `None` pour une valeur manquante |
| `mesures(df, t)` | tous les indicateurs d'un titre : variations, moyennes 20/50/200, RSI, volatilité, plus haut et plus bas sur un an, liquidité |
| `signal(m)` | signal à 5 séances : « hausse » si prix > MM20 > MM50 et RSI < 70, « baisse » à l'inverse, sinon « neutre » |
| `rang(serie)` | rang en centiles, pour combiner des mesures d'échelles différentes |
| `classer(lignes)` | score : 35 % perf 3 mois, 25 % 1 mois, 15 % 1 semaine, 15 % tendance, 10 % faible volatilité ; −10 si RSI > 75 |
| `evaluer_signaux(jour, prix_du_jour)` | juge les signaux émis il y a au moins 5 séances |
| `bilan(lignes)` | taux de signaux justes, comparé au repère (part de hausses) |
| `nombre_fr(txt)` | lit un nombre écrit à la française ou à l'anglaise (« 1 234,56 € », « 512.3 ») |
| `date_iso(txt)` | « 06/11/2026 » ou « 2026-11-06 » → « 2026-11-06 » ; `None` pour une date impossible |
| `lire_investissements(texte)` | lit le tableau de `mes-investissements.md` (colonnes reconnues à leur titre, dans n'importe quel ordre) |
| `mes_investissements(entrees, mesure_de, categories, jour)` | regroupe les achats par titre : prix de revient, évolution depuis l'achat, valeur, plus-value et variation du jour en euros si les quantités sont notées, total ; codes ISIN ou introuvables listés dans `erreurs` |
| `suggestions(candidats, top30, signaux_veille, top30_veille, deja, n)` | jusqu'à 5 actions à regarder, une par règle : nouveau signal « hausse », entrée dans le top 30, plus haut sur un an, repli (RSI < 40) au-dessus de la moyenne 200 jours, variation d'au moins 3 % ; chacune avec sa raison chiffrée |
| `paques(annee)` | date de Pâques (algorithme de Meeus) |
| `bourse_fermee(j)` | jours de fermeture d'Euronext : week-end, 1er janvier, Vendredi saint, lundi de Pâques, 1er mai, 25 et 26 décembre |
| `attendre_seance(jour, max_minutes)` | attend que Yahoo publie la séance du jour (décalage de 15 min) |
| `enregistrer(jour, tous, top30, petites, res)` | à la clôture : juge les anciens signaux, note ceux du jour, complète l'historique |
| `cloture_dans_meta(m, jour)` | vrai si les métadonnées Yahoo montrent un dernier échange du jour, après la fin de séance + 5 min |
| `cloture_publiee(jour)` | vérifie la clôture définitive (fixing de 17 h 35) sur deux titres témoins |
| `attendre_cloture(jour, max_minutes)` | attend la clôture définitive, une vérification par minute |
| `main()` | enchaîne tout et écrit `data/jours/AAAA-MM-JJ.json` ; une erreur dans les suggestions ou dans `mes-investissements.md` ne bloque jamais la fiche |

Aides internes : `_signaux_veille` (signaux de la dernière clôture, d'après `historique.csv`),
`_top30_veille`, `_suggestions_recentes` (titres suggérés les 3 jours précédents, pour varier),
`_prix_simple` (dernier cours d'un fonds à l'historique trop court pour les indicateurs).

### `verif.py` : contrôle croisé des prix
Usage : `python scripts/verif.py AAAA-MM-JJ`. Compare chaque prix Yahoo avec Boursorama et le
Financial Times (tolérance 1 %, 2 % à l'ouverture). Quantalys n'est pas interrogé : il bloque les robots.

| Fonction | Rôle |
|---|---|
| `nombre(txt, style)` | lit un nombre écrit à la française ou à l'anglaise |
| `get(url)` | requête polie : pause de 0,9 s, délai de 20 s, `None` en cas d'échec |
| `boursorama(code)` | dernier cours sur la page Boursorama (rejette les redirections vers la recherche) |
| `ft(genre, code)` | dernier cours sur la page « tearsheet » du Financial Times |
| `codes(m)` | traduit un ticker Yahoo en codes Boursorama et FT (place de cotation, ETF, indice, devise) |
| `main()` | ajoute sources, prix de référence (médiane) et statut `ok`, `ecart` ou `seul` à chaque titre |

### `fiches.py` : fiches détaillées
Usage : `python scripts/fiches.py AAAA-MM-JJ`. Ajoute `details` au JSON du jour pour chaque titre affiché.

| Fonction | Rôle |
|---|---|
| `lignes(t)` | découpe une page HTML en lignes de texte |
| `apres(L, motif, debut, exact)` | valeur qui suit une étiquette, en sautant les bulles d'aide |
| `lire_bourso(code, etf)` | caractéristiques sur Boursorama : ISIN, éligibilité PEA, SRI du DIC, frais, secteur, PER… |
| `lire_profil(code)` | page « société » de Boursorama : effectif, pays, site |
| `lire_yahoo(t)` | repli pour les titres absents de Boursorama |
| `infos(m)` | caractéristiques d'un titre, gardées 7 jours dans `data/fiches/` |
| `nombre(txt)` | « 157 569,38 MEUR » → 157569.38 |
| `compacte(s)` | historique compact : date de départ, écarts en jours, 5 chiffres significatifs |
| `r1(x, n)` | arrondi tolérant aux valeurs manquantes |
| `perte_max(s)` | pire baisse depuis un plus haut |
| `sri_estime(vol)` | SRI PRIIPs estimé d'après la volatilité (seuils 0,5 / 5 / 12 / 20 / 30 / 80 %) |
| `statistiques(sj, ss, cac)` | volatilités 1 et 5 ans, pires baisses, performances, bêta face au CAC 40, SRI estimé |
| `stats_seance(b, jour)` | prix moyen du jour (VWAP), plus haut et plus bas de la séance, d'après les barres de 5 min |
| `lien_yahoo(t)` | lien vers la page Yahoo Finance internationale (la française renvoie souvent 404) |
| `signaux_du_titre(t)` | historique des signaux du titre et leur résultat |
| `description_auto(m, inf)` | description de secours, construite à partir des caractéristiques |
| `frais(m, inf)` | frais de l'ETF, plafonds légaux du PEA, taxe sur les transactions financières |
| `main()` | construit les fiches et leurs liens (Boursorama, FT, Yahoo, DIC, justETF) |

### `rendu.py` et `modele.html` : le site et la note Obsidian
Usage : `python scripts/rendu.py AAAA-MM-JJ`. `modele.html` contient toute la page (styles,
animations, graphiques en SVG, fiche détaillée) ; `rendu.py` y insère les données du jour en JSON.

| Fonction | Rôle |
|---|---|
| `md_en_html(md)` | convertit l'analyse Markdown en HTML (titres, listes, gras) |
| `pct(x)`, `prix(x)`, `pct_simple(x)` | formats français des nombres pour la note |
| `note_obsidian(d, analyse, url)` | note du jour pour Obsidian : mes investissements, marchés, analyse, suggestions, top 30, petits prix, fiabilité, liens |
| `eur(x, signe)` | montant en euros à la française (« 1 234,56 € », « +12,30 € ») |
| `note_investissements(mes)` | partie « Mes investissements » de la note : total, une ligne par titre, codes à corriger |
| `note_suggestions(sugg)` | partie « Suggestions du jour » de la note, avec la raison de chaque suggestion |
| `risque_de(det)` | niveau de risque 1 à 7 du badge de la page principale (SRI officiel, sinon estimé) |
| `archives()` | page `docs/archives/` qui liste toutes les fiches |
| `main()` | écrit `docs/index.html`, l'archive du jour et la note ; ajoute la nouveauté du programme et l'état du dernier contrôle |

### `controle.py` : le contrôle qualité du chef d'orchestre
Usage : `python scripts/controle.py [--hors-ligne]`. Ne modifie rien sauf `pilotage/etat.json`.
Code de sortie : 0 vert, 1 orange, 2 rouge.

| Fonction | Rôle |
|---|---|
| `controle(nom, titre, niveau, resume, details)` | fabrique le résultat d'un contrôle |
| `pire(niveaux)` | niveau le plus grave : ok < non vérifiable < alerte < problème |
| `lire(chemin)` | lit un fichier, texte vide s'il n'existe pas |
| `c_tests()` | lance `tests.py` |
| `fiche_attendue(maintenant)` | quelle fiche devrait être en ligne à cette heure (avec des marges) |
| `c_fraicheur(d, maintenant)` | la dernière fiche est-elle celle attendue, et la clôture postérieure au fixing ? |
| `anomalies_donnees(d)` | prix impossibles, RSI hors de 0-100, top 30 incomplet, moins de 8 ETF, petits prix ≥ 2 €, cours pas datés du jour… |
| `c_donnees(d)` | résume `anomalies_donnees` et le contrôle entre sources |
| `chiffres_incoherents(analyse, d)` | variations citées en gras dans l'analyse qui ne collent pas aux données |
| `c_analyse(d)` | analyse présente, 6 parties, longueur, aucune formulation de conseil, chiffres justes |
| `telecharger(url)` | requête polie (même pause que `verif.py`), `None` si le site est injoignable |
| `robots_autorise(url)` | respecte `robots.txt` avant d'ouvrir une page |
| `cours_comparables(d, maintenant)` | vrai si aucune séance n'a eu lieu depuis la clôture de la fiche |
| `c_prix(d, maintenant, n)` | revérifie 8 prix tirés au sort sur Boursorama |
| `verifier_lien(lib, url, info)` | un lien de fiche : page existante, bon titre (ISIN ou symbole), robots.txt respecté |
| `c_liens(d, k)` | tous les liens de 8 titres tirés au sort chaque jour (dont 4 ETF) |
| `donnees_de_page(html)` | extrait les données JSON d'une page de la fiche |
| `c_page_depot(d)` | `docs/index.html` montre-t-elle la dernière fiche ? |
| `c_site(d)` | le site en ligne montre-t-il la dernière fiche ? |
| `fonctions_publiques(chemin)` | liste les fonctions d'un script |
| `manques_documentation(archi, scripts)` | scripts et fonctions absents de ce document |
| `c_documentation(d, maintenant)` | ce document, les notes, archives et analyses de chaque jour, les journaux de nuit |
| `agent_du_commit(message)` | reconnaît l'agent d'après le message de commit |
| `ecarts_aux_regles(agent, fichiers, jour_commit, dernier_jour)` | fichiers hors du rôle de l'agent, données passées modifiées, suppressions, taille du changement |
| `git(*args)` | lance une commande Git dans le dépôt |
| `c_agents(d, heures)` | relit les commits des 30 dernières heures |
| `resume_court(controles, etat)` | phrase affichée en bas de la fiche |
| `main()` | enchaîne les contrôles, écrit `pilotage/etat.json`, affiche le résumé |

### `tests.py` : les garde-fous
Usage : `python scripts/tests.py` (sans réseau, quelques secondes). Aucun agent ne publie de code
si un test échoue. Chaque nouvelle fonction de calcul doit avoir son test.
La syntaxe JavaScript de la page est vérifiée avec `node --check` dans le cloud, ou avec
JavaScriptCore (`jsc`, présent sur tous les Mac) en local.

## Techniques à retenir

- **Données du jour seulement** : la clôture n'est utilisée qu'une fois le fixing de 17 h 35 publié
  (métadonnées `regularMarketTime` du graphique Yahoo, qui ne demandent pas de « crumb »).
- **Prix moyen du jour (VWAP)** : somme de (prix typique × volume) / somme des volumes, barres de 5 min.
- **Risque SRI** : officiel (DIC PRIIPs, lu sur Boursorama) pour les ETF, estimé d'après la volatilité pour les actions.
- **Contrôle croisé** : médiane de trois sources, tolérance 1 % (2 % en séance). Les suggestions et les
  investissements de Mathieu sont contrôlés comme le reste.
- **Suggestions** : règles fixes et publiées, une raison chiffrée par titre, jamais « achète » ni
  « vends » ; elles signalent des titres à regarder, ce ne sont pas des recommandations.
- **Mes investissements** : prix de revient pondéré par les quantités ; un achat du jour compte depuis
  son prix d'achat, pas depuis la clôture de la veille ; frais de courtage non compris.
- **Politesse** : une requête par seconde au plus, `robots.txt` respecté, caches pour limiter les appels,
  aucune protection anti-robot contournée.
- **Page autonome** : données JSON compactes intégrées à la page (`<script id="donnees">`), aucun
  appel réseau à l'ouverture, sauf les polices.
- **Contourner le cache** de GitHub Pages pour vérifier une mise à jour : ajouter `?v=<commit>` à l'adresse.
- **Garde-fous** : tests obligatoires, filet de sécurité (annulation d'une amélioration de la nuit qui
  casse la fiche), règles de rôle par agent vérifiées par `controle.py`.
