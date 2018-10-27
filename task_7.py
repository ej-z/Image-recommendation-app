import numpy as np
from pymongo import MongoClient
from tensorly import decomposition
from sklearn.cluster import KMeans
import pandas as pd
import os

class Task_7:

    def task_7(self, k):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['LIU_commonterms']

        locations = {}
        images = {}
        users = {}
        l_idx = 0
        i_idx = 0
        u_idx = 0
        #i = 0
        for s in table.find({}):
            if s['location'] not in locations:
                locations[s['location']] = l_idx
                l_idx = l_idx+1
            if s['image'] not in images:
                images[s['image']] = i_idx
                i_idx = i_idx+1
            if s['user'] not in users:
                users[s['user']] = u_idx
                u_idx = u_idx+1
            #i = i+1
            #if l_idx == 10:
            #    break

        tensor = np.empty((len(locations), len(images), len(users)), dtype=float)
        #j = 0
        for s in table.find({}):
            tensor[locations[s['location']]][images[s['image']]][users[s['user']]] = float(s['terms'])
            #j = j + 1
            #if i == j:
            #    break

        factors = decomposition.parafac(tensor, k)

        locationGroups = [[] for _ in range(k)]
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(factors[0])
        i = 0
        for l in locations:
            locationGroups[kmeans.labels_[i]].append(l)
            i = i+1
        imageGroups = [[] for _ in range(k)]
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(factors[1])
        i = 0
        for l in images:
            imageGroups[kmeans.labels_[i]].append(l)
            i = i + 1
        userGroups = [[] for _ in range(k)]
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(factors[2])
        i = 0
        for l in users:
            userGroups[kmeans.labels_[i]].append(l)
            i = i + 1

        for j in range(k):
            print("User Group "+str(j+1))
            print(userGroups[j])
            print('-'*30)
            print("Image Group " + str(j+1))
            print(imageGroups[j])
            print('-' * 30)
            print("Location Group " + str(j+1))
            print(locationGroups[j])
            print('-' * 30)
            print('-' * 30)


