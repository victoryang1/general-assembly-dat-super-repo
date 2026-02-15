# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import requests
#import json
#from bs4 import BeautifulSoup
#import pandas as pd
import nflgame

games_all = nflgame.games(range(2009, 2016))
games2 = nflgame.games(range(2009, 2016), kind='REG')
len(games_all) #1553 when 2009-2015

players = nflgame.combine_game_stats(games_all)

for p in players.rushing().sort("rushing_yds").limit(10):
    print p, p.rushing_yds

# cd ~/Desktop/DAT8/project/qb_projections
nflgame.combine(games_all).csv('season2009_2015.csv')

test = games_all[1552]
test.players.filter(passing_yds=lambda x:x>0)
test.players.filter(pos=lambda x:x=='qb').csv('qb_test3.csv')
test.players.filter(passing_att=lambda x:x>5).csv('qb_test3.csv')

import sys
sys.stdout()

import nfldb
db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2013, season_type='Regular', week=17, team='NE')
q.play_player(team='NE')
pps = q.as_aggregate()
print sum(pp.rushing_yds for pp in pps)

#################################
import nflgame
import glob
import pandas as pd

# cd ~/Desktop/DAT8/project/qb_projections/data/temp/attempt_0
games_all = nflgame.games(range(2009, 2013))
#games2 = nflgame.games(2013)

#writer = csv.writer(sys.stdout)
#writer.writerow(['gamekey', 'full_name', 'pos', 'home', 'fumbles_lost', 'passing_att', 'passing_cmp', 'passing_ints', 'passing_tds',
#                 'passing_twopta', 'passing_twoptm', 'passing_yds', 'rushing_att', 'rushing_tds', 'rushing_twopta', 'rushing_twoptm',
#                 'rushing_yds', 'team'])

for game in games_all:
    p = game.players.filter(passing_att=lambda x:x>0).csv('%s.csv' % game.gamekey)
    
for game in games_all:
    game.players.filter(pos='QB')
#    game.players.filter(passing_yds=lambda x:x>0).csv('%s.csv' % game.gamekey)
    
path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\temp\attempt_0'
allFiles = glob.glob(path + "/*.csv")
len(allFiles)
dfs1 = []
for file_ in allFiles[0:len(allFiles)/4]:
    dfs1.append(pd.read_csv(file_))
    
dfs2 = []
for file_ in allFiles[len(allFiles)/4:len(allFiles)/2]:
    dfs2.append(pd.read_csv(file_))
    
dfs3 = []
for file_ in allFiles[len(allFiles)/2:3*len(allFiles)/4]:
    dfs3.append(pd.read_csv(file_))

dfs4 = []
for file_ in allFiles[3*len(allFiles)/4:len(allFiles)]:
    dfs4.append(pd.read_csv(file_))

dfs5 = pd.concat([dfs3[0], dfs4[0]])
dfs6 = pd.concat([dfs3[1], dfs4[1]])

cols = ['name','id','home','team','pos','passing_att','passing_cmp',
'passing_ints','passing_tds','passing_twopta','passing_twoptm','passing_yds',
]

test_frame = pd.concat(dfs1)
test_frame[cols]
    
big_frame = pd.concat(dfs, ignore_index=True)
frame = pd.concat(list_)


for df in dfs:
    df_max 