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

# cd ~/DAT8/project/qb_projections/data/temp/attempt_2
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

path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/temp/attempt_2'
#path =r'~/DAT8/project/qb_projections/data/temp/attempt_2'
years = range(2009, 2014)
dfs = []
for year in years:
    files = glob.glob(path + "/" + str(year) + "/*.csv")
    for file_ in files:
#        print str(file_)
        tempdf = pd.read_csv(file_)
        missing_col = list(frozenset(cols) - frozenset(tempdf.columns))
        if len(missing_col) > 0:
#            print missing_col
            included_col = list(frozenset(cols) - frozenset(missing_col))
#            print included_col
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
player_data.isnull().sum()
player_data['score'] = player_data.passing_yds * .04 + player_data.passing_tds * 4 + player_data.rushing_yds * .1 + player_data.rushing_tds * 6 - player_data.fumbles_lost * 2 - player_data.passing_ints * 2

import seaborn as sns
cols.append('score')
sns.heatmap(player_data[cols].corr())


# cd ~/Desktop/DAT8/project/qb_projections/data/lines_csv
#path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\lines_csv'
#path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/lines_csv'
#allFiles = glob.glob(path + "/*.csv")
#
#dfLines = []
#for file_ in allFiles:
#    dfLines.append(pd.read_csv(file_))
#    
#bigDfLines = pd.concat(dfLines, ignore_index=True)
#bigDfLines.dtypes
#del bigDfLines['Unnamed: 7']
#bigDfLines.isnull().sum()
#del bigDfLines['Total Line']
#del bigDfLines['Total Line ']
#bigDfLines['year'] = bigDfLines.Date.str[-4:].astype(int)
#bigDfLines.Line.hist()
#bigDfLines = bigDfLines[bigDfLines.year >= 2009]

#bigDfLines[bigDfLines.year >= 2009].groupby('year').Line.boxplot()
#bigDfLines.boxplot(column='Line', by='year')

#train['vtype_int'] = train['vtype'].map({'car':0, 'truck':1})
import numpy as np
#long_names = np.sort(bigDfLines.Visitor.unique())

#bigDfLines['home_team'] = bigDfLines['Home Team'].map(dict_names)
#bigDfLines['visitor'] = bigDfLines['Visitor'].map(dict_names)
#del bigDfLines['Home Team']
#del bigDfLines['Visitor']
#del bigDfLines['Home Score']
#del bigDfLines['Visitor Score']
#bigDfLines[]

#player_data['team'] = ''
#player_data.ix[player_data.home=='yes','team'] = player_data.home_team[player_data.home=='yes']
#player_data.ix[player_data.home!='yes','team'] = player_data.visitor[player_data.home!='yes']

#dfAll = pd.merge(player_data, bigDfLines)

# cd ~/Desktop/DAT8/project/qb_projections/data/stats_csv
#path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\stats_csv'
path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/stats_csv'
allFiles = glob.glob(path + "/*.csv")

dfStats = []
for file_ in allFiles:
    dfStats.append(pd.read_csv(file_))
    
team_data = pd.concat(dfStats, ignore_index=True)
team_data.dtypes
#del team_data['Unnamed: 30']
#del team_data['Unnamed: 33']
del team_data['Unnamed: 35']
team_data['year'] = team_data.Date.str[-4:]
team_data.head()

long_names = np.sort(team_data.TeamName.unique())
short_names = np.sort(player_data.visitor.unique())

dict_names = dict(zip(long_names, short_names))
dict_names['Seattle Seahawks'] = 'SEA'
dict_names['San Francisco 49ers'] = 'SF'

#team_data.head()
#len(team_data.TeamName.unique())
#team_names = team_data.TeamName.unique()
#dict_map = dict(zip(team_names,range(0, len(team_names))))
#team_data['team_int'] = team_data.TeamName.map(dict_map)
team_data['team'] = team_data['TeamName'].map(dict_names)

team_data.isnull().sum()

team_data['home_team'] = ''
team_data.ix[team_data.Site=='H','home_team'] = team_data.team[team_data.Site=='H']
team_data.ix[team_data.Site!='H','home_team'] = team_data.Opponent[team_data.Site!='H'].map(dict_names)

team_data['visitor'] = ''
team_data.ix[team_data.Site!='H','visitor'] = team_data.team[team_data.Site!='H']
team_data.ix[team_data.Site=='H','visitor'] = team_data.Opponent[team_data.Site=='H'].map(dict_names)

merge_cols = ['team','year','home_team','visitor']
team_data[merge_cols] = team_data[merge_cols].astype(str)
player_data[merge_cols] = player_data[merge_cols].astype(str)
team_data.year = team_data.year.astype(int)
player_data.year = player_data.year.astype(int)

dfAll = pd.merge(player_data, team_data, on=merge_cols)

gameId = dfAll[['year', 'home_team', 'visitor']].drop_duplicates()
gameId['gameId'] = range(0,gameId.shape[0])

dfAll = pd.merge(dfAll, gameId, on=['year','home_team','visitor'])

team_data['paydof'] = team_data.PassYdsOff.astype(int)

team_data.plot(kind='scatter', x='paydof', y='ScoreDef')

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import cm
#dir(cm)

plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['font.size'] = 14
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
team_data.plot(kind='scatter', x='ScoreDef', y='ScoreOff', c='team_int', alpha=.3, colormap='spectral')
team_data['ScoreDelta'] = team_data.ScoreOff-team_data.ScoreDef

test = team_data.groupby(['year','team_int']).ScoreDelta.mean().reset_index()
test['year_int'] = test.year.astype(int)
test['team_int'] = test.team_int.astype(int)

test.plot(kind='scatter', x='year_int',y='ScoreDelta',
c='team_int', alpha=.3, colormap='spectral')

