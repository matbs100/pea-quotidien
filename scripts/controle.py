"""Contrôle qualité du « chef d'orchestre » : vérifie tout Matin PEA sans rien modifier, sauf
pilotage/etat.json.

Usage : python scripts/controle.py [--hors-ligne]
  --hors-ligne : saute ce qui a besoin d'Internet (prix revérifiés, liens, site en ligne) et
                 garde les résultats réseau du dernier contrôle du jour s'il y en a un.
Vérifie : tests, fraîcheur de la fiche, cohérence des données et de l'analyse, prix (échantillon
revérifié sur Boursorama), liens des fiches (échantillon tournant, robots.txt respecté), page du
dépôt et site en ligne, documentation (ARCHITECTURE.md, journaux, notes Obsidian) et travail des
agents (commits des 30 dernières heures comparés à leurs règles).
Écrit pilotage/etat.json (lu par la fiche et par les agents) et affiche un résumé en Markdown.
Code de sortie : 0 vert, 1 orange (à surveiller), 2 rouge (à corriger avant la prochaine fiche).
"""
import ast
import json
import math
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from fnmatch import fnmatch
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data"
ETAT = RACINE / "pilotage" / "etat.json"
PARIS = ZoneInfo("Europe/Paris")
sys.path.insert(0, str(RACINE / "scripts"))

NIVEAUX = ("ok", "non_verifiable", "alerte", "probleme")  # du meilleur au pire
EMOJI = {"ok": "✅", "non_verifiable": "⚪", "alerte": "🟠", "probleme": "🔴"}
COULEUR = {"vert": "🟢", "orange": "🟠", "rouge": "🔴"}
RESEAU = ("prix", "liens", "site")
TITRES_ANALYSE = ["Le marché en une phrase", "Ce que disent les données", "Ce qui a changé",
                  "Fiabilité des signaux", "À garder en tête", "Pour apprendre"]
CONSEIL = re.compile(r"(?<![A-Za-z]['’])\b(achète|achetez|vends|vendez)\b|\bmets?\s+\d+\s?€", re.I)
RANG_MOMENT = {"ouverture": 0, "cloture": 1}

# Fichiers que chaque agent ne doit pas modifier (le chef juge les cas limites)
HORS_ROLE = {  # mes-investissements.md : tenu par Mathieu seul, aucun agent n'y touche
    "fiche": ["scripts/*", "AMELIORATION.md", "CHEF.md", "ROUTINE.md", "UNIVERS.md", "ARCHITECTURE.md", "config.json",
              "pilotage/*", "apprentissage/*", "mes-investissements.md", "guide/*"],
    "nuit": ["AMELIORATION.md", "CHEF.md", "ROUTINE.md", "UNIVERS.md", "config.json", "pilotage/*", "data/*",
             "mes-investissements.md", "guide/*"],
    "chef": ["AMELIORATION.md", "CHEF.md", "ROUTINE.md", "UNIVERS.md", "config.json", "data/jours/*",
             "data/analyses/*", "data/signaux.csv", "data/historique.csv", "mes-investissements.md", "guide/*"],
    "univers": ["scripts/*", "AMELIORATION.md", "CHEF.md", "ROUTINE.md", "UNIVERS.md", "ARCHITECTURE.md",
                "config.json", "data/*", "docs/*", "notes/*", "apprentissage/*", "mes-investissements.md",
                "guide/*", "pilotage/*"],
}
# exceptions : filet de sécurité de la fiche ; pistes de nouveaux titres (nuit) ; rapport du samedi
PERMIS = {"fiche": ["apprentissage/idees.md"], "nuit": ["pilotage/candidats.md"],
          "univers": ["pilotage/candidats.md"]}
PERMIS_MOTIFS = {"univers": ["pilotage/univers/*"]}
MAX_LIGNES = {"nuit": 300, "chef": 250}         # lignes de code modifiées par passage


def controle(nom, titre, niveau, resume, details=None):
    return {"nom": nom, "titre": titre, "niveau": niveau, "resume": resume, "details": list(details or [])[:20]}


def pire(niveaux):
    niveaux = list(niveaux)
    return max(niveaux, key=NIVEAUX.index) if niveaux else "ok"


def lire(chemin):
    return chemin.read_text(encoding="utf-8") if chemin.exists() else ""


# ---------- tests et fraîcheur ----------

def c_tests():
    r = subprocess.run([sys.executable, str(RACINE / "scripts" / "tests.py")],
                       capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+)/(\d+) tests réussis", r.stdout)
    lignes = [l for l in r.stdout.splitlines() if l.startswith(("✗", "•"))]
    resume = f"{m.group(1)}/{m.group(2)} tests réussis" if m else "résultat des tests illisible"
    return controle("tests", "Tests garde-fous", "ok" if r.returncode == 0 else "probleme", resume, lignes)


def fiche_attendue(maintenant):
    """(jour, moment) de la fiche la plus récente qui devrait être en ligne à cet instant (heure de
    Paris). Marges : la fiche d'ouverture paraît vers 9 h 30, celle de clôture vers 18 h 10."""
    from collecte import bourse_fermee
    j, minutes = maintenant.date(), maintenant.hour * 60 + maintenant.minute
    if not bourse_fermee(j):
        if minutes >= 18 * 60 + 50:
            return str(j), "cloture"
        if minutes >= 10 * 60:
            return str(j), "ouverture"
    j -= timedelta(days=1)
    while bourse_fermee(j):
        j -= timedelta(days=1)
    return str(j), "cloture"


def c_fraicheur(d, maintenant):
    jour_a, moment_a = fiche_attendue(maintenant)
    details = [f"dernière fiche : {d['date']} ({d.get('moment', '?')}), générée le {d.get('genere_le', '?')}",
               f"fiche attendue à cette heure : {jour_a} ({moment_a})"]
    titre = "Fraîcheur de la fiche"
    if (d["date"], RANG_MOMENT.get(d.get("moment"), 1)) < (jour_a, RANG_MOMENT[moment_a]):
        return controle("fraicheur", titre, "probleme", f"fiche manquante : {jour_a} ({moment_a})", details)
    if d.get("moment") == "cloture" and d.get("genere_le"):
        g = datetime.fromisoformat(d["genere_le"])
        if str(g.date()) == d["date"] and g.hour * 60 + g.minute < 17 * 60 + 35:
            return controle("fraicheur", titre, "probleme", "fiche de clôture générée avant le fixing de 17 h 35", details)
    return controle("fraicheur", titre, "ok", "la dernière fiche est bien celle attendue", details)


# ---------- données et analyse ----------

def anomalies_donnees(d):
    """(problèmes, alertes) : incohérences des données d'une fiche ; deux listes vides si tout va bien."""
    pb, al = [], []
    for k in ("date", "indices", "devises", "top30", "petites", "regles"):
        if k not in d:
            pb.append(f"clé absente : {k}")
    if pb:
        return pb, al
    for groupe in ("indices", "devises", "matieres", "top30", "petites"):
        for m in d.get(groupe, []):
            t, p = m.get("ticker", "?"), m.get("prix")
            if not isinstance(p, (int, float)) or not math.isfinite(p) or p <= 0:
                pb.append(f"{t} : prix invalide ({p})")
                continue
            v, rsi, vol = m.get("var_1j"), m.get("rsi"), m.get("volatilite")
            seuil = 10 if groupe == "indices" else 25
            if isinstance(v, (int, float)) and abs(v) > seuil and t != "^VIX":
                al.append(f"{t} : {v:+.1f} % sur la séance, à confirmer (division d'action, erreur ?)")
            if isinstance(rsi, (int, float)) and not 0 <= rsi <= 100:
                pb.append(f"{t} : RSI impossible ({rsi})")
            if isinstance(vol, (int, float)) and not 0 <= vol <= 400:
                pb.append(f"{t} : volatilité impossible ({vol})")
            if groupe in ("top30", "petites") and m.get("date_cours") not in (None, d["date"]):
                al.append(f"{t} : cours daté du {m.get('date_cours')}, pas du {d['date']}")
    tickers = [m["ticker"] for m in d["top30"]]
    if len(tickers) != 30:
        pb.append(f"top 30 : {len(tickers)} titres au lieu de 30")
    if len(set(tickers)) != len(tickers):
        pb.append("top 30 : titre en double")
    if sum(m.get("categorie") == "etf" for m in d["top30"]) < 8:
        al.append("top 30 : moins de 8 ETF (règle de diversification)")
    for m in d["petites"]:
        if isinstance(m.get("prix"), (int, float)) and m["prix"] >= 2:
            pb.append(f"petits prix : {m['ticker']} vaut {m['prix']} €, pas moins de 2 €")
    if len(d["petites"]) < 10:
        al.append(f"petits prix : {len(d['petites'])} titres au lieu de 10")
    for e in (d.get("mes_investissements") or {}).get("erreurs", []):
        al.append(f"mes investissements : {e.get('ticker')} : {e.get('message')} (à corriger par Mathieu)")
    eu = next((m for m in d["devises"] if m.get("ticker") == "EURUSD=X"), None)
    if not eu:
        pb.append("euro/dollar absent")
    elif not 0.8 <= eu["prix"] <= 1.6:
        pb.append(f"euro/dollar improbable : {eu['prix']}")
    det = d.get("details", {})
    sans = [t for t in tickers + [m["ticker"] for m in d["petites"]] if t not in det]
    if det and sans:
        al.append(f"{len(sans)} titres sans fiche détaillée : {', '.join(sans[:6])}")
    cs = d.get("controle_sources")
    if not cs:
        al.append("contrôle des prix entre sources absent")
    elif cs.get("ecart", 0) > 3:
        al.append(f"{cs['ecart']} écarts entre sources : " + ", ".join(e["ticker"] for e in cs.get("ecarts", [])[:6]))
    return pb, al


def c_donnees(d):
    pb, al = anomalies_donnees(d)
    n = sum(len(d.get(g, [])) for g in ("indices", "devises", "matieres", "top30", "petites"))
    niveau = "probleme" if pb else "alerte" if al else "ok"
    cs = d.get("controle_sources") or {}
    resume = f"{n} cours examinés, {len(pb)} problème(s), {len(al)} alerte(s)"
    if cs:
        resume += f" ; entre sources : {cs.get('ok', 0)} confirmés, {cs.get('ecart', 0)} écart(s)"
    return controle("donnees", "Cohérence des données", niveau, resume, pb + al)


def chiffres_incoherents(analyse, d):
    """Variations en gras citées au début de l'analyse (« CAC 40 **+0,34 %** ») qui ne collent pas
    aux données du jour, arrondi compris. Les chiffres sur plusieurs jours ou mois sont ignorés."""
    debut = analyse.split("### Ce qui a changé")[0]
    ecarts = []
    for m in d.get("indices", []) + d.get("devises", []) + d.get("matieres", []) + d.get("top30", []):
        nom, v = m.get("nom", "").split(" (")[0].strip(), m.get("var_1j")
        if len(nom) < 3 or not isinstance(v, (int, float)):
            continue
        motif = re.escape(nom) + r"[^\n%]{0,25}?\*\*\s*([+−-]\s?\d+(?:,\d+)?)\s?%\s*\*\*"
        for x in re.finditer(motif, debut):
            if re.search(r"\b(mois|semaines?|ans?|année|trimestre|depuis|jours)\b", debut[x.end():x.end() + 30]):
                continue
            txt = x.group(1).replace("−", "-").replace(" ", "").replace(",", ".")
            dec = len(txt.split(".")[1]) if "." in txt else 0
            if abs(float(txt) - v) > 0.5 * 10 ** -dec + 0.011:
                ecarts.append(f"« {nom} {x.group(1)} % » dans l'analyse, {v:+.2f} % dans les données")
    return ecarts


def c_analyse(d):
    titre = "Analyse du jour"
    texte = lire(DATA / "analyses" / f"{d['date']}.md")
    if not texte:
        return controle("analyse", titre, "probleme", "analyse absente")
    pb, al = [], []
    al += [f"titre manquant : {t}" for t in TITRES_ANALYSE if f"### {t}" not in texte]
    mots = sum(1 for w in texte.split() if re.search(r"[A-Za-zÀ-ÿ0-9]", w))
    if mots > 380:
        al.append(f"{mots} mots (350 au plus)")
    if d.get("moment") == "cloture" and not texte.lstrip().startswith("*Mise à jour à la clôture"):
        al.append("la version de clôture ne commence pas par « Mise à jour à la clôture de la séance »")
    if CONSEIL.search(texte):
        pb.append("formulation de conseil d'investissement : " + CONSEIL.search(texte).group(0))
    al += chiffres_incoherents(texte, d)
    niveau = "probleme" if pb else "alerte" if al else "ok"
    return controle("analyse", titre, niveau, f"{mots} mots, {len(pb) + len(al)} remarque(s)", pb + al)


# ---------- réseau : prix, liens, site ----------

def telecharger(url):
    """Réponse HTTP (redirections suivies), ou None si le site est injoignable d'ici."""
    import verif
    time.sleep(verif.PAUSE)
    try:
        return verif.session.get(url, timeout=20)
    except Exception:  # noqa: BLE001  réseau coupé, domaine non autorisé, délai dépassé
        return None


ROBOTS = {}


def robots_autorise(url):
    """True / False selon robots.txt du site, None si le site est injoignable."""
    dom = urlparse(url).netloc
    if dom not in ROBOTS:
        r = telecharger(f"https://{dom}/robots.txt")
        rp = RobotFileParser()
        if r is None:
            rp = None
        elif r.status_code == 200:
            rp.parse(r.text.splitlines())
        elif r.status_code in (401, 403):
            rp.disallow_all = True
        else:
            rp.allow_all = True
        ROBOTS[dom] = rp
    return None if ROBOTS[dom] is None else ROBOTS[dom].can_fetch("*", url)


def cours_comparables(d, maintenant):
    """Vrai si aucune séance n'a eu lieu depuis la fiche de clôture : son prix doit alors être
    exactement le dernier cours affiché par les autres sites."""
    from collecte import bourse_fermee
    if d.get("moment") != "cloture":
        return False
    j = datetime.fromisoformat(d["date"]).date() + timedelta(days=1)
    while bourse_fermee(j):
        j += timedelta(days=1)
    ouverture = datetime(j.year, j.month, j.day, 9, 0, tzinfo=PARIS)
    fin = datetime.fromisoformat(d["date"]).replace(hour=17, minute=45, tzinfo=PARIS)
    return fin <= maintenant < ouverture


def c_prix(d, maintenant, n=8):
    import verif
    titre = "Prix revérifiés après coup"
    if not cours_comparables(d, maintenant):
        return controle("prix", titre, "non_verifiable", "une séance a eu lieu depuis la fiche : rien de comparable")
    candidats = [m for m in d["indices"] + d["top30"] if verif.codes(m)[0]]
    ok, ecarts, illisibles = 0, [], []
    for m in random.Random(d["date"]).sample(candidats, min(n, len(candidats))):
        p = verif.boursorama(verif.codes(m)[0])
        if p is None:
            illisibles.append(m["ticker"])
        elif abs(p / m["prix"] - 1) * 100 <= verif.TOL:
            ok += 1
        else:
            ecarts.append(f"{m['ticker']} : {m['prix']} dans la fiche, {p} sur Boursorama")
    lus = ok + len(ecarts)
    if not lus:
        return controle("prix", titre, "non_verifiable", "Boursorama injoignable d'ici", illisibles)
    resume = f"{ok}/{lus} prix identiques sur Boursorama"
    details = ecarts + ([f"illisibles : {', '.join(illisibles)}"] if illisibles else [])
    return controle("prix", titre, "alerte" if ecarts else "ok", resume, details)


def verifier_lien(lib, url, info):
    """(statut, explication) d'un lien de fiche : ok, casse, revoir, non_controle, injoignable."""
    if "morningstar" in url:
        bon = "investmentid=" in url and "format=PDF" in url
        return ("non_controle" if bon else "revoir",
                "DIC : lien bien formé (robots.txt du site interdit de l'ouvrir)" if bon else "DIC : lien mal formé")
    autorise = robots_autorise(url)
    if autorise is None:
        return "injoignable", "site injoignable d'ici"
    if not autorise:
        return "non_controle", "robots.txt interdit de l'ouvrir"
    r = telecharger(url)
    if r is None:
        return "injoignable", "site injoignable d'ici"
    if r.status_code in (404, 410):
        return "casse", f"page introuvable ({r.status_code})"
    if r.status_code != 200:
        return "revoir", f"réponse {r.status_code}"
    isin = info.get("isin")
    if "boursorama" in url:
        code = url.rstrip("/").split("/")[-1].lower()
        if code not in r.url.lower():
            return "casse", "redirigé vers la recherche : code inconnu"
        if isin and isin not in r.text:
            return "revoir", f"la page ne mentionne pas l'ISIN {isin}"
    if "markets.ft.com" in url and url.split("s=")[-1].split("&")[0] not in r.text:
        return "revoir", "la page ne mentionne pas le symbole"
    if "justetf" in url and isin and isin not in r.text:
        return "revoir", f"la page ne mentionne pas l'ISIN {isin}"
    return "ok", "page valide"


def c_liens(d, k=8):
    titre = "Liens des fiches détaillées"
    det = d.get("details", {})
    titres = sorted(t for t in det if not t.startswith("^") and "=X" not in t)
    if not titres:
        return controle("liens", titre, "non_verifiable", "aucune fiche détaillée")
    etf = {m["ticker"] for m in d["top30"] + d["petites"] if m.get("categorie") == "etf"}
    rng = random.Random(d["date"])
    choix = rng.sample(sorted(etf & set(titres)), min(k // 2, len(etf & set(titres))))
    reste = [t for t in titres if t not in choix]
    choix += rng.sample(reste, min(k - len(choix), len(reste)))
    compte, details = {}, []
    for t in choix:
        for lib, url in (det[t].get("liens") or {}).items():
            statut, pourquoi = verifier_lien(lib, url, det[t].get("infos") or {})
            compte[statut] = compte.get(statut, 0) + 1
            if statut in ("casse", "revoir"):
                details.append(f"{t} · {lib} : {pourquoi} ({url})")
    verifies = compte.get("ok", 0) + compte.get("casse", 0) + compte.get("revoir", 0)
    resume = (f"{compte.get('ok', 0)}/{verifies} liens valides sur {len(choix)} titres"
              + "".join(f", {compte[s]} {lib}" for s, lib in (("non_controle", "non ouverts (robots.txt)"),
                                                               ("injoignable", "injoignables d'ici")) if compte.get(s)))
    if not verifies:
        return controle("liens", titre, "non_verifiable", resume, details)
    return controle("liens", titre, "probleme" if compte.get("casse") else "alerte" if compte.get("revoir") else "ok",
                    resume, details)


def donnees_de_page(html):
    m = re.search(r'<script id="donnees" type="application/json">(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


def c_page_depot(d):
    titre = "Page du dépôt (docs/index.html)"
    p = donnees_de_page(lire(RACINE / "docs" / "index.html"))
    if not p:
        return controle("page", titre, "probleme", "docs/index.html absente ou illisible")
    if (p.get("date"), p.get("moment")) != (d["date"], d.get("moment")):
        return controle("page", titre, "probleme",
                        f"elle montre la fiche du {p.get('date')} ({p.get('moment')}), pas celle du {d['date']} ({d.get('moment')})")
    return controle("page", titre, "ok", f"régénérée avec la fiche du {d['date']} ({d.get('moment')})")


def c_site(d):
    titre = "Site en ligne"
    cfg = json.loads(lire(RACINE / "config.json") or "{}")
    url = cfg.get("url_site", "")
    r = telecharger(f"{url}?v={int(time.time())}") if url else None
    if r is None:
        return controle("site", titre, "non_verifiable", f"{urlparse(url).netloc or 'site'} injoignable d'ici (réseau du cloud ?)")
    if r.status_code != 200:
        return controle("site", titre, "probleme", f"le site répond {r.status_code}")
    p = donnees_de_page(r.text)
    if not p:
        return controle("site", titre, "probleme", "données de la page introuvables")
    if (p.get("date"), p.get("moment")) != (d["date"], d.get("moment")):
        return controle("site", titre, "probleme",
                        f"le site affiche encore la fiche du {p.get('date')} ({p.get('moment')})")
    return controle("site", titre, "ok", f"le site affiche la fiche du {d['date']} ({d.get('moment')})")


# ---------- documentation et mémoire (Obsidian) ----------

def fonctions_publiques(chemin):
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    return [n.name for n in arbre.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]


def manques_documentation(archi, scripts):
    """Scripts et fonctions publiques absents de ARCHITECTURE.md (cités entre `accents graves`)."""
    manques = []
    for p in scripts:
        if p.name not in archi:
            manques.append(f"script non décrit : {p.name}")
        if p.suffix == ".py" and p.name != "tests.py":
            manques += [f"fonction non décrite : {p.stem}.{f}" for f in fonctions_publiques(p)
                        if not re.search(rf"`{re.escape(f)}[`(]", archi)]
    return manques


def c_documentation(d, maintenant):
    titre = "Documentation et mémoire Obsidian"
    al = []
    archi = lire(RACINE / "ARCHITECTURE.md")
    scripts = sorted(p for p in (RACINE / "scripts").glob("*") if p.suffix in (".py", ".html"))
    al += ["ARCHITECTURE.md absent"] if not archi else manques_documentation(archi, scripts)
    for f in sorted((DATA / "jours").glob("20*.json")):
        for attendu in (f"notes/{f.stem}.md", f"docs/archives/{f.stem}.html", f"data/analyses/{f.stem}.md"):
            if not (RACINE / attendu).exists():
                al.append(f"{attendu} manquant")
    readme = lire(RACINE / "apprentissage" / "README.md")
    journaux = sorted((RACINE / "apprentissage" / "journal").glob("20*.md"))
    al += [f"journal {j.stem} absent de la liste de apprentissage/README.md" for j in journaux
           if f"journal/{j.stem}.md" not in readme]
    if journaux:
        dernier = lire(journaux[-1])
        al += [f"journal {journaux[-1].stem} : partie « {t} » absente" for t in
               ("Veille du jour", "Ce que j'ai appris", "À retenir", "Amélioration") if f"# {t}" not in dernier]
        if (maintenant.date() - datetime.fromisoformat(journaux[-1].stem).date()).days > 1:
            al.append(f"aucun journal de nuit depuis le {journaux[-1].stem}")
    textes = [lire(p) for p in (RACINE / "apprentissage" / "connaissances").glob("*.md") if p.name != "README.md"]
    attente, douteux = sum(t.count("⏳") for t in textes), sum(t.count("❔") for t in textes)
    infos = ([f"{attente} connaissance(s) en attente de vérification (⏳)"] if attente else []) + \
            ([f"{douteux} connaissance(s) non vérifiable(s) (❔)"] if douteux else [])
    return controle("documentation", titre, "alerte" if al else "ok",
                    f"{len(al)} manque(s)" if al else "tout est documenté et rangé", al + infos)


# ---------- travail des agents (Git) ----------

def agent_du_commit(message):
    if re.match(r"Matin PEA \d{4}-\d{2}-\d{2}", message):
        return "fiche"
    if re.match(r"(Amélioration|Veille) :", message):
        return "nuit"
    if message.startswith("Chef :"):
        return "chef"
    if message.startswith("Univers :"):
        return "univers"
    if message.startswith("Revert"):
        return "annulation"
    return "autre"


def ecarts_aux_regles(agent, fichiers, jour_commit, dernier_jour):
    """fichiers : [(statut Git, chemin, lignes modifiées)]. Renvoie (problèmes, alertes)."""
    pb, al = [], []
    for statut, chemin, _ in fichiers:
        if any(fnmatch(chemin, motif) for motif in HORS_ROLE.get(agent, [])) and chemin not in PERMIS.get(agent, []) \
                and not any(fnmatch(chemin, m) for m in PERMIS_MOTIFS.get(agent, [])):
            al.append(f"{chemin} : hors du rôle de l'agent « {agent} »")
        m = re.match(r"data/(jours|analyses)/(\d{4}-\d{2}-\d{2})\.", chemin)
        if m and m.group(2) < jour_commit and agent != "autre":
            pb.append(f"{chemin} : donnée d'un jour passé modifiée")
        m = re.match(r"(docs/archives|notes)/(\d{4}-\d{2}-\d{2})\.", chemin)
        if m and m.group(2) < dernier_jour and agent in ("nuit", "chef"):
            al.append(f"{chemin} : fiche d'un jour passé régénérée")
        if statut.startswith("D") and agent in HORS_ROLE and not chemin.startswith("data/fiches/"):
            (pb if chemin.startswith(("scripts/", "data/")) else al).append(f"{chemin} : fichier supprimé")
    code = sum(n for _, chemin, n in fichiers if chemin.startswith("scripts/"))
    if agent in MAX_LIGNES and code > MAX_LIGNES[agent]:
        al.append(f"{code} lignes de code modifiées (au plus {MAX_LIGNES[agent]})")
    chemins = {c for _, c, _ in fichiers}
    if agent == "nuit" and any(c.startswith("scripts/") for c in chemins) and "apprentissage/CHANGELOG.md" not in chemins:
        al.append("amélioration du code sans entrée dans apprentissage/CHANGELOG.md")
    return pb, al


def git(*args):
    return subprocess.run(["git", "-C", str(RACINE), *args], capture_output=True, text=True, timeout=60).stdout


def c_agents(d, heures=30):
    titre = "Travail des agents (30 dernières heures)"
    journal = git("log", f"--since={heures} hours ago", "--format=%H%x1f%aI%x1f%s")
    pb, al, vus = [], [], []
    for ligne in filter(None, journal.splitlines()):
        sha, quand, message = ligne.split("\x1f", 2)
        agent = agent_du_commit(message)
        statuts = dict(reversed(l.split("\t", 1)) for l in git("show", "--name-status", "--format=", sha).splitlines() if "\t" in l)
        fichiers = []
        for l in git("show", "--numstat", "--format=", sha).splitlines():
            a, s, chemin = (l.split("\t") + ["", "", ""])[:3]
            n = (int(a) if a.isdigit() else 0) + (int(s) if s.isdigit() else 0)
            fichiers.append((statuts.get(chemin, "M"), chemin, n))
        jour = str(datetime.fromisoformat(quand).astimezone(PARIS).date())
        p, a = ecarts_aux_regles(agent, fichiers, jour, d["date"])
        pb += [f"{sha[:7]} « {message[:50]} » : {x}" for x in p]
        al += [f"{sha[:7]} « {message[:50]} » : {x}" for x in a]
        vus.append(f"{sha[:7]} [{agent}] {message[:70]}")
    niveau = "probleme" if pb else "alerte" if al else "ok"
    resume = f"{len(vus)} commit(s), {len(pb)} problème(s), {len(al)} alerte(s)"
    return controle("agents", titre, niveau, resume, pb + al + vus)


# ---------- assemblage ----------

def resume_court(controles, etat):
    """Phrase affichée en bas de la fiche : « À surveiller. 11/11 tests, 8/8 prix revérifiés… »."""
    c = {x["nom"]: x for x in controles}
    morceaux = [c["tests"]["resume"].replace(" réussis", "")]
    if c.get("prix", {}).get("niveau") in ("ok", "alerte"):
        morceaux.append(c["prix"]["resume"].split(" prix")[0] + " prix revérifiés")
    if c.get("liens", {}).get("niveau") in ("ok", "alerte", "probleme"):
        morceaux.append(c["liens"]["resume"].split(" sur ")[0])
    if c.get("site", {}).get("niveau") == "ok":
        morceaux.append("site à jour")
    soucis = [x["titre"][0].lower() + x["titre"][1:] for x in controles if x["niveau"] in ("alerte", "probleme")]
    tete = {"vert": "Tout est en ordre", "orange": "À surveiller", "rouge": "À corriger"}[etat]
    return f"{tete}. " + ", ".join(morceaux) + "." + (f" Points à voir : {', '.join(soucis)}." if soucis else "")


def main():
    hors_ligne = "--hors-ligne" in sys.argv
    maintenant = datetime.now(PARIS)
    jours = sorted((DATA / "jours").glob("20*.json"))
    d = json.loads(jours[-1].read_text(encoding="utf-8"))
    controles = [c_tests(), c_fraicheur(d, maintenant), c_donnees(d), c_analyse(d), c_page_depot(d)]
    if hors_ligne:
        ancien = json.loads(lire(ETAT) or "{}")
        meme_jour = ancien.get("genere_le", "")[:10] == str(maintenant.date())
        for nom in RESEAU:
            x = next((c for c in ancien.get("controles", []) if c["nom"] == nom), None) if meme_jour else None
            controles.append(x or controle(nom, nom, "non_verifiable", "non vérifié (hors ligne)"))
    else:
        controles += [c_prix(d, maintenant), c_liens(d), c_site(d)]
    controles += [c_documentation(d, maintenant), c_agents(d)]
    pire_niveau = pire(c["niveau"] for c in controles)
    etat = {"probleme": "rouge", "alerte": "orange"}.get(pire_niveau, "vert")
    sortie = {"genere_le": maintenant.isoformat(timespec="minutes"), "fiche": f"{d['date']} ({d.get('moment')})",
              "lieu": "cloud" if str(RACINE).startswith("/home/") else "local", "etat": etat,
              "resume": resume_court(controles, etat), "controles": controles}
    ETAT.parent.mkdir(exist_ok=True)
    ETAT.write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"# Contrôle du {maintenant:%d/%m/%Y à %H h %M} · {COULEUR[etat]} {etat}\n\n{sortie['resume']}\n")
    print("| Contrôle | État | Résumé |\n|---|:-:|---|")
    for c in controles:
        print(f"| {c['titre']} | {EMOJI[c['niveau']]} | {c['resume']} |")
    for c in controles:
        if c["details"]:
            print(f"\n## {EMOJI[c['niveau']]} {c['titre']}\n" + "\n".join(f"- {x}" for x in c["details"]))
    sys.exit({"vert": 0, "orange": 1, "rouge": 2}[etat])


if __name__ == "__main__":
    main()
