"""Taux directeurs de la BCE : valeur en vigueur et date du dernier changement, lues à la source.

Usage : python scripts/taux.py   (appelé par rendu.py, jamais bloquant)
Source : entrepôt de données de la BCE (data-api.ecb.europa.eu, série FM, taux quotidiens). Jamais un taux
écrit en dur : sans réseau, la fiche affiche le dernier relevé gardé dans data/taux_bce.json, avec sa date.
Information et apprentissage, pas un conseil en investissement.
"""
import csv
import io
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CACHE = RACINE / "data" / "taux_bce.json"
URL = "https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.{s}.LEV?startPeriod={d}&format=csvdata"
SERIES = {"depot": "DFR", "refinancement": "MRR_FR", "pret_marginal": "MLFR"}
URL_INFLATION = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr"
                 "?format=JSON&geo=EA&coicop18=TOTAL&unit=RCH_A&sinceTimePeriod={d}")
PAGE_INFLATION = "https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_minr/default/table?lang=en"
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


def lire_inflation(donnees):
    """Dernier taux annuel d'inflation (zone euro) d'une réponse JSON d'Eurostat : {"mois", "taux", "precedent"}.

    Renvoie None si la réponse n'a pas la forme attendue ou ne contient aucun mois."""
    try:
        mois = donnees["dimension"]["time"]["category"]["index"]
        val = donnees["value"]
        pts = sorted((m, float(val[str(i)])) for m, i in mois.items() if str(i) in val)
    except (KeyError, TypeError, ValueError, AttributeError):
        return None
    if not pts:
        return None
    res = {"mois": pts[-1][0], "taux": pts[-1][1], "precedent": pts[-2][1] if len(pts) > 1 else None}
    maj = donnees.get("updated")  # date de mise à jour du jeu de données (ex. « 2026-11-18T11:00:00+0100 »)
    if isinstance(maj, str) and re.match(r"\d{4}-\d{2}-\d{2}", maj):
        res["maj"] = maj[:10]  # Eurostat ne marque pas « rapide » ou « finale » : on donne seulement la date
    return res
# Réunions de politique monétaire du Conseil des gouverneurs (jour 1, jour 2 avec décision et conférence de
# presse). Source : calendrier officiel de la BCE, lu le 2026-11-25 ; à revérifier avant la fin de la liste.
REUNIONS = [("2026-12-16", "2026-12-17"), ("2027-02-03", "2027-02-04"), ("2027-03-17", "2027-03-18"),
            ("2027-04-28", "2027-04-29"), ("2027-06-09", "2027-06-10"), ("2027-07-21", "2027-07-22"),
            ("2027-09-08", "2027-09-09"), ("2027-10-27", "2027-10-28"), ("2027-12-15", "2027-12-16")]
PAGE_CALENDRIER = "https://www.ecb.europa.eu/press/calendars/mgcgc/html/index.en.html"
# Réunions du FOMC (comité de la banque centrale américaine) : jour 1, jour 2 (décision). Source : calendrier
# officiel de la Fed, lu le 2026-11-26 ; les dates de 2027 y sont dites provisoires, à revérifier.
REUNIONS_FED = [("2026-12-08", "2026-12-09"), ("2027-01-26", "2027-01-27"), ("2027-03-16", "2027-03-17"),
                ("2027-04-27", "2027-04-28"), ("2027-06-08", "2027-06-09"), ("2027-07-27", "2027-07-28"),
                ("2027-09-14", "2027-09-15"), ("2027-10-26", "2027-10-27"), ("2027-11-16", "2027-11-17")]
PAGE_FED = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"


def prochaine_reunion(jour, reunions=REUNIONS):
    """Première réunion dont le jour de décision n'est pas passé (jour au format AAAA-MM-JJ), ou None."""
    for debut, decision in reunions:
        if decision >= jour:
            return {"debut": debut, "decision": decision, "source": PAGE_CALENDRIER}
    return None


def charger_cache():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def mesurer(depuis="2023-01-01"):
    """Taux lus sur la BCE (garde le cache si la lecture échoue), ou {} si rien n'est connu."""
    import requests
    res = {}
    try:  # inflation (Eurostat) : lue à part, une panne ne retire pas les taux
        import requests as _r
        ri = _r.get(URL_INFLATION.format(d="2026-01"), timeout=20, headers={"User-Agent": "matin-pea"})
        ri.raise_for_status()
        infl = lire_inflation(ri.json())
    except Exception:
        infl = None
    try:
        for nom, serie in SERIES.items():
            r = requests.get(URL.format(s=serie, d=depuis), timeout=20, headers={"User-Agent": "matin-pea"})
            r.raise_for_status()
            m = dernier_changement(lire_csv(r.text))
            if not m:
                raise ValueError(serie)
            res[nom] = m
    except Exception:
        cache = charger_cache()
        if infl:
            cache["inflation"] = infl
        cache["reunions"] = REUNIONS
        cache["source_reunions"] = PAGE_CALENDRIER
        cache["reunions_fed"] = REUNIONS_FED
        cache["source_fed"] = PAGE_FED
        return cache
    res["inflation"] = infl or charger_cache().get("inflation")
    res["source"] = PAGE_BCE
    res["reunions"] = REUNIONS
    res["source_reunions"] = PAGE_CALENDRIER
    res["reunions_fed"] = REUNIONS_FED
    res["source_fed"] = PAGE_FED
    try:
        CACHE.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass
    return res


if __name__ == "__main__":
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))
