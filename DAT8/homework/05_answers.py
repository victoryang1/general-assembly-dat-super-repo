# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 18:52:49 2015

@author: vyang91
"""
# %reset
# cd ~/Desktop/DAT8/data

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)
plt.style.use('ggplot')

movies = pd.read_csv('imdb_1000.csv')

# 979 rows, 6 columns
movies.shape

# star rating is a column of floats
# duration is a column of ints
# title, content rating, genre, and actors list are objects
movies.dtypes

# average movie duration is a little over 2 hours
round(movies.duration.mean(), 2)

# 5 shortest and 5 longest movies
movies.sort('duration').head()
movies.sort('duration', ascending=0).head()

# histogram of movie durations using default bin amounts
movies.duration.plot(kind='hist')
plt.xlabel('Movie Duration (mins)')
plt.ylabel('Count')

# boxplot of movie durations
movies.boxplot(column='duration')

# count of each content rating
movies.content_rating.value_counts(dropna=0)

# bar plot of value counts
movies.content_rating.value_counts(dropna=0).plot(kind='bar')
plt.xlabel('Content Rating')
plt.ylabel('Count')

# convert 'not rated', 'approved', 'passed', 'gp' to 'unrated'
movies.loc[movies.content_rating.isin(
    ['NOT RATED', 'APPROVED', 'PASSED', 'GP']), 'content_rating'] = 'UNRATED'

# convert 'x', 'tv-ma' to 'nc-17'
movies.loc[movies.content_rating.isin(
    ['X', 'TV-MA']), 'content_rating'] = 'NC-17'

# count missing values in each column
movies.isnull().sum()

# examine movies with null content rating
movies[movies.content_rating.isnull()]
# originally rated US:M, now considered PG
# (https://en.wikipedia.org/wiki/Motion_Picture_Association_of_America_film_rating_system#From_M_to_GP_to_PG)
movies.loc[movies.content_rating.isnull(), 'content_rating'] = 'PG'

# 7.95 average rating for movies >= 2 hours vs. 7.84 rating for movies < 2
# hours
round(movies[movies.duration >= 120].star_rating.mean(), 2)
round(movies[movies.duration < 120].star_rating.mean(), 2)

# scatter plot of duration vs. star rating seems to indicate some
# relationship between the two
movies.plot(kind='scatter', x='duration', y='star_rating', alpha=.3)

# average durations for each genre, also sorted by length descending
movies.groupby('genre').duration.mean()
movies.groupby('genre').duration.agg(['mean']).sort('mean', ascending=0)

# boxplots of movie durations by content rating
movies.boxplot(column='duration', by='content_rating')

# highest star rated movie for each genre
movies = movies.sort('star_rating', ascending=0)
movies[~movies.genre.duplicated()]
# compare with
genre_max = movies.groupby('genre').star_rating.agg(
    ['max']).sort(
        'max', ascending=0)
genre_max['genre'] = genre_max.index.values
pd.merge(
    genre_max, movies, left_on=[
        'genre', 'max'], right_on=[
            'genre', 'star_rating']).sort(
                'star_rating', ascending=0)

# movies with duplicated titles sorted alphabetically then by star rating;
# they appear to be distinct movies
movies[movies.title.isin(movies[movies.title.duplicated()].title.tolist())].sort(
    ['title', 'star_rating'], ascending=[1, 0])

# identify genres with count >= 10 then subset dataframe and find grouped means
top_genre = movies.genre.value_counts() >= 10
top_genre = top_genre[top_genre == 1].index
movies[movies.genre.isin(top_genre)].groupby('genre').star_rating.mean()
movies[movies.genre.isin(top_genre)].groupby(
    'genre').star_rating.agg(['mean']).sort('mean', ascending=0)


# BONUS
import numpy as np
import statsmodels as sm

# clean actors list
actors = movies.actors_list.tolist()
actors = [
    actor.replace(
        '[',
        '').replace(
            'u\'',
            '').replace(
                'u\"',
                '').replace(
                    '\'',
                    '').replace(
                        '\"',
                        '').replace(
                            ']',
        '') for actor in actors]
actors = [actor.split(', ') for actor in actors]
test = [len(i) for i in actors]
# check that each list is made of three actors
float(sum(test)) / len(test) == 3.0

# which actor appears the most in the top 3 actors list of top 1000 movies
actors_flat = [item for sublist in actors for item in sublist]
from collections import Counter
actors_count = Counter(actors_flat)
actors_count.most_common(5)

actors_sorted = [sorted(actor_sub) for actor_sub in actors]

# which actor has the highest average rating in the top 1000 movies
#movies['actors_list_clean'] = actors
#movies['actors_clean_str'] = [', '.join(actor) for actor in actors]

movies['actors'] = actors_sorted
movies['actor_1'] = [actor[0] for actor in actors_sorted]
movies['actor_2'] = [actor[1] for actor in actors_sorted]
movies['actor_3'] = [actor[2] for actor in actors_sorted]

# super hackish stack attempt; didn't figure out hierarchical column
# labels to use pd.DataFrame.stack()
movies_new = movies.drop('actors_list', 1)
movies_one = movies_new.drop(['actor_2', 'actor_3'], 1).rename(
    columns={'actor_1': 'actor'})
movies_two = movies_new.drop(['actor_1', 'actor_3'], 1).rename(
    columns={'actor_2': 'actor'})
movies_three = movies_new.drop(['actor_1', 'actor_2'], 1).rename(
    columns={'actor_3': 'actor'})
movies_all = pd.concat([movies_one, movies_two, movies_three], axis=0)

# top actors by appearance in imdb 1000, mean, and median
movies_all.groupby('actor').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['count', 'mean', 'median'], ascending=[0, 0, 0]).head()
movies_all.groupby('actor').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['mean', 'count', 'median'], ascending=[0, 0, 0]).head()
movies_all.groupby('actor').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['median', 'count', 'mean'], ascending=[0, 0, 0]).head()

# distribution of actors and their appearances in the imdb 1000; most are
# in just 1 film
ecdf = sm.tools.tools.ECDF(movies_all.actor.value_counts())
x = np.linspace(min(movies_all.actor.value_counts()),
                max(movies_all.actor.value_counts()))
y = ecdf(x)
plt.step(x, y)

# three or more films puts an actor in the 86th percentile
top_actor = movies_all.actor.value_counts() >= 3
top_actor = top_actor[top_actor == 1].index
round(float(len(top_actor)) / movies_all.actor.nunique(), 2)

# recalculate top top actors by mean and median star rating
movies_all[movies_all.actor.isin(top_actor)].groupby('actor').star_rating.agg(
    ['count', 'mean', 'median', 'min', 'max']).sort(['mean', 'count', 'median'], ascending=[0, 0, 0]).head()
movies_all[movies_all.actor.isin(top_actor)].groupby('actor').star_rating.agg(
    ['count', 'mean', 'median', 'min', 'max']).sort(['median', 'count', 'mean'], ascending=[0, 0, 0]).head()

# top top actors' appearances in each genre
movies_all[movies_all.actor.isin(top_actor)].groupby(
    'genre').actor.value_counts()
# top actors in each genre
movies_all.groupby('genre').actor.value_counts()[
    movies_all.groupby('genre').actor.value_counts() > 2]

# which two actors work together the most often in top 1000 movies; the
# harry potter trio appears the most; highest rated pairs are LotR and
# Star Wars
movies_pair_all = pd.Series(
    pd.concat(
        [
            movies_new.actor_1 +
            ', ' +
            movies_new.actor_2,
            movies_new.actor_1 +
            ', ' +
            movies_new.actor_3,
            movies_new.actor_2 +
            ', ' +
            movies_new.actor_3],
        axis=0),
    name='pair')
movies_all = pd.concat([movies_all, movies_pair_all], axis=1)
movies_all.pair.value_counts()[movies_all.pair.value_counts() > 2]

movies_all.groupby('pair').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['count', 'mean', 'median'], ascending=[0, 0, 0]).head()
movies_all.groupby('pair').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['mean', 'count', 'median'], ascending=[0, 0, 0]).head()
movies_all.groupby('pair').star_rating.agg(['count', 'mean', 'median', 'min', 'max']).sort(
    ['median', 'count', 'mean'], ascending=[0, 0, 0]).head()

top_pair = movies_all.pair.value_counts() >= 2
top_pair = top_pair[top_pair == 1].index
movies_all[movies_all.pair.isin(top_pair)].groupby('pair').star_rating.agg(
    ['count', 'mean', 'median', 'min', 'max']).sort(['mean', 'count', 'median'], ascending=[0, 0, 0]).head()
movies_all[movies_all.pair.isin(top_pair)].groupby('pair').star_rating.agg(
    ['count', 'mean', 'median', 'min', 'max']).sort(['median', 'count', 'mean'], ascending=[0, 0, 0]).head()
