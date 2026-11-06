---
tags: [pea, guide, univers, etf]
date: 2026-11-06
---
# Ajout de titres éligibles au PEA : rapport du 6 novembre 2026

Fait par Claude depuis le Mac le 6 novembre vers 18 h 30, à la demande du propriétaire (« ajoute plus de fonds éligibles au PEA »).
Les deux essais dans le cloud (10 h 50 et 18 h 25) n'avaient rien pu ajouter : ces tâches avaient été créées dans un autre
environnement cloud, où pypi.org, Yahoo et Boursorama sont bloqués. Elles sont désactivées ; la tâche du samedi a été recréée
dans le bon environnement (`UNIVERS.md`).

**Méthode** : chaque candidat a passé deux vérifications : (a) cours du 6 novembre 2026 sur Yahoo Finance ;
(b) page Boursorama indiquant « PEA » dans l'éligibilité, avec un ISIN. Le nom retenu est celui du produit qui porte cet ISIN.
L'ISIN est aussi enregistré dans le cache (`data/fiches/`), donc la recherche par ISIN les trouve dès la prochaine fiche.

## Résultat : 72 titres ajoutés

### ETF (section `etf`) : 23

| Code | Nom | ISIN |
|---|---|---|
| `GPEA.PA` | Amundi PEA Global (MSCI ACWI) | FR0014017NX3 |
| `PAASI.PA` | Amundi PEA Asie Émergente (MSCI EM Asia) | FR0013412012 |
| `PAEJ.PA` | Amundi PEA Asie Pacifique hors Japon | FR0011869312 |
| `PINR.PA` | Amundi PEA Inde (MSCI India) | FR0011869320 |
| `PMEH.PA` | Amundi PEA Immobilier Europe (FTSE EPRA/NAREIT) | FR0011869304 |
| `OBLI.PA` | Amundi PEA Euro Court Terme (monétaire) | FR0013346681 |
| `CACC.PA` | Amundi CAC 40 (capitalisation, CACC) | FR0013380607 |
| `C50.PA` | Amundi Core Euro Stoxx 50 | LU1681047236 |
| `ETDD.PA` | BNP Paribas Easy Euro Stoxx 50 | FR0012739431 |
| `DAX.PA` | Amundi DAX II | LU0252633754 |
| `CG1.PA` | Amundi DAX (CG1) | FR0010655712 |
| `CD8.PA` | Amundi MSCI EMU High Dividend | FR0010717090 |
| `MMS.PA` | Amundi MSCI EMU Small Cap ESG | LU1598689153 |
| `PABZ.PA` | Amundi MSCI EMU Climate Paris Aligned | LU2182388582 |
| `TNO.PA` | Amundi Stoxx Europe 600 Technologie | LU1834988518 |
| `HLT.PA` | Amundi Stoxx Europe 600 Santé | LU1834986900 |
| `BNK.PA` | Amundi Stoxx Europe 600 Banques | LU1834983477 |
| `INS.PA` | Amundi Stoxx Europe 600 Assurance | LU1834987973 |
| `FOO.PA` | Amundi Stoxx Europe 600 Consommation de base | LU1834985845 |
| `TRV.PA` | Amundi Stoxx Europe 600 Consommation discrétionnaire | LU1834988781 |
| `CHM.PA` | Amundi Stoxx Europe 600 Matériaux de base | LU1834983634 |
| `IND.PA` | Amundi Stoxx Europe 600 Industrie | LU1834987890 |
| `UTI.PA` | Amundi Stoxx Europe 600 Services aux collectivités | LU1834988864 |

### ETF à effet de levier (section `etf_levier`, hors top 30 et suggestions) : 4

| Code | Nom | ISIN |
|---|---|---|
| `LVC.PA` | Amundi CAC 40 Daily (2x) Leveraged | FR0010592014 |
| `LQQ.PA` | Amundi Nasdaq-100 Daily (2x) Leveraged | FR0010342592 |
| `CL2.PA` | Amundi MSCI USA Daily (2x) Leveraged | FR0010755611 |
| `BX4.PA` | Amundi CAC 40 Daily (-2x) Inverse | FR0010411884 |

### Actions (section `actions`) : 45

| Code | Nom | ISIN |
|---|---|---|
| `AKE.PA` | Arkema | FR0010313833 |
| `AMUN.PA` | Amundi | FR0004125920 |
| `BB.PA` | Bic | FR0000120966 |
| `BIM.PA` | bioMérieux | FR0013280286 |
| `COFA.PA` | Coface | FR0010667147 |
| `DBG.PA` | Derichebourg | FR0000053381 |
| `DEC.PA` | JCDecaux | FR0000077919 |
| `DIM.PA` | Sartorius Stedim Biotech | FR0013154002 |
| `ERA.PA` | Eramet | FR0000131757 |
| `FNAC.PA` | Fnac Darty | FR0011476928 |
| `FR.PA` | Valeo | FR0013176526 |
| `GET.PA` | Getlink | FR0010533075 |
| `IPN.PA` | Ipsen | FR0010259150 |
| `IPS.PA` | Ipsos | FR0000073298 |
| `MF.PA` | Wendel | FR0000121204 |
| `NK.PA` | Imerys | FR0000120859 |
| `RCO.PA` | Rémy Cointreau | FR0000130395 |
| `RF.PA` | Eurazeo | FR0000121121 |
| `RUI.PA` | Rubis | FR0013269123 |
| `SCR.PA` | SCOR | FR0010411983 |
| `SK.PA` | SEB | FR0000121709 |
| `SW.PA` | Sodexo | FR0000121220 |
| `TE.PA` | Technip Energies | NL0014559478 |
| `TFI.PA` | TF1 | FR0000054900 |
| `TRI.PA` | Trigano | FR0005691656 |
| `VCT.PA` | Vicat | FR0000031775 |
| `VIRP.PA` | Virbac | FR0000031577 |
| `VIV.PA` | Vivendi | FR0000127771 |
| `WLN.PA` | Worldline | FR00140182K6 |
| `EXA.PA` | Exail Technologies | FR0000062671 |
| `AYV.PA` | Ayvens | FR0013258662 |
| `PLX.PA` | Pluxee | NL0015001W49 |
| `OPM.PA` | OPmobility | FR0000124570 |
| `FRVIA.PA` | Forvia | FR0000121147 |
| `TKO.PA` | Tikehau Capital | FR0013230612 |
| `ANTIN.PA` | Antin Infrastructure Partners | FR0014005AL0 |
| `VU.PA` | Vusion | FR0010282822 |
| `ADP.PA` | Aéroports de Paris (ADP) | FR0010340141 |
| `ELIOR.PA` | Elior | FR0011950732 |
| `EXENS.PA` | Exosens | FR001400Q9V2 |
| `AD.AS` | Ahold Delhaize | NL0011794037 |
| `WKL.AS` | Wolters Kluwer | NL0000395903 |
| `HEIA.AS` | Heineken | NL0000009165 |
| `UCG.MI` | UniCredit | IT0005239360 |
| `ENI.MI` | Eni | IT0003132476 |

## Candidats écartés

| Code | Raison |
|---|---|
| `CEU.PA` | Boursorama ne l'indique pas éligible au PEA (LU1681042609) |
| `SMC.PA` | Boursorama ne l'indique pas éligible au PEA (IE00BKWQ0M75) |
| `ESEE.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `AUT.PA` | plus de cours sur Yahoo (LU1834983394, probablement fermé ou renommé) |
| `MDA.PA` | plus de cours sur Yahoo (LU1834988195, probablement fermé ou renommé) |
| `PUSA.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PAQ.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `MEUD.PA` | Boursorama ne l'indique pas éligible au PEA (LU0908500753) |
| `C6E.PA` | Boursorama ne l'indique pas éligible au PEA (LU1681040223) |
| `ETSZ.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `EESM.PA` | Boursorama ne l'indique pas éligible au PEA (LU1291101555) |
| `EKLD.PA` | Boursorama ne l'indique pas éligible au PEA (LU1291103338) |
| `PCWD.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PMJP.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `AASI.PA` | Boursorama ne l'indique pas éligible au PEA (LU1681044480) |
| `PUSN.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PSMR.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PMEU.PA` | plus de cours sur Yahoo (FR0013400256, probablement fermé ou renommé) |
| `MFDD.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `HSTE.PA` | Boursorama ne l'indique pas éligible au PEA (IE00BMWXKN31) |
| `UST.PA` | Boursorama ne l'indique pas éligible au PEA (LU1829221024) |
| `500.PA` | Boursorama ne l'indique pas éligible au PEA (LU1681048804) |
| `EPRA.PA` | Boursorama ne l'indique pas éligible au PEA (LU1437018838) |
| `OIL.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `CON.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `BRE.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `CST.PA` | plus de cours sur Yahoo (LU1834983808, probablement fermé ou renommé) |
| `RTA.PA` | plus de cours sur Yahoo (LU1834988435, probablement fermé ou renommé) |
| `TEL.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `ESGE.PA` | Boursorama ne l'indique pas éligible au PEA (LU1940199711) |
| `CW8U.PA` | éligible, mais copie de CW8 cotée en dollars : doublon |
| `EUE.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PEMG.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `PRAJ.PA` | Boursorama ne l'indique pas éligible au PEA (LU2089238385) |
| `PTPX.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `ZPRV.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `CI2.PA` | Boursorama ne l'indique pas éligible au PEA (LU1681043086) |
| `EMSRI.PA` | Boursorama ne l'indique pas éligible au PEA (LU1861138961) |
| `PTEC.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `CBEF.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `ECRP.PA` | Boursorama ne l'indique pas éligible au PEA (LU1437018168) |
| `ESGW.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `MWRD.PA` | Boursorama ne l'indique pas éligible au PEA (IE000BI8OT95) |
| `DSD.PA` | Boursorama ne l'indique pas éligible au PEA (FR0010869495) |
| `SHC.PA` | éligible, gardé en réserve (4 ETF à effet de levier suffisent) : voir `pilotage/candidats.md` |
| `LEVE.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `COV.PA` | Boursorama ne l'indique pas éligible au PEA (FR0000064578) |
| `FDJ.PA` | code inconnu de Boursorama (mnémonique faux ou radié) |
| `GFC.PA` | Boursorama ne l'indique pas éligible au PEA (FR0010040865) |
| `ICAD.PA` | Boursorama ne l'indique pas éligible au PEA (FR0000035081) |
| `LI.PA` | Boursorama ne l'indique pas éligible au PEA (FR0000121964) |
| `MERY.PA` | Boursorama ne l'indique pas éligible au PEA (FR0010241638) |
| `SESG.PA` | Boursorama ne l'indique pas éligible au PEA (LU0088087324) |
| `ALTA.PA` | Boursorama ne l'indique pas éligible au PEA (FR0000033219) |
| `CNP.PA` | plus de cours sur Yahoo (FR0000120222, probablement fermé ou renommé) |
| `MBG.DE` | Boursorama ne l'indique pas éligible au PEA (DE0007100000) |
| `BMW.DE` | Boursorama ne l'indique pas éligible au PEA (DE0005190003) |
| `BAS.DE` | Boursorama ne l'indique pas éligible au PEA (DE000BASF111) |
| `BAYN.DE` | Boursorama ne l'indique pas éligible au PEA (DE000BAY0017) |
| `MUV2.DE` | Boursorama ne l'indique pas éligible au PEA (DE0008430026) |
| `DB1.DE` | Boursorama ne l'indique pas éligible au PEA (DE0005810055) |
| `ADS.DE` | Boursorama ne l'indique pas éligible au PEA (DE000A1EWWW0) |
| `VOW3.DE` | Boursorama ne l'indique pas éligible au PEA (DE0007664039) |
| `DHL.DE` | Boursorama ne l'indique pas éligible au PEA (DE0005552004) |
| `BBVA.MC` | Boursorama ne l'indique pas éligible au PEA (ES0113211835) |

## À savoir

- Les foncières cotées (SIIC : Covivio, Gecina, Klépierre, Icade, Mercialys, Altarea) ne sont pas éligibles au PEA.
- Les actions allemandes cotées sur Xetra (Mercedes-Benz, BMW, BASF…) ne sont pas indiquées éligibles par Boursorama sur cette place, comme SAP et Allianz déjà suivis : à demander à BNP Paribas.
- `OBLI.PA` (Amundi PEA Euro Court Terme) suit les taux à court terme en euros (placement monétaire), éligible au PEA par construction ; ce n'est pas un ETF d'obligations au sens strict.
- 12 titres déjà suivis restent sans ISIN (places sans page Boursorama : Copenhague, Helsinki, Athènes, et quelques petites valeurs) : la recherche par nom les trouve.
- Liste totale suivie : 42 ETF, 4 ETF à effet de levier, 122 actions, 68 petites valeurs.
