# Souhaits du propriétaire pour le design de la page

Recopiés ici (sans aucune information personnelle) par la fonction mémoire quand le propriétaire parle du
projet avec Claude. Lus chaque nuit par l'agent design (`DESIGN.md`, étape 1). Le plus récent en haut.

## Cartes des marchés sur grand écran (2026-11-27, soir)

Le propriétaire a signalé, capture à l'appui, que sur grand écran la courbe rouge des cartes des marchés prenait
trop de place (elle passait sur le texte « 1 mois ») et que, dans les cartes du haut, prix et points n'étaient
pas alignés (prix de la part d'ETF du DAX à la ligne). Corrigé pour toutes les largeurs (commit 8a173c8,
D-20261127-7) : courbe sous le texte, « 1 mois » sur sa propre ligne, prix et part d'ETF sur une ligne et
alignés. Préférence : les cartes doivent être propres aussi sur ordinateur, pas seulement sur iPhone. À garder :
tester tout changement de cartes à 390, 1 000 et 1 400 px.

## Audit des failles (2026-11-27, soir)

Le propriétaire a demandé de trouver et corriger les failles de la fiche. Corrigé : le texte des suggestions
renvoie à l'onglet Marchés pour la fiabilité ; « Ajouter à mes investissements » depuis une fiche ouverte dans
un autre onglet ouvre d'abord l'onglet Top 30 ; le seuil des petits prix affiché doit toujours être le seuil
réel de la collecte du jour. À garder : textes cohérents avec les onglets, zones tactiles d'au moins 24 px,
aucun changement qui annule les commits « Propriétaire : » du 27/11.

## Fiche en 7 onglets (2026-11-27, soir)

Le propriétaire a demandé que la fiche soit rangée en 7 onglets sous la bande des indices : Marchés,
Actualité, Top 30, Valeurs connues, Petits prix, OPCVM, Globe. Barre collante en haut qui défile de côté ;
glisser le doigt sur le contenu passe d'un onglet à l'autre. Il veut une expérience fluide et sympa. À la fin
de Marchés : « Les signaux tiennent-ils la route ? » puis « Contrôle des prix » ; dans Top 30, « Mes
investissements » au-dessus des suggestions. Sans rien retirer ni ralentir la page ; glissement sur vrai
iPhone pas encore essayé.

## Actualité, onglets et cartes (2026-11-27)

Le propriétaire a demandé des onglets Actualité · Globe · Petits prix, placés sous la bande des indices et
au-dessus de « Mes investissements » : l'actualité ne va jamais en bas de page. Sur téléphone, dans les cartes
des marchés, le prix et la part d'ETF doivent tenir sur une seule ligne. La fiche détail doit s'ouvrir tout en
haut. Chaque actualité montre clairement si elle est confirmée par deux sources ou non confirmée. Sans rien
retirer et sans ralentir la page ; rendu sur vrai iPhone pas encore essayé.

## Carte du monde (2026-11-23)

Le propriétaire a demandé la carte du monde : globe en bas de la fiche, au-dessus de « Contrôle des prix »
(océans bleus, pays verts, pays des titres suivis en orange). Il doit se tourner au doigt ou à la souris,
se zoomer, et un pays orange ouvre sa fiche (titres du plus au moins performant). Tu peux modifier
`scripts/globe.js` pour l'apparence seulement (couleurs, animations, lisibilité), jamais les règles de
placement (`scripts/globe.py`). Le propriétaire veut une page plus belle sans rien retirer et sans la
ralentir ; le geste sur iPhone n'a pas été essayé sur un vrai appareil.

## Tâches demandées par le propriétaire (à faire en premier, dans l'ordre)

- [x] 2026-11-17 · fait le 2026-11-18 [D-20261118-1] · **Défilement au doigt bloqué sur les lignes (téléphone, iPhone).** Le propriétaire n'arrive
  pas à faire défiler la page quand son doigt glisse sur le nom des titres, au centre de l'écran (lignes du
  Top 30, valeurs connues, etc.) ; il doit glisser sur les bords, à côté des lignes, pour naviguer. C'est
  **prioritaire** : la page doit défiler quel que soit l'endroit où le doigt se pose (lignes, cartes,
  badges, graphiques, fiche détaillée ouverte), un simple toucher ouvrant toujours la fiche.
  1. **Reproduire d'abord** dans Playwright avec un vrai écran tactile (`has_touch=True`, `is_mobile=True`,
     390 × 844, WebKit si disponible, sinon Chromium) : geste de glissement vertical par CDP
     (`Input.dispatchTouchEvent` ou `Input.synthesizeScrollGesture`) partant du centre d'une ligne `.ligne`,
     puis d'un bord ; comparer `scrollY` avant / après. Note le résultat dans ton journal.
  2. **Pistes à vérifier** (dans `scripts/modele.html`) : `body { overflow-x: hidden }` qui fait de `body`
     le conteneur de défilement sur iOS (préférer `overflow-x: clip` sur `html`/`body`, ou sur `main`) ;
     `.clic:active { transform: scale(.985) }` et l'animation d'apparition `.rv` sur les lignes ; `.rsq`
     (`cursor: help`, info-bulle `#bulle-r`) ; `.feuille` reste `display: flex` même fermée (vérifier
     qu'elle et `.voile` ne captent aucun toucher une fois fermées : `visibility: hidden` ou
     `pointer-events: none` hors `.ouvert`) ; les écouteurs `touchstart`/`touchmove` du glisser-pour-fermer
     (doivent rester `passive`) ; `touch-action` sur `.f-tete`, `.f-poignee` et les SVG (`pan-y`).
  3. Corrige la cause trouvée, sans retirer d'information ni casser le glisser-vers-le-bas qui ferme la
     fiche. Ajoute un test (`scripts/tests.py`) qui vérifie qu'un glissement tactile partant du centre d'une
     ligne fait défiler la page.
  Indicateur : dans Playwright tactile, glisser depuis le centre d'une ligne fait défiler autant que depuis
  le bord ; un toucher ouvre toujours la fiche ; `design.py comparer` 🟢. Si la cause n'est pas trouvée,
  ne coche pas : écris dans ton journal ce qui a été essayé, et le chef le reprend.
  Quand c'est fait : cocher la case avec la date et la décision `[D-…]`.
  (18/11, chef) D-20261118-1 corrige 4 causes probables (Chromium tactile : OK) ; iOS non reproduit. Case laissée ouverte jusqu'au retour du propriétaire sur son iPhone.
  (18/11, propriétaire) Confirmé sur iPhone : le défilement marche bien depuis le centre des lignes. Case cochée.

- [x] 2026-11-16 · fait le 2026-11-17 [D-20261117-1] · **Effet « verre dépoli » (style liquid glass) sur les éléments flottants seulement.**
  Le fond animé `.blobs` donne déjà de la couleur à faire transparaître. À faire dans `scripts/modele.html` :
  surface semi-transparente + `backdrop-filter: blur(…) saturate(…)` (avec `-webkit-`), liseré clair d'1 px
  et légère ombre, **seulement** sur ce qui flotte : en-tête et poignée de la fiche détaillée (`.feuille`),
  info-bulle `#bulle-r`. **Ne pas** l'appliquer aux cartes de prix, tableaux ni graphiques (`.card`,
  `.ligne`, SVG) : ils restent opaques. Ne pas créer d'en-tête collant pour l'occasion.
  Précautions : `@supports not (backdrop-filter: blur(1px))` → surface opaque actuelle ;
  `@media (prefers-reduced-transparency: reduce)` → surface opaque ; contrastes ≥ 4,5 dans les deux thèmes
  (test `contrastes_des_deux_themes`) ; flou modéré (≤ 20 px) pour ne pas ralentir un téléphone.
  Passe par la grille de `pilotage/decision.md` : si le gain est < 3 ou si c'est moins lisible sur les
  captures 360 px (clair et sombre, fiche ouverte au-dessus du Top 30), ne le garde pas et explique pourquoi.
  Indicateur : `design.py comparer` 🟢, aucune information retirée, contrastes inchangés ou meilleurs.
  Quand c'est fait (ou écarté) : cocher la case avec la date et la décision `[D-…]`.

- [x] 2026-11-13 · fait le 2026-11-13 [D-20261113-1] · **Glisser vers le bas pour fermer une fiche sur téléphone** (action, ETF, fonds, indice…).
  Aujourd'hui, seule la croix ✕ ferme la fiche. À faire dans `scripts/modele.html` (fenêtre `#feuille`,
  fonction `fermer()`) : suivre le doigt (`touchstart` / `touchmove` / `touchend`, `{passive: true}`), la
  fiche descend avec le doigt, se ferme au-delà d'un seuil (environ 120 px ou un geste rapide) et revient en
  place sinon ; seulement quand le contenu de la fiche est déjà tout en haut (`scrollTop === 0`), pour ne pas
  gêner le défilement ni les graphiques ; une petite poignée visible en haut de la fiche ; la croix, la touche
  Échap et le bouton retour restent ; animation coupée si `prefers-reduced-motion`. Indicateur : sur
  téléphone, un glissement vers le bas depuis le haut de la fiche la ferme, sans fermeture par erreur pendant
  le défilement. Quand c'est fait : cocher la case avec la date et la décision `[D-…]`.

- [x] 2026-11-17 · fait le 2026-11-20 [D-20261120-1] · **Toucher n'importe où sur une ligne ouvre la fiche détaillée** (action, ETF, fonds ; Top 30,
  30 valeurs connues, petites capitalisations, Mes investissements, cartes des marchés). Le propriétaire veut
  pouvoir toucher ou cliquer n'importe où sur le bloc d'un titre (nom, badges, prix, variations, RSI, score,
  signal, espaces vides) pour afficher ses informations. Constat du 17/11 (ordinateur) : tout le bloc ouvre
  déjà la fiche **sauf la pastille « Risque n/7 »** (`.rsq`), qui ouvre une bulle (`#bulle-r`) et bloque
  l'ouverture (`stopPropagation`). À faire dans `scripts/modele.html` : un toucher sur la pastille ouvre la
  fiche ; l'explication du risque n'est pas perdue (elle est reprise dans la fiche, à côté du risque, et
  reste au survol à la souris / au clavier si tu le juges utile). Vérifie aussi « ✓ n sources » (`.vf`) et
  les autres badges. **Sur téléphone (tactile)**, vérifie dans Playwright `has_touch` qu'un toucher sur chaque
  zone ouvre la fiche (lien probable avec la tâche précédente : fais-les ensemble si la cause est commune).
  Ajoute un test (`scripts/tests.py`) qui touche chaque zone d'une ligne et vérifie que la fiche s'ouvre.
  Indicateur : toutes les zones d'une ligne ouvrent la fiche, sur ordinateur et au doigt ; aucune
  information retirée ; `design.py comparer` 🟢. Quand c'est fait : cocher la case avec la date et la
  décision `[D-…]`.

## Souhaits (le plus récent en haut)

- 2026-11-16 · **Trouver un ISIN absent de la fiche** (pour information : **ne le code pas**). Réalisé par
  l'agent de nuit (idée n° 48, consigne du 16/11 dans `pilotage/consignes.md`) : liens « Chercher cet ISIN
  sur Boursorama · justETF · Euronext » quand un ISIN valide n'est pas suivi. Un cours en direct est écarté
  (CSP `connect-src 'self'`, CORS des sites). Toi : la nuit qui suit sa réalisation, regarde seulement le
  rendu de ces liens à 360 px (clair et sombre).

- 2026-11-13 · **Graphiques** : regarder chaque nuit s'ils sont bien faits, bien écrits (titre, axes,
  unités, légende, dates), visibles (taille, contraste, téléphone), et s'il faut en ajouter (ou en retirer
  un inutile, en gardant son information ailleurs). Critère « Graphiques » de la grille de `DESIGN.md`.
- 2026-11-13 · La page doit devenir **plus compréhensible et plus simple d'utilisation, sans supprimer
  d'information**, et **plus attirante**. Faire une « étude de marché » de ce qui existe : sites sur GitHub,
  sites originaux (exemple cité : Ciao Energie), sites faits par d'autres utilisateurs de Claude, Shopify,
  vidéos YouTube et TikTok, X, Reddit. Le chef vérifie que rien n'est supprimé et que la page n'est pas pire
  qu'avant. L'agent doit s'améliorer de jour en jour, comme les autres.
