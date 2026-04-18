# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:33:51 2015

@author: user
"""

import pandas as pd
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/titanic.csv'
titanic = pd.read_csv(url, index_col='PassengerId')

titanic.shape
titanic.isnull().sum()
titanic.dropna().shape
titanic[titanic.Age.notnull()].shape

titanic.Age.fillna(titanic.Age.median(), inplace=True) # could also be mean, mode, or knn neighbor

titanic['Sex_Female'] = titanic.Sex.map({'male':0, 'female':1})

embarked_dummies = pd.get_dummies(titanic.Embarked, prefix='Embarked')
embarked_dummies.drop(embarked_dummies.columns[0], axis=1, inplace=True)
titanic = pd.concat([titanic, embarked_dummies], axis=1)

feature_cols = ['Pclass', 'Parch', 'Age', 'Sex_Female', 'Embarked_Q', 'Embarked_S']
X = titanic[feature_cols]
y = titanic.Survived

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e9)
logreg.fit(X_train, y_train)
y_pred_class = logreg.predict(X_test)

from sklearn import metrics
print metrics.accuracy_score(y_test, y_pred_class)

y_pred_prob = logreg.predict_proba(X_test)[:, 1]


import matplotlib.pyplot as plt

# plot ROC curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_prob)
plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
print metrics.roc_auc_score(y_test, y_pred_prob)

df = pd.DataFrame({'probability':y_pred_prob, 'actual':y_test})
df.hist(column='probability', by='actual', sharex=True, sharey=True)

###

from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


# read in the iris data
iris = load_iris()

# create X (features) and y (response)
X = iris.data
y = iris.target

# use train/test split with different random_state values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)

# check classification accuracy of KNN with K=5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print metrics.accuracy_score(y_test, y_pred)


from sklearn.cross_validation import cross_val_score


# 10-fold cross-validation with K=5 for KNN (the n_neighbors parameter)
knn = KNeighborsClassifier(n_neighbors=5)
scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
print scores

###
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/bank-additional.csv'
data = pd.read_csv(url, delimiter=';')
data.isnull().sum()
data['target'] = data[['y']].astype(str)
data['target'].unique()
data['target_int'] = data['target'].map({'no':0, 'yes':1})
plt.rcParams['figure.figsize'] = (12, 12)
#axes = pd.tools.plotting.scatter_matrix(data)

data['education'].unique()
education_dummies = pd.get_dummies(data.education, prefix='education')
education_dummies.drop(education_dummies.columns[0], axis=1, inplace=True) # basic 4y is base
data = pd.concat([data, education_dummies], axis=1)


data['default'].unique()
default_dummies = pd.get_dummies(data.default, prefix='default')
default_dummies.drop(default_dummies.columns[0], axis=1, inplace=True) # no is base
data = pd.concat([data, default_dummies], axis=1)

feature_cols = list(education_dummies.columns) + list(default_dummies.columns)
X = data[feature_cols]
y = data.target_int




