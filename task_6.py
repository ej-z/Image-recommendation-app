import numpy as np
from pymongo import MongoClient
from decomposition_algorithms import Decomposition_Sparse, Decomposition

'''
Implement a program which, given a value k,
– creates a location-location similarity matrix,
– performs SVD on this location-location similarity matrix, and
– reports the top-k latent semantics.
Each latent semantic should be presented in the form of location (name)-weight pairs, ordered in decreasing order of
weights.
'''
class Task_6:

    def task6(self, tb, model, algorithm, k):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db[tb]

        data = {}
        ids = []
        cnt = 0
        location_names = []
        for s in table.find({}):
            ids.append(s['id'])
            location_names.append(s['title'])
            for desc in s['desc']:
                term = desc['term']
                if term in data:
                    data[term].append({'id': cnt, 'model': float(desc[model])})
                else:
                    data[term] = [{'id': cnt, 'model': float(desc[model])}]
            cnt = cnt + 1

        truncated_terms = []
        truncated_data = []
        for key in data:
            #print('key = ', key, ' value = ', data[key])
            truncated_data.append(data[key])
            truncated_terms.append(key)
        arr = [[0 for _ in range(len(truncated_terms))] for _ in range(len(ids))]

        j = 0
        for t_d in truncated_data:
            for d in t_d:
                arr[d['id']][j] = d['model']
            j = j + 1

        n_arr = np.matrix(arr)
        result = n_arr * n_arr.T
        decomposition = Decomposition(result, k, algorithm, location_names)
        print('Top-k latent semantics in the form of location (name)-weight pairs, in decreasing order of weights:')
        print(decomposition.loading_scores)
