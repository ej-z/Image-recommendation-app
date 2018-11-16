import numpy as np
from lsh_index import LSH_index
from pymongo import MongoClient
from sklearn import metrics
from sorted_list import sorted_list
from UI import PicturesApp
class Task_5ab:
    def task4(self, l, k, data):
        self.lsh_index = LSH_index(data, l,k,1.7)

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
        self.task4(7, 5, data)
        given_image_index = data_ids.index(float(id))
        res = self.lsh_index.query(data[given_image_index])
        for i in res:
            #print("data_result", data[i])
           # print("given_image", data[given_image_index])
            print("index =",i)
            print("data id =",data_ids[i])
            print("value =",np.linalg.norm(data[i]-data[given_image_index]))

        ''' To Rank them in order '''
        distances = sorted_list(len(res)-2, 'distance', True)
        for i in res:
            distances.add({'id': data_ids[i], 'distance': np.linalg.norm(data[i]-data[given_image_index])})
        print('Total considered images= ',len(res))
        print('Top 5 similar images and similarity score using LSH')
        print()
        for i in range(0,len(res)-2):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))

        '''To delete'''
        s_mat = [data[given_image_index]]

        distances = sorted_list(len(res)-2, 'distance', True)

        euc_distance = metrics.euclidean_distances(s_mat,data)
        # euc_distance = metrics.euclidean_distances([self.images[given_image_index]],self.images)
        for i in range(0, len(data_ids)):
            distances.add({'id': data_ids[i], 'distance': euc_distance[0][i]})

        print('Top 5 similar images and similarity score for validation purpose')
        print()
        for i in range(0,len(res)-2):
            o = distances.extract()
            print(str(o['id'])+' - '+str(o['distance']))

if __name__ == '__main__':
    tk = Task_5ab()
    pic_info = []
    pic_info.append({'cluster': 'cluster1', 'data':[{'id':'10041290516', 'info':'kool'},{'id':'10041384303', 'info':'kool2'},{'id':'9960455216', 'info':'kool3'},{'id':'9960426144', 'info':'kool2'},{'id':'9960411914', 'info':'kool'},{'id':'8557266548', 'info':'kool2'},{'id':'10427997426', 'info':'kool3'},{'id':'10686677944', 'info':'kool2'}]})
    pk = PicturesApp.PicturesApp(pic_info).run()
    tk.task5(4268828872,5)


