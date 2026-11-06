"""Fonds de la liste Wealins (supports d'assurance vie au Luxembourg) pour « Mes investissements ».

Usage : python scripts/wealins.py [--forcer]   (collecte.py l'appelle aussi, une fois par jour)
Actualise data/wealins.json : pour chaque fonds de https://www.wealins.com/funds-list/ (environ
1 350, sur 135 pages), son nom, son ISIN, sa devise, sa dernière valeur liquidative et la date de
cette valeur, plus la valeur précédente (pour la variation). La barre de recherche de la fiche trouve
ainsi chaque fonds par son ISIN ou son nom.

Un fonds calcule sa valeur liquidative une fois par jour, après la clôture, et Wealins la publie le
lendemain : la date de chaque valeur est gardée et affichée. Règle de Mathieu (06/11/2026) : une
source qui ne donne que la valeur d'un jour précédent n'est pas prise en compte quand une autre a une
valeur plus récente ; le Financial Times publie parfois la valeur d'un fonds plus tôt (fonds d'actions
asiatiques, par exemple). mesure() choisit donc la valeur la plus récente des deux.

robots.txt de www.wealins.com : tout est autorisé (lu le 06/11/2026). Requêtes espacées d'une seconde,
aucune protection contournée. Seulement des données chiffrées et factuelles, aucun texte copié.
"""
import html as H
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
# requests et verif sont importés seulement pour lire le web : rendu.py lit le cache sans eux

RACINE = Path(__file__).resolve().parent.parent
CACHE = RACINE / "data" / "wealins.json"
BASE = "https://www.wealins.com"
LISTE = BASE + "/funds-list/"
PAUSE = 1.0           # secondes entre deux pages (politesse)
MAX_PAGES = 400       # garde-fou si la pagination change
OUBLI_JOURS = 14      # un fonds absent de la liste depuis 14 jours n'est plus proposé
PARIS = ZoneInfo("Europe/Paris")
ISIN = re.compile(r"[A-Z]{2}[A-Z0-9]{9}\d")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

_session = None


def _get(url):
    """Requête polie (pause, délai de 20 s, même identité de navigateur que verif.py) ; None en cas
    d'échec ou de réseau bloqué."""
    global _session
    import requests
    if _session is None:
        from verif import UA
        _session = requests.Session()
        _session.headers.update(UA)
    time.sleep(PAUSE)
    try:
        r = _session.get(url, timeout=20)
        return r.text if r.status_code == 200 else None
    except requests.RequestException:
        return None


def _texte(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x or ""))).strip()


def _nombre(txt):
    """« 1323.519 » ou « 1,323.52 » (format anglais) -> 1323.519 ; None si ce n'est pas un prix."""
    try:
        v = float(_texte(txt).replace(",", ""))
    except ValueError:
        return None
    return v if v > 0 else None


def _sfdr(txt):
    t = _texte(txt)
    return t if t.lower().startswith("article") else None


# ---------- lecture des pages ----------

def lire_liste(page):
    """Fonds d'une page de la liste : [{isin, nom, date_vl, devise, vl, sfdr}]."""
    out = []
    for bloc in re.findall(r'<tr class="wsa-table-row[^"]*">(.*?)</tr>', page or "", re.S):
        nom = re.search(r'<th[^>]*scope="row"[^>]*>(.*?)</th>', bloc, re.S)
        cel = dict(re.findall(r'<td data-label="([^"]+)"[^>]*>(.*?)</td>', bloc, re.S))
        isin = _texte(cel.get("ISIN")).upper()
        if not nom or not ISIN.fullmatch(isin):
            continue
        dv = _texte(cel.get("Val.date"))
        devise = _texte(cel.get("Currency")).upper()
        out.append({"isin": isin, "nom": _texte(nom.group(1)), "date_vl": dv if DATE.fullmatch(dv) else None,
                    "devise": devise if re.fullmatch(r"[A-Z]{3}", devise) else None,
                    "vl": _nombre(cel.get("Actual")), "sfdr": _sfdr(cel.get("SFDR"))})
    return out


def nb_pages(page):
    """Nombre de pages de la liste, d'après les liens de pagination (1 s'il n'y en a pas)."""
    n = [int(x) for x in re.findall(r"/funds-list/page/(\d+)/", page or "")]
    return max(n) if n else 1


def lire_fonds(page):
    """Page d'un fonds : nom, ISIN, valeur et date, performance depuis le 1er janvier, gestionnaire, SFDR,
    devise (lue dans le nom des documents), lien du DIC en français et historique [(date, valeur)]."""
    page = page or ""
    champs = {_texte(k).rstrip(":"): v for k, v in re.findall(
        r'<dt class="wsa-fund-graph-top-right-info-list__label">(.*?)</dt>\s*'
        r'<dd class="wsa-fund-graph-top-right-info-list__value">(.*?)</dd>', page, re.S)}
    nom = re.search(r'<h1[^>]*wp-block-post-title[^>]*>(.*?)</h1>', page, re.S)
    isin = _texte(champs.get("ISIN")).upper()
    dv = _texte(champs.get("Val.date"))
    perf = re.fullmatch(r"(-?[\d.]+)\s*%", _texte(champs.get("Year to date performance")))
    docs = re.findall(r'href="(https://www\.e-wealins\.com/fundDocument/([A-Z0-9]{12})_([A-Z]{3})_([A-Z]+)_([A-Z]{2})_[^"]+\.pdf)"', page)
    dic = next((u for u, _, _, genre, langue in docs if genre == "KIDDOC" and langue == "FR"), None) \
        or next((u for u, _, _, genre, _ in docs if genre == "KIDDOC"), None)
    histo = [(d, float(v)) for d, v in re.findall(r'new Date\("(\d{4}-\d{2}-\d{2})T[^"]*"\)\s*,\s*([\d.]+)', page)]
    return {"nom": _texte(nom.group(1)) if nom else None, "isin": isin if ISIN.fullmatch(isin) else None,
            "vl": _nombre(champs.get("Current NAV")), "date_vl": dv if DATE.fullmatch(dv) else None,
            "perf_annee": float(perf.group(1)) if perf else None,
            "gestionnaire": _texte(champs.get("Manager")) or None, "sfdr": _sfdr(champs.get("SFDR")),
            "devise": docs[0][2] if docs else None, "dic": dic, "historique": sorted(histo)}


def url_fonds(isin):
    return f"{BASE}/funds/{isin.lower()}/"


def url_ft(isin, devise):
    return f"https://markets.ft.com/data/funds/tearsheet/summary?s={isin}:{devise or 'EUR'}"


# ---------- cache data/wealins.json ----------

def charger():
    """Contenu du cache ({"maj", "complet", "pages", "fonds": {isin: fonds}}), vide s'il n'existe pas."""
    try:
        c = json.loads(CACHE.read_text(encoding="utf-8"))
        if isinstance(c.get("fonds"), dict):
            return c
    except (OSError, ValueError):
        pass
    return {"maj": None, "complet": False, "pages": 0, "fonds": {}}


def enregistrer(c):
    """Écrit le cache d'un coup (fichier temporaire puis renommage), un fonds par ligne pour des
    différences Git lisibles."""
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tete = {k: c.get(k) for k in ("maj", "complet", "pages")}
    lignes = [f" {json.dumps(i)}: {json.dumps(f, ensure_ascii=False, separators=(',', ':'))}"
              for i, f in sorted(c["fonds"].items())]
    texte = json.dumps(tete, ensure_ascii=False)[:-1] + ', "fonds": {\n' + ",\n".join(lignes) + "\n}}\n"
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(texte, encoding="utf-8")
    os.replace(tmp, CACHE)


def fusionner(c, nouveaux, vu_le):
    """Ajoute les fonds lus au cache. Quand la date de valeur avance, l'ancienne valeur devient la
    valeur précédente (vl_prec, date_vl_prec), qui sert à calculer la variation."""
    for f in nouveaux:
        ancien = c["fonds"].get(f["isin"]) or {}
        g = {k: v for k, v in f.items() if k != "isin"}
        if ancien.get("date_vl") and f.get("date_vl") and f["date_vl"] > ancien["date_vl"] and ancien.get("vl"):
            g["vl_prec"], g["date_vl_prec"] = ancien["vl"], ancien["date_vl"]
        elif ancien.get("date_vl") == f.get("date_vl"):
            g["vl_prec"], g["date_vl_prec"] = ancien.get("vl_prec"), ancien.get("date_vl_prec")
        elif ancien.get("date_vl") and f.get("date_vl") and f["date_vl"] < ancien["date_vl"]:
            ancien["vu_le"] = vu_le  # page en retard : on garde la valeur la plus récente
            continue
        g["vu_le"] = vu_le
        c["fonds"][f["isin"]] = {k: v for k, v in g.items() if v is not None}
    return c


def date_dominante(c):
    """Date de valeur la plus fréquente dans le cache (None s'il est vide)."""
    n = Counter(f.get("date_vl") for f in c["fonds"].values() if f.get("date_vl"))
    return n.most_common(1)[0][0] if n else None


def jour_ouvre_precedent(j):
    j -= timedelta(days=1)
    while j.weekday() >= 5:
        j -= timedelta(days=1)
    return j


def a_actualiser(c, maintenant):
    """Une lecture complète par jour ; une seconde dans la journée (après 4 h) seulement si la première
    n'avait pas encore les valeurs du jour ouvré précédent."""
    if not c.get("maj") or not c["fonds"]:
        return True
    maj = datetime.fromisoformat(c["maj"])
    if maj.date() < maintenant.date():
        return True
    attendu = jour_ouvre_precedent(maintenant.date()).isoformat()
    return (maintenant - maj) > timedelta(hours=4) and (date_dominante(c) or "") < attendu


def actualiser(forcer=False, max_minutes=8):
    """Relit toute la liste si nécessaire (environ 135 pages, 3 à 4 minutes) et met le cache à jour.
    Ne lève jamais d'erreur : si le site est injoignable (réseau du cloud), le cache reste tel quel.
    Renvoie un court bilan pour le journal."""
    c = charger()
    maintenant = datetime.now(PARIS).replace(tzinfo=None)
    if not forcer and not a_actualiser(c, maintenant):
        return f"Wealins : cache à jour ({len(c['fonds'])} fonds, valeurs du {date_dominante(c)})"
    debut, page1 = time.monotonic(), _get(LISTE)
    if not page1 or not lire_liste(page1):
        return "Wealins : liste injoignable (réseau du cloud ?), cache gardé tel quel"
    n = min(nb_pages(page1), MAX_PAGES)
    lus, echecs, faites = lire_liste(page1), 0, 1
    for k in range(2, n + 1):
        if time.monotonic() - debut > max_minutes * 60 or echecs >= 5:
            break
        f = lire_liste(_get(f"{LISTE}page/{k}/"))
        faites = k
        if f:
            lus += f
        else:
            echecs += 1
    complet = faites == n and echecs == 0
    fusionner(c, lus, maintenant.date().isoformat())
    limite = (maintenant.date() - timedelta(days=OUBLI_JOURS)).isoformat()
    c["fonds"] = {i: f for i, f in c["fonds"].items() if f.get("vu_le", "") >= limite}
    c.update(maj=maintenant.isoformat(timespec="minutes"), complet=complet, pages=n)
    enregistrer(c)
    return (f"Wealins : {len(lus)} fonds lus sur {n} pages{'' if complet else ' (lecture incomplète)'}, "
            f"valeurs du {date_dominante(c)}")


# ---------- pour collecte.py, verif.py, fiches.py et rendu.py ----------

def variation(f):
    """Variation (%) entre la valeur précédente et la dernière valeur d'un fonds du cache."""
    if f.get("vl") and f.get("vl_prec"):
        return round((f["vl"] / f["vl_prec"] - 1) * 100, 2)
    return None


def mesure(isin, c, ft=True):
    """Prix d'un fonds pour « Mes investissements » : la valeur liquidative la plus récente entre Wealins
    et le Financial Times (règle de Mathieu : la source qui n'a que la veille est écartée). Si les deux
    sources ont la même date, verif.py compare leurs valeurs. None si le fonds n'est pas dans la liste."""
    f = c["fonds"].get(isin)
    if not f or not f.get("vl"):
        return None
    sources = {"wealins": [f["vl"], f.get("date_vl")]}
    if ft:
        from verif import ft_date
        p, d = ft_date("funds", f"{isin}:{f.get('devise') or 'EUR'}")
        if p:
            sources["ft"] = [p, d]
    dates = [d for _, d in sources.values() if d]
    ref = max(dates) if dates else None
    recentes = {k: v for k, v in sources.items() if v[1] == ref} or sources
    prix = recentes["wealins"][0] if "wealins" in recentes else recentes["ft"][0]
    precedent = f["vl"] if ref and f.get("date_vl") and ref > f["date_vl"] else f.get("vl_prec")
    return {"ticker": isin, "isin": isin, "nom": f.get("nom") or isin, "categorie": "fonds", "source": "wealins",
            "prix": prix, "date_cours": ref, "devise": f.get("devise"), "sfdr": f.get("sfdr"),
            "var_1j": round((prix / precedent - 1) * 100, 2) if precedent else None,
            "sources_vl": sources, "url_wealins": url_fonds(isin)}


def catalogue_page(c, exclus=()):
    """Fonds à mettre dans la page pour la barre de recherche, en tableaux compacts :
    [isin, nom, devise, valeur, date de valeur, variation]. exclus : ISIN déjà suivis par la fiche."""
    exclus = set(exclus)
    return [[i, f.get("nom") or i, f.get("devise"), f.get("vl"), f.get("date_vl"), variation(f)]
            for i, f in sorted(c["fonds"].items(), key=lambda x: (x[1].get("nom") or "").lower())
            if f.get("vl") and i not in exclus]


if __name__ == "__main__":
    print(actualiser(forcer="--forcer" in sys.argv[1:]))
