"""Construit la fiche animée (docs/) et la note Obsidian (notes/) du jour.

Usage : python scripts/rendu.py AAAA-MM-JJ
Lit data/jours/AAAA-MM-JJ.json et, s'il existe, data/analyses/AAAA-MM-JJ.md (texte de Claude).
"""
import html
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA, DOCS, NOTES = RACINE / "data", RACINE / "docs", RACINE / "notes"
CONFIG = json.loads((RACINE / "config.json").read_text(encoding="utf-8"))


def md_en_html(md):
    out, liste = [], False
    for brut in md.strip().splitlines():
        l = html.escape(brut.strip())
        l = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", l)
        l = re.sub(r"(?<!\*)\*(?!\s)(.+?)\*", r"<em>\1</em>", l)
        if l.startswith(("- ", "* ")):
            if not liste:
                out.append("<ul>")
                liste = True
            out.append(f"<li>{l[2:]}</li>")
            continue
        if liste:
            out.append("</ul>")
            liste = False
        if not l:
            continue
        if l.startswith("#"):
            out.append(f"<h3>{l.lstrip('#').strip()}</h3>")
        else:
            out.append(f"<p>{l}</p>")
    if liste:
        out.append("</ul>")
    return "\n".join(out)


def pct(x):
    return "—" if x is None else f"{x:+.2f} %".replace(".", ",")


def prix(x):
    if x is None:
        return "—"
    d = 0 if x >= 1000 else 2 if x >= 10 else 3 if x >= 1 else 4
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def pct_simple(x):
    return "—" if x is None else f"{x:.1f} %".replace(".", ",")


def eur(x, signe=False):
    """Montant en euros à la française : « 1 234,56 € » (« +12,30 € » avec signe)."""
    if x is None:
        return "—"
    return f"{x:{'+' if signe else ''},.2f} €".replace(",", " ").replace(".", ",")


VERIF = {"ok": "✅", "ecart": "⚠️", "seul": "·", None: ""}


def note_obsidian(d, analyse, url):
    j = d["date"]
    L = ["---", f"date: {j}", f"moment: {d.get('moment', '')}", "tags: [finance, pea, pea-quotidien]", "---", "",
         f"# Matin PEA — {j}", ""]
    MOMENTS = {"ouverture": "⏱ Premiers cours de la séance (ouverture, données décalées d'environ 15 min)",
               "cloture": "🔔 Cours de clôture de la séance"}
    if d.get("moment") in MOMENTS:
        L += [f"> {MOMENTS[d['moment']]}", ""]
    if url:
        L += [f"[Ouvrir la fiche animée]({url}archives/{j}.html)", ""]
    nv = d.get("nouveaute")
    if nv and nv["date"] >= j[:8] + "01" and nv["date"] <= j:
        L += [f"> 🛠 Nouveau ({nv['date']}) : {nv['titre']} — voir [[apprentissage/CHANGELOG|les nouveautés]]", ""]
    cc = d.get("controle_chef")
    if cc and cc.get("etat"):
        pastille = {"vert": "🟢", "orange": "🟠", "rouge": "🔴"}.get(cc["etat"], "⚪")
        L += [f"> {pastille} Contrôle qualité du {cc['genere_le'][:16].replace('T', ' à ')} : {cc['resume']} "
              f"— voir [[pilotage/README|le pilotage]]", ""]
    L += ["> [!warning] Information et apprentissage, pas un conseil en investissement. "
          "Vérifier l'éligibilité PEA auprès de la banque.", ""]
    L += note_investissements(d.get("mes_investissements"))
    L += ["## Marchés", "", "| Indice | Clôture | 1 jour | 1 mois | Sources |", "|---|---:|---:|---:|:-:|"]
    L += [f"| {m['nom']} | {prix(m['prix'])} | {pct(m['var_1j'])} | {pct(m['var_1m'])} | {VERIF[m.get('verif')]} |"
          for m in d["indices"]]
    L += ["", "## Devises et matières premières", "", "| | Cours | 1 jour | 1 mois |", "|---|---:|---:|---:|"]
    L += [f"| {m['nom']} | {prix(m['prix'])} | {pct(m['var_1j'])} | {pct(m['var_1m'])} |"
          for m in d["devises"] + d["matieres"]]
    L += ["", "## Analyse du jour", "", analyse.strip() or "_Pas d'analyse ce jour._", ""]
    L += note_suggestions(d.get("suggestions", []))
    L += ["## Top 30 éligible PEA", "",
          "| # | Titre | Type | Prix | 1 j | 1 mois | 3 mois | RSI | Signal | Score | Sources |",
          "|--:|---|---|--:|--:|--:|--:|--:|---|--:|:-:|"]
    typ = {"etf": "ETF", "actions": "Action", "petites": "Petite cap."}
    for i, m in enumerate(d["top30"], 1):
        L.append(f"| {i} | {m['nom']} (`{m['ticker']}`) | {typ[m['categorie']]} | {prix(m['prix'])} | "
                 f"{pct(m['var_1j'])} | {pct(m['var_1m'])} | {pct(m['var_3m'])} | {m['rsi']:.0f} | "
                 f"{m['signal']} | {m['score']:.0f} | {VERIF[m.get('verif')]} |")
    L += ["", "## 10 petits prix (moins de 2 €)", "",
          "> [!caution] Sociétés souvent fragiles et très volatiles : risque de perte élevé.", "",
          "| # | Titre | Prix | 1 mois | 3 mois | Liquidité €/j | Signal | Déjà vu |",
          "|--:|---|--:|--:|--:|--:|---|:-:|"]
    for i, m in enumerate(d["petites"], 1):
        L.append(f"| {i} | {m['nom']} (`{m['ticker']}`) | {prix(m['prix'])} | {pct(m['var_1m'])} | "
                 f"{pct(m['var_3m'])} | {m['liquidite']:,} | {m['signal']} | {'oui' if m.get('deja_vu') else ''} |"
                 .replace(",", " "))
    b, c = d["bilan_signaux"], d.get("controle_sources")
    L += ["", "## Fiabilité", ""]
    if b["jugees"]:
        L.append(f"- Signaux justes : **{b['taux']} %** ({b['justes']}/{b['jugees']}) — repère "
                 f"(titres montés sur 5 séances) : {b['repere_hausse']} %")
    else:
        L.append("- Signaux : premiers résultats dans 5 séances.")
    if c:
        L.append(f"- Prix contrôlés (Yahoo / Boursorama / FT) : {c['ok']} concordants, "
                 f"{c['ecart']} écarts, {c['seul']} sans 2e source.")
        for e in c["ecarts"]:
            L.append(f"  - ⚠️ {e['nom']} : " + " / ".join(f"{k} {prix(v)}" for k, v in e["sources"].items()))
    det = d.get("details", {})
    if det:
        L += ["", "## Fiches détaillées", "",
              "> PEA : éligibilité indiquée par Boursorama pour cette place de cotation (à confirmer auprès de BNP Paribas). "
              "SRI : risque de 1 à 7, officiel (DIC) pour les ETF, estimé à partir de la volatilité pour les actions.", "",
              "| Titre | ISIN | PEA | Risque | Frais gestion | PER | Rendement | Volatilité 1 an | Pire baisse 1 an |",
              "|---|---|:-:|:-:|--:|--:|--:|--:|--:|"]
        vu = set()
        for m in d["top30"] + d["petites"]:
            x = det.get(m["ticker"])
            if not x or m["ticker"] in vu:
                continue
            vu.add(m["ticker"])
            i, st = x["infos"], x["stats"]
            pea = {True: "✅", False: "⚠️ non indiqué", None: "?"}[i.get("pea_bourso")]
            sri = f"{i['sri_officiel']}/7 (DIC)" if i.get("sri_officiel") else (
                f"{st['sri_estime']}/7 (estimé)" if st.get("sri_estime") else "—")
            L.append(f"| {m['nom']} (`{m['ticker']}`) | {i.get('isin', '—')} | {pea} | {sri} | "
                     f"{i.get('frais_gestion', '—')} | {i.get('per', '—')} | {i.get('rendement', '—')} | "
                     f"{pct_simple(st.get('vol_1a'))} | {pct_simple(st.get('perte_max_1a'))} |")
    L += ["", "## Règles", ""] + [f"- **{k}** : {v}" for k, v in d["regles"].items()]
    return "\n".join(L) + "\n"


def note_investissements(mes):
    """Partie « Mes investissements » de la note Obsidian : total, une ligne par titre, codes à corriger."""
    mes = mes or {}
    lignes, erreurs, t = mes.get("lignes", []), mes.get("erreurs", []), mes.get("total")
    L = ["## Mes investissements", ""]
    if not lignes and not erreurs:
        return L + ["_Aucun investissement noté : remplis [[mes-investissements]] (une ligne par achat)._", ""]
    if t:
        L += [f"- Valeur : **{eur(t['valeur'])}** pour {eur(t['investi'])} investis, soit "
              f"**{eur(t['plus_value'], True)}** ({pct(t['perf'])}) ; sur la séance : "
              f"{eur(t['var_jour_eur'], True)} ({pct(t['var_jour'])})"
              + ("" if t["complet"] else " ; sans les titres dont la quantité n'est pas notée"), ""]
    if lignes:
        L += ["| Titre | Prix | Séance | Prix d'achat | Depuis l'achat | Valeur | Plus-value | Sources |",
              "|---|--:|--:|--:|--:|--:|--:|:-:|"]
        L += [f"| {m['nom']} (`{m['ticker']}`) | {prix(m.get('prix'))} | {pct(m.get('var_1j'))} | "
              f"{prix(m.get('prix_revient'))} | {pct(m.get('perf_achat'))} | {eur(m.get('valeur'))} | "
              f"{eur(m.get('plus_value'), True)} | {VERIF.get(m.get('verif'), '')} |" for m in lignes]
        L.append("")
    L += [f"- ⚠️ `{e['ticker']}` : {e['message']}" for e in erreurs]
    return L + ["", "Frais de courtage non compris. Pour ajouter un achat : [[mes-investissements]].", ""]


def note_suggestions(sugg):
    """Partie « Suggestions du jour » de la note Obsidian (rien s'il n'y en a pas)."""
    if not sugg:
        return []
    L = ["## Suggestions du jour", "",
         "> [!note] Des actions à regarder de plus près, choisies par des règles chiffrées (voir « Règles ») : "
         "pas une liste d'achats.", ""]
    L += [f"- **{s['nom']}** (`{s['ticker']}`, {prix(s.get('prix'))}, {pct(s.get('var_1j'))}) · "
          f"*{s['critere_lib']}* : {s['raison']}" for s in sugg]
    return L + [""]


def archives():
    fiches = sorted((DOCS / "archives").glob("20*.html"), reverse=True)
    items = "\n".join(f'<li><a href="{f.name}">{f.stem}</a></li>' for f in fiches)
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Archives Matin PEA</title>
<style>:root{{--bg:#f4f2ec;--ink:#1a1d1b;--a:#17795a}}@media (prefers-color-scheme:dark){{:root{{--bg:#0d1412;--ink:#e8efe9;--a:#5fd0a3}}}}
body{{background:var(--bg);color:var(--ink);font:16px/1.7 system-ui,sans-serif;max-width:640px;margin:0 auto;padding:32px 16px}}
a{{color:var(--a)}}ul{{list-style:none;padding:0}}li{{font-family:ui-monospace,Menlo,monospace}}</style></head>
<body><h1>Archives Matin PEA</h1><p><a href="../">← Fiche du jour</a></p><ul>{items}</ul></body></html>"""


def risque_de(det):
    """Niveau de risque (1 à 7) d'un titre pour le badge de la page principale : SRI officiel du DIC,
    sinon SRI estimé. Renvoie (niveau, officiel) ou None si on ne sait pas."""
    if not det:
        return None
    off = (det.get("infos") or {}).get("sri_officiel")
    est = (det.get("stats") or {}).get("sri_estime")
    for niv, officiel in ((off, True), (est, False)):
        if isinstance(niv, int) and 1 <= niv <= 7:
            return niv, officiel
    return None


def main():
    jour = sys.argv[1]
    d = json.loads((DATA / "jours" / f"{jour}.json").read_text(encoding="utf-8"))
    fa = DATA / "analyses" / f"{jour}.md"
    analyse = fa.read_text(encoding="utf-8") if fa.exists() else ""
    d["analyse_html"] = md_en_html(analyse) if analyse else ""
    sugg, mes = d.get("suggestions", []), (d.get("mes_investissements") or {}).get("lignes", [])
    for m in d["indices"] + d["devises"] + d["matieres"] + d["top30"] + d["petites"] + sugg + mes:
        m["courbe"] = (m.get("courbe") or [])[-60:]
    fc = RACINE / "apprentissage" / "CHANGELOG.md"
    if fc.exists():
        n = re.search(r"^## (\d{4}-\d{2}-\d{2}) · (.+)$", fc.read_text(encoding="utf-8"), re.M)
        if n:
            d["nouveaute"] = {"date": n.group(1), "titre": n.group(2).strip()}
    d["url_depot"] = CONFIG.get("url_depot", "")
    fe = RACINE / "pilotage" / "etat.json"
    if fe.exists():
        e = json.loads(fe.read_text(encoding="utf-8"))
        d["controle_chef"] = {k: e.get(k, "") for k in ("genere_le", "etat", "resume")}
    fd = RACINE / "descriptions.json"
    textes = json.loads(fd.read_text(encoding="utf-8")).get("titres", {}) if fd.exists() else {}
    for m in d["top30"] + d["petites"] + sugg + mes:
        r = risque_de(d.get("details", {}).get(m["ticker"]))
        if r:
            m["risque"], m["risque_officiel"] = r
    for t, x in d.get("details", {}).items():
        x["description"] = textes.get(t) or x.get("description_auto", "")

    modele = (RACINE / "scripts" / "modele.html").read_text(encoding="utf-8")
    donnees = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = modele.replace("/*__DONNEES__*/", donnees)
    (DOCS / "archives").mkdir(parents=True, exist_ok=True)
    (DOCS / "archives" / f"{jour}.html").write_text(page.replace('href="archives/"', 'href="./"'), encoding="utf-8")
    dernier = max(p.stem for p in (DATA / "jours").glob("20*.json"))
    if jour == dernier:
        (DOCS / "index.html").write_text(page, encoding="utf-8")
    (DOCS / "archives" / "index.html").write_text(archives(), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    NOTES.mkdir(exist_ok=True)
    (NOTES / f"{jour}.md").write_text(note_obsidian(d, analyse, CONFIG.get("url_site", "")), encoding="utf-8")
    print("Fiche :", DOCS / "index.html", "| Note :", NOTES / f"{jour}.md")


if __name__ == "__main__":
    main()
