#!/bin/zsh
# Récupère les fiches publiées par l'agent cloud pour qu'elles apparaissent dans Obsidian.
cd "$(dirname "$0")/.." || exit 1
git pull --ff-only --quiet origin claude/pea >> /tmp/matin-pea-synchro.log 2>&1
