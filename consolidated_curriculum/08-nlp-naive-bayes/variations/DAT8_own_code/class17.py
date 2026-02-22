# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 19:14:47 2015

@author: user
"""

# cd ~/Desktop/DAT8/data

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (15, 12)

url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/vehicles_train.csv'
train = pd.read_csv(url)
train['vtype_int'] = train['vtype'].map({'car':0, 'truck':1})

pd.scatter_matrix(train)

train_1 = train[train.miles < 100000]
train_1[train_1.year < 2010].price.mean()
train_1[train_1.year >= 2010].price.mean()
train_2 = train[train.miles >= 100000]
train_2[train_2.year < 2001].price.mean()
train_2[train_2.year >= 2001].price.mean()

pd.scatter_matrix(train_1)
pd.scatter_matrix(train_2)

pd.scatter_matrix(train_1[train_1.year < 2010])
pd.scatter_matrix(train_1[train_1.year >= 2010])

pd.scatter_matrix(train_2[train_2.year < 2001])
pd.scatter_matrix(train_2[train_2.year >= 2001])