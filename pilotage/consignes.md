---
tags: [pea, agent, pilotage]
---
# 📋 Consignes du chef d'orchestre

Lues en premier par l'agent de nuit et par l'agent de la fiche. Mises à jour chaque matin par le chef.

## Priorités pour l'agent de nuit
- (06/11, demande de Mathieu) **Afficher le risque sur la page principale** : un petit badge « Risque 4/7 » (SRI officiel `infos.sri_officiel`, sinon estimé `stats.sri_estime`, avec la mention « estimé ») sur chaque ligne du top 30, des petits prix et des cartes d'ETF, sans avoir à ouvrir la fiche. Couleur selon le niveau, lisible sur téléphone, avec sa définition au toucher. Aujourd'hui le risque n'apparaît que dans la fiche détaillée.
- (06/11) Ouvre au moins 3 sources par nuit et cite-les avec leur lien.
- (06/11) Range chaque connaissance nouvelle dans `apprentissage/connaissances/` avec « ⏳ à vérifier ».
- (06/11) Toute nouvelle fonction a son test dans `scripts/tests.py` et sa ligne dans `ARCHITECTURE.md`.

## Pour la fiche du jour
- (06/11) Analyse : 350 mots au plus (celle du 05/11 en faisait 390).
- (06/11) Si un cours est daté d'un autre jour (ALPHA.AT le 05/11), dis-le dans « À garder en tête ».

## Chantier interface
0. Risque visible sur la page principale (voir priorités de la nuit) : à faire en premier si l'agent de nuit ne l'a pas fait.
1. Contrastes du texte gris (`--muted`) : au moins 4,5:1 en clair et sombre.
2. Sur téléphone : textes des tableaux et fiches d'au moins 14 px.
3. Graphiques : trait pointillé pour les moyennes mobiles (idée n° 18).
4. Bouton clair / sombre manuel (idée n° 14).
5. Graphique utilisable au clavier (idée n° 15).

## Interdits temporaires
- Aucun.
