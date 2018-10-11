from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np


class Decomposition:

    def __init__(self, data, k, algorithm, features, scale=True):
        _data = data
        if scale:
            _data = StandardScaler().fit_transform(data)
        if algorithm == 'PCA':
            model = PCA(n_components=k)
        elif algorithm == 'SVD':
            model = TruncatedSVD(n_components=k)
        elif algorithm == 'LDA':
            model = LatentDirichletAllocation(n_components=k)
        else:
            raise Exception('Unrecognized algorithm '+algorithm)

        self.decomposed_data = model.fit_transform(_data)
        self.variance = np.sum(model.explained_variance_ratio_)
        self.loading_scores = []
        for i in range(0, k):
            l_s = pd.Series(model.components_[i], index=features)
            self.loading_scores.append(pd.Series.sort_values(l_s, ascending=False))

