# -*- coding: utf-8 -*-

# Remove Warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Import a few basic modules
import pandas as pd
from collections import OrderedDict

# Custom Scripts
import HybridModel
from PredictionEngine import PredictionEngine

# Search anime in database
def find_anime(input_anime, name_to_id):
    print('Anime Id', '\t', 'Title')
    for n in name_to_id.index:
        if input_anime in n.lower():
            print(name_to_id[n], '\t', n)

# Main Function
def main():

    # Load all the datasets
    all_anime = pd.read_csv("anime_cleaned.csv")
    name_to_id = pd.Series(list(all_anime['anime_id']), index=all_anime['title'])
    aniId_to_index = pd.Series(all_anime.index, index=all_anime['anime_id'])
        
    print("Starting...\n")
    
    # Load the AutoEncoder
    model = PredictionEngine()

    # Get basic information from the user
    age = int(input("Enter Age: "))
    gender = input("Enter Gender (Male/Female): ")
    input_ratings = OrderedDict()

    # Let the user rate some animes
    print("\nIt is recommended to rate atleast 5 animes in the beginning.")
    print("Note:- Currently search mechanism searches for anime using the Japanese Title only.")
    
    # Start the recommendation process
    k1 = input("\nStart the process? [y/n]: ")

    while k1 == 'y' or k1 == 'Y':

        # If user want to search and rate
        k2 = input("\nSearch and rate? [y/n]: ")
        while k2 == 'y' or k2 == 'Y':
            p = 'n'
            while p == 'n' or p == 'N':
                input_anime = input("Enter Anime title: ")
                find_anime(input_anime.lower(), name_to_id)
                p = input("Anime found? [y/n]: ")

            aniId = int(input("Enter anime id: "))
            rate = int(input("Your rating (1 - 10): "))
            input_ratings[aniId] = rate

            k2 = input("Search and rate more? [y/n]: ")

        # Main Game
        HybridModel.showRecommendations(age, gender, input_ratings, model, all_anime, aniId_to_index)

        # If user want to rate anime from above list
        k2 = input("\nRate anime from above list? [y/n]:")
        while k2 == 'y' or k2 == 'Y':
            aniId = int(input("Enter anime id: "))
            rate = int(input("Your rating (1 - 10): "))
            input_ratings[aniId] = rate

            k2 = input("Rate again from above list? [y/n]: ")

        k1 = input("\nKeep going? [y/n]: ")

# Run script
main()
