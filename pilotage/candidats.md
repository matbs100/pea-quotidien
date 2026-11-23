---
tags: [pea, agent, pilotage, univers]
---
# 🔎 Pistes de nouveaux titres

Notées par le chef d'orchestre et l'agent de nuit dans la semaine ; vérifiées et ajoutées (ou
écartées) par la tâche du samedi (`UNIVERS.md`). Format : `- [ ] CODE.PA · nom · ISIN · source · pourquoi`.

## À vérifier
- [x] SHC.PA · Amundi CAC 40 Daily (-1x) Inverse · FR0010591362 · Boursorama (éligible PEA, 06/11) · gardé en réserve : `etf_levier` compte déjà 4 titres · écarté : en réserve, section pleine
- [x] ticker à trouver · BNP Paribas Easy MSCI EMU Min TE · LU1291098827 · pea.fr, tableau de février 2026 (extrait de recherche, page non ouverte) · ETF « minimum tracking error » zone euro, absent de l'univers · ajouté (EEMU.PA)
- [x] ticker à trouver · BNP Paribas Easy CAC 40 ESG · FR0010150458 · guide cité dans les résultats de recherche (non ouvert) et AMF p. 3 (CAC ESG cité) · version ESG du CAC 40 · ajouté (E40.PA)
- [x] ticker à trouver · Ossiam Europe ESG Machine Learning · LU0599612842 · pea.fr (extrait de recherche) · premier ETF Ossiam, stratégie ESG · écarté : pas de cotation Paris sur Yahoo
- [x] ticker à trouver · Ossiam Bloomberg Eurozone PAB · LU1847674733 · pea.fr (extrait de recherche) · indice zone euro aligné Paris · écarté : pas de cotation Paris sur Yahoo
- [x] ticker à trouver · HSBC Euro Stoxx 50 (Acc) · IE000MWUQBJ0 · pea.fr et liste UniCredit (extraits) · code contesté (IE00B4K6B022 cité ailleurs) : vérifier sur Boursorama avant tout ajout · ajouté (50E.PA, ISIN IE00B4K6B022 confirmé par Boursorama)

- [x] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · ISIN à recouper (non lu) · cotation vue sur Yahoo le 08/11 (cours du 06/11, EUR, Paris) · ligne « Core » de l'émetteur, absente de l'univers ; éligibilité PEA à vérifier sur Boursorama · écarté : Boursorama pea_bourso False (14/11)
- [x] MFE.PA · Amundi Core MSCI EMU UCITS ETF Dist · ISIN à recouper (non lu) · cotation Yahoo du 08/11 (cours du 06/11) · distribue ses dividendes, rare dans l'univers ; éligibilité PEA à vérifier · ajouté (MFE.PA, LU1646360971, pea_bourso True)
- [x] CEU.PA · Amundi MSCI Europe ESG Broad Transition UCITS ETF DR (C) · ISIN à recouper (non lu) · cotation Yahoo du 08/11 · version ESG de l'Europe ; éligibilité PEA à vérifier · écarté : ISIN introuvable (CEU = action canadienne sur Boursorama), ne pas inventer
- [x] CEM.PA · Amundi MSCI Europe Small Cap ESG Broad Transition Acc · ISIN à recouper (non lu) · cotation Yahoo du 08/11 · petites capitalisations européennes, absentes de l'univers ; éligibilité PEA à vérifier · écarté : Boursorama pea_bourso False (14/11)

## Traitées
- [x] 06/11 (ajout fait par Claude depuis le Mac) : 25 ETF, 4 ETF à effet de levier et 41 actions ajoutés, voir `guide/2026-11-06 Ajout des ETF - rapport.md`

## Notes de la nuit du 09/11 (devoir « nouveaux fonds », partiel)
- [x] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (extraits de recherche, page non ouverte : getquin, Trackinsight) · frais 0,12-0,13 % selon les sources · éligibilité PEA non confirmée (aucune page ouverte l'indique) · à lire sur Boursorama par la tâche du samedi · écarté : Boursorama pea_bourso False (14/11)
- [x] CEM.PA · Amundi MSCI Europe Small Cap ESG Broad Transition Acc · LU1681041544 (extraits : easybourse, Borsa Italiana) · frais 0,23 % (TradingView : 0,57 %) · éligibilité PEA non confirmée · à lire sur Boursorama · écarté : Boursorama pea_bourso False (14/11)
- [x] EQQQ.PA · Invesco EQQQ NASDAQ-100 UCITS ETF · ISIN non lu · émetteur Invesco absent de `univers.json` (émetteurs présents : Amundi, BNP Paribas Easy, HSBC, iShares) ; cotation Yahoo ouverte le 09/11 (Paris, EUR, 593,5) · ETF américain : probablement non éligible PEA (fonds physique), à vérifier avant tout ajout · écarté : Boursorama pea_bourso False, ISIN IE0032077012 (14/11)

## Notes de la nuit du 10/11
- [x] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (lu sur Finect le 10/11) · frais 0,12 %, encours 16,9 Md€ · éligibilité PEA non lue (la page ne la mentionne pas) · fonds irlandais, probablement non éligible : à vérifier sur Boursorama avant tout ajout · écarté : Boursorama pea_bourso False (14/11)


## Notes de la nuit du 10/11 (devoir 1)
- [x] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (lu sur Boursorama le 2026-11-10) · frais de gestion max 0,08 %, droits d'entrée et de sortie 0 % · éligibilité PEA **non lue** (la page ne la mentionne pas ; un extrait de recherche Trackinsight la suggère, non confirmé) · à lire sur une liste officielle avant tout ajout · écarté : Boursorama pea_bourso False (14/11)
- CEU : le code `CEU` de Boursorama est une action canadienne (ISIN CA15713J1049, non éligible), pas l'ETF Amundi : devoir 1 passé à CEU sans résultat ; l'ETF reste à retrouver par son ISIN.
- [x] MWRD.PA · Amundi Core MSCI World · IE000BI8OT95 · extrait de recherche du 11/11 (francetransactions.com : assurance vie et PER, pas de mention PEA) · devoir 1 : éligibilité PEA **non lue** ; à traiter comme probablement non éligible (CEU : pas passé, devoir limité à MWRD) · écarté : Boursorama pea_bourso False (14/11)

## Notes de la nuit du 12/11 (devoir 1 : émetteur Ossiam, absent de `univers.json`)
- [x] S6EW · Ossiam STOXX Europe 600 ESG Equal Weight NR UCITS ETF 1C · LU0599613147 (lu sur francetransactions.com le 12/11) · « éligible au PEA » lu sur la même page · frais de gestion 0,35 % · ticker S6EW lu ; cotation Paris non confirmée (page muette ; Yahoo S6EW.PA répond mais le dernier cours est vide : peu échangé, à surveiller) · ajouté (S6EW.PA, LU0599613147, pea_bourso True, dernier cours 12/11)
- [x] (ticker non lu) · Ossiam Europe ESG Machine Learning UCITS ETF 1C · LU0599612842 (lu sur francetransactions.com le 12/11) · « éligible au PEA » lu · frais de gestion 0,65 % · ticker et place de cotation non lus (MLEU.PA et EUMV.PA : introuvables sur Yahoo) : à retrouver avant tout ajout · écarté : pas de cotation Paris trouvée (déjà écarté le 14/11)
- Invesco EURO STOXX High Dividend Low Volatility (IE00BZ4BMM98) : **non éligible au PEA** (justETF, ouvert le 12/11, « Éligible au PEA : Non ») et sans cotation à Paris : écarté malgré la liste de pea.fr.

## Notes de la nuit du 13/11 (devoir 1)
- S6EW · Ossiam STOXX Europe 600 ESG Equal Weight · LU0599613147 · seconde source : un extrait de recherche (TradingView) confirme le ticker « S6EW FP » à Paris, mais aucune page lue ne mentionne « éligible PEA » hors francetransactions.com : éligibilité **non confirmée** par une seconde source. Autre émetteur : pas trouvé cette nuit.
## Notes de la nuit du 14/11 (devoir 1)
- Pas de piste confirmée en 15 minutes : les extraits de recherche citent Xtrackers (Euro Stoxx Quality Dividend, LU0292095535) et SPDR (MSCI Europe Small Cap, ticker SMC) comme éligibles PEA, mais la page francetransactions.com/etf-pour-pea, ouverte le 14/11, ne mentionne ni l'un ni l'autre : ISIN et éligibilité **non lus**, ticker Paris non vérifié. À lire sur la fiche de l'émetteur ou Boursorama avant tout ajout.
## Notes de la nuit du 15/11 (devoir 2)
- Pas fait : pas de page d'émetteur ouverte cette nuit pour les ETF écartés (MWRD, CEM, EQQQ) ; à reprendre.
## Notes de la nuit du 16/11 (devoir 2)
- Pas fait : aucune page d'émetteur ouverte cette nuit (temps pris par la lecture BCE et la presse) ; MWRD, CEM, EQQQ restent à lire.
## Notes de la nuit du 17/11 (devoir 2)
- EQQQ.PA · Invesco EQQQ Nasdaq-100 UCITS ETF · IE0032077012 (Dist) / IE00BFZXGZ54 (Acc) (extrait de recherche Trackinsight, non lu sur une page ouverte) · page émetteur ouverte le 17/11 (invesco.com/be/fr/etf/eqqq.html) : aucune mention « PEA », ni ISIN, ni frais ; la fiche produit invesco.com/fr/fr/... renvoie 404 · **non éligible probable** (ETF irlandais sur actions américaines) · ne plus y revenir (règle du 11/11).
## Notes de la nuit du 18/11 (devoir 2)
- MWRD.PA · Amundi MSCI World UCITS ETF · LU1437016972 (une fiche tierce) · extraits de recherche du 18/11 : MWRD est un fonds domicilié en Irlande ou au Luxembourg, aucune source ne le dit éligible au PEA ; les versions éligibles sont Amundi PEA Monde (FR001400U5Q4) et LU1681043599 (« PEA Oui » sur abcbourse) · non éligible probable ; pages Amundi ouvertes : 404 (liens devinés), à lire demain.
## Notes de la nuit du 19/11 (devoir 3)
- CEM.PA · Amundi MSCI Emerging Markets Swap UCITS ETF · LU1681045370 (ticker de cotation AEEM selon Fortuneo, lu en extrait de recherche) · aucune source ouverte ne mentionne « éligible PEA » ; fonds luxembourgeois à réplication synthétique (swap) · **non éligible probable** (le ticker CEM n'a pas pu être rapproché de cet ISIN : à ne pas afficher) ; ne plus y revenir (règle du 11/11). Alternative éligible déjà suivie : PAEEM (FR0013412020).
## Notes de la nuit du 20/11 (devoir 3)
- PEA MSCI USA ESG Selection (Amundi) · LU1681042864 (extrait de recherche d'une liste de fonds qui le marque « PEA », non lu sur une page émetteur) · ticker Paris non vérifié · éligibilité non confirmée par une seconde source : piste faible, à ouvrir sur la page Amundi avant tout ajout. PCEU (FR0013412038) est déjà dans `univers.json`.
## Notes du chef du 20/11 (devoir « nouveaux fonds »)
- [x] CU2.PA · Amundi PEA MSCI USA ESG Selection UCITS ETF · LU1681042864 · ticker Euronext Paris CU2 lu sur la fiche mensuelle Amundi de mai 2026 (extrait de recherche, PDF non ouvert) · le nom contient « PEA » mais aucune source ouverte ne confirme l'éligibilité (❔) · à vérifier le samedi sur la page émetteur ou Euronext avant tout ajout. · ajouté (CU2.PA, LU1681042864, pea_bourso True, 21/11)
## Notes de la nuit du 22/11 (devoir 3)
- [ ] PMEH.PA · Amundi PEA Immobilier Europe (FTSE EPRA/NAREIT) UCITS ETF Acc · FR0011869304 (lu sur la page francetransactions.com/etf-pour-pea, ouverte le 22/11 ; ticker PMEH et « éligible au PEA » vus dans des extraits de recherche : fiche mensuelle Amundi de mai 2026, Fortuneo, TradingView) · réplication synthétique, frais courants 0,40 %, encours d'environ 28 M€ (petit) · pourquoi : seul ETF immobilier coté éligible, les foncières cotées ne le sont pas · à vérifier le samedi : cours récents sur Yahoo (PMEH.PA) et « éligible PEA » sur Boursorama.
- Autres fonds de la liste francetransactions du 22/11 : déjà dans `univers.json` (DAX, Euro Stoxx 50, MSCI Europe, Asie-Pacifique, TOPIX, Nasdaq-100, OBLI) ; LU0908501058 (Amundi MSCI EMU ESG Broad Transition) : **non éligible probable** (extraits : fonds luxembourgeois, aucune mention PEA, fusion annoncée avec un autre fonds). Devoir : 1 piste sur 3 demandées, faute d'autres fonds absents de l'univers dans la liste lue.
## Note du propriétaire du 23/11
- [x] EEMK.PA · BNP Paribas Easy MSCI Emerging Min TE · LU1291097779 · écarté : non éligible au PEA (justETF et Boursorama, 23/11), retiré de `univers.json` (D-20261123-1) ; ne plus l'ajouter.
- [x] URW.PA · Unibail-Rodamco-Westfield · FR0013326246 · écarté : foncière au régime SIIC, non éligible au PEA (règle SIIC et Boursorama, contrôle quotidien du 23/11), retiré de `univers.json` (D-20261123-6) ; ne plus l'ajouter, ni une autre foncière SIIC.
## Notes de la nuit du 23/11 (devoir 3)
- PMEH.PA · Amundi PEA Immobilier Europe (FTSE EPRA/NAREIT) UCITS ETF Acc · FR0011869304 · DIC du 12/06/2026 ouvert et lu le 23/11 (amundietf.fr, p. 1-3) : frais de gestion et autres coûts **0,40 %** par an (pas 0,18 %), aucun coût d'entrée ni de sortie, SRI 5 sur 7, réplication indirecte par swap, texte « éligible au PEA » (p. 1). Reste à faire le samedi : cours récents sur Yahoo et ligne Boursorama.
