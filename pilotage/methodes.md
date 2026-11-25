---
tags: [pea, agent, pilotage, methodes]
---
# 🛠️ Le manuel des méthodes

Règles de travail apprises en chemin, lues par tous les agents avant de commencer. Tenu par le chef
d'orchestre : une règle par ligne, datée, avec l'agent concerné et l'exemple qui l'a motivée.

## Toutes les tâches
- (06/11, tous) **Prix du jour seulement** : une source qui ne donne que le cours de la veille n'est
  pas prise en compte dans la comparaison des prix (règle du propriétaire ; `source_perimee()` dans
  `scripts/verif.py`). Exemple : Wealins publie la valeur des fonds le lendemain, il n'est donc pas
  une source de comparaison.
- (06/11, tous) **Vérifier avant d'ajouter un titre** : cours récents sur Yahoo **et** « éligible PEA »
  + ISIN sur Boursorama. Les foncières cotées (SIIC : Covivio, Gecina, Klépierre, Icade, Mercialys,
  Altarea) et les actions allemandes cotées sur Xetra ne sont pas indiquées éligibles : ne pas les
  ajouter.
- (06/11, tous) **Pas de doublon d'indice inutile** : un ETF coté en dollars (CW8U) qui copie un ETF
  déjà suivi en euros (CW8) n'est pas ajouté.
- (06/11, tous) Si `pip install` échoue (pypi.org bloqué), la tâche ne peut rien vérifier : le dire
  dans le rapport et s'arrêter, sans rien ajouter. Cause trouvée le 06/11 : routine créée dans un
  autre environnement cloud que les autres.

## Fiche du jour
- (06/11, fiche) Un cours daté d'un autre jour (ALPHA.AT) se signale dans « À garder en tête ».

## Agent de nuit
- (06/11, nuit) Une piste de nouveau titre va dans `pilotage/candidats.md`, jamais directement dans
  `univers.json`.
- (, nuit / nouveaux fonds) Une piste de fonds porte son ticker Yahoo, ouvert et vérifié, pas seulement
  l'ISIN : deux pistes du 06/11 (Ossiam) ont été écartées faute de cotation à Paris.
- (, nuit / lectures) Après une lecture, relire le PDF avant d'écrire chaque chiffre : le chef a retrouvé
  tous ceux des deux fiches du 06-07/11, garde cette méthode.
- (09/11, nuit / tous devoirs) Quand les pages sont bloquées deux nuits de suite, ne cherche pas à deviner une adresse : cherche-la avec WebSearch (`site:amundietf.fr …`), ouvre-la, et à défaut note « bloqué » et passe au devoir suivant. Exemple : adresse amundietf.fr devinée en 404 le 09/11.
- (08/11, nuit / nouveaux fonds) Une piste porte l'ISIN **lu** sur une page ouverte, jamais « à recouper » ; avant de proposer un émetteur « peu présent », compter ses fonds dans `univers.json`. Exemple : 4 pistes Amundi du 08/11 sans ISIN, alors que l'émetteur est déjà présent.
- (11/11, nuit) **Pas plus de deux nuits sur un même fonds** : si la page ouverte ne mentionne pas « éligible PEA », noter « non éligible probable » dans `candidats.md` et passer au suivant. Exemple : MWRD, trois jours de devoirs sans réponse.
- (11/11, nuit) **Une fiche de lecture cite des pages lisibles** : le chef relit chaque chiffre à la page indiquée ; garde cette précision (exemple : fiche arXiv du 11/11, tous les chiffres exacts).
- (12/11, nuit) **Presse d'abord** : `data/presse/` n'a que 2 jours ; la nuit du 12/11 l'a sautée « faute de temps ». Fais la presse (5 sources, estimations attribuées) avant l'amélioration, ou écris pourquoi elle est impossible.
- (12/11, chef) **Un lien Yahoo en 404 n'est pas un symbole faux** : la page HTML de Yahoo refuse les adresses du cloud (FOO.PA, CD8.PA) ; le symbole est bon si la collecte a des cours. L'API de Yahoo est interdite par robots.txt : ne l'appelle pas.
- (13/11, design) **Écris l'identifiant de décision tel quel** (D-20261113-1) et place l'entrée de `CHANGELOG.md` sous l'en-tête du fichier ; regarde les captures `rendre` avant de pousser. Exemple : entrée collée au-dessus de l'en-tête, identifiant « D-2026-11-13 sans tirets-1 ».
- (13/11, nuit / presse) **Quand un site est bloqué, WebSearch `site:` avant d'abandonner** : 2 sources sur 5 le 13/11 alors que Les Echos, BFM et MarketWatch se retrouvent par recherche.
- (14/11, nuit) **Une amélioration qui touche `data/presse/` reste dans le rôle** quand la consigne la demande ; écris-le dans le journal pour que le contrôle n'ait pas à le signaler. Exemple : alerte « hors du rôle » sur la revue de presse du 14/11, levée par le chef.
- (14/11, nuit) **Nouveaux fonds : pars des fonds écartés par la tâche du samedi**, pas d'une recherche libre par émetteur : deux nuits sans piste confirmée (CEU, Ossiam).
- (14/11, tous) **Un cours Boursorama vide n'est pas un écart de prix** : la page FF55-IBE (Espagne) renvoie `last` nul ; Yahoo et FT donnent 23,70 €. Regarde les deux autres sources avant de conclure.
- (2026-11-15) Agent de nuit et design : une décision provisoire se note dans le **tableau** de `pilotage/decisions.md` (ligne `| D-… |` à 12 colonnes), pas en liste à puces : sinon le contrôle la voit comme absente (exemple : D-20261115-2).
- (2026-11-16, design) **Une décision du design va dans le tableau de `pilotage/decisions.md`** (ligne `| D-… |`), pas en puces ; regarde le graphique à **360 px** comme demandé, pas 390 px. Exemple : D-20261116-1 écrite en puces, devoir 360 px fait à 390 px.
- (2026-11-16, nuit) **Une revue de presse demandée par `ecole.md` se déclare dans le journal** (« fichier demandé par le chef ») ; la nuit l'a fait, l'alerte reste mais est vérifiable.
- (17/11, chef et tous) **Pas d'API de Yahoo, même pour vérifier un prix** : le chef l'a appelée par erreur le 17/11 ; pour confirmer un cours, ouvre la page FT (`markets.ft.com`, déjà lue par la collecte) ou celle de l'émetteur. Une page Boursorama d'une place étrangère (FF55-IBE) peut afficher un vieux cours : compare à FT avant de conclure.
- (17/11, chef) **Un devoir de vérification reporté 5 fois est abandonné** et devient une règle prudente (exemple : l'heure d'ouverture d'Euronext, aucune source officielle en ligne : idée n° 52).

- (18/11, nuit) **Un devoir « lire » demande un PDF avec du texte** : une infographie (AMF, 4 pages) est presque vide ; ouvre-le d'abord, et prends-en un autre s'il n'a pas de paragraphes. Le chef ne peut lui-même relire qu'un PDF lisible depuis le cloud (la FAQ AMF s'y ouvre mal : confirme par la page web).
- (18/11, nuit) **Une presse « une source » compte deux chiffres du corps d'un article**, pas un titre de liste ; sinon le devoir est 🔁.
- (19/11, nuit) **Citer l'étude au mot près** : « la meilleure règle bat la détention » n'est pas « les règles battent la détention ». Exemple : note du signal de tendance corrigée par le chef.
- (20/11, nuit et design) **Identifiant de décision unique** : avant de numéroter, lis les dernières lignes de `pilotage/decisions.md` ; le 20/11 la nuit et le design ont tous deux pris D-20261120-1 (le chef a renuméroté celle du design en D-20261120-2).
- (21/11, nuit) Écris toi-même la ligne de ta décision dans `pilotage/decisions.md` avant de pousser ; si le système refuse, réessaie en ajoutant la ligne en fin de tableau, sinon note-le pour le chef (exemple : D-20261121-2 manquait).
- (22/11, design et nuit) **Une décision va dans le tableau de `pilotage/decisions.md`** (ligne `| D-… |` à 12 colonnes), pas en puce ; le 22/11 la nuit n'avait écrit aucune ligne pour D-20261122-2 (le contrôle l'a signalée) et le design l'avait écrite en puce. Écris-la toi-même avant de pousser.
- (22/11, nuit) **Une revue de presse = 2 chiffres du corps de 2 articles de 2 sources entières** : Zonebourse seule (+ titres Boursorama) reste 🔁, comme le 18/11.
- (23/11, design) **Même défaut que le 22/11 : sa décision est en puce, sans ligne dans le tableau** de `pilotage/decisions.md` (D-20261123-1 design, D-20261123-1 propriétaire : même identifiant deux fois). Avant de numéroter, `grep D-AAAAMMJJ pilotage/decisions.md`, prends le numéro suivant et écris la ligne à 12 colonnes dans le tableau. Le chef reporte la ligne si elle manque.
- (23/11, tous) **Un rendu qui ne change que la date `releve` de `data/taux_bce.json` n'est plus une alerte** (permis au design, D-20261123-3) ; `data/presse/*` est permis à la nuit. Toute autre donnée touchée par un agent reste hors rôle.
- (24/11, design) **Troisième fois : décision en puce.** Le design écrit sa décision en puce et pas dans le tableau (D-20261122-1, D-20261123-1, D-20261124-1). Avant de pousser, `grep "^| D-AAAAMMJJ" pilotage/decisions.md` doit montrer ta ligne ; le chef a dû la recopier.
- (24/11, nuit / presse) **Un chiffre d'une page de liste n'est pas un chiffre de presse** : VIX 26,62 et Brent 88,87 $ du 24/11 viennent de la page d'actualités Boursorama ; ouvre l'article avant de les écrire.
- (25/11, design) **4e fois : décision en puce** (D-20261125-1) ; le contrôle « Méthode de décision » la signale désormais (D-20261125-3). Écris la ligne `| D-… |` du tableau avant de pousser, 12 colonnes.
- (25/11, nuit) **Le tableau a 12 colonnes** : ta ligne D-20261125-2 mettait la date dans la colonne « Bilan » (13e cellule) ; le bilan reste vide jusqu'au passage du chef. `data/taux_bce.json` est un cache écrit par `scripts/taux.py` : si tu y changes quelque chose, écris-le dans le journal pour qu'il soit vérifié.
