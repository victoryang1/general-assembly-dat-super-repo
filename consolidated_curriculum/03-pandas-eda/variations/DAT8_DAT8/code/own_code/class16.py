# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 19:04:44 2015

@author: user
"""

# cd ~/Desktop/DAT8/data/so_kaggle

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (10, 8)

train = pd.read_csv('train.csv', index_col=0)
train_clean = pd.read_csv('train_.csv', index_col=0)

train.dtypes
train.OpenStatus.value_counts()
train.OwnerUserId.value_counts().head()

train[train.OwnerUserId == 466534].head()
train.groupby('OwnerUserId').OpenStatus.agg(['mean','count']).sort('count', ascending=0).head()
train.groupby('OpenStatus').ReputationAtPostCreation.describe().unstack()

# pd.scatter_matrix(train)

train[train.ReputationAtPostCreation < 1000].ReputationAtPostCreation.plot(kind='hist')
train.rename(columns={'OwnerUndeletedAnswerCountAtPostTime':'Answers'}, inplace=True)
train.groupby('OpenStatus').Answers.describe().unstack()

train['title_len'] = train.Title.apply(len)

def make_features(filename):
    df = pd.read_csv(filename, index_col=0, parse_dates=['OwnerCreationDate', 'PostCreationDate'])
    df.rename(columns={'OwnerUndeletedAnswerCountAtPostTime':'Answers'}, inplace=True)
    df['title_len'] = df.Title.apply(len)
    df['num_tags'] = df.loc[:,'Tag1':'Tag5'].notnull().sum(axis=1)
    df['poster_age'] = (df.PostCreationDate - df.OwnerCreationDate).dt.days
    df['poster_age'] = np.where(df.poster_age < 0, 0, df.poster_age)
    return df
    
train = make_features('train.csv')
test = make_features('test.csv')

feature_cols = ['ReputationAtPostCreation', 'Answers', 'title_len', 'num_tags', 'poster_age']
X = train[feature_cols]
y = train.OpenStatus

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e9)
logreg.fit(X_train, y_train)

logreg.coef_

y_pred_class = logreg.predict(X_test)
y_pred_prob = logreg.predict_proba(X_test)[:, 1]

from sklearn import metrics
metrics.accuracy_score(y_test, y_pred_class)
metrics.confusion_matrix(y_test, y_pred_class)

logreg.fit(X, y)
X_oos = test[feature_cols]
oos_pred_prob = logreg.predict_proba(X_oos)[:, 1]

###
submit = pd.DataFrame({'id':test.index, 'OpenStatus':oos_pred_prob}).set_index('id')
submit.to_csv('sub2.csv')
###

from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer()
dtm = vect.fit_transform(train.Title)

X = dtm
y = train.OpenStatus

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

vect = CountVectorizer(stop_words='english')
dtm = vect.fit_Transform(train.Title)


