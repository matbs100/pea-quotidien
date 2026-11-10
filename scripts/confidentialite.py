"""Contrôle de confidentialité du dépôt public et du site (agent « Vérificateur du code », chaque jour).

Le dépôt et le site sont publics : aucune information personnelle du propriétaire ne doit y apparaître
(prénom, nom, adresse e-mail, identifiants, chemins de son Mac, sujet de notification, montants…).
Ce script cherche, sans rien modifier :
- les **termes protégés** : jamais écrits en clair dans le dépôt, seulement leur empreinte HMAC-SHA256
  (`pilotage/confidentialite.json`). La clé secrète vient de la variable `CONF_CLE` (routine du
  vérificateur) ou de la ligne `CONF_CLE=` de `.matin-pea-local` (Mac, non publié) ;
- les **motifs génériques** : adresse e-mail (sauf adresses techniques autorisées), dossier personnel
  (`/Users/…`, `/home/…`), téléphone, IBAN, clé d'API ou jeton, sujet ntfy ;
- les **auteurs et messages des commits** (adresse personnelle, termes protégés) ;
- les **doublons** « … 2.md » créés par la synchronisation ;
- avec `--site`, la page en ligne.
Le rapport ne recopie **jamais** l'information trouvée : seulement le fichier, la ligne et la catégorie.

Usage : python3 scripts/confidentialite.py [--site] [--commits N] [--json]
        python3 scripts/confidentialite.py --empreinte "terme"   (empreinte d'un nouveau terme, avec la clé)
Codes de sortie : 0 rien trouvé, 1 points à revoir (🟠), 2 information personnelle trouvée (🔴).
"""
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGLES = RACINE / "pilotage" / "confidentialite.json"
LOCAL = RACINE / ".matin-pea-local"
TAILLE_MAX = 8 * 1024 * 1024
ROUGE, ORANGE = "rouge", "orange"

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
DOSSIER_PERSO = re.compile(r"(?<![\w.-])(?:/Users|/home)/([A-Za-z0-9._-]+)")  # pas « site.com/home/… »
TELEPHONE = re.compile(r"(?<![\d.,])(?:\+33\s?|0)[1-9](?:[ .-]\d{2}){4}(?![\d.,])")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){4,7}(?: ?[A-Z0-9]{1,3})?\b")
SECRET = re.compile(r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-ant-[A-Za-z0-9_-]{20,}|"
                    r"sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})")
NTFY = re.compile(r"ntfy\.sh/([A-Za-z0-9_-]{6,})")
DOUBLON = re.compile(r" \d\.(?:md|json|html|csv|py|txt)$")
MOT = re.compile(r"[\w.+@-]+")


def regles(chemin=REGLES):
    """Empreintes des termes protégés et exceptions (adresses techniques, dossiers génériques)."""
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"empreintes": [], "emails_autorises": [], "dossiers_autorises": []}


def cle():
    """Clé secrète (octets) : variable CONF_CLE, sinon .matin-pea-local ; None si absente."""
    valeur = os.environ.get("CONF_CLE", "").strip()
    if not valeur and LOCAL.exists():
        for ligne in LOCAL.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("CONF_CLE="):
                valeur = ligne.split("=", 1)[1].strip()
    return valeur.encode() if valeur else None


def normalise(mot):
    """Minuscules, sans accents ni ponctuation de bord : « Élodie, » → « elodie »."""
    t = unicodedata.normalize("NFKD", mot.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).strip("._-+@")


def empreinte(terme, k):
    return hmac.new(k, normalise(terme).encode(), hashlib.sha256).hexdigest()


def mots(texte):
    """Mots candidats d'un texte : formes entières (adresse, identifiant) et morceaux alphanumériques."""
    vus = set()
    for brut in MOT.findall(texte):
        vus.add(normalise(brut))
        vus.update(normalise(x) for x in re.split(r"[^\w]+|_", brut))
    vus.discard("")
    return vus


def email_autorise(adresse, autorises):
    a = adresse.lower()
    return any(re.fullmatch(motif, a) for motif in autorises)


def iban_valide(texte):
    """Vrai si le texte est un IBAN dont la clé (modulo 97) est juste : évite les faux positifs."""
    s = texte.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    chiffres = "".join(str(int(c, 36)) for c in s[4:] + s[:4])
    return int(chiffres) % 97 == 1


def analyser_texte(texte, k, empreintes, conf):
    """Liste de (n° de ligne, catégorie, gravité) ; ne renvoie jamais la valeur trouvée."""
    trouves = []
    if k and empreintes:
        caches = {m for m in mots(texte) if empreinte(m, k) in empreintes}
        if caches:
            for n, ligne in enumerate(texte.splitlines(), 1):
                if mots(ligne) & caches:
                    trouves.append((n, "terme protégé (identité du propriétaire)", ROUGE))
    autorises = conf.get("emails_autorises", [])
    dossiers_ok = {d.lower() for d in conf.get("dossiers_autorises", [])}
    for n, ligne in enumerate(texte.splitlines(), 1):
        if any(not email_autorise(a, autorises) for a in EMAIL.findall(ligne)):
            trouves.append((n, "adresse e-mail", ORANGE))
        if any(d.lower() not in dossiers_ok for d in DOSSIER_PERSO.findall(ligne)):
            trouves.append((n, "chemin d'un dossier personnel", ROUGE))
        if TELEPHONE.search(ligne):
            trouves.append((n, "numéro de téléphone", ORANGE))
        if any(iban_valide(x) for x in IBAN.findall(ligne)):
            trouves.append((n, "IBAN", ROUGE))
        if SECRET.search(ligne):
            trouves.append((n, "clé d'API ou jeton", ROUGE))
        if NTFY.search(ligne):
            trouves.append((n, "sujet de notification ntfy", ROUGE))
    return trouves


def fichiers_suivis():
    sortie = subprocess.run(["git", "-C", str(RACINE), "ls-files", "-z"], capture_output=True, text=True).stdout
    return [f for f in sortie.split("\0") if f]


def lire_texte(chemin):
    """Texte d'un fichier, None s'il est binaire ou trop gros."""
    try:
        if chemin.stat().st_size > TAILLE_MAX:
            return None
        octets = chemin.read_bytes()
    except OSError:
        return None
    if b"\0" in octets[:8192]:
        return None
    return octets.decode("utf-8", errors="replace")


def doublons(fichiers):
    """Fichiers « nom 2.md » dont l'original existe : copies créées par la synchronisation."""
    ensemble = set(fichiers)
    return [f for f in fichiers if DOUBLON.search(f) and re.sub(r" \d(\.\w+)$", r"\1", f) in ensemble]


def analyser_depot(k, conf):
    empreintes = set(conf.get("empreintes", []))
    points = []
    fichiers = fichiers_suivis()
    for f in fichiers:
        texte = lire_texte(RACINE / f)
        if texte is None:
            continue
        points += [(f, n, cat, g) for n, cat, g in analyser_texte(texte, k, empreintes, conf)]
    points += [(f, 0, "doublon créé par la synchronisation", ORANGE) for f in doublons(fichiers)]
    return points


def analyser_commits(k, conf, n=50):
    """Auteurs et messages des n derniers commits (0 = tout l'historique)."""
    empreintes = set(conf.get("empreintes", []))
    args = ["git", "-C", str(RACINE), "log", "--format=%h%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e"]
    if n:
        args.insert(4, f"-{n}")
    sortie = subprocess.run(args, capture_output=True, text=True).stdout
    noms_ok = {x.lower() for x in conf.get("auteurs_autorises", [])}
    points = []
    for bloc in filter(str.strip, sortie.split("\x1e")):
        sha, an, ae, cn, ce, message = (bloc.strip("\n").split("\x1f") + [""] * 6)[:6]
        for nom, mail in ((an, ae), (cn, ce)):
            if not email_autorise(mail, conf.get("emails_autorises", [])):
                points.append((f"commit {sha}", 0, "adresse e-mail personnelle de l'auteur", ROUGE))
            elif noms_ok and nom.lower() not in noms_ok:
                points.append((f"commit {sha}", 0, "nom d'auteur inconnu", ORANGE))
            if k and empreintes and any(empreinte(m, k) in empreintes for m in mots(nom)):
                points.append((f"commit {sha}", 0, "terme protégé dans le nom de l'auteur", ROUGE))
        points += [(f"commit {sha}", n2, cat, g) for n2, cat, g in analyser_texte(message, k, empreintes, conf)]
    return list(dict.fromkeys(points))


def analyser_site(k, conf):
    try:
        url = json.loads((RACINE / "config.json").read_text(encoding="utf-8")).get("url_site", "")
        req = urllib.request.Request(url, headers={"User-Agent": "MatinPEA-confidentialite/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            texte = r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001  site injoignable : signalé, pas bloquant
        return [("site en ligne", 0, f"non vérifié ({type(e).__name__})", ORANGE)]
    return [("site en ligne", n, cat, g) for n, cat, g in analyser_texte(texte, k, set(conf.get("empreintes", [])), conf)]


def gravite(points):
    if any(g == ROUGE for *_, g in points):
        return 2
    return 1 if points else 0


def rapport(points, k):
    lignes = ["# 🔒 Confidentialité", ""]
    if not k:
        lignes.append("⚪ Termes protégés non vérifiés ici (clé absente) : seulement les motifs génériques.")
    if not points:
        lignes.append("✅ Aucune information personnelle trouvée.")
    for lieu, n, cat, g in points:
        lignes.append(f"- {'🔴' if g == ROUGE else '🟠'} {lieu}{f' (ligne {n})' if n else ''} : {cat}")
    return "\n".join(lignes)


def main(args):
    if "--empreinte" in args:
        k = cle()
        if not k:
            sys.exit("Clé absente : CONF_CLE ou .matin-pea-local")
        print(empreinte(args[args.index("--empreinte") + 1], k))
        return 0
    conf, k = regles(), cle()
    n = int(args[args.index("--commits") + 1]) if "--commits" in args else 50
    points = analyser_depot(k, conf) + analyser_commits(k, conf, n)
    if "--site" in args:
        points += analyser_site(k, conf)
    if "--json" in args:
        print(json.dumps({"code": gravite(points), "cle": bool(k),
                          "points": [{"lieu": l, "ligne": n2, "categorie": c, "gravite": g} for l, n2, c, g in points]},
                         ensure_ascii=False, indent=1))
    else:
        print(rapport(points, k))
    return gravite(points)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
