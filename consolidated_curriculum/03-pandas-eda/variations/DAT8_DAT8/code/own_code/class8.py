# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 18:32:13 2015

@author: user
"""

# cd ~/Desktop/DAT8/code

import pandas as pd
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['font.size'] = 14
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

df = df.head()

def shape_types(obj):
    print(type(obj))
    print(obj.shape)

obj_list = [df, df.continent, df['continent'], df[['continent']], df[['continent', 'country']], df[[False, True, False, True, False]], df[[]]]

for obj in obj_list:
    shape_types(obj)
    
df.ix[:,[False, True, False, True, False, True]]
df.ix[:,[False, True, False, True, False, False]]
df.ix[:,[False, True, False, True, False]]
df.ix[[False, True, False, True, False],:]

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
iris = pd.read_csv(url, header=None, names=col_names)
iris['species_num'] = iris.species.map({'Iris-setosa':0, 'Iris-versicolor':1, 'Iris-virginica':2})
iris.plot(kind='scatter', x='petal_length', y='petal_width', c='species_num', colormap=cmap_bold)
iris.plot(kind='scatter', x='sepal_length', y='sepal_width', c='species_num', colormap=cmap_bold)

feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
X = iris[feature_cols]

X = iris.drop(['species', 'species_num'], axis=1)
X = iris.loc[:, 'sepal_length':'petal_width']
X = iris.iloc[:, 0:4]

y = iris.species_num

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
type(knn)

mylist = [1, 2, 3]
type(mylist)

knn.fit(X, y)
knn.predict([3, 5, 4, 2])

X_new = [[3, 5, 4, 2], [5, 4, 3, 2]]
knn.predict(X_new)

knn = KNeighborsClassifier(n_neighbors=5, weights = 'distance')
knn.fit(X, y)
knn.predict(X_new)

knn.predict_proba(X_new)

from sklearn import neighbors #, datasets
#import numpy as np
n_neighbors = 15

X = iris.loc[:, ['petal_length', 'petal_width']].values
X = iris.loc[:, ['sepal_length', 'sepal_width', 'petal_length']].values
y = iris.species_num
h = .02

cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

#for weights in ['uniform', 'distance']:
#    # we create an instance of Neighbours Classifier and fit the data.
#    weights = 'distance'
#    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
#    clf.fit(X, y)
#
#    # Plot the decision boundary. For that, we will assign a color to each
#    # point in the mesh [x_min, m_max]x[y_min, y_max].
#    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#    z_min, z_max = X[:, 2].min() - 1, X[:, 1].max() + 1
#    xx0, yy0 = np.meshgrid(np.arange(x_min, x_max, h),
#                         np.arange(y_min, y_max, h))
#    xx, yy, zz = np.meshgrid(np.arange(x_min, x_max, h),
#                             np.arange(y_min, y_max, h),
#                             np.arange(z_min, z_max, 2 * h),
#                             indexing='ij')
#                             
#    xx2 = xx.reshape(xx.shape[0] * xx.shape[2], xx.shape[1])
#    yy2 = yy.reshape(yy.shape[0] * yy.shape[2], yy.shape[1])
#    zz2 = zz.reshape(zz.shape[0] * zz.shape[2], zz.shape[1])
#    
#    Z = clf.predict(np.c_[xx0.ravel(), yy0.ravel()])
#    pred = clf.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])
#    # Z_fail = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#    
#
#    # Put the result into a color plot
#    Z = Z.reshape(xx0.shape)
#
#    plt.figure()
##    plt.pcolormesh(xx2, yy2, Z, cmap=cmap_light)
#    
#    pred2 = pred.reshape(zz.shape)
#    
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    ax.scatter(xx.flatten()[0:100], yy.flatten()[0:100], zz.flatten()[0:100], c=pred2.flatten()[0:100])    
#    
#    N = zz2/zz2.max()
#
#    from mpl_toolkits.mplot3d import Axes3D
#    from matplotlib import cm
#
#    fig = plt.figure()
#    ax = fig.gca(projection='3d')
#    
#    Axes3D.scatter(xx.flatten(), yy.flatten(), zz.flatten())
#
#    surf = ax.plot_surface(
#    xx2[0:100], yy2[0:100], zz2[0:100], rstride=1, cstride=1,
#    facecolors=cm.jet(N),
#    linewidth=0, antialiased=False, shade=False)
#
#    # Plot also the training points
#    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
#    plt.xlim(xx.min(), xx.max())
#    plt.ylim(yy.min(), yy.max())
#    plt.title("3-Class classification (k = %i, weights = '%s')"
#              % (n_neighbors, weights))
#
#plt.show()

### nba stuff
players = pd.read_csv('https://raw.githubusercontent.com/justmarkham/DAT4-students/master/kerry/Final/NBA_players_2015.csv')
players.drop('Unnamed: 0', 1, inplace=True)

feature_cols = ['ast', 'stl', 'blk', 'tov', 'pf']
X = players[feature_cols].values
y = players.pos
clf = neighbors.KNeighborsClassifier(50, weights='distance')
clf.fit(X, y)

test = [1, 1, 0, 1, 2]
clf.predict(test)
clf.predict_proba(test)

players['pos_num'] = players.pos.map({'F': 0, 'G':1, 'C':2})

plt.rcParams['figure.max_open_warning'] = 100

diff_features = []
diff_threshold = 2
for icolumn in players.columns[7:-1]:
    try:
        imeans = players[[icolumn, 'pos_num']].groupby('pos_num').mean()
        f_mean = float(imeans.ix[0,:])
        g_mean = float(imeans.ix[1,:])
        c_mean = float(imeans.ix[2,:])
        if (bool(abs(f_mean - g_mean)/abs(g_mean) > diff_threshold) | bool(abs(c_mean - g_mean)/abs(c_mean) > diff_threshold) | bool(abs(f_mean - c_mean)/abs(c_mean) > diff_threshold)):
            print(round(max(abs(f_mean - g_mean)/abs(g_mean), abs(c_mean - g_mean)/abs(c_mean), abs(f_mean - c_mean)/abs(c_mean)), 2))
            print(icolumn)
            diff_features.append(icolumn)
            #plt.figure()
            #players.boxplot(column=icolumn, by='pos')
    except:
        print('Fail on', icolumn)
        pass

round(float(len(diff_features))/len(players.columns[7:-1]), 2)
print(diff_features)

for i in diff_features:
    plt.figure()
    players.boxplot(column=i, by='pos')

for i in range(0, len(diff_features)):
    print(players.groupby('pos')[diff_features[i]].mean())

