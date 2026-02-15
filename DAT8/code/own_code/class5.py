# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 18:37:01 2015

@author: user
"""

import pandas as pd
drinks = pd.read_table('drinks.csv', sep=',')

drinks.rename(columns={'beer_servings':'beer', 'wine_servings':'wine'}, inplace=True)
drink_cols = ['country', 'beer', 'spirit', 'wine', 'liters', 'continent']
drinks.columns = drink_cols

# replace all column names when reading the file
drinks = pd.read_csv('drinks.csv', header=0, names=drink_cols)
drinks.continent.fillna(value='NA', inplace=True)

drinks = pd.read_csv('drinks.csv', header=0, names=drink_cols, na_filter=False)

ufo = pd.read_csv('ufo.csv')
ufo.shape
ufo.describe().loc['top']
ufo['Colors Reported'].value_counts().head(4)
ufo_colors_all = ufo['Colors Reported'].value_counts()

# colors_all = [i.split() for i in color if !isinstance(i, float)]
colors_all = [i.split() for i in set(ufo.Colors_Reported) if isinstance(i, str)]
colors_unique = set([item for sublist in colors_all for item in sublist])

from collections import defaultdict
dcolor = defaultdict(int)
for color in colors_unique:
    if color in ufo.Colors_Reported:
        print(color)
    for row in ufo:
        if color in row.Colors_Reported:
            dcolor[color] += 1
            
for row in ufo:
    print(type(row))
    print(row)

        

ufo[ufo.State == 'VA'].City.value_counts().head(1)
ufo[(ufo.State == 'VA') & (ufo.City == 'Arlington')]
# ufo[ufo.State == 'VA'][ufo.City == 'Arlington']
ufo.isnull().sum()
ufo[ufo.City.isnull()]
ufo.dropna().shape[0]
ufo_cols = ufo.columns.tolist()
ufo_cols = [names.replace(' ', '_') for names in ufo.columns.tolist()]
ufo_cols2 = [names.replace(' ', '_') for names in ufo.columns]
ufo.columns = ufo.columns.str.replace(' ', '_')
ufo.columns = ufo_cols
# ufo.Location = ufo.City + ', ' + ufo.State
ufo['Location'] = ufo.City + ', ' + ufo.State

users = pd.read_table('u.user', sep='|', index_col='user_id')
users.groupby('occupation').count()
users.occupation.value_counts()
users.groupby('occupation').age.mean()
users.groupby('occupation').age.agg(['min','max'])
users.groupby(['occupation','gender']).age.mean()
users.groupby(['occupation','gender']).age.agg(['mean','count'])

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 8)


drinks[['beer', 'wine']].sort('beer').values
drinks.plot(kind='scatter', x='beer', y='wine', alpha=.3)
plt.xlabel('Beer')
plt.ylabel('Wine')
pd.scatter_matrix(drinks[['beer', 'spirit', 'wine']], figsize=(10,8))
plt.style.use('ggplot')
drinks.continent.value_counts().plot(kind='bar')
drinks.groupby('continent').mean().plot(kind='bar', figsize=(10,8))
drinks.groupby('continent').mean().drop('liters', axis=1).plot(kind='bar')
drinks.groupby('continent').mean().drop('liters', axis=1).plot(kind='bar', stacked=True)
