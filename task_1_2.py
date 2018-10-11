from pymongo import MongoClient
from decomposition_algorithms import Decomposition
from scipy import spatial
from sklearn import metrics
from sorted_list import sorted_list

class Task_1_2:

    def __decompose(self, tb, model, algorithm, k):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db[tb]

        data = {}
        self.ids = []
        cnt = 0
        for s in table.find({}):

            self.ids.append(s['id'])
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
            if len(data[key]) >= 10:
                truncated_data.append(data[key])
                truncated_terms.append(key)
        arr = [[0 for _ in range(len(truncated_terms))] for _ in range(len(self.ids))]

        j = 0
        for t_d in truncated_data:
            for d in t_d:
                arr[d['id']][j] = d['model']
            j = j + 1

        self.features = truncated_terms
        self.decomposition = Decomposition(arr, k, algorithm, self.features, True)

    def task1(self, tb, model, algorithm, k):

        self.__decompose(tb, model, algorithm, k)

        print('Variance captured by top ' + str(k) + ' latent semantics: ' + str(self.decomposition.variance))

        for i in range(0, k):
            print()
            print()
            print('Latent semantic '+str(i+1))
            print(self.decomposition.loading_scores[i])

    def task2(self, tb, model, algorithm, k, id):

        self.__decompose(tb, model, algorithm, k)

        print('Variance captured by top ' + str(k) + ' latent semantics: ' + str(self.decomposition.variance))

        index = self.ids.index(id)

        s_mat = [self.decomposition.decomposed_data[index]]

        distances = sorted_list(5, 'distance', True)

        euc_distance = metrics.euclidean_distances(s_mat,self.decomposition.decomposed_data)

        for i in range(0, len(self.ids)):
            distances.add({'id': self.ids[i], 'distance': euc_distance[0][i]})

        print('Top 5 similar objects - Euclidean distance')
        print()
        for i in range(0,5):
            o = distances.extract()
            print(o['id']+' - '+str(o['distance']))
