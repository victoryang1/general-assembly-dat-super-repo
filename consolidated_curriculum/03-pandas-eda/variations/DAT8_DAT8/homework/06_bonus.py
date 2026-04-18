# -*- coding: utf-8 -*-
"""
Created on Thu Sep 03 20:54:09 2015

@author: vyang91
"""
# cd ~/Desktop/DAT8/data
# %reset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# display plots in the notebook
# %matplotlib inline

# increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# define a list of column names (as strings)
col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

# define the URL from which to retrieve the data (as a string)
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

# retrieve the CSV file and add the column names
iris = pd.read_csv(url, header=None, names=col_names)

iris['species_int'] = iris.species.factorize()[0]
# species_names = iris.species.unique()
# iris['species_int'] = iris.species.map({species_names[0]: 0, species_names[1]: 1, species_names[2]: 2})

# plt.colormaps()
iris.plot(kind='scatter', x='petal_length', y='petal_width', c='species_int', colormap='Spectral')
iris.plot(kind='scatter', x='sepal_length', y='sepal_width', c='species_int', colormap='Spectral')
pd.scatter_matrix(iris.drop('species_int', axis=1), c=iris.species_int, figsize=(12,10))

iris.boxplot(by='species')

iris['petal_area'] = iris.petal_length * iris.petal_width
sns.violinplot(x='species', y='petal_length', data=iris)
sns.violinplot(x='species', y='petal_width', data=iris)
sns.violinplot(x='species', y='petal_area', data=iris)

def predict_species(df):
    ans = df.copy(deep=True);
    ans['species_pred'] = ''
    ans.species_pred[df.petal_length <= 2] = 'setosa'
    ans.species_pred[(df.petal_length > 2) & (df.petal_length <= 5)] = 'versicolor'
    ans.species_pred[df.petal_length > 5] = 'virginica'
    return ans
        
iris_pred = predict_species(iris)
