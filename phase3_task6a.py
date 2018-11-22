from classification_algorithms import KNN
import numpy as np
from pymongo import MongoClient

import pandas as pd
class Phase3_Task_6a:
    def process_distances(self):
        '''
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        data_table = db['image_image_vis']
        id_table = db['image_id_vis']
        graph = []
        img_ids = []
        for id in id_table.find({}):
            image_id = str(id['image_id'])
            img_ids.append(image_id[:len(image_id)-2])
        for d in data_table.find({}):
            graph.append(d['data'][:])
        self.img_ids = img_ids
        self.graph
        '''
    def task6a(self, k, fileName):
        pd.read_csv(fileName, delim_whitespace=True)



