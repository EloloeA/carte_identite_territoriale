# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:19:36 2020

MERGE des datasets
"""

import pandas as pd


####### import des informations sur la POPULATION
df_POP = pd.read_csv(r'C:/Users/scriba/Drive_Go/Wild_Code_School/PROJET_4/Bases SELECTION/populationsuperficie.csv', sep =';')
####### import des informations sur les DEPARTEMENTS
df_DEP = pd.read_csv(r'C:/Users/scriba/Drive_Go/Wild_Code_School/PROJET_4/Bases SELECTION/departement_INSEE.csv')
####### import des informations sur les PARCS NATURELS REGIONAUX
df_PNR = pd.read_csv(r'C:\Users\scriba\Drive_Go\Wild_Code_School\PROJET_4\Bases SELECTION\EPCI_densitePop_ParcNaturel.csv',\
                      sep = ';', skiprows = 3,  names = ['Code' , 'PNR_label', 'pop_density_2016' ,'EPCI_2019'])

# nettoyage colonne PNR_label:
detail_PNR = df_PNR["PNR_label"].str.rsplit(' - ', expand = True)
df_PNR = df_PNR.join(detail_PNR, on = df_PNR.index)
df_PNR.drop(['PNR_label', 0], axis = 1, inplace = True)
df_PNR.reset_index(inplace = True)

#renommage des colonnes
df_PNR.columns = ['CodeINSEE', 'Name', 'pop_density_2016', 'EPCI_2019', 'PNR_label']
df_PNR['PNR_label'].replace('hors champ', '', inplace = True)


####### import des COORDONNEES GEOGRAPHIQUES de chaque commune

# import du fichier csv des commmunes et calcule de la distance entre chaque ville pour la ville sélectionnée
df_commune = pd.read_excel(r'C:\Users\scriba\Drive_Go\Wild_Code_School\PROJET_4\Bases SELECTION\Communes_informations_SUD.xlsx', encoding = 'utf-8')

# création du tuple des coordonnées géo
df_commune['COORD_GEO'] = df_commune[['LATITUDE', 'LONGITUDE']].apply(tuple, axis = 1)

# nettoyage des lignes doublons : suppression des mairies déléguées
df_commune.drop(index = [25,289], inplace = True)
# nettoyage des arrondissements de Marseille
df_commune.drop(index = [649,650, 651, 652, 653, 654, 655, 656], inplace = True)
# nettoyage regroupement communes 05
df_commune.drop(index = [233, 275 , 307, 325, 333], inplace = True)


####### MERGE des 2 datasets : left join on df_commune pour voir les lignes en plus
df_PORTRAIT = pd.merge(df_DEP, df_POP, how = 'left', left_on = 'Code INSEE', right_on = 'Code')
df_PORTRAIT_2 = pd.merge(df_commune, df_PNR, how = 'left', left_on = 'CODE INSEE', right_on = 'CodeINSEE')

df_PORTRAIT = pd.merge(df_PORTRAIT, df_PORTRAIT_2, how = 'left', left_on = 'Code INSEE', right_on = 'CODE INSEE' )
df_PORTRAIT.drop(columns = ['Code', 'Libellé','population 2015', 'population 2014',\
       'population 2013', 'population 2012', 'population 2011',\
       'population 2010', 'population 2009', 'indice de jeunesse 2015',\
         'indice de vieillissement 2015', 'CODE INSEE', 'LIBELLE COMMUNE',\
        'CODE POSTAL','CODE REGION', 'LIBELLE REGION', 'CODE ZE2010',\
       'LIBELLE ZONE EMPLOI','ACADEMIE', 'LIBELLE DEPARTEMENT', 'CODE ARRONDISSEMENT',\
           'CODE CANTON','CodeINSEE', 'Name', 'EPCI_2019', 'POPULATION TOTALE 2017', 'pop_density_2016',\
               'COMMUNE MAIRIE' ], inplace = True)

df_PORTRAIT.info()

#renommage des colonnes
df_PORTRAIT.columns  = ['CODE_INSEE', 'CODE_POSTAL', 'COMMUNE',
       'DEPARTEMENT', 'SUPERFICIE_2016', 'POPULATION_2016',
       'DENSITE_POP_2016', 'MAIRIE', 'ADRESSE_MAIRIE', 'TELEPHONE_MAIRIE',
       'E_MAIL_MAIRIE', 'SITE_INTERNET_MAIRIE', 'LATITUDE', 'LONGITUDE', 
       'CODE_DEPARTEMENT', 'INTERCOMMUNALITE', 'COORD_GEO', 'PNR']

#mise en ordre
df_PORTRAIT = df_PORTRAIT[['CODE_INSEE', 'CODE_POSTAL', 'COMMUNE',
       'DEPARTEMENT', 'CODE_DEPARTEMENT', 'SUPERFICIE_2016', 'POPULATION_2016',
       'DENSITE_POP_2016', 'MAIRIE', 'ADRESSE_MAIRIE', 'TELEPHONE_MAIRIE',
       'E_MAIL_MAIRIE', 'SITE_INTERNET_MAIRIE',  'INTERCOMMUNALITE', 'LATITUDE',
       'LONGITUDE', 'COORD_GEO', 'PNR']]

#export du csv
df_PORTRAIT.to_csv('df_PORTRAIT.csv')