import numpy as np
from lsh_index import LSH_index
from pymongo import MongoClient
from sklearn import metrics
from sorted_list import sorted_list

class Task_5ab:
    def task4(self, l, k, data):
        self.lsh_index = LSH_index(data, l,k,1.5)

    def task5(self, id, t):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        models = ['CM3x3', 'CN3x3', 'LBP3x3']
        locations_table = db["locations"].find({})
        data = []
        data_ids = []
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
            data_ids.extend(image_ids)
            data.extend(images)

        data = np.asarray(data)
        self.task4(13, 12, data)
        given_image_index = data_ids.index(float(id))
        res = self.lsh_index.query(data[given_image_index])
        for i in res:
            #print("data_result", data[i])
           # print("given_image", data[given_image_index])
            print("data id =",data_ids[i])
            print("value =",np.linalg.norm(data[i]-data[given_image_index]))

        '''To delete'''
        s_mat = [data[given_image_index]]

        distances = sorted_list(25, 'distance', True)

        euc_distance = metrics.euclidean_distances(s_mat,data)
        # euc_distance = metrics.euclidean_distances([self.images[given_image_index]],self.images)
        for i in range(0, len(data_ids)):
            distances.add({'id': data_ids[i], 'distance': euc_distance[0][i]})

        print('Top 5 similar images and similarity score')
        print()
        for i in range(0,25):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))

if __name__ == '__main__':
    tk = Task_5ab()
    tk.task5(10045488655,5)

