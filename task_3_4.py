from pymongo import MongoClient
from decomposition_algorithms import Decomposition
from scipy import spatial
import numpy as np
from sklearn import metrics
from sorted_list import sorted_list
from numpy import linalg as LA
import operator

'''
: Implement a program which, given a visual descriptor model (CM, CM3x3, CN, CN3x3,CSD,GLRLM, GLRLM3x3,
HOG,LBP, LBP3x3) and value “k”,
– first identifies (and lists) k latent semantics
'''
class Task_3_4:
    def __decompose(self, table_name, model, algorithm, k):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        locations_table = db[table_name].find({})
        self.locations = {}
        data = []
        count = 0
        for loc in locations_table:
            each_loc_table = db[loc['title']].find({"model":model})[0]
            data.extend(each_loc_table["data"])
            new_loc_size = len(each_loc_table["data"])
            self.locations[loc['id']] = (count, count+new_loc_size)
            count+=new_loc_size
        self.images_with_id = np.array(data)
        self.images_with_id = self.images_with_id.astype(np.float)
        self.images_id = self.images_with_id[:, 0].transpose()
        self.images = self.images_with_id[:, 1:]
        if algorithm == "LDA":
            min = np.amin(self.images)
            if min<0:
                self.images[:,:]+=(abs(min))
            self.decomposition = Decomposition(self.images, k, algorithm, [], False)
        else:
            self.decomposition = Decomposition(self.images, k, algorithm, [], True)




    def task3(self, table_name, model, algorithm, k, id):
        self.__decompose(table_name, model, algorithm, k)
        given_image_index = self.images_id.tolist().index(float(id))
        for i in range(0, k):
            print()
            print()
            print('Latent semantic '+str(i+1))
            print('FeatureNo  Weight')
            print(self.decomposition.loading_scores[i])
        #decompose

        s_mat = [self.decomposition.decomposed_data[given_image_index]]

        distances = sorted_list(5, 'distance', True)

        euc_distance = metrics.euclidean_distances(s_mat,self.decomposition.decomposed_data)
        # euc_distance = metrics.euclidean_distances([self.images[given_image_index]],self.images)
        for i in range(0, len(self.images_id)):
            distances.add({'id': self.images_id[i], 'distance': euc_distance[0][i]})

        print('Top 5 similar objects in terms of image Id - Euclidean distance')
        print()
        for i in range(0,5):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))

        distances_loc = sorted_list(5, 'distance', True)

        for location_id, ranges in self.locations.items():
            start_index = ranges[0]
            end_index = ranges[1]
            sum = 0.0
            for j in range(start_index, end_index):
                sum = sum + euc_distance[0][j]
            distances_loc.add({'id': location_id, 'distance': sum/(end_index-start_index)})

        print('Top 5 similar objects in terms of location Id - Euclidean distance')
        print()
        for i in range(0,5):
            o = distances_loc.extract()
            print(str(o['id'])+' - '+str(o['distance']))

    def task4(self, table_name, model, algorithm, k, id):
        self.__decompose(table_name, model, algorithm, k)
        for i in range(0, k):
            print()
            print()
            print('Latent semantic '+str(i+1))
            print('FeatureNo  Weight')
            print(self.decomposition.loading_scores[i])
        #decompose
        s_mat = self.decomposition.decomposed_data[self.locations[id][0]:self.locations[id][1],:]
        distances = sorted_list(5, 'distance', True)

        for location_id, ranges in self.locations.items():
            #euc_distance = metrics.euclidean_distances(s_mat,self.decomposition.decomposed_data[ranges[0]:ranges[1],:])
            #distances.add({'id': location_id, 'distance': np.mean(euc_distance)})
            euc_distance = abs(LA.norm(s_mat)-LA.norm(self.decomposition.decomposed_data[ranges[0]:ranges[1],:]))
            distances.add({'id': location_id, 'distance': euc_distance})


        print('Top 5 similar locations in terms of Euclidean distance')
        print()
        for i in range(0,5):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))



