"""Lectures des agents : des PDF de sources vérifiées, une fiche de lecture par document dans Obsidian.

Usage (agent de nuit, chef d'orchestre, vérificateur du code) :
  python scripts/lectures.py telecharger <url>
      vérifie que le lien est sur un site de pilotage/sources-verifiees.md, que son robots.txt le permet,
      qu'il ne redirige pas ailleurs et que c'est bien un PDF (30 Mo au plus), puis l'enregistre dans
      /tmp/lectures/ (jamais dans le dépôt).
  python scripts/lectures.py lire <chemin du PDF> [1-10]
      affiche le texte des pages demandées (10 par défaut, 30 au plus par appel), avec leur numéro,
      pour écrire la fiche ; le texte n'est jamais enregistré.
  python scripts/lectures.py note <url> "<titre>" "<organisme>" [<date de publication>] [nuit|chef|code]
      crée apprentissage/lectures/AAAA-MM-JJ-<titre>.md à remplir (résumé, chiffres clés avec leur page,
      ce que Matin PEA peut en tirer) ; ne remplace jamais une fiche existante.
  python scripts/lectures.py index
      refait apprentissage/lectures/README.md, la bibliothèque (une ligne par lecture, avec ses liens).

Droits d'auteur : le PDF et son texte ne vont jamais dans le dépôt, qui est public. Une fiche contient
seulement le lien, un résumé écrit avec ses propres mots, des chiffres avec leur page et au plus une
courte citation entre guillemets.
"""
import hashlib
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "pilotage" / "sources-verifiees.md"
AGENTS = {"nuit": "de nuit", "chef": "chef d'orchestre", "code": "vérificateur du code"}  # auteur d'une fiche
DOSSIER = RACINE / "apprentissage" / "lectures"
TELECHARGEMENTS = Path("/tmp/lectures")
MAX_MO = 30
MOTS_RESUME = (80, 300)   # un résumé tient en 80 à 300 mots
PARIS = ZoneInfo("Europe/Paris")
CHAMPS = ("titre", "organisme", "url", "lu_le")


# ---------- sources vérifiées ----------

def domaines_verifies(texte=None):
    """Domaines de la table de pilotage/sources-verifiees.md (première colonne, entre accents graves)."""
    if texte is None:
        texte = SOURCES.read_text(encoding="utf-8") if SOURCES.exists() else ""
    return set(re.findall(r"^\|\s*`([a-z0-9.-]+\.[a-z]{2,})`\s*\|", texte, re.M))


def est_verifie(url, domaines):
    """Vrai si le lien est en https sur un domaine exact de la liste (pas un sous-domaine imité)."""
    try:
        u = urlparse(url)
    except ValueError:
        return False
    return u.scheme == "https" and (u.hostname or "") in domaines


def robots_permet(statut, texte, url, agent="*"):
    """Règle de robots.txt : 401 ou 403 = tout est interdit, absent (404…) = tout est permis."""
    if statut in (401, 403):
        return False
    if statut != 200:
        return True
    rp = RobotFileParser()
    rp.parse((texte or "").splitlines())
    return rp.can_fetch(agent, url)


def telecharger(url, domaines=None, dossier=TELECHARGEMENTS, max_mo=MAX_MO):
    """Télécharge un PDF d'une source vérifiée dans un dossier hors du dépôt. Renvoie
    {url, url_finale, chemin, taille_ko, sha256} ou lève ValueError avec la raison du refus."""
    import requests
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from verif import UA
    domaines = domaines_verifies() if domaines is None else domaines
    if not est_verifie(url, domaines):
        raise ValueError("source non vérifiée : le domaine n'est pas dans pilotage/sources-verifiees.md")
    u = urlparse(url)
    r = requests.get(f"https://{u.hostname}/robots.txt", headers=UA, timeout=20)
    if not robots_permet(r.status_code, r.text, url, UA.get("User-Agent", "*")):
        raise ValueError("lecture interdite par le robots.txt du site")
    with requests.get(url, headers=UA, timeout=60, stream=True, allow_redirects=True) as p:
        if p.status_code != 200:
            raise ValueError(f"page indisponible (code {p.status_code})")
        if not est_verifie(p.url, domaines):
            raise ValueError(f"le lien redirige vers un site non vérifié ({urlparse(p.url).hostname})")
        contenu, h = b"", hashlib.sha256()
        for bloc in p.iter_content(65536):
            contenu += bloc
            if len(contenu) > max_mo * 1024 * 1024:
                raise ValueError(f"document trop lourd (plus de {max_mo} Mo)")
    if not contenu.startswith(b"%PDF"):
        raise ValueError("ce n'est pas un PDF")
    h.update(contenu)
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / f"{h.hexdigest()[:12]}.pdf"
    chemin.write_bytes(contenu)
    return {"url": url, "url_finale": p.url, "chemin": str(chemin), "taille_ko": len(contenu) // 1024,
            "sha256": h.hexdigest()}


def pages_demandees(spec, total, maxi=30):
    """« 3-8 » -> [3, …, 8] (numéros de page à partir de 1), bornés au document et à `maxi` pages."""
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", (spec or "1-10").strip())
    if not m:
        raise ValueError("pages : écrire par exemple 1-10")
    debut = max(1, int(m.group(1)))
    fin = min(total, int(m.group(2) or debut), debut + maxi - 1)
    return list(range(debut, fin + 1))


def texte(chemin, spec="1-10"):
    """Texte des pages demandées d'un PDF (pypdf, licence BSD-3-Clause), chaque page précédée de son
    numéro, pour lire le document et citer la page d'un chiffre."""
    from pypdf import PdfReader
    lecteur = PdfReader(str(chemin))
    out = [f"[{len(lecteur.pages)} pages au total]"]
    for p in pages_demandees(spec, len(lecteur.pages)):
        out.append(f"\n===== page {p} =====\n" + (lecteur.pages[p - 1].extract_text() or "(page sans texte)"))
    return "\n".join(out)


# ---------- fiches de lecture ----------

def slug(texte, n=60):
    """« Rapport annuel 2025 : l'épargne » -> « rapport-annuel-2025-l-epargne »."""
    t = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:n].rstrip("-") or "lecture"


def nouvelle_note(url, titre, organisme, publie_le="", auteur="nuit", jour=None, dossier=None):
    """Crée la fiche de lecture à remplir et renvoie son chemin (une fiche existante n'est pas remplacée)."""
    dossier = Path(dossier or DOSSIER)
    jour = jour or datetime.now(PARIS).date().isoformat()
    f = dossier / f"{jour}-{slug(titre)}.md"
    if f.exists():
        return f
    dossier.mkdir(parents=True, exist_ok=True)
    guillemets = lambda x: '"' + str(x).replace('"', "'") + '"'
    f.write_text(f"""---
type: lecture
titre: {guillemets(titre)}
organisme: {guillemets(organisme)}
url: {url}
publie_le: {publie_le}
lu_le: {jour}
lu_par: {auteur}
statut: ⏳ à vérifier
---
# 📄 {titre}

[Lire le PDF]({url}) · {organisme}{f" · publié le {publie_le}" if publie_le else ""} · lu le {jour} par l'agent {AGENTS.get(auteur, "chef d'orchestre")}

## Résumé
(80 à 300 mots, avec tes propres mots : de quoi parle le document, ce qu'il montre, ses limites.)

## Chiffres et faits clés
- (un fait par ligne, avec sa page : « … (p. 12) ») ; chacun va aussi dans apprentissage/connaissances/ avec « ⏳ à vérifier ».

## Ce que Matin PEA peut en tirer
- (idées notées avec la grille de pilotage/decision.md dans apprentissage/idees.md, ou « rien pour la fiche »)

## Vérification du chef
- (le chef relit : le lien ouvre bien ce PDF, le résumé est fidèle, rien n'est copié)
""", encoding="utf-8")
    return f


def _entete(texte):
    m = re.match(r"---\n(.*?)\n---\n", texte, re.S)
    out = {}
    for l in (m.group(1).splitlines() if m else []):
        if ":" in l:
            k, v = l.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def mots_resume(texte):
    """Nombre de mots de la partie « Résumé », sans la consigne entre parenthèses."""
    m = re.search(r"^## Résumé\s*\n(.*?)(?=^## |\Z)", texte, re.S | re.M)
    if not m:
        return 0
    lignes = [l for l in m.group(1).splitlines() if l.strip() and not l.strip().startswith("(")]
    return len(re.findall(r"\w+", " ".join(lignes)))


def lire_notes(dossier=None):
    """Fiches de lecture du dossier (sauf README) : en-tête, nombre de mots du résumé, nom du fichier."""
    dossier = Path(dossier or DOSSIER)
    out = []
    for f in sorted(dossier.glob("20*.md")):
        t = f.read_text(encoding="utf-8")
        x = _entete(t)
        x.update(fichier=f.stem, mots=mots_resume(t))
        out.append(x)
    return out


def index(notes):
    """Contenu de apprentissage/lectures/README.md : la bibliothèque, de la plus récente à la plus ancienne."""
    L = ["---", "tags: [pea, agent, apprentissage, lectures]", "---", "# 📚 Bibliothèque des agents", "",
         "Les PDF lus par les agents pour apprendre, tous sur des [[Finance/PEA Quotidien/pilotage/sources-verifiees|"
         "sources vérifiées]] : une fiche par document, avec le lien, un résumé et ce que Matin PEA peut en tirer.",
         "Ce fichier est refait par `python scripts/lectures.py index`.", "",
         "| Lu le | Fiche de lecture | Organisme | Document | Statut |", "|---|---|---|---|---|"]
    for n in sorted(notes, key=lambda x: (x.get("lu_le", ""), x["fichier"]), reverse=True):
        titre = (n.get("titre") or n["fichier"]).replace("|", "-")
        L.append(f"| {n.get('lu_le', '')} | [[{n['fichier']}\\|{titre}]] | {n.get('organisme', '')} | "
                 f"[PDF]({n.get('url', '')}) | {n.get('statut', '')} |")
    if not notes:
        L.append("| | (aucune lecture pour l'instant) | | | |")
    return "\n".join(L) + "\n"


def ecrire_index(dossier=None):
    dossier = Path(dossier or DOSSIER)
    dossier.mkdir(parents=True, exist_ok=True)
    (dossier / "README.md").write_text(index(lire_notes(dossier)), encoding="utf-8")
    return dossier / "README.md"


def defauts(notes, domaines, texte_index, jour, debut="2026-11-07", jours_sans_lecture=3):
    """Ce que le contrôle signale : champ manquant, lien hors des sources vérifiées, résumé absent ou trop
    long, fiche absente de la bibliothèque, aucune lecture depuis plusieurs jours."""
    al = []
    for n in notes:
        nom = n["fichier"]
        manque = [c for c in CHAMPS if not n.get(c)]
        if manque:
            al.append(f"lecture {nom} : champ(s) manquant(s) : {', '.join(manque)}")
        if n.get("url") and not est_verifie(n["url"], domaines):
            al.append(f"lecture {nom} : lien hors des sources vérifiées")
        if not MOTS_RESUME[0] <= n.get("mots", 0) <= MOTS_RESUME[1]:
            al.append(f"lecture {nom} : résumé de {n.get('mots', 0)} mots (attendu : {MOTS_RESUME[0]} à {MOTS_RESUME[1]})")
        if f"[[{nom}" not in texte_index:
            al.append(f"lecture {nom} : absente de la bibliothèque (lancer lectures.py index)")
    dates = sorted(n.get("lu_le", "") for n in notes)
    j = datetime.fromisoformat(jour).date()
    if (j - datetime.fromisoformat(debut).date()).days >= jours_sans_lecture:
        if not dates or (j - datetime.fromisoformat(dates[-1]).date()).days >= jours_sans_lecture:
            al.append(f"aucune lecture depuis {jours_sans_lecture} jours (agent de nuit : une lecture par nuit)")
    return al


def main(args):
    if args[:1] == ["telecharger"] and len(args) == 2:
        try:
            print(telecharger(args[1]))
        except ValueError as e:
            sys.exit(f"Refusé : {e}")
    elif args[:1] == ["lire"] and len(args) in (2, 3):
        print(texte(args[1], args[2] if len(args) == 3 else "1-10"))
    elif args[:1] == ["note"] and len(args) >= 4:
        print(nouvelle_note(args[1], args[2], args[3], args[4] if len(args) > 4 else "",
                            args[5] if len(args) > 5 else "nuit"))
        print(ecrire_index())
    elif args[:1] == ["index"]:
        print(ecrire_index())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
