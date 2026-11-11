"""Résumés pour Obsidian, écrits dans le dépôt par le chef d'orchestre (plus besoin du relais du Mac).

Le coffre Obsidian du propriétaire contient ce dépôt (synchronisé par le plugin Obsidian « Git ») ; ses
notes intègrent ces fichiers avec `![[…]]`, si bien qu'aucune copie n'est à faire sur le Mac :
- `pilotage/obsidian-decisions.md` : les 40 décisions les plus récentes du journal des décisions ;
- `apprentissage/a-retenir.md` : la phrase « À retenir » de chaque journal de nuit (depuis le 11/11/2026),
  sauf si la « Vérification du chef » la marque fausse (❌).

Usage : python3 scripts/obsidian.py      (sans réseau ; n'écrit un fichier que s'il change)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from controle import lire_decisions  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
DECISIONS = RACINE / "pilotage" / "decisions.md"
JOURNAUX = RACINE / "apprentissage" / "journal"
SORTIE_DECISIONS = RACINE / "pilotage" / "obsidian-decisions.md"
SORTIE_RETENIR = RACINE / "apprentissage" / "a-retenir.md"
LIEN = "Finance/PEA Quotidien"          # chemin du dépôt dans le coffre Obsidian
DEBUT_RETENIR = "2026-11-11"            # avant : lignes déjà copiées à la main dans Savoir-faire.md
MAX_DECISIONS = 40


def jj_mm(date):
    """« 2026-11-11 » → « 11/11 » ; renvoie la valeur telle quelle si ce n'est pas une date."""
    m = re.fullmatch(r"\d{4}-(\d{2})-(\d{2})", (date or "").strip())
    return f"{m.group(2)}/{m.group(1)}" if m else (date or "").strip()


def ligne_decision(d):
    """Une décision du journal → une ligne de liste Obsidian."""
    gain = d.get("gain", "").strip() or "—"
    l = f"- **{jj_mm(d.get('date'))}** · `{d['id']}` · {d.get('idée', '').strip()} → {d.get('décision', '').strip()} (gain {gain})"
    if d.get("réalisée", "").strip():
        l += f" ; réalisée le {jj_mm(d['réalisée'])}"
    if d.get("bilan", "").strip():
        l += f" ; bilan : {d['bilan'].strip()}"
    return l


def resume_decisions(texte, nombre=MAX_DECISIONS):
    """Les décisions les plus récentes d'abord (ordre inverse du journal)."""
    decisions = list(lire_decisions(texte).values())[::-1][:nombre]
    entete = ("Décisions des agents, les plus récentes d'abord (généré par `scripts/obsidian.py` depuis "
              f"[[{LIEN}/pilotage/decisions|le journal des décisions]]).\n\n")
    return entete + "\n".join(ligne_decision(d) for d in decisions) + "\n"


def section(texte, titre):
    """Contenu d'une partie « ## titre » d'un journal, sans les lignes vides du bord."""
    m = re.search(rf"^## {re.escape(titre)}\s*\n(.*?)(?=^## |\Z)", texte, re.M | re.S)
    return m.group(1).strip() if m else ""


def a_retenir(texte):
    """La phrase « À retenir » d'un journal, ou "" si absente ou marquée fausse (❌) par le chef."""
    phrase = " ".join(section(texte, "À retenir").split())
    verif = section(texte, "Vérification du chef")
    if any("❌" in l and "retenir" in l.lower() for l in verif.splitlines()):
        return ""
    return phrase


def resume_retenir(journaux, debut=DEBUT_RETENIR):
    """journaux : liste de (date AAAA-MM-JJ, texte) → liste Obsidian, la plus ancienne d'abord."""
    lignes = []
    for jour, texte in sorted(journaux):
        phrase = a_retenir(texte)
        if jour >= debut and phrase:
            lignes.append(f"- **{jj_mm(jour)}** : {phrase} → [[{LIEN}/apprentissage/journal/{jour}|journal]]")
    entete = ("Ce que l'agent de nuit retient, une ligne par nuit (généré par `scripts/obsidian.py` ; "
              "phrases marquées fausses par le chef retirées).\n\n")
    return entete + ("\n".join(lignes) if lignes else "_Rien pour l'instant._") + "\n"


def ecrire_si_change(chemin, contenu):
    """Écrit le fichier seulement s'il change ; vrai s'il a été écrit."""
    if chemin.exists() and chemin.read_text(encoding="utf-8") == contenu:
        return False
    chemin.write_text(contenu, encoding="utf-8")
    return True


def main():
    texte = DECISIONS.read_text(encoding="utf-8") if DECISIONS.exists() else ""
    journaux = [(p.stem, p.read_text(encoding="utf-8")) for p in JOURNAUX.glob("20*.md")]
    for chemin, contenu in ((SORTIE_DECISIONS, resume_decisions(texte)), (SORTIE_RETENIR, resume_retenir(journaux))):
        print(f"{chemin.relative_to(RACINE)} : {'mis à jour' if ecrire_si_change(chemin, contenu) else 'inchangé'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
