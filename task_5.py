from pymongo import MongoClient
from decomposition_algorithms import Decomposition
from scipy import spatial
import numpy as np
from sklearn import metrics
from sorted_list import sorted_list
import operator


class Task_5:
    def __decompose(self, table_name, algorithm, k):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        locations_table = db[table_name].find({})
        self.locations = {}
        self.locations_img_ids = {}
        data = []
        count = 0
        for loc in locations_table:
            images = []
            image_ids = []
            for idx, model in enumerate(models):
                # model = 'CN'
                # idx = 0
                each_loc_model_table = db[loc['title']].find({"model":model})[0]
                images_with_ids = np.array(each_loc_model_table['data'])
                images_with_ids = images_with_ids.astype(np.float)
                if idx == 0:
                    #image_ids.extend(each_loc_model_table['data'])
                    image_ids.extend(images_with_ids[:, 0])
                    images.extend(images_with_ids[:, 1:])
                else:
                    images = np.concatenate((images, images_with_ids[:, 1:]), axis=1)
            data.extend(images)
            new_loc_size = len(images)
            self.locations_img_ids[loc['id']] = image_ids
            self.locations[loc['id']] = (count, count + new_loc_size)
            count += new_loc_size

        self.decomposition = Decomposition(data, k, algorithm, [], True)



        '''for loc in locations_table:
            each_loc_table = db[loc['title']].find({"model":model})[0]
            data.extend(each_loc_table["data"])
            new_loc_size = len(each_loc_table["data"])
            self.locations[loc['id']] = (count, count+new_loc_size)
            count+=new_loc_size

        self.images_with_id = np.array(data)
        self.images_with_id = self.images_with_id.astype(np.float)
        self.images_id = self.images_with_id[:, 0].transpose()
        self.images = self.images_with_id[:, 1:]
        self.decomposition = Decomposition(self.images, k, algorithm, [], True)'''


    def task5(self, table_name, algorithm, k, id):
        self.__decompose(table_name, algorithm, k*10)
        print('Variance captured by top ' + str(k) + ' latent semantics: ' + str(self.decomposition.variance))
        for i in range(0, k):
            print()
            print()
            print('Latent semantic '+str(i+1))
            print(self.decomposition.loading_scores[i])
        #decompose

        print(self.decomposition.decomposed_data.shape)
        s_mat = self.decomposition.decomposed_data[self.locations[id][0]:self.locations[id][1],:]
        distances = sorted_list(5, 'distance', True)

        for location_id, ranges in self.locations.items():
            euc_distance = metrics.euclidean_distances(s_mat,self.decomposition.decomposed_data[ranges[0]:ranges[1],:])
            distances.add({'id': location_id, 'distance': np.mean(euc_distance)})

        print('Top 5 similar locations in terms of Euclidean distance')
        print()
        for i in range(0,5):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))



