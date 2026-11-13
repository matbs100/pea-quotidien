# Souhaits du propriétaire pour le design de la page

Recopiés ici (sans aucune information personnelle) par la fonction mémoire quand le propriétaire parle du
projet avec Claude. Lus chaque nuit par l'agent design (`DESIGN.md`, étape 1). Le plus récent en haut.

## Tâches demandées par le propriétaire (à faire en premier, dans l'ordre)

- [ ] 2026-11-13 · **Glisser vers le bas pour fermer une fiche sur téléphone** (action, ETF, fonds, indice…).
  Aujourd'hui, seule la croix ✕ ferme la fiche. À faire dans `scripts/modele.html` (fenêtre `#feuille`,
  fonction `fermer()`) : suivre le doigt (`touchstart` / `touchmove` / `touchend`, `{passive: true}`), la
  fiche descend avec le doigt, se ferme au-delà d'un seuil (environ 120 px ou un geste rapide) et revient en
  place sinon ; seulement quand le contenu de la fiche est déjà tout en haut (`scrollTop === 0`), pour ne pas
  gêner le défilement ni les graphiques ; une petite poignée visible en haut de la fiche ; la croix, la touche
  Échap et le bouton retour restent ; animation coupée si `prefers-reduced-motion`. Indicateur : sur
  téléphone, un glissement vers le bas depuis le haut de la fiche la ferme, sans fermeture par erreur pendant
  le défilement. Quand c'est fait : cocher la case avec la date et la décision `[D-…]`.

## Souhaits (le plus récent en haut)

- 2026-11-13 · **Graphiques** : regarder chaque nuit s'ils sont bien faits, bien écrits (titre, axes,
  unités, légende, dates), visibles (taille, contraste, téléphone), et s'il faut en ajouter (ou en retirer
  un inutile, en gardant son information ailleurs). Critère « Graphiques » de la grille de `DESIGN.md`.
- 2026-11-13 · La page doit devenir **plus compréhensible et plus simple d'utilisation, sans supprimer
  d'information**, et **plus attirante**. Faire une « étude de marché » de ce qui existe : sites sur GitHub,
  sites originaux (exemple cité : Ciao Energie), sites faits par d'autres utilisateurs de Claude, Shopify,
  vidéos YouTube et TikTok, X, Reddit. Le chef vérifie que rien n'est supprimé et que la page n'est pas pire
  qu'avant. L'agent doit s'améliorer de jour en jour, comme les autres.
