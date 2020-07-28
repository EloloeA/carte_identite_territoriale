# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:20:18 2020

@author: scriba
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

import outils


lien_df_portrait = "https://raw.githubusercontent.com/MeryemGrassi/Projet-CI-territoitre/master/data/df_PORTRAIT.csv"
df = pd.read_csv(lien_df_portrait, index_col = 0)
# retirer les nan des PNR
df['PNR'].fillna('', inplace = True)

# dictionnaire des départements pour le dropdown #TODO PB avec accents capital avec accent triés à la fin...
dep = df[['CODE_INSEE', 'COMMUNE']]
dep = dep.sort_values(by='COMMUNE')
dep.columns = ['value', 'label']
dep = dep.to_dict(orient = 'records')

 


app = dash.Dash(__name__)

colors = {
    'background': 'white',
    'text': '#0072bc'
}


# carte
def mapSud(df):
    geo = px.scatter_mapbox(df, lat='LATITUDE', lon='LONGITUDE', hover_name= 'COMMUNE',
                            size = 'POPULATION_2016', zoom=8, height=300, width = 300)
    geo.update_layout(mapbox_style="open-street-map")
    geo.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return geo


# (essai graphe à ne pas conserver)
def portraitVille(df, commune):
    fig = px.bar(df, y='COMMUNE', x='POPULATION_2016',
             hover_data=['SUPERFICIE_2016', 'DENSITE_POP_2016'], color='DENSITE_POP_2016',
             title = f"Population 2016 pour la commune : {commune}",
             height=500,
             orientation = 'h')
    return fig



app.layout = html.Div(id= 'main',
                      children = [
                          html.Div(className = 'one_column', 
                                   children = [
                                     html.H1(children = "Carte d'identité Territoriale - REGION SUD",
                                     ),
                             
                                    html.H3(children = "Prototype d'application de l'utilisation des données OpenSource de la région SUD. Projet REGION SUD by WILD CODE SCHOOL", 
                                     ),
                                    
                                    html.P('Sélectionnez une ville :'),
                             
                                    dcc.Dropdown(
                                        id = 'cityChoice',
                                        options = dep,
                                        multi=False,
                                        value = 4001
                                        ),
                             
                                    html.P(id = 'display_name_of_city'),
                                    ]),
                          
                          html.Div([
                              html.Div(['Superficie (en km²) :',
                                html.Div(id = 'superficie')
                                        ], style = {'textAlign' : 'center', 'margin' : '10px 10px 10px 10px'}),
                              html.Div(['Département : ',
                                        html.Div(id = 'departement')
                                        ], style = {'textAlign' : 'center', 'margin' : '10px 10px 10px 10px'}),
                              html.Div(['Densité de population : ',
                                        html.Div(id = 'densitePop')
                                        ], style = {'textAlign' : 'center',  'margin' : '10px 10px 10px 10px'}),
                              html.Div(["Nombre d'habitants : ",
                                        html.Div(id = 'nbreHabitant')
                                        ], style = {'textAlign' : 'center',  'margin' : '10px 10px 10px 10px'})
                              ],
                              
                              style = {'color' : 'orange', 'display' : 'flex', 'justify-content' : 'center'}),
                                                         
                                    
                            html.Div(className = 'two_columns',
                                     children = [
                                         html.Div(id = 'bloc_droite'),
                                         html.Div(className = 'bloc2', children = [
                                             dcc.Graph(id = 'mapOfCity', figure = {}),
                                             html.Div(id = 'PNR')
                                             ])
                                         ]),
                            
                            html.Div(className = 'one_column',
                                     children = [
                                         dash_table.DataTable(
                                            id='table',
                                            columns=[{"name": i, "id": i} for i in df.columns],
                                            data=df.to_dict('records')),
                                         
                                         dcc.Graph(),
                                         
                                         dash_table.DataTable()
                                         ])
                            ])
                          

# MAJ du portrait
# @app.callback(
#     Output('portrait', 'children'),
#     [Input('cityChoice', 'value')])
# def update_output_div(input_value):
#     dff = df[df['CODE_INSEE'] == input_value]
#     ville = dff.iloc[0]['COMMUNE']
#     nbreHabitant = dff.iloc[0]['POPULATION_2016']
#     superficie = dff.iloc[0]['SUPERFICIE_2016']
#     densitePop = dff.iloc[0]['DENSITE_POP_2016']
#     departement = dff.iloc[0]['DEPARTEMENT']
#     return f"""\
#         Votre commune : {ville} a {nbreHabitant} habitants, pour une surface totale de {superficie} km²
#         soit une densité de population de {densitePop} habitants par km² (source : INSEE 2016).
#         DEPARTEMENT : {departement}\
#         """

# décomposition du portrait
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


# MAJ du PNR
@app.callback(
    Output('PNR', 'children'),
    [Input('cityChoice', 'value')])
def update_output_pnr(input_value):
    resPNR = df.loc[df['CODE_INSEE'] == input_value, 'PNR'].values[0]
    if resPNR != '':
        # pour un parc : nbre de villes
        nbre_ville_dans_le_PNR = df.loc[df['PNR'] == resPNR,'COMMUNE'].count()
        # pour un parc : densité moyenne de population de la zone ?
        densiteMoy = df.loc[df['PNR'] == resPNR,'DENSITE_POP_2016'].mean()
        # densiteMediane = df.loc[df['PNR'] == resPNR,'DENSITE_POP_2016'].median()
        densiteMoy = round(densiteMoy)
        return(f'La ville que vous avez choisie fait partie du {resPNR}. \
               Il y a {nbre_ville_dans_le_PNR} villes qui font parties du {resPNR}. \
               La densité moyenne des communes du {resPNR} est de {densiteMoy} hab/km2.')
    
    else:
        df_PNR = df.loc[df["PNR"] != ""]
        resVilleProche, nbre_km = outils.distanceCommunes(df, input_value)
        resVilleProche = int(resVilleProche)
        resPNR_villeProche = df.loc[df['CODE_INSEE'] == resVilleProche, 'PNR'].values[0]
            
        return (f"Cette commune ne fait pas partie d'un Parc Naturel Régional, \
                La ville la plus proche est {outils.correspondanceInseeVille(resVilleProche)},\
                qui appartient au {resPNR_villeProche}.\
                Distance en km : {round(nbre_km)}")  

     

#MAJ table
@app.callback(
    Output('table', 'data'),
    [Input('cityChoice', 'value')])
def update_table(input_value):
    dff = df[df['CODE_INSEE'] == input_value]
    return dff.to_dict('records')





if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

