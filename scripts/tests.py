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
def rendu_de_bout_en_bout():
    jours = sorted((RACINE / "data" / "jours").glob("20*.json"))
    assert jours, "aucune donnée dans data/jours"
    jour = jours[-1].stem
    with tempfile.TemporaryDirectory() as tmp:
        c = Path(tmp) / "depot"
        shutil.copytree(SCRIPTS, c / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        for f in ("config.json", "descriptions.json", "apprentissage/CHANGELOG.md", f"data/jours/{jour}.json",
                  f"data/analyses/{jour}.md"):
            if (RACINE / f).exists():
                (c / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(RACINE / f, c / f)
        (c / "docs" / "archives").mkdir(parents=True)
        r = subprocess.run([sys.executable, str(c / "scripts" / "rendu.py"), jour],
                           capture_output=True, text=True, timeout=180)
        assert r.returncode == 0, "rendu.py a planté :\n" + r.stderr[-1500:]
        page = (c / "docs" / "index.html").read_text(encoding="utf-8")
        for morceau in ('id="feuille"', "pas un conseil en investissement", "Matin <span>PEA</span>", 'id="top30"'):
            assert morceau in page, f"absent de la page : {morceau}"
        assert len(page) < 3_000_000, f"page trop lourde : {len(page) // 1024} Ko"
        m = re.search(r'<script id="donnees" type="application/json">(.*?)</script>', page, re.S)
        assert m, "données de la page introuvables"
        d = json.loads(m.group(1))
        for k in ("date", "indices", "devises", "top30", "petites", "regles"):
            assert k in d, f"clé absente des données : {k}"
        note = (c / "notes" / f"{jour}.md").read_text(encoding="utf-8")
        assert "## Top 30" in note and "pas un conseil" in note.lower(), "note Obsidian incomplète"
        assert (c / "docs" / "archives" / f"{jour}.html").exists() and (c / "docs" / "archives" / "index.html").exists()
        node = shutil.which("node")
        if node:
            for i, js in enumerate(re.findall(r"<script>(.*?)</script>", page, re.S)):
                f = c / f"page{i}.js"
                f.write_text(js, encoding="utf-8")
                r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True, timeout=60)
                assert r.returncode == 0, "erreur de syntaxe JavaScript :\n" + r.stderr[-1500:]
        else:
            REMARQUES.append("node absent : syntaxe JavaScript non vérifiée")


@test
def garde_fous():
    modele = (SCRIPTS / "modele.html").read_text(encoding="utf-8")
    assert "pas un conseil en investissement" in modele, "avertissement retiré du modèle"
    assert not re.search(r"(?<![A-Za-z]['’])\b(achète|achetez|vends|vendez)\b", modele, re.I), "formulation de conseil dans le modèle"
    routine = (RACINE / "ROUTINE.md").read_text(encoding="utf-8")
    assert "Pas de conseil en investissement personnalisé" in routine, "règle retirée de ROUTINE.md"
    assert (RACINE / "AMELIORATION.md").exists(), "AMELIORATION.md manquant"
    cfg = json.loads((RACINE / "config.json").read_text(encoding="utf-8"))
    assert cfg.get("url_site") == "https://matbs100.github.io/pea-quotidien/", "adresse du site modifiée"
    motif_secret = re.compile(r"ntfy\.sh/matin-pea-[0-9a-f]{10}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9-]{20,}")
    for p in list(SCRIPTS.glob("*")) + list(RACINE.glob("*.md")) + list(RACINE.glob("*.json")) + list((RACINE / "apprentissage").rglob("*.md")):
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
