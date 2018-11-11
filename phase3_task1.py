from pymongo import MongoClient
from scipy.spatial.distance import cdist
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from operator import itemgetter
import pickle


class Phase3_task1:
    def task1(self, k, desc):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        tb = 'imagetext'
        if desc != 'text':
            tb =''
        table = db[tb]

        data = []

        img_dist = {}
        self.image_terms = set()
        img_values = []

        for img in table.find({}):
            data.append(img)
            for term in img['desc']:
                self.image_terms.add(term['term'])

        print('image_terms', self.image_terms)

        # for img in data:
        #     img_values.append(self.get_values(img['desc']))
        #
        # img_values = np.array(img_values)
        # print(img_values.shape)

        # for img1 in data:
        #     img_dist[img1['id']] = []
        #     for img2 in data:
        #         img1_val = np.array(self.get_values(img1['desc']))
        #         img2_val = np.array(self.get_values(img2['desc']))
        #         dist = cdist(img1_val, img2_val, 'euclidean')
        #         img_dist[img1['id']].append({'id':img2['id'], 'dist':dist})

        for img1 in data:
            img_dist[img1['id']] = []
            distances = []
            for img2 in data:
                dist = self.get_sim(img1, img2)
                distances.append({'id': img2['id'], 'dist': dist})
            img_dist[img1['id']] = sorted(distances, key=itemgetter('dist'), reverse=True)
            if len(img_dist) > 100:
                break

        print("sim")
        print(img_dist)
        file = open('img_img_graph', 'wb')
        pickle.dump(img_dist, file)
        file.close()


    def get_sim(self, img1, img2):
        all_terms = set()

        img1_fr_val = {}
        img2_fr_val = {}

        img1_values = []
        img2_values = []

        for term in img1['desc']:
            all_terms.add(term['term'])
            img1_fr_val[term['term']] = term['TF-IDF']

        for term in img2['desc']:
            all_terms.add(term['term'])
            img2_fr_val[term['term']] = term['TF-IDF']

        for t in all_terms:
            img1_values.append(float(img1_fr_val.get(t, 0)))
            img2_values.append(float(img2_fr_val.get(t, 0)))


        # img1_values = np.array(img1_values).reshape(-1,1)
        # img2_values = np.array(img2_values).reshape(-1,1)

        # img1_values = np.reshape(img1_values, (-1, 2))
        # img2_values = np.reshape(img2_values, (-1, 2))


        sim = 1 - cosine(img1_values, img2_values)

        return sim


    def get_values(self, desc):
        values = []

        terms={}
        for term in desc:
            terms[term['term']] = term['TF-IDF'];

        for t in self.image_terms:
            if(t in terms.keys()):
                values.append(terms[t])
            else:
                values.append(0)
        return values

