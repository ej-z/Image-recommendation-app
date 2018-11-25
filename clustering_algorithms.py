from scipy import sparse
from scipy import linalg
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
            for j in range(data.k):
                x = data.graph[i][j]
                if i == j:
                    laplacian[i, j] = 1 #data.degree_mat[i]
                elif data.adjacency_mat[i, x] == 1:
                    d = -1/math.sqrt(data.degree_mat[i] * data.degree_mat[x])
                    laplacian[i, x] = d

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

        clusters = clusters.astype(np.int)
        clusters = clusters.tolist()
        return clusters

    def euclidean_distance(self, x, y, along=1):
        # return scipy.spatial.distance.cdist(x,y,'euclidean')
        return np.linalg.norm(x - y, axis=along)


    def clustering_2(self, data, n_clusters):

        n = len(data.img_ids)

        laplacian = sparse.csc_matrix((n, n), dtype=float)

        # Symmetric normalized Laplacian
        for i in range(n):
            for j in range(data.k):
                x = data.graph[i][j]
                if i == j:
                    laplacian[i, j] = 1  # data.degree_mat[i]
                elif data.adjacency_mat[i, x] == 1:
                    d = -1 / math.sqrt(data.degree_mat[i] * data.degree_mat[x])
                    laplacian[i, x] = d

        #eig_val, eig_vect = sparse.linalg.eigs(laplacian, 2, sigma=0, which='LM')
        eig_val, eig_vec = np.linalg.eig(laplacian.todense())

        print(eig_val.shape)

        min_idx = -1
        min_val = 100
        sec_min_idx = -1

        for idx, e in enumerate(eig_val):
            if e < min_val:
                sec_min_idx = min_idx
                min_idx = idx
                min_val = e

        y = eig_vec[sec_min_idx]

        cluster1 = []
        cluster2 = []

        for i in range(len(y)):
            if y[i] >= 0:
                cluster1.append(i)
            else:
                cluster2.append(i)

    def normalised_cut(self, data, c):

        nodes = [i for i in range(len(data.img_ids))]
        clusters = []

        self._normalised_cut_rec(data, nodes, c, clusters)
        return clusters

    def _normalised_cut_rec(self, data, nodes, c, clusters):
        if c < 2:
            clusters.append(nodes)
            return

        n = len(nodes)

        laplacian = sparse.lil_matrix((n, n), dtype=float)

        for m in range(n):
            i = nodes[m]
            for j in range(data.k):
                x = data.graph[i][j]
                if i == j:
                    laplacian[i, j] = 1  # data.degree_mat[i]
                elif data.adjacency_mat[i, x] == 1:
                    d = -1 / math.sqrt(data.degree_mat[i] * data.degree_mat[x])
                    laplacian[i, x] = d

        eig_val, eig_vec = np.linalg.eig(laplacian.todense())

        min_idx = -1
        min_val = 100
        sec_min_idx = -1
        print(eig_val)
        print(eig_vec)
        for idx, e in enumerate(eig_val.real):
            print('idx: '+str(idx)+'  e: '+str(e))
            if e < min_val:
                sec_min_idx = min_idx
                min_idx = idx
                min_val = e

        y = eig_vec[sec_min_idx]
        print(sec_min_idx)
        print(min_val)
        print(eig_val[min_idx])
        print(y.shape)
        print(y.to_list())
        print(len(y.to_list()))
        print(y[0].shape)
        print(y[0])
        y = y.real
        '''
        cluster1 = []
        cluster2 = []

        for i in range(len(y)):
            if y[i] >= 0:
                cluster1.append(i)
            else:
                cluster2.append(i)

        c = c - 2

        if c == 2:
            clusters.append(cluster1)
            clusters.append(cluster2)
        elif c == 3:
            if len(cluster1) < len(cluster2):
                clusters.append(cluster1)
                self._normalised_cut_rec(data, cluster2, c-1, clusters)
            else:
                clusters.append(cluster2)
                self._normalised_cut_rec(data, cluster1, c - 1, clusters)
        else:
            if len(cluster1) < len(cluster2):
                self._normalised_cut_rec(data, cluster1, math.floor(c / 2), clusters)
                self._normalised_cut_rec(data, cluster2, math.ciel(c / 2), clusters)
            else:
                self._normalised_cut_rec(data, cluster2, math.floor(c / 2), clusters)
                self._normalised_cut_rec(data, cluster1, math.ciel(c / 2), clusters)
                
        '''