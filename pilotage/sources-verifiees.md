---
tags: [pea, agent, pilotage, sources]
---
# ✅ Sources vérifiées pour les lectures des agents

Les agents ne lisent des PDF (rapports, guides, études, méthodologies, DIC) **que** sur ces sites :
organismes officiels, régulateurs, banques centrales, bourses, fournisseurs d'indices, émetteurs des
produits et institutions de recherche. `scripts/lectures.py` refuse tout autre domaine, vérifie le
`robots.txt` de chaque lien et refuse un lien qui redirige ailleurs. Liste établie le 6 novembre 2026,
`robots.txt` lus ce jour-là.

Le PDF et son texte ne vont **jamais** dans le dépôt (il est public, et les documents ont des droits
d'auteur) : seulement le lien, un résumé écrit avec ses propres mots, les chiffres clés avec leur page et
ce que Matin PEA peut en tirer (`apprentissage/lectures/`).

| Domaine | Organisme | Type | Ce qu'on y trouve | Réseau du cloud |
|---|---|---|---|---|
| `www.amf-france.org` | Autorité des marchés financiers | régulateur (France) | guides de l'épargnant, études sur les frais, les ETF, le PEA | autorisé |
| `www.banque-france.fr` | Banque de France | banque centrale | bulletins, études sur l'épargne des ménages, l'inflation, les taux | autorisé |
| `www.ecb.europa.eu` | Banque centrale européenne | banque centrale | bulletin économique, revue de stabilité financière, décisions de taux | autorisé |
| `www.esma.europa.eu` | Autorité européenne des marchés financiers (ESMA) | régulateur (UE) | rapports sur les coûts des fonds et ETF, risques des marchés | à autoriser |
| `www.eiopa.europa.eu` | Autorité européenne des assurances et des pensions (EIOPA) | régulateur (UE) | rapports sur l'assurance vie en unités de compte, les coûts | à autoriser |
| `www.bis.org` | Banque des règlements internationaux | institution internationale | rapport annuel, études sur les marchés et les ETF | à autoriser |
| `www.insee.fr` | INSEE | statistique publique | inflation, épargne, conjoncture | autorisé |
| `www.impots.gouv.fr` | Direction générale des finances publiques | administration | fiscalité du PEA et de l'épargne | autorisé |
| `bofip.impots.gouv.fr` | BOFiP (doctrine fiscale) | administration | règles fiscales officielles (PEA, TTF) | autorisé |
| `www.lafinancepourtous.com` | Institut pour l'éducation financière du public | pédagogie (soutenu par la Banque de France) | guides pour débutants : bourse, PEA, ETF, risques | à autoriser |
| `www.euronext.com` | Euronext | bourse | règles de marché, horaires, fixings, indices CAC | autorisé |
| `live.euronext.com` | Euronext | bourse | fiches et documents des titres cotés | autorisé |
| `www.stoxx.com` | STOXX (fournisseur d'indices) | indices | méthodologies des indices Stoxx Europe 600, Euro Stoxx 50 | à autoriser |
| `www.msci.com` | MSCI (fournisseur d'indices) | indices | méthodologies MSCI World, Emerging Markets (certains chemins interdits par `robots.txt` : vérifiés lien par lien) | à autoriser |
| `www.amundietf.fr` | Amundi ETF | émetteur | DIC, prospectus, rapports des ETF Amundi | autorisé |
| `www.ishares.com` | iShares (BlackRock) | émetteur | DIC, fiches et rapports des ETF iShares | autorisé |
| `www.e-wealins.com` | Wealins | assureur (supports d'assurance vie) | DIC et prospectus des fonds de la liste Wealins | à autoriser |
| `arxiv.org` | arXiv (Université Cornell) | recherche | articles de finance quantitative (momentum, volatilité, diversification) | autorisé |
| `www.nber.org` | National Bureau of Economic Research | recherche | études sur les marchés, l'épargne, les frais des fonds | à autoriser |
| `www.w3.org` | W3C | normes du web | accessibilité (WCAG), lisibilité des pages | autorisé |

**Écartés le 6 novembre 2026** (ne pas utiliser) : `www.imf.org`, `www.spglobal.com` et `papers.ssrn.com`
(leur `robots.txt` n'est pas lisible par un robot : accès refusé), `www.oecd.org` (le `robots.txt` interdit le
dossier des PDF), `www.economie.gouv.fr` et `www.legifrance.gouv.fr` (accès des robots refusé).

## Ajouter une source

Le chef d'orchestre peut ajouter une ligne si le site est celui d'un organisme officiel, d'une bourse, d'un
fournisseur d'indices, d'un émetteur du produit ou d'une institution de recherche reconnue, et si son
`robots.txt` permet de lire ses PDF ; il l'écrit dans son rapport, avec « réseau : à autoriser par
Le propriétaire » (lui seul règle les domaines autorisés du cloud). Jamais de blog, de forum, de site commercial
ni de média qui vend des conseils.

## Code, sécurité et confidentialité (vérificateur du code)

Ajoutées le 10 novembre 2026 pour l'apprentissage quotidien du vérificateur du code ; `robots.txt` lus ce
jour-là (tous autorisent la lecture). Documentation officielle, organismes publics et journaux techniques
reconnus seulement : pas de blog inconnu ni de forum.

| Domaine | Organisme | Type | Ce qu'on y trouve | Réseau du cloud |
|---|---|---|---|---|
| `docs.python.org` | Python Software Foundation | documentation officielle | nouveautés de chaque version (« What's New »), bibliothèque standard | autorisé |
| `www.python.org` | Python Software Foundation | éditeur | versions publiées, avis de sécurité | autorisé |
| `peps.python.org` | Python (PEP) | normes du langage | propositions d'évolution du langage | autorisé |
| `blog.python.org` | Python Insider (équipe Python) | journal technique | annonces de versions et de correctifs | autorisé |
| `pypi.org` | Python Package Index | registre | versions et notes de version des bibliothèques du projet | autorisé |
| `pandas.pydata.org` | pandas | documentation officielle | nouveautés et changements de pandas | autorisé |
| `osv.dev` | Open Source Vulnerabilities (Google, open source) | base de failles | failles connues des bibliothèques Python | autorisé |
| `nvd.nist.gov` | NIST (États-Unis) | base de failles officielle | fiches CVE | autorisé |
| `csrc.nist.gov` | NIST | normes (PDF) | développement sécurisé (SSDF), cryptographie | autorisé |
| `owasp.org` | OWASP Foundation | sécurité du web | Top 10 des risques, guides (PDF) | autorisé |
| `cheatsheetseries.owasp.org` | OWASP | fiches pratiques | échappement, en-têtes de sécurité, politique de contenu (CSP) | autorisé |
| `developer.mozilla.org` | Mozilla (MDN) | documentation du web | HTML, CSS, JavaScript, sécurité des pages, accessibilité | autorisé |
| `www.cnil.fr` | CNIL | autorité (France) | protection des données personnelles, guide RGPD du développeur (PDF) | autorisé |
| `cyber.gouv.fr` | ANSSI | agence publique (France) | guides de sécurité informatique (PDF) | autorisé |
| `docs.github.com` | GitHub | documentation officielle | Git, GitHub Pages, confidentialité de l'adresse e-mail des commits | autorisé |
| `github.blog` | GitHub | journal technique | nouveautés et changelog de GitHub | autorisé |
| `lwn.net` | LWN.net | journal technique reconnu | actualité du logiciel libre et de Python | autorisé |
| `code.claude.com` | Anthropic | documentation officielle | Claude Code, routines, *skills* des agents | autorisé |
| `docs.claude.com` | Anthropic | documentation officielle | bonnes pratiques des agents et des *skills* | autorisé |

