import numpy as np
import math

'''
From Near-Optimal Hashing Algorithms for
Approximate Nearest Neighbor in High Dimensions by  Alexandr Andoni and Piotr Indyk
Using LSH Euclidean Hash family
'''
class LSH_index:

    def __init__(self, data, l, k, w):
        # hr, b = floor((r·x + b)/w)
        self.layers = l
        self.k = k
        self.w = w
        self._data = np.array(data)
        n = self._data.shape[0]
        c = self._data.shape[1]
        self.shifts = np.random.rand(l, k)
        self.shifts = self.shifts * (w-1)
        self.dict_arr = [dict() for x in range(l)]
        self.random_vectors = np.random.rand(l, k, c)
        for i in range(n):
            for j in range(l):
                key = ""
                for f in range(k):
                    rv_hat = self.random_vectors[j][f]/np.linalg.norm(self.random_vectors[j][f])
                    key+=(","+(str(math.floor((np.dot(rv_hat,self._data[i])+self.shifts[j][f])/self.w))))
                if key not in self.dict_arr[j]:
                    self.dict_arr[j][key] = set()
                self.dict_arr[j][key].add(i)


    def query(self, q):
        index_res = set()
        for j in range(self.layers):
            key = ""
            for f in range(self.k):
                rv_hat = self.random_vectors[j][f]/np.linalg.norm(self.random_vectors[j][f])
                key+=(","+(str(math.floor((np.dot(rv_hat,q)+self.shifts[j][f])/self.w))))
            print("unique data in single layer",self.dict_arr[j][key])
            index_res.update(self.dict_arr[j][key])
        return index_res






