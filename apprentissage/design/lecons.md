# Leçons de l'agent design (sa mémoire)

Une leçon par ligne, datée, 60 lignes au plus. Relue chaque nuit avant de travailler.

## Ce que le propriétaire veut
- 2026-11-13 · Plus clair, plus simple, plus attirant, **sans jamais retirer d'information** (voir `pilotage/design/souhaits.md`).

## Ce qui a marché
- 2026-11-13 · Glisser pour fermer : touch-action none sur poignée et en-tête, overscroll-behavior contain sur le corps (à confirmer par le chef).

- 2026-11-14 · Masquer un séparateur « · » en mobile règle l'orphelin sans retirer d'information.

- 2026-11-15 · Mesurer un chevauchement avec getBoundingClientRect à 320/360/390 px ; garder les textes ≥ 12 px (sinon 🟠).

- 2026-11-16 · Une unité (devise) doit figurer près de chaque graphique, pas seulement dans le prix de l'en-tête.
- 2026-11-16 · Captures lisibles : fenêtre 390×844, pas la page entière (18 000 px) ; playwright==1.63.0 avec le Chromium préinstallé.

- 2026-11-17 · Verre dépoli : base opaque, flou ≤ 14 px dans @supports, repli reduced-transparency ; l'effet est discret sans contenu dessous.

## Ce qui a été annulé, et pourquoi

## Erreurs à ne plus refaire
- 2026-11-15 · Ma capture cliquait sur la bulle de risque au lieu d'ouvrir la fiche : ouvrir une fiche par l'adresse #code.
- 2026-11-13 · Ne jamais charger une police, une image ou un script depuis un autre site : la politique de sécurité de la page (CSP) le bloque et `design.py` le signale 🔴.
- 2026-11-14 · Captures : défiler avant de photographier (blocs `.rv`) ; installer Chromium via `python3 -m playwright install chromium`.
