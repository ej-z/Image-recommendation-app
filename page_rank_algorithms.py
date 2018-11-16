import numpy as np
import pandas as pd
from scipy import sparse

class PageRanks:

    def page_rank(self, data):

        n = len(data.img_ids)
        M = self._process_data(data)
        E = np.zeros((n, n))
        dp = 1/n
        #TODO: presonalization should come into effect here, I think.
        E[:] = dp
        d = 0.85
        A = d * M.transpose() + ((1 - d) * E)

        old, new = np.zeros(shape=(n, 1)), np.zeros(shape=(n, 1))
        new[:] = dp
        while abs(sum(old)-sum(new)) > 0.0001:
            old = new.copy()
            new = A * new

        final_ranks = np.zeros(n)
        for i in range(n):
            final_ranks[i] = new[i][0]
        l_s = pd.Series(final_ranks/float(sum(final_ranks)), index=data.img_ids)
        return pd.Series.sort_values(l_s, ascending=False)


    def _process_data(self, data):

        n = len(data.img_ids)
        M = sparse.lil_matrix((n, n), dtype=float)

        for i in range(n):
            for j in range(data.k):
                #TODO: actual probability distribution
                M[i, data.graph[i][j]['id']] = 1/data.k

        return M