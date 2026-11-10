"""Fiches détaillées de chaque titre affiché sur la fiche du jour.

Usage : python scripts/fiches.py AAAA-MM-JJ   (après collecte.py et verif.py)
Ajoute « details » à data/jours/AAAA-MM-JJ.json, pour chaque indice, devise, matière première,
titre du top 30, petit prix, suggestion du jour et investissement noté par le propriétaire :
- historique de prix : 14 mois en quotidien et 5 ans en hebdomadaire (graphique interactif) ;
- statistiques : performances, plus haut et plus bas, volatilité, pire baisse, bêta face au CAC 40 ;
- risque : SRI officiel du DIC (document PRIIPs) pour les ETF, lu sur Boursorama ; pour les
  actions (qui n'ont pas de DIC), SRI estimé à partir de la volatilité sur 5 ans avec les seuils PRIIPs ;
- frais : frais de gestion des ETF, plafonds légaux du PEA, taxe sur les transactions financières ;
- caractéristiques : ISIN, éligibilité PEA indiquée par Boursorama, secteur, valorisation, PER…
Les caractéristiques sont gardées 7 jours dans data/fiches/ pour limiter les requêtes.
Aucun texte n'est copié des sites : seulement des données chiffrées et factuelles.
"""
import base64
import csv
import html as H
import json
import math
import re
import sys
import warnings
from datetime import date
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import yfinance as yf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verif import codes, get  # noqa: E402  mêmes codes de place et même politesse que verif.py

warnings.filterwarnings("ignore")
RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data"
CACHE = DATA / "fiches"
VALIDITE_JOURS = 7
NB_NOUVEAUX_ISIN = 60  # titres du catalogue sans cache lus sur Boursorama par passage (complété peu à peu)
SEUILS_SRI = [0.5, 5, 12, 20, 30, 80]  # volatilité annuelle (%) -> classes 1 à 7 (PRIIPs, risque de marché)
PLACES = {"PA": ("Euronext Paris", "EUR"), "AS": ("Euronext Amsterdam", "EUR"),
          "DE": ("Xetra (Francfort)", "EUR"), "MI": ("Borsa Italiana (Milan)", "EUR"),
          "MC": ("Bourse de Madrid", "EUR"), "CO": ("Nasdaq Copenhague", "DKK"),
          "HE": ("Nasdaq Helsinki", "EUR"), "AT": ("Bourse d'Athènes", "EUR")}
VIDES = {"-", "ND", "NC", "n.d.", ""}
ETF_CHAMPS = {"Date de création": "creation", "Société de gestion": "societe", "Forme juridique": "forme",
              "Classe d'actifs": "classe", "Zone géographique": "zone", "Catégorie morningstar": "categorie_ms",
              "Affectation des résultats": "affectation", "Réplication": "replication",
              "Frais d'entrée": "frais_entree", "Frais de sortie": "frais_sortie",
              "Frais de gestion maximum": "frais_gestion"}


# ---------- lecture des pages Boursorama ----------

def lignes(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = H.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [l.strip() for l in t.split("\n") if l.strip()]


def apres(L, motif, debut=0, exact=True):
    """Valeur qui suit une étiquette, en sautant les bulles d'aide (« …? », « Fermer »)."""
    for i in range(debut, len(L)):
        if (L[i] == motif) if exact else re.match(motif, L[i], re.I):
            for v in L[i + 1:i + 6]:
                if v.endswith("?") or v == "Fermer":
                    continue
                return v
            return None
    return None


def lire_bourso(code, etf):
    url = f"https://www.boursorama.com/cours/{code}/"
    r = get(url)
    if not r or f"/cours/{code}".lower().replace("$", "%24") not in r.url.lower().replace("$", "%24"):
        return {}
    t, L = r.text, lignes(r.text)
    out = {"url_boursorama": r.url}
    for l in L:
        m = re.match(r"^([A-Z]{2}[A-Z0-9]{9}\d)(?:\s+-\s+(.+)|\s+\S+)?$", l)
        if m:
            out["isin"] = m.group(1)
            if m.group(2):
                out["societe"] = m.group(2).strip()
            break
    if "Éligibilité" in L:
        i = L.index("Éligibilité")
        out["pea_bourso"] = "PEA" in L[i + 1:i + 25]
    if etf:
        out["actif_net"] = apres(L, "Actif net (EUR)")
        i = t.find("Risque du fonds (SRI)")
        m = re.search(r'data-gauge-current-step="(\d)"', t[i:i + 900]) if i >= 0 else None
        if m:
            out["sri_officiel"] = int(m.group(1))
        debut = L.index("Caractéristiques") if "Caractéristiques" in L else 0
        for lab, cle in ETF_CHAMPS.items():
            v = apres(L, lab, debut)
            if v and v not in VIDES and v not in ETF_CHAMPS:
                out[cle] = v
        m = re.search(r'data-rel="([A-Za-z0-9+/=]+)"[^>]*title="Télécharger le DIC', t)
        if m:
            try:
                lien = base64.b64decode(m.group(1)).decode()
                if lien.startswith("https://"):
                    out["dic"] = lien
            except ValueError:
                pass
    else:
        for lab, cle, exact in (("secteur (niv. 2)", "secteur", True), ("Indice de référence", "indice", True),
                                ("valorisation", "valorisation", True), (r"^rendement estimé", "rendement", False),
                                (r"^PER estimé", "per", False), ("dernier dividende", "dernier_dividende", True)):
            v = apres(L, lab, exact=exact)
            if v and v not in VIDES:
                out[cle] = v
        m = next((l for l in L if re.match(r"^PER estimé \d{4}$", l)), None)
        if m:
            out["per_annee"] = m[-4:]
    return out


def lire_profil(code):
    r = get(f"https://www.boursorama.com/cours/societe/profil/{code}/")
    if not r or "/profil/" not in r.url:
        return {}
    L = lignes(r.text)
    debut = L.index("Raison sociale") if "Raison sociale" in L else 0
    out = {}
    champs = (("Effectif", "effectif"), ("Nombre de titres", "nb_titres"),
              ("Capitalisation boursière", "capitalisation"), ("Marché", "marche"), ("Site Web", "site"))
    etiquettes = {lab for lab, _ in champs} | {"Dernier coupon", "Dirigeants", "Téléphone", "Fax", "Adresse"}
    for lab, cle in champs:
        v = apres(L, lab, debut)
        if v and v not in etiquettes and v not in VIDES:
            out[cle] = v
    if "Adresse" in L:
        i = L.index("Adresse")
        for j in range(i + 1, min(i + 14, len(L))):
            if L[j] in ("Site Web", "Téléphone", "Effectif", "Fax"):
                avant = [x.strip(" ,") for x in L[i + 1:j] if x.strip(" ,")]
                if len(avant) >= 2:
                    out["pays"] = avant[-1]
                break
    if out.get("site") and not out["site"].startswith("http"):
        out.pop("site")
    return out


def lire_yahoo(t):
    """Repli pour les titres absents de Boursorama (Copenhague, Helsinki, Athènes…)."""
    try:
        i = yf.Ticker(t).info or {}
    except Exception:
        return {}
    out = {"secteur": i.get("sector"), "pays": i.get("country"), "site": i.get("website"),
           "source_infos": "Yahoo Finance"}
    if i.get("marketCap"):
        out["valorisation"] = f"{i['marketCap'] / 1e6:,.0f} M{i.get('currency', '')}".replace(",", " ")
    if i.get("trailingPE"):
        out["per"] = f"{i['trailingPE']:.2f}".replace(".", ",")
    if i.get("dividendYield"):
        y = i["dividendYield"]
        out["rendement"] = f"{(y if y > 1 else y * 100):.2f}%".replace(".", ",")
    if i.get("fullTimeEmployees"):
        out["effectif"] = f"{i['fullTimeEmployees']:,}".replace(",", " ")
    return {k: v for k, v in out.items() if v}


def fichier_cache(t):
    """Fichier de data/fiches/ où sont gardées les caractéristiques d'un titre."""
    return CACHE / (re.sub(r"[^A-Za-z0-9.-]", "_", t) + ".json")


def isin_en_cache(t):
    """ISIN d'un titre d'après le cache, même périmé (un ISIN ne change pas) ; None s'il est inconnu."""
    f = fichier_cache(t)
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))["infos"].get("isin")
    except (ValueError, KeyError, AttributeError):
        return None


def infos(m):
    """Caractéristiques d'un titre, avec un cache de 7 jours."""
    t, cat = m["ticker"], m["categorie"]
    f = fichier_cache(t)
    if f.exists():
        c = json.loads(f.read_text(encoding="utf-8"))
        if (date.today() - date.fromisoformat(c["maj"])).days < VALIDITE_JOURS:
            return c["infos"]
    out = {}
    if cat in ("etf", "actions", "petites", "fonds"):
        bc, _ = codes(m)
        if bc:
            out = lire_bourso(bc, cat == "etf")
            if out and cat != "etf":
                out.update(lire_profil(bc))
        if not out:
            out = lire_yahoo(t)
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"maj": date.today().isoformat(), "infos": out}, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    return out


# ---------- calculs sur les prix ----------

def nombre(txt):
    """« 157 569,38 MEUR » -> 157569.38 ; « 0,15 % » -> 0.15."""
    if not txt:
        return None
    m = re.search(r"-?[\d\s \xa0]+(?:,\d+)?", txt)
    if not m:
        return None
    try:
        return float(re.sub(r"[\s \xa0]", "", m.group(0)).replace(",", "."))
    except ValueError:
        return None


def compacte(s):
    t0 = s.index[0].date()
    return {"t0": t0.isoformat(), "o": [(d.date() - t0).days for d in s.index],
            "c": [float(f"{x:.5g}") for x in s]}


def r1(x, n=1):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), n)


def perte_max(s):
    return r1((s / s.cummax() - 1).min() * 100) if len(s) > 1 else None


def sri_estime(vol):
    if vol is None:
        return None
    for i, seuil in enumerate(SEUILS_SRI):
        if vol < seuil:
            return i + 1
    return 7


def ratios_rendement(rs, periodes=52):
    """Ratios de Sharpe et de Sortino (taux sans risque pris à 0) d'après des rendements périodiques `rs`.
    Sharpe = rendement moyen / écart-type ; Sortino = rendement moyen / écart-type des seules baisses ;
    les deux sont ramenés à l'année. Renvoie (sharpe, sortino), None si la mesure est impossible."""
    rs = rs.dropna()
    if len(rs) < 30:
        return None, None
    sd, bas = rs.std(), math.sqrt((rs.clip(upper=0) ** 2).mean())
    k = math.sqrt(periodes)
    return (r1(rs.mean() / sd * k, 2) if sd > 0 else None), (r1(rs.mean() / bas * k, 2) if bas > 0 else None)


def statistiques(sj, ss, cac):
    out = {}
    an = sj.tail(253)
    rj = an.pct_change().dropna()
    out["vol_1a"] = r1(rj.std() * math.sqrt(252) * 100) if len(rj) > 20 else None
    out["perte_max_1a"] = perte_max(an)
    out["haut_1a"], out["bas_1a"] = r1(an.max(), 4), r1(an.min(), 4)
    out["jours_hausse_1a"] = r1((rj > 0).mean() * 100, 0) if len(rj) else None
    fin_annee = sj[sj.index.year < sj.index[-1].year]
    out["perf_annee"] = r1((sj.iloc[-1] / fin_annee.iloc[-1] - 1) * 100) if len(fin_annee) else None
    if ss is not None and len(ss) > 10:
        rs = ss.pct_change().dropna()
        out["annees_hist"] = r1((ss.index[-1] - ss.index[0]).days / 365.25)
        out["vol_5a"] = r1(rs.std() * math.sqrt(52) * 100)
        out["perte_max_5a"] = perte_max(ss)
        out["pire_semaine"], out["meilleure_semaine"] = r1(rs.min() * 100), r1(rs.max() * 100)
        if out["annees_hist"] >= 2:
            out["sharpe"], out["sortino"] = ratios_rendement(rs)
        if out["annees_hist"] >= 2.9:
            out["perf_3a"] = r1((ss.iloc[-1] / ss[ss.index >= ss.index[-1] - pd.Timedelta(days=1096)].iloc[0] - 1) * 100)
        if out["annees_hist"] >= 4.8:
            out["perf_5a"] = r1((ss.iloc[-1] / ss.iloc[0] - 1) * 100)
        if cac is not None:
            x = pd.concat([rs, cac.pct_change()], axis=1, join="inner").dropna().tail(156)
            if len(x) > 30 and x.iloc[:, 1].var() > 0:
                out["beta_cac"] = r1(x.iloc[:, 0].cov(x.iloc[:, 1]) / x.iloc[:, 1].var(), 2)
    base = out.get("vol_5a") if out.get("annees_hist", 0) >= 2 else out.get("vol_1a")
    out["sri_estime"] = sri_estime(base)
    a = out.get("annees_hist", 0)
    out["sri_base"] = "5 ans" if a >= 4.8 else (f"{a:.1f} ans".replace(".", ",") if a >= 2 else "1 an")
    return out


def stats_seance(b, jour):
    """Prix moyen pondéré par les volumes (VWAP), plus haut et plus bas de la séance du jour,
    à partir de barres de 5 minutes (colonnes High, Low, Close, Volume)."""
    if b is None or b.empty:
        return None
    b = b.dropna(subset=["Close"])
    idx = b.index.tz_convert("Europe/Paris") if b.index.tz is not None else b.index
    b = b[[str(x.date()) == jour for x in idx]]
    if b.empty:
        return None
    out = {"haut_jour": r1(b["High"].max(), 4), "bas_jour": r1(b["Low"].min(), 4)}
    v = b["Volume"].fillna(0)
    if v.sum() > 0:
        typique = (b["High"] + b["Low"] + b["Close"]) / 3
        out["vwap"] = r1((typique * v).sum() / v.sum(), 4)
    return out


def lien_yahoo(t):
    """Page Yahoo Finance d'un titre, sur le site international : le site français renvoie une
    erreur 404 pour beaucoup d'ETF et de petites valeurs (constaté par le contrôle du 06/11/2026)."""
    return f"https://finance.yahoo.com/quote/{quote(t, safe='.=-')}/"


def signaux_du_titre(t):
    f = DATA / "signaux.csv"
    if not f.exists():
        return []
    L = [l for l in csv.DictReader(open(f, encoding="utf-8")) if l["ticker"] == t]
    return [{"date": l["date"], "signal": l["signal"], "prix": float(l["prix"]),
             "rendement": float(l["rendement"]) if l["rendement"] else None, "resultat": l["resultat"] or None}
            for l in L[-15:]]


def description_auto(m, inf):
    nom, cat = m["nom"], m["categorie"]
    if cat == "etf":
        bouts = []
        if inf.get("societe"):
            bouts.append(f"géré par {inf['societe']}")
        if inf.get("categorie_ms"):
            bouts.append(f"catégorie « {inf['categorie_ms']} »")
        if inf.get("replication"):
            bouts.append(f"réplication {inf['replication'].lower()}")
        if inf.get("affectation"):
            bouts.append(f"dividendes : {inf['affectation'].lower()}")
        return f"ETF {', '.join(bouts)}." if bouts else ""
    if cat in ("actions", "petites"):
        bouts = []
        if inf.get("secteur"):
            bouts.append(f"secteur « {inf['secteur']} »")
        if inf.get("pays"):
            bouts.append(f"siège : {inf['pays']}")
        if inf.get("effectif"):
            bouts.append(f"{inf['effectif']} salariés")
        return f"{nom} : entreprise cotée ({', '.join(bouts)})." if bouts else ""
    if cat == "fonds":
        bouts = [f"géré par {inf['gestionnaire']}"] if inf.get("gestionnaire") else []
        if inf.get("sfdr"):
            bouts.append(f"classé {inf['sfdr'].lower()} du règlement SFDR")
        return f"Fonds {', '.join(bouts)}, proposé dans les contrats d'assurance vie de Wealins." if bouts else ""
    return ""


def frais(m, inf):
    cat, t = m["categorie"], m["ticker"]
    if cat not in ("etf", "actions", "petites"):
        return None
    out = {"courtage_max": 0.5, "courtage_agence_max": 1.2, "garde_max": 0.4}
    if cat == "etf":
        g = nombre(inf.get("frais_gestion"))
        if g is not None:
            out["gestion"] = g
        for k in ("frais_entree", "frais_sortie"):
            v = nombre(inf.get(k))
            if v is not None:
                out[k.split("_")[1]] = v
    else:
        cap = nombre(inf.get("capitalisation")) or nombre(inf.get("valorisation"))
        unite = (inf.get("capitalisation") or inf.get("valorisation") or "")
        if t.endswith(".PA") and inf.get("isin", "").startswith("FR") and cap and "MEUR" in unite and cap >= 1000:
            out["ttf"] = 0.4
    return out


def infos_en_cache(t):
    """Caractéristiques gardées dans data/fiches/, même périmées (frais et ISIN changent rarement) ; {} sinon."""
    try:
        return json.loads(fichier_cache(t).read_text(encoding="utf-8"))["infos"] or {}
    except (OSError, ValueError, KeyError):
        return {}


def frais_compact(m, inf=None):
    """Frais d'un titre du catalogue, en court pour la page : g = frais de gestion annuels (%), e / s =
    frais d'entrée / de sortie (%), ttf = taxe sur les transactions financières. None si rien n'est connu."""
    fx = frais(m, infos_en_cache(m["ticker"]) if inf is None else inf)
    if not fx:
        return None
    out = {k: fx[c] for k, c in (("g", "gestion"), ("e", "entree"), ("s", "sortie")) if fx.get(c) is not None}
    if m["categorie"] in ("actions", "petites"):
        out["g"] = 0  # une action n'a pas de frais annuels
    if fx.get("ttf"):
        out["ttf"] = 1
    return out or None


def ajouter_frais_catalogue(d):
    """Ajoute « fx » (frais) à chaque titre du catalogue, d'après le cache : sans réseau. Renvoie le nombre."""
    n = 0
    for m in d.get("catalogue", []):
        fx = frais_compact(m)
        if fx:
            m["fx"], n = fx, n + 1
    return n


def fiche_fonds_wealins(m):
    """Fiche détaillée d'un fonds de la liste Wealins (noté dans mes-investissements.md) : historique de la
    valeur liquidative (jusqu'à 5 ans, lu sur la page du fonds), statistiques, gestionnaire, SFDR, DIC.
    None si la page est injoignable ou sans historique."""
    import wealins
    isin = m["ticker"]
    f = wealins.lire_fonds(wealins._get(wealins.url_fonds(isin) + "?period=60"))
    h = f["historique"]
    if len(h) < 2:
        return None
    s = pd.Series([v for _, v in h], index=pd.to_datetime([d for d, _ in h])).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    sj = s[s.index >= s.index[-1] - pd.Timedelta(days=430)]  # 14 mois, comme pour les autres titres
    ss = s.resample("W-FRI").last().dropna()
    devise = m.get("devise") or f["devise"]
    inf = {k: v for k, v in {"isin": isin, "gestionnaire": f["gestionnaire"], "sfdr": f["sfdr"] or m.get("sfdr"),
                             "perf_annee_wealins": f["perf_annee"], "dic": f["dic"],
                             "source_infos": "Wealins"}.items() if v is not None}
    return {"j": compacte(sj), "s": compacte(ss) if len(ss) > 10 else None,
            "stats": statistiques(sj, ss if len(ss) > 10 else None, None), "infos": inf,
            "place": None, "devise": devise,
            "description_auto": description_auto(m, inf), "frais": None, "signaux": [],
            "liens": {k: v for k, v in {"Wealins (fiche du fonds)": wealins.url_fonds(isin),
                                        "Financial Times": wealins.url_ft(isin, devise),
                                        "DIC (document PRIIPs, PDF)": f["dic"]}.items() if v}}


def main():
    if sys.argv[1] == "--frais":  # sans réseau : seulement les frais du catalogue, d'après le cache
        fj = DATA / "jours" / f"{sys.argv[2]}.json"
        d = json.loads(fj.read_text(encoding="utf-8"))
        n = ajouter_frais_catalogue(d)
        fj.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Frais connus : {n}/{len(d.get('catalogue', []))} titres")
        return
    jour = sys.argv[1]
    fj = DATA / "jours" / f"{jour}.json"
    d = json.loads(fj.read_text(encoding="utf-8"))
    tous = {}
    for cle in ("indices", "devises", "matieres", "top30", "petites"):
        for m in d.get(cle, []):
            tous.setdefault(m["ticker"], m)
    # Suggestions du jour et investissements notés par le propriétaire : fiche détaillée aussi
    for m in d.get("suggestions", []) + (d.get("mes_investissements") or {}).get("lignes", []):
        tous.setdefault(m["ticker"], m)
    fonds = {t for t, m in tous.items() if m.get("source") == "wealins"}  # pas sur Yahoo : page Wealins
    tickers = sorted((set(tous) - fonds) | {"^FCHI"})
    dj = yf.download(tickers, period="14mo", interval="1d", auto_adjust=True, group_by="ticker",
                     progress=False, threads=True)
    ds = yf.download(tickers, period="5y", interval="1wk", auto_adjust=True, group_by="ticker",
                     progress=False, threads=True)

    def serie(df, t):
        try:
            s = df[t]["Close"].dropna()
        except (KeyError, TypeError):
            return None
        return s if len(s) > 1 else None

    cac = serie(ds, "^FCHI")
    # À la clôture : barres de 5 minutes de la séance pour le prix moyen du jour (VWAP)
    d5 = None
    if d.get("moment") == "cloture":
        try:
            d5 = yf.download(tickers, period="1d", interval="5m", auto_adjust=False, group_by="ticker",
                             progress=False, threads=True)
        except Exception as e:  # non bloquant
            print("Barres de 5 minutes indisponibles :", e, file=sys.stderr)
    details = {}
    for t in sorted(fonds):
        try:
            det = fiche_fonds_wealins(tous[t])
        except Exception as e:  # noqa: BLE001  un fonds illisible ne bloque jamais la fiche
            print("Fiche du fonds impossible :", t, e, file=sys.stderr)
            det = None
        if det:
            details[t] = det
    for t, m in tous.items():
        if t in fonds:
            continue
        sj, ss = serie(dj, t), serie(ds, t)
        if sj is None:
            continue
        inf = infos(m)
        suffixe = t.rsplit(".", 1)[1] if "." in t and not t.startswith("^") else None
        place, devise = PLACES.get(suffixe, (None, None))
        det = {"j": compacte(sj), "s": compacte(ss) if ss is not None else None,
               "stats": statistiques(sj, ss, cac if m["categorie"] in ("etf", "actions", "petites", "fonds") else None),
               "infos": inf, "place": place, "devise": devise,
               "description_auto": description_auto(m, inf),
               "frais": frais(m, inf), "signaux": signaux_du_titre(t)}
        if d5 is not None:
            try:
                det["seance"] = stats_seance(d5[t], jour)
            except (KeyError, TypeError):
                pass
        bc, fcode = codes(m)
        det["liens"] = {k: v for k, v in {
            "Boursorama": inf.get("url_boursorama") or (f"https://www.boursorama.com/cours/{bc}/" if bc else None),
            "Financial Times": f"https://markets.ft.com/data/{fcode[0]}/tearsheet/summary?s={fcode[1]}" if fcode else None,
            "Yahoo Finance": lien_yahoo(t),
            "DIC (document PRIIPs, PDF)": inf.get("dic"),
            "justETF": f"https://www.justetf.com/fr/etf-profile.html?isin={inf['isin']}"
            if m["categorie"] == "etf" and inf.get("isin") else None,
        }.items() if v}
        details[t] = det
    d["details"] = details
    # Barre de recherche « Mes investissements » : ISIN de chaque titre suivi, lu dans le cache ; les
    # titres jamais lus sont complétés peu à peu (NB_NOUVEAUX_ISIN par passage), sans bloquer la fiche
    nouveaux = 0
    for m in d.get("catalogue", []):
        isin = isin_en_cache(m["ticker"])
        if isin is None and not fichier_cache(m["ticker"]).exists() and nouveaux < NB_NOUVEAUX_ISIN:
            nouveaux += 1
            try:
                isin = infos(m).get("isin")
            except Exception as e:  # noqa: BLE001
                print("ISIN illisible pour", m["ticker"], ":", e, file=sys.stderr)
        if isin:
            m["isin"] = isin
    nb_fx = ajouter_frais_catalogue(d)
    fj.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Frais connus : {nb_fx}/{len(d.get('catalogue', []))} titres")
    nb_sri = sum(1 for x in details.values() if x["infos"].get("sri_officiel"))
    nb_pea = sum(1 for x in details.values() if x["infos"].get("pea_bourso"))
    nb_isin = sum(1 for m in d.get("catalogue", []) if m.get("isin"))
    print(f"Fiches : {len(details)} titres, {nb_sri} SRI officiels, {nb_pea} éligibles PEA selon Boursorama ; "
          f"recherche par ISIN : {nb_isin}/{len(d.get('catalogue', []))} titres ({nouveaux} nouveaux)")


if __name__ == "__main__":
    main()
