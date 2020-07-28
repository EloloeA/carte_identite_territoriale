# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 08:43:49 2020

@author: elo

"""
# import des librairies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# chargement du fichier de réponses:
df = pd.read_csv('https://raw.githubusercontent.com/MeryemGrassi/Projet-CI-territoitre/master/REP_QST.csv', skiprows = 1,  names = ['horodateur', 'Q1', 'Q2', 'QO'])
NOMBRE_REPONSES = len(df)


#liste des items proposés dans le qst :
vocabulaire = ["Hôtels / camping/ Auberges",\
               "Activités / centres de loisirs",\
                "Réserves naturelles régionales",\
                "Jour de marché",\
                "Restaurants/ bars",\
                "Musées/patrimoine",\
                "Evènements à venir",\
                "Liste de cinéma",\
                "Stations-services",\
                "Pharmacies /défibrillateurs",\
                "Transports en commun",\
                "Parkings",\
                "Météo",\
                "Qualité de l'air"]
'''
la liste de vocabulaire tel quel ne fonctionne pas avec CountVectorizer
car il prend les mots 1/1 => il faut simplifier la liste de vocab :
'''
vocabulaire_low = ["Hôtels",\
               "centres",\
                "Réserves",\
                "marché",\
                "Restaurants",\
                "Musées",\
                "Evènements",\
                "cinéma",\
                "Stations",\
                "Pharmacies",\
                "Transports",\
                "Parkings",\
                "Météo",\
                "Qualité"]
    
# liste d'items passé en minuscule
voca = []
for e in vocabulaire_low:
    voca.append(e.lower())

# utiliser CountVectorizer pour séparer les items
cv = CountVectorizer(vocabulary = voca)


# la colonne à vectoriser est celle des réponses, passée également en minuscules
X = df['Q1']
X = X.apply(str.lower)

# on entraine et transforme le transformer cv
res = cv.fit_transform(X)

# création d'un dataframe:
features = cv.get_feature_names() #vérification du découpage / CV
resQ = pd.DataFrame(res.A, columns = vocabulaire) #simplification des noms des colonnes, utiliser ensuite vocab complet ?
resQ = pd.concat([X, resQ], axis = 1)


# pour sauvegarder le fichier en csv:
# resQ.to_csv('out.csv')

#Calcul de stats sur le df resQ
votes = resQ.loc[:,"Hôtels / camping/ Auberges":"Qualité de l'air"].sum()
percentVote = votes/NOMBRE_REPONSES*100

# création d'un dataframe qui reprend les colonnes votes et percentVote
df_stat = pd.DataFrame({'nombre de vote' : votes, 'pourcentage de votes' : percentVote})
df_stat.reset_index(inplace = True)

# tri des valeurs
df_stat = df_stat.sort_values(by = 'nombre de vote', ascending = False)


# ///////visualisations ///////

#REGLAGES FENETRE GRAPHIQUE
font = {'family' : 'tahoma',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)

# histogramme avec SEABORN
#TODO : mettre le nom complet en index
plt.figure(figsize = (14,12))
g = sns.barplot(data = df_stat, y = 'index', x = 'pourcentage de votes', palette = 'Set2')
ax = g.axes

for p in ax.patches:
    ax.text(p.get_width() +.3,p.get_y()+0.6,\
        str(round(p.get_width(),2)) + '%', fontsize = 15)

plt.title('Résultat du sondage') 
sns.despine()
plt.show()


# WORDCLOUD de la question ouverte
from wordcloud import WordCloud
text = df['QO'].dropna()
t = ''
for word in text:
    t += word + ''
    
    
wordcloud = WordCloud(background_color="white", max_words=200, width=400, height=400,  random_state=1).generate(t)

plt.figure(figsize = (15,10))
plt.clf()
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
