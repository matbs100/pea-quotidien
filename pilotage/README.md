---
tags: [pea, agent, pilotage]
---
# 🧭 Pilotage : le chef d'orchestre

Chaque jour à **5 h (heure de Paris)**, l'agent « Chef d'orchestre » (consigne : `CHEF.md`) vérifie
tout le projet avant la fiche de 9 h 15 :
1. **Contrôles** automatiques (`scripts/controle.py`) : tests, fraîcheur de la fiche, données, analyse,
   prix revérifiés, liens des fiches, site en ligne, documentation, travail des autres agents ;
2. **Revue** des commits des autres agents : il garde, corrige ou annule (`git revert`) ce qui casse ;
3. **Vérification des connaissances** apprises la nuit, avec des sources ouvertes le jour même ;
4. **Une correction ou un embellissement** de l'interface, testé ;
5. **Consignes** pour les autres agents, et **rapport** du jour.

## Où lire
| Fichier | Contenu |
|---|---|
| [Consignes](consignes.md) | ce que le chef demande aux autres agents (lu par eux en premier) |
| [État](etat.json) | le dernier contrôle, affiché en bas de la fiche |
| [Rapports](rapports/) | un rapport par jour : contrôles, revue, faits vérifiés, corrections |
| [Comment c'est construit](../ARCHITECTURE.md) | le programme expliqué fichier par fichier |

## Couleurs de l'état
- 🟢 **vert** : tout est en ordre ;
- 🟠 **orange** : à surveiller (alerte, lien à revoir, documentation incomplète…) ;
- 🔴 **rouge** : à corriger avant la prochaine fiche (test cassé, fiche manquante, donnée fausse).

## Rapports
