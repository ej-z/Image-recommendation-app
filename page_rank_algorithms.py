import numpy as np
import pandas as pd
from scipy import sparse


class PageRanks:

    def page_rank(self, data):

        n = len(data.img_ids)
        #M = self._process_data(data)
        M = data.adjacency_mat/data.k
        E = np.zeros((n, n))

        #TODO: presonalization should come into effect here, I think.
        alpha = 0.85
        dp = (1 - alpha) / n
        E[:] = dp
        A = (alpha * M) + E
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
                M[i, data.graph[i][j]] = 1/data.k

        return M

    def personalized_page_rank(self, data, query_imgs):

        n = len(data.img_ids)

        R = data.adjacency_mat/data.k   #row-normalization
        V = np.zeros((1,n))

        for img in query_imgs:
            idx = data.img_ids.index(img)
            print(idx)
            V[0][idx] = 1/len(query_imgs)

        alpha = 0.15
        old = np.zeros((1, n))
        new = V
        term1 = (1-alpha) * R.todense()
        print('old shape', np.shape(old))
        print('term1 shape', np.shape(term1))
        iter = 0
        while iter < 100 and not np.array_equal(old, new):
            old = new.copy()
            # print(np.shape(new))
            new = np.matmul(new, term1) + (alpha * V)
            iter = iter + 1
        final_ranks = np.zeros(n)
        for i in range(n):
            final_ranks[i] = new[0, i]
        l_s = pd.Series(final_ranks, index=data.img_ids)
        return pd.Series.sort_values(l_s, ascending=False)