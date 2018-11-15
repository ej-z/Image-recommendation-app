from pymongo import MongoClient
from scipy.spatial.distance import cdist
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from operator import itemgetter
import pickle
from img_img_data import Img_Img_Data


class Phase3_task1:
    def task1(self, k, type):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']

        if type == 'text':
            data_table = db['img_img_text']
            id_table = db['imagetext']
        else:
            return

        graph = []
        img_ids = []
        for id in id_table.find({}):
            img_ids.append(id['id'])


        for d in data_table.find({}):
            graph.append(d['data'][:k])

        return Img_Img_Data(img_ids, graph, k)

    def task111(self, k, desc):
        if desc == 'text':
            self.text_graph(k)
        else:
            self.vis_graph(k)

    def text_graph(self, k):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        tb = 'imagetext'

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
            print("image id", img1['id'])
            img_dist[img1['id']] = []
            distances = []
            for img2 in data:
                dist = self.get_sim(img1, img2)
                distances.append({'id': img2['id'], 'dist': dist})
            img_dist[img1['id']] = sorted(distances, key=itemgetter('dist'), reverse=True)
            if len(img_dist) % 100 == 0:
                print(len(img_dist))
                break

        print("-----------------------")
        # print(img_dist)
        print("writing to file")
        file = open('img_img_graph', 'wb')
        pickle.dump(img_dist, file)
        file.close()
        print("writing to file done")


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


    def vis_graph(self, k):
        print("using visual descriptors")

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        tb = 'locations'

        table = db[tb]
        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        data = []
        count = 0
        self.locations_img_ids = {}
        img_dist = {}
        index = 0
        image_ids = []


        for loc in table.find({}):
            index += 1
            images = []
            # image_ids = []
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
            # new_loc_size = len(images)
            # self.locations_img_ids[loc['id']] = image_ids
            # self.locations[loc['id']] = (count, count + new_loc_size)
            # count += new_loc_size
            # if index == 2:
            #     break


        data = np.asarray(data)
        print(data.shape)

        for i, img1 in enumerate(data):
            img_dist[image_ids[i]] = []
            distances = []
            for j, img2 in enumerate(data):
                dist = euclidean(img1, img2)
                distances.append({'id': image_ids[j], 'dist': dist})
                # img_dist[image_ids[i]]  = distances
            img_dist[image_ids[i]] = sorted(distances, key=itemgetter('dist'))
            if len(img_dist) > 1:
                break

        file = open('img_img_graph_vis', 'wb')
        pickle.dump(img_dist, file)
        file.close()
