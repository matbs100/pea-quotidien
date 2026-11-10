#!/bin/bash
# Matin PEA sur le Mac, en un double-clic (lancé par « Matin PEA.command »).
# Prépare Python tout seul, puis propose : fiche du jour, Obsidian, contrôle, publication.
# Compatible avec le bash 3.2 de macOS. Information et apprentissage : pas un conseil en investissement.

set -u
cd "$(dirname "$0")/.." || exit 1
RACINE=$(pwd)
REGLAGES="$RACINE/.matin-pea-local"   # réglages propres à ce Mac (non publiés)
VENV="$RACINE/.venv"
PY="$VENV/bin/python"

vert()  { printf '\033[32m%s\033[0m\n' "$*"; }
jaune() { printf '\033[33m%s\033[0m\n' "$*"; }
rouge() { printf '\033[31m%s\033[0m\n' "$*"; }
titre() { printf '\n\033[1m▶ %s\033[0m\n' "$*"; }
pause() { printf '\nAppuie sur Entrée pour fermer… '; read -r _; }

JOUR=$(TZ=Europe/Paris date +%F)
HEURE=$(TZ=Europe/Paris date +%H)
if [ "$HEURE" -lt 13 ]; then MOMENT=ouverture; else MOMENT=cloture; fi

# ---------- 1. Python ----------
preparer_python() {
  titre "Préparation de Python"
  if ! command -v python3 >/dev/null 2>&1; then
    rouge "Python 3 est introuvable."
    echo "Installe-le avec : xcode-select --install   (ou depuis https://www.python.org/downloads/)"
    pause; exit 1
  fi
  if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then
    rouge "Python 3.9 ou plus récent est nécessaire (trouvé : $(python3 --version 2>&1))."
    pause; exit 1
  fi
  if [ ! -x "$PY" ]; then
    echo "Création de l'environnement .venv (une seule fois)…"
    python3 -m venv "$VENV" || { rouge "Impossible de créer .venv"; pause; exit 1; }
  fi
  local empreinte ancienne
  empreinte=$(shasum -a 256 requirements.txt | cut -d' ' -f1)
  ancienne=$(cat "$VENV/.empreinte" 2>/dev/null || true)
  if [ "$empreinte" != "$ancienne" ]; then
    echo "Installation des bibliothèques (yfinance, pandas…), 1 à 2 minutes la première fois…"
    "$PY" -m pip install -q --upgrade pip >/dev/null 2>&1
    if "$PY" -m pip install -q -r requirements.txt; then
      echo "$empreinte" > "$VENV/.empreinte"
    else
      rouge "L'installation a échoué : vérifie la connexion Internet, puis relance."
      pause; exit 1
    fi
  fi
  vert "Python prêt ($("$PY" --version 2>&1))."
}

# ---------- 2. Dernière version du dépôt ----------
mettre_a_jour() {
  titre "Récupération de la dernière version (agents du cloud)"
  if [ ! -d .git ]; then jaune "Pas un dépôt Git : étape sautée."; return; fi
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    jaune "Des fichiers ont été modifiés sur ce Mac : je ne récupère rien pour ne rien écraser."
    git status --short --untracked-files=no | head -10
    return
  fi
  if git pull --ff-only -q origin claude/pea; then vert "À jour."; else jaune "Mise à jour impossible (hors ligne ?). Je continue avec la version locale."; fi
}

# ---------- 3. Fiche du jour ----------
fiche_du_jour() {
  titre "Fiche du $JOUR ($MOMENT)"
  echo "Collecte des cours (peut attendre que Yahoo publie la séance, jusqu'à 30 min)…"
  local code essai
  for essai in 1 2; do
    "$PY" scripts/collecte.py "$JOUR" "$MOMENT"; code=$?
    [ "$code" -ne 3 ] && break
    [ "$essai" -eq 1 ] && { jaune "Cours pas encore disponibles : nouvel essai dans 2 minutes…"; sleep 120; }
  done
  case "$code" in
    0) vert "Collecte terminée." ;;
    4) jaune "Bourse fermée aujourd'hui (week-end ou jour férié) : j'ouvre la dernière fiche."; return 4 ;;
    *) rouge "Collecte échouée (code $code). Fiche non générée."; return 1 ;;
  esac

  echo; echo "Contrôle des prix (Yahoo / Boursorama / Financial Times)…"
  "$PY" scripts/verif.py "$JOUR" || jaune "Contrôle des prix incomplet (non bloquant)."
  echo; echo "Fiches détaillées (2 à 3 minutes)…"
  "$PY" scripts/fiches.py "$JOUR" || jaune "Fiches détaillées incomplètes (non bloquant)."
  echo; echo "Rendu de la fiche et de la note Obsidian…"
  if "$PY" scripts/rendu.py "$JOUR"; then vert "Fiche prête : docs/index.html"; else rouge "Rendu échoué."; return 1; fi
  if [ ! -f "data/analyses/$JOUR.md" ]; then
    jaune "Pas d'analyse écrite pour aujourd'hui : c'est l'agent du cloud qui la rédige (17 h 55)."
  fi
  FICHE_FAITE=1
}

ouvrir_fiche() {
  if [ -f docs/index.html ]; then open docs/index.html; else jaune "Aucune fiche trouvée dans docs/."; fi
}

# ---------- 4. Obsidian ----------
coffre_obsidian() {
  local coffre=""
  [ -f "$REGLAGES" ] && coffre=$(sed -n 's/^OBSIDIAN=//p' "$REGLAGES")
  if [ -z "$coffre" ] || [ ! -d "$coffre" ]; then
    # Coffres connus d'Obsidian, s'il en a déjà ouvert sur ce Mac
    local liste="$HOME/Library/Application Support/obsidian/obsidian.json"
    if [ -f "$liste" ]; then
      echo "Coffres Obsidian trouvés sur ce Mac :" >&2
      python3 -c 'import json,sys; [print(" -", v["path"]) for v in json.load(open(sys.argv[1]))["vaults"].values()]' "$liste" >&2 2>/dev/null
    fi
    printf "Chemin du coffre Obsidian (tu peux glisser le dossier ici) : " >&2
    read -r coffre
    coffre=$(printf '%s' "$coffre" | sed "s/^[\"']//; s/[\"']$//; s/\\\\ / /g; s/[[:space:]]*$//")
    if [ ! -d "$coffre" ]; then rouge "Dossier introuvable : $coffre" >&2; return 1; fi
    grep -v '^OBSIDIAN=' "$REGLAGES" 2>/dev/null > "$REGLAGES.tmp"; echo "OBSIDIAN=$coffre" >> "$REGLAGES.tmp"; mv "$REGLAGES.tmp" "$REGLAGES"
  fi
  printf '%s' "$coffre"
}

coffre_englobant() {  # coffre Obsidian qui contient déjà le projet (dossier .obsidian au-dessus)
  local d="$RACINE"
  while [ "$d" != "/" ]; do
    [ -d "$d/.obsidian" ] && { printf '%s' "$d"; return 0; }
    d=$(dirname "$d")
  done
  return 1
}

vers_obsidian() {
  titre "Copie dans Obsidian"
  local coffre cible englobant
  # Le projet est déjà dans le coffre (synchronisé par git pull) : une copie ferait des doublons.
  if englobant=$(coffre_englobant); then
    vert "Déjà dans ton coffre Obsidian ($(basename "$englobant")) : tout y est, aucune copie (pas de doublon)."
    return 0
  fi
  coffre=$(coffre_obsidian) || return 1
  cible="$coffre/Matin PEA"
  mkdir -p "$cible/Fiches" "$cible/Guide" "$cible/Apprentissage"
  # Copie sans rien supprimer dans le coffre ; les doublons macOS « … 2.md » sont ignorés.
  copier() {
    if command -v rsync >/dev/null 2>&1; then rsync -a --exclude '* 2.md' "$1/" "$2/"; else cp -R "$1/." "$2/"; fi
  }
  copier notes "$cible/Fiches" && copier guide "$cible/Guide" && \
    { [ ! -d apprentissage ] || copier apprentissage "$cible/Apprentissage"; } && \
    cp mes-investissements.md ARCHITECTURE.md "$cible/" || { rouge "La copie a échoué."; return 1; }
  vert "Copié dans : $cible"
  echo "  Fiches : $(ls "$cible/Fiches" | wc -l | tr -d ' ') notes · Guide : $(ls "$cible/Guide" | wc -l | tr -d ' ') notes"
}

# ---------- 5. Contrôle ----------
controle() {
  titre "Contrôle du projet et tests"
  "$PY" scripts/controle.py || jaune "Le contrôle signale des points (détail ci-dessus et dans pilotage/etat.json)."
  "$PY" scripts/tests.py && vert "Tests réussis." || rouge "Des tests échouent : ne publie pas avant correction."
}

# ---------- 6. Publication ----------
publier() {
  [ "${FICHE_FAITE:-0}" = 1 ] || return
  printf '\nPublier la fiche sur le site (GitHub) ? [o/N] '; read -r rep
  case "$rep" in o|O|oui|Oui) ;; *) echo "Non publiée (elle reste sur ce Mac)."; return ;; esac
  git add docs notes data descriptions.json 2>/dev/null
  if git diff --cached --quiet; then jaune "Rien de nouveau à publier."; return; fi
  git commit -q -m "Propriétaire : fiche du $JOUR ($MOMENT) depuis le Mac" && \
    git push -q origin HEAD:claude/pea && vert "Publiée : $(sed -n 's/.*"url_site": *"\([^"]*\)".*/\1/p' config.json)" || \
    rouge "Publication impossible (connexion GitHub ?). Le commit est gardé : relance « git push origin HEAD:claude/pea »."
}

# ---------- Menu ----------
preparer_python
mettre_a_jour
cat <<EOF

=========  Matin PEA · $JOUR · $MOMENT  =========
  1) Tout : fiche du jour + Obsidian + contrôle   (Entrée)
  2) Fiche du jour seulement
  3) Ouvrir la dernière fiche
  4) Copier les notes dans Obsidian
  5) Contrôle du projet et tests
  q) Quitter
EOF
printf 'Ton choix : '; read -r choix
FICHE_FAITE=0
case "${choix:-1}" in
  1) fiche_du_jour; ouvrir_fiche; vers_obsidian; controle; publier ;;
  2) fiche_du_jour; ouvrir_fiche; publier ;;
  3) ouvrir_fiche ;;
  4) vers_obsidian ;;
  5) controle ;;
  q|Q) exit 0 ;;
  *) jaune "Choix inconnu." ;;
esac
vert "Terminé."
pause
