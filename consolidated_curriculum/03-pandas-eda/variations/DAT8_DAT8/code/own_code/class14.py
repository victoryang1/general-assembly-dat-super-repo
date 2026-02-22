# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 19:24:36 2015

@author: user
"""

import pandas as pd
import numpy as np

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
iris = pd.read_csv(url, header=None, names=col_names)
iris.head()

iris.loc[:, 'sepal_length':'petal_width'] = iris.loc[:, 'sepal_length':'petal_width'].apply(np.ceil)
iris.head()

obs_features = [7, 3, 5, 2]
# show all observations with features: 7, 3, 5, 2
iris[(iris.sepal_length==obs_features[0]) &
    (iris.sepal_width==obs_features[1]) &
    (iris.petal_length==obs_features[2]) &
    (iris.petal_width==obs_features[3])]


# count the species for these observations
iris[(iris.sepal_length==obs_features[0]) &
    (iris.sepal_width==obs_features[1]) &
    (iris.petal_length==obs_features[2]) &
    (iris.petal_width==obs_features[3])].species.value_counts()

# count the species for all observations
iris.species.value_counts()

