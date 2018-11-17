import numpy as np
import pandas as pd
from scipy import sparse


class PageRanks:

    def page_rank(self, data):

        n = len(data.img_ids)
        M = self._process_data(data)
        E = np.zeros((n, n))

        #TODO: presonalization should come into effect here, I think.
        alpha = 0.85
        dp = (1 - alpha) / n
        E[:] = dp
        A = (alpha * M) + E

        '''
        w, v = np.linalg.eig(A.T)
        left_vec = v[:, w.argmax()]
        left_vec = left_vec / float(sum(left_vec.real))
        final_ranks = np.zeros(n)
        for i in range(n):
            final_ranks[i] = left_vec[i,0]
        l_s = pd.Series(final_ranks, index=data.img_ids)
        return pd.Series.sort_values(l_s, ascending=False)
        '''
        old, new = np.zeros((1, n)), np.zeros((1, n))
        new[0][0] = 1
        iter = 0
        while iter < 100 and not np.array_equal(old, new):
            old = new.copy()
            new = np.matmul(new, A)
            iter = iter + 1
        final_ranks = np.zeros(n)
        for i in range(n):
            final_ranks[i] = new[0, i]
        l_s = pd.Series(final_ranks, index=data.img_ids)
        return pd.Series.sort_values(l_s, ascending=False)


    def _process_data(self, data):

        n = len(data.img_ids)
        M = sparse.lil_matrix((n, n), dtype=float)

        for i in range(n):
            for j in range(data.k):
                #TODO: actual probability distribution
                M[i, data.graph[i][j]['id']] = 1/data.k

        return M