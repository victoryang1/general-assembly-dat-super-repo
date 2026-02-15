# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 04:01:34 2015

@author: yang
"""

# pip install nflgame
# conda install seaborn

#import nflgame
import glob
import pandas as pd

# cd ~/DAT8/project/qb_projections/data #/temp/attempt_2
#games_all = nflgame.games(range(2009, 2014), kind='REG')

# cd ~/Desktop/DAT8/project/qb_projections/data/temp/attempt_2/2014
# games_all = nflgame.games(2013)
#for game in games_all:
#    p = game.players.filter(passing_att=lambda x:x>1).csv('%s.csv' % game)
#    p = game.players.filter(passing_att=lambda x:x>0).csv('%s.csv' % game.gamekey)


cols = ['name','home','team','pos','passing_att','passing_cmp',
'passing_ints','passing_tds','passing_twopta','passing_twoptm','passing_yds',
'rushing_att', 'rushing_tds', 'rushing_twopta', 'rushing_twoptm', 'rushing_yds',
'fumbles_lost'
]

#path =r'/Users/lindenthetree/DAT8/project/qb_projections/data'
path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/temp/attempt_2'
years = range(2009, 2014)
dfs = []
for year in years:
    files = glob.glob(path + "/" + str(year) + "/*.csv")
    for file_ in files:
        tempdf = pd.read_csv(file_)
        missing_col = list(frozenset(cols) - frozenset(tempdf.columns))
        if len(missing_col) > 0:
            included_col = list(frozenset(cols) - frozenset(missing_col))
            tempdf = tempdf[included_col]
            for col in missing_col:
                tempdf[col] = 0
        else:
            tempdf = tempdf[cols]
        tempdf = tempdf.fillna(0)
        tempdf['year'] = year
        home_team = tempdf.team[tempdf.home == 'yes'].unique().repeat(tempdf.shape[0])
        visitor = tempdf.team[tempdf.home == 'no'].unique().repeat(tempdf.shape[0])
        tempdf['home_team'] = home_team
        tempdf['visitor'] = visitor
        dfs.append(tempdf)

player_data = pd.concat(dfs, ignore_index=True)
player_data = player_data[player_data.pos=='QB']
player_data.isnull().sum()
player_data['score'] = player_data.passing_yds * .04 + player_data.passing_tds * 4 + player_data.rushing_yds * .1 + player_data.rushing_tds * 6 - player_data.fumbles_lost * 2 - player_data.passing_ints * 2

import seaborn as sns
#cols.append('score')
#sns.heatmap(player_data[cols].corr())

import numpy as np
path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/stats_csv'
allFiles = glob.glob(path + "/*.csv")

dfStats = []
for file_ in allFiles:
    dfStats.append(pd.read_csv(file_))
    
team_data = pd.concat(dfStats, ignore_index=True)
#team_data.dtypes
del team_data['Unnamed: 35']
team_data['year'] = team_data.Date.str[-4:]
team_data.head()

long_names = np.sort(team_data.TeamName.unique())
short_names = np.sort(player_data.visitor.unique())

dict_team_id_name = dict(zip(long_names, short_names))
dict_team_id_name['Seattle Seahawks'] = 'SEA'
dict_team_id_name['San Francisco 49ers'] = 'SF'

team_data['team'] = team_data['TeamName'].map(dict_team_id_name)

team_data.isnull().sum()

team_data['home_team'] = ''
team_data.ix[team_data.Site=='H','home_team'] = team_data.team[team_data.Site=='H']
team_data.ix[team_data.Site!='H','home_team'] = team_data.Opponent[team_data.Site!='H'].map(dict_team_id_name)

team_data['visitor'] = ''
team_data.ix[team_data.Site!='H','visitor'] = team_data.team[team_data.Site!='H']
team_data.ix[team_data.Site=='H','visitor'] = team_data.Opponent[team_data.Site=='H'].map(dict_team_id_name)

merge_cols = ['team','year','home_team','visitor']
team_data[merge_cols] = team_data[merge_cols].astype(str)
player_data[merge_cols] = player_data[merge_cols].astype(str)
team_data.year = team_data.year.astype(int)
player_data.year = player_data.year.astype(int)

dfAll = pd.merge(player_data, team_data, on=merge_cols)

gameId = dfAll[['year', 'Date', 'home_team', 'visitor']].drop_duplicates()
gameId['month'] = gameId.ix[:,'Date'].str[0:2].astype(int)
gameId['date'] = gameId.ix[:,'Date'].str[3:5].astype(int)
gameId['datetime'] = pd.to_datetime(gameId['Date'])
del gameId['Date']
gameId.sort_values(by='datetime', inplace=True)
gameId['season'] = gameId['year']
gameId.ix[gameId.month < 9,'season'] = gameId.season - 1
gameId['week'] = gameId['datetime'].dt.week
gameId['week'] = gameId['week'] - 35
gameId.ix[gameId.season==2009,'week'] = gameId.week[gameId.season==2009]-1
#gameId[['season','week']].drop_duplicates().season.value_counts()
gameId.reset_index(inplace=True, drop=True)
gameId['gameId'] = range(0,gameId.shape[0])
gameCols = gameId.columns.tolist()

dfAll2 = pd.merge(dfAll, gameId, on=['year','home_team','visitor'])
#dfAll2.ix[0,:]
dfAll2['TimePossOff'] = dfAll2.TimePossOff.str[0:2].astype(float)+dfAll2.TimePossOff.str[3:5].astype(float)/60
dfAll2.home = dfAll2.home.map({'yes':1, 'no':0})
dict_team_id = dict(zip(sorted(list(set(dfAll2.team))),range(0,32)))
dict_player_id = dict(zip(sorted(list(set(dfAll2.name))),range(0,len(set(dfAll2.name)))))
dfAll2['team_int'] = dfAll2.team.map(dict_team_id)
dfAll2['player_id'] = dfAll2.name.map(dict_player_id)

cols = ['gameId', 'team_int', 'player_id', 'season', 'week', 'fumbles_lost', 'passing_att', 'passing_cmp', 'passing_ints', 'passing_tds',
'passing_twopta', 'passing_twoptm', 'passing_yds', 'rushing_att', 'rushing_tds', 'rushing_twopta',
'rushing_twoptm', 'rushing_yds', 'year', 'FirstDownOff', 'SackNumOff',
'PenYdsOff', 'TimePossOff', 'FirstDownDef', 'PenYdsDef', 'home', 'Line', 'TotalLine', 'score']

#dfAll2.ThirdDownPctOff = dfAll2.ThirdDownPctOff.dfAll.ThirdDownPctOff = dfAll.ThirdDownPctOff.str.extract('(\d)').astype(int)
dfRollingAll = dfAll2[cols]
dfRollingAll.sort_values(by=['team_int', 'player_id', 'gameId', 'season', 'week'], inplace=True)

feature_cols = cols[1:-1]

dfTest = dfRollingAll[feature_cols]
dfTest = dfTest.groupby(['team_int', 'player_id'])[feature_cols].apply(pd.expanding_mean)
dfTest.drop(dfTest.columns[-3:], axis=1, inplace=True)
newTestnames = dfTest.columns[4:].tolist()
dfTest.columns = dfTest.columns[0:4].tolist() + [i + '_all' for i in newTestnames]

dfRolling5 = dfAll2[cols]
dfRolling5.sort_values(by=['team_int', 'player_id', 'gameId', 'season', 'week'], inplace=True)

feature_cols = cols[1:-1]

dfTest2 = dfRolling5[feature_cols]
dfTest2 = dfTest2.groupby(['team_int', 'player_id'])[feature_cols].apply(pd.rolling_mean, 5)
dfTest2.drop(dfTest2.columns[-3:], axis=1, inplace=True)
newTest2names = dfTest2.columns[4:].tolist()
dfTest2.columns = dfTest2.columns[0:4].tolist() + [i + '_5' for i in newTest2names]

dfTest2.dropna(inplace=True)

dfAll3 = pd.merge(dfAll2[['score', 'team_int','player_id','gameId','season','week', 'home', 'Line', 'TotalLine']], dfTest)

from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
X = dfAll3.ix[:,4:]
y = dfAll3.ix[:,0]

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

linreg.fit(X_train, y_train)
y_pred = linreg.predict(X_test)

from sklearn import metrics
np.sqrt(metrics.mean_squared_error(y_test, y_pred))

zip(dfAll3.columns[4:], linreg.coef_)

import matplotlib.pyplot as plt
y_all = linreg.predict(X)
plt.scatter(dfAll3.score, y_all)

from sklearn.metrics import r2_score
r2_score(dfAll3.score, y_all)


#
#
#team_data['paydof'] = team_data.PassYdsOff.astype(int)
#
#team_data.plot(kind='scatter', x='paydof', y='ScoreDef')
#
#import matplotlib.pyplot as plt
#from matplotlib.colors import ListedColormap
#from matplotlib import cm
##dir(cm)
#
#plt.rcParams['figure.figsize'] = (6, 4)
#plt.rcParams['font.size'] = 14
#cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
#team_data.plot(kind='scatter', x='ScoreDef', y='ScoreOff', c='team_int', alpha=.3, colormap='spectral')
#team_data['ScoreDelta'] = team_data.ScoreOff-team_data.ScoreDef
#
#test = team_data.groupby(['year','team_int']).ScoreDelta.mean().reset_index()
#test['year_int'] = test.year.astype(int)
#test['team_int'] = test.team_int.astype(int)
#
#test.plot(kind='scatter', x='year_int',y='ScoreDelta',
#c='team_int', alpha=.3, colormap='spectral')
#
