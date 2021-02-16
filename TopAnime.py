# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:15:34 2021

@author: Debangan Daemon
"""
from tabulate import tabulate

# Find top animes of given genre
def top_animes(genre, ani_genre, all_anime):
    top = []
    print("\nTop", genre)
    temp = list(ani_genre[ani_genre[genre]==1]['anime_id'])
    temp.sort(key=lambda x: all_anime['score'][x], reverse=True)

    for i in range(5):
        r = [i+1, temp[i], all_anime['title'][temp[i]], all_anime['title_english'][temp[i]],
             all_anime['score'][temp[i]], all_anime['genre'][temp[i]]]
        top.append(r)

    table = tabulate(top, headers=['S.No.', 'Anime ID', 'Title', 'English Title',
                                   'Anime Score', 'Anime Genre'], tablefmt='orgtbl')
    print(table)