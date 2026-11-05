"""Collecte quotidienne : prix, indicateurs, top 30 PEA, 10 titres < 2 €, suivi des signaux.

Usage : python scripts/collecte.py [AAAA-MM-JJ] [ouverture|cloture]   (par défaut : aujourd'hui, cloture)
- ouverture (vers 9 h 15) : premiers cours de la séance. Rien n'est ajouté à l'historique ni aux signaux.
- cloture (vers 17 h 55) : attend que le fixing de clôture soit publié, puis cours de clôture, la
  référence. Historique et signaux mis à jour.
Codes de sortie : 0 = OK ; 3 = cours du jour (ou clôture définitive) pas encore publiés ; 4 = Bourse fermée.
Produit : data/jours/AAAA-MM-JJ.json, data/historique.csv, data/signaux.csv
Aucune donnée personnelle. Ce n'est pas un conseil en investissement.
"""
import csv
import json
import math
import sys
import time
import warnings
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data"
PARIS = ZoneInfo("Europe/Paris")
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
    if not f.exists() or f.stat().st_size == 0:
        return []
    lignes = list(csv.DictReader(open(f, encoding="utf-8")))
    if not lignes:  # fichier avec seulement l'en-tête : rien à juger, et surtout rien à réécrire
        return []
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


def paques(annee):
    """Dimanche de Pâques (calendrier grégorien, algorithme de Meeus)."""
    a, (b, c) = annee % 19, divmod(annee, 100)
    d, e = divmod(b, 4)
    g = (b - (b + 8) // 25 + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mois, jour = divmod(h + l - 7 * m + 114, 31)
    return date(annee, mois, jour + 1)


def bourse_fermee(j):
    """Euronext Paris est fermée le week-end, le 1er janvier, le Vendredi saint, le lundi de Pâques,
    le 1er mai et les 25 et 26 décembre."""
    p = paques(j.year)
    return (j.weekday() >= 5 or (j.month, j.day) in {(1, 1), (5, 1), (12, 25), (12, 26)}
            or j in (p - timedelta(days=2), p + timedelta(days=1)))


def attendre_seance(jour, max_minutes=20):
    """Yahoo diffuse les cours de Paris avec 15 min de décalage : on attend que la séance du jour
    apparaisse pour le CAC 40 (une vérification par minute)."""
    for essai in range(max_minutes):
        try:
            h = yf.Ticker("^FCHI").history(period="5d", interval="1d")
            if len(h) and str(h.index[-1].date()) == jour:
                return True
        except Exception as e:  # réseau, limite de Yahoo
            print("Vérification de la séance :", e, file=sys.stderr)
        if essai < max_minutes - 1:
            print(f"Cours du {jour} pas encore publiés, nouvel essai dans 1 minute…", file=sys.stderr)
            time.sleep(60)
    return False


def enregistrer(jour, tous, top30, petites, res):
    """À la clôture : juge les anciens signaux, note ceux du jour et complète l'historique."""
    lignes = evaluer_signaux(jour, {t: m["prix"] for t, m in tous.items()})
    f = DATA / "signaux.csv"
    neuf = not f.exists() or f.stat().st_size == 0
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
    existe = h.exists() and h.stat().st_size > 0
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

    return lignes


def cloture_dans_meta(m, jour):
    """Vrai si les métadonnées Yahoo (accès « graphique ») montrent un dernier échange daté du jour
    et postérieur de 5 minutes à la fin de la séance continue : le fixing de clôture est publié."""
    rt = m.get("regularMarketTime")
    fin = ((m.get("currentTradingPeriod") or {}).get("regular") or {}).get("end")
    if not rt or not fin:
        return False
    return str(datetime.fromtimestamp(rt, PARIS).date()) == jour and rt >= fin + 5 * 60


def cloture_publiee(jour):
    """Clôture définitive à Paris : fixing de 17 h 35 (14 h 05 les jours de séance courte), diffusé par
    Yahoo avec 15 min de décalage. On vérifie LVMH (très échangée) et le CAC 40."""
    for t in ("MC.PA", "^FCHI"):
        tk = yf.Ticker(t)
        tk.history(period="1d", interval="1d")
        if not cloture_dans_meta(tk.history_metadata or {}, jour):
            return False
    return True


def attendre_cloture(jour, max_minutes=30):
    """N'avance jamais sur des cours provisoires : attend (une vérification par minute) que la clôture
    soit définitive."""
    for essai in range(max_minutes):
        try:
            if cloture_publiee(jour):
                return True
        except Exception as e:  # réseau, limite de Yahoo
            print("Vérification de la clôture :", e, file=sys.stderr)
        if essai < max_minutes - 1:
            print(f"Clôture du {jour} pas encore définitive, nouvel essai dans 1 minute…", file=sys.stderr)
            time.sleep(60)
    return False


def main():
    args = sys.argv[1:]
    aujourdhui = datetime.now(PARIS).date().isoformat()
    jour = args[0] if args else aujourdhui
    moment = args[1] if len(args) > 1 else "cloture"
    if moment not in ("ouverture", "cloture"):
        sys.exit("Le moment doit être « ouverture » ou « cloture ».")
    if bourse_fermee(date.fromisoformat(jour)):
        print(f"FERME {jour} : Bourse de Paris fermée (week-end ou jour férié)")
        sys.exit(4)
    if jour == aujourdhui and not attendre_seance(jour):
        print(f"ATTENTE {jour} : les cours de la séance du jour ne sont pas encore publiés")
        sys.exit(3)
    if jour == aujourdhui and moment == "cloture" and not attendre_cloture(jour):
        print(f"ATTENTE {jour} : la clôture n'est pas encore définitive")
        sys.exit(3)
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

    f = DATA / "signaux.csv"
    if moment == "ouverture":
        # À l'ouverture, les prix sont provisoires : on ne note rien, on lit seulement le bilan
        lignes = list(csv.DictReader(open(f, encoding="utf-8"))) if f.exists() else []
    else:
        lignes = enregistrer(jour, tous, top30, petites, res)
    sortie = {
        "date": jour,
        "moment": moment,
        "genere_le": datetime.now(PARIS).isoformat(timespec="minutes"),
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
    print(f"OK {jour} ({moment}) : {len(tous)} titres, top30={len(top30)}, petites={len(petites)}")


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
