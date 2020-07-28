# -*- coding: utf-8 -*-
"""
Outils Carte identité du territoire - Juillet 2020
by Elodie
"""
import pandas as pd
import haversine as hs # module de calcul de distance géographique


# liens vers dataframe
lien_df_portrait = "https://raw.githubusercontent.com/EloloeA/carte_identite_territoriale/master/data/df_PORTRAIT.csv"


# FONCTIONS

def init():
    '''importe les différents df nécessaires'''
    df_PORTRAIT = pd.read_csv(lien_df_portrait, index_col = 0)
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


# calcul des distances des plus proches communes appartenant à un Parc Naturel Régional

def calculDistance(loc1, loc2):
    '''calcul de la distance entre 2 points géographiques avec loc1 et loc2 = tuples (long, lat)'''
    return hs.haversine(loc1,loc2)

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
    id_ville = df_temp["distance"].idxmin()[0]
    return id_ville, df_temp.loc[id_ville, 'distance'].values[0]



