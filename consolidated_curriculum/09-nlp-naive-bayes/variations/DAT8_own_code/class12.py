# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:45:16 2015

@author: yang
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.rcParams['figure.figsize'] = (10, 8)

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data'
col_names = ['id','ri','na','mg','al','si','k','ca','ba','fe','glass_type']
glass = pd.read_csv(url, names=col_names, index_col='id')
glass.sort('al', inplace=True)
glass.head()

sns.lmplot(x='al', y='ri', data=glass)


linreg = LinearRegression()
feature_cols = ['al']
X = glass[feature_cols]
y = glass.ri
linreg.fit(X, y)
glass['ri_pred'] = linreg.predict(X)

linreg.intercept_ + linreg.coef_ * 2

glass['household'] = glass.glass_type.map({1:0, 2:0, 3:0, 5:1, 6:1, 7:1})

feature_cols = ['al']
X = glass[feature_cols]
y = glass.household
linreg.fit(X, y)
glass['household_pred'] = linreg.predict(X)

import numpy as np
nums = np.array([5, 15, 8])
np.where(nums > 10, 'big', 'small')

glass['household_pred_class'] = np.where(glass.household_pred >= .5, 1, 0)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e9)
feature_cols = ['al']
X = glass[feature_cols]
y = glass.household
logreg.fit(X, y)
glass['household_pred_class'] = logreg.predict(X)

glass['household_pred_prob'] = logreg.predict_proba(X)[:, 1]

plt.scatter(glass.al, glass.household)
plt.plot(glass.al, glass.household_pred_prob, color='red')
plt.xlabel('al')
plt.ylabel('household')

glass['high_ba'] = np.where(glass.ba > .5, 1, 0)
sns.lmplot(x='ba', y='household', data=glass, logistic=True)
sns.lmplot(x='high_ba', y='household', data=glass, logistic=True, x_jitter=.01, y_jitter=.01)

###

titanic = pd.read_csv('https://github.com/justmarkham/DAT8/raw/master/data/titanic.csv')
feature_cols = ['Pclass', 'Parch']
X = titanic[feature_cols]
y = titanic.Survived

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

logreg.fit(X_train, y_train)
logreg.coef_

y_pred_class = logreg.predict(X_test)
y_pred_prob = logreg.predict_proba(X_test)[:,1]
# titanic['y_pred'] = y_pred
#dfTest = pd.concat([y_test, pd.Series(y_pred, name='pred')], axis=1)

from sklearn import metrics
metrics.accuracy_score(y_test, y_pred_class)

y_test.value_counts().head(1) / len(y_test)

confusion = metrics.confusion_matrix(y_test, y_pred_class)

# accuracy: 8/12
# sensitivity: 4/5
# specificity: 4/7