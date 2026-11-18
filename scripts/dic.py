"""DIC officiels des ETF suivis : risque (SRI) et frais courants lus dans le document lui-même.

Le DIC (document d'informations clés, règlement européen PRIIPs) est le document officiel publié par la
société de gestion. On y lit :
- le SRI, indicateur de risque de 1 à 7 (« classe de risque 4 sur 7 », « 4 out of 7 ») ;
- les frais courants : « frais de gestion et autres frais administratifs et d'exploitation », en % par an
  (l'équivalent du TER) ;
- les coûts de transaction estimés du fonds, en % par an ;
- la date de production du document quand elle est écrite.

Sources, dans cet ordre (demande du propriétaire, 17/11/2026), toutes dans pilotage/sources-verifiees.md
et lues seulement si leur robots.txt le permet :
1. Fundsquare (Bourse de Luxembourg), onglet Documents, version « en cours » du « Key Information
   Document (PRIIPs) » : fonds luxembourgeois, irlandais et une partie des fonds français ;
2. sinon, le site de l'émetteur : Amundi ETF (www.amundietf.fr/pdfDocuments/kid-priips/<ISIN>/FRA/FRA),
   pour les ETF français d'Amundi.
Non lus : la copie Morningstar dont Boursorama donne le lien (robots.txt de doc.morningstar.com : tout est
interdit) et Quantalys (bloque les robots : page « requires JS enabled and cookies »), qui reste un lien.

Seuls des chiffres sont gardés (aucun texte copié), dans data/dic.json, relus tous les 30 jours
(VALIDITE_JOURS) : le DIC change au plus quelques fois par an. Jamais bloquant : un DIC illisible garde
ses anciennes valeurs.

Usage : python3 scripts/dic.py            (titres sans DIC ou périmés, au plus MAX_PAR_PASSAGE)
        python3 scripts/dic.py --tout     (relit tous les DIC)
        python3 scripts/dic.py CW8.PA …   (seulement ces titres)
"""
import io
import json
import re
import sys
import time
import unicodedata
from datetime import date
from paris import aujourdhui  # noqa: E402
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data" / "dic.json"
CACHE_FICHES = RACINE / "data" / "fiches"
FUNDSQUARE = "https://www.fundsquare.net"
VALIDITE_JOURS = 30
MAX_PAR_PASSAGE = 60
PAUSE = 0.5  # secondes entre deux requêtes (politesse)
UA = "Mozilla/5.0 (compatible; MatinPEA/1.0; lecture des DIC publics)"

# ---------- lecture du texte d'un DIC ----------

# Le texte est lu « compact » : sans espaces et en minuscules, car l'extraction des PDF colle souvent des
# mots (« KeyInformationDocument », « fraisadministratifs »). Les motifs ci-dessous sont donc sans espaces.
POURCENT = (r"(\d+(?:[.,]\d+)?)%(?:ofthevalueof(?:your|the)investments?(?:per|each|a)year"
            r"|delavaleurde(?:votre|l')investissement(?:paran|chaqueannée))")
LIB_GESTION = (r"managementfeesandotheradministrativeoroperatingcosts"
               r"|managementcostsandotheradministrativeandoperatingcosts"
               r"|fraisdegestionetautres(?:frais|coûts)administratifs(?:et|ou)d.exploitation"
               r"|otherongoingcosts")
LIB_TRANSACTION = r"transactioncosts|coûtsdetransaction"
FIN_TRANSACTION = (r"incidentalcosts|coûtsaccessoires|performancefees|commissionsliées|otherongoingcosts"
                   r"|fraisdegestionetautres|management(?:fees|costs)andother")
FIN_GESTION = r"transactioncosts|coûtsdetransaction|" + FIN_TRANSACTION
COURS_RECURRENTS = r"ongoingcosts|coûtsrécurrents"
SANS_TRANSACTION = (r"pasde(?:coûts?|frais)detransaction|aucun(?:coût|frais)detransaction|notransactioncosts?"
                    r"|(?:donot|don't)charge(?:a|any)?transaction(?:costs?|fees?)")
MOTIFS_SRI = (r"as(\d)outof7", r"classederisque(\d)sur7", r"riskclass(\d)(?!\d)", r"classederisque(\d)(?!\d)",
              r"(\d)outof7", r"(\d)sur7", r"risikoklasse(\d)von7")
MOTIFS_DATE = (r"datedeproductiondudocumentd.informationsclés:?(\d{1,2}/\d{1,2}/\d{4})",
               r"(?:accurateas(?:at|of)|validas(?:at|of)|dated|dateofproduction[^:]{0,30}:)"
               r"(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})",
               r"(?:document|informations?)(?:est|sont)(?:exact|valable|àjour)\w*au(\d{1,2}/\d{1,2}/\d{4})")
FENETRE = 260  # caractères compacts lus après une étiquette


def normaliser(texte):
    """Ligatures (« ﬁ »), apostrophes, espaces insécables et retours à la ligne ramenés à une forme simple."""
    t = unicodedata.normalize("NFKC", texte or "")
    t = t.replace("’", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t)


def compact(texte):
    """Texte normalisé, sans aucun espace et en minuscules : résiste aux mots collés par l'extraction."""
    return re.sub(r"\s+", "", normaliser(texte)).lower()


def _nombre(s):
    return float(s.replace(",", "."))


def _apres(c, libelle, fin, pourcents, sans=None):
    """Valeur qui suit une étiquette : le premier « x % … par an » situé après elle, avant l'étiquette suivante
    (motif `fin`, FENETRE caractères au plus) ; 0 si la phrase `sans` (« pas de frais de transaction ») y figure.
    Essaie chaque occurrence de l'étiquette ; None si aucune ne donne de valeur."""
    for m in re.finditer(libelle, c):
        suite = c[m.end():m.end() + FENETRE]
        f = re.search(fin, suite)
        fenetre = suite[:f.start()] if f else suite
        if sans and re.search(sans, fenetre):
            return 0.0
        for pos, v in pourcents:
            if m.end() <= pos < m.end() + len(fenetre):
                return v
    return None


def analyser(texte, isin=None):
    """Chiffres d'un DIC : {sri, frais_courants, couts_transaction, date_doc, isin_ok}. Les valeurs non
    trouvées sont absentes ; frais en % par an. Chaque « x % de la valeur de votre investissement par an » est
    rattaché à l'étiquette qui le précède (frais de gestion, « other ongoing costs », coûts de transaction).
    Si les frais de gestion n'ont pas de pourcentage juste après leur étiquette (mise en page en colonnes),
    on prend le premier de la partie des coûts récurrents, qui est le leur dans le modèle PRIIPs."""
    c = compact(texte)
    out = {}
    for motif in MOTIFS_SRI:
        m = re.search(motif, c)
        if m and 1 <= int(m.group(1)) <= 7:
            out["sri"] = int(m.group(1))
            break
    pourcents = [(m.start(), _nombre(m.group(1))) for m in re.finditer(POURCENT, c)]
    g = _apres(c, LIB_GESTION, FIN_GESTION, pourcents)
    if g is None and pourcents and re.search(LIB_GESTION, c):
        r = re.search(COURS_RECURRENTS, c)
        apres_r = [v for pos, v in pourcents if not r or pos >= r.start()]
        g = apres_r[0] if apres_r else None
    if g is not None and 0 <= g <= 3:
        out["frais_courants"] = g
    tr = _apres(c, LIB_TRANSACTION, FIN_TRANSACTION, pourcents, SANS_TRANSACTION)
    if tr is not None and 0 <= tr <= 3:
        out["couts_transaction"] = tr
    for motif in MOTIFS_DATE:
        m = re.search(motif, c)
        if m:
            out["date_doc"] = m.group(1)
            break
    if isin:
        out["isin_ok"] = isin.lower() in c
    return out


def texte_pdf(octets):
    """Texte d'un PDF ; '' s'il est illisible (chiffré, abîmé)."""
    from pypdf import PdfReader
    try:
        r = PdfReader(io.BytesIO(octets))
        return "\n".join((p.extract_text() or "") for p in r.pages[:6])
    except Exception:  # noqa: BLE001  un PDF illisible ne doit jamais bloquer
        return ""


# ---------- récupération du document ----------

def session():
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = UA
    return s


def page_fundsquare(isin):
    """Adresse stable de la page du fonds sur Fundsquare (recherche par ISIN)."""
    return f"{FUNDSQUARE}/search-results?fastSearch=O&isISIN=O&search={isin}"


def lien_fundsquare(s, isin):
    """Lien du DIC « en cours » sur Fundsquare (le bloc class="courantKIDD" de l'onglet Documents) ; None
    si le fonds n'y a pas de DIC. Les liens contiennent un jeton : on ne les garde pas, on les relit."""
    url = f"{FUNDSQUARE}/search-results?ajaxContentView=renderContent&fastSearch=O&isISIN=O&search={isin}"
    if not permis(s, url):
        return None
    r = s.get(url, timeout=60)
    ids = sorted(set(re.findall(r"idInstr=(\d+)", r.text)))
    if len(ids) != 1:
        return None
    time.sleep(PAUSE)
    url = f"{FUNDSQUARE}/security/documents?ajaxContentView=renderContent&idInstr={ids[0]}&lang=EN"
    if not permis(s, url):
        return None
    r = s.get(url, timeout=60)
    h = None  # la ligne du DIC a plusieurs cellules « courantKIDD » (icône, nom, lien) : on prend le lien
    for m in re.finditer(r'class="courantKIDD"(.*?)(?=class="histoKIDD"|class="courant[A-Z]{4}"|$)', r.text, re.S):
        h = re.search(r'href=["\']([^"\']*download/dl\?[^"\']+)', m.group(1))
        if h:
            break
    if not h:
        return None
    url = h.group(1).replace("&amp;", "&")
    return url if url.startswith("http") else FUNDSQUARE + url


# DIC publiés par les émetteurs eux-mêmes, à une adresse fixe par ISIN (essayés après Fundsquare)
SOURCES_EMETTEURS = (("Amundi ETF", "https://www.amundietf.fr/pdfDocuments/kid-priips/{isin}/FRA/FRA"),)
_ROBOTS = {}


def permis(s, url):
    """Le robots.txt du site permet-il de lire cette adresse ? (lu une fois par site ; injoignable = non)"""
    from urllib.parse import urlparse
    from lectures import robots_permet
    hote = urlparse(url).hostname
    if hote not in _ROBOTS:
        try:
            r = s.get(f"https://{hote}/robots.txt", timeout=20)
            _ROBOTS[hote] = (r.status_code, r.text)
        except Exception:  # noqa: BLE001  dans le doute, on s'abstient
            _ROBOTS[hote] = (403, "")
    statut, texte = _ROBOTS[hote]
    return robots_permet(statut, texte, url, UA)


def telecharger_pdf(s, url):
    if not permis(s, url):
        raise ValueError("lecture interdite par le robots.txt du site")
    r = s.get(url, timeout=120)
    return r.content if r.ok and r.content[:5] == b"%PDF-" else None


def infos_fiche(ticker):
    """Caractéristiques d'un titre (dont son ISIN) d'après le cache de fiches.py ; {} si inconnu."""
    f = CACHE_FICHES / (re.sub(r"[^A-Za-z0-9.-]", "_", ticker) + ".json")
    try:
        return json.loads(f.read_text(encoding="utf-8"))["infos"] or {}
    except (OSError, ValueError, KeyError):
        return {}


def lire_dic(s, ticker, isin):
    """Lit le DIC d'un titre : Fundsquare d'abord, l'émetteur ensuite. Renvoie l'entrée de data/dic.json."""
    essais = []
    try:
        u = lien_fundsquare(s, isin)
        if u:
            essais.append(("Fundsquare", u, page_fundsquare(isin)))
    except Exception as e:  # noqa: BLE001
        print(f"  Fundsquare injoignable pour {ticker} : {e}", file=sys.stderr)
    for nom, modele in SOURCES_EMETTEURS:
        url = modele.format(isin=isin)
        essais.append((nom, url, url))
    erreur = "aucun DIC trouvé"
    for source, url, page in essais:
        time.sleep(PAUSE)
        try:
            pdf = telecharger_pdf(s, url)
        except Exception as e:  # noqa: BLE001
            erreur = f"{source} : {e}"
            continue
        if not pdf:
            erreur = f"{source} : pas un PDF"
            continue
        chiffres = analyser(texte_pdf(pdf), isin)
        if chiffres.get("isin_ok") is False:
            erreur = f"{source} : le DIC ne cite pas l'ISIN {isin}"
            continue
        if "sri" not in chiffres and "frais_courants" not in chiffres:
            erreur = f"{source} : ni SRI ni frais lisibles"
            continue
        chiffres.pop("isin_ok", None)
        return {"isin": isin, "source": source, "page": page, "lu_le": aujourdhui().isoformat(), **chiffres}
    return {"isin": isin, "erreur": erreur, "lu_le": aujourdhui().isoformat()}


# ---------- fichier data/dic.json ----------

def charger():
    try:
        return json.loads(FICHIER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"titres": {}}


def dic_de(ticker, base=None):
    """Chiffres valides du DIC d'un titre (sans les entrées en erreur) ; {} sinon. Utilisé par fiches.py."""
    e = (base if base is not None else charger()).get("titres", {}).get(ticker) or {}
    return e if ("sri" in e or "frais_courants" in e) else {}


def a_relire(e):
    if not e or "erreur" in e or "lu_le" not in e:
        return True
    return (aujourdhui() - date.fromisoformat(e["lu_le"])).days >= VALIDITE_JOURS


def etf_suivis():
    u = json.loads((RACINE / "univers.json").read_text(encoding="utf-8"))
    return [t for c in ("etf", "etf_levier") for t in u.get(c, {})]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tout = "--tout" in sys.argv
    base = charger()
    titres = base.setdefault("titres", {})
    choix = args or etf_suivis()
    s = session()
    lus = 0
    for t in choix:
        inf = infos_fiche(t)
        isin = inf.get("isin")
        if not isin:
            print(f"{t} : ISIN inconnu (fiches.py le lira d'abord)")
            continue
        ancien = titres.get(t)
        if not (tout or args or a_relire(ancien) or (ancien or {}).get("isin") != isin):
            continue
        if lus >= MAX_PAR_PASSAGE:
            break
        lus += 1
        e = lire_dic(s, t, isin)
        if "erreur" in e and dic_de(t, base):  # on garde les anciennes valeurs, en notant l'échec
            e = dict(ancien, echec=e["erreur"], echec_le=e["lu_le"])
        titres[t] = e
        print(f"{t} {isin} : " + (f"SRI {e.get('sri', '?')}, frais {e.get('frais_courants', '?')} %, "
                                  f"transaction {e.get('couts_transaction', '?')} % ({e.get('source')})"
                                  if "erreur" not in e else f"✗ {e['erreur']}"))
    base["maj"] = aujourdhui().isoformat()
    base["_note"] = ("Chiffres lus dans le DIC officiel (PRIIPs) de chaque ETF par scripts/dic.py : Fundsquare "
                     "d'abord, sinon le site de l'émetteur (Amundi ETF). Frais en % par an.")
    base["titres"] = dict(sorted(titres.items()))
    FICHIER.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for e in titres.values() if dic_de("", {"titres": {"": e}}))
    print(f"DIC : {lus} lus, {ok}/{len(titres)} titres avec des chiffres officiels → {FICHIER.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
