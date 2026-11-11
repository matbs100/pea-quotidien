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
