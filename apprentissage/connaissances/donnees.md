---
tags: [pea, connaissances, donnees]
---
# 🗄 Données et sources

- **Liens Yahoo Finance** : le site français (`fr.finance.yahoo.com/quote/…`) renvoie une erreur 404
  pour beaucoup d'ETF et de petites valeurs (ETZ.PA, C40.PA, WPEA.PA, ALCJ.PA…), alors que le site
  international (`finance.yahoo.com/quote/…/`) fonctionne. Les fiches utilisent désormais le site
  international (`lien_yahoo()`). Source : contrôle des liens du 2026-11-06 (`scripts/controle.py`).
  Statut : ✅ vérifié le 2026-11-06 (constaté sur 6 titres)
- **DIC des ETF** : le lien du document PRIIPs vient de Boursorama et pointe vers `doc.morningstar.com`,
  dont le `robots.txt` interdit les robots. Le contrôle vérifie seulement que le lien est bien formé,
  sans l'ouvrir. Source : [robots.txt de doc.morningstar.com](https://doc.morningstar.com/robots.txt),
  lu le 2026-11-06. Statut : ✅ vérifié le 2026-11-06
- **Cours de Paris sur Yahoo** : diffusés avec 15 minutes de décalage ; les barres d'une minute
  s'arrêtent à 17 h 29, le fixing de clôture (17 h 35) n'apparaît que dans le cours quotidien et les
  métadonnées. Source : observations du programme le 2026-11-05. Statut : ⏳ à vérifier
- **Mesure du taux d'épargne** : selon un document de travail de l'INSEE (sept. 2026), les comptes bancaires d'un échantillon de clients donnent 5,8 % en 2022 contre 16,9 % dans les comptes nationaux, mais leurs variations trimestrielles suivent la comptabilité nationale (p. 3-4). Source : [INSEE, DT 2026-13](https://www.insee.fr/fr/statistiques/fichier/version-html/9041404/DT2026-13.pdf), lu le 2026-11-08. Statut : ✅ vérifié le 2026-11-08 (PDF rouvert : 5,8 % / 16,9 % / 18,5 % contre 17 % / 180 000 ménages retrouvés dans le texte ; pages 3-4 imprimées = 4-5 du PDF, [INSEE](https://www.insee.fr/fr/statistiques/fichier/version-html/9041404/DT2026-13.pdf))
- **Fonds Amundi Core MSCI World (MWRD)** : les extraits de recherche donnent l'ISIN IE000BI8OT95, un fonds irlandais, des frais courants de 0,12 à 0,13 % selon les sites ; l'éligibilité PEA n'y est pas confirmée. Source proposée : [getquin](https://app.getquin.com/en/etf/IE000BI8OT95/amundi-core-msci-world-ucits-etf-accum-usd) (page non ouverte). Statut : ⏳ à vérifier
- **Fonds Amundi MSCI Europe Small Cap ESG (CEM)** : ISIN LU1681041544, Luxembourg, frais 0,23 % pour la plupart des sources (0,57 % sur TradingView, contradictoire) ; éligibilité PEA non confirmée (extraits de recherche). Source proposée : [easybourse](https://www.easybourse.com/trackers/LU1681041544-25/am-is-msci-elsf-ue). Statut : ⏳ à vérifier
- **Sites bloqués le 2026-11-09 par le réseau du cloud** : pea.fr et trackinsight.com (WebFetch), page Boursorama de MWRD sans contenu. L'API Yahoo répond (EQQQ.PA : Invesco, Paris, EUR, cours 593,5). Statut : ⏳ à vérifier
- **Frais et encours des ETF (devoir)** : aucune source ouverte et lisible trouvée cette nuit ; piste : fiches `amundietf.fr` (autorisé) dont l'adresse exacte reste à trouver (404 sur l'adresse devinée). Statut : ⏳ à vérifier
