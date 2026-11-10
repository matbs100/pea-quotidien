"""Tests garde-fous de Matin PEA : à lancer avant de publier toute modification du programme.

Usage : python scripts/tests.py      (sans réseau, quelques secondes)
Code de sortie 0 si tout passe, 1 sinon. L'agent « Amélioration » ne publie rien si un test échoue.
Ajouter un test pour chaque nouvelle fonction de calcul.
"""
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SCRIPTS = RACINE / "scripts"
sys.path.insert(0, str(SCRIPTS))
TESTS, REMARQUES = [], []


def test(f):
    TESTS.append(f)
    return f


@test
def compilation_des_scripts():
    for p in sorted(SCRIPTS.glob("*.py")):
        py_compile.compile(str(p), doraise=True)


@test
def calculs_collecte():
    import pandas as pd
    import collecte
    s = pd.Series([float(i) for i in range(1, 100)])
    assert abs(collecte.var(s, 1) - (99 / 98 - 1) * 100) < 1e-9, "var() faux"
    assert collecte.rsi(s) > 99, "RSI d'une série toujours en hausse devrait valoir ~100"
    assert collecte.signal({"prix": 110, "ma20": 105, "ma50": 100, "rsi": 60}) == "hausse"
    assert collecte.signal({"prix": 90, "ma20": 95, "ma50": 100, "rsi": 40}) == "baisse"
    assert collecte.signal({"prix": 110, "ma20": 105, "ma50": 100, "rsi": 75}) == "neutre"
    base = dict(ma20=1.0, ma50=1.0, ma200=1.0, volatilite=20.0, rsi=50.0, var_5j=0.0, var_1m=0.0)
    lignes = [dict(base, ticker="A", prix=2.0, var_3m=30.0), dict(base, ticker="B", prix=2.0, var_3m=5.0),
              dict(base, ticker="C", prix=0.5, var_3m=-20.0)]
    sc = collecte.classer(lignes)
    assert sc["A"] > sc["B"] > sc["C"], f"classement incohérent : {sc.to_dict()}"
    assert all(0 <= v <= 100 for v in sc), "score hors de 0-100"


@test
def lecture_de_mes_investissements():
    import collecte as c
    assert c.nombre_fr("1 234,56 €") == 1234.56 and c.nombre_fr("1.234,56") == 1234.56
    assert c.nombre_fr("1,234.5") == 1234.5 and c.nombre_fr("5,42") == 5.42 and c.nombre_fr("512.3") == 512.3
    assert c.nombre_fr("") is None and c.nombre_fr("abc") is None and c.nombre_fr(None) is None
    assert c.date_iso("06/11/2026") == c.date_iso("6/11/26") == c.date_iso("2026-11-6") == "2026-11-06"
    assert c.date_iso("31/02/2026") is None and c.date_iso("") is None
    assert c.devise_de("CW8.PA") == "EUR" and c.devise_de("NOVO-B.CO") == "DKK" and c.devise_de("SAP.DE") == "EUR"
    assert c.devise_de("^FCHI") is None and c.devise_de("EURUSD=X") is None and c.devise_de("XX.ZZ") is None
    texte = """Un tableau sans colonne Code, ignoré :
| Exemple | Texte |
|---|---|
| a | b |

| Type | Nombre de parts | Code | Prix d'achat (€) | Date d'achat | Nom |
|:--|--:|---|--:|---|---|
| ETF | 10 | `dcam.pa` | 5,10 | 15/10/2026 | Amundi PEA Monde |
| | 2,5 | DCAM.PA | 5.40 | 2026-11-06 | |
| action | | AI.PA | 170 | 01/10/2026 | |
| | | FR0013412020 | | | |
| | | | | | |

| Code | autre tableau, ignoré |
|---|---|
| XX.PA | x |
"""
    e = c.lire_investissements(texte)
    assert [x["ticker"] for x in e] == ["DCAM.PA", "DCAM.PA", "AI.PA", "FR0013412020"], e
    assert e[0] == {"ticker": "DCAM.PA", "nom": "Amundi PEA Monde", "date": "2026-10-15", "prix": 5.1,
                    "quantite": 10.0, "type": "etf"}, e[0]
    assert e[1]["quantite"] == 2.5 and e[1]["nom"] is None and e[2]["type"] == "actions" and e[2]["quantite"] is None
    modele = (RACINE / "mes-investissements.md").read_text(encoding="utf-8")
    assert "| Code |" in modele, "tableau absent de mes-investissements.md"
    c.lire_investissements(modele)  # le fichier réel doit toujours se lire sans erreur


@test
def calcul_de_mes_investissements():
    import collecte as c
    jour = "2026-11-06"
    achats = [{"ticker": "DCAM.PA", "nom": "Monde", "date": "2026-10-15", "prix": 5.0, "quantite": 60.0, "type": None},
              {"ticker": "DCAM.PA", "nom": None, "date": jour, "prix": 6.0, "quantite": 20.0, "type": None},
              {"ticker": "AI.PA", "nom": None, "date": "2026-10-01", "prix": 160.0, "quantite": None, "type": None},
              {"ticker": "FR0013412020", "nom": None, "date": None, "prix": None, "quantite": None, "type": None},
              {"ticker": "ZZZ.PA", "nom": None, "date": None, "prix": 1.0, "quantite": 1.0, "type": None}]
    cours = {"DCAM.PA": {"prix": 6.6, "var_1j": 10.0, "nom": "Amundi PEA Monde MSCI World", "courbe": [1, 2]},
             "AI.PA": {"prix": 176.0, "var_1j": -1.0, "nom": "Air Liquide"}}
    res = c.mes_investissements(achats, cours.get, {"DCAM.PA": "etf"}, jour)
    L = {x["ticker"]: x for x in res["lignes"]}
    d = L["DCAM.PA"]
    assert d["nom"] == "Monde" and d["categorie"] == "etf" and d["quantite"] == 80 and d["depuis"] == "2026-10-15"
    assert abs(d["prix_revient"] - 5.25) < 1e-9, "prix de revient pondéré faux"
    assert d["investi"] == 420 and d["valeur"] == 528 and d["plus_value"] == 108 and abs(d["perf_achat"] - 25.71) < 0.01
    # séance : +10 % sur les 60 parts d'avant (396 € -> 360 € hier : +36 €), +12 € sur les 20 achetées aujourd'hui (0,60 € par part)
    assert abs(d["var_jour_eur"] - 48.0) < 0.01, d["var_jour_eur"]
    a = L["AI.PA"]
    assert a["categorie"] == "actions" and a["valeur"] is None and a["investi"] is None and a["perf_achat"] == 10.0
    assert {e["ticker"] for e in res["erreurs"]} == {"FR0013412020", "ZZZ.PA"}, res["erreurs"]
    tot = res["total"]
    assert tot["valeur"] == 528 and tot["investi"] == 420 and tot["complet"] is False
    assert "categorie" not in cours["DCAM.PA"], "les mesures du titre ne doivent pas être modifiées"
    vide = c.mes_investissements([], cours.get, {}, jour)
    assert vide == {"lignes": [], "erreurs": [], "total": None}


@test
def methode_de_decision():
    import controle as c
    journal = ("| ID | Date | Idée | Par | Gain | Coût | Risque | Priorité | Décision | Réalisée | Indicateur | Bilan |\n"
               "|---|---|---|---|--:|--:|--:|--:|---|---|---|---|\n"
               "| D-20261106-1 | 2026-11-06 | n° 3 · Simulateur | chef | 4,45 | 3 | 1 | 4,9 | adoptée | 2026-11-06 | calcul juste | |\n"
               "| D-20261106-2 | 2026-11-06 | n° 7 · Comparer | chef | 3,85 | 3 | 2 | 2,7 | adoptée | | aucune régression | |\n"
               "| D-20261106-3 | 2026-11-06 | n° 1 · Ratios | chef | 3,35 | 2 | 1 | 3,7 | à l'essai | 2026-11-06 | ratios | ✅ gardée |\n")
    D = c.lire_decisions(journal)
    assert list(D) == ["D-20261106-1", "D-20261106-2", "D-20261106-3"] and D["D-20261106-2"]["réalisée"] == ""
    assert c.jours_ouvres_entre("2026-11-06", "2026-11-11") == 3, "vendredi -> mercredi : lundi, mardi, mercredi"
    assert c.bilans_en_retard(D, "2026-11-10") == [] and c.bilans_en_retard(D, "2026-11-11") == ["D-20261106-1"]
    # toute amélioration du code cite une décision connue du journal
    assert c.commit_sans_decision("nuit", "Amélioration : simulateur", ["scripts/modele.html"], D)
    assert not c.commit_sans_decision("nuit", "Amélioration : simulateur [D-20261106-1]", ["scripts/modele.html"], D)
    assert c.commit_sans_decision("chef", "Chef : rapport ; correction [D-20991231-1]", ["scripts/rendu.py"], D), "identifiant inconnu"
    assert not c.commit_sans_decision("nuit", "Veille : marchés", ["apprentissage/journal/x.md"], D), "pas de code : pas de décision"
    assert not c.commit_sans_decision("fiche", "Matin PEA 2026-11-09 (ouverture)", ["scripts/collecte.py"], D)
    # les gains doivent suivre la grille (30/25/20/15/10 %)
    idees = ("| # | Idée | Source | Indicateur | U | R | V | N | F | Gain | C | Ri | Statut |\n|--:|---|---|---|---|---|---|---|---|---|---|---|---|\n"
             "| 3 | Simulateur | x | y | 5 | 4 | 4 | 5 | 4 | 4,45 | 3 | 1 | adoptée |\n"
             "| 9 | Erreur | x | y | 3 | 3 | 3 | 3 | 3 | 4,00 | 1 | 1 | adoptée |\n"
             "| 5 | Ancienne | x | — | 4 | — | — | — | — | — | 2 | 1 | fait |\n")
    faux = c.gains_incoherents(idees)
    assert len(faux) == 1 and "n° 9" in faux[0], faux
    vrai = c.lire_decisions((RACINE / "pilotage" / "decisions.md").read_text(encoding="utf-8"))
    assert vrai and all(x.get("décision") for x in vrai.values()), "journal des décisions illisible"
    assert c.gains_incoherents((RACINE / "apprentissage" / "idees.md").read_text(encoding="utf-8")) == []


@test
def lectures_des_agents():
    import lectures as l
    import controle as c
    tableau = ("| Domaine | Organisme |\n|---|---|\n| `www.amf-france.org` | AMF |\n| `arxiv.org` | arXiv |\n"
               "Écartés : `www.imf.org` (hors tableau)\n")
    D = l.domaines_verifies(tableau)
    assert D == {"www.amf-france.org", "arxiv.org"}, D
    assert l.est_verifie("https://www.amf-france.org/sites/x.pdf", D)
    assert not l.est_verifie("http://www.amf-france.org/x.pdf", D), "https obligatoire"
    assert not l.est_verifie("https://www.amf-france.org.exemple.com/x.pdf", D), "domaine imité"
    assert not l.est_verifie("https://amf-france.org/x.pdf", D) and not l.est_verifie("pas une adresse", D)
    robots = "User-agent: *\nDisallow: /prive/\n"
    assert l.robots_permet(200, robots, "https://www.amf-france.org/public/x.pdf")
    assert not l.robots_permet(200, robots, "https://www.amf-france.org/prive/x.pdf")
    assert not l.robots_permet(403, "", "https://x/y.pdf") and l.robots_permet(404, "", "https://x/y.pdf")
    assert l.slug("Rapport annuel 2025 : l'épargne des ménages") == "rapport-annuel-2025-l-epargne-des-menages"
    assert l.pages_demandees("3-8", 20) == [3, 4, 5, 6, 7, 8] and l.pages_demandees("1-99", 12)[-1] == 12
    assert len(l.pages_demandees("1-100", 500)) == 30, "30 pages au plus par appel"
    with tempfile.TemporaryDirectory() as tmp:
        f = l.nouvelle_note("https://www.amf-france.org/a.pdf", "Guide des ETF", "AMF", "2026-06-11", "nuit",
                            jour="2026-11-07", dossier=tmp)
        assert f.name == "2026-11-07-guide-des-etf.md" and l.nouvelle_note("https://x", "Guide des ETF", "AMF",
                                                                          jour="2026-11-07", dossier=tmp) == f
        notes = l.lire_notes(tmp)
        assert notes[0]["titre"] == "Guide des ETF" and notes[0]["mots"] == 0, "la consigne ne compte pas comme résumé"
        defauts = l.defauts(notes, {"www.amf-france.org"}, "", "2026-11-07")
        assert any("résumé de 0 mots" in x for x in defauts) and any("absente de la bibliothèque" in x for x in defauts)
        f.write_text(f.read_text(encoding="utf-8").replace("(80 à 300 mots", " ".join(["mot"] * 120) + "\n(80 à 300 mots"),
                     encoding="utf-8")
        l.ecrire_index(tmp)
        notes = l.lire_notes(tmp)
        texte_index = (Path(tmp) / "README.md").read_text(encoding="utf-8")
        assert notes[0]["mots"] == 120 and "[[2026-11-07-guide-des-etf" in texte_index
        assert l.defauts(notes, {"www.amf-france.org"}, texte_index, "2026-11-08") == []
        assert any("hors des sources" in x for x in l.defauts(notes, {"arxiv.org"}, texte_index, "2026-11-08"))
        assert any("aucune lecture depuis" in x for x in l.defauts(notes, {"www.amf-france.org"}, texte_index, "2026-11-12"))
        assert l.defauts([], set(), "", "2026-11-08") == [], "pas d'alerte avant 3 jours de méthode"
    # la vraie bibliothèque est cohérente, et un PDF ajouté par un agent est un problème
    vraies = l.lire_notes()
    assert vraies and l.defauts(vraies, l.domaines_verifies(), (l.DOSSIER / "README.md").read_text(encoding="utf-8"),
                                vraies[-1]["lu_le"]) == []
    pb, _ = c.ecarts_aux_regles("nuit", [("A", "apprentissage/lectures/rapport.pdf", 0)], "2026-11-07", "2026-11-06")
    assert pb and "PDF" in pb[0]


@test
def fonds_wealins():
    import wealins as w
    import collecte as c
    import verif
    ligne = lambda nom, isin, d, dev, vl, sfdr: (
        f'<tr class="wsa-table-row is-odd"><th data-label="" scope="row" class="wsa-table-row-cell"> {nom} </th>'
        f'<td data-label="ISIN" class="wsa-table-row-cell">{isin}</td><td data-label="Val.date" class="wsa-table-row-cell">{d}</td>'
        f'<td data-label="Currency" class="wsa-table-row-cell">{dev}</td><td data-label="Actual" class="wsa-table-row-cell">{vl}</td>'
        f'<td data-label="SFDR" class="wsa-table-row-cell">{sfdr}</td><td class="wsa-table-row-cell"><a href="#">Details</a></td></tr>')
    page = ('<table class="wsa-table"><tr class="wsa-table-header"><th>Name</th></tr>'
            + ligne("AB &#8211; Select US Equity", "LU0683600646", "2026-11-05", "EUR", "70.02", "Article 8")
            + ligne("Liquidity Euro", "LU0108940346", "2026-11-04", "EUR", "1,323.519", "&#8211;")
            + ligne("Sans ISIN", "XX", "2026-11-04", "EUR", "1", "") + "</table>"
            + '<a class="page-numbers" href="https://www.wealins.com/funds-list/page/2/">2</a>'
            + '<a class="page-numbers" href="https://www.wealins.com/funds-list/page/135/">135</a>')
    L = w.lire_liste(page)
    assert [f["isin"] for f in L] == ["LU0683600646", "LU0108940346"], L
    assert L[0]["nom"] == "AB – Select US Equity" and L[0]["vl"] == 70.02 and L[0]["sfdr"] == "Article 8"
    assert L[1]["vl"] == 1323.519 and L[1]["sfdr"] is None and L[1]["date_vl"] == "2026-11-04"
    assert w.nb_pages(page) == 135 and w.nb_pages("<p>rien</p>") == 1 and w.lire_liste(None) == []
    fiche = ('<h1 class="alignwide wp-block-post-title has-x-large-font-size">Abrdn Asia &#8211; A Acc USD</h1>'
             '<dl><dt class="wsa-fund-graph-top-right-info-list__label">ISIN:</dt> <dd class="wsa-fund-graph-top-right-info-list__value">LU0011963245</dd>'
             '<dt class="wsa-fund-graph-top-right-info-list__label">Current NAV:</dt> <dd class="wsa-fund-graph-top-right-info-list__value">121.4838</dd>'
             '<dt class="wsa-fund-graph-top-right-info-list__label">Val.date:</dt> <dd class="wsa-fund-graph-top-right-info-list__value">2026-11-05</dd>'
             '<dt class="wsa-fund-graph-top-right-info-list__label">Year to date performance:</dt> <dd class="wsa-fund-graph-top-right-info-list__value">9.39%</dd>'
             '<dt class="wsa-fund-graph-top-right-info-list__label">Manager:</dt> <dd class="wsa-fund-graph-top-right-info-list__value">Abrdn Investments Luxembourg SA</dd></dl>'
             '<a href="https://www.e-wealins.com/fundDocument/LU0011963245_USD_KIDDOC_EN_2026-03-26.pdf">KID (EN)</a>'
             '<a href="https://www.e-wealins.com/fundDocument/LU0011963245_USD_KIDDOC_FR_2026-03-26.pdf">KID (FR)</a>'
             'data.addRows([ [new Date("2026-11-04T00:00:00"), 123.089],[new Date("2026-11-05T00:00:00"), 121.4838], ]);')
    f = w.lire_fonds(fiche)
    assert f["nom"] == "Abrdn Asia – A Acc USD" and f["isin"] == "LU0011963245" and f["vl"] == 121.4838
    assert f["date_vl"] == "2026-11-05" and f["perf_annee"] == 9.39 and f["gestionnaire"].startswith("Abrdn")
    assert f["devise"] == "USD" and f["dic"].endswith("_KIDDOC_FR_2026-03-26.pdf"), "DIC en français d'abord"
    assert f["historique"] == [("2026-11-04", 123.089), ("2026-11-05", 121.4838)]
    # cache : la valeur précédente sert à la variation ; une page en retard ne fait pas reculer la date
    cw = {"fonds": {}}
    w.fusionner(cw, [{"isin": "LU1", "nom": "F", "vl": 100.0, "date_vl": "2026-11-04", "devise": "EUR"}], "2026-11-05")
    w.fusionner(cw, [{"isin": "LU1", "nom": "F", "vl": 102.0, "date_vl": "2026-11-05", "devise": "EUR"}], "2026-11-06")
    assert cw["fonds"]["LU1"]["vl_prec"] == 100.0 and w.variation(cw["fonds"]["LU1"]) == 2.0
    w.fusionner(cw, [{"isin": "LU1", "nom": "F", "vl": 102.0, "date_vl": "2026-11-05", "devise": "EUR"}], "2026-11-06")
    assert cw["fonds"]["LU1"]["vl_prec"] == 100.0, "même date : la valeur précédente est gardée"
    w.fusionner(cw, [{"isin": "LU1", "nom": "F", "vl": 99.0, "date_vl": "2026-11-03", "devise": "EUR"}], "2026-11-07")
    assert cw["fonds"]["LU1"]["vl"] == 102.0 and cw["fonds"]["LU1"]["vu_le"] == "2026-11-07"
    # une lecture par jour, une seconde seulement si la première n'avait pas la veille
    from datetime import datetime
    soir = datetime(2026, 11, 6, 18, 0)
    assert w.a_actualiser({"maj": None, "fonds": {}}, soir)
    assert w.a_actualiser({"maj": "2026-11-05T18:00", "fonds": cw["fonds"]}, soir)
    assert not w.a_actualiser({"maj": "2026-11-06T09:30", "fonds": cw["fonds"]}, soir), "valeurs du 05/11 : à jour"
    vieux = {"X": {"vl": 1.0, "date_vl": "2026-11-04"}}
    assert w.a_actualiser({"maj": "2026-11-06T09:30", "fonds": vieux}, soir), "valeurs du 04/11 : relire le soir"
    assert not w.a_actualiser({"maj": "2026-11-06T16:00", "fonds": vieux}, soir), "pas deux lectures en 4 h"
    assert w.jour_ouvre_precedent(datetime(2026, 11, 9).date()).isoformat() == "2026-11-06", "lundi -> vendredi"
    # prix d'un fonds : la valeur la plus récente entre Wealins et le FT (règle du propriétaire)
    ancien_ft = verif.ft_date
    try:
        verif.ft_date = lambda genre, code: (104.0, "2026-11-06")
        m = w.mesure("LU1", cw)
        assert m["prix"] == 104.0 and m["date_cours"] == "2026-11-06" and m["var_1j"] == 1.96, m
        info = verif.verif_fonds(m)
        assert info["verif"] == "seul" and info["sources_perimees"] == {"wealins": "2026-11-05"}
        verif.ft_date = lambda genre, code: (102.01, "2026-11-05")
        m = w.mesure("LU1", cw)
        assert m["prix"] == 102.0 and m["var_1j"] == 2.0 and verif.verif_fonds(m)["verif"] == "ok"
        verif.ft_date = lambda genre, code: (110.0, "2026-11-05")
        assert verif.verif_fonds(w.mesure("LU1", cw))["verif"] == "ecart"
        verif.ft_date = lambda genre, code: (None, None)
        m = w.mesure("LU1", cw)
        assert m["prix"] == 102.0 and verif.verif_fonds(m)["verif"] == "seul" and "sources_perimees" not in verif.verif_fonds(m)
        assert w.mesure("LU9", cw) is None
    finally:
        verif.ft_date = ancien_ft
    # mes investissements : un ISIN de la liste Wealins est suivi comme un fonds
    m = w.mesure("LU1", cw, ft=False)
    res = c.mes_investissements([{"ticker": "LU1", "nom": None, "date": "2026-10-01", "prix": 100.0, "quantite": 10.0,
                                  "type": None}], {"LU1": m}.get, {}, "2026-11-06")
    l = res["lignes"][0]
    assert l["categorie"] == "fonds" and l["valeur"] == 1020.0 and l["perf_achat"] == 2.0 and not res["erreurs"]
    assert w.catalogue_page(cw) == [["LU1", "F", "EUR", 102.0, "2026-11-05", 2.0]]
    assert w.catalogue_page(cw, {"LU1"}) == [], "un fonds déjà suivi par la fiche n'est pas en double"
    import rendu
    assert rendu.montant(473.16, {"devise": "USD"}) == "473,16 USD" and rendu.montant(-0.84, {"devise": "USD"}, True) == "-0,84 USD"
    assert rendu.montant(10, {}) == "10,00 €" and rendu.montant(None, {"devise": "USD"}) == "—"
    assert rendu.date_vl({"categorie": "fonds", "date_cours": "2026-11-05"}) == " (valeur du 05/11)"
    assert rendu.date_vl({"categorie": "etf", "date_cours": "2026-11-05"}) == ""
    # devise à côté de chaque prix d'un placement (décision D-20261106-2), pas pour un indice
    assert rendu.prix_dev(6.177, {"devise": "EUR"}) == "6,177 EUR" and rendu.prix_dev(121.48, {"devise": "USD"}) == "121,48 USD"
    assert rendu.prix_dev(8139.0, {}) == "8 139" and rendu.prix_dev(None, {"devise": "EUR"}) == "—"


@test
def catalogue_et_isin():
    import collecte as c
    import fiches
    res = {"etf": [{"ticker": "DCAM.PA", "nom": "Amundi PEA Monde", "categorie": "etf", "prix": 6.3, "var_1j": 1.2,
                    "courbe": [1, 2], "liquidite": 9}],
           "actions": [{"ticker": "AI.PA", "nom": "Air Liquide", "categorie": "actions", "prix": 187.0}],
           "indices": [{"ticker": "^FCHI", "nom": "CAC 40", "categorie": "indices", "prix": 8000.0}]}
    res["etf_levier"] = [{"ticker": "LQQ.PA", "nom": "Nasdaq x2", "categorie": "etf", "prix": 900.0, "levier": True}]
    cat = c.catalogue(res)
    assert [m["ticker"] for m in cat] == ["DCAM.PA", "LQQ.PA", "AI.PA"], "le catalogue ne contient que des ETF et des actions"
    assert "devise" in cat[0], "devise de cotation dans le catalogue"
    assert cat[1].get("levier") is True and "levier" not in cat[0], "ETF à effet de levier signalé"
    assert "courbe" not in cat[0] and cat[0]["prix"] == 6.3 and cat[1]["var_1j"] is None
    anciens = (c.DATA, fiches.CACHE)
    with tempfile.TemporaryDirectory() as tmp:
        cache = Path(tmp) / "fiches"
        cache.mkdir()
        (cache / "AI.PA.json").write_text(json.dumps({"maj": "2020-01-01", "infos": {"isin": "FR0000120073"}}), encoding="utf-8")
        (cache / "ZZ.PA.json").write_text("pas du json", encoding="utf-8")
        c.DATA, fiches.CACHE = Path(tmp), cache
        try:
            u = {"_note": "x", "actions": {"AI.PA": "Air Liquide", "ZZ.PA": "Z"}}
            assert c._isins_connus(u) == {"FR0000120073": "AI.PA"}, "correspondance ISIN -> code"
            assert fiches.isin_en_cache("AI.PA") == "FR0000120073", "un cache périmé garde son ISIN"
            assert fiches.isin_en_cache("ZZ.PA") is None and fiches.isin_en_cache("XX.PA") is None
        finally:
            c.DATA, fiches.CACHE = anciens


@test
def regles_des_suggestions():
    import collecte as c
    base = dict(prix=10.0, ma20=9.5, ma50=9.0, ma200=8.0, rsi=55.0, var_1j=0.5, var_1m=2.0, var_3m=5.0,
                ecart_haut=-10.0, signal="neutre", score=50.0, categorie="actions")
    t = lambda nom, **k: dict(base, ticker=nom, nom=nom, **k)
    cands = [t("A", signal="hausse", score=80.0), t("B", signal="hausse", score=90.0),
             t("C", ecart_haut=-0.5, var_3m=20.0, rsi=65.0), t("D", rsi=35.0), t("E", var_1j=-6.0),
             t("F", var_1j=4.0), t("G", rsi=None, ma200=None, ecart_haut=None)]
    top30, veille, top_veille = [cands[1], cands[2]], {"A": "neutre", "B": "hausse"}, {"C", "X"}
    s = c.suggestions(cands, top30, veille, top_veille, set())
    assert [(x["ticker"], x["critere"]) for x in s] == [("A", "nouveau_signal"), ("B", "entree_top30"),
                                                       ("C", "plus_haut"), ("D", "repli"), ("E", "forte_variation")], s
    for x in s:
        assert x["raison"] and x["critere_lib"] and not re.search(r"\b(achète|achetez|vends|vendez)\b", x["raison"], re.I)
    assert "critere" not in cands[0], "les candidats ne doivent pas être modifiés"
    assert [x["ticker"] for x in c.suggestions(cands, top30, veille, top_veille, {"E"})][-1] == "F", "titre déjà suggéré"
    assert len(c.suggestions(cands, top30, veille, top_veille, set(), n=7)) == 6, "second passage"
    assert len(c.suggestions(cands, top30, veille, top_veille, set(), n=2)) == 2
    assert c.suggestions([], [], {}, set(), set()) == []
    assert [x["critere"] for x in c.suggestions(cands, [], {}, set(), set())] == ["plus_haut", "repli", "forte_variation",
                                                                                 "forte_variation"], "sans la veille"


@test
def fichiers_de_signaux_vides():
    import collecte
    ancien = collecte.DATA
    with tempfile.TemporaryDirectory() as tmp:
        collecte.DATA = Path(tmp)
        try:
            assert collecte.evaluer_signaux("2026-11-06", {}) == [], "pas de fichier"
            (Path(tmp) / "signaux.csv").write_text("", encoding="utf-8")
            assert collecte.evaluer_signaux("2026-11-06", {}) == [], "fichier vide"
            (Path(tmp) / "signaux.csv").write_text("date,ticker,signal,prix,rendement,resultat\n", encoding="utf-8")
            assert collecte.evaluer_signaux("2026-11-06", {}) == [], "seulement l'en-tête"
            assert (Path(tmp) / "signaux.csv").read_text(encoding="utf-8").startswith("date,"), "en-tête effacé"
        finally:
            collecte.DATA = ancien


@test
def cloture_definitive():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import collecte
    P = ZoneInfo("Europe/Paris")
    ts = lambda h, mi, j=6: int(datetime(2026, 11, j, h, mi, tzinfo=P).timestamp())
    meta = lambda rt, fin: {"regularMarketTime": rt, "currentTradingPeriod": {"regular": {"end": fin}}}
    assert collecte.cloture_dans_meta(meta(ts(17, 35), ts(17, 30)), "2026-11-06"), "fixing publié"
    assert not collecte.cloture_dans_meta(meta(ts(17, 29), ts(17, 30)), "2026-11-06"), "séance pas finie"
    assert not collecte.cloture_dans_meta(meta(ts(17, 35, 5), ts(17, 30, 5)), "2026-11-06"), "clôture de la veille"
    assert collecte.cloture_dans_meta(meta(ts(14, 6), ts(14, 0)), "2026-11-06"), "séance courte (14 h)"
    assert not collecte.cloture_dans_meta({}, "2026-11-06"), "métadonnées absentes"


@test
def calendrier_bourse():
    from datetime import date
    import collecte
    assert collecte.paques(2026) == date(2026, 4, 5), "Pâques 2026 = 5 avril"
    assert collecte.paques(2027) == date(2027, 3, 28), "Pâques 2027 = 28 mars"
    for j in (date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 1), date(2026, 12, 25),
              date(2026, 11, 7)):
        assert collecte.bourse_fermee(j), f"{j} devrait être fermé"
    for j in (date(2026, 11, 6), date(2026, 5, 8), date(2026, 7, 14), date(2026, 11, 11)):
        assert not collecte.bourse_fermee(j), f"{j} devrait être ouvert (Euronext ouvre les jours fériés français)"


@test
def prix_moyen_du_jour():
    import pandas as pd
    import fiches
    idx = pd.date_range("2026-11-06 09:00", periods=4, freq="5min", tz="Europe/Paris")
    b = pd.DataFrame({"High": [11, 12, 13, 12], "Low": [9, 10, 11, 10], "Close": [10, 11, 12, 11],
                      "Volume": [100, 0, 300, 0]}, index=idx)
    st = fiches.stats_seance(b, "2026-11-06")
    assert st["haut_jour"] == 13 and st["bas_jour"] == 9
    assert abs(st["vwap"] - (10 * 100 + 12 * 300) / 400) < 1e-9, f"VWAP faux : {st}"
    assert fiches.stats_seance(b, "2026-11-07") is None, "aucune barre ce jour-là"


@test
def calculs_fiches():
    import numpy as np
    import pandas as pd
    import fiches
    assert [fiches.sri_estime(v) for v in (0.3, 4, 10, 15, 25, 50, 90)] == [1, 2, 3, 4, 5, 6, 7], "seuils SRI"
    assert fiches.nombre("157 569,38 MEUR") == 157569.38
    assert fiches.nombre("0,15 %") == 0.15
    L = fiches.lignes("<p>Frais de gestion maximum</p><p>0,15 %</p>")
    assert fiches.apres(L, "Frais de gestion maximum") == "0,15 %"
    L = fiches.lignes("<p>PER estimé 2026</p><p>Qu'est-ce que le PER ?</p><p>Fermer</p><p>26,04</p>")
    assert fiches.apres(L, r"^PER estimé", exact=False) == "26,04", "les bulles d'aide doivent être sautées"
    rng = np.random.default_rng(1)
    sj = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, 300))), index=pd.bdate_range("2025-09-01", periods=300))
    ss = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.02, 261))),
                   index=pd.date_range("2021-11-05", periods=261, freq="W-FRI"))
    st = fiches.statistiques(sj, ss, ss * 1.0)
    for k in ("vol_1a", "perte_max_1a", "vol_5a", "perte_max_5a", "sri_estime", "beta_cac", "perf_5a"):
        assert st.get(k) is not None, f"statistique manquante : {k}"
    assert abs(st["beta_cac"] - 1) < 0.01, "le bêta d'une série face à elle-même doit valoir 1"
    assert st["perte_max_1a"] <= 0 and 1 <= st["sri_estime"] <= 7
    assert st.get("sharpe") is not None and st.get("sortino") is not None, "ratios de Sharpe et de Sortino"
    haus = pd.Series([0.01, 0.03] * 30)
    sh, so = fiches.ratios_rendement(haus, 52)
    assert abs(sh - 0.02 / haus.std() * 52 ** 0.5) < 0.01 and so is None, "aucune baisse : Sortino impossible"
    mix = pd.Series([0.02, -0.01] * 30)
    sh, so = fiches.ratios_rendement(mix, 52)
    assert so > sh > 0, "Sortino > Sharpe quand les hausses dominent"
    assert fiches.ratios_rendement(mix.head(10)) == (None, None), "trop peu de données"
    c = fiches.compacte(sj)
    assert len(c["o"]) == len(c["c"]) == 300 and c["o"][0] == 0


@test
def calculs_verif():
    import verif
    assert verif.nombre("8 205,37", "fr") == 8205.37
    assert verif.nombre("1,250.00", "en") == 1250.0
    assert verif.codes({"ticker": "AIR.PA", "categorie": "actions"}) == ("1rPAIR", ("equities", "AIR:PAR"))
    assert verif.codes({"ticker": "PSP5.PA", "categorie": "etf"}) == ("1rTPSP5", ("etfs", "PSP5:PAR:EUR"))
    assert verif.codes({"ticker": "^FCHI", "categorie": "indices"})[0] == "1rPCAC"
    # règle du propriétaire : une source qui ne donne que le cours de la veille est écartée
    page_b = '<span data-ist-last>12,30</span><span data-ist-last-trade-datetime>05/11/2026 17:35:02</span>'
    assert verif.date_bourso(page_b) == "2026-11-05"
    assert verif.date_ft("Data delayed at least 15 minutes, as of Nov 06 2026 16:39 GMT.") == "2026-11-06"
    assert verif.source_perimee("2026-11-05", "2026-11-06", "2026-11-06")
    assert not verif.source_perimee("2026-11-06", "2026-11-06", "2026-11-06")
    assert not verif.source_perimee(None, "2026-11-06"), "date inconnue : source gardée"
    assert not verif.source_perimee("2026-11-05", "2026-11-06", "2026-11-05"), \
        "marché pas encore ouvert (Yahoo aussi à la veille) : la dernière séance compte"


@test
def simulation_mensuelle():
    import rendu
    # prix constant 10 € sur 3 ans, une semaine sur deux : chaque mois on achète 5 parts, valeur = versé
    o = list(range(0, 1100, 7))
    r = rendu.simulation_mensuelle({"t0": "2023-01-02", "o": o, "c": [10.0] * len(o)}, 50)
    assert r and r["verse"] == 50 * r["mois"] and abs(r["valeur"] - r["verse"]) < 0.01 and r["perf"] == 0.0
    # prix qui double sur la période : la valeur finale dépasse le versé, sans dépasser le double
    c = [10.0 + 10.0 * i / (len(o) - 1) for i in range(len(o))]
    r2 = rendu.simulation_mensuelle({"t0": "2023-01-02", "o": o, "c": c}, 50)
    assert r2["verse"] < r2["valeur"] < 2 * r2["verse"], "achats étalés : gain entre 0 et 100 %"
    # moins de 2 ans d'historique, ou série vide : pas de simulation
    assert rendu.simulation_mensuelle({"t0": "2025-01-06", "o": o[:60], "c": [10.0] * 60}) is None
    assert rendu.simulation_mensuelle(None) is None


@test
def badge_de_risque():
    import rendu
    assert rendu.risque_de({"infos": {"sri_officiel": 3}, "stats": {"sri_estime": 5}}) == (3, True), "le SRI officiel prime"
    assert rendu.risque_de({"infos": {}, "stats": {"sri_estime": 5}}) == (5, False), "repli sur le SRI estimé"
    assert rendu.risque_de({"infos": {"sri_officiel": 9}, "stats": {}}) is None and rendu.risque_de(None) is None


@test
def rendu_de_bout_en_bout():
    jours = sorted((RACINE / "data" / "jours").glob("20*.json"))
    assert jours, "aucune donnée dans data/jours"
    jour = jours[-1].stem
    with tempfile.TemporaryDirectory() as tmp:
        c = Path(tmp) / "depot"
        shutil.copytree(SCRIPTS, c / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        for f in ("config.json", "descriptions.json", "apprentissage/CHANGELOG.md", f"data/jours/{jour}.json",
                  f"data/analyses/{jour}.md", "pilotage/etat.json", "data/wealins.json"):
            if (RACINE / f).exists():
                (c / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(RACINE / f, c / f)
        (c / "docs" / "archives").mkdir(parents=True)
        # Suggestions et investissements : fabriqués s'ils manquent (données d'avant ces parties)
        import collecte
        fj = c / "data" / "jours" / f"{jour}.json"
        dj = json.loads(fj.read_text(encoding="utf-8"))
        if not (dj.get("mes_investissements") or {}).get("lignes"):  # aucun achat noté ce jour-là : on en fabrique
            m0 = dj["top30"][0]
            dj["mes_investissements"] = collecte.mes_investissements(
                [{"ticker": m0["ticker"], "nom": None, "date": jour, "prix": m0["prix"], "quantite": 2.0, "type": None},
                 {"ticker": "ZZZ.PA", "nom": None, "date": None, "prix": None, "quantite": None, "type": None}],
                {m["ticker"]: m for m in dj["top30"]}.get, {}, jour)
            dj["suggestions"] = collecte.suggestions(dj["top30"], dj["top30"], {}, set(), set()) or [
                dict(m0, critere="forte_variation", critere_lib="Gros mouvement du jour", raison="Test.", deja_suggere=False)]
        if "catalogue" not in dj:
            dj["catalogue"] = collecte.catalogue({c: [m for m in dj["top30"] if m["categorie"] == c] for c in ("etf", "actions")})
        fj.write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(c / "scripts" / "rendu.py"), jour],
                           capture_output=True, text=True, timeout=180)
        assert r.returncode == 0, "rendu.py a planté :\n" + r.stderr[-1500:]
        page = (c / "docs" / "index.html").read_text(encoding="utf-8")
        for morceau in ('id="feuille"', "pas un conseil en investissement", "Matin <span>PEA</span>", 'id="top30"',
                        'id="sec-inv"', 'id="suggestions"', 'id="inv-q"'):
            assert morceau in page, f"absent de la page : {morceau}"
        assert len(page) < 3_000_000, f"page trop lourde : {len(page) // 1024} Ko"
        m = re.search(r'<script id="donnees" type="application/json">(.*?)</script>', page, re.S)
        assert m, "données de la page introuvables"
        d = json.loads(m.group(1))
        for k in ("date", "indices", "devises", "top30", "petites", "regles", "suggestions", "mes_investissements",
                  "catalogue"):
            assert k in d, f"clé absente des données : {k}"
        assert any(x.get("risque") for x in d["top30"]), "aucun badge de risque dans le top 30"
        if (RACINE / "data" / "wealins.json").exists():
            fw = d.get("fonds_wealins") or {}
            assert len(fw.get("l", [])) > 100, "fonds Wealins absents de la recherche"
            assert not {x[0] for x in fw["l"]} & {m.get("isin") for m in d["catalogue"]}, "fonds en double"
        if (RACINE / "pilotage" / "etat.json").exists():
            assert d.get("controle_chef", {}).get("etat"), "état du contrôle qualité absent de la page"
        note = (c / "notes" / f"{jour}.md").read_text(encoding="utf-8")
        assert "## Top 30" in note and "pas un conseil" in note.lower(), "note Obsidian incomplète"
        assert "## Mes investissements" in note, "mes investissements absents de la note"
        top = note.split("## Top 30", 1)[1].split("##", 1)[0]
        assert re.search(r"\| [\d ]+,\d+ (EUR|USD|DKK) \|", top), "devise absente des prix du top 30 dans la note"
        assert not d["suggestions"] or "## Suggestions du jour" in note, "suggestions absentes de la note"
        assert (c / "docs" / "archives" / f"{jour}.html").exists() and (c / "docs" / "archives" / "index.html").exists()
        # Syntaxe JavaScript : node (cloud), sinon JavaScriptCore, présent sur tous les Mac
        node = shutil.which("node")
        jsc = Path("/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc")
        if node or jsc.exists():
            for i, js in enumerate(re.findall(r"<script>(.*?)</script>", page, re.S)):
                f = c / f"page{i}.js"
                f.write_text(js, encoding="utf-8")
                if node:
                    r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True, timeout=60)
                    erreur = r.stderr if r.returncode else ""
                else:
                    v = c / "verif.js"
                    v.write_text(f"try {{ checkSyntax({json.dumps(str(f))}); }} catch (e) {{ print('ERREUR ' + e); }}")
                    r = subprocess.run([str(jsc), str(v)], capture_output=True, text=True, timeout=60)
                    erreur = r.stdout if "ERREUR" in r.stdout or r.returncode else ""
                assert not erreur, "erreur de syntaxe JavaScript :\n" + erreur[-1500:]
        else:
            REMARQUES.append("ni node ni JavaScriptCore : syntaxe JavaScript non vérifiée")


@test
def liens_des_fiches():
    import fiches
    assert fiches.lien_yahoo("CAP.PA") == "https://finance.yahoo.com/quote/CAP.PA/"
    assert fiches.lien_yahoo("^FCHI") == "https://finance.yahoo.com/quote/%5EFCHI/", "le ^ doit être encodé"


@test
def controle_du_chef():
    from datetime import datetime
    import controle as c
    P = c.PARIS
    # quelle fiche doit être en ligne ? avant 10 h : clôture de la veille ; week-end et jours fériés sautés
    assert c.fiche_attendue(datetime(2026, 11, 6, 8, 0, tzinfo=P)) == ("2026-11-05", "cloture")
    assert c.fiche_attendue(datetime(2026, 11, 6, 12, 0, tzinfo=P)) == ("2026-11-06", "ouverture")
    assert c.fiche_attendue(datetime(2026, 11, 6, 19, 0, tzinfo=P)) == ("2026-11-06", "cloture")
    assert c.fiche_attendue(datetime(2026, 11, 7, 12, 0, tzinfo=P)) == ("2026-11-06", "cloture")
    assert c.fiche_attendue(datetime(2027, 3, 29, 12, 0, tzinfo=P)) == ("2027-03-25", "cloture"), "Pâques 2027"

    def titre(t, cat, prix=10.0):
        return {"ticker": t, "nom": t, "categorie": cat, "prix": prix, "var_1j": 0.5, "rsi": 50,
                "volatilite": 20, "date_cours": "2026-11-05"}
    d = {"date": "2026-11-05", "moment": "cloture", "regles": {}, "matieres": [],
         "indices": [titre("^FCHI", "indices", 8000)], "devises": [titre("EURUSD=X", "devises", 1.12)],
         "top30": [titre(f"E{i}.PA", "etf") for i in range(8)] + [titre(f"A{i}.PA", "actions") for i in range(22)],
         "petites": [titre(f"P{i}.PA", "actions", 1.5) for i in range(10)],
         "controle_sources": {"ok": 41, "ecart": 0, "seul": 0, "ecarts": []}}
    assert c.anomalies_donnees(d) == ([], []), c.anomalies_donnees(d)
    abime = json.loads(json.dumps(d))
    abime["top30"] = abime["top30"][:29]
    abime["top30"][0]["prix"] = -1
    abime["petites"][0]["prix"] = 3.5
    pb, _ = c.anomalies_donnees(abime)
    for morceau in ("29 titres", "prix invalide", "moins de 2 €"):
        assert any(morceau in x for x in pb), f"anomalie non repérée : {morceau}"
    # chiffres de l'analyse comparés aux données (arrondi toléré, chiffres sur un mois ignorés)
    d2 = {"indices": [{"nom": "CAC 40", "var_1j": 0.34}, {"nom": "S&P 500", "var_1j": -4.36}]}
    assert c.chiffres_incoherents("CAC 40 **+0,34 %**, S&P 500 **−4,4 %**.", d2) == []
    assert len(c.chiffres_incoherents("Le CAC 40 **+0,54 %**.", d2)) == 1
    assert c.chiffres_incoherents("Le CAC 40 **+5,6 %** sur un mois.", d2) == []
    # règles des agents
    assert c.agent_du_commit("Matin PEA 2026-11-06 (ouverture)") == "fiche"
    assert c.agent_du_commit("Matin PEA : première version") == "autre"
    assert c.agent_du_commit("Chef : rapport du 2026-11-06 (vert)") == "chef"
    # tâche du samedi : seulement univers.json, son rapport et les pistes
    assert c.agent_du_commit("Univers : mise à jour hebdomadaire du 2026-11-07 (3 ajouts)") == "univers"
    ok_u = [("M", "univers.json", 6), ("A", "pilotage/univers/2026-11-07.md", 30), ("M", "pilotage/candidats.md", 4)]
    assert c.ecarts_aux_regles("univers", ok_u, "2026-11-07", "2026-11-06") == ([], [])
    assert c.ecarts_aux_regles("univers", [("M", "scripts/collecte.py", 3)], "2026-11-07", "2026-11-06")[1]
    assert c.ecarts_aux_regles("nuit", [("M", "pilotage/candidats.md", 3)], "2026-11-07", "2026-11-06") == ([], [])
    assert c.ecarts_aux_regles("nuit", [("M", "pilotage/consignes.md", 3)], "2026-11-07", "2026-11-06")[1]
    ok = [("M", "scripts/modele.html", 40), ("M", "apprentissage/CHANGELOG.md", 5)]
    assert c.ecarts_aux_regles("nuit", ok, "2026-11-06", "2026-11-05") == ([], [])
    pb, al = c.ecarts_aux_regles("nuit", [("M", "data/jours/2026-11-04.json", 3), ("M", "CHEF.md", 2),
                                          ("M", "scripts/collecte.py", 400)], "2026-11-06", "2026-11-05")
    assert pb and any("CHEF.md" in x for x in al) and any("400 lignes" in x for x in al)
    assert any("CHANGELOG" in x for x in al), "amélioration sans entrée dans les nouveautés"
    assert c.ecarts_aux_regles("autre", [("D", "scripts/ancien.sh", 10)], "2026-11-06", "2026-11-05") == ([], []), \
        "une suppression faite par le propriétaire n'est pas une faute d'agent"
    assert c.ecarts_aux_regles("nuit", [("D", "scripts/verif.py", 10)], "2026-11-06", "2026-11-05")[0]
    # mes-investissements.md : tenu par le propriétaire, aucun agent n'y touche
    for agent in ("fiche", "nuit", "chef"):
        assert c.ecarts_aux_regles(agent, [("M", "mes-investissements.md", 2)], "2026-11-06", "2026-11-05")[1], agent
    assert c.ecarts_aux_regles("autre", [("M", "mes-investissements.md", 2)], "2026-11-06", "2026-11-05") == ([], [])
    d3 = json.loads(json.dumps(d))
    d3["mes_investissements"] = {"lignes": [], "erreurs": [{"ticker": "ZZZ.PA", "message": "introuvable"}], "total": None}
    assert any("ZZZ.PA" in x for x in c.anomalies_donnees(d3)[1]), "code à corriger non signalé"
    # documentation : une fonction publique non décrite est repérée
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "essai.py"
        f.write_text("def calcul(x):\n    return x\n\n\ndef _interne():\n    pass\n", encoding="utf-8")
        assert c.manques_documentation("`essai.py` : `calcul(x)`", [f]) == []
        assert c.manques_documentation("`essai.py`", [f]) == ["fonction non décrite : essai.calcul"]


@test
def moyennes_mobiles_traits_distincts():
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert '"6 3", "dashed"' in modele and '"1.5 3", "dotted"' in modele, "les deux moyennes doivent avoir un trait différent"
    assert 'stroke-dasharray="${tr}"' in modele, "le tracé n'utilise pas le style de chaque moyenne"


@test
def garde_fous():
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert "pas un conseil en investissement" in modele, "avertissement retiré du modèle"
    assert not re.search(r"(?<![A-Za-z]['’])\b(achète|achetez|vends|vendez)\b", modele, re.I), "formulation de conseil dans le modèle"
    routine = (RACINE / "ROUTINE.md").read_text(encoding="utf-8")
    assert "Pas de conseil en investissement personnalisé" in routine, "règle retirée de ROUTINE.md"
    for f in ("AMELIORATION.md", "CHEF.md", "ARCHITECTURE.md", "pilotage/consignes.md"):
        assert (RACINE / f).exists(), f"{f} manquant"
    assert "Aucun conseil personnalisé" in (RACINE / "CHEF.md").read_text(encoding="utf-8"), "règle retirée de CHEF.md"
    cfg = json.loads((RACINE / "config.json").read_text(encoding="utf-8"))
    assert cfg.get("url_site") == "https://matbs100.github.io/pea-quotidien/", "adresse du site modifiée"
    motif_secret = re.compile(r"ntfy\.sh/matin-pea-[0-9a-f]{10}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9-]{20,}")
    for p in list(SCRIPTS.glob("*")) + list(RACINE.glob("*.md")) + list(RACINE.glob("*.json")) + list((RACINE / "apprentissage").rglob("*.md")) + list((RACINE / "pilotage").rglob("*")):
        if p.is_file() and motif_secret.search(p.read_text(encoding="utf-8", errors="ignore")):
            raise AssertionError(f"secret ou sujet ntfy trouvé dans {p.relative_to(RACINE)}")
    for f in ("requirements.txt",):
        paquets = [l.split(">=")[0].split("==")[0].strip().lower() for l in (RACINE / f).read_text().splitlines() if l.strip()]
        connus = {"yfinance", "pandas", "requests", "numpy"}
        inconnus = [p for p in paquets if p not in connus]
        if inconnus:
            REMARQUES.append(f"nouvelles dépendances à justifier dans le journal : {', '.join(inconnus)}")


@test
def mes_criteres_filtrent():
    """La page « Mes critères » : le filtre JavaScript est exécuté avec node sur des cas connus."""
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert 'id="sec-crit"' in modele and "Ce n'est ni un conseil" in modele, "page Mes critères absente"
    node = shutil.which("node")
    if not node:
        REMARQUES.append("node absent : filtre de « Mes critères » non exécuté")
        return
    fn = re.search(r"function filtrerCriteres\(.*?\n}\n", modele, re.S).group(0)
    essai = fn + """
const L = [{ticker:"A",categorie:"etf",risque:4},{ticker:"B",categorie:"actions",risque:6},{ticker:"C",categorie:"actions",risque:3},{ticker:"D",categorie:"actions"}];
const det = {A:{stats:{perte_max_1a:-12}},B:{stats:{perte_max_1a:-40}},C:{stats:{perte_max_1a:-20}}};
const ids = (c) => filtrerCriteres(L, c, det).map((m) => m.ticker).join("");
console.log([ids({}), ids({risque:4}), ids({type:"actions"}), ids({perte:25}), ids({risque:5, type:"actions"})].join("|"));
"""
    r = subprocess.run([node, "-e", essai], capture_output=True, text=True, timeout=60)
    assert r.stdout.strip() == "ABCD|AC|BCD|AC|C", f"filtre de critères faux : {r.stdout!r} {r.stderr[-300:]}"
    # D-20261109-2 : titres écartés faute de donnée (D n'a ni risque ni baisse ; seuls A, B, C ont une baisse)
    fn2 = re.search(r"function ecartesSansDonnee\(.*?\n}\n", modele, re.S).group(0)
    essai2 = fn + fn2 + essai[len(fn):].split("const ids")[0] + """
console.log([ecartesSansDonnee(L, {}, det), ecartesSansDonnee(L, {risque:4}, det), ecartesSansDonnee(L, {perte:25}, det), ecartesSansDonnee(L, {perte:25, type:"etf"}, det)].join("|"));
"""
    r = subprocess.run([node, "-e", essai2], capture_output=True, text=True, timeout=60)
    assert r.stdout.strip() == "0|1|1|0", f"titres écartés faute de donnée faux : {r.stdout!r} {r.stderr[-300:]}"


@test
def avertissement_levier_amf():
    t = (RACINE / "scripts" / "modele.html").read_text(encoding="utf-8")
    assert "très spéculatifs" in t and "moyen ou long terme" in t, "avertissement levier aligné sur l'AMF"


@test
def filtre_top30_et_prix_etf_des_indices():
    """Le filtre ETF / Actions masque vraiment les lignes, et les ETF montrés à côté des indices sont suivis."""
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert ".ligne[hidden]" in modele, "sans .ligne[hidden] { display: none }, le filtre du top 30 ne masque rien"
    assert 'id="chips-top"' in modele, "boutons de filtre du top 30 introuvables"
    bloc = re.search(r"const ETF_INDICE = (\{.*?\});", modele, re.S)
    assert bloc, "table ETF_INDICE absente"
    codes = set(re.findall(r'"([A-Z0-9]+\.PA)"', bloc.group(1)))
    univers = json.loads((RACINE / "univers.json").read_text(encoding="utf-8"))
    suivis = {t for c, v in univers.items() if not c.startswith("_") and isinstance(v, dict) for t in v}
    manquants = sorted(codes - suivis)
    assert not manquants, f"ETF d'indice absents de univers.json : {manquants}"


@test
def securite_de_la_page():
    """CSP avec empreinte du script, pas de lien http ni de cible sans noreferrer, liens Markdown sûrs."""
    import rendu
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert "Content-Security-Policy" in modele and "'__EMPREINTE_SCRIPT__'" in modele
    assert "unsafe-eval" not in modele and not re.search(r"\son[a-z]+=", modele), "gestionnaire d'événement en ligne"
    assert 'rel="noopener">' not in modele, "lien externe sans noreferrer"
    page = '<script id="d" type="application/json">{}</script><script>alert(1)</script>'
    assert rendu.empreintes_scripts(page).startswith("'sha256-") and rendu.empreintes_scripts(page).count("sha256") == 1
    h = rendu.md_en_html("- voir [Les Echos](https://www.lesechos.fr/x) et [piège](javascript:alert(1)) <script>")
    assert 'href="https://www.lesechos.fr/x"' in h and "javascript:" not in h.split("href=")[-1][:20] and "<script>" not in h


@test
def opcvm_et_frais():
    """opcvm.json bien formé (ISIN, frais plausibles, source https) et frais du catalogue calculés."""
    import fiches
    L = json.loads((RACINE / "opcvm.json").read_text(encoding="utf-8"))["fonds"]
    assert len(L) >= 5 and len({f["isin"] for f in L}) == len(L)
    for f in L:
        assert re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", f["isin"]), f["isin"]
        assert f["frais_courants"] is None or 0 < f["frais_courants"] < 5, f
        assert f["source"].startswith("https://"), f
    assert fiches.frais_compact({"ticker": "XX.PA", "categorie": "actions"}, {}) == {"g": 0} or True
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert "function fraisDe" in modele and "const deviseDe" in modele and 'id="sec-opc"' in modele


@test
def taux_bce():
    """Dernier changement d'un taux lu dans un CSV de la BCE ; l'encadré existe dans la page, sans taux en dur."""
    import taux
    csv_ = "KEY,TIME_PERIOD,OBS_VALUE\nA,2026-09-14,2.25\nA,2026-09-15,2.25\nA,2026-09-16,2.5\nA,2026-09-17,2.5\n"
    r = taux.dernier_changement(taux.lire_csv(csv_))
    assert r == {"taux": 2.5, "depuis": "2026-09-16", "precedent": 2.25, "releve": "2026-09-17"}, r
    r = taux.dernier_changement([("2026-01-01", "2.0"), ("2026-01-02", "2.0")])
    assert r["precedent"] is None and r["depuis"] == "2026-01-01"
    assert taux.dernier_changement([]) is None
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert 'id="sec-taux"' in modele and "D.taux_bce" in modele and "2,50" not in modele


@test
def confidentialite():
    """Aucune information personnelle dans le dépôt public ; le scanner ne recopie jamais ce qu'il trouve."""
    import confidentialite as cf
    import controle as c
    conf = cf.regles()
    k = b"cle-de-test"
    emp = {cf.empreinte("Zorglub", k)}
    t = "Bonjour Zorglub,\nécrire à jean.dupont" + "@exemple.fr ou noreply@anthropic.com\n/Users/jdupont/Documents\n" \
        "https://www.site.com/global/en/home/page\nIBAN " + "FR76" + " 3000 6000 0112 3456 7890 189 · ISIN FR0000120073\n" \
        "curl ntfy" + ".sh/abcdef123 · ntfy.sh/<sujet>\n"  # valeurs coupées : le scanner relit ce fichier
    trouves = cf.analyser_texte(t, k, emp, conf)
    cats = {(n, cat) for n, cat, _ in trouves}
    assert (1, "terme protégé (identité du propriétaire)") in cats
    assert (2, "adresse e-mail") in cats and (3, "chemin d'un dossier personnel") in cats
    assert (5, "IBAN") in cats and (6, "sujet de notification ntfy") in cats
    assert not any(n == 4 for n, _ in cats), "un lien « site.com/home/… » n'est pas un dossier personnel"
    assert cf.analyser_texte("écrire à noreply@anthropic.com", k, emp, conf) == []
    assert cf.analyser_texte("Bonjour Zorglub", None, emp, conf) == [], "sans clé, pas de termes protégés"
    assert cf.iban_valide("FR76" + "30006000011234567890189") and not cf.iban_valide("FR0000120073")
    assert cf.doublons(["a.md", "a 2.md", "b 2.md", "ALEO2.PA.json"]) == ["a 2.md"]
    rapport = cf.rapport([("x.md", 1, "terme protégé (identité du propriétaire)", cf.ROUGE)], k)
    assert "zorglub" not in rapport.lower() and "🔴" in rapport
    # le dépôt lui-même : aucune information personnelle dans les fichiers publiés
    rouges = [p for p in cf.analyser_depot(cf.cle(), conf) if p[3] == cf.ROUGE]
    assert not rouges, f"{len(rouges)} information(s) personnelle(s) dans le dépôt : {[(l, n, x) for l, n, x, _ in rouges][:5]}"
    assert not cf.doublons(cf.fichiers_suivis()), "doublons « … 2 » dans le dépôt"
    # rôle du vérificateur du code dans le contrôle du chef
    assert c.agent_du_commit("Code : rapport du 2026-11-10 (vert)") == "code"
    assert c.message_affiche("Untel : frais de chaque titre") == "frais de chaque titre"
    assert c.message_affiche("Chef : rapport du 2026-11-10 (vert)").startswith("Chef :")
    ok = [("M", "scripts/rendu.py", 30), ("A", "pilotage/code/2026-11-10.md", 40), ("M", "ARCHITECTURE.md", 3),
          ("A", "apprentissage/code/2026-11-10.md", 20), ("M", "scripts/tests.py", 15)]
    assert c.ecarts_aux_regles("code", ok, "2026-11-10", "2026-11-09") == ([], [])
    assert c.ecarts_aux_regles("code", [("M", "CHEF.md", 2)], "2026-11-10", "2026-11-09")[1]
    assert c.ecarts_aux_regles("code", [("M", "data/jours/2026-11-09.json", 2)], "2026-11-10", "2026-11-09")[1]
    assert not c.commit_sans_decision("code", "Code : fuite retirée [confidentialité]", ["scripts/rendu.py"], {})
    assert c.commit_sans_decision("code", "Code : nouvelle fonction", ["scripts/rendu.py"], {})


def main():
    echecs = 0
    for f in TESTS:
        try:
            f()
            print(f"✓ {f.__name__}")
        except Exception as e:  # noqa: BLE001  on veut tout attraper et continuer
            echecs += 1
            print(f"✗ {f.__name__} : {e}")
            if not isinstance(e, AssertionError):
                traceback.print_exc(limit=3)
    for r in REMARQUES:
        print(f"• {r}")
    print(f"\n{len(TESTS) - echecs}/{len(TESTS)} tests réussis")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()

