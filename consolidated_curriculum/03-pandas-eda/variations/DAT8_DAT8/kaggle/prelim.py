# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 03:12:00 2015

@author: victor
"""

# %reset
# cd ~/victor_dat8

import pandas as pd
import math

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

train = pd.read_csv('train.csv', index_col=0)
train.OpenStatus = train.OpenStatus.map({1:1, 0:-1})
train.to_csv('train_wc.csv', index=False)

train_wc = pd.read_csv('train_wc.csv')
# python extract.py train_wc.csv train_.csv
train_ = pd.read_csv('train_.csv')
# python csv2vw.py train_.csv train.vw
# vw --loss_function logistic -d train.vw -f model

test = pd.read_csv('test.csv', index_col=0)
test = test.reset_index()
test.to_csv('test_wc.csv', index=False)

test_wc = pd.read_csv('test_wc.csv')
test_ = pd.read_csv('test_.csv')
# vw -i model -t test.vw -p raw_predictions.txt

pred = pd.read_csv('raw_predictions.txt', sep=' ', header=None)
pred.rename(columns={0:'OpenStatus', 1:'id'}, inplace=True)
pred.OpenStatus = pred.OpenStatus.apply(sigmoid)
pred = pred[['id', 'OpenStatus']]
pred.to_csv('sub_copycat.csv', index=False)