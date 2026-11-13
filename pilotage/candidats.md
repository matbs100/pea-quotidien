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

- [ ] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · ISIN à recouper (non lu) · cotation vue sur Yahoo le 08/11 (cours du 06/11, EUR, Paris) · ligne « Core » de l'émetteur, absente de l'univers ; éligibilité PEA à vérifier sur Boursorama
- [ ] MFE.PA · Amundi Core MSCI EMU UCITS ETF Dist · ISIN à recouper (non lu) · cotation Yahoo du 08/11 (cours du 06/11) · distribue ses dividendes, rare dans l'univers ; éligibilité PEA à vérifier
- [ ] CEU.PA · Amundi MSCI Europe ESG Broad Transition UCITS ETF DR (C) · ISIN à recouper (non lu) · cotation Yahoo du 08/11 · version ESG de l'Europe ; éligibilité PEA à vérifier
- [ ] CEM.PA · Amundi MSCI Europe Small Cap ESG Broad Transition Acc · ISIN à recouper (non lu) · cotation Yahoo du 08/11 · petites capitalisations européennes, absentes de l'univers ; éligibilité PEA à vérifier

## Traitées
- [x] 06/11 (ajout fait par Claude depuis le Mac) : 25 ETF, 4 ETF à effet de levier et 41 actions ajoutés, voir `guide/2026-11-06 Ajout des ETF - rapport.md`

## Notes de la nuit du 09/11 (devoir « nouveaux fonds », partiel)
- [ ] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (extraits de recherche, page non ouverte : getquin, Trackinsight) · frais 0,12-0,13 % selon les sources · éligibilité PEA non confirmée (aucune page ouverte l'indique) · à lire sur Boursorama par la tâche du samedi
- [ ] CEM.PA · Amundi MSCI Europe Small Cap ESG Broad Transition Acc · LU1681041544 (extraits : easybourse, Borsa Italiana) · frais 0,23 % (TradingView : 0,57 %) · éligibilité PEA non confirmée · à lire sur Boursorama
- [ ] EQQQ.PA · Invesco EQQQ NASDAQ-100 UCITS ETF · ISIN non lu · émetteur Invesco absent de `univers.json` (émetteurs présents : Amundi, BNP Paribas Easy, HSBC, iShares) ; cotation Yahoo ouverte le 09/11 (Paris, EUR, 593,5) · ETF américain : probablement non éligible PEA (fonds physique), à vérifier avant tout ajout

## Notes de la nuit du 10/11
- [ ] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (lu sur Finect le 10/11) · frais 0,12 %, encours 16,9 Md€ · éligibilité PEA non lue (la page ne la mentionne pas) · fonds irlandais, probablement non éligible : à vérifier sur Boursorama avant tout ajout


## Notes de la nuit du 10/11 (devoir 1)
- [ ] MWRD.PA · Amundi Core MSCI World UCITS ETF Acc · IE000BI8OT95 (lu sur Boursorama le 2026-11-10) · frais de gestion max 0,08 %, droits d'entrée et de sortie 0 % · éligibilité PEA **non lue** (la page ne la mentionne pas ; un extrait de recherche Trackinsight la suggère, non confirmé) · à lire sur une liste officielle avant tout ajout
- CEU : le code `CEU` de Boursorama est une action canadienne (ISIN CA15713J1049, non éligible), pas l'ETF Amundi : devoir 1 passé à CEU sans résultat ; l'ETF reste à retrouver par son ISIN.
- [ ] MWRD.PA · Amundi Core MSCI World · IE000BI8OT95 · extrait de recherche du 11/11 (francetransactions.com : assurance vie et PER, pas de mention PEA) · devoir 1 : éligibilité PEA **non lue** ; à traiter comme probablement non éligible (CEU : pas passé, devoir limité à MWRD)

## Notes de la nuit du 12/11 (devoir 1 : émetteur Ossiam, absent de `univers.json`)
- [ ] S6EW · Ossiam STOXX Europe 600 ESG Equal Weight NR UCITS ETF 1C · LU0599613147 (lu sur francetransactions.com le 12/11) · « éligible au PEA » lu sur la même page · frais de gestion 0,35 % · ticker S6EW lu ; cotation Paris non confirmée (page muette ; Yahoo S6EW.PA répond mais le dernier cours est vide : peu échangé, à surveiller)
- [ ] (ticker non lu) · Ossiam Europe ESG Machine Learning UCITS ETF 1C · LU0599612842 (lu sur francetransactions.com le 12/11) · « éligible au PEA » lu · frais de gestion 0,65 % · ticker et place de cotation non lus (MLEU.PA et EUMV.PA : introuvables sur Yahoo) : à retrouver avant tout ajout
- Invesco EURO STOXX High Dividend Low Volatility (IE00BZ4BMM98) : **non éligible au PEA** (justETF, ouvert le 12/11, « Éligible au PEA : Non ») et sans cotation à Paris : écarté malgré la liste de pea.fr.

## Notes de la nuit du 13/11 (devoir 1)
- S6EW · Ossiam STOXX Europe 600 ESG Equal Weight · LU0599613147 · seconde source : un extrait de recherche (TradingView) confirme le ticker « S6EW FP » à Paris, mais aucune page lue ne mentionne « éligible PEA » hors francetransactions.com : éligibilité **non confirmée** par une seconde source. Autre émetteur : pas trouvé cette nuit.