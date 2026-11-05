"""Collecte quotidienne : prix, indicateurs, top 30 PEA, 10 titres < 2 €, suivi des signaux.

Usage : python scripts/collecte.py            (date du jour)
Produit : data/jours/AAAA-MM-JJ.json, data/historique.csv, data/signaux.csv
Aucune donnée personnelle. Ce n'est pas un conseil en investissement.
"""
import csv
import json
import math
import sys
import time
import warnings
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data"
HORIZON = 5            # un signal est jugé 5 séances plus tard
LIQ_MIN = 50_000       # € échangés par jour en moyenne pour entrer dans le top 30
LIQ_MIN_PETITES = 5_000
PRIX_MIN_PETITES = 0.05  # en dessous : quasi-faillite / "penny" extrême, exclu


def telecharger(tickers):
    for essai in range(3):
        try:
            df = yf.download(tickers, period="14mo", interval="1d", auto_adjust=True,
                             group_by="ticker", progress=False, threads=True)
            if not df.empty:
                return df
        except Exception as e:  # réseau / limite Yahoo
            print("Essai", essai + 1, "échoué :", e, file=sys.stderr)
        time.sleep(10 * (essai + 1))
    sys.exit("Impossible de joindre Yahoo Finance.")


def rsi(s, n=14):
    d = s.diff()
    gain = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    perte = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    g, p = float(gain.iloc[-1]), float(perte.iloc[-1])
    if p == 0:  # aucune baisse récente : RSI maximal (ou neutre si le prix n'a pas bougé)
        return 100.0 if g > 0 else 50.0
    return 100 - 100 / (1 + g / p)


def var(s, n):
    return float(s.iloc[-1] / s.iloc[-1 - n] - 1) * 100 if len(s) > n else None


def r(x, n=2):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), n)


def mesures(df, t):
    try:
        bloc = df[t].dropna(subset=["Close"])
    except KeyError:
        return None
    if len(bloc) < 30:
        return None
    s, v = bloc["Close"], bloc["Volume"].fillna(0)
    dernier = float(s.iloc[-1])
    ma20, ma50 = s.rolling(20).mean().iloc[-1], s.rolling(50).mean().iloc[-1]
    ma200 = s.rolling(200).mean().iloc[-1] if len(s) >= 200 else math.nan
    an = s.tail(252)
    vol = s.pct_change().tail(20).std() * math.sqrt(252) * 100
    return {
        "prix": r(dernier, 4 if dernier < 10 else 2),
        "date_cours": str(s.index[-1].date()),
        "var_1j": r(var(s, 1)), "var_5j": r(var(s, 5)), "var_1m": r(var(s, 21)),
        "var_3m": r(var(s, 63)), "var_1a": r(var(s, 252)),
        "ma20": r(ma20, 4), "ma50": r(ma50, 4), "ma200": r(ma200, 4),
        "rsi": r(rsi(s), 1), "volatilite": r(vol, 1),
        "haut_1a": r(an.max(), 4), "bas_1a": r(an.min(), 4),
        "ecart_haut": r((dernier / an.max() - 1) * 100),
        "liquidite": int((s.tail(20) * v.tail(20)).mean()),
        "courbe": [r(x, 4) for x in s.tail(60).tolist()],
    }


def signal(m):
    """Signal technique à 5 séances. Règle simple, publiée, mesurée dans le temps."""
    p, a, b, rs = m["prix"], m["ma20"], m["ma50"], m["rsi"]
    if None in (p, a, b, rs):
        return "neutre"
    if p > a > b and rs < 70:
        return "hausse"
    if p < a < b and rs > 30:
        return "baisse"
    return "neutre"


def rang(serie):
    return serie.rank(pct=True).fillna(0.5)


def classer(lignes):
    d = pd.DataFrame(lignes).set_index("ticker")
    tendance = ((d.prix > d.ma50).astype(int) + (d.ma50 > d.ma200).fillna(False).astype(int)
                + (d.prix > d.ma20).astype(int)) / 3
    score = (0.35 * rang(d.var_3m) + 0.25 * rang(d.var_1m) + 0.15 * rang(d.var_5j)
             + 0.15 * tendance + 0.10 * (1 - rang(d.volatilite)))
    score -= ((d.rsi > 75) * 0.10)  # surchauffe
    return (score * 100).round(1)


def evaluer_signaux(jour, prix_du_jour):
    """Juge les signaux émis il y a au moins HORIZON séances."""
    f = DATA / "signaux.csv"
    if not f.exists():
        return []
    lignes = list(csv.DictReader(open(f, encoding="utf-8")))
    dates = sorted({l["date"] for l in lignes})
    for l in lignes:
        if l["resultat"] or l["date"] == jour:
            continue
        seances = len([x for x in dates if x > l["date"]]) + 1  # +1 : aujourd'hui
        t = l["ticker"]
        if seances >= HORIZON and t in prix_du_jour:
            ret = (prix_du_jour[t] / float(l["prix"]) - 1) * 100
            l["rendement"] = f"{ret:.2f}"
            if l["signal"] == "hausse":
                l["resultat"] = "juste" if ret > 0 else "faux"
            elif l["signal"] == "baisse":
                l["resultat"] = "juste" if ret < 0 else "faux"
            else:
                l["resultat"] = "neutre"
    with open(f, "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)
    return lignes


def bilan(lignes):
    jugees = [l for l in lignes if l["resultat"] in ("juste", "faux")]
    neutres = [l for l in lignes if l["resultat"] == "neutre"]
    hausses_reelles = [l for l in lignes if l["resultat"] and float(l["rendement"] or 0) > 0]
    toutes = [l for l in lignes if l["resultat"]]
    out = {"jugees": len(jugees), "justes": sum(l["resultat"] == "juste" for l in jugees)}
    out["taux"] = r(out["justes"] / len(jugees) * 100, 1) if jugees else None
    # Repère : % de titres montés sur 5 séances, sans aucun signal (« pile ou face » du marché)
    out["repere_hausse"] = r(len(hausses_reelles) / len(toutes) * 100, 1) if toutes else None
    out["neutres"] = len(neutres)
    return out


def main():
    jour = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    u = json.loads((RACINE / "univers.json").read_text(encoding="utf-8"))
    cats = [c for c in u if not c.startswith("_")]
    tickers = sorted({t for c in cats for t in u[c]})
    df = telecharger(tickers)

    res = {c: [] for c in cats}
    for c in cats:
        for t, nom in u[c].items():
            m = mesures(df, t)
            if m:
                m.update(ticker=t, nom=nom, categorie=c, signal=signal(m))
                res[c].append(m)
    tous = {m["ticker"]: m for c in cats for m in res[c]}

    # Top 30 : ETF + actions + petites capitalisations assez liquides (tout est éligible PEA)
    pea = [m for c in ("etf", "actions", "petites") for m in res.get(c, [])
           if m["liquidite"] >= LIQ_MIN and m["date_cours"] >= _recent(m, tous)]
    scores = classer(pea)
    for m in pea:
        m["score"] = float(scores[m["ticker"]])
    # Diversité : au moins 8 ETF, le reste au meilleur score
    tries = sorted(pea, key=lambda m: -m["score"])
    etf = [m for m in tries if m["categorie"] == "etf"][:8]
    reste = [m for m in tries if m not in etf][:30 - len(etf)]
    top30 = sorted(etf + reste, key=lambda m: -m["score"])

    # 10 titres < 2 € : liquides, triés par score, en évitant ceux montrés les 3 derniers jours
    deja = _petites_recentes(jour, 3)
    cand = [m for c in ("etf", "actions", "petites") for m in res.get(c, [])
            if PRIX_MIN_PETITES <= m["prix"] < 2 and m["liquidite"] >= LIQ_MIN_PETITES]
    if cand:
        sc = classer(cand)
        for m in cand:
            m["score_petite"] = float(sc[m["ticker"]])
    cand.sort(key=lambda m: (m["ticker"] in deja, -m.get("score_petite", 0)))
    petites = cand[:10]
    for m in petites:
        m["deja_vu"] = m["ticker"] in deja

    # Signaux : on note ceux du top 30, des petites et des indices, pour les juger plus tard
    lignes = evaluer_signaux(jour, {t: m["prix"] for t, m in tous.items()})
    f = DATA / "signaux.csv"
    neuf = not f.exists()
    deja_notes = {(l["date"], l["ticker"]) for l in lignes}
    with open(f, "a", newline="", encoding="utf-8") as h:
        w = csv.writer(h)
        if neuf:
            w.writerow(["date", "ticker", "signal", "prix", "rendement", "resultat"])
        for m in top30 + petites + res.get("indices", []):
            if (jour, m["ticker"]) not in deja_notes:
                w.writerow([jour, m["ticker"], m["signal"], m["prix"], "", ""])
                deja_notes.add((jour, m["ticker"]))
    lignes = list(csv.DictReader(open(f, encoding="utf-8")))

    # Historique long de tous les titres suivis (une ligne par titre et par jour)
    h = DATA / "historique.csv"
    champs = ["date", "ticker", "nom", "categorie", "prix", "var_1j", "var_1m", "var_3m",
              "rsi", "volatilite", "liquidite", "signal", "score"]
    existe = h.exists()
    deja_h = set()
    if existe:
        deja_h = {(l["date"], l["ticker"]) for l in csv.DictReader(open(h, encoding="utf-8"))}
    with open(h, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=champs, extrasaction="ignore")
        if not existe:
            w.writeheader()
        for m in tous.values():
            if (jour, m["ticker"]) not in deja_h:
                w.writerow({"date": jour, "score": m.get("score", ""), **m})

    sortie = {
        "date": jour,
        "genere_le": datetime.now().isoformat(timespec="minutes"),
        "indices": res.get("indices", []), "devises": res.get("devises", []),
        "matieres": res.get("matieres", []),
        "top30": top30, "petites": petites,
        "bilan_signaux": bilan(lignes),
        "nb_suivis": len(tous),
        "regles": {
            "score": "35 % perf. 3 mois + 25 % perf. 1 mois + 15 % perf. 1 semaine + 15 % tendance "
                     "(prix > moyennes 20/50/200 j) + 10 % faible volatilité ; −10 si RSI > 75",
            "signal": "hausse si prix > MM20 > MM50 et RSI < 70 ; baisse si prix < MM20 < MM50 et RSI > 30 ; "
                      f"jugé {HORIZON} séances plus tard",
            "filtres": f"liquidité ≥ {LIQ_MIN:,} €/jour (top 30), ≥ {LIQ_MIN_PETITES:,} €/jour et prix "
                       f"entre {PRIX_MIN_PETITES} et 2 € (petits prix)".replace(",", " "),
        },
    }
    (DATA / "jours" / f"{jour}.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    print(f"OK {jour} : {len(tous)} titres, top30={len(top30)}, petites={len(petites)}")


def _recent(m, tous):
    """Exclut les titres dont le dernier cours a plus de 5 jours (suspendus, radiés)."""
    plus_recent = max(x["date_cours"] for x in tous.values())
    return (pd.Timestamp(plus_recent) - pd.Timedelta(days=5)).date().isoformat()


def _petites_recentes(jour, n):
    vus = set()
    fichiers = sorted((DATA / "jours").glob("*.json"))
    fichiers = [f for f in fichiers if f.stem < jour][-n:]
    for f in fichiers:
        vus |= {m["ticker"] for m in json.loads(f.read_text(encoding="utf-8"))["petites"]}
    return vus


if __name__ == "__main__":
    main()
