import numpy as np
import pandas as pd

class PageRanks:

    def page_rank(self, data):

        n = len(data.img_ids)

        old, new = np.zeros(n), np.zeros(n)
        initial = float(1/n)
        for i in range(n):
            new[i] = initial

        d = 0.85
        while abs(sum(old)-sum(new)) > 0.0001:
            old = new.copy()
            for i in range(n):
                s = 0
                for x in data.graph[i]:
                    s = s + (old[x['id']]/data.k)
                new[i] = (1-d) + (d * s)

        l_s = pd.Series(new/float(sum(new)), index=data.img_ids)
        return pd.Series.sort_values(l_s, ascending=False)


    def _process_data(self, data, k):

        img_ids = []
        img_ind = {}

        i = 0
        for key in data:
            img_ids.append(key)
            img_ind[key] = i
            i = i+1

        d = np.zeros((len(data), k))
        i = 0
        for key in data:
            j = 0
            for ids in data[key]:
                d[i][j] = img_ind[ids['id']]
                j = j + 1
            i = i + 1

        return img_ids, d