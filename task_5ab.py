import numpy as np
from lsh_index import LSH_index
from pymongo import MongoClient

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
        self.task4(6, 7, data)
        given_image_index = data_ids.index(float(id))
        res = self.lsh_index.query(data[given_image_index])
        for i in res:
            print(data_ids[i])

if __name__ == '__main__':
    tk = Task_5ab()
    tk.task5(10045488655,5)

