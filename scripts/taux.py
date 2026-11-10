"""Taux directeurs de la BCE : valeur en vigueur et date du dernier changement, lues à la source.

Usage : python scripts/taux.py   (appelé par rendu.py, jamais bloquant)
Source : entrepôt de données de la BCE (data-api.ecb.europa.eu, série FM, taux quotidiens). Jamais un taux
écrit en dur : sans réseau, la fiche affiche le dernier relevé gardé dans data/taux_bce.json, avec sa date.
Information et apprentissage, pas un conseil en investissement.
"""
import csv
import io
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CACHE = RACINE / "data" / "taux_bce.json"
URL = "https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.{s}.LEV?startPeriod={d}&format=csvdata"
SERIES = {"depot": "DFR", "refinancement": "MRR_FR", "pret_marginal": "MLFR"}
PAGE_BCE = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html"


def dernier_changement(points):
    """Valeur en vigueur, date de son entrée en vigueur et valeur précédente, d'une liste [(date, taux)].

    Renvoie None si la liste est vide. « précédent » vaut None si le taux n'a jamais changé sur la période."""
    pts = sorted((d, float(v)) for d, v in points if v not in (None, ""))
    if not pts:
        return None
    actuel = pts[-1][1]
    depuis, avant = pts[0][0], None
    for (_, v0), (d1, v1) in zip(pts, pts[1:]):  # paires voisines (sans option stricte : absente de Python 3.9, celui du Mac)
        if v1 != v0:
            depuis, avant = d1, v0
    return {"taux": actuel, "depuis": depuis, "precedent": avant, "releve": pts[-1][0]}


def lire_csv(texte):
    """Points (date, taux) d'une réponse CSV de la BCE (colonnes TIME_PERIOD et OBS_VALUE)."""
    return [(r["TIME_PERIOD"], r["OBS_VALUE"]) for r in csv.DictReader(io.StringIO(texte))
            if r.get("TIME_PERIOD") and r.get("OBS_VALUE")]


def charger_cache():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def mesurer(depuis="2023-01-01"):
    """Taux lus sur la BCE (garde le cache si la lecture échoue), ou {} si rien n'est connu."""
    import requests
    res = {}
    try:
        for nom, serie in SERIES.items():
            r = requests.get(URL.format(s=serie, d=depuis), timeout=20, headers={"User-Agent": "matin-pea"})
            r.raise_for_status()
            m = dernier_changement(lire_csv(r.text))
            if not m:
                raise ValueError(serie)
            res[nom] = m
    except Exception:
        return charger_cache()
    res["source"] = PAGE_BCE
    try:
        CACHE.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass
    return res


if __name__ == "__main__":
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))
