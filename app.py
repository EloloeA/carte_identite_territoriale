# -*- coding: utf-8 -*-
"""
Dashboard Carte identité du territoire - Juillet 2020
by Elodie
"""

# import des librairies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import os

import plotly.express as px
import pandas as pd

import outils

# chargement des dataframes df et df_hebergement
lien_df_portrait = "https://raw.githubusercontent.com/EloloeA/carte_identite_territoriale/master/data/df_PORTRAIT.csv"
df = pd.read_csv(lien_df_portrait, index_col = 0)
# retirer les valeurs nulles de la colonne PNR
df['PNR'].fillna('', inplace = True)
# Retirer les lettres capitales avec accents de la colonne COMMUNE car sinon ne se trie pas bien dans le dropdown
df['COMMUNE'] = df['COMMUNE'].str.replace('É', 'E').str.replace('È', 'E')


dir = os.getcwd() + "\data"
# lien = "C:\\Users\\scriba\\Drive_Go\\Wild_Code_School\\PROJET_4\\carte_identite_territoriale\\data\\APIDAE_Final.csv"
lien_df_hebergement = os.path.join(dir, "APIDAE_Final.csv")
df_hebergement = pd.read_csv(lien_df_hebergement, index_col = 0)


# réglage échelle couleur pour les tables
colorscale = [[0, '#014b86'],[.5, '#C1E2FA'],[1, '#ffffff']]

# dictionnaire des départements pour le dropdown 
dep = df[['CODE_INSEE', 'COMMUNE']]
dep = dep.sort_values(by='COMMUNE')
dep.columns = ['value', 'label']
dep = dep.to_dict(orient = 'records')

 

#initialisation du dashboard
app = dash.Dash(__name__)


# fonction carte
def mapSud(df):
    geo = px.scatter_mapbox(df, lat='LATITUDE', lon='LONGITUDE', hover_name= 'COMMUNE',
                            size = 'POPULATION_2016', zoom=8, height=300, width = 300)
    geo.update_layout(mapbox_style="open-street-map")
    geo.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return geo

# layout dash => construction des balises html et incorporation de graphiques (cartes et tables)
app.layout = html.Div(id= 'main', children = [
                          html.Div(className = 'topHeader',
                                   children = [
                                    html.H1(children = "Carte d'identité Territoriale - REGION SUD"),
                                    html.H3(children = "Prototype d'application de l'utilisation des données OpenSource de la région SUD"),
                                    html.Br(),
                                    html.P('Sélectionnez une ville :'),
                                    # liste déroulante :
                                    dcc.Dropdown(
                                        id = 'cityChoice',
                                        options = dep,
                                        multi=False,
                                        value = 4001)
                                        ]),
                          html.Br(),
                          
                          html.Div(id = 'display_name_of_city'),
                          
                          html.Div(id = 'superficieDepPop', 
                                   children = [
                                      html.Div(['Département : ',
                                                html.Div(id = 'departement')
                                                ], style = {'margin' : '20px'}),
                                      html.Div(['Densité de population (hab/km²): ',
                                                html.Div(id = 'densitePop')
                                                ], style = {'margin' : '20px'}),
                                      html.Div(["Nombre d'habitants : ",
                                                html.Div(id = 'nbreHabitant')
                                                ], style = {'margin' : '20px'}),
                                      html.Div(['Superficie (en km²) :',
                                                 html.Div(id = 'superficie')
                                                ], style = {'margin' : '20px'}),
                                      dcc.Graph(id = 'mapOfCity', className = 'mapLocalisation',
                                              figure = {})
                                              ]),
                                                         
                            html.Br(),
                            html.P(id = 'PNR'),
                            html.Br(),
                            html.Br(),
                            
                            html.Div("Nombre d'hébergements (hôtels, campings, auberges)\
                                         pour cette commune : ", style = {'textAlign' : 'center'}),
                            html.Div(id = 'nbreLogement', style = {'textAlign' : 'center'}),
                            
                            #table logement si existant ou < 5
                            html.Div(dcc.Graph(id = 'hotel', figure = {})),
                            
                            dcc.Graph(id = 'mapOfHotel', figure = {}),
                            
                            html.Br(),
                            html.Br(),
                            
                            html.Footer("Projet REGION SUD by WILD CODE SCHOOL")
                            ])
                          

# MAJ des éléments du portrait
@app.callback(
    Output('nbreHabitant', 'children'),
    [Input('cityChoice', 'value')])
def update_output_habitant(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    nbreHabitant = dff.iloc[0]['POPULATION_2016']
    return nbreHabitant

@app.callback(
    Output('superficie', 'children'),
    [Input('cityChoice', 'value')])
def update_output_superficie(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    superficie = dff.iloc[0]['SUPERFICIE_2016']
    return superficie
        
@app.callback(
    Output('densitePop', 'children'),
    [Input('cityChoice', 'value')])
def update_output_densite(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    densitePop = dff.iloc[0]['DENSITE_POP_2016']
    return densitePop
        
@app.callback(
    Output('departement', 'children'),
    [Input('cityChoice', 'value')])
def update_output_dep(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    departement = dff.iloc[0]['DEPARTEMENT']
    return departement


# MAJ nom de la ville
@app.callback(
    Output('display_name_of_city', 'children'),
    [Input('cityChoice', 'value')])
def update_ville(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    ville = dff.iloc[0]['COMMUNE']
    return ville

#MAJ carte de situation de la ville
@app.callback(
    Output('mapOfCity', 'figure'),
    [Input('cityChoice', 'value')])
def update_map(input_value):
    df_sel = df[df['CODE_INSEE'] == input_value]
    fig2 = mapSud(df_sel)
    fig2.update_layout(transition_duration=500)
    return fig2

#MAJ carte des hôtels, campings et auberges
@app.callback(
    Output('mapOfHotel', 'figure'),
    [Input('cityChoice', 'value')])
def update_mapHebergement(input_value):
    df_sel = df_hebergement[df_hebergement['Code insee'] == input_value]
    geo = px.scatter_mapbox(df_sel, lat='Latitude', lon='Longitude', hover_name= 'Nom',\
                        zoom = 10, height = 500, width = 800, title = "Hôtels, campings et Auberges",\
                        color = df_sel.index) 
    geo.update_layout(mapbox_style="carto-positron")
    return geo

# table avec liste hotels/camping/auberge
@app.callback(
    Output('hotel', 'figure'),
    [Input('cityChoice', 'value')])
def liste_hotel(input_value):
    df_sel = df_hebergement[df_hebergement['Code insee'] == input_value]
    if df_sel.shape[0] == 0:
        nombre = 0
        commune = df[df['CODE_INSEE'] == input_value]['COMMUNE']
        df_hotel = [['Commune', "Nombre d'hébergements"], [commune, nombre]]
        df_hotel = ff.create_table(df_hotel, colorscale=colorscale)
    elif df_sel.shape[0] < 6:
        commune = df_sel.iloc[0]['Commune']
        df_hotel = ff.create_table(df_sel[['Commune', 'Nom', 'Type']], colorscale=colorscale)
    else:
        nombre = df_sel.shape[0]
        commune = df_sel.iloc[0]['Commune']
        df_hotel = [['Commune', "Nombre d'hébergements"], [commune, nombre]]
        df_hotel = ff.create_table(df_hotel, colorscale=colorscale)
    return df_hotel
        
        
# nombre d'hôtel/campings/auberges
@app.callback(
    Output('nbreLogement', 'children'),
    [Input('cityChoice', 'value')])
def nombre_logement(input_value):
    df_sel = df_hebergement[df_hebergement['Code insee'] == input_value]
    return df_sel.shape[0]

# MAJ du PNR
@app.callback(
    Output('PNR', 'children'),
    [Input('cityChoice', 'value')])
def update_output_pnr(input_value):
    resPNR = df.loc[df['CODE_INSEE'] == input_value, 'PNR'].values[0]
    if resPNR != '':
        # pour un parc : nbre de villes
        nbre_ville_dans_le_PNR = df.loc[df['PNR'] == resPNR,'COMMUNE'].count()
        # pour un parc : densité moyenne de population de la zone
        densiteMoy = df.loc[df['PNR'] == resPNR,'DENSITE_POP_2016'].mean()
        densiteMoy = round(densiteMoy)
        return(f'La ville que vous avez choisie fait partie du {resPNR}. \
               Il y a {nbre_ville_dans_le_PNR} villes qui font parties du {resPNR}. \
               La densité moyenne des communes du {resPNR} est de {densiteMoy} hab/km2.')
    
    else:
        resVilleProche, nbre_km = outils.distanceCommunes(df, input_value)
        resVilleProche = int(resVilleProche)
        resPNR_villeProche = df.loc[df['CODE_INSEE'] == resVilleProche, 'PNR'].values[0]
            
        return (f"Cette commune ne fait pas partie d'un Parc Naturel Régional, \
                La ville la plus proche est {outils.correspondanceInseeVille(resVilleProche)},\
                qui appartient au {resPNR_villeProche}.\
                Distance en km : {round(nbre_km)}")  

     
# lancement de l'application:
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

