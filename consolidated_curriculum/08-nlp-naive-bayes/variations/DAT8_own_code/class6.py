# -*- coding: utf-8 -*-
"""
Created on Thu Sep 03 18:39:04 2015

@author: user
"""

# cd ~/Desktop/DAT8/data

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (10, 8)

# pip install seaborn
import seaborn as sns

# plt.style.available
plt.style.use('ggplot')

drinks = pd.read_table('drinks.csv', sep=',')
drinks.rename(columns={'beer_servings':'beer', 'wine_servings':'wine'}, inplace=True)
drink_cols = ['country', 'beer', 'spirit', 'wine', 'liters', 'continent']
drinks.columns = drink_cols

ufo = pd.read_csv('ufo.csv')
ufo['Time'] = pd.to_datetime(ufo.Time)
ufo['Year'] = ufo.Time.dt.year

drinks.beer.plot(kind='hist', bins=20)
drinks.groupby('continent').mean().drop('liters', axis=1).plot(kind='bar')

drinks.boxplot('beer', by='continent')
sns.violinplot(x='continent', y='beer', data=drinks)

drinks.hist(column='beer', by='continent', sharex=True, sharey=True)

flower_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
flowers = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None, names=flower_cols)
flowers.isnull().sum()

flowers.boxplot(by='species')
sns.violinplot(x='species', y='petal_length', data=flowers)
flowers['species_int'] = flowers.species.factorize()[0]
species_names = flowers.species.unique()
flowers['species_int'] = flowers.species.map({species_names[0]: 0, species_names[1]: 1, species_names[2]: 2})
flowers.plot('scatter', x='petal_length', y='sepal_length', c='species_int')
pd.scatter_matrix(flowers.drop('species_int', axis=1), c=flowers.species_int, figsize=(12,10))


groups = flowers.groupby('species')
groups.describe()

fig, ax = plt.subplots()
ax.margins(0.05)
for name, group in groups:
    ax.plot(group.sepal_length, group.sepal_width, marker='o', linestyle='', ms=12, label=name)
ax.legend(numpoints=1, loc='upper left')

plt.show()

fig, ax = plt.subplots()
ax.margins(0.05)
for name, group in groups:
    ax.plot(group.petal_length, group.petal_width, marker='o', linestyle='', ms=12, label=name)
ax.legend(numpoints=1, loc='upper left')

plt.show()

def predict_species(df):
    temp = df.copy(deep=True);
    temp['species_pred'] = ''
    temp.species_pred[df.petal_length <= 2] = 'setosa'
    temp.species_pred[(df.petal_length > 2) & (df.petal_length <= 5)] = 'versicolor'
    temp.species_pred[df.petal_length > 5] = 'virginica'
    return temp
        
flowers_hat = predict_species(flowers)

flowers['petal_area'] = flowers.petal_length * flowers.petal_width
flowers.groupby('species').petal_area.describe().unstack()