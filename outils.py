# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:39:45 2020

@author: elo
"""
import pandas as pd
#=> dans le main ?

# liens vers dataframe
lien_df_portrait = "https://raw.githubusercontent.com/MeryemGrassi/Projet-CI-territoitre/master/data/df_PORTRAIT.csv"
lien_distance_villes = "https://raw.githubusercontent.com/MeryemGrassi/Projet-CI-territoitre/master/data/distanceVilles.csv"


# FONCTIONS

# FAIRE une fonction init qui charge les df et renvoie le final;l'appeler depuis le main script
def init():
    '''importe les différents df nécessaires'''
    df_PORTRAIT = pd.read_csv(lien_df_portrait, index_col = 0)
    # TODO autres bases
    return df_PORTRAIT


# fonctions 'utiles'
def correspondanceVilleInsee(ville):
    df_PORTRAIT = init()
    resINSEE = df_PORTRAIT.loc[df_PORTRAIT['COMMUNE'] == ville, 'CODE_INSEE'].values[0]
    return resINSEE

def correspondanceInseeVille(insee):
    df_PORTRAIT = init()
    resVILLE = df_PORTRAIT.loc[df_PORTRAIT['CODE_INSEE'] == insee, 'COMMUNE'].values[0]
    return resVILLE

# calcul d'un plus petit df de distances
def distanceCommunes(df, codeINSEE):
    '''création d'un df de distances avec code INSEE des communes'''
    df_PNR = df.loc[df["PNR"] != ""]
    liste_Com = list(df_PNR['CODE_INSEE'].unique())
    if codeINSEE in liste_Com:
        liste_Com.remove(codeINSEE)
    df_temp = pd.DataFrame(index = [liste_Com])
    premVille = df.loc[df['CODE_INSEE'] == codeINSEE, 'COORD_GEO']
    for j in liste_Com:
        deuxVille = df_PNR.loc[df_PNR['CODE_INSEE'] == j, 'COORD_GEO']
        dist = calculDistance(eval(premVille.values[0]), eval(deuxVille.values[0]))
        df_temp.loc[j, 'distance'] = dist
    #enregistrement en csv
    # df_temp.to_csv(r'C:\Users\scriba\Drive_Go\Wild_Code_School\PROJET_4\distanceVillesv2.csv')   
    id_ville = df_temp["distance"].idxmin()[0]
    return id_ville, df_temp.loc[id_ville, 'distance'].values[0]


# def villeLaPlusProche(codeInsee, i = 1):
#     '''fonction qui retourne le code INSEE de la ième plus proche ville de celle donnée'''
#     distancesTab = pd.read_csv(lien_distance_villes, index_col = 0)

#     # trier la ligne correspondantes à ce code Insee:
#     distancesTab = distancesTab.sort_values(by=codeInsee, axis=1)
#     # extraire ligne qui nous intéresse
#     resDistance = distancesTab.loc[codeInsee]
    
#     #la première ligne = la même ville, distance de 0
#     villeProche = resDistance.index[i]
#     nbre_km = resDistance.iloc[i]
#     return int(villeProche), nbre_km

# # ATTENTION TEMPS d'EXECUTION ASSEZ LONG (fichier déjà crée sous = distanceVilles) DANS SRC ?
import haversine as hs # calcul de distance géographique

def calculDistance(loc1, loc2):
    '''calcul de la distance entre 2 points géographiques avec loc1 et loc2 = tuples (long, lat)'''
    return hs.haversine(loc1,loc2)

# def distanceCommunes(df):
#     '''création d'un df de distances avec code INSEE des communes'''
#     liste_Com = list(df['CODE_INSEE'].unique())
#     df_temp = pd.DataFrame(index = [liste_Com])
#     for i in liste_Com:
#         premVille = df.loc[df['CODE_INSEE'] == i, 'COORD_GEO']
#         for j in liste_Com:
#             deuxVille = df.loc[df['CODE_INSEE'] == j, 'COORD_GEO']
#             dist = calculDistance(eval(premVille.values[0]), eval(deuxVille.values[0]))
#             new_col = str(j)
#             df_temp.loc[i, new_col] = dist
#     #enregistrement en csv
#     df_temp.to_csv(r'C:\Users\scriba\Drive_Go\Wild_Code_School\PROJET_4\distanceVilles.csv')   
#     return df_temp

#############



