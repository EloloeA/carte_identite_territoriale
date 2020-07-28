# Projet-CI-territoire
L’idée est de constituer une « carte d’identité » de n’importe quelle commune de Provence-Alpes-Côte d’Azur,
qui permettrait de la valoriser, à travers la disponibilité d’informations essentielles à une perception globale de son territoire.
Une telle carte permettrait également de mettre au même niveau de lisibilité une commune de 50, 1000, 100 000 ou 1 M d’habitants.
Cette carte d’identité pourrait idéalement prendre l’aspect d’un dashboard où, en filtrant par commune, un certain nombre d’éléments 
seraient mis à jour automatiquement. Ces éléments appelés « widgets » pourront être cartographiques (carte pour situer la commune en région
par exemple, carte des hôtels, des campings, etc.), des données affichées (nombre d’habitants, surface en km², densité de population,
contacts de la Mairie, indice de qualité de l’air, etc.) ou calculées (nombre d’hôtels, de campings), ou encore des listes
(musées sur la commune, collections présentes dans ces musées, sites patrimoniaux à visiter, événements culturels à venir, etc.). 
L’intégration en en-tête d’un sélecteur de période (date de début et date de fin), permettant de filtrer certaines listes datées
(événements culturels par exemple) serait un plus.
Le point d’entrée de la carte sera donc le code INSEE de la commune et si possible une période. 
En matière communale, le Code INSEE est une donnée-pivot incontournable. Grâce à elle, tout jeu de donnée la contenant peut être croisé 
avec un autre, filtré, représenté géographiquement, etc. Cette donnée est donc considérée comme essentielle dans le cadre de ce prototype.
