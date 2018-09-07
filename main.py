from pymongo import MongoClient
import collections
import math
from scipy import spatial

def insert(filename, tablename):
    with open(filename, encoding="utf8") as f:
        lines = f.readlines()
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db[tablename]
        dataArr = []
        for line in lines:
            words = line.split(' ')
            data = collections.OrderedDict()
            data['Id'] = words[0]
            data['Desc'] = []

            i = 1;
            while i + 3 < len(words):
                textDesc = collections.OrderedDict()
                textDesc['Term'] = words[i][1:-1]
                textDesc['TF'] = words[i + 1]
                textDesc['DF'] = words[i + 2]
                textDesc['TFIDF'] = words[i + 3]
                data['Desc'].append(textDesc)
                i = i + 4

            dataArr.append(data)

        table.insert_many(dataArr)


def insert_data():

    #insert users
    insert('E:\Studies\MWDB\project\desctxt\desctxt\devset_textTermsPerUser.txt', 'users')

def findModelVal(desc, u, model):
    for udesc in u['Desc']:
        if desc['Term'] == udesc['Term']:
            return (int(desc[model])-int(udesc[model])) * (int(desc[model])-int(udesc[model]))
    #return (int(desc[model])) * (int(desc[model]))
    return 0

def prettyPrint(m, model):

    print('Id : '+m['Id'])
    print('Model : '+model)
    print()
    for desc in m['Desc']:
        print(desc['Term'] + ' : ' + desc[model])
    print('Total terms : ' + str(len(m['Desc'])))
    print('--------------------------------------')
    print('--------------------------------------')
    print()

def prettyPrint1(m,mm, model):
    m1 = mm['User']
    print('Id : ' + m1['Id'])
    print('Distance : ' + str(mm['Distance']))
    print('Model : ' + model)
    print()
    for desc in m['Desc']:
        for desc1 in m1['Desc']:
            if desc['Term'] == desc1['Term']:
                print(desc1['Term'] + ' : ' + desc1[model])
    print('Total terms : '+str(len(m1['Desc'])))
    print('--------------------------------------')

def main():

    # insert_data()

    client = MongoClient('localhost', 27017)
    db = client['mwdb']
    table = db['users']
    model = 'DF'
    K = 4
    user = table.find_one({'Id': '39052554@N00'})

    maxVal = 0
    for desc in user['Desc']:
        maxVal = maxVal + (int(desc[model])) * (int(desc[model]))

    result = []
    for u in table.find({}):

        res = {}
        val = 0
        if user['Id'] != u['Id']:

            a1 = []
            a2 = []

            #n = max(len(user['Desc'], len(u['User']['Desc'])))
            i = 0
            j = 0

            while i < len(user['Desc']) and j < len(u['Desc']):
                if(user['Desc'][i]['Term'] == u['Desc'][j]['Term']):
                    a1.append(int(user['Desc'][i][model]))
                    a2.append(int(u['Desc'][j][model]))
                    i = i+1
                    j = j+1
                elif user['Desc'][i]['Term'] < u['Desc'][j]['Term']:
                    a1.append(int(user['Desc'][i][model]))
                    a2.append(0)
                    i = i+1
                else:
                    a1.append(0)
                    a2.append(int(u['Desc'][j][model]))
                    j = j+1

            while i < len(user['Desc']):
                a1.append(int(user['Desc'][i][model]))
                a2.append(0)
                i = i + 1

            while j < len(u['Desc']):
                a1.append(0)
                a2.append(int(u['Desc'][j][model]))
                j = j + 1

            #for desc in user['Desc']:
            #    val = val + findModelVal(desc, u, model)
            val = 1 - spatial.distance.cosine(a1, a2)
            #if val < maxVal:
            res['Distance'] = math.sqrt(val)
            res['User'] = u
            result.append(res)


    newlist = sorted(result, key=lambda k: k['Distance'], reverse=True)

    i = 0

    prettyPrint(user, model)

    while i < K and i < len(newlist):
        prettyPrint1(user, newlist[i], model)
        i = i+1


    #print('hello world!')




if __name__ == "__main__":
    main()