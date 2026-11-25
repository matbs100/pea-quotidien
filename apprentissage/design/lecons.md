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

- 2026-11-20 · Pastille Risque : toucher = fiche (D-20261120-1) ; une bulle au survol n'a pas d'équivalent tactile (NN/g). Reste à mesurer sa cible (24 px, WCAG 2.5.8).

- 2026-11-21 · Phrase-résumé du marché en tête (D-20261121-1) : une phrase calculée depuis les données déjà affichées ne retire rien et règle la compréhension en 5 s.

- 2026-11-22 · Bandeau « Nouveau » : nettoyer le titre à l'affichage en JS (D-20261122-1) ; ne pas oublier l'étude de marché, reportée deux nuits.

- 2026-11-24 · Pastille Risque ≥ 24 px (D-20261124-1) : min-height + inline-flex suffit ; mesurer toutes les pastilles à 320/390 px. Devoirs restants : fiche ETF 360 px, idée 74.
- 2026-11-25 · Encadré vide compact en mobile (D-20261125-1) : réduire padding/taille (≥ 13 px) fait remonter le contenu utile sans rien retirer. Ne pas sauter l'étude de marché : reportée, à faire en premier demain.

## Ce qui a été annulé, et pourquoi

## Erreurs à ne plus refaire
- 2026-11-15 · Ma capture cliquait sur la bulle de risque au lieu d'ouvrir la fiche : ouvrir une fiche par l'adresse #code.
- 2026-11-13 · Ne jamais charger une police, une image ou un script depuis un autre site : la politique de sécurité de la page (CSP) le bloque et `design.py` le signale 🔴.
- 2026-11-14 · Captures : défiler avant de photographier (blocs `.rv`) ; installer Chromium via `python3 -m playwright install chromium`.
- 2026-11-18 · Tester un glissement tactile avec Input.dispatchTouchEvent par petits pas (synthesizeScrollGesture ne défile pas en headless) ; pas de WebKit ici : un bug iOS reste à confirmer par le propriétaire.
- 2026-11-21 · Installer playwright==1.63.0 avant `design.py rendre` ; photographier une fenêtre 390×844 (la page entière fait 24 000 px).
- 2026-11-23 · Mesurer le bord droit de chaque élément contre sa carte (overflow:hidden cache les coupures, scrollWidth ne les voit pas) ; flex-wrap règle sans retirer d'information.
