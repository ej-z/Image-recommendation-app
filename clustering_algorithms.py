from scipy import sparse
import numpy as np
import math
from sklearn.cluster import KMeans

class Clustering_Algorithms:

    def k_means(self, X, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters, random_state=1231)
        return kmeans.fit(X).labels_

    def spectral_clustering(self, data, c):

        n = len(data.img_ids)

        laplacian = sparse.lil_matrix((n, n), dtype=float)

        # Symmetric normalized Laplacian
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    laplacian[i, j] = data.degree_mat[i]
                elif data.adjacency_mat[i, j] == 1:
                    d = -1/math.sqrt(data.degree_mat[i] * data.degree_mat[j])
                    laplacian[i, j] = d
                    laplacian[j, i] = d

        eig_val, eig_vect = sparse.linalg.eigs(laplacian, c)
        X = eig_vect.real
        rows_norm = np.linalg.norm(X, axis=1, ord=2)
        Y = (X.T / rows_norm).T
        # TODO: implement k means from scratch
        labels = self.k_means(Y, c)

        return labels