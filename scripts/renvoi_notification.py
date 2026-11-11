"""Renvoie la notification que ntfy.sh a refusée au cloud : par GitHub Actions dès que la fiche la dépose
(`.github/workflows/renvoi-notification.yml`), ou depuis le Mac (relais, 9 h 40 et 18 h 40).

ntfy.sh compte son quota gratuit par adresse Internet ; les machines du cloud partagent la leur avec
beaucoup d'utilisateurs, d'où des refus « daily message quota reached » (429). La fiche du cloud laisse
alors le message dans `pilotage/notification.json` (jamais le sujet ntfy, qui ne va pas dans ce dépôt
public) ; ce script le renvoie une seule fois depuis la connexion du propriétaire.

Usage : python3 scripts/renvoi_notification.py <sujet ntfy>
Affiche une ligne de résultat. Code de sortie : 0 renvoyée ou rien à faire, 1 échec.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "pilotage" / "notification.json"
LOCAL = RACINE / ".matin-pea-local"   # ignoré par Git : garde la trace du dernier renvoi
CLE = "NTFY_RENVOYEE="


def deja_renvoyee():
    """« date moment » de la dernière notification renvoyée depuis ce Mac, ou ""."""
    if not LOCAL.exists():
        return ""
    return next((l[len(CLE):].strip() for l in LOCAL.read_text(encoding="utf-8").splitlines() if l.startswith(CLE)), "")


def a_renvoyer(notif, aujourd_hui, deja):
    """Vrai si la notification est du jour, complète et pas encore renvoyée."""
    if not notif or notif.get("date") != aujourd_hui or not notif.get("message"):
        return False
    return f"{notif['date']} {notif.get('moment', '')}" != deja


def noter_renvoi(notif):
    lignes = [l for l in (LOCAL.read_text(encoding="utf-8").splitlines() if LOCAL.exists() else []) if not l.startswith(CLE)]
    lignes.append(f"{CLE}{notif['date']} {notif.get('moment', '')}")
    LOCAL.write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main(args):
    if len(args) != 1:
        print("Usage : renvoi_notification.py <sujet ntfy>")
        return 1
    try:
        notif = json.loads(FICHIER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        notif = None
    aujourd_hui = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    if not a_renvoyer(notif, aujourd_hui, deja_renvoyee()):
        print("Rien à renvoyer.")
        return 0
    import requests
    url_site = json.loads((RACINE / "config.json").read_text(encoding="utf-8")).get("url_site", "")
    entetes = {"Title": notif.get("titre", "Matin PEA").encode("utf-8"), "Tags": "chart_with_upwards_trend",
               "Click": url_site}
    try:
        r = requests.post(f"https://ntfy.sh/{args[0]}", data=notif["message"].encode("utf-8"), headers=entetes, timeout=30)
    except requests.RequestException as e:
        print(f"Échec du renvoi : {type(e).__name__}")
        return 1
    if r.status_code != 200:
        print(f"Échec du renvoi : ntfy a répondu {r.status_code}")
        return 1
    noter_renvoi(notif)
    quand = {"ouverture": "d'ouverture", "cloture": "de clôture"}.get(notif.get("moment"), "du jour")
    depuis = "GitHub" if os.environ.get("GITHUB_ACTIONS") else "le Mac"
    print(f"📲 Notification {quand} renvoyée depuis {depuis} (ntfy l'avait refusée au cloud).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
