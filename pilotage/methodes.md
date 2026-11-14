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
