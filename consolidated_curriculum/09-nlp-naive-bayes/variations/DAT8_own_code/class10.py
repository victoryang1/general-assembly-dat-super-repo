# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 18:55:22 2015

@author: yang
"""

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import linear_model, metrics
import numpy as np

plt.rcParams['figure.figsize'] = (13, 10)

url = 'https://github.com/justmarkham/DAT8/raw/master/data/bikeshare.csv'
bikes = pd.read_csv(url, index_col='datetime', parse_dates=True)

bikes.rename(columns={'count':'total'}, inplace=True)


bikes.plot(kind='scatter', x='temp', y='total', alpha=.1)
sns.lmplot(x='temp', y='total', data=bikes, aspect=1.5, scatter_kws={'alpha':.1})

feature_cols = ['temp']
X = bikes[feature_cols]
y = bikes.total

linreg = linear_model.LinearRegression()
linreg.fit(X, y)

print linreg.intercept_
print linreg.coef_

feature_cols = ['temp', 'season', 'weather', 'humidity']
sns.pairplot(bikes, x_vars=feature_cols, y_vars='total', kind='reg')

fig, axs = plt.subplots(1, len(feature_cols), sharey=True)
for index, feature in enumerate(feature_cols):
    bikes.plot(kind='scatter', x=feature, y='total', ax=axs[index], figsize=(16, 3))
    
pd.crosstab(bikes.season, bikes.index.month)
bikes.boxplot(column='total', by='season')
bikes.total.plot()
#bikes.reset_index().total.plot()

bikes.corr()
sns.heatmap(bikes.corr())

feature_cols = ['temp', 'season', 'weather', 'humidity']
X = bikes[feature_cols]
y = bikes.total

# instantiate and fit
linreg = linear_model.LinearRegression()
linreg.fit(X, y)

# print the coefficients
print linreg.intercept_
print linreg.coef_

zip(feature_cols, linreg.coef_)

min(bikes.index)
max(bikes.index)

bikes.plot(kind='scatter', x='season', y='temp')

actual = [10, 7, 5, 5]
pred = [8, 6, 5, 10]

dfTest = pd.concat([pd.Series(actual, name='actual'), pd.Series(pred, name='pred')], axis=1)
np.mean(abs(dfTest.actual-dfTest.pred))
np.mean((dfTest.actual-dfTest.pred)**2)
np.sqrt(np.mean((dfTest.actual-dfTest.pred)**2))

metrics.mean_absolute_error(actual, pred)
metrics.mean_squared_error(actual, pred)
np.sqrt(metrics.mean_squared_error(actual, pred))

from sklearn.cross_validation import train_test_split

def train_test_rmse(feature_cols):
    X = bikes[feature_cols]
    y = bikes.total
    X_train, X_test, Y_train, y_test = train_test_split(X, y, random_state=123)
    linreg.fit(X, y)
    y_pred = linreg.predict(X_test)
    return np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    

train_test_rmse(['temp', 'season', 'humidity'])

season_dummies = pd.get_dummies(bikes.season, prefix='season')
season_dummies.drop(season_dummies.columns[0], axis=1, inplace=True)
bikes = pd.concat([bikes, season_dummies], axis=1)

train_test_rmse(['temp', 'season', 'humidity'])
train_test_rmse(['temp', 'season_2', 'season_3', 'season_4', 'humidity'])

bikes['hour'] = bikes.index.hour
hour_dummies = pd.get_dummies(bikes.hour, prefix='hour')
hour_dummies.drop(hour_dummies.columns[0], axis=1, inplace=True)
bikes = pd.concat([bikes, hour_dummies], axis=1)


