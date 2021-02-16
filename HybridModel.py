# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:09:29 2021

@author: Debangan Daemon
"""
#Import a few basic modules
import pandas as pd
from tabulate import tabulate

# Import Torch
from torch.utils.data import DataLoader

# Custom Scripts
import TopAnime
import AnimeClusters
from UserVector import UserVector
from PredictionEngine import PredictionEngine

# Get similar anime
def similarAnime(uratings, all_anime):

    if len(uratings) == 0:
        ani_genre = pd.read_csv("anime_genres.csv", index_col=[0])

        TopAnime.top_animes('Shounen', ani_genre, all_anime)
        TopAnime.top_animes('Supernatural', ani_genre, all_anime)
        TopAnime.top_animes('Romance', ani_genre, all_anime)
        TopAnime.top_animes('Slice of Life', ani_genre, all_anime)

        return []

    else:
        temp = list(reversed(uratings.items()))
        SimilarAnime = []

        i = 0
        while i < len(temp) and i < 3:
            if temp[i][1] >= 6:
                SimilarAnime += AnimeClusters.getCluster(opposite=False)
            else:
                SimilarAnime += AnimeClusters.getCluster(opposite=True)

        return SimilarAnime

# Get Anime You May Like
def animeYouMayLike(age, gender, uratings, all_anime):

    # Load the AutoEncoder
    model = PredictionEngine()

    # User Data Column
    user_data = UserVector(age, gender, uratings)

    # User Data Loader
    user_dl = DataLoader(dataset=user_data, num_workers=1)

    # Get model Predictions
    preds = model.getPredictedRatings(user_data, user_dl)
    preds = preds.reshape(-1)

    # Get top predicted anime
    topN = list(preds.argsort()[-1000:][::-1])
    animes = list(map(user_data.get_anime_id, topN))

    # Get Similar Anime
    SimilarAnime = similarAnime(uratings, all_anime)
    if len(SimilarAnime) == 0:
        return

    # Generate 'Similar Anime' and 'Anime You May Like'
    FinalList1 = []
    FinalList2 = []

    for aniID in animes:
        r = [aniID, all_anime['title'][aniID], all_anime['title_english'][aniID], all_anime['genre'][aniID]]

        if aniID in SimilarAnime and len(FinalList1) <=5:
            FinalList1.append(r)
        elif len(FinalList2) <=5:
            FinalList2.append(r)
        else:
            break

    return FinalList1, FinalList2

# Main Game
def showRecommendations(age, gender, uratings, all_anime):
    List1, List2 = animeYouMayLike(age, gender, uratings, all_anime)

    # Tabulate the Results
    print("similar Anime")
    table = tabulate(List1, headers=['Anime ID', 'JP Title', 'EN Title', 'Genre'], tablefmt='orgtbl')
    print(table)

    print("Anime You May Like")
    table = tabulate(List2, headers=['Anime ID', 'JP Title', 'EN Title', 'Genre'], tablefmt='orgtbl')
    print(table)