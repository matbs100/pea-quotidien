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
def catalogue_et_isin():
    import collecte as c
    import fiches
    res = {"etf": [{"ticker": "DCAM.PA", "nom": "Amundi PEA Monde", "categorie": "etf", "prix": 6.3, "var_1j": 1.2,
                    "courbe": [1, 2], "liquidite": 9}],
           "actions": [{"ticker": "AI.PA", "nom": "Air Liquide", "categorie": "actions", "prix": 187.0}],
           "indices": [{"ticker": "^FCHI", "nom": "CAC 40", "categorie": "indices", "prix": 8000.0}]}
    cat = c.catalogue(res)
    assert [m["ticker"] for m in cat] == ["DCAM.PA", "AI.PA"], "le catalogue ne contient que des ETF et des actions"
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
                  f"data/analyses/{jour}.md", "pilotage/etat.json"):
            if (RACINE / f).exists():
                (c / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(RACINE / f, c / f)
        (c / "docs" / "archives").mkdir(parents=True)
        # Suggestions et investissements : fabriqués s'ils manquent (données d'avant ces parties)
        import collecte
        fj = c / "data" / "jours" / f"{jour}.json"
        dj = json.loads(fj.read_text(encoding="utf-8"))
        if "mes_investissements" not in dj:
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
        if (RACINE / "pilotage" / "etat.json").exists():
            assert d.get("controle_chef", {}).get("etat"), "état du contrôle qualité absent de la page"
        note = (c / "notes" / f"{jour}.md").read_text(encoding="utf-8")
        assert "## Top 30" in note and "pas un conseil" in note.lower(), "note Obsidian incomplète"
        assert "## Mes investissements" in note, "mes investissements absents de la note"
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
    ok = [("M", "scripts/modele.html", 40), ("M", "apprentissage/CHANGELOG.md", 5)]
    assert c.ecarts_aux_regles("nuit", ok, "2026-11-06", "2026-11-05") == ([], [])
    pb, al = c.ecarts_aux_regles("nuit", [("M", "data/jours/2026-11-04.json", 3), ("M", "CHEF.md", 2),
                                          ("M", "scripts/collecte.py", 400)], "2026-11-06", "2026-11-05")
    assert pb and any("CHEF.md" in x for x in al) and any("400 lignes" in x for x in al)
    assert any("CHANGELOG" in x for x in al), "amélioration sans entrée dans les nouveautés"
    assert c.ecarts_aux_regles("autre", [("D", "scripts/ancien.sh", 10)], "2026-11-06", "2026-11-05") == ([], []), \
        "une suppression faite par Mathieu n'est pas une faute d'agent"
    assert c.ecarts_aux_regles("nuit", [("D", "scripts/verif.py", 10)], "2026-11-06", "2026-11-05")[0]
    # mes-investissements.md : tenu par Mathieu, aucun agent n'y touche
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
