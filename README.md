# Projet-CI-territoire

## Description du projet
Le projet est une "Carte d’identité" de n’importe quelle commune de la région SUD (Provence-Alpes-Côte d’Azur).

## Objectif du projet
Une telle carte permet de mettre au même niveau de lisibilité une commune de 50, 1000, 100 000 ou 1 M d’habitants.
Cette carte d'identité territoriale permet de valoriser une perception globale de son territoire. 

Le projet est possible grace aux données Open Source disponibles sur [DATASUD](https://www.datasud.fr/). 
La carte d'identité de la région Sud permet donc également de mettre en avant cette plateforme et de démontrer concrètement l'utilité pour les producteurs de partager leurs données.

## Organisation
La donnée pivot de ce travail est le code INSEE de la commune.
Un sélecteur de période peut aussi être ajouté. 

Cette carte d’identité a été pensée comme un dashboard où, en filtrant par commune, un certain nombre d’éléments 
sont mis à jour automatiquement. 
Ces éléments appelés « widgets » peuvent être cartographiques (carte pour situer la commune en région
par exemple, carte des hôtels, des campings, etc.), des données affichées (nombre d’habitants, surface en km², densité de population,
contacts de la Mairie, indice de qualité de l’air, etc.) ou calculées (nombre d’hôtels, de campings), ou encore des listes
(musées sur la commune, collections présentes dans ces musées, sites patrimoniaux à visiter, événements culturels à venir, etc.). 

Le travail a été effectué par une équipe de 5 étudiants de la Wild Code School de Marseille durant les mois de juin et juillet 2020 sous la direction d'un représentant de la région Sud.
Dash est un framework Python permettant de créer des applications web. Plus d'infos sur [Dash Plotly](https://dash.plotly.com/).

Les fichiers :
- app.py => code Python d'execution du dashboard. 
Attention "Le programme suppose que la base de donnée APIDAE_Final.csv ce trouve dans le dossier data."
- outils.py => module nécessaire à l'execution de app.py et contenant les principales fonctions

data => répertoire des données

assets => contient le code style.css qui est directement lu par le dashboard pour sa mise en page

Un sondage auprès de 160 personnes a été préalablement effectué. Les résultats de ce sondage sont également disponibles dans le dossier SONDAGE.
