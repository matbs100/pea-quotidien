"""Garde-fou de l'agent design : prouver qu'un changement de la page ne retire aucune information
et ne la rend pas moins lisible.

Usage :
  python scripts/design.py inventaire [REF]           inventaire de scripts/modele.html (REF : commit, défaut : fichier)
  python scripts/design.py comparer AVANT [APRES]     informations retirées et mesures entre deux versions
                                                      (APRES : commit, défaut : fichier de travail) ;
                                                      code 0 rien de retiré, 1 à revoir, 2 information retirée
  python scripts/design.py rendre AVANT [APRES] [--jour J] [--dossier D]
                                                      les deux pages avec les mêmes données ; avec Playwright
                                                      (facultatif) : captures téléphone et ordinateur, et
                                                      comparaison des textes et des nombres affichés

Un retrait volontaire (élément déplacé ou renommé) se déclare dans pilotage/design/deplacements.json :
[{"commit": "<7 caractères>", "retire": "titre:Ancien", "nouveau": "titre:Nouveau", "raison": "…"}]
Il n'est accepté que si l'élément « nouveau » existe bien après le changement.
"""
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MODELE = "scripts/modele.html"
DEPLACEMENTS = RACINE / "pilotage" / "design" / "deplacements.json"
# catégories dont un retrait est une information perdue (🔴) ; les autres sont à revoir (🟠)
BLOQUANTES = ("titre", "id", "champ", "avertissement")
AVERTISSEMENTS = re.compile(r"pas (?:un|de) conseil|pas une liste d'achats|à titre (?:informatif|pédagogique)", re.I)


def git(*args):
    return subprocess.run(["git", "-C", str(RACINE), *args], capture_output=True, text=True, timeout=60).stdout


def lire_modele(ref=None):
    if ref:
        return git("show", f"{ref}:{MODELE}")
    return (RACINE / MODELE).read_text(encoding="utf-8")


def texte_visible(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", "\n", fragment)
    return [re.sub(r"\s+", " ", unescape(t)).strip() for t in fragment.split("\n")]


def cles_des_donnees():
    """Noms des champs présents dans les données de la dernière fiche (data/jours)."""
    jours = sorted((RACINE / "data" / "jours").glob("20*.json"))
    cles = set()

    def parcourir(x, profondeur=0):
        if profondeur > 6:
            return
        if isinstance(x, dict):
            for k, v in x.items():
                if re.fullmatch(r"[a-z_][a-z0-9_]{1,40}", k):
                    cles.add(k)
                parcourir(v, profondeur + 1)
        elif isinstance(x, list):
            for v in x[:30]:
                parcourir(v, profondeur + 1)
    if jours:
        parcourir(json.loads(jours[-1].read_text(encoding="utf-8")))
    # champs ajoutés par rendu.py au moment de construire la page
    return cles | {"analyse_html", "nouveaute", "url_depot", "fonds_wealins", "controle_chef", "risque",
                   "risque_officiel", "simulation", "description", "opcvm_verifie_le", "taux_bce"}


def inventaire(modele, cles=None):
    """Ce que la page montre ou lit : titres, identifiants, champs de données, textes, avertissements."""
    cles = cles_des_donnees() if cles is None else cles
    corps = modele.split("<body", 1)[-1]
    titres = set()
    for _, t in re.findall(r"<h([1-4])\b[^>]*>(.*?)</h\1>", modele, re.S):
        t = " ".join(x for x in texte_visible(t) if x)
        if t and "${" not in t:
            titres.add(t)
    titres |= {t for t in re.findall(r"""\bbloc\(\s*["'`]([^"'`$]{2,80})["'`]""", modele)}
    ids = set(re.findall(r'\bid="([A-Za-z][\w-]*)"', modele))
    champs = {k for k in cles if re.search(r"(?:\.%s\b|\[[\"']%s[\"']\]|\b%s\s*[:,})])" % (k, k, k), modele)}
    textes = {t for t in texte_visible(corps) if len(t) >= 3 and not t.startswith(("{", "//", "$"))}
    avertissements = {t for t in textes if AVERTISSEMENTS.search(t)}
    avertissements |= {m.group(0).lower() for m in AVERTISSEMENTS.finditer(modele)}
    return {"titre": sorted(titres), "id": sorted(ids), "champ": sorted(champs),
            "texte": sorted(textes), "avertissement": sorted(avertissements)}


def contraste(c1, c2):
    def lum(c):
        c = c.lstrip("#")
        if len(c) == 3:
            c = "".join(x * 2 for x in c)
        r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
        f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return round((a + 0.05) / (b + 0.05), 2)


def mesures(modele):
    """Indicateurs simples : un changement de design ne doit pas les dégrader."""
    m = {"taille_ko": round(len(modele.encode("utf-8")) / 1024, 1)}
    themes = re.findall(r"--bg:\s*(#[0-9a-fA-F]{3,6});.*?--surface:\s*(#[0-9a-fA-F]{3,6});.*?--ink:\s*(#[0-9a-fA-F]{3,6});"
                        r".*?--muted:\s*(#[0-9a-fA-F]{3,6});.*?--accent:\s*(#[0-9a-fA-F]{3,6});.*?--up:\s*(#[0-9a-fA-F]{3,6});"
                        r".*?--down:\s*(#[0-9a-fA-F]{3,6});", modele, re.S)
    if themes:
        m["contraste_min"] = min(contraste(fg, fond) for bg, surf, ink, muted, acc, up, down in themes
                                 for fond in (bg, surf) for fg in (ink, muted, acc, up, down))
    tailles = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", modele)]
    m["polices_sous_12px"] = sum(1 for t in tailles if t < 12)
    m["boutons_sans_nom"] = len([b for b in re.findall(r"<button\b([^>]*)>\s*</button>", modele)
                                 if "aria-label" not in b])
    m["images_sans_alt"] = len([i for i in re.findall(r"<img\b([^>]*)>", modele) if "alt=" not in i])
    m["sites_externes"] = sorted(set(re.findall(r"""(?:src|href)=["']https://([^/"']+)""", modele)))
    m["sections"] = len(re.findall(r"<section\b", modele))
    return m


def deplacements_acceptes(commit):
    try:
        lignes = json.loads(DEPLACEMENTS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [x for x in lignes if not commit or str(x.get("commit", ""))[:7] == commit[:7]]


def comparer_modeles(avant, apres, commit="", cles=None):
    """Renvoie (niveau, lignes) : niveau 0 rien de retiré, 1 à revoir, 2 information retirée."""
    cles = cles_des_donnees() if cles is None else cles
    ia, ib = inventaire(avant, cles), inventaire(apres, cles)
    tous_apres = {f"{cat}:{v}" for cat, vals in ib.items() for v in vals}
    justifies = {x["retire"]: x for x in deplacements_acceptes(commit) if x.get("nouveau") in tous_apres
                 and len(str(x.get("raison", ""))) >= 10}
    niveau, lignes = 0, []
    for cat in ("titre", "id", "champ", "avertissement", "texte"):
        for v in sorted(set(ia[cat]) - set(ib[cat])):
            cle = f"{cat}:{v}"
            if cle in justifies:
                lignes.append(f"✔ {cle} → {justifies[cle]['nouveau']} ({justifies[cle]['raison'][:80]})")
            elif cat in BLOQUANTES:
                niveau = 2
                lignes.append(f"🔴 {cat} retiré : {v[:90]}")
            else:
                niveau = max(niveau, 1)
                lignes.append(f"🟠 texte retiré ou reformulé : {v[:90]}")
    ma, mb = mesures(avant), mesures(apres)
    if mb.get("contraste_min", 99) < min(4.5, ma.get("contraste_min", 99)):
        niveau = 2
        lignes.append(f"🔴 contraste minimal {ma.get('contraste_min')} → {mb['contraste_min']} (au moins 4,5 : WCAG AA)")
    nouveaux_sites = set(mb["sites_externes"]) - set(ma["sites_externes"])
    if nouveaux_sites:
        niveau = 2
        lignes.append(f"🔴 nouveau site externe chargé par la page : {', '.join(sorted(nouveaux_sites))}")
    for k, lib in (("polices_sous_12px", "textes de moins de 12 px"), ("boutons_sans_nom", "boutons sans nom"),
                   ("images_sans_alt", "images sans texte de remplacement")):
        if mb[k] > ma[k]:
            niveau = max(niveau, 1)
            lignes.append(f"🟠 plus de {lib} : {ma[k]} → {mb[k]}")
    if mb["taille_ko"] > ma["taille_ko"] * 1.25 + 5:
        niveau = max(niveau, 1)
        lignes.append(f"🟠 modèle bien plus lourd : {ma['taille_ko']} → {mb['taille_ko']} Ko")
    if mb["sections"] < ma["sections"]:
        niveau = max(niveau, 1)
        lignes.append(f"🟠 moins de sections : {ma['sections']} → {mb['sections']} (regroupées ? vérifier)")
    lignes.append("Mesures avant → après : " + ", ".join(
        f"{k} {ma.get(k)} → {mb.get(k)}" for k in mb if k != "sites_externes"))
    return niveau, lignes


def rendre(avant, apres, jour=None, dossier="/tmp/design"):
    """Construit les deux pages avec les mêmes données ; avec Playwright, captures et textes affichés."""
    sys.path.insert(0, str(RACINE / "scripts"))
    import rendu
    jour = jour or max(p.stem for p in (RACINE / "data" / "jours").glob("20*.json"))
    d, _ = rendu.donnees_du_jour(jour)
    out = Path(dossier)
    out.mkdir(parents=True, exist_ok=True)
    pages = {}
    for nom, ref in (("avant", avant), ("apres", apres)):
        pages[nom] = out / f"{nom}.html"
        pages[nom].write_text(rendu.page_html(json.loads(json.dumps(d)), lire_modele(ref)), encoding="utf-8")
    lignes = [f"Pages construites avec la fiche du {jour} : {pages['avant']} et {pages['apres']}"]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return 1, lignes + ["🟠 Playwright absent : pas de captures ni de comparaison du texte affiché "
                            "(python3 -m pip install playwright && python3 -m playwright install --with-deps chromium)"]
    textes = {}
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for nom, page_html in pages.items():
            for appareil, (l, h) in (("telephone", (390, 844)), ("ordinateur", (1280, 900))):
                pg = nav.new_page(viewport={"width": l, "height": h})
                pg.goto(page_html.resolve().as_uri())
                pg.wait_for_timeout(1500)
                pg.screenshot(path=str(out / f"{nom}-{appareil}.png"), full_page=True)
                if appareil == "ordinateur":
                    textes[nom] = pg.inner_text("body")
                pg.close()
        nav.close()
    nombres = {k: set(re.findall(r"[+-]?\d[\d  ]*(?:,\d+)?\s?%?", v)) for k, v in textes.items()}
    mots = {k: set(re.findall(r"[A-Za-zÀ-ÿ’']{4,}", v.lower())) for k, v in textes.items()}
    perdus_n = sorted(x.strip() for x in nombres["avant"] - nombres["apres"] if len(x.strip()) > 1)
    perdus_m = sorted(mots["avant"] - mots["apres"])
    niveau = 2 if perdus_n else 1 if perdus_m else 0
    lignes.append(f"Captures : {out}/avant-telephone.png, apres-telephone.png, avant-ordinateur.png, apres-ordinateur.png")
    lignes.append(f"Texte affiché : {len(textes['avant'])} → {len(textes['apres'])} caractères")
    if perdus_n:
        lignes.append(f"🔴 {len(perdus_n)} nombre(s) affiché(s) avant et plus après : {', '.join(perdus_n[:15])}")
    if perdus_m:
        lignes.append(f"🟠 {len(perdus_m)} mot(s) disparu(s) : {', '.join(perdus_m[:25])}")
    return niveau, lignes


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("inventaire", "comparer", "rendre"):
        print(__doc__)
        return 2
    if args[0] == "inventaire":
        inv = inventaire(lire_modele(args[1] if len(args) > 1 else None))
        print(json.dumps({k: len(v) for k, v in inv.items()}, ensure_ascii=False))
        print(json.dumps(inv, ensure_ascii=False, indent=1))
        return 0
    options = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in args if a.startswith("--") and "=" in a}
    refs = [a for a in args[1:] if not a.startswith("--")]
    avant, apres = refs[0], (refs[1] if len(refs) > 1 else None)
    if args[0] == "comparer":
        commit = git("rev-parse", "--short=7", apres).strip() if apres else ""
        niveau, lignes = comparer_modeles(lire_modele(avant), lire_modele(apres), commit)
    else:
        niveau, lignes = rendre(avant, apres, options.get("--jour"), options.get("--dossier", "/tmp/design"))
    print({0: "🟢 Aucune information retirée", 1: "🟠 À revoir", 2: "🔴 Information retirée ou page dégradée"}[niveau])
    print("\n".join(f"- {x}" for x in lignes))
    return niveau


if __name__ == "__main__":
    sys.exit(main())
