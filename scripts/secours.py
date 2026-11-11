"""Fiche de secours, sans Claude : GitHub Actions publie la fiche si l'agent Claude ne l'a pas fait.

Lancé par `.github/workflows/fiche-secours.yml` un peu après chaque passage prévu de l'agent (ouverture et
clôture). Si la fiche de ce moment est déjà publiée, il ne fait rien : tant que l'abonnement Claude tourne,
c'est un filet de sécurité ; sans abonnement, il prend le relais. L'analyse est alors écrite à partir des
chiffres seuls (pas de revue de presse ni d'avis rédigé), avec les sept titres habituels.

Usage :
  python3 scripts/secours.py verifier AAAA-MM-JJ <ouverture|cloture>   code 0 : à faire ; 10 : déjà publiée
  python3 scripts/secours.py analyse AAAA-MM-JJ                       écrit data/analyses/AAAA-MM-JJ.md
  python3 scripts/secours.py notification AAAA-MM-JJ                  affiche le titre puis le message
  python3 scripts/secours.py envoyer AAAA-MM-JJ <sujet> [échec]       envoie la notification par ntfy
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA, NOTES = RACINE / "data", RACINE / "notes"
RANG = {"": -1, "ouverture": 0, "cloture": 1}
NOTIONS = [
    ("Le RSI", "le RSI (indice de force relative) va de 0 à 100 ; au-dessus de 70, la hausse récente est forte "
     "et un repli devient plus probable ; sous 30, c'est l'inverse. Ce n'est pas une prédiction."),
    ("La moyenne à 200 jours", "c'est le prix moyen des 200 dernières séances : un cours au-dessus indique "
     "une tendance de fond plutôt haussière, en dessous plutôt baissière."),
    ("La volatilité", "elle mesure l'ampleur des variations d'un prix : plus elle est forte, plus la valeur "
     "peut monter ou baisser vite, dans les deux sens."),
    ("Les frais d'un ETF", "les frais courants sont prélevés chaque année sur l'encours ; 0,2 % ou 0,5 % "
     "semblent faibles, mais ils s'additionnent sur 10 ou 20 ans."),
    ("La diversification", "répartir son épargne entre beaucoup de sociétés, de secteurs et de pays limite "
     "l'effet d'une mauvaise surprise sur une seule d'entre elles."),
    ("Le VIX", "on l'appelle « indice de la peur » : il mesure la nervosité attendue sur la Bourse américaine ; "
     "il monte souvent quand les marchés baissent."),
    ("L'investissement régulier", "investir la même somme à intervalles réguliers lisse le prix d'achat "
     "moyen et évite de devoir choisir « le bon moment »."),
]


def fr(x, dec=2):
    """Nombre à la française : 8 332,87 ; « — » si absent."""
    if x is None:
        return "—"
    return f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")


def pct(x):
    """Variation signée : +0,66 % ; « — » si absente."""
    return "—" if x is None else ("+" if x >= 0 else "−") + fr(abs(x)) + " %"


def moment_publie(jour):
    """Moment de la fiche déjà publiée pour ce jour (« ouverture », « cloture ») ou ""."""
    note = NOTES / f"{jour}.md"
    if not note.exists():
        return ""
    m = re.search(r"^moment:\s*(\w+)", note.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else ""


def a_faire(moment, publie):
    """Vrai si la fiche de ce moment manque (une clôture remplace une ouverture, jamais l'inverse)."""
    return RANG.get(moment, -1) > RANG.get(publie, -1)


def _par_ticker(d):
    return {x["ticker"]: x for x in d.get("indices", []) + d.get("devises", []) + d.get("matieres", [])}


def _veille(jour):
    """Données du jour de bourse précédent, ou {}."""
    avant = sorted(p for p in (DATA / "jours").glob("20*.json") if p.stem < jour)
    return json.loads(avant[-1].read_text(encoding="utf-8")) if avant else {}


def analyse_auto(d, veille=None):
    """Analyse écrite à partir des chiffres seuls, avec les sept titres attendus par le contrôle."""
    t, cloture = _par_ticker(d), d.get("moment") == "cloture"
    cac, sx5 = t.get("^FCHI", {}), t.get("^STOXX50E", {})
    v = cac.get("var_1j")
    sens = "en hausse" if (v or 0) > 0 else "en baisse" if (v or 0) < 0 else "stable"
    L = ["*Mise à jour à la clôture de la séance.*" if cloture else "*Premiers cours de la séance.*", "",
         "*Analyse automatique, écrite à partir des chiffres seuls (fiche de secours, sans revue de presse).*", ""]
    L += ["### Le marché en une phrase",
          f"Paris {'termine' if cloture else 'ouvre'} {sens} : CAC 40 **{pct(v)}** à {fr(cac.get('prix'), 0)} points, "
          f"Euro Stoxx 50 **{pct(sx5.get('var_1j'))}**.", ""]
    L += ["### Ce que disent les données"]
    if cac.get("rsi") is not None and cac.get("ma200") is not None:
        pos = "au-dessus de" if cac["prix"] >= cac["ma200"] else "sous"
        L.append(f"- CAC 40 : RSI {fr(cac['rsi'], 1)}, {pos} sa moyenne à 200 jours ({fr(cac['ma200'], 0)}).")
    L.append("- Europe : " + ", ".join(f"{n} {pct(t.get(k, {}).get('var_1j'))}" for k, n in
                                      (("^GDAXI", "DAX"), ("^STOXX", "Stoxx 600"), ("^FTSE", "FTSE 100"))) + ".")
    L.append("- Hors Europe : " + ", ".join(f"{n} {pct(t.get(k, {}).get('var_1j'))}" for k, n in
                                           (("^GSPC", "S&P 500"), ("^NDX", "Nasdaq 100"), ("^N225", "Nikkei"))) + ".")
    usd, vix = t.get("EURUSD=X", {}), t.get("^VIX", {})
    L.append(f"- 1 € = {fr(usd.get('prix'), 3)} $ ({pct(usd.get('var_1j'))}) ; VIX {fr(vix.get('prix'), 1)} ({pct(vix.get('var_1j'))}).")
    top = [x for x in d.get("top30", []) if x.get("var_1j") is not None]
    if top:
        hi, lo = max(top, key=lambda x: x["var_1j"]), min(top, key=lambda x: x["var_1j"])
        L.append(f"- Top 30 : meilleure valeur {hi['nom']} ({pct(hi['var_1j'])}), moins bonne {lo['nom']} ({pct(lo['var_1j'])}).")
    L += ["", "### Ce qui a changé"]
    avant = {x["ticker"] for x in (veille or {}).get("top30", [])}
    if avant:
        maint = {x["ticker"]: x["nom"] for x in d.get("top30", [])}
        entrees = [n for k, n in maint.items() if k not in avant]
        sorties = len(avant - set(maint))
        L.append(f"- Top 30 : {len(entrees)} entrée(s)" + (f" ({', '.join(entrees[:5])})" if entrees else "")
                 + f", {sorties} sortie(s) par rapport à la séance précédente.")
    else:
        L.append("- Pas de séance précédente à comparer.")
    b = d.get("bilan_signaux", {})
    L += ["", "### Fiabilité des signaux"]
    if b.get("jugees"):
        L.append(f"{b['justes']} signaux justes sur {b['jugees']} jugés ({fr(100 * b['justes'] / b['jugees'], 0)} %). "
                 "Ce sont des indicateurs techniques, pas des prédictions.")
    else:
        L.append("Aucun signal n'est encore jugé : impossible de dire s'ils font mieux que le hasard.")
    L += ["", "### L'actualité et les estimations",
          "- Pas de revue de presse dans la fiche de secours : elle est rédigée seulement par l'agent Claude.", ""]
    L += ["### À garder en tête"]
    c = d.get("controle_sources", {})
    L.append(f"- Prix contrôlés : {c.get('ok', 0)} concordants, {c.get('ecart', 0)} écart(s), {c.get('seul', 0)} sans 2e source.")
    hors = [x["nom"] for x in d.get("top30", [])
            if d.get("details", {}).get(x["ticker"], {}).get("infos", {}).get("pea_bourso") is False]
    if hors:
        L.append(f"- Non indiqués éligibles au PEA par Boursorama : {', '.join(hors)}.")
    L.append("- Information et apprentissage, pas un conseil en investissement.")
    titre, texte = NOTIONS[int(d.get("date", "2000-01-01").replace("-", "")) % len(NOTIONS)]
    L += ["", "### Pour apprendre", f"**{titre}** : {texte}", ""]
    return "\n".join(L)


def notification(d):
    """(titre, message) de la notification, comme ceux de l'agent Claude."""
    t, jour = _par_ticker(d), d.get("date", "")
    cac, sx5 = t.get("^FCHI", {}), t.get("^STOXX50E", {})
    alerte = any(abs(x.get("var_1j") or 0) > 3 for x in d.get("indices", []) if x.get("ticker") != "^VIX")
    debut = "⚠️ " if alerte else ""
    if d.get("moment") == "cloture":
        top = [x for x in d.get("top30", []) if x.get("var_1j") is not None]
        ligne2 = ""
        if top:
            hi, lo = max(top, key=lambda x: x["var_1j"]), min(top, key=lambda x: x["var_1j"])
            ligne2 = f"\nMeilleure valeur du top 30 : {hi['nom']} {pct(hi['var_1j'])} ; moins bonne : {lo['nom']} {pct(lo['var_1j'])}."
        return (f"Clôture du {jour}",
                f"{debut}CAC 40 {pct(cac.get('var_1j'))} ({fr(cac.get('prix'), 0)}), Euro Stoxx 50 {pct(sx5.get('var_1j'))} sur la séance.{ligne2}\n(fiche de secours, sans Claude)")
    noms = ", ".join(x["nom"] for x in d.get("top30", [])[:3])
    usd = t.get("EURUSD=X", {})
    return (f"Matin PEA du {jour} · ouverture",
            f"{debut}CAC 40 {pct(cac.get('var_1j'))}, Euro Stoxx 50 {pct(sx5.get('var_1j'))} ; 1 € = {fr(usd.get('prix'), 3)} $.\n"
            f"Top 30 : {noms}.\n(fiche de secours, sans Claude)")


def envoyer(titre, message, sujet, url_site):
    """Envoie la notification par ntfy ; renvoie le code HTTP (0 si le réseau échoue)."""
    import requests
    try:
        r = requests.post(f"https://ntfy.sh/{sujet}", data=message.encode("utf-8"), timeout=30,
                          headers={"Title": titre.encode("utf-8"), "Tags": "chart_with_upwards_trend", "Click": url_site})
        return r.status_code
    except requests.RequestException:
        return 0


def main(args):
    if len(args) < 2 or args[0] not in ("verifier", "analyse", "notification", "envoyer"):
        print(__doc__)
        return 2
    action, jour = args[0], args[1]
    if action == "verifier":
        publie = moment_publie(jour)
        faire = a_faire(args[2] if len(args) > 2 else "", publie)
        print(f"Fiche {args[2] if len(args) > 2 else '?'} du {jour} : {'à faire' if faire else 'déjà publiée (' + publie + ')'}")
        return 0 if faire else 10
    if action == "envoyer":
        url = json.loads((RACINE / "config.json").read_text(encoding="utf-8")).get("url_site", "")
        if len(args) > 3:   # échec de la collecte : message d'échec, pas de données du jour
            titre, message = f"Matin PEA du {jour}", f"Fiche non générée : {args[3]} (fiche de secours, sans Claude)"
        else:
            titre, message = notification(json.loads((DATA / "jours" / f"{jour}.json").read_text(encoding="utf-8")))
        code = envoyer(titre, message, args[2], url)
        print(f"ntfy : {code}")
        return 0 if code == 200 else 1
    d = json.loads((DATA / "jours" / f"{jour}.json").read_text(encoding="utf-8"))
    if action == "analyse":
        (DATA / "analyses").mkdir(exist_ok=True)
        (DATA / "analyses" / f"{jour}.md").write_text(analyse_auto(d, _veille(jour)), encoding="utf-8")
        print(f"data/analyses/{jour}.md écrit (analyse automatique)")
    else:
        titre, message = notification(d)
        print(json.dumps({"titre": titre, "message": message}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
