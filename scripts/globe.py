"""Carte du monde de la fiche : dans quel pays placer chaque titre suivi (globe de la page, D-20261123-4).

Règles choisies par le propriétaire le 22/11/2026 :
- actions : pays du siège (champ « pays » des caractéristiques en cache, data/fiches/<ticker>.json) ;
- ETF : pays de création du fonds (deux premières lettres de l'ISIN), sauf ceux qui investissent aux
  États-Unis, au Japon ou en Inde, placés dans ce pays, et les 4 ETF émergents et Asie éligibles au PEA,
  placés dans chacun des pays qu'ils couvrent (classement MSCI habituel, à vérifier fonds par fonds) ;
- tous les titres suivis ; la page les classe par la variation du jour.
Aucun appel réseau : tout vient du catalogue du jour et des fiches en cache. Le tracé des pays est à part
(docs/globe/, voir trace_pays.py), chargé par la page seulement quand on arrive au globe.
"""
import json
import re
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHES = RACINE / "data" / "fiches"

# Pays où un titre peut être placé : nom, région, point d'étiquette (latitude, longitude, Natural Earth)
PAYS = {
    "FR": ("France", "Europe", 46.7, 2.55), "LU": ("Luxembourg", "Europe", 49.73, 6.08),
    "NL": ("Pays-Bas", "Europe", 52.42, 5.61), "DE": ("Allemagne", "Europe", 50.96, 9.68),
    "IT": ("Italie", "Europe", 44.73, 11.08), "ES": ("Espagne", "Europe", 40.09, -3.46),
    "GR": ("Grèce", "Europe", 39.49, 21.73), "CH": ("Suisse", "Europe", 46.72, 7.46),
    "DK": ("Danemark", "Europe", 55.97, 9.02), "FI": ("Finlande", "Europe", 63.25, 27.28),
    "IE": ("Irlande", "Europe", 53.08, -7.8), "BE": ("Belgique", "Europe", 50.79, 4.8),
    "PT": ("Portugal", "Europe", 39.61, -8.27), "AT": ("Autriche", "Europe", 47.52, 14.13),
    "SE": ("Suède", "Europe", 65.86, 19.02), "NO": ("Norvège", "Europe", 61.36, 9.68),
    "GB": ("Royaume-Uni", "Europe", 54.4, -2.12), "IS": ("Islande", "Europe", 64.78, -18.67),
    "LI": ("Liechtenstein", "Europe", 47.11, 9.56), "MT": ("Malte", "Europe", 35.89, 14.43),
    "CY": ("Chypre", "Europe", 34.91, 33.08), "EE": ("Estonie", "Europe", 58.72, 25.87),
    "LV": ("Lettonie", "Europe", 57.07, 25.46), "LT": ("Lituanie", "Europe", 55.1, 24.09),
    "PL": ("Pologne", "Europe", 51.99, 19.49), "CZ": ("Tchéquie", "Europe", 49.88, 15.38),
    "SK": ("Slovaquie", "Europe", 48.73, 19.05), "SI": ("Slovénie", "Europe", 46.06, 14.92),
    "HU": ("Hongrie", "Europe", 47.09, 19.45), "RO": ("Roumanie", "Europe", 45.73, 24.97),
    "BG": ("Bulgarie", "Europe", 42.51, 25.16), "HR": ("Croatie", "Europe", 45.81, 16.37),
    "US": ("États-Unis", "Amérique du Nord", 39.54, -97.48), "CA": ("Canada", "Amérique du Nord", 60.32, -101.91),
    "MX": ("Mexique", "Amérique du Nord", 23.92, -102.29), "BR": ("Brésil", "Amérique du Sud", -12.1, -49.56),
    "CL": ("Chili", "Amérique du Sud", -38.15, -72.32), "CO": ("Colombie", "Amérique du Sud", 3.37, -73.17),
    "PE": ("Pérou", "Amérique du Sud", -12.98, -72.9), "JP": ("Japon", "Asie", 36.14, 138.44),
    "IN": ("Inde", "Asie", 22.69, 79.36), "CN": ("Chine", "Asie", 32.5, 106.34),
    "KR": ("Corée du Sud", "Asie", 36.38, 128.13), "TW": ("Taïwan", "Asie", 23.65, 120.87),
    "ID": ("Indonésie", "Asie", -0.95, 101.89), "MY": ("Malaisie", "Asie", 2.53, 113.84),
    "PH": ("Philippines", "Asie", 11.2, 122.47), "TH": ("Thaïlande", "Asie", 15.46, 101.07),
    "HK": ("Hong Kong", "Asie", 22.45, 114.1), "SG": ("Singapour", "Asie", 1.37, 103.82),
    "AU": ("Australie", "Océanie", -24.13, 134.05), "NZ": ("Nouvelle-Zélande", "Océanie", -39.76, 172.79),
    "TR": ("Turquie", "Moyen-Orient", 39.35, 34.51), "SA": ("Arabie saoudite", "Moyen-Orient", 23.81, 44.7),
    "AE": ("Émirats arabes unis", "Moyen-Orient", 23.47, 54.55), "QA": ("Qatar", "Moyen-Orient", 25.24, 51.14),
    "KW": ("Koweït", "Moyen-Orient", 29.41, 47.31), "IL": ("Israël", "Moyen-Orient", 30.91, 34.85),
    "ZA": ("Afrique du Sud", "Afrique", -29.71, 23.67),
}
# Noms de pays lus dans les caractéristiques (Boursorama en français, Yahoo en anglais) → code ISO
ALIAS = {"pays bas": "NL", "netherlands": "NL", "the netherlands": "NL", "germany": "DE", "italy": "IT",
         "spain": "ES", "greece": "GR", "switzerland": "CH", "denmark": "DK", "finland": "FI",
         "ireland": "IE", "belgium": "BE", "austria": "AT", "sweden": "SE", "norway": "NO",
         "united kingdom": "GB", "uk": "GB", "grande bretagne": "GB", "royaume uni": "GB", "iceland": "IS",
         "malta": "MT", "cyprus": "CY", "estonia": "EE", "latvia": "LV", "lithuania": "LT", "poland": "PL",
         "czech republic": "CZ", "czechia": "CZ", "republique tcheque": "CZ", "slovakia": "SK",
         "slovenia": "SI", "hungary": "HU", "romania": "RO", "bulgaria": "BG", "croatia": "HR",
         "united states": "US", "usa": "US", "etats unis": "US", "canada": "CA", "mexico": "MX",
         "brazil": "BR", "chile": "CL", "colombia": "CO", "peru": "PE", "japan": "JP", "india": "IN",
         "china": "CN", "south korea": "KR", "korea": "KR", "taiwan": "TW", "indonesia": "ID",
         "malaysia": "MY", "philippines": "PH", "thailand": "TH", "hong kong": "HK", "singapore": "SG",
         "australia": "AU", "new zealand": "NZ", "turkey": "TR", "turkiye": "TR", "saudi arabia": "SA",
         "united arab emirates": "AE", "qatar": "QA", "kuwait": "KW", "israel": "IL", "south africa": "ZA",
         "bermuda": "", "jersey": "", "guernsey": "", "isle of man": "", "cayman islands": ""}
# Sièges complétés à la main quand la fiche n'en donne pas (siège social, rapport annuel de la société)
SIEGES = {"STLAM.MI": "NL",   # Stellantis N.V., société de droit néerlandais
          "ALCLS.PA": "FR",   # Cellectis, Paris
          "ADOC.PA": "FR",    # Adocia, Lyon
          "ALGEN.PA": "FR",   # Genomic Vision, Bagneux
          # places que Boursorama ne couvre pas : le pays ne vient que de Yahoo, qui l'omet parfois (EUROB.AT, 23/11)
          "EUROB.AT": "GR",   # Eurobank, Athènes
          "ALPHA.AT": "GR",   # Alpha Bank (Alpha Services and Holdings), Athènes
          "ETE.AT": "GR",     # Banque nationale de Grèce, Athènes
          "NOVO-B.CO": "DK",  # Novo Nordisk, Bagsværd
          "NOKIA.HE": "FI"}   # Nokia, Espoo
# ETF placés dans le pays où ils investissent (États-Unis, Japon, Inde : choix du propriétaire, 22/11/2026)
ETF_ZONE = {"ESE.PA": "US", "PSP5.PA": "US", "PE500.PA": "US", "PUST.PA": "US", "PANX.PA": "US",
            "RS2K.PA": "US", "CU2.PA": "US", "LQQ.PA": "US", "CL2.PA": "US", "PTPXE.PA": "JP", "PINR.PA": "IN"}
# Même règle pour un ETF ajouté plus tard, d'après son nom
MOTS_ZONE = [(r"s&p 500|nasdaq|msci usa|russell|\busa\b|dow jones", "US"), (r"japan|japon|topix|nikkei", "JP"),
             (r"\binde\b|\bindia\b", "IN")]
# Les 4 ETF émergents et Asie éligibles au PEA : dans chacun des pays qu'ils couvrent (classement MSCI)
EM_ASIE = ["CN", "IN", "ID", "KR", "MY", "PH", "TW", "TH"]
EM_EMEA = ["CZ", "GR", "HU", "KW", "PL", "QA", "SA", "ZA", "TR", "AE"]
EM_AMERIQUES = ["BR", "CL", "CO", "MX", "PE"]
ETF_MULTI = {"PAEEM.PA": sorted(EM_ASIE + EM_EMEA + EM_AMERIQUES),  # MSCI EM sans l'Égypte : 23 pays
             "PLEM.PA": sorted(EM_EMEA),                          # MSCI EM EMEA sans l'Égypte : 10 pays
             "PAASI.PA": sorted(EM_ASIE),                         # MSCI EM Asie : 8 pays
             "PAEJ.PA": sorted(EM_ASIE + ["AU", "HK", "NZ", "SG"])}  # Asie-Pacifique hors Japon : 12 pays
# Règle appliquée, rappelée sur la page : siège, domicile (pays de création), zone investie, pays couverts
REGLES = {"s": "siège de la société", "d": "pays de création du fonds", "z": "pays où le fonds investit",
          "m": "un des pays couverts par le fonds"}


def cle_nom(s):
    """« Pays-Bas » → « pays bas » : sans accents, minuscules, tirets et apostrophes en espaces."""
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[\s'’-]+", " ", s).strip().lower()


NOMS = {cle_nom(v[0]): k for k, v in PAYS.items()}
NOMS.update(ALIAS)


def code_pays(nom):
    """Code ISO à deux lettres d'un nom de pays, en français ou en anglais ; "" si inconnu."""
    return NOMS.get(cle_nom(nom), "")


def caracteristiques(dossier=FICHES):
    """Caractéristiques en cache de chaque titre ({ticker: infos}) ; {} si le dossier manque."""
    out = {}
    for f in sorted(Path(dossier).glob("*.json")):
        try:
            out[f.stem] = json.loads(f.read_text(encoding="utf-8")).get("infos") or {}
        except (OSError, ValueError):
            continue
    return out


def pays_du_titre(m, infos=None):
    """(codes ISO, règle) d'un titre du catalogue : voir le haut du fichier. ([], "") si on ne sait pas."""
    infos = infos or {}
    t = m.get("ticker", "")
    if m.get("categorie") == "etf":
        if t in ETF_MULTI:
            return list(ETF_MULTI[t]), "m"
        if t in ETF_ZONE:
            return [ETF_ZONE[t]], "z"
        nom = str(m.get("nom") or "").lower()
        for motif, code in MOTS_ZONE:
            if re.search(motif, nom):
                return [code], "z"
        isin = str(m.get("isin") or infos.get("isin") or "")
        if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin) and isin[:2] in PAYS:
            return [isin[:2]], "d"
        return [], ""
    code = SIEGES.get(t) or code_pays(infos.get("pays"))
    return ([code], "s") if code in PAYS else ([], "")


def table(catalogue, infos=None, jour="", statuts=None):
    """Données du globe pour la page : un titre par ligne (liste courte, pour une page légère) et les pays
    qui en ont. t : [ticker, nom, catégorie, prix, devise, variation du jour, date du cours, éligibilité au
    PEA (1 oui, 0 non, null à vérifier : contrôle quotidien `statuts` de eligibilite.py, sinon Boursorama),
    [codes pays], règle, effet de levier (1/0)]."""
    infos, statuts = infos or {}, statuts or {}
    lignes, pays, sans = [], {}, []
    for m in catalogue:
        if m.get("categorie") not in ("etf", "actions", "petites"):
            continue
        i = infos.get(m["ticker"]) or {}
        codes, regle = pays_du_titre(m, i)
        if not codes:
            sans.append(m["ticker"])
            continue
        s = statuts.get(m["ticker"])
        pea = {"oui": 1, "non": 0, "doute": None}[s] if s in ("oui", "non", "doute") else \
            (None if i.get("pea_bourso") is None else int(bool(i.get("pea_bourso"))))
        lignes.append([m["ticker"], m.get("nom") or m["ticker"], m["categorie"], m.get("prix"), m.get("devise"),
                       m.get("var_1j"), m.get("date_cours"), pea, codes, regle, int(bool(m.get("levier")))])
        for c in codes:
            pays.setdefault(c, list(PAYS[c]))
    return {"date": jour, "t": lignes, "p": pays, "sans": sans, "regles": REGLES}


def nombres(g):
    """Résumé lisible du globe : {code: nombre de titres}, du plus fourni au moins fourni."""
    n = {}
    for ligne in g.get("t", []):
        for c in ligne[8]:
            n[c] = n.get(c, 0) + 1
    return dict(sorted(n.items(), key=lambda x: (-x[1], x[0])))
