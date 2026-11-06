"""Collecte quotidienne : prix, indicateurs, top 30 PEA, 10 titres < 2 €, suivi des signaux,
suggestions du jour et suivi des investissements notés par le propriétaire.

Usage : python scripts/collecte.py [AAAA-MM-JJ] [ouverture|cloture]   (par défaut : aujourd'hui, cloture)
- ouverture (vers 9 h 15) : premiers cours de la séance. Rien n'est ajouté à l'historique ni aux signaux.
- cloture (vers 17 h 55) : attend que le fixing de clôture soit publié, puis cours de clôture, la
  référence. Historique et signaux mis à jour.
Codes de sortie : 0 = OK ; 3 = cours du jour (ou clôture définitive) pas encore publiés ; 4 = Bourse fermée.
Lit : univers.json, mes-investissements.md (rempli par le propriétaire, jamais modifié par le programme).
Produit : data/jours/AAAA-MM-JJ.json, data/historique.csv, data/signaux.csv
Ce n'est pas un conseil en investissement.
"""
import csv
import json
import math
import re
import statistics
import sys
import time
import unicodedata
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
DEVISES = {"PA": "EUR", "AS": "EUR", "BR": "EUR", "LS": "EUR", "IR": "EUR", "DE": "EUR", "F": "EUR", "MI": "EUR",
           "MC": "EUR", "HE": "EUR", "AT": "EUR", "VI": "EUR", "CO": "DKK", "ST": "SEK", "OL": "NOK"}
FICHIER_INV = RACINE / "mes-investissements.md"
NB_SUGGESTIONS = 5
ISIN = re.compile(r"[A-Z]{2}[A-Z0-9]{9}\d")
TYPES_INV = {"etf": "etf", "tracker": "etf", "action": "actions", "actions": "actions",
             "fonds": "fonds", "opcvm": "fonds", "sicav": "fonds", "fcp": "fonds"}


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


def devise_de(t):
    """Devise de cotation d'un titre, d'après sa place (suffixe du code Yahoo) ; None si inconnue."""
    if t.startswith("^") or "=" in t or "." not in t:
        return None
    return DEVISES.get(t.rsplit(".", 1)[1])


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


# ---------- mes investissements (fichier rempli par le propriétaire) ----------

def _sans_accents(txt):
    return "".join(c for c in unicodedata.normalize("NFKD", str(txt)) if not unicodedata.combining(c)).lower()


def nombre_fr(txt):
    """« 1 234,56 € », « 1.234,56 » ou « 512.3 » -> nombre ; vide ou illisible -> None."""
    t = re.sub(r"[\s\xa0 €$]", "", str(txt or ""))
    if not t:
        return None
    if "," in t and "." in t:  # le dernier séparateur est celui des décimales
        t = t.replace(".", "").replace(",", ".") if t.rfind(",") > t.rfind(".") else t.replace(",", "")
    else:
        t = t.replace(",", ".")
    try:
        x = float(t)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def date_iso(txt):
    """« 2026-11-06 », « 06/11/2026 » ou « 6/11/26 » -> « 2026-11-06 » ; date impossible -> None."""
    t = str(txt or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        a, mo, j = m.groups()
    else:
        m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2}|\d{4})", t)
        if not m:
            return None
        j, mo, a = m.groups()
        a = "20" + a if len(a) == 2 else a
    try:
        return date(int(a), int(mo), int(j)).isoformat()
    except ValueError:
        return None


def _colonne(titre):
    """Nom interne d'une colonne du tableau, d'après son titre (sans accents, en minuscules)."""
    for mot, cle in (("code", "code"), ("nombre", "quantite"), ("quantit", "quantite"), ("parts", "quantite"),
                     ("nom", "nom"), ("date", "date"), ("prix", "prix"), ("type", "type")):
        if mot in titre:
            return cle
    return None


def lire_investissements(texte):
    """Lit le tableau de mes-investissements.md : une entrée par achat (code Yahoo obligatoire ; nom,
    date, prix d'achat, quantité et type facultatifs). Seul le premier tableau qui a une colonne « Code »
    compte ; les colonnes sont reconnues à leur titre, dans n'importe quel ordre."""
    cles, out = None, []
    for brut in texte.splitlines():
        l = brut.strip()
        if not l.startswith("|"):
            if cles is not None:
                break  # fin du tableau
            continue
        cellules = [c.strip() for c in l.strip("|").split("|")]
        if cles is None:
            titres = [_sans_accents(c) for c in cellules]
            if any("code" in x for x in titres):
                cles = [_colonne(x) for x in titres]
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cellules if c):  # ligne de séparation
            continue
        v = dict(zip(cles, cellules))
        code = (v.get("code") or "").strip("`* ").upper()
        if not code or code in ("-", "—"):
            continue
        prix, q = nombre_fr(v.get("prix")), nombre_fr(v.get("quantite"))
        out.append({"ticker": code, "nom": (v.get("nom") or "").strip("`* ") or None,
                    "date": date_iso(v.get("date")),
                    "prix": prix if prix and prix > 0 else None, "quantite": q if q and q > 0 else None,
                    "type": TYPES_INV.get(_sans_accents(v.get("type") or "").strip())})
    return out


def mes_investissements(entrees, mesure_de, categories, jour):
    """Regroupe les achats par titre et les compare au prix du jour : prix de revient (moyenne pondérée
    par les quantités, sinon moyenne simple), évolution depuis l'achat et, si toutes les quantités sont
    notées, valeur, plus-value et variation du jour en euros. mesure_de(t) : mesures du titre ou None ;
    categories : ticker -> catégorie dans univers.json."""
    groupes, erreurs = {}, []
    for e in entrees:
        if ISIN.fullmatch(e["ticker"]):
            erreurs.append({"ticker": e["ticker"], "message": "ISIN pas encore dans les titres suivis par la "
                                                              "fiche : donne-le à Claude pour qu'il ajoute le titre"})
        else:
            groupes.setdefault(e["ticker"], []).append(e)
    lignes = []
    for t, achats in groupes.items():
        m = mesure_de(t)
        if not m or not m.get("prix"):
            erreurs.append({"ticker": t, "message": "aucun cours trouvé chez Yahoo Finance pour ce code"})
            continue
        p, v = m["prix"], m.get("var_1j")
        achats = sorted(achats, key=lambda a: a["date"] or "")
        complet = all(a["prix"] and a["quantite"] for a in achats)
        q = sum(a["quantite"] for a in achats) if complet else None
        investi = sum(a["prix"] * a["quantite"] for a in achats) if complet else None
        connus = [a["prix"] for a in achats if a["prix"]]
        pru = investi / q if complet else (statistics.mean(connus) if connus else None)
        var_jour = None
        if complet and v is not None and v > -100:  # un achat du jour compte depuis son prix d'achat
            var_jour = sum(a["quantite"] * (p - a["prix"]) if a["date"] == jour
                           else a["quantite"] * p * (1 - 1 / (1 + v / 100)) for a in achats)
        ligne = dict(m)  # copie : le top 30 n'est pas touché
        ligne.update(
            ticker=t, nom=next((a["nom"] for a in achats if a["nom"]), None) or m.get("nom") or t,
            categorie=next((a["type"] for a in achats if a["type"]), None) or categories.get(t)
            or ("fonds" if t.startswith("0P") else "actions"),
            achats=[{k: a[k] for k in ("date", "prix", "quantite")} for a in achats],
            depuis=next((a["date"] for a in achats if a["date"]), None),
            prix_revient=r(pru, 4), pru_pondere=complet, quantite=r(q, 4),
            perf_achat=r((p / pru - 1) * 100) if pru else None,
            investi=r(investi), valeur=r(q * p) if complet else None,
            plus_value=r(q * p - investi) if complet else None, var_jour_eur=r(var_jour))
        lignes.append(ligne)
    avec = [l for l in lignes if l["valeur"] is not None and (l.get("devise") or "EUR") == "EUR"]  # total en euros
    total = None
    if avec:
        inv, val = sum(l["investi"] for l in avec), sum(l["valeur"] for l in avec)
        vj = sum(l["var_jour_eur"] or 0 for l in avec)
        total = {"investi": r(inv), "valeur": r(val), "plus_value": r(val - inv),
                 "perf": r((val / inv - 1) * 100) if inv else None, "var_jour_eur": r(vj),
                 "var_jour": r(vj / (val - vj) * 100) if val - vj else None, "complet": len(avec) == len(lignes)}
    return {"lignes": lignes, "erreurs": erreurs, "total": total}


def catalogue(res):
    """Titres que la barre de recherche « Mes investissements » peut trouver : tous les ETF et actions
    suivis, avec leur prix du jour (fiches.py y ajoute l'ISIN)."""
    cles = ("ticker", "nom", "categorie", "prix", "devise", "var_1j", "var_1m", "date_cours", "signal", "rsi")
    out = [{k: m.get(k) for k in cles} for c in ("etf", "etf_levier", "actions", "petites") for m in res.get(c, [])]
    for x, m in zip(out, [m for c in ("etf", "etf_levier", "actions", "petites") for m in res.get(c, [])]):
        if m.get("levier"):
            x["levier"] = True
    return out


# ---------- suggestions du jour ----------

def _pc(x):
    return "n.d." if x is None else f"{x:+.1f}\u00a0%".replace(".", ",")


def suggestions(candidats, top30, signaux_veille, top30_veille, deja, n=NB_SUGGESTIONS):
    """Jusqu'à n actions à regarder de plus près, choisies par des règles chiffrées et publiées (ce n'est
    pas une liste d'achats). Chaque règle propose son meilleur titre (deux au plus) avec une raison
    factuelle ; les titres déjà suggérés les jours précédents (deja) passent après les autres."""
    dans_top = {m["ticker"] for m in top30}
    ok = lambda m, *cles: all(m.get(k) is not None for k in cles)
    regles = [
        ("nouveau_signal", "Nouveau signal «\u00a0hausse\u00a0»",
         lambda m: ok(m, "rsi") and m.get("signal") == "hausse"
         and signaux_veille.get(m["ticker"]) in ("neutre", "baisse"),
         lambda m: -(m.get("score") or 0),
         lambda m: f"Le signal technique passe de «\u00a0{signaux_veille[m['ticker']]}\u00a0» à «\u00a0hausse\u00a0» : prix "
                   f"au-dessus de ses moyennes 20 et 50 jours, sans surchauffe (RSI {m['rsi']:.0f}). "
                   "Sa fiabilité est mesurée en bas de page."),
        ("entree_top30", "Nouveau dans le top 30",
         lambda m: bool(top30_veille) and m["ticker"] in dans_top and m["ticker"] not in top30_veille,
         lambda m: -(m.get("score") or 0),
         lambda m: f"Entre dans le top 30 aujourd'hui avec un score de {m.get('score') or 0:.0f}/100 "
                   f"({_pc(m.get('var_1m'))} sur 1 mois, {_pc(m.get('var_3m'))} sur 3 mois)."),
        ("plus_haut", "Au plus haut sur un an",
         lambda m: ok(m, "ecart_haut", "var_3m", "rsi") and m["ecart_haut"] >= -1 and m["var_3m"] > 0,
         lambda m: -m["var_3m"],
         lambda m: f"À moins de 1 % de son plus haut sur un an, après {_pc(m['var_3m'])} en 3 mois. RSI "
                   f"{m['rsi']:.0f}" + (" : la hausse est déjà forte, le risque de repli augmente."
                                        if m["rsi"] > 70 else ".")),
        ("repli", "Repli dans une tendance haussière",
         lambda m: ok(m, "ma200", "rsi", "prix") and m["prix"] > m["ma200"] and m["rsi"] < 40,
         lambda m: m["rsi"],
         lambda m: f"Toujours au-dessus de sa moyenne 200 jours (tendance de fond haussière), mais en repli "
                   f"récent : {_pc(m.get('var_1m'))} sur 1 mois, RSI {m['rsi']:.0f}. Un repli peut aussi durer."),
        ("forte_variation", "Gros mouvement du jour",
         lambda m: ok(m, "var_1j") and abs(m["var_1j"]) >= 3,
         lambda m: -abs(m["var_1j"]),
         lambda m: f"{_pc(m['var_1j'])} sur la séance : un mouvement inhabituel, souvent lié à une annonce "
                   "(résultats, contrat, avertissement). Mieux vaut comprendre pourquoi avant tout."),
    ]
    choisis, vus = [], set()
    for passe in range(2):  # 1er passage : un titre par règle ; 2e : un second si de la place reste
        for cle, lib, garde, tri, raison in regles:
            if len(choisis) >= n:
                break
            possibles = sorted((m for m in candidats if m["ticker"] not in vus and garde(m)),
                               key=lambda m: (m["ticker"] in deja, tri(m)))
            if passe:
                possibles = [m for m in possibles if m["ticker"] not in deja]
            if possibles:
                m = possibles[0]
                vus.add(m["ticker"])
                choisis.append(dict(m, critere=cle, critere_lib=lib, raison=raison(m),
                                    deja_suggere=m["ticker"] in deja))
    return choisis


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
    # Investissements notés par le propriétaire : une erreur dans le fichier ne doit jamais bloquer la fiche
    try:
        entrees = lire_investissements(FICHIER_INV.read_text(encoding="utf-8")) if FICHIER_INV.exists() else []
        connus = _isins_connus(u) if any(ISIN.fullmatch(e["ticker"]) for e in entrees) else {}
        for e in entrees:  # un ISIN connu est remplacé par le code Yahoo du titre
            if e["ticker"] in connus:
                e["isin"], e["ticker"] = e["ticker"], connus[e["ticker"]]
    except Exception as e:  # noqa: BLE001
        print("mes-investissements.md illisible :", e, file=sys.stderr)
        entrees = []
    tickers = sorted({t for c in cats for t in u[c]}
                     | {e["ticker"] for e in entrees if not ISIN.fullmatch(e["ticker"])})
    df = telecharger(tickers)

    res = {c: [] for c in cats}
    for c in cats:
        for t, nom in u[c].items():
            m = mesures(df, t)
            if m:
                # ETF à effet de levier : des ETF comme les autres, mais hors classements (trop risqués)
                m.update(ticker=t, nom=nom, categorie="etf" if c == "etf_levier" else c, signal=signal(m))
                if c in ("etf", "etf_levier", "actions", "petites"):
                    m["devise"] = devise_de(t)
                if c == "etf_levier":
                    m["levier"] = True
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

    # Suggestions et investissements : sections en plus, qui ne doivent jamais bloquer la fiche
    try:
        seance = max(m["date_cours"] for m in pea)  # cours de la dernière séance seulement
        sugg = suggestions([m for m in pea if m["categorie"] in ("actions", "petites") and m["date_cours"] == seance],
                           top30, _signaux_veille(jour), _top30_veille(jour), _suggestions_recentes(jour, 3))
    except Exception as e:  # noqa: BLE001
        print("Suggestions impossibles :", e, file=sys.stderr)
        sugg = []
    categories = {t: "etf" if c == "etf_levier" else c for c in cats for t in u[c]}

    def mesure_de(t):
        if t in tous:
            return tous[t]
        m = mesures(df, t)
        if m:
            m["signal"] = signal(m)
        m = m or _prix_simple(df, t)
        if m:
            m["devise"] = devise_de(t)
        return m

    try:
        mes = mes_investissements(entrees, mesure_de, categories, jour)
    except Exception as e:  # noqa: BLE001
        print("Calcul de mes investissements impossible :", e, file=sys.stderr)
        mes = {"lignes": [], "erreurs": [{"ticker": "—", "message": f"calcul impossible ({e})"}], "total": None}

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
        "suggestions": sugg, "mes_investissements": mes, "catalogue": catalogue(res),
        "bilan_signaux": bilan(lignes),
        "nb_suivis": len(tous),
        "regles": {
            "score": "35 % perf. 3 mois + 25 % perf. 1 mois + 15 % perf. 1 semaine + 15 % tendance "
                     "(prix > moyennes 20/50/200 j) + 10 % faible volatilité ; −10 si RSI > 75",
            "signal": "hausse si prix > MM20 > MM50 et RSI < 70 ; baisse si prix < MM20 < MM50 et RSI > 30 ; "
                      f"jugé {HORIZON} séances plus tard",
            "filtres": f"liquidité ≥ {LIQ_MIN:,} €/jour (top 30), ≥ {LIQ_MIN_PETITES:,} €/jour et prix "
                       f"entre {PRIX_MIN_PETITES} et 2 € (petits prix)".replace(",", " "),
            "suggestions": f"jusqu'à {NB_SUGGESTIONS} actions assez échangées, une par règle : nouveau signal "
                           "« hausse », entrée dans le top 30, plus haut sur un an après une hausse sur 3 mois, "
                           "repli (RSI < 40) au-dessus de la moyenne 200 jours, variation d'au moins 3 % sur la "
                           "séance ; les titres suggérés les 3 jours précédents passent après les autres",
        },
    }
    (DATA / "jours" / f"{jour}.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    print(f"OK {jour} ({moment}) : {len(tous)} titres, top30={len(top30)}, petites={len(petites)}, "
          f"suggestions={len(sugg)}, mes investissements={len(mes['lignes'])}"
          + (f" ({len(mes['erreurs'])} à corriger)" if mes["erreurs"] else ""))


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


def _jours_avant(jour):
    return [p for p in sorted((DATA / "jours").glob("20*.json")) if p.stem < jour]


def _suggestions_recentes(jour, n):
    """Titres suggérés les n jours précédents (pour varier les suggestions)."""
    return {s["ticker"] for p in _jours_avant(jour)[-n:]
            for s in json.loads(p.read_text(encoding="utf-8")).get("suggestions", [])}


def _top30_veille(jour):
    """Top 30 de la fiche précédente (vide s'il n'y en a pas)."""
    avant = _jours_avant(jour)
    return {m["ticker"] for m in json.loads(avant[-1].read_text(encoding="utf-8"))["top30"]} if avant else set()


def _signaux_veille(jour):
    """Signal de chaque titre à la dernière clôture enregistrée avant ce jour (data/historique.csv)."""
    f = DATA / "historique.csv"
    if not f.exists() or f.stat().st_size == 0:
        return {}
    lignes = [l for l in csv.DictReader(open(f, encoding="utf-8")) if l["date"] < jour]
    if not lignes:
        return {}
    dernier = max(l["date"] for l in lignes)
    return {l["ticker"]: l["signal"] for l in lignes if l["date"] == dernier}


def _isins_connus(u):
    """ISIN -> code Yahoo des titres suivis, d'après les caractéristiques gardées dans data/fiches/."""
    par_fichier = {re.sub(r"[^A-Za-z0-9.-]", "_", t): t for c in u if not c.startswith("_") for t in u[c]}
    out = {}
    for f in (DATA / "fiches").glob("*.json"):
        try:
            isin = json.loads(f.read_text(encoding="utf-8"))["infos"].get("isin")
        except (ValueError, KeyError, AttributeError):
            continue
        if isin and f.stem in par_fichier:
            out[isin] = par_fichier[f.stem]
    return out


def _prix_simple(df, t):
    """Dernier cours d'un titre dont l'historique est trop court pour les indicateurs (fonds récent…)."""
    try:
        s = df[t]["Close"].dropna()
    except (KeyError, TypeError):
        return None
    if s.empty:
        return None
    p = float(s.iloc[-1])
    return {"prix": r(p, 4 if p < 10 else 2), "date_cours": str(s.index[-1].date()), "var_1j": r(var(s, 1)),
            "var_1m": r(var(s, 21)), "var_3m": r(var(s, 63)), "signal": "neutre",
            "courbe": [r(x, 4) for x in s.tail(60).tolist()]}


if __name__ == "__main__":
    main()
