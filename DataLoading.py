from pymongo import MongoClient
import collections
import csv
import requests
import xml.etree.ElementTree as ET

class DataLoading:

    def insert_textual_data(self, filename, tablename):
        with open(filename, encoding="utf8") as f:
            lines = f.readlines()
            client = MongoClient('localhost', 27017)
            db = client['mwdb']
            table = db[tablename]
            dataArr = []
            for line in lines:
                words = line.split(' ')
                data = collections.OrderedDict()
                data['id'] = words[0]
                data['desc'] = []

                i = 1;
                while i + 3 < len(words):
                    textDesc = collections.OrderedDict()
                    textDesc['term'] = words[i][1:-1]
                    textDesc['TF'] = words[i + 1]
                    textDesc['DF'] = words[i + 2]
                    textDesc['TF-IDF'] = words[i + 3]
                    data['desc'].append(textDesc)
                    i = i + 4

                dataArr.append(data)

            table.insert_many(dataArr)

    def insert_location_textual_data(self, filename, tablename):
        with open(filename, encoding="utf8") as f:
            lines = f.readlines()
            client = MongoClient('localhost', 27017)
            db = client['mwdb']
            table = db[tablename]
            locations = db['locations']
            dataArr = []
            for line in lines:
                words = line.split(' ')
                data = collections.OrderedDict()
                data['title'] = words[0]

                x = 1
                while x < len(words):
                    if words[x][0] == '"':
                        break
                    data['title'] = data['title'] + '_' + words[x]
                    x = x + 1

                data['id'] = locations.find_one({'title': data['title']})['id']
                data['desc'] = []

                i = x
                while i + 3 < len(words):
                    textDesc = collections.OrderedDict()
                    textDesc['term'] = words[i][1:-1]
                    textDesc['TF'] = words[i + 1]
                    textDesc['DF'] = words[i + 2]
                    textDesc['TF-IDF'] = words[i + 3]
                    data['desc'].append(textDesc)
                    i = i + 4

                dataArr.append(data)

            table.insert_many(dataArr)
    def process_users_textual_data(self):

        #insert usertext
        self.insert_textual_data(self.path+'\desctxt\desctxt\devset_textTermsPerUser.txt', 'usertext')

    def process_images_textual_data(self):

        #insert imagetext
        self.insert_textual_data(self.path+'\desctxt\desctxt\devset_textTermsPerImage.txt', 'imagetext')

    def process_locations_textual_data(self):

        #insert loctexts
        self.insert_location_textual_data(self.path+'\desctxt\desctxt\devset_textTermsPerPOI.txt', 'loctext')

    def process_location_data(self):

        filename = self.path + '\devset_topics.xml'

        root = ET.parse(filename).getroot()

        locations = []

        for topic in root.findall('topic'):
            location = {}
            location['id'] = topic.find('number').text
            location['title'] = topic.find('title').text
            location['latitude'] = topic.find('latitude').text
            location['longitude'] = topic.find('longitude').text
            location['wiki'] = topic.find('wiki').text

            locations.append(location)

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['locations']

        table.insert_many(locations)


    def process_visual_data(self):

        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CN3x3', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['locations']

        for l in table.find({}):
            data = []
            for m in models:
                model = {}
                arr = []
                filename = self.path + '\descvis\descvis\img\\'+l['title']+' '+m+'.csv'
                with open(filename, encoding="utf8") as f:
                    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                    for row in reader:  # each row is a list
                        arr.append(row)

                model['model'] = m
                model['data'] = arr
                data.append(model)
            t = db[l['title']]
            t.insert_many(data)



    def __init__(self, p):

        self.path = p

