# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:02:14 2021

@author: Debangan Daemon
"""
import pandas as pd

results = pd.read_csv('Clusters.csv')

clusters = []

for i in range(341):
    clusters.append([])

for i in range(len(results)):
    clusters[results['alpha'][i]].append(results['anime_id'][i])

def getCluster(anime_id, opposite=False):
    if opposite == False:
        temp = results[results['anime_id'] == anime_id]['alpha'].reset_index(drop=True)
        clusterID = temp[0]
        return clusters[clusterID]
    else:
        temp = results[results['anime_id'] == anime_id]['omega'].reset_index(drop=True)
        clusterID = temp['omega'][0]
        return clusters[clusterID]