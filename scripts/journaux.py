"""Agent « Journaux » : l'actualité des marchés et des entreprises du jour, lue dans de grands journaux
de plusieurs pays, puis vérifiée par le chef d'orchestre (règle : 2 sources concordantes). Choix du
propriétaire du 27/11/2026 (D-20261127-2).

Usage :
  python scripts/journaux.py collecter [AAAA-MM-JJ]
      (agent Journaux, vers 8 h puis 16 h ; à 16 h, le travail du matin est gardé et seuls les nouveaux
      articles sont ajoutés, en infos « NOUVEAU » que le chef relit à 16 h 30) : lit le flux RSS de chaque journal de JOURNAUX (ou, s'il n'en a pas,
      Google Actualités limité au site du journal), garde les articles des dernières 24 h qui parlent de
      marchés ou d'entreprises, puis regroupe ceux qui annoncent la même information (« infos »
      candidates). Écrit data/journaux/AAAA-MM-JJ.json : titres et liens seulement (le texte des
      articles n'est jamais enregistré : droits d'auteur, dépôt public).
  python scripts/journaux.py ajouter <journal> "<titre>" <lien https> <date ISO> [AAAA-MM-JJ]
      (agent Journaux) ajoute un article trouvé à la main (WebSearch limité au site du journal) quand le
      flux du journal est bloqué par le réseau du cloud ; le lien doit être sur le site du journal.
  python scripts/journaux.py regrouper [AAAA-MM-JJ]
      refait les infos candidates après des ajouts (le travail du chef n'a pas encore commencé).
  python scripts/journaux.py lire [AAAA-MM-JJ]
      (chef, vers 8 h 30) affiche les infos candidates et leurs articles, avec le chapeau du flux RSS
      quand il existe (relu en direct, jamais enregistré), pour vérifier chaque regroupement.
  python scripts/journaux.py valider [AAAA-MM-JJ] [--chef]
      contrôle le fichier après le travail du chef et recalcule chaque statut : « confirmée » s'il y a
      au moins 2 journaux différents, sinon « non confirmée ». Avec --chef, note l'heure de vérification
      (la page n'affiche que des nouvelles vérifiées). Code 1 s'il reste un problème.

Le chef corrige data/journaux/AAAA-MM-JJ.json : il sépare les articles regroupés à tort, réunit ceux
qui parlent de la même chose dans deux langues, écrit pour chaque info un titre en français avec ses
propres mots (« titre ») et retire ce qui ne parle ni de marchés ni d'entreprises. Il ne peut pas
inventer de source : seuls les articles collectés comptent.
"""
import html
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parent.parent
DOSSIER = RACINE / "data" / "journaux"
PARIS = ZoneInfo("Europe/Paris")
AGENT = "Mozilla/5.0 (compatible; MatinPEA-journaux/1.0; lecture de flux RSS publics)"
FENETRE_H = 24          # articles publiés dans les 24 h qui précèdent la collecte
MAX_PAR_JOURNAL = 40
MAX_NON_CONFIRMEES = 15  # la page en montre au plus autant (les confirmées : toutes)

# Journaux choisis par le propriétaire (27/11/2026). « rss » : flux officiels essayés dans l'ordre ;
# « filtrer » : flux généraliste, on ne garde que ce qui parle de marchés ou d'entreprises ;
# sans flux qui marche, secours : Google Actualités limité au site (« site:domaine when:1d »), dont
# chaque article doit venir du bon site (balise <source url>).
JOURNAUX = [
    {"id": "wsj", "nom": "The Wall Street Journal", "pays": "États-Unis", "site": "https://www.wsj.com",
     "rss": ["https://feeds.content.dowjones.io/public/rss/mw_topstories"], "langue": "en-US"},
    {"id": "nyt", "nom": "The New York Times", "pays": "États-Unis", "site": "https://www.nytimes.com",
     "rss": ["https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"], "langue": "en-US"},
    {"id": "bloomberg", "nom": "Bloomberg", "pays": "États-Unis", "site": "https://www.bloomberg.com",
     "rss": ["https://feeds.bloomberg.com/markets/news.rss"], "langue": "en-US"},
    {"id": "cnbc", "nom": "CNBC", "pays": "États-Unis", "site": "https://www.cnbc.com",
     "rss": ["https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"], "langue": "en-US"},
    {"id": "reuters", "nom": "Reuters", "pays": "États-Unis", "site": "https://www.reuters.com",
     "rss": [], "langue": "en-US"},  # plus de flux RSS public : Google Actualités
    {"id": "ft", "nom": "Financial Times", "pays": "Royaume-Uni", "site": "https://www.ft.com",
     "rss": ["https://www.ft.com/markets?format=rss", "https://www.ft.com/companies?format=rss"], "langue": "en-GB"},
    {"id": "bbc", "nom": "BBC", "pays": "Royaume-Uni", "site": "https://www.bbc.co.uk",
     "rss": ["https://feeds.bbci.co.uk/news/business/rss.xml"], "langue": "en-GB"},
    {"id": "guardian", "nom": "The Guardian", "pays": "Royaume-Uni", "site": "https://www.theguardian.com",
     "rss": ["https://www.theguardian.com/business/rss"], "langue": "en-GB", "filtrer": True},
    {"id": "economist", "nom": "The Economist", "pays": "Royaume-Uni", "site": "https://www.economist.com",
     "rss": ["https://www.economist.com/finance-and-economics/rss.xml", "https://www.economist.com/business/rss.xml"], "langue": "en-GB"},
    {"id": "figaro", "nom": "Le Figaro", "pays": "France", "site": "https://www.lefigaro.fr",
     "rss": ["https://www.lefigaro.fr/rss/figaro_bourse.xml", "https://www.lefigaro.fr/rss/figaro_economie.xml"], "langue": "fr"},
    {"id": "echos", "nom": "Les Échos", "pays": "France", "site": "https://www.lesechos.fr",
     "rss": ["https://services.lesechos.fr/rss/les-echos-finance-marches.xml"], "langue": "fr"},
    {"id": "monde", "nom": "Le Monde", "pays": "France", "site": "https://www.lemonde.fr",
     "rss": ["https://www.lemonde.fr/economie/rss_full.xml"], "langue": "fr"},
    {"id": "bfm", "nom": "BFM Business", "pays": "France", "site": "https://www.bfmtv.com/economie/",
     "rss": ["https://www.bfmtv.com/rss/economie/"], "langue": "fr"},
    {"id": "lessentiel", "nom": "L'essentiel", "pays": "Luxembourg", "site": "https://www.lessentiel.lu",
     "rss": [], "langue": "fr", "filtrer": True},
    {"id": "wort", "nom": "Luxemburger Wort", "pays": "Luxembourg", "site": "https://www.wort.lu",
     "rss": ["https://www.wort.lu/de/rss"], "langue": "de", "filtrer": True},
    {"id": "paperjam", "nom": "Paperjam", "pays": "Luxembourg", "site": "https://paperjam.lu",
     "rss": [], "langue": "fr", "filtrer": True},
    {"id": "handelsblatt", "nom": "Handelsblatt", "pays": "Allemagne", "site": "https://www.handelsblatt.com",
     "rss": ["https://www.handelsblatt.com/contentexport/feed/finanzen", "https://www.handelsblatt.com/contentexport/feed/unternehmen"], "langue": "de"},
    {"id": "sole", "nom": "Il Sole 24 Ore", "pays": "Italie", "site": "https://www.ilsole24ore.com",
     "rss": ["https://www.ilsole24ore.com/rss/finanza.xml"], "langue": "it"},
    {"id": "expansion", "nom": "Expansión", "pays": "Espagne", "site": "https://www.expansion.com",
     "rss": ["https://e00-expansion.uecdn.es/rss/mercados.xml", "https://e00-expansion.uecdn.es/rss/empresas.xml"], "langue": "es"},
    {"id": "lecho", "nom": "L'Echo", "pays": "Belgique", "site": "https://www.lecho.be",
     "rss": [], "langue": "fr"},
    {"id": "fd", "nom": "Het Financieele Dagblad", "pays": "Pays-Bas", "site": "https://fd.nl",
     "rss": ["https://fd.nl/?rss"], "langue": "nl"},
]
PAR_ID = {j["id"]: j for j in JOURNAUX}
GN_LANGUE = {"en-US": ("en-US", "US", "US:en"), "en-GB": ("en-GB", "GB", "GB:en"), "fr": ("fr", "FR", "FR:fr"),
             "de": ("de", "DE", "DE:de"), "it": ("it", "IT", "IT:it"), "es": ("es", "ES", "ES:es"), "nl": ("nl", "NL", "NL:nl")}

# Mots qui signalent un article de marchés ou d'entreprises (flux généralistes et secours Google)
MOTS_FINANCE = set("""
bourse boursier boursiere action actions actionnaire actionnaires cac marche marches indice indices obligation
obligations taux bce fed inflation resultats resultat chiffre affaires benefice benefices perte pertes dividende
dividendes rachat fusion acquisition introduction entreprise entreprises societe groupe banque banques euro dollar
petrole croissance pib emploi faillite investisseurs investissement fonds etf
stock stocks shares share market markets index earnings revenue profit profits loss dividend merger acquisition
ipo bank banks bond bonds yields rates investors nasdaq dow wall economy inflation tariffs tariff oil company
companies ceo deal
borse boerse aktie aktien anleger markt markte zinsen ezb unternehmen gewinn umsatz konzern dax bank banken
borsa azioni mercati mercato titoli spread banche utili ricavi societa piazza affari
bolsa acciones mercados ibex empresa empresas beneficio beneficios banco bancos
beurs aandelen aex rente bedrijf bedrijven winst omzet banken
""".split())

# Mots trop généraux pour prouver à eux seuls que deux articles parlent de la même chose
FAIBLES = set("""
trump biden europe european europeenne europa us usa america american americaine china chinese chine chinois
wall street stocks markets market bourse bourses world monde global economie economy euro dollar uk france
germany allemagne deutschland italia italie espana espagne nederland luxembourg belgique belgium
monday tuesday wednesday thursday friday lundi mardi mercredi jeudi vendredi samedi dimanche
montag dienstag mittwoch donnerstag freitag new york london londres paris investors investisseurs
week semaine woche settimana semana rally shares share stock deal deals sales ceo pdg video live markets wrap
""".split())

# Mots vides (toutes langues des journaux) : ignorés pour la ressemblance des titres
VIDES = set("""
the a an of to in on for and or but with from by at as is are was were be been it its this that these
those after before over under into amid about than more most new says say said will would could can may
how why what who when where which while just not no up down out off his her their our your you we they
le la les un une des du de d l au aux et ou mais avec pour par sur dans en est sont a ont ce cet cette ces
qui que quoi dont ou plus moins pas ne se sa son ses leur leurs nous vous ils elles il elle apres avant
selon face vers entre sous comme tout tous toute toutes fait faire va
der die das ein eine einer eines und oder mit fur von zu im in am auf aus bei nach vor uber unter ist sind
war wird werden hat haben nicht auch noch wie was wer den dem des sich
il lo gli i una uno di da del della dei delle e o con per su tra fra non piu come che chi
el los las unos unas y o con para por sobre en es son mas como que quien al
het de een en of met voor van op in uit bij naar is zijn wordt niet ook nog hoe wat
""".split())

# Mêmes choses dans plusieurs langues : ramenées à un seul mot pour comparer les titres
SYNONYMES = {
    "ecb": "bce", "ezb": "bce", "lagarde": "bce",
    "federal": "fed", "reserve": "fed", "powell": "fed",
    "oil": "petrole", "ol": "petrole", "petrolio": "petrole", "petroleo": "petrole", "olie": "petrole",
    "brent": "petrole", "opec": "opep", "opep": "opep",
    "inflazione": "inflation", "inflacion": "inflation", "inflatie": "inflation",
    "zolle": "droits_douane", "tariffs": "droits_douane", "tariff": "droits_douane", "dazi": "droits_douane",
    "aranceles": "droits_douane", "douane": "droits_douane", "heffingen": "droits_douane",
    "earnings": "resultats", "ergebnis": "resultats", "trimestrali": "resultats", "cijfers": "resultats",
    "bitcoin": "bitcoin", "btc": "bitcoin",
}


# ---------- texte ----------

def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def mots(titre):
    """Mots utiles d'un titre, en minuscules, sans accents, synonymes ramenés à un seul mot."""
    brut = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’-]*", titre or "")
    out = []
    for m in brut:
        m = sans_accents(m.lower()).strip(".'’-")
        m = re.sub(r"['’]s$", "", m)
        m = re.sub(r"^[ld]['’]", "", m)
        if len(m) < 2 or m in VIDES:
            continue
        out.append(SYNONYMES.get(m, m))
    return out


MOT = r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’-]*"


def _norm(m):
    n = sans_accents(m.lower()).strip(".'’-")
    n = re.sub(r"['’]s$", "", n)
    return re.sub(r"^[ld]['’]", "", n)


def en_majuscules_partout(titre):
    """Titre « à l'anglaise » (Stocks Rally at End of a Week) : la majuscule n'y dit rien d'un nom propre."""
    brut = [m for m in re.findall(MOT, titre or "") if len(m) > 3]
    return len(brut) >= 4 and sum(m[:1].isupper() for m in brut) / len(brut) > 0.6


def vocabulaire(titres):
    """Noms propres du jour : mots écrits avec une majuscule au milieu d'un titre ordinaire (pas « à
    l'anglaise »), et sigles. Un nom propre en premier mot (« Thales confirme… ») est reconnu s'il
    figure dans un autre titre."""
    v = set()
    for t in titres:
        brut = re.findall(MOT, t or "")
        ordinaire = not en_majuscules_partout(t)
        for i, m in enumerate(brut):
            n = _norm(m)
            if len(n) < 3 or n in VIDES or n.isdigit():
                continue
            if (m.isupper() and len(m) >= 2) or (ordinaire and i > 0 and m[:1].isupper()):
                v.add(SYNONYMES.get(n, n))
    return v - FAIBLES


def entites(titre, vocab=None):
    """Noms propres d'un titre : ses mots qui sont dans le vocabulaire du jour, plus ceux que SYNONYMES
    ramène à un seul mot (BCE, Fed, pétrole…) ; sans les mots trop généraux (FAIBLES)."""
    vocab = vocabulaire([titre]) if vocab is None else vocab
    out = set()
    for m in re.findall(MOT, titre or ""):
        n = _norm(m)
        if len(n) < 3 or n in VIDES:
            continue
        n2 = SYNONYMES.get(n, n)
        if (n2 in vocab or n != n2) and n2 not in FAIBLES:
            out.add(n2)
    return out


def parle_finance(titre, resume=""):
    return bool(set(mots(titre + " " + (resume or ""))) & MOTS_FINANCE)


def nettoyer(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()


# ---------- lecture des flux ----------

def telecharger(url, essais=2):
    err = None
    for _ in range(essais):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read(5_000_000)
        except Exception as e:  # noqa: BLE001  une panne de site n'arrête jamais la collecte
            err = e
    raise err


def _date(txt):
    if not txt:
        return None
    try:
        d = parsedate_to_datetime(txt)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(txt.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def lire_flux(donnees):
    """Articles d'un flux RSS 2.0 ou Atom : [{titre, lien, publie (datetime), resume, source_url}]."""
    racine = ET.fromstring(donnees)
    ns_atom = "{http://www.w3.org/2005/Atom}"
    out = []
    for it in racine.iter("item"):
        src = it.find("source")
        out.append({"titre": nettoyer(it.findtext("title")), "lien": (it.findtext("link") or "").strip(),
                    "publie": _date(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date")),
                    "resume": nettoyer(it.findtext("description"))[:400],
                    "source_url": src.get("url") if src is not None else None})
    for it in racine.iter(ns_atom + "entry"):
        lien = it.find(ns_atom + "link")
        out.append({"titre": nettoyer(it.findtext(ns_atom + "title")), "lien": lien.get("href") if lien is not None else "",
                    "publie": _date(it.findtext(ns_atom + "updated") or it.findtext(ns_atom + "published")),
                    "resume": nettoyer(it.findtext(ns_atom + "summary"))[:400], "source_url": None})
    return [a for a in out if a["titre"] and a["lien"].startswith("https://")]


def domaine(url):
    h = (urllib.parse.urlparse(url or "").hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def url_google(j):
    hl, gl, ceid = GN_LANGUE[j["langue"]]
    q = urllib.parse.quote(f"site:{domaine(j['site'])} when:1d")
    return f"https://news.google.com/rss/search?q={q}&hl={hl}&gl={gl}&ceid={ceid}"


def articles_du_journal(j, depuis):
    """Articles récents d'un journal : (articles, voie, erreur). Voie : « rss » ou « google »."""
    erreurs, voie, bruts = [], None, []
    for u in j["rss"]:
        try:
            a = lire_flux(telecharger(u))
            if a:
                bruts += a
                voie = "rss"
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"{domaine(u)} : {type(e).__name__}")
    if not bruts:  # secours : Google Actualités, seulement les articles de ce site
        try:
            a = lire_flux(telecharger(url_google(j)))
            dom = domaine(j["site"])
            bruts = [x for x in a if x["source_url"] and domaine(x["source_url"]).endswith(dom)]
            for x in bruts:  # « Titre - Reuters » : on retire le nom du journal ajouté par Google
                x["titre"] = re.sub(r"\s+[-–|]\s+[^-–|]{2,40}$", "", x["titre"])
            voie = "google" if bruts else voie
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"Google Actualités : {type(e).__name__}")
    filtrer = j.get("filtrer") or voie == "google"
    vus, out = set(), []
    for x in sorted(bruts, key=lambda x: x["publie"] or depuis, reverse=True):
        cle = " ".join(mots(x["titre"]))  # même article publié deux fois (« – 27/11 » et « - 27/11 »)
        if not x["publie"] or x["publie"] < depuis or x["lien"] in vus or cle in vus:
            continue
        if filtrer and not parle_finance(x["titre"], x["resume"]):
            continue
        vus |= {x["lien"], cle}
        out.append(x)
    return out[:MAX_PAR_JOURNAL], voie, "; ".join(erreurs) or None


# ---------- regroupement ----------

def meme_info(a, b, vocab=None):
    """Deux titres de journaux différents annoncent-ils la même information ? Il faut au moins un nom
    propre commun (pas un mot trop général) et, en plus, un second nom commun ou des titres assez proches."""
    if vocab is None:
        vocab = vocabulaire([a, b])
    communs = entites(a, vocab) & entites(b, vocab)
    if not communs:
        return False
    if len(communs) >= 2:
        return True
    ma, mb = set(mots(a)), set(mots(b))
    return len(ma & mb) / max(1, len(ma | mb)) >= 0.2


def regrouper(articles):
    """Infos candidates. Un article rejoint le groupe dont il ressemble à au moins la moitié des articles
    (pas de chaîne A ~ B ~ C qui mélangerait des sujets différents) ; sinon il ouvre un nouveau groupe.
    Deux articles d'un même journal ne se confirment jamais entre eux."""
    vocab = vocabulaire(a["titre"] for a in articles)
    groupes = []
    for a in sorted(articles, key=lambda a: a["publie"]):
        meilleur, score = None, 0.0
        for g in groupes:
            autres = [x for x in g if x["journal"] != a["journal"]]
            if not autres:
                continue
            f = sum(meme_info(a["titre"], x["titre"], vocab) for x in autres) / len(g)
            if f >= 0.5 and f > score:
                meilleur, score = g, f
        if meilleur is None:
            groupes.append([a])
        else:
            meilleur.append(a)
    infos = []
    for g in sorted(groupes, key=lambda g: (-len({x["journal"] for x in g}), g[-1]["publie"].timestamp() * -1)):
        infos.append({"id": f"i{len(infos) + 1}", "articles": [x["id"] for x in g], "titre": "", "titre_origine": g[-1]["titre"]})
    return infos


# ---------- fichier du jour ----------

def chemin(jour):
    return DOSSIER / f"{jour}.json"


def statut(info, arts):
    journaux = {arts[a]["journal"] for a in info["articles"] if a in arts}
    return ("confirmee" if len(journaux) >= 2 else "non_confirmee"), len(journaux)


def collecter(jour, maintenant=None):
    maintenant = maintenant or datetime.now(timezone.utc)
    depuis = maintenant - timedelta(hours=FENETRE_H)
    articles, etat = [], {}
    for j in JOURNAUX:
        a, voie, err = articles_du_journal(j, depuis)
        etat[j["id"]] = {"nom": j["nom"], "pays": j["pays"], "site": j["site"], "voie": voie, "articles": len(a), "erreur": err}
        for x in a:
            articles.append({"journal": j["id"], "titre": x["titre"][:300], "lien": x["lien"], "publie": x["publie"]})
        print(f"{j['nom']:<26} {voie or '—':<7} {len(a):>3} article(s){' · ' + err if err else ''}")
    articles.sort(key=lambda a: a["publie"], reverse=True)
    f = chemin(jour)
    ancien = json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    if ancien:  # second passage du jour (16 h) : on garde tout le travail du matin, on ajoute les nouveaux
        vus = {a["lien"] for a in ancien["articles"]}
        articles = [a for a in articles if a["lien"] not in vus]
        n0 = max([int(a["id"][1:]) for a in ancien["articles"]] or [0])
    else:
        n0 = 0
    for n, a in enumerate(articles, n0 + 1):
        a["id"] = f"a{n}"
    infos = regrouper(articles)  # nouvelles infos candidates (le chef les réunit aux anciennes s'il le faut)
    for a in articles:
        a["publie"] = a["publie"].astimezone(PARIS).isoformat(timespec="minutes")
    if ancien:
        k0 = max([int(i["id"][1:]) for i in ancien["infos"]] or [0])
        for k, i in enumerate(infos, k0 + 1):
            i["id"] = f"i{k}"
        for jid, e in etat.items():  # nombre d'articles du jour par journal, matin et après-midi
            e["articles"] += ancien["journaux"].get(jid, {}).get("articles", 0)
        articles, infos = ancien["articles"] + articles, ancien["infos"] + infos
    arts = {a["id"]: a for a in articles}
    for i in infos:
        i["statut"], i["nb_journaux"] = statut(i, arts)
    d = {"date": jour, "collecte_le": maintenant.astimezone(PARIS).isoformat(timespec="minutes"),
         "regle": "confirmée = au moins 2 journaux différents ; sinon non confirmée",
         "journaux": etat, "articles": articles, "infos": infos, "chef": ancien.get("chef") if ancien else None}
    if ancien:
        d["passages"] = ancien.get("passages", [ancien.get("collecte_le")]) + [d["collecte_le"]]
    DOSSIER.mkdir(parents=True, exist_ok=True)
    chemin(jour).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    nc = sum(i["statut"] == "confirmee" for i in infos)
    lus = sum(1 for e in etat.values() if e["articles"])
    print(f"\n{len(articles)} articles de {lus}/{len(JOURNAUX)} journaux, {len(infos)} infos dont {nc} à 2 sources ou plus → {chemin(jour)}")
    return d


def ajouter(jour, journal, titre, lien, date_iso):
    """Article ajouté à la main par l'agent Journaux (flux bloqué) : même règles que la collecte."""
    if journal not in PAR_ID:
        raise SystemExit(f"journal inconnu : {journal} (choix : {', '.join(PAR_ID)})")
    dom = domaine(PAR_ID[journal]["site"])
    if not lien.startswith("https://") or not domaine(lien).endswith(dom):
        raise SystemExit(f"le lien doit être en https sur {dom}")
    pub = _date(date_iso)
    if pub is None:
        raise SystemExit("date illisible (format attendu : 2026-11-28T07:40+01:00)")
    f = chemin(jour)
    d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {
        "date": jour, "collecte_le": datetime.now(PARIS).isoformat(timespec="minutes"),
        "regle": "confirmée = au moins 2 journaux différents ; sinon non confirmée",
        "journaux": {j["id"]: {"nom": j["nom"], "pays": j["pays"], "site": j["site"], "voie": None, "articles": 0, "erreur": None} for j in JOURNAUX},
        "articles": [], "infos": [], "chef": None}
    if any(a["lien"] == lien for a in d["articles"]):
        print("déjà présent")
        return
    n = max([int(a["id"][1:]) for a in d["articles"]] or [0]) + 1
    d["articles"].append({"journal": journal, "titre": nettoyer(titre)[:300], "lien": lien,
                          "publie": pub.astimezone(PARIS).isoformat(timespec="minutes"), "id": f"a{n}", "ajoute_a_la_main": True})
    e = d["journaux"].setdefault(journal, {"nom": PAR_ID[journal]["nom"], "pays": PAR_ID[journal]["pays"], "site": PAR_ID[journal]["site"]})
    e["articles"] = e.get("articles", 0) + 1
    e["voie"] = e.get("voie") or "recherche"
    d["infos"].append({"id": f"i{len(d['infos']) + 1}", "articles": [f"a{n}"], "titre": "", "titre_origine": d["articles"][-1]["titre"]})
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"a{n} ajouté ({PAR_ID[journal]['nom']})")


def refaire_groupes(jour):
    f = chemin(jour)
    d = json.loads(f.read_text(encoding="utf-8"))
    gardees = [i for i in d["infos"] if i.get("verifie")]  # le travail du chef n'est jamais refait
    pris = {a for i in gardees for a in i["articles"]}
    arts = [dict(a, publie=datetime.fromisoformat(a["publie"])) for a in d["articles"] if a["id"] not in pris]
    nouvelles = regrouper(arts)
    k0 = max([int(i["id"][1:]) for i in gardees] or [0])
    for k, i in enumerate(nouvelles, k0 + 1):
        i["id"] = f"i{k}"
    d["infos"] = gardees + nouvelles
    par = {a["id"]: a for a in d["articles"]}
    for i in d["infos"]:
        i["statut"], i["nb_journaux"] = statut(i, par)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(d['infos'])} infos, dont {sum(i['statut'] == 'confirmee' for i in d['infos'])} à 2 journaux ou plus")


def lire(jour):
    d = json.loads(chemin(jour).read_text(encoding="utf-8"))
    arts = {a["id"]: a for a in d["articles"]}
    chapeaux = {}
    for j in JOURNAUX:  # chapeaux relus en direct pour aider le chef (jamais enregistrés)
        if not any(a["journal"] == j["id"] for a in d["articles"]):
            continue
        for u in j["rss"] or [url_google(j)]:
            try:
                for x in lire_flux(telecharger(u, 1)):
                    chapeaux[x["lien"]] = x["resume"][:240]
            except Exception:  # noqa: BLE001
                pass
    for i in d["infos"]:
        st, n = statut(i, arts)
        print(f"\n[{i['id']}]{'' if i.get('verifie') else ' NOUVEAU'} {'✓' if st == 'confirmee' else '·'} {n} journal(aux) · titre chef : {i.get('titre') or '—'}")
        for a in i["articles"]:
            x = arts[a]
            print(f"   {a} {PAR_ID[x['journal']]['nom']} ({x['publie'][11:16]}) : {x['titre']}\n      {x['lien']}")
            if chapeaux.get(x["lien"]):
                print(f"      « {chapeaux[x['lien']]} »")


def problemes(d):
    """Règles que le fichier du jour doit respecter (contrôlées après chaque passage du chef)."""
    pb = []
    arts = {a["id"]: a for a in d.get("articles", [])}
    vus = set()
    for a in arts.values():
        if a["journal"] not in PAR_ID:
            pb.append(f"{a['id']} : journal inconnu « {a['journal']} » (seuls ceux de JOURNAUX comptent)")
        if not str(a.get("lien", "")).startswith("https://"):
            pb.append(f"{a['id']} : lien non https")
    for i in d.get("infos", []):
        if not i.get("articles"):
            pb.append(f"{i.get('id')} : aucune source")
            continue
        for a in i["articles"]:
            if a not in arts:
                pb.append(f"{i['id']} : article {a} inexistant (une source ne s'invente pas)")
            if a in vus:
                pb.append(f"{i['id']} : article {a} déjà utilisé par une autre info")
            vus.add(a)
        t = i.get("titre") or ""
        if i.get("verifie") and not t.strip():
            pb.append(f"{i['id']} : titre en français manquant")
        if len(t) > 180:
            pb.append(f"{i['id']} : titre trop long ({len(t)} caractères, 180 au plus)")
        if i.get("lien") and i["lien"] not in {arts[a]["lien"] for a in i["articles"] if a in arts}:
            pb.append(f"{i['id']} : le lien choisi n'est pas celui d'un de ses articles")
    return pb


def valider(jour, par_chef=False):
    f = chemin(jour)
    d = json.loads(f.read_text(encoding="utf-8"))
    arts = {a["id"]: a for a in d["articles"]}
    for i in d["infos"]:
        i["statut"], i["nb_journaux"] = statut(i, arts)
    pb = []
    if par_chef:  # le chef a relu toutes les infos du fichier : chacune doit avoir son titre en français
        pb = [f"{i['id']} : titre en français manquant" for i in d["infos"] if not (i.get("titre") or "").strip()]
        if not pb:
            for i in d["infos"]:
                i["verifie"] = True
            d["chef"] = {"verifie_le": datetime.now(PARIS).isoformat(timespec="minutes")}
    pb += problemes(d)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for p in pb:
        print("✗", p)
    nc = sum(i["statut"] == "confirmee" for i in d["infos"])
    print(f"{len(d['infos'])} infos, {nc} confirmées (2 journaux ou plus), {len(pb)} problème(s)")
    return not pb


def pour_la_page(jour, jours_max=3):
    """Nouvelles vérifiées par le chef pour la fiche : le fichier le plus récent (au plus 3 jours avant)
    qui a été vérifié. Confirmées d'abord (lien vers un article), puis au plus 15 non confirmées (lien
    vers le site du journal). None s'il n'y en a pas."""
    try:
        j0 = datetime.strptime(jour, "%Y-%m-%d").date()
    except ValueError:
        return None
    for k in range(jours_max + 1):
        f = chemin((j0 - timedelta(days=k)).isoformat())
        if not f.exists():
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not d.get("chef"):
            continue
        if any("verifie" in i for i in d["infos"]):  # seulement ce que le chef a relu (pas le passage de 16 h en attente)
            d["infos"] = [i for i in d["infos"] if i.get("verifie")]
        if problemes(d):
            continue
        arts = {a["id"]: a for a in d["articles"]}
        out = []
        for i in d["infos"]:
            st, n = statut(i, arts)
            A = sorted((arts[a] for a in i["articles"] if a in arts), key=lambda a: a["publie"])
            if not A:
                continue
            noms = []
            for a in A:
                if PAR_ID[a["journal"]]["nom"] not in noms:
                    noms.append(PAR_ID[a["journal"]]["nom"])
            if st == "confirmee":
                lien = i.get("lien") or next((a["lien"] for a in A if "news.google." not in a["lien"]), A[0]["lien"])
                choisi = next((a for a in A if a["lien"] == lien), A[0])
                lien_nom = PAR_ID[choisi["journal"]]["nom"]
            else:
                lien, lien_nom = PAR_ID[A[0]["journal"]]["site"], PAR_ID[A[0]["journal"]]["nom"]
            out.append({"titre": (i.get("titre") or i.get("titre_origine") or A[-1]["titre"]).strip(),
                        "confirmee": st == "confirmee", "nb": n, "journaux": noms, "lien": lien, "lien_nom": lien_nom,
                        "heure": A[-1]["publie"]})
        conf = sorted((x for x in out if x["confirmee"]), key=lambda x: (x["nb"], x["heure"]), reverse=True)
        non = sorted((x for x in out if not x["confirmee"]), key=lambda x: x["heure"], reverse=True)[:MAX_NON_CONFIRMEES]
        lus = [e["nom"] for e in d["journaux"].values() if e.get("articles")]
        return {"date": d["date"], "verifie_le": d["chef"]["verifie_le"], "infos": conf + non,
                "journaux_lus": len(lus), "journaux_total": len(d["journaux"])}
    return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("collecter", "ajouter", "regrouper", "lire", "valider"):
        print(__doc__)
        sys.exit(2)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import paris
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    if sys.argv[1] == "ajouter":
        if len(args) < 4:
            raise SystemExit('usage : journaux.py ajouter <journal> "<titre>" <lien> <date ISO> [AAAA-MM-JJ]')
        ajouter(args[4] if len(args) > 4 else paris.aujourdhui().isoformat(), *args[:4])
        return
    jour = args[0] if args else paris.aujourdhui().isoformat()
    if sys.argv[1] == "regrouper":
        refaire_groupes(jour)
    elif sys.argv[1] == "collecter":
        collecter(jour)
    elif sys.argv[1] == "lire":
        lire(jour)
    else:
        sys.exit(0 if valider(jour, "--chef" in sys.argv) else 1)


if __name__ == "__main__":
    main()
