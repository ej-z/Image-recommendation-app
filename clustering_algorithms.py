from scipy import sparse
import numpy as np
import math
from sklearn.cluster import KMeans
import copy

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
                    laplacian[i, j] = -1
                    laplacian[j, i] = -1

        eig_val, eig_vect = sparse.linalg.eigs(laplacian, c)
        X = eig_vect.real
        rows_norm = np.linalg.norm(X, axis=1, ord=2)
        Y = (X.T / rows_norm).T
        labels = self.find_converging_centroid(Y, c)

        return labels

    def find_converging_centroid(self, data, k):
        clusters = np.zeros(data.shape[0])
        C = np.random.uniform(low=np.min(data), high=np.max(data), size=(k, data.shape[1]))
        C_previous = np.zeros(C.shape)
        change_in_centroid = self.euclidean_distance(C, C_previous, None)

        while change_in_centroid != 0:
            empty_cluster = False
            empty_cluster_index = 0
            biggest_cluster = 0
            single_biggest_cluster = []
            biggest_cluster_index = 0
            # CLASSIFY
            for i in range(data.shape[0]):
                distance_X_allC = self.euclidean_distance(data[i], C)
                cluster_index = np.argmin(distance_X_allC)
                clusters[i] = cluster_index
            C_previous = np.array(C, copy=True)
            # RECENTER
            for i in range(k):
                x_of_single_cluster = []
                for h in range(data.shape[0]):
                    if clusters[h] == i:
                        x_of_single_cluster.append(data[h])
                if len(x_of_single_cluster) == 0:
                    empty_cluster = True
                    empty_cluster_index = i
                    print("empty cluster found")
                else:
                    C[i] = np.mean(x_of_single_cluster, axis=0)
                if biggest_cluster < len(x_of_single_cluster):
                    biggest_cluster = len(x_of_single_cluster)
                    single_biggest_cluster = copy.copy(x_of_single_cluster)
                    biggest_cluster_index = i
            if empty_cluster:
                # divide the biggest cluster into two equal cluster
                list1 = single_biggest_cluster[:int(len(single_biggest_cluster) / 2)]
                list2 = single_biggest_cluster[int(len(single_biggest_cluster) / 2):]
                C[biggest_cluster_index] = np.mean(list1, axis=0)
                C[empty_cluster_index] = np.mean(list2, axis=0)
            change_in_centroid = self.euclidean_distance(C, C_previous, None)
        return clusters

    def euclidean_distance(self, x, y, along=1):
        # return scipy.spatial.distance.cdist(x,y,'euclidean')
        return np.linalg.norm(x - y, axis=along)