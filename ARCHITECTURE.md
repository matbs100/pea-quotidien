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
                  Claude écrit data/analyses/AAAA-MM-JJ.md (7 parties dont l'actualité et les estimations, 450 mots au plus ; revue de presse dans data/presse/)
                                         ▼
                rendu.py + modele.html ──► docs/ (site GitHub Pages)  et  notes/ (Obsidian)
                                         ▼
                 git push ──► GitHub Pages (≈ 1 min) ──► notification ntfy sur le téléphone
```

« Mes investissements » : le propriétaire tape un ISIN ou un nom dans la barre de recherche de la fiche ; ses
achats restent dans son navigateur (`localStorage`, rien n'est publié) et la page calcule leur évolution
avec le catalogue des titres suivis (prix du jour de `collecte.py`, ISIN ajouté par `fiches.py`). Les
achats notés dans `mes-investissements.md` sont, eux, calculés par `collecte.py`. Les « Suggestions du
jour » sont choisies par des règles chiffrées. La barre trouve aussi les **fonds de la liste Wealins**
(supports d'assurance vie, environ 1 350) : `wealins.py` relit la liste une fois par jour
(`data/wealins.json`) et `rendu.py` l'ajoute à la page ; un fonds a pour prix sa dernière valeur
liquidative, avec sa date.

Tout tourne dans le cloud (routines Claude Code) : le Mac peut être éteint. Le dépôt est rangé
dans le coffre Obsidian, donc un `git pull` sur le Mac suffit à tout y amener.

## L'équipe d'agents

| Heure (Paris) | Agent | Consigne | Rôle |
|---|---|---|---|
| 1 h 30, chaque nuit | **Design** | `DESIGN.md` | étude de marché quotidienne du design (GitHub, sites originaux, galeries d'artefacts Claude, thèmes Shopify, vidéos et fils YouTube, TikTok, X, Reddit : seulement ce qui est lisible sans contourner d'anti-robot), catalogue de motifs dans `apprentissage/design/`, une amélioration de l'apparence de la page au plus (« Design : … [D-…] »), prouvée sans perte d'information par `design.py` ; relu par le chef à 5 h |
| 3 h, chaque nuit | **Veille et amélioration** | `AMELIORATION.md` | apprend (marchés, design, pédagogie, open source), note ce qu'il apprend dans `apprentissage/`, fait une amélioration testée |
| 4 h, chaque jour | **Vérificateur du code** | `VERIFICATION.md` | sous la direction du chef : confidentialité du propriétaire (`confidentialite.py`, avec la clé secrète de la routine), tests, contrôle, analyse statique (`ruff`) et failles des bibliothèques (`pip-audit`), revue des commits du jour, une correction au plus (« Code : … [correctif] »), apprentissage quotidien dans des sources fiables (`apprentissage/code/`), idées ; rapport dans `pilotage/code/` |
| 5 h, chaque jour | **Chef d'orchestre** | `CHEF.md` | contrôle tout (`controle.py`), vérifie les faits appris, relit les commits des autres, annule ce qui casse, corrige un bug ou embellit l'interface, écrit `pilotage/` |
| 12 h 30, jours de bourse | **Chef d'orchestre, passage de mi-journée** | routine dédiée (lit `CHEF.md`) | vérifie la fiche d'ouverture, la refait et corrige le programme si besoin, s'assure que la clôture pourra tourner ; pas d'embellissement |
| 9 h 15 et 17 h 55, jours de bourse | **Fiche du jour** | `ROUTINE.md` | collecte, contrôle des prix, fiches détaillées, analyse, site, notification |
| samedi à 4 h 20 | **Mise à jour des titres suivis** | `UNIVERS.md` | ajoute à `univers.json` les nouveaux ETF éligibles au PEA et les actions entrées dans le CAC 40, le SBF 120 ou l'Euro Stoxx 50, chacun vérifié (Yahoo, Boursorama) ; 20 ajouts au plus ; signale sans les supprimer les titres qui ne cotent plus |
| 9 h 40 et 18 h 40, si le Mac est allumé | **Relais du Mac** | tâche planifiée de l'appli Claude | `git pull` dans Obsidian, vérifie le site en ligne, recopie l'essentiel dans les notes ; renvoie depuis le Mac la notification que ntfy a refusée au cloud (`pilotage/notification.json`, quota gratuit compté par adresse Internet, partagée dans le cloud) |

Les agents ne se parlent pas directement : ils communiquent par des fichiers du dépôt.
- `pilotage/consignes.md` : les consignes du chef, que les autres agents lisent en premier ;
- `pilotage/etat.json` : le dernier contrôle, affiché en bas de la fiche ;
- `pilotage/verifie.json` : les alertes 🟠 que le chef a vérifiées lui-même (preuve à l'appui), comptées ✔ par le contrôle pour ce jour ou ce commit seulement ;
- `pilotage/rapports/` : un rapport du chef par jour ;
- `apprentissage/` : ce que l'agent de nuit apprend (journal, idées, connaissances) ;
- `apprentissage/design/` et `pilotage/design/` : l'étude de marché, le catalogue de motifs, la mémoire (`lecons.md`) et le journal de l'agent design ; les souhaits du propriétaire (`souhaits.md`, recopiés par la fonction mémoire) et les déplacements déclarés (`deplacements.json`) ;
- `pilotage/decision.md` et `pilotage/decisions.md` : **la méthode de décision** et son journal. Tous les
  agents proposent des idées (notées avec la grille : utilité, résultats, visuel, avantage de la nouveauté,
  fiabilité ; coût et risque à part) ; le chef décide chaque matin (adoptée, à l'essai, en attente,
  rejetée), l'agent de nuit ou le chef réalise, et le chef mesure le résultat trois jours de bourse plus
  tard (gardée, à ajuster, annulée). Le propriétaire a autorisé (06/11/2026) l'adoption sans sa validation de ce
  que la méthode juge utile ; chaque commit d'amélioration cite sa décision (`[D-…]`).

Les consignes sont dans `ROUTINE.md`, `AMELIORATION.md`, `CHEF.md`, `UNIVERS.md`, `VERIFICATION.md` et `DESIGN.md` : depuis le 06/11/2026,
chaque routine dit seulement « lis ce fichier et applique-le » (la routine de la fiche garde en plus
l'adresse de notification, qui ne doit pas être dans le dépôt public). Pour changer une consigne, il
suffit donc de modifier le fichier. Les agents ne modifient jamais ces fichiers : si une routine voit
qu'un agent l'a fait, elle applique la version d'avant. Seul le propriétaire (avec Claude) les change.

## Les fichiers

| Chemin | Contenu |
|---|---|
| `univers.json` | les titres suivis, par catégorie (indices, devises, matières, ETF, ETF à effet de levier, actions, petits prix). Les ETF de `etf_levier` sont traités comme des ETF (fiche, contrôle des prix, recherche) mais restent hors du top 30 et des suggestions, et portent un avertissement |
| `descriptions.json` | courtes descriptions des titres, rédigées sans copier de site |
| `guide/` | notes pour le propriétaire (dans Obsidian) : ce qui a été ajouté et comment s'en servir. Les agents ne les modifient pas |
| `mes-investissements.md` | autre façon de noter les achats du propriétaire (code Yahoo ou ISIN, date, prix, quantité, type), un par ligne de tableau, pour les retrouver dans Obsidian. Tenu par le propriétaire seul : les agents le lisent mais ne le modifient jamais (`controle.py` le signale). Public, comme tout le dépôt, contrairement à la barre de recherche |
| `config.json` | adresse du site et du dépôt (ne pas changer) |
| `data/jours/` | une capture JSON par jour (écrasée à la clôture) |
| `data/analyses/` | l'analyse écrite par Claude, une par jour |
| `data/historique.csv`, `data/signaux.csv` | historique des cours de clôture et des signaux, jugés 5 séances plus tard |
| `data/correspondances.json`, `data/fiches/` | caches : codes Boursorama / FT trouvés, caractéristiques des titres (7 jours) |
| `data/wealins.json` | les fonds de la liste Wealins (nom, ISIN, devise, dernière valeur liquidative et sa date, valeur précédente), un par ligne, relus une fois par jour par `wealins.py` |
| `docs/` | le site : `index.html` (dernière fiche) et `archives/` |
| `notes/` | une note Obsidian par jour |
| `apprentissage/` | journal de nuit, idées, connaissances, veille GitHub, nouveautés, crédits |
| `apprentissage/lectures/` | les fiches de lecture des agents (une par PDF lu : lien, résumé, chiffres avec leur page, idées) et la bibliothèque `README.md` |
| `pilotage/sources-verifiees.md` | les sites où les agents peuvent lire des PDF (organismes officiels, bourses, indices, émetteurs, recherche), avec leur `robots.txt` lu et l'état du réseau du cloud |
| `pilotage/` | consignes, état et rapports du chef d'orchestre ; `decision.md` (la méthode de décision des améliorations : grille, seuils, vetos, bilans) et `decisions.md` (le journal des décisions, une ligne par décision avec son identifiant `D-AAAAMMJJ-n`) ; école, méthodes, pistes de fonds |
| `scripts/` | le programme (ci-dessous) |

## Les scripts, fonction par fonction

### `collecte.py` : cours, indicateurs, classement, signaux, suggestions, mes investissements
Usage : `python scripts/collecte.py [AAAA-MM-JJ] [ouverture|cloture]`. Codes de sortie : 0 OK,
3 cours du jour (ou clôture définitive) pas encore publiés, 4 Bourse fermée.

| Fonction | Rôle |
|---|---|
| `telecharger(tickers)` | télécharge 14 mois de cours quotidiens pour tous les titres en un seul appel Yahoo |
| `devise_de(t)` | devise de cotation d'un titre d'après sa place (EUR, DKK, SEK, NOK), affichée à côté de chaque prix |
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
| `mes_investissements(entrees, mesure_de, categories, jour)` | regroupe les achats par titre : prix de revient, évolution depuis l'achat, valeur, plus-value et variation du jour en euros si les quantités sont notées, total ; un ISIN qui n'est pas suivi est cherché dans la liste Wealins (fonds) ; codes introuvables listés dans `erreurs` |
| `catalogue(res)` | tous les ETF et actions suivis, avec leur prix du jour : la liste où cherche la barre de recherche « Mes investissements » |
| `suggestions(candidats, top30, signaux_veille, top30_veille, deja, n)` | jusqu'à 5 actions à regarder, une par règle : nouveau signal « hausse », entrée dans le top 30, plus haut sur un an, repli (RSI < 40) au-dessus de la moyenne 200 jours, variation d'au moins 3 % ; chacune avec sa raison chiffrée |
| `paques(annee)` | date de Pâques (algorithme de Meeus) |
| `bourse_fermee(j)` | jours de fermeture d'Euronext : week-end, 1er janvier, Vendredi saint, lundi de Pâques, 1er mai, 25 et 26 décembre |
| `attendre_seance(jour, max_minutes)` | attend que Yahoo publie la séance du jour (décalage de 15 min) |
| `enregistrer(jour, tous, top30, petites, res)` | à la clôture : juge les anciens signaux, note ceux du jour, complète l'historique |
| `cloture_dans_meta(m, jour)` | vrai si les métadonnées Yahoo montrent un dernier échange du jour, après la fin de séance + 5 min |
| `cloture_publiee(jour)` | vérifie la clôture définitive (fixing de 17 h 35) sur deux titres témoins |
| `attendre_cloture(jour, max_minutes)` | attend la clôture définitive, une vérification par minute |
| `main()` | enchaîne tout et écrit `data/jours/AAAA-MM-JJ.json` ; une erreur dans les suggestions ou dans `mes-investissements.md` ne bloque jamais la fiche |

Aides internes : `_isins_connus` (ISIN → code Yahoo, d'après le cache `data/fiches/`, pour accepter un
ISIN dans `mes-investissements.md`), `_signaux_veille` (signaux de la dernière clôture, d'après `historique.csv`),
`_top30_veille`, `_suggestions_recentes` (titres suggérés les 3 jours précédents, pour varier),
`_prix_simple` (dernier cours d'un fonds à l'historique trop court pour les indicateurs),
`_actualiser_wealins` et `_fonds_wealins` (lecture de la liste Wealins dans un fil parallèle, puis du cache,
sans jamais bloquer la fiche).

### `verif.py` : contrôle croisé des prix
Usage : `python scripts/verif.py AAAA-MM-JJ`. Compare chaque prix Yahoo avec Boursorama et le
Financial Times (tolérance 1 %, 2 % à l'ouverture). Quantalys n'est pas interrogé : il bloque les robots.

| Fonction | Rôle |
|---|---|
| `nombre(txt, style)` | lit un nombre écrit à la française ou à l'anglaise |
| `get(url)` | requête polie : pause de 0,9 s, délai de 20 s, `None` en cas d'échec |
| `boursorama(code)` | dernier cours sur la page Boursorama (rejette les redirections vers la recherche) |
| `ft(genre, code)` | dernier cours sur la page « tearsheet » du Financial Times |
| `date_bourso(page)` / `date_ft(page)` | date du dernier cours affiché par la page Boursorama / FT |
| `boursorama_date(code)` / `ft_date(genre, code)` | cours et date du cours (les deux fonctions sans `_date` ne renvoient que le cours) |
| `source_perimee(date_source, jour, date_yahoo)` | règle du propriétaire (06/11) : une source qui ne donne que le cours d'un jour précédent est écartée (notée dans `sources_perimees`) ; si Yahoo n'a pas encore de cours du jour, la dernière séance compte |
| `codes(m)` | traduit un ticker Yahoo en codes Boursorama et FT (place de cotation, ETF, indice, devise) |
| `verif_fonds(m, tol)` | contrôle d'un fonds Wealins : compare les valeurs de même date (Wealins, FT) ; une source plus ancienne que la plus récente est écartée |
| `main()` | ajoute sources, prix de référence (médiane) et statut `ok`, `ecart` ou `seul` à chaque titre (fonds Wealins : `verif_fonds`, sans nouvelle requête) |

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
| `fichier_cache(t)` | fichier de `data/fiches/` d'un titre |
| `isin_en_cache(t)` | ISIN d'un titre d'après le cache, même périmé (un ISIN ne change pas) |
| `nombre(txt)` | « 157 569,38 MEUR » → 157569.38 |
| `compacte(s)` | historique compact : date de départ, écarts en jours, 5 chiffres significatifs |
| `r1(x, n)` | arrondi tolérant aux valeurs manquantes |
| `perte_max(s)` | pire baisse depuis un plus haut |
| `sri_estime(vol)` | SRI PRIIPs estimé d'après la volatilité (seuils 0,5 / 5 / 12 / 20 / 30 / 80 %) |
| `ratios_rendement(rs, periodes)` | ratios de Sharpe et de Sortino (taux sans risque 0) ramenés à l'année ; None sous 30 points |
| `statistiques(sj, ss, cac)` | volatilités 1 et 5 ans, pires baisses, performances, bêta face au CAC 40, Sharpe et Sortino (dès 2 ans), SRI estimé |
| `stats_seance(b, jour)` | prix moyen du jour (VWAP), plus haut et plus bas de la séance, d'après les barres de 5 min |
| `lien_yahoo(t)` | lien vers la page Yahoo Finance internationale (la française renvoie souvent 404) |
| `signaux_du_titre(t)` | historique des signaux du titre et leur résultat |
| `description_auto(m, inf)` | description de secours, construite à partir des caractéristiques |
| `frais(m, inf)` | frais de l'ETF, plafonds légaux du PEA, taxe sur les transactions financières |
| `fiche_fonds_wealins(m)` | fiche d'un fonds Wealins noté dans `mes-investissements.md` : historique de la valeur liquidative (jusqu'à 5 ans, page du fonds), statistiques, SRI estimé, gestionnaire, SFDR, lien du DIC |
| `main()` | construit les fiches et leurs liens (Boursorama, FT, Yahoo, DIC, justETF) ; ajoute l'ISIN de chaque titre du catalogue (60 titres jamais lus au plus par passage, pour compléter peu à peu sans ralentir la fiche) |

### `wealins.py` : les fonds de la liste Wealins
Usage : `python scripts/wealins.py [--forcer]` (`collecte.py` l'appelle aussi, dans un fil parallèle qui
ne bloque jamais la fiche). Source : https://www.wealins.com/funds-list/ (135 pages de 10 fonds ; robots.txt
lu le 06/11/2026 : tout est autorisé). Une requête par seconde, 3 à 4 minutes par lecture complète. Le réseau
du cloud doit autoriser `www.wealins.com` ; sinon le cache reste tel quel (le Mac peut le remplir).

| Fonction | Rôle |
|---|---|
| `lire_liste(page)` | fonds d'une page de la liste : ISIN, nom, date de valeur, devise, valeur, SFDR |
| `nb_pages(page)` | nombre de pages, d'après la pagination |
| `lire_fonds(page)` | page d'un fonds : valeur et date, performance depuis le 1er janvier, gestionnaire, SFDR, devise, DIC en français, historique |
| `url_fonds(isin)`, `url_ft(isin, devise)` | pages du fonds chez Wealins et au Financial Times |
| `charger()` | contenu de `data/wealins.json` (vide s'il n'existe pas) |
| `enregistrer(c)` | écrit le cache d'un coup (fichier temporaire puis renommage), un fonds par ligne |
| `fusionner(c, nouveaux, vu_le)` | ajoute les fonds lus ; l'ancienne valeur devient la valeur précédente quand la date avance |
| `date_dominante(c)` | date de valeur la plus fréquente du cache |
| `jour_ouvre_precedent(j)` | jour ouvré précédent (week-ends sautés) |
| `a_actualiser(c, maintenant)` | une lecture par jour ; une seconde (après 4 h) si la première n'avait pas les valeurs de la veille |
| `actualiser(forcer, max_minutes)` | relit toute la liste si besoin et met le cache à jour ; ne lève jamais d'erreur |
| `variation(f)` | variation entre la valeur précédente et la dernière |
| `mesure(isin, c, ft)` | prix d'un fonds pour « Mes investissements » : la valeur la plus récente entre Wealins et le FT (règle du propriétaire), avec les deux sources dans `sources_vl` |
| `catalogue_page(c, exclus)` | fonds pour la barre de recherche : `[isin, nom, devise, valeur, date, variation]` |

### `lectures.py` : les PDF lus par les agents (bibliothèque)
Usage : `python scripts/lectures.py telecharger <url>`, `lire <chemin> [1-10]`, `note <url> "<titre>" "<organisme>" [date] [nuit|chef]`, `index`.
Les agents ne lisent des PDF que sur les sites de `pilotage/sources-verifiees.md` ; le PDF reste dans
`/tmp/lectures/` (jamais dans le dépôt public : droits d'auteur), et chaque lecture donne une fiche dans
`apprentissage/lectures/` (lien, résumé avec ses propres mots, chiffres avec leur page, idées).

| Fonction | Rôle |
|---|---|
| `domaines_verifies(texte)` | domaines de la table de `pilotage/sources-verifiees.md` |
| `est_verifie(url, domaines)` | lien en https sur un domaine exact de la liste (un domaine imité est refusé) |
| `robots_permet(statut, texte, url, agent)` | règle du `robots.txt` (401 ou 403 : tout interdit ; absent : tout permis) |
| `telecharger(url, domaines, dossier, max_mo)` | vérifie source, `robots.txt`, redirection, type et taille (30 Mo), puis enregistre le PDF hors du dépôt |
| `pages_demandees(spec, total, maxi)` | « 3-8 » → numéros de pages, bornés au document et à 30 pages |
| `texte(chemin, spec)` | texte des pages demandées (pypdf), chaque page précédée de son numéro ; jamais enregistré |
| `slug(texte, n)` | nom de fichier à partir d'un titre |
| `nouvelle_note(url, titre, organisme, publie_le, auteur, jour, dossier)` | crée la fiche de lecture à remplir (ne remplace jamais une fiche existante) |
| `mots_resume(texte)` | nombre de mots du résumé d'une fiche (sans la consigne) |
| `lire_notes(dossier)` | en-têtes des fiches de lecture et longueur de leur résumé |
| `index(notes)`, `ecrire_index(dossier)` | la bibliothèque `apprentissage/lectures/README.md`, de la plus récente à la plus ancienne |
| `defauts(notes, domaines, texte_index, jour, debut, jours_sans_lecture)` | ce que le contrôle signale : champ manquant, lien hors liste, résumé hors de 80 à 300 mots, fiche absente de la bibliothèque, aucune lecture depuis 3 jours |

### `rendu.py` et `modele.html` : le site et la note Obsidian
Usage : `python scripts/rendu.py AAAA-MM-JJ`. `modele.html` contient toute la page (styles,
animations, graphiques en SVG, fiche détaillée, barre de recherche « Mes investissements » avec ses
calculs) ; `rendu.py` y insère les données du jour en JSON. Les achats saisis dans la barre sont gardés
dans le navigateur (clé `matin-pea:investissements` du `localStorage`) : ils ne sont ni publiés, ni lus
par les agents. Dans le graphique, la moyenne courte est en tirets et la longue en pointillés (lisible sans la couleur, notamment pour les daltoniens ; test `moyennes_mobiles_traits_distincts`).

| Fonction | Rôle |
|---|---|
| `md_en_html(md)` | convertit l'analyse Markdown en HTML (titres, listes, gras) |
| `pct(x)`, `prix(x)`, `pct_simple(x)` | formats français des nombres pour la note |
| `note_obsidian(d, analyse, url)` | note du jour pour Obsidian : mes investissements, marchés, analyse, suggestions, top 30, petits prix, fiabilité, liens |
| `eur(x, signe)` | montant en euros à la française (« 1 234,56 € », « +12,30 € ») |
| `montant(x, m, signe)` | montant d'une ligne dans sa devise (« 473,16 USD » hors euros) |
| `note_investissements(mes)` | partie « Mes investissements » de la note : total, une ligne par titre, codes à corriger |
| `note_suggestions(sugg)` | partie « Suggestions du jour » de la note, avec la raison de chaque suggestion |
| `risque_de(det)` | niveau de risque 1 à 7 du badge de la page principale (SRI officiel, sinon estimé) |
| `simulation_mensuelle(serie, mensuel, ans)` | simulateur pédagogique « 50 € par mois » sur 5 ans au plus, d'après la série hebdomadaire ; None sous 2 ans d'historique (bloc « Et si j'avais investi régulièrement ? ») |
| Bloc `#sec-fisc` (`modele.html`) | « PEA : fiscalité en un coup d'œil » : plafond 150 000 €, 12,8 % avant 5 ans, 18,6 % de prélèvements sociaux, 0 % d'impôt sur le revenu après 5 ans ; texte fixe avec date de relecture (13/11/2026) et liens service-public ; test `bloc_fiscalite_pea` (D-20261113-3) |
| `filtrerCriteres(liste, c, det)` (JavaScript, `modele.html`) | filtre le Top 30 selon « Mes critères » : type, risque maximum, baisse maximale sur 1 an ; un titre sans la donnée n'est pas retenu ; critères gardés dans `localStorage` |
| `rendementsMensuels(serie)` et `blocMois(det)` (JavaScript, `modele.html`) | carte de chaleur « Mois par mois » de la fiche d'un titre : rendement de chaque mois civil (dernière clôture hebdomadaire du mois contre celle du mois précédent) sur 5 ans au plus, une ligne par année ; vert pour une hausse, rouge pour une baisse, intensité selon l'écart (D-20261106-6) |
| `aligner100(ptsA, serieB)` et `comparer()` (JavaScript, `modele.html`) | comparaison de deux titres dans le graphique de la fiche : menu « Comparer avec… », les deux séries ramenées à 100 au premier jour de la période (B : dernier cours connu à chaque date de A) ; bandeau « ni prévision ni conseil » (D-20261106-7) |
| `ecartesSansDonnee(liste, c, det)` (JavaScript, `modele.html`) | compte les titres du Top 30 écartés par « Mes critères » parce que le risque ou la baisse sur 1 an manque ; le bilan du filtre l'annonce (D-20261109-2) |
| `TARIF`, `fraisDe(m)`, `couts(m, M)`, `fraisCourt(m)`, `blocFrais(m)` (JavaScript, `modele.html`) | frais de chaque titre : gestion (ETF : `fx.g` du catalogue ou `details.frais` ; action : 0 ; OPCVM : `frais_courants`), courtage BNP Bourse Start plafonné à 0,5 %, TTF, garde, total sur 1 an pour 100 / 500 / 1 000 € |
| `deviseDe(m)`, `dev(m)` (JavaScript) | devise de chaque cours : `m.devise`, sinon d'après la place du code Yahoo ; « pts » pour un indice ; `UNITE` pour devises et matières premières |
| `opcvm.json`, `scripts/opcvm.py` | OPCVM éligibles au PEA (frais et SRI relevés dans les DIC, avec source et date) ; `mesurer_tout()` lit la valeur liquidative (Yahoo par ISIN, puis FT), garde la dernière dans `data/opcvm.json` ; appelé par `collecte.py`, liste `opcvm` de la fiche du jour; `liste()` (fonds du fichier, `[]` si absent ou illisible), `charger_cache()` (dernières valeurs liquidatives, `{"vl": {}}` si absent), `mesures_serie()` (valeur, date et variations d'une série pandas), `lire_ft()` (valeur et date lues sur le Financial Times, `(None, None)` en cas d'échec) |
| `scripts/taux.py` | Taux directeurs de la BCE (dépôt, refinancement, prêt marginal) lus sur data-api.ecb.europa.eu, cache `data/taux_bce.json` ; appelé par `rendu.py` (clé `taux_bce`), encadré « Le contexte des taux » ; `dernier_changement()` (valeur en vigueur, date d'effet, valeur précédente), `lire_csv()` (points d'un CSV BCE), `charger_cache()` (dernier relevé, `{}` si absent), `mesurer()` (lecture, cache si échec) |
| `fiches.frais_compact`, `ajouter_frais_catalogue` | frais `fx` de chaque titre du catalogue, depuis le cache `data/fiches/` (sans réseau) ; `python scripts/fiches.py --frais AAAA-MM-JJ`; `infos_en_cache()` (caractéristiques du cache `data/fiches/`, même périmées, `{}` sinon) alimente `frais_compact` |
| `empreintes_scripts(page)` | empreintes SHA-256 des scripts exécutables de la page, insérée dans la politique de sécurité (CSP) à la place de `'__EMPREINTE_SCRIPT__'` |
| `ETF_INDICE`, `etfIndice(t)`, `prixEtf(m)` (JavaScript, `modele.html`) | à côté de chaque indice, prix d'une part du premier ETF éligible au PEA de la table `ETF_INDICE` qui a un cours (avec sa date si elle n'est pas celle de la fiche) ; dans la fiche de l'indice, bouton vers la fiche de l'ETF |
| boutons `#chips-top` (JavaScript, `modele.html`) | filtre ETF / Actions du Top 30 (les petites capitalisations comptent comme actions) ; la règle CSS `.ligne[hidden]` est indispensable |
| `date_vl(m)` | « (valeur du 05/11) » après le prix d'un fonds dans la note |
| `prix_dev(x, m)` | prix suivi de la devise du titre dans la note (« 6,177 EUR ») ; sans devise pour un indice |
| `fonds_wealins(d)` | fonds de `data/wealins.json` pour la barre de recherche, en tableaux compacts, sans ceux que la fiche suit déjà |
| `archives()` | page `docs/archives/` qui liste toutes les fiches |
| `donnees_du_jour(jour)` | données de la fiche complétées comme la page les lit (analyse en HTML, courbes raccourcies, nouveauté, état du contrôle, risque, simulation, taux BCE) ; renvoie `(d, analyse)` |
| `page_html(d, modele)` | page autonome : le modèle (`scripts/modele.html` par défaut, ou un texte donné, par exemple une ancienne version pour `design.py rendre`) rempli avec les données, avec les empreintes CSP |
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
| `lire_verifications()` | entrées valides de `pilotage/verifie.json` (texte de l'alerte, jour ou commit, preuve de 20 caractères au moins) |
| `appliquer_verifications(alertes, jour, verifs)` | sépare les alertes restantes de celles vérifiées par le chef pour ce jour ou ce commit (jamais un 🔴) |
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
| `c_liens(d, k)` | tous les liens de 8 titres tirés au sort chaque jour (dont 4 ETF) ; un lien Yahoo en 404 depuis le cloud n'est pas « cassé » si le symbole a des cours collectés |
| `donnees_de_page(html)` | extrait les données JSON d'une page de la fiche |
| `c_page_depot(d)` | `docs/index.html` montre-t-elle la dernière fiche ? |
| `c_site(d)` | le site en ligne montre-t-il la dernière fiche ? |
| `fonctions_publiques(chemin)` | liste les fonctions d'un script |
| `manques_documentation(archi, scripts)` | scripts et fonctions absents de ce document |
| `c_documentation(d, maintenant)` | ce document, les notes, archives et analyses de chaque jour, les journaux de nuit |
| `agent_du_commit(message)` | reconnaît l'agent d'après le message de commit (fiche, nuit, chef, univers pour la tâche du samedi) |
| `message_affiche(message)` | message de commit recopié dans `pilotage/etat.json` (public) : sans le préfixe d'un commit du propriétaire |
| `ecarts_aux_regles(agent, fichiers, jour_commit, dernier_jour)` | fichiers hors du rôle de l'agent, données passées modifiées, suppressions, taille du changement |
| `jour_de_reference(jours, jour_commit)` | dernière fiche existante au moment d'un commit : la régénérer est permis, pas les plus anciennes |
| `git(*args)` | lance une commande Git dans le dépôt |
| `c_agents(d, heures)` | relit les commits des 30 dernières heures |
| `lire_decisions(texte)` | lignes du journal `pilotage/decisions.md` (identifiant → colonnes) |
| `gains_incoherents(texte_idees)` | idées dont le « Gain » ne suit pas la grille (moyenne pondérée 30/25/20/15/10 %) |
| `jours_ouvres_entre(debut, fin)` | jours de semaine entre deux dates |
| `bilans_en_retard(decisions, jour, delai)` | décisions réalisées depuis 3 jours ouvrés et toujours sans bilan |
| `commit_sans_decision(agent, message, chemins, decisions)` | commit d'agent qui change le programme sans citer une décision connue (`[D-…]`) |
| `c_lectures(d)` | contrôle « Lectures des agents » (voir `lectures.defauts`) ; un PDF ajouté au dépôt par un agent est un problème (dans `ecarts_aux_regles`) |
| `c_decisions(d, heures)` | contrôle « Méthode de décision » : bilans en retard, gains mal calculés, améliorations sans décision (commits depuis le 07/11/2026) |
| `c_confidentialite(d, heures)` | contrôle « Confidentialité » : aucune information personnelle dans les fichiers publiés (🔴) ni dans les commits récents (🟠) ; voir `confidentialite.py` |
| `c_design(heures)` | contrôle « Design : aucune information retirée » : pour chaque commit des 30 dernières heures qui touche `scripts/modele.html` (tout agent), `design.comparer_modeles` entre la version d'avant et celle du commit ; un titre, un champ de données, un identifiant ou un avertissement retiré sans déplacement déclaré, un contraste sous 4,5 ou un nouveau site externe chargé (`src`, `<link href>` ; un lien `<a href>` vers une source n'en charge aucun) = 🔴 ; un texte reformulé, des textes sous 12 px, une page bien plus lourde = 🟠 |
| `resume_court(controles, etat)` | phrase affichée en bas de la fiche |
| `main()` | enchaîne les contrôles, écrit `pilotage/etat.json`, affiche le résumé |

### `design.py` : le garde-fou de l'agent design (aucune information retirée)
Usage : `python3 scripts/design.py inventaire [REF]`, `comparer AVANT [APRES]` (codes 0 / 1 / 2),
`rendre AVANT [APRES] [--jour=J] [--dossier=D]`. Un déplacement volontaire se déclare dans
`pilotage/design/deplacements.json` (`commit`, `retire`, `nouveau`, `raison`) ; il n'est accepté que si le nouvel élément existe.

| Fonction | Rôle |
|---|---|
| `git(*args)` | commande Git dans le dépôt, texte de sortie |
| `lire_modele(ref)` | `scripts/modele.html` du fichier de travail, ou d'un commit (`git show`) |
| `texte_visible(fragment)` | morceaux de texte visibles d'un fragment HTML (sans scripts ni styles) |
| `cles_des_donnees()` | noms des champs des données de la dernière fiche, plus ceux ajoutés par `rendu.py` |
| `inventaire(modele, cles)` | ce que la page montre ou lit : titres (h1–h4 et `bloc("…")`), identifiants, champs de données lus par le JavaScript, textes visibles, avertissements « pas un conseil » |
| `contraste(c1, c2)` | rapport de contraste WCAG entre deux couleurs hexadécimales (1 à 21) |
| `mesures(modele)` | taille, contraste minimal des couleurs de texte sur les fonds (clair et sombre), textes sous 12 px, boutons sans nom, images sans `alt`, sites externes, nombre de sections |
| `deplacements_acceptes(commit)` | déplacements déclarés pour un commit dans `pilotage/design/deplacements.json` |
| `comparer_modeles(avant, apres, commit, cles)` | `(niveau, lignes)` : 0 rien de retiré, 1 à revoir, 2 information retirée ou page dégradée |
| `rendre(avant, apres, jour, dossier)` | construit les deux pages avec les mêmes données (`rendu.donnees_du_jour`, `rendu.page_html`) ; avec Playwright (facultatif, installé pour la séance) : captures téléphone et ordinateur, et nombres ou mots affichés avant et plus après |
| `main()` | ligne de commande |

### `confidentialite.py` : aucune information personnelle dans le dépôt public
Usage : `python3 scripts/confidentialite.py [--site] [--commits N] [--json]` (N = 0 : tout l'historique) ;
`--empreinte "terme"` calcule l'empreinte d'un nouveau terme protégé. Ne modifie rien. Code de sortie :
0 rien, 1 points à revoir, 2 information personnelle. Les termes protégés (identité du propriétaire, sujet
de notification…) ne sont **jamais** écrits en clair : seulement leur empreinte HMAC-SHA256 dans
`pilotage/confidentialite.json`, avec une clé secrète hors du dépôt (variable `CONF_CLE` de la routine du
vérificateur, ou ligne `CONF_CLE=` de `.matin-pea-local` sur le Mac). Le rapport ne recopie jamais ce qu'il
trouve : fichier, ligne et catégorie seulement.

| Fonction | Rôle |
|---|---|
| `regles(chemin)` | lit `pilotage/confidentialite.json` (empreintes, adresses techniques, auteurs et dossiers autorisés) |
| `cle()` | clé secrète : variable `CONF_CLE`, sinon `.matin-pea-local` ; `None` si absente |
| `normalise(mot)` | minuscules, sans accents ni ponctuation de bord |
| `empreinte(terme, k)` | HMAC-SHA256 du terme normalisé |
| `mots(texte)` | mots candidats : formes entières (adresse, identifiant) et morceaux |
| `email_autorise(adresse, autorises)` | adresse technique autorisée (noreply…) |
| `iban_valide(texte)` | IBAN dont la clé modulo 97 est juste (évite les faux positifs) |
| `analyser_texte(texte, k, empreintes, conf)` | (ligne, catégorie, gravité) : terme protégé, e-mail, dossier personnel, téléphone, IBAN, clé d'API, sujet ntfy |
| `fichiers_suivis()` | fichiers suivis par Git (ce qui est publié) |
| `lire_texte(chemin)` | texte d'un fichier, `None` s'il est binaire ou trop gros |
| `doublons(fichiers)` | copies « nom 2.md » créées par la synchronisation |
| `analyser_depot(k, conf)` | tous les fichiers publiés et les doublons |
| `analyser_commits(k, conf, n)` | auteurs et messages des n derniers commits (0 : tout l'historique) |
| `analyser_site(k, conf)` | la page en ligne |
| `gravite(points)` | 0, 1 ou 2 |
| `rapport(points, k)` | rapport Markdown, sans jamais la valeur trouvée |
| `main(args)` | options de la ligne de commande |

### `renvoi_notification.py` : la notification refusée au cloud, renvoyée par le Mac
Usage : `python3 scripts/renvoi_notification.py <sujet ntfy>` (appelé par le relais du Mac ; le sujet n'est
jamais écrit dans le dépôt). ntfy.sh compte son quota gratuit par adresse Internet, partagée dans le cloud :
quand il refuse (429), la fiche laisse le message dans `pilotage/notification.json` et ce script le renvoie
une seule fois depuis la connexion du Mac (trace dans `.matin-pea-local`, non publié). Il tourne aussi dans
GitHub Actions (`.github/workflows/renvoi-notification.yml`, sujet dans le secret `NTFY_TOPIC` du dépôt) dès
que la fiche dépose le fichier : la notification part alors même Mac éteint.

| Fonction | Rôle |
|---|---|
| `deja_renvoyee()` | « date moment » de la dernière notification renvoyée par ce Mac |
| `a_renvoyer(notif, aujourd_hui, deja)` | notification du jour, complète, pas encore renvoyée |
| `noter_renvoi(notif)` | garde la trace du renvoi dans `.matin-pea-local` |
| `main(args)` | lit le fichier, renvoie par ntfy, affiche une ligne de résultat |

### `secours.py` : la fiche de secours, sans Claude (GitHub Actions)
Lancé par `.github/workflows/fiche-secours.yml` (lun.–ven., UTC 8 h 50 et 9 h 50 pour l'ouverture, 17 h 40 et
18 h 40 pour la clôture). Si la fiche de ce moment est déjà publiée par l'agent Claude, il ne fait rien ; sinon
il enchaîne collecte, contrôle des prix, fiches détaillées, analyse automatique (chiffres seuls, sans presse),
rendu, publication (commit « Matin PEA … : fiche de secours sans Claude ») et notification ntfy (secret
`NTFY_TOPIC`). Le site continue donc de se mettre à jour même sans abonnement Claude.

| Fonction | Rôle |
|---|---|
| `fr(x, dec)` / `pct(x)` | nombres et variations à la française |
| `moment_publie(jour)` | moment de la fiche déjà publiée (lu dans `notes/`) |
| `a_faire(moment, publie)` | vrai si la fiche de ce moment manque (une clôture remplace une ouverture) |
| `analyse_auto(d, veille)` | analyse à partir des chiffres, avec les sept titres attendus par le contrôle |
| `notification(d)` | titre et message, comme ceux de l'agent Claude |
| `envoyer(titre, message, sujet, url_site)` | envoi par ntfy, renvoie le code HTTP |
| `main(args)` | `verifier`, `analyse`, `notification` ou `envoyer` |

### `obsidian.py` : les résumés lus par Obsidian (sans relais du Mac)
Usage : `python3 scripts/obsidian.py` (lancé par le chef à l'étape 10, sans réseau ; n'écrit que ce qui change).
Le coffre Obsidian contient ce dépôt, tenu à jour par le plugin Obsidian « Git » ; ses notes intègrent
ces fichiers avec `![[…]]` : `pilotage/obsidian-decisions.md` (40 décisions, les plus récentes d'abord) et
`apprentissage/a-retenir.md` (la phrase « À retenir » de chaque nuit depuis le 11/11/2026, sauf ❌ du chef).

| Fonction | Rôle |
|---|---|
| `jj_mm(date)` | « 2026-11-11 » → « 11/11 » |
| `ligne_decision(d)` | une décision → une ligne (idée, décision, gain, réalisation, bilan) |
| `resume_decisions(texte, nombre)` | les décisions les plus récentes d'abord |
| `section(texte, titre)` | contenu d'une partie « ## titre » d'un journal |
| `a_retenir(texte)` | phrase « À retenir », vide si le chef l'a marquée fausse (❌) |
| `resume_retenir(journaux, debut)` | une ligne par nuit, la plus ancienne d'abord |
| `ecrire_si_change(chemin, contenu)` | écrit seulement si le contenu change |
| `main()` | écrit les deux fichiers et affiche ce qui a changé |

### `mac.sh` et `Matin PEA.command` : le lanceur du Mac
Double-clic sur `Matin PEA.command` : crée `.venv` et installe `requirements.txt` (seulement s'il a changé),
récupère la dernière version (`git pull --ff-only`, sauté si des fichiers sont modifiés), puis propose :
fiche du jour (collecte → verif → fiches → rendu, ouverture dans le navigateur), copie des notes dans le
coffre Obsidian (sautée si le projet est déjà dans un coffre, pour ne jamais créer de doublon) (`Matin PEA/` : Fiches, Guide, Apprentissage ; chemin gardé dans `.matin-pea-local`, non
publié), contrôle et tests, et publication sur `claude/pea` après confirmation.

### `tests.py` : les garde-fous
Usage : `python scripts/tests.py` (sans réseau, quelques secondes). Aucun agent ne publie de code
si un test échoue. Chaque nouvelle fonction de calcul doit avoir son test.
`contrastes_des_deux_themes` (D-20261112-2) lit les couleurs des thèmes de `modele.html` et exige 4,5:1 (WCAG AA) pour chaque texte de couleur sur le fond, la carte et la carte 2, dans le thème clair et le sombre.
La syntaxe JavaScript de la page est vérifiée avec `node --check` dans le cloud, ou avec
JavaScriptCore (`jsc`, présent sur tous les Mac) en local.

## Techniques à retenir

- **Données du jour seulement** : la clôture n'est utilisée qu'une fois le fixing de 17 h 35 publié
  (métadonnées `regularMarketTime` du graphique Yahoo, qui ne demandent pas de « crumb »).
- **Prix moyen du jour (VWAP)** : somme de (prix typique × volume) / somme des volumes, barres de 5 min.
- **Risque SRI** : officiel (DIC PRIIPs, lu sur Boursorama) pour les ETF, estimé d'après la volatilité pour les actions.
- **Contrôle croisé** : médiane de trois sources, tolérance 1 % (2 % en séance). Les suggestions et les
  investissements du propriétaire sont contrôlés comme le reste.
- **Suggestions** : règles fixes et publiées, une raison chiffrée par titre, jamais « achète » ni
  « vends » ; elles signalent des titres à regarder, ce ne sont pas des recommandations.
- **Mes investissements** : prix de revient pondéré par les quantités ; un achat du jour compte depuis
  son prix d'achat, pas depuis la clôture de la veille ; frais de courtage non compris. Mêmes calculs dans
  `collecte.py` (fichier) et dans la page (barre de recherche). Une fiche archivée n'affiche que les
  achats antérieurs à sa date.
- **Politesse** : une requête par seconde au plus, `robots.txt` respecté, caches pour limiter les appels,
  aucune protection anti-robot contournée.
- **Page autonome** : données JSON compactes intégrées à la page (`<script id="donnees">`), aucun
  appel réseau à l'ouverture, sauf les polices.
- **Contourner le cache** de GitHub Pages pour vérifier une mise à jour : ajouter `?v=<commit>` à l'adresse.
- **Garde-fous** : tests obligatoires, filet de sécurité (annulation d'une amélioration de la nuit qui
  casse la fiche), règles de rôle par agent vérifiées par `controle.py`.
