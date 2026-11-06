"""Contrôle croisé des prix : Yahoo Finance vs Boursorama vs Financial Times.

Usage : python scripts/verif.py AAAA-MM-JJ
Complète data/jours/AAAA-MM-JJ.json : pour chaque titre affiché (indices, devises, top 30,
petits prix, suggestions, mes investissements), ajoute les prix des autres sources, un prix de référence (médiane) et un statut :
  ok      toutes les sources disponibles sont d'accord (écart ≤ tolérance)
  ecart   au moins une source s'écarte : à vérifier avant toute décision
  seul    aucune autre source n'a pu être lue
Quantalys n'est pas interrogé : le site bloque les robots (vérification anti-robot).
Requêtes espacées (≈1 s) pour rester discret ; codes trouvés gardés dans data/correspondances.json.
"""
import json
import re
import statistics
import sys
import time
from pathlib import Path

import requests

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
      "Accept-Language": "fr-FR,fr;q=0.9"}
PAUSE = 0.9
TOL = 1.0  # % d'écart toléré (places de cotation et arrondis légèrement différents)

INDICES = {  # ticker Yahoo -> (code Boursorama, code FT)
    "^FCHI": ("1rPCAC", "CAC:PAR"), "^SBF120": ("1rPPX4", None),
    "^STOXX50E": ("2cSX5E", "SX5E:STX"), "^STOXX": ("2cSXXP", "SXXP:STX"),
    "^GDAXI": ("5pDAX", "DAX:GER"), "^FTSE": ("UKX", "FTSE:FSI"),
    "^GSPC": (None, "INX:IOM"), "^IXIC": ("$COMPX", "COMP:NAS"), "^NDX": (None, "NDX:NAS"),
    "^DJI": ("$INDU", "DJI:DJI"), "^HSI": (None, "HSI:HKG"),
}
PLACES = {  # suffixe Yahoo -> (préfixe Boursorama, place FT)
    "PA": ("1rP", "PAR"), "AS": ("1rA", "AEX"), "DE": ("1z", "FRA"), "MI": ("1g", "MIL"),
    "MC": ("FF55-", "MCE"), "CO": (None, "CPH"), "AT": (None, "ATH"), "HE": (None, "HEL"),
}

session = requests.Session()
session.headers.update(UA)


def nombre(txt, style):
    txt = txt.strip().replace(" ", "").replace("\xa0", "")
    if style == "fr":
        txt = txt.replace(" ", "").replace(",", ".")
    else:
        txt = txt.replace(",", "")
    try:
        return float(txt)
    except ValueError:
        return None


def get(url):
    time.sleep(PAUSE)
    try:
        r = session.get(url, timeout=20)
        return r if r.status_code == 200 else None
    except requests.RequestException:
        return None


MOIS_EN = {m: i for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                                        "Oct", "Nov", "Dec"), 1)}


def date_bourso(page):
    """Date (AAAA-MM-JJ) du dernier cours affiché par une page Boursorama, ou None."""
    i = page.find("data-ist-last")
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", page[i:i + 6000] if i >= 0 else page)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def date_ft(page):
    """Date (AAAA-MM-JJ) du cours d'une page du Financial Times (« as of Nov 06 2026 »), ou None."""
    m = re.search(r"as of ([A-Z][a-z]{2}) (\d{2}) (\d{4})", page)
    return f"{m.group(3)}-{MOIS_EN[m.group(1)]:02d}-{m.group(2)}" if m and m.group(1) in MOIS_EN else None


def boursorama_date(code):
    """(prix, date du cours) lus sur Boursorama, ou (None, None)."""
    r = get(f"https://www.boursorama.com/cours/{code}/")
    # Code inconnu -> redirection vers la recherche : on rejette
    if not r or f"/cours/{code}".lower().replace("$", "%24") not in r.url.lower().replace("$", "%24"):
        return None, None
    m = re.search(r"data-ist-last>([^<]+)", r.text)
    return (nombre(m.group(1), "fr") if m else None), date_bourso(r.text)


def boursorama(code):
    return boursorama_date(code)[0]


def ft_date(genre, code):
    """(prix, date du cours) lus sur le Financial Times, ou (None, None)."""
    r = get(f"https://markets.ft.com/data/{genre}/tearsheet/summary?s={code}")
    if not r or "summary" not in r.text[:5000].lower():
        return None, None
    m = re.search(r'mod-ui-data-list__value">([^<]+)', r.text)
    return (nombre(m.group(1), "en") if m else None), date_ft(r.text)


def ft(genre, code):
    return ft_date(genre, code)[0]


def source_perimee(date_source, jour, date_yahoo=None):
    """Règle du propriétaire (06/11) : une source qui ne donne que le cours d'un jour précédent n'est pas
    prise en compte. On attend le cours du jour, ou celui de la dernière séance du titre si Yahoo
    lui-même n'a pas encore de cours du jour (marché pas encore ouvert). Date inconnue : gardée."""
    if not date_source:
        return False
    return date_source < min(jour, date_yahoo or jour)


def codes(m):
    t, cat = m["ticker"], m["categorie"]
    if cat == "indices":
        b, f = INDICES.get(t, (None, None))
        return b, ("indices", f) if f else None
    if cat == "devises":
        return None, ("currencies", t.replace("=X", ""))
    if "." not in t:
        return None, None
    base, place = t.rsplit(".", 1)
    pb, pf = PLACES.get(place, (None, None))
    if cat == "etf" and place == "PA":
        return f"1rT{base}", ("etfs", f"{base}:PAR:EUR")
    b = f"{pb}{base}" if pb else None
    f = ("equities", f"{base.replace('-', ' ')}:{pf}") if pf else None
    return b, f


def main():
    jour = sys.argv[1]
    fj = DATA / "jours" / f"{jour}.json"
    d = json.loads(fj.read_text(encoding="utf-8"))
    # En séance, les sources n'ont pas le même décalage (temps réel ou 15 min) : tolérance plus large
    tol = 2.0 if d.get("moment") == "ouverture" else TOL
    fc = DATA / "correspondances.json"
    cache = json.loads(fc.read_text(encoding="utf-8")) if fc.exists() else {}

    a_verifier = (d["indices"] + [x for x in d["devises"] if x["ticker"] == "EURUSD=X"]
                  + d["top30"] + d["petites"] + d.get("suggestions", [])
                  + (d.get("mes_investissements") or {}).get("lignes", []))
    vus, bilan = {}, {"ok": 0, "ecart": 0, "seul": 0, "ecarts": []}
    for m in a_verifier:
        t = m["ticker"]
        if t in vus:
            m.update(vus[t])
            continue
        bc, fcode = codes(m)
        echecs = cache.get(t, {}).get("echecs", {})  # source -> nb d'échecs d'affilée
        src = {"yahoo": m["prix"]}
        perimees = {}
        for nom_src, code, lire in (("boursorama", bc, lambda c: boursorama_date(c)),
                                     ("ft", fcode, lambda c: ft_date(*c))):
            if not code or echecs.get(nom_src, 0) >= 3:  # abandon après 3 échecs
                continue
            p, dt = lire(code)
            if p and source_perimee(dt, jour, m.get("date_cours")):
                perimees[nom_src] = dt  # cours de la veille : écarté (règle du propriétaire)
                echecs.pop(nom_src, None)
            elif p:
                src[nom_src] = p
                echecs.pop(nom_src, None)
            else:
                echecs[nom_src] = echecs.get(nom_src, 0) + 1
        cache[t] = {"boursorama": bc, "ft": fcode[1] if fcode else None, "echecs": echecs}

        ref = statistics.median(src.values())
        ecarts = {k: round((v / ref - 1) * 100, 2) for k, v in src.items()}
        if len(src) == 1:
            statut = "seul"
        else:
            tol_abs = 0.006 / ref * 100  # arrondi à 2 décimales sur les petits prix
            statut = "ok" if all(abs(e) <= max(tol, tol_abs) for e in ecarts.values()) else "ecart"
        info = {"sources": src, "prix_reference": round(ref, 4), "ecarts_sources": ecarts, "verif": statut}
        if perimees:
            info["sources_perimees"] = perimees
        m.update(info)
        vus[t] = info
        bilan[statut] += 1
        if statut == "ecart":
            bilan["ecarts"].append({"ticker": t, "nom": m["nom"], "sources": src})
        print(f"{statut:5} {t:12} {src}")

    # Les mêmes titres apparaissent parfois dans le top 30 et les petits prix : comptés une fois
    d["controle_sources"] = bilan
    fj.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    fc.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Contrôle : {bilan['ok']} ok, {bilan['ecart']} écarts, {bilan['seul']} sans 2e source")


if __name__ == "__main__":
    main()
