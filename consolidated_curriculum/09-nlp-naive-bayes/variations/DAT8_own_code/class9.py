# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
url = 'https://raw.githubusercontent.com/justmarkham/DAT4-students/master/kerry/Final/NBA_players_2015.csv'
nba = pd.read_csv(url, index_col=0)

nba['pos_num'] = nba.pos.map({'C':0, 'F':1, 'G':2})
feature_cols = ['ast', 'stl', 'blk', 'tov', 'pf']
X = nba[feature_cols]
y = nba.pos_num

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(X, y)
y_pred_class = knn.predict(X)

from sklearn import metrics
print metrics.accuracy_score(y, y_pred_class)

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X, y)
y_pred_class = knn.predict(X)
print metrics.accuracy_score(y, y_pred_class)



