"""OPCVM (SICAV et FCP, hors ETF) éligibles au PEA : valeur liquidative du jour et frais.

Usage : python scripts/opcvm.py [AAAA-MM-JJ]   (appelé aussi par collecte.py, jamais bloquant)
La liste, les frais et le risque viennent de opcvm.json (relevés à la main dans les DIC, avec leur source).
La valeur liquidative est lue sur Yahoo Finance (le code ISIN est accepté par yfinance), puis sur le
Financial Times si Yahoo ne répond pas. La dernière valeur connue est gardée dans data/opcvm.json :
sans réseau, la fiche affiche cette valeur avec sa date (jamais une valeur inventée).
Information et apprentissage, pas un conseil en investissement.
"""
import json
import math
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
LISTE = RACINE / "opcvm.json"
CACHE = RACINE / "data" / "opcvm.json"
CHAMPS = ("societe", "zone", "frais_courants", "entree_max", "sortie_max", "surperformance", "sri", "pea_pme")


def liste():
    """Fonds de opcvm.json ([] si le fichier manque ou est illisible)."""
    try:
        return json.loads(LISTE.read_text(encoding="utf-8")).get("fonds", [])
    except (OSError, ValueError):
        return []


def charger_cache():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"vl": {}}


def _r(x, n=2):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), n)


def mesures_serie(s):
    """Valeur, date et variations d'une série de valeurs liquidatives (pandas, index de dates)."""
    s = s.dropna()
    if len(s) == 0:
        return None
    v = float(s.iloc[-1])

    def var(n):
        return _r((v / float(s.iloc[-1 - n]) - 1) * 100) if len(s) > n and float(s.iloc[-1 - n]) else None
    an = s.tail(252)
    return {"prix": _r(v, 2), "date_cours": str(s.index[-1].date()), "var_1j": var(1), "var_1m": var(21),
            "var_3m": var(63), "var_1a": var(252), "haut_1a": _r(an.max()), "bas_1a": _r(an.min()),
            "courbe": [_r(x, 2) for x in s.tail(60).tolist()]}


def lire_yahoo(isin):
    """Mesures lues sur Yahoo Finance (14 mois), ou None."""
    try:
        import yfinance as yf
        h = yf.Ticker(isin).history(period="14mo", interval="1d", auto_adjust=True)
        return mesures_serie(h["Close"]) if h is not None and not h.empty else None
    except Exception as e:  # noqa: BLE001  réseau, ISIN inconnu de Yahoo…
        print("OPCVM : Yahoo illisible pour", isin, ":", e, file=sys.stderr)
        return None


def lire_ft(isin):
    """(valeur, date) lus sur le Financial Times, ou (None, None)."""
    try:
        from verif import ft_date
        return ft_date("funds", f"{isin}:EUR")
    except Exception as e:  # noqa: BLE001
        print("OPCVM : FT illisible pour", isin, ":", e, file=sys.stderr)
        return None, None


def mesure(f, cache, en_ligne=True):
    """Ligne d'un fonds pour la fiche du jour : valeur (la plus récente des sources), frais et risque.
    Sans valeur lue aujourd'hui, la dernière valeur gardée est reprise avec sa date ; sinon prix None."""
    isin = f["isin"]
    m = lire_yahoo(isin) if en_ligne else None
    if en_ligne:
        p, d = lire_ft(isin)
        if p and d and (not m or d > m["date_cours"]):  # le FT a une valeur plus récente : on la prend
            prec = m["prix"] if m else (cache["vl"].get(isin) or {}).get("prix")
            m = {**(m or {}), "prix": p, "date_cours": d,
                 "var_1j": _r((p / prec - 1) * 100) if prec else None, "source_vl": "Financial Times"}
        elif m:
            m["source_vl"] = "Yahoo Finance"
    if m:
        cache["vl"][isin] = {k: m.get(k) for k in ("prix", "date_cours", "var_1j", "source_vl")}
    else:
        m = dict(cache["vl"].get(isin) or {"prix": None, "date_cours": None, "var_1j": None})
    return {"ticker": isin, "isin": isin, "nom": f["nom"], "categorie": "fonds", "source": "opcvm",
            "devise": "EUR", **m, **{k: f.get(k) for k in CHAMPS}, "url_source": f.get("source")}


def mesurer_tout(en_ligne=True):
    """Liste des OPCVM avec leur valeur ; met à jour data/opcvm.json. Jamais d'exception."""
    cache = charger_cache()
    out = []
    for f in liste():
        try:
            out.append(mesure(f, cache, en_ligne))
        except Exception as e:  # noqa: BLE001  un fonds illisible ne bloque jamais les autres
            print("OPCVM illisible :", f.get("isin"), e, file=sys.stderr)
    if en_ligne:
        cache["maj"] = date.today().isoformat()
        try:
            CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        except OSError as e:
            print("data/opcvm.json non écrit :", e, file=sys.stderr)
    return out


if __name__ == "__main__":
    # Ajoute (ou met à jour) la liste « opcvm » dans la fiche d'un jour, sans relancer toute la collecte.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    jour = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    fj = RACINE / "data" / "jours" / f"{jour}.json"
    d = json.loads(fj.read_text(encoding="utf-8"))
    d["opcvm"] = mesurer_tout(en_ligne="--hors-ligne" not in sys.argv)
    fj.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OPCVM : {sum(1 for m in d['opcvm'] if m.get('prix'))}/{len(d['opcvm'])} valeurs pour le {jour}")
