---
tags: [pea, connaissances, design]
---
# 🎨 Design, lisibilité et facilité d'utilisation

- **Contraste du texte** : au moins 4,5:1 entre le texte et le fond pour un texte normal, 3:1 pour un
  grand texte (critère 1.4.3 des WCAG, niveau AA). Source proposée : [W3C, Understanding SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Statut : ✅ vérifié le 2026-11-11 ([source](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), extrait de recherche : 4,5:1 et 3:1 pour le grand texte, soit 18 pt ou 14 pt gras)
- **Ne pas compter sur la couleur seule** : une information portée par la couleur (hausse en vert,
  baisse en rouge) doit aussi l'être par un signe, un texte ou un motif (critère 1.4.1 des WCAG). La
  fiche affiche déjà le signe + ou − devant chaque variation. Source proposée : [W3C, Understanding SC 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Statut : ✅ vérifié le 2026-11-11 ([source](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html), extrait de recherche : l'information ne doit pas passer par la couleur seule, niveau A)
- **Pas d'information seulement au survol** : un téléphone n'a pas de survol ; les définitions et les
  valeurs du graphique doivent aussi s'afficher au toucher. Source : journal de nuit du 2026-11-05
  (guides d'accessibilité des graphiques de Penn State). Statut : ⏳ à vérifier (le 2026-11-06 : sites officiels bloqués par le réseau du cloud)
- **Palette des courbes en mode sombre** : ne pas réutiliser la palette claire ; éclaircir et désaturer le vert et le rouge, viser 6 à 8 couleurs bien distinctes, vérifier chaque couleur contre le fond. Exemple donné : vert hsl(145, 65 %, 55 %), rouge hsl(0, 70 %, 60 %), fond hsl(225, 15 %, 10 %). Source : [ColorArchive, couleurs fintech en mode sombre](https://color-archive.vercel.app/guides/fintech-dark-mode-colors/), lu le 2026-11-12 (guide d'un site de design, pas une norme). Statut : ⏳ à vérifier
- **Lisibilité d'un tableau de bord dense** : contraste élevé texte/fond, en mode sombre un gris très clair sur un fond bleu-noir plutôt que du blanc pur ; concevoir autour de la personne qui lit plutôt que des données disponibles. Source proposée (extrait de recherche du 2026-11-12) : Databricks (blog, version française) et Lazarev (agence). Statut : ⏳ à vérifier
- **Contrastes de la page** : après mesure (formule WCAG de `scripts/design.py`), le thème sombre est à 5,3:1 au minimum ; le clair avait trois couleurs sous 4,5:1 (ambre 3,2, neutre 3,5, vert sur son fond doux 4,47), corrigées le 13/11. Source : [W3C WCAG 2.2, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Statut : ⏳ à vérifier.