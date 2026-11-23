"""Tracé des pays du globe de la fiche (docs/globe/), à partir de Natural Earth (domaine public).

Usage : python scripts/trace_pays.py NE_110M.geojson NE_50M.geojson [--commit SHA]
Les deux fichiers sources se téléchargent sur le dépôt officiel de Natural Earth (à faire une seule fois,
le tracé ne change presque jamais) :
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
Écrit docs/globe/monde-110m.json (globe entier) et docs/globe/monde-50m.json (zoom) : pour chaque pays, son
code ISO à deux lettres, son nom en français, son point d'étiquette, son rayon en degrés et ses anneaux en
centièmes de degré, chaque point codé par différence avec le précédent. Aucune donnée personnelle.
"""
import json
import math
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "docs" / "globe"
SOURCE = "Natural Earth, Admin 0 – Countries (domaine public), github.com/nvkelso/natural-earth-vector"
# Noms courts en français quand celui de Natural Earth est long ou ancien
NOMS = {"CN": "Chine", "CZ": "Tchéquie", "KR": "Corée du Sud", "KP": "Corée du Nord", "US": "États-Unis",
        "AE": "Émirats arabes unis", "TW": "Taïwan", "HK": "Hong Kong", "MK": "Macédoine du Nord",
        "RU": "Russie", "GB": "Royaume-Uni", "VN": "Viêt Nam", "LA": "Laos", "CD": "RD Congo",
        "CG": "Congo", "CI": "Côte d'Ivoire", "SY": "Syrie", "IR": "Iran", "BO": "Bolivie",
        "VE": "Venezuela", "TZ": "Tanzanie", "MD": "Moldavie", "BA": "Bosnie-Herzégovine",
        "DO": "République dominicaine", "CF": "Centrafrique", "SZ": "Eswatini", "TL": "Timor oriental"}


def code_iso(props):
    """Code ISO à deux lettres d'un pays de Natural Earth (« FR » même quand ISO_A2 vaut -99), sinon ""."""
    for cle in ("ISO_A2_EH", "ISO_A2"):
        c = str(props.get(cle) or "")
        if re.fullmatch(r"[A-Z]{2}", c):
            return c
    return ""


def nom_fr(props, code):
    """Nom français court d'un pays (table NOMS, sinon NAME_FR de Natural Earth, sinon son nom anglais)."""
    return NOMS.get(code) or props.get("NAME_FR") or props.get("NAME") or ""


def aire(anneau):
    """Aire plane d'un anneau [(lon, lat)…] en degrés carrés (formule du lacet), toujours positive."""
    s = 0.0
    for (x1, y1), (x2, y2) in zip(anneau, anneau[1:] + anneau[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def simplifier(anneau, tolerance):
    """Douglas-Peucker sur un anneau fermé : retire les points à moins de `tolerance` degrés de la ligne
    entre leurs voisins gardés. Garde toujours au moins 4 points (3 sommets distincts et la fermeture)."""
    pts = anneau[:-1] if len(anneau) > 1 and anneau[0] == anneau[-1] else list(anneau)
    if tolerance <= 0 or len(pts) <= 4:
        return pts
    # deux points d'appui : le premier et le plus éloigné de lui
    loin = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
    garde = {0, loin}
    pile = [(0, loin), (loin, len(pts))]
    while pile:
        a, b = pile.pop()
        if b - a < 2:
            continue
        (xa, ya), (xb, yb) = pts[a], pts[b % len(pts)]
        dx, dy = xb - xa, yb - ya
        n = math.hypot(dx, dy)
        pire, ip = -1.0, None
        for i in range(a + 1, b):
            x, y = pts[i]
            d = abs(dy * (x - xa) - dx * (y - ya)) / n if n else math.hypot(x - xa, y - ya)
            if d > pire:
                pire, ip = d, i
        if pire > tolerance:
            garde.add(ip)
            pile += [(a, ip), (ip, b)]
    out = [pts[i] for i in sorted(garde)]
    return out if len(out) >= 3 else pts


def encoder(anneau):
    """Anneau en centièmes de degré codé par différences : [x0, y0, dx1, dy1, …] ; None s'il reste moins de
    3 points distincts après arrondi."""
    q = []
    for lon, lat in anneau:
        p = (round(lon * 100), round(lat * 100))
        if not q or p != q[-1]:
            q.append(p)
    if len(q) > 1 and q[0] == q[-1]:
        q.pop()
    if len(q) < 3:
        return None
    out = [q[0][0], q[0][1]]
    for (x1, y1), (x2, y2) in zip(q, q[1:]):
        out += [x2 - x1, y2 - y1]
    return out


def distance(lon1, lat1, lon2, lat2):
    """Distance angulaire entre deux points, en degrés (formule de haversine)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return math.degrees(2 * math.asin(min(1.0, math.sqrt(a))))


def dans(lon, lat, anneau):
    """Vrai si le point est dans l'anneau (test du rayon, en coordonnées planes lon/lat)."""
    c = False
    for (x1, y1), (x2, y2) in zip(anneau, anneau[1:] + anneau[:1]):
        if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
            c = not c
    return c


def convertir(geojson, tolerance=0.0, aire_min=0.0):
    """Pays du GeoJSON de Natural Earth en liste compacte (voir le haut du fichier)."""
    pays = []
    for f in geojson["features"]:
        props, geo = f["properties"], f["geometry"]
        if not geo:
            continue
        code = code_iso(props)
        polys = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        polys = [[[(float(x), float(y)) for x, y in r] for r in p] for p in polys]
        lon, lat = float(props.get("LABEL_X") or 0), float(props.get("LABEL_Y") or 0)
        # polygone principal : celui qui contient le point d'étiquette, sinon le plus grand
        plus_grand = max(polys, key=lambda p: aire(p[0]))
        principal = next((p for p in polys if dans(lon, lat, p[0])), plus_grand)
        # rayon du zoom : le pays sans ses territoires lointains (Guyane pour la France, Hawaï…) ni ses îlots
        proches = [p for p in polys if aire(p[0]) >= 0.01 * aire(plus_grand[0])
                   and min(distance(lon, lat, x, y) for x, y in p[0]) <= 25]
        rayon = min(40.0, max(distance(lon, lat, x, y) for p in proches + [principal] for x, y in p[0]))
        sortie = []
        for p in polys:
            if p is not plus_grand and p is not principal and aire(p[0]) < aire_min:
                continue  # petite île : invisible au zoom de la fiche
            anneaux = [encoder(simplifier(r, tolerance)) for r in p]
            if anneaux[0] is None:
                continue
            sortie.append([a for a in anneaux if a])
        if sortie:
            pays.append({"c": code, "n": nom_fr(props, code), "l": [round(lon, 2), round(lat, 2)],
                         "r": round(rayon, 1), "p": sortie, "_officiel": props.get("ISO_A2") == code,
                         "_aire": aire(plus_grand[0])})
    return fusionner(pays)


def fusionner(pays):
    """Un seul pays par code ISO : les territoires qui partagent un code (îles Ashmore-et-Cartier et
    territoires de l'océan Indien pour l'Australie) rejoignent le pays principal, qui garde son nom, son
    étiquette et son rayon. Les entités sans code (Chypre du Nord, Somaliland…) restent à part."""
    par_code, out = {}, []
    for x in sorted(pays, key=lambda x: (not x["_officiel"], -x["_aire"])):
        principal = par_code.get(x["c"]) if x["c"] else None
        if principal:
            principal["p"] += x["p"]
            continue
        if x["c"]:
            par_code[x["c"]] = x
        out.append(x)
    for x in out:
        del x["_officiel"], x["_aire"]
    out.sort(key=lambda x: (x["c"] or "~", x["n"]))
    return out


def ecrire(pays, chemin, echelle, commit):
    doc = {"source": SOURCE + (f", commit {commit}" if commit else ""), "echelle": echelle,
           "unite": "centièmes de degré, chaque point codé par différence avec le précédent", "pays": pays}
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    nb = sum(len(a) // 2 for x in pays for p in x["p"] for a in p)
    print(f"{chemin.relative_to(RACINE)} : {len(pays)} pays, {nb} points, {chemin.stat().st_size // 1024} Ko")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    commit = sys.argv[sys.argv.index("--commit") + 1] if "--commit" in sys.argv else ""
    if len(args) < 2:
        sys.exit(__doc__)
    args = [a for a in args if a != commit]
    src110, src50 = (json.loads(Path(a).read_text(encoding="utf-8")) for a in args[:2])
    ecrire(convertir(src110), SORTIE / "monde-110m.json", "1:110 millions", commit)
    ecrire(convertir(src50, tolerance=0.02, aire_min=0.02), SORTIE / "monde-50m.json", "1:50 millions", commit)


if __name__ == "__main__":
    main()
