"""Contrôle quotidien de l'éligibilité au PEA de chaque titre suivi (D-20261123-5, demande du propriétaire :
« que rien ne soit oublié et qu'aucune mauvaise information ne soit donnée »).

Usage : python scripts/eligibilite.py                relit Boursorama pour chaque titre suivi (environ 5 min,
                                                     une page par seconde, robots.txt respecté) ; lancé chaque
                                                     nuit par l'agent de nuit (AMELIORATION.md)
        python scripts/eligibilite.py --sans-reseau  règles et cache data/fiches/ seulement
Écrit data/eligibilite.json : pour chaque titre suivi, un statut « oui », « doute » ou « non », ses raisons et
ses sources, le jour de la dernière lecture de Boursorama (« relu ») et celui depuis lequel le statut n'a pas
changé (« depuis »). Les vérifications faites à la main (clé « verifications », avec source et date) passent
avant le calcul et sont gardées d'une nuit à l'autre.

Règles (information générale, à vérifier auprès de la banque) :
- action : société dont le siège est dans l'Union européenne ou l'EEE (Islande, Norvège, Liechtenstein) et
  soumise à l'impôt sur les sociétés ; le pays de l'ISIN sert de repère du siège social. Les foncières au
  régime SIIC (exonérées d'impôt sur les sociétés) sont exclues du PEA depuis le 21/10/2011 ; une autre
  société immobilière reste « à vérifier » (régimes exonérés étrangers : SOCIMI, SIIQ, REIT…) ;
- ETF : éligible si son émetteur l'annonce (au moins 75 % d'actions de l'UE ou de l'EEE, souvent par contrat
  d'échange), lu sur Boursorama ; « non » seulement après une deuxième source (vérification à la main) ;
- OPCVM de opcvm.json : éligibles d'après leur documentation (pea.fr), « à vérifier » si elle a plus de 180 jours ;
- obligations en direct : jamais éligibles.
Pour une action, « oui » demande deux sources concordantes (la règle du siège et Boursorama, ou une
vérification à la main) ; une seule source donne « doute ». Pour un ETF, « oui » vient de la déclaration de
l'émetteur lue sur Boursorama. Une panne de site ne change jamais un statut : on garde le dernier (« non_relu »).
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paris import aujourdhui  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data" / "eligibilite.json"
UE_EEE = {"AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR", "HR", "HU", "IE", "IT", "LT",
          "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "IS", "LI", "NO"}
# Foncières françaises au régime SIIC (exclues du PEA depuis le 21/10/2011), si l'une est suivie
SIIC = {"URW.PA": "Unibail-Rodamco-Westfield", "LI.PA": "Klépierre", "GFC.PA": "Gecina", "COV.PA": "Covivio",
        "ICAD.PA": "Icade", "MERY.PA": "Mercialys", "CARM.PA": "Carmila", "ALTA.PA": "Altarea", "ARG.PA": "Argan"}
IMMOBILIER = re.compile(r"immobili|fonci[eè]r|real estate|reit\b|socimi|siic", re.I)
OBLIGATIONS = re.compile(r"\b(obligations?|bonds?|govt|treasury|aggregate)\b", re.I)
CATEGORIES = {"etf": "etf", "etf_levier": "etf", "actions": "actions", "petites": "petites", "obligations": "obligations"}
JOURS_DOC_OPCVM = 180


def titres_suivis(univers):
    """Titres suivis de univers.json : [{ticker, nom, categorie}] (ETF à effet de levier compris)."""
    out = []
    for cle, cat in CATEGORIES.items():
        for t, nom in (univers.get(cle) or {}).items():
            out.append({"ticker": t, "nom": nom, "categorie": cat})
    return out


def statut_action(t, nom, isin, bourso, secteur=""):
    """(statut, raisons, sources) d'une action d'après la règle du siège et Boursorama (True/False/None)."""
    if not isin or not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin):
        return "doute", ["ISIN inconnu : siège social non vérifié"], []
    pays = isin[:2]
    if pays not in UE_EEE:
        return "non", [f"siège hors de l'Union européenne et de l'EEE (ISIN {pays})"], ["règle du siège"]
    if t in SIIC:
        return "non", [f"{SIIC[t]} : foncière au régime SIIC, exclue du PEA depuis le 21/10/2011"], ["règle SIIC"]
    if IMMOBILIER.search(f"{nom} {secteur or ''}"):
        return "doute", ["société immobilière : vérifier qu'elle n'a pas un régime exonéré d'impôt sur les "
                         "sociétés (SIIC, SOCIMI, SIIQ, REIT…)"], ["règle du siège"]
    raisons, sources = [f"siège dans l'Union européenne ou l'EEE (ISIN {pays})"], ["règle du siège"]
    if bourso is True:
        return "oui", raisons + ["Boursorama : éligible au PEA"], sources + ["Boursorama"]
    if bourso is False:
        return "doute", raisons + ["Boursorama ne l'indique pas éligible sur cette place de cotation : la banque "
                                   "doit pouvoir l'acheter dans un PEA sur ce marché"], sources
    return "doute", raisons + ["Boursorama non lu pour ce titre : deuxième source à trouver"], sources


def statut_etf(t, nom, isin, bourso):
    """(statut, raisons, sources) d'un ETF : éligibilité annoncée par l'émetteur, lue sur Boursorama."""
    if OBLIGATIONS.search(nom or "") and bourso is not True:
        return "non", ["ETF d'obligations : pas éligible au PEA sans contrat d'échange sur des actions"], ["règle"]
    if bourso is True:
        return "oui", ["Boursorama : éligible au PEA (annoncé par l'émetteur)"], ["Boursorama"]
    if bourso is False:
        return "doute", ["Boursorama ne l'indique pas éligible au PEA : à confirmer dans le DIC ou sur justETF, "
                         "puis à retirer des titres suivis si c'est confirmé"], ["Boursorama"]
    return "doute", ["Boursorama non lu pour ce titre"], []


def statut_opcvm(f, jour):
    """(statut, raisons, sources) d'un OPCVM de opcvm.json, éligible d'après sa documentation."""
    lu = str(f.get("verifie_le") or "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lu):
        return "doute", ["documentation du fonds sans date de lecture"], []
    age = (date.fromisoformat(jour) - date.fromisoformat(lu)).days
    if age > JOURS_DOC_OPCVM:
        return "doute", [f"documentation lue il y a {age} jours : à relire"], ["pea.fr"]
    return "oui", [f"éligible d'après sa documentation (pea.fr, lue le {lu})"], ["pea.fr", "opcvm.json"]


def evaluer(m, isin, bourso, secteur, verif):
    """Statut d'un titre ; une vérification à la main (verif) passe avant le calcul."""
    if m["categorie"] == "obligations":
        calc = ("non", ["obligation en direct : jamais éligible au PEA"], ["règle"])
    elif m["categorie"] == "etf":
        calc = statut_etf(m["ticker"], m["nom"], isin, bourso)
    else:
        calc = statut_action(m["ticker"], m["nom"], isin, bourso, secteur)
    if verif and verif.get("statut") in ("oui", "doute", "non") and verif.get("source"):
        return verif["statut"], [f"vérifié à la main le {verif.get('date', '?')} : {verif.get('raison', '')}".strip(" :")], \
            [verif["source"]]
    return calc


def fusionner(ancien, nouveau, jour, relu, panne=False):
    """Nouveau statut d'un titre. `relu` : Boursorama lu aujourd'hui ; `panne` : sa page existe mais n'a pas pu
    être lue. En cas de panne, un statut déjà connu ne change jamais (une panne n'est pas une information).
    La date « depuis » reste celle du premier jour du statut actuel."""
    if panne and ancien and ancien.get("statut"):
        garde = dict(ancien)
        garde["non_relu"] = jour
        return garde
    out = dict(nouveau)
    out["depuis"] = ancien["depuis"] if ancien and ancien.get("statut") == nouveau["statut"] and ancien.get("depuis") else jour
    if relu:
        out["relu"] = jour
    elif ancien and ancien.get("relu"):
        out["relu"] = ancien["relu"]
    return out


def resume(titres):
    """Nombre de titres par statut."""
    r = {"oui": 0, "doute": 0, "non": 0}
    for x in titres.values():
        r[x["statut"]] = r.get(x["statut"], 0) + 1
    return r


def charger(chemin=FICHIER):
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def statuts(e):
    """{ticker: statut} de data/eligibilite.json (dict déjà lu) ; {} s'il est vide."""
    return {t: x.get("statut") for t, x in (e.get("titres") or {}).items() if x.get("statut")}


def pour_la_page(e):
    """Ce que la page affiche : le jour du contrôle, le résumé, la liste des titres « oui » et, pour les titres
    « doute » ou « non », [statut, raison]. None si le contrôle n'a jamais tourné."""
    if not e.get("titres"):
        return None
    return {"jour": e.get("jour", ""), "resume": e.get("resume", {}),
            "oui": sorted(t for t, x in e["titres"].items() if x.get("statut") == "oui"),
            "d": {t: [x["statut"], (x.get("raisons") or [""])[-1]] for t, x in e["titres"].items() if x.get("statut") != "oui"}}


def lire_boursorama(m):
    """(éligibilité PEA lue sur Boursorama : True/False/None, caractéristiques lues, code Boursorama) ; le code
    est None si Boursorama n'a pas de page pour cette place (Copenhague, Athènes, Helsinki)."""
    import fiches
    from verif import codes
    bc, _ = codes(m)
    if not bc:
        return None, {}, None
    out = fiches.lire_bourso(bc, m["categorie"] == "etf")
    return out.get("pea_bourso"), out, bc


def main():
    reseau = "--sans-reseau" not in sys.argv
    jour = aujourdhui().isoformat()
    univers = json.loads((RACINE / "univers.json").read_text(encoding="utf-8"))
    ancien = charger()
    verifs = ancien.get("verifications") or {}
    import globe  # caractéristiques en cache (ISIN, secteur, Boursorama d'il y a moins de 7 jours)
    cache = globe.caracteristiques()
    titres, lus = {}, 0
    for m in titres_suivis(univers):
        t = m["ticker"]
        avant = (ancien.get("titres") or {}).get(t) or {}
        inf = dict(cache.get(t) or {})
        # dernière lecture de Boursorama : celle du contrôle précédent, plus récente que le cache des fiches
        bourso = avant["boursorama"] if "boursorama" in avant else inf.get("pea_bourso")
        for k in ("isin", "secteur"):
            inf[k] = inf.get(k) or avant.get(k)
        relu, panne = False, False
        if reseau and m["categorie"] != "obligations":
            b, page, code = lire_boursorama(m)
            if page:
                bourso, relu = b, True
                lus += 1
                inf.update({k: v for k, v in page.items() if k in ("isin", "secteur") and v})
            panne = bool(code) and not page
        isin = inf.get("isin") or (verifs.get(t) or {}).get("isin")
        statut, raisons, sources = evaluer(m, isin, bourso, inf.get("secteur"), verifs.get(t))
        nouveau = {"statut": statut, "raisons": raisons, "sources": sources, "isin": isin, "nom": m["nom"],
                   "categorie": m["categorie"], "boursorama": bourso, "secteur": inf.get("secteur")}
        titres[t] = fusionner(avant or None, nouveau, jour, relu, panne and t not in verifs)
    try:
        for f in json.loads((RACINE / "opcvm.json").read_text(encoding="utf-8")).get("fonds", []):
            statut, raisons, sources = statut_opcvm(f, jour)
            titres[f["isin"]] = fusionner((ancien.get("titres") or {}).get(f["isin"]),
                                          {"statut": statut, "raisons": raisons, "sources": sources, "isin": f["isin"],
                                           "nom": f.get("nom", ""), "categorie": "opcvm"}, jour, False)
    except (OSError, ValueError, KeyError):
        pass
    doc = {"maj": datetime.now().astimezone().isoformat(timespec="minutes"), "jour": jour,
           "lecture": "Boursorama relu" if reseau else "règles et cache seulement",
           "pages_lues": lus, "resume": resume(titres), "titres": titres, "verifications": verifs}
    FICHIER.parent.mkdir(parents=True, exist_ok=True)
    FICHIER.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    r = doc["resume"]
    print(f"Éligibilité PEA du {jour} : {r['oui']} oui, {r['doute']} à vérifier, {r['non']} non "
          f"({len(titres)} titres, {lus} pages Boursorama lues)")
    for t, x in titres.items():
        if x["statut"] == "non":
            print(f"  NON : {t} ({x['nom']}) : {x['raisons'][0]}")


if __name__ == "__main__":
    main()
