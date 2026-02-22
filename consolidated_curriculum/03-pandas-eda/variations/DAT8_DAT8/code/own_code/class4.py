# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 18:37:19 2015

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt

# cd ~/Desktop/DAT8/data
users = pd.read_table('u.user', sep='|', index_col='user_id')

users.shape
users.dtypes
users.describe()
users.describe(include=['object'])
users.describe(include='all')
users.age.value_counts().sort_index().tail()


drinks = pd.read_table('drinks.csv', sep=',')
drinks.head()
drinks.tail()
drinks.index
drinks.dtypes
drinks.shape
drinks.beer_servings
drinks.beer_servings.mean()
drinks.continent.value_counts()

users.shape[0]
users.occupation.value_counts().head(3)

pd.read_table('u.user_original', sep='|',
              header=None,
              names=['user_id', 'age', 'gender', 'occupation', 'zip_code'], index_col='user_id')
              
users.age.hist()
users.age.hist(by=users.occupation)
users.gender_num = users.gender.map({'M':0, 'F':1})
users.gender_num.hist()

young_bool = users.age < 20
users.age.hist(by=users.gender)

drinks[drinks.continent == 'EU']
drinks[drinks.continent == 'EU' & drinks.wine_servings > 300]
drinks.beer_servings.mean()
drinks.sort('total_litres_of_pure_alcohol', ascending=0).head(10)
users.sort(['occupation','age']).head()
users[users.occupation.isin(['doctor','lawyer'])]

ufo = pd.read_csv('ufo.csv')
ufo.shape
ufo.describe()
ufo['Colors Reported'].value_counts().head(4)
ufo[ufo.State == 'VA'].City.value_counts().head(1)
ufo[ufo.State == 'VA' & ufo.City == 'Arlington']
ufo[ufo.State == 'VA'][ufo.City == 'Arlington']
ufo.isnull().sum()
ufo[ufo.City.isnull()]
ufo.dropna().shape[0]
