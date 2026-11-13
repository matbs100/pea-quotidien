# Leçons de l'agent design (sa mémoire)

Une leçon par ligne, datée, 60 lignes au plus. Relue chaque nuit avant de travailler.

## Ce que le propriétaire veut
- 2026-11-13 · Plus clair, plus simple, plus attirant, **sans jamais retirer d'information** (voir `pilotage/design/souhaits.md`).

## Ce qui a marché
- 2026-11-13 · Glisser pour fermer : touch-action none sur poignée et en-tête, overscroll-behavior contain sur le corps (à confirmer par le chef).

## Ce qui a été annulé, et pourquoi

## Erreurs à ne plus refaire
- 2026-11-13 · Ne jamais charger une police, une image ou un script depuis un autre site : la politique de sécurité de la page (CSP) le bloque et `design.py` le signale 🔴.
