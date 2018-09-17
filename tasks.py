from pymongo import MongoClient
import math
from scipy import spatial
from sklearn import metrics


def task1_3(tb, id, model, k):

    # insert_data()

    client = MongoClient('localhost', 27017)
    db = client['mwdb']
    table = db[tb]
    src = table.find_one({'id': id})

    maxVal = 0
    for desc in src['desc']:
        maxVal = maxVal + (float(desc[model])) * (float(desc[model]))

    result = []
    for s in table.find({}):

        res = {}
        val = 0
        if src['id'] != s['id']:

            terms = []
            a1 = []
            a2 = []

            # n = max(len(user['Desc'], len(u['User']['Desc'])))
            i = 0
            j = 0

            while i < len(src['desc']) and j < len(s['desc']):
                if (src['desc'][i]['term'] == s['desc'][j]['term']):
                    terms.append(src['desc'][i]['term'])
                    a1.append(float(src['desc'][i][model]))
                    a2.append(float(s['desc'][j][model]))
                    i = i + 1
                    j = j + 1
                elif src['desc'][i]['term'] < s['desc'][j]['term']:
                    terms.append(src['desc'][i]['term'])
                    a1.append(float(src['desc'][i][model]))
                    a2.append(0)
                    i = i + 1
                else:
                    terms.append(s['desc'][j]['term'])
                    a1.append(0)
                    a2.append(float(s['desc'][j][model]))
                    j = j + 1

            while i < len(src['desc']):
                terms.append(src['desc'][i]['term'])
                a1.append(float(src['desc'][i][model]))
                a2.append(0)
                i = i + 1

            while j < len(s['desc']):
                terms.append(s['desc'][j]['term'])
                a1.append(0)
                a2.append(float(s['desc'][j][model]))
                j = j + 1

            val = 1 - spatial.distance.cosine(a1, a2)
            res['distance'] = val
            res['id'] = s['id']
            res['s'] = a1
            res['t'] = a2
            res['terms'] = terms
            result.append(res)

    newlist = sorted(result, key=lambda k: k['distance'], reverse=True)

    print('id : ' + src['id'] + "   model :" + model + "    k :" + str(k))
    n = 0
    print()
    while n < k and n < len(newlist):
        print('id : '+str(newlist[n]['id']) + " - "+ str(newlist[n]['distance']))
        top3 = top3_textual_matches(newlist[n]['s'], newlist[n]['t'])
        print('Top 3 contributors (euclidean distance)')
        for t in top3:
            print(newlist[n]['terms'][t['i']]+':'+str(t['d']))
        print()
        n = n + 1

def top3_textual_matches(s_mat, t_mat):

    res = []
    n = len(s_mat)

    for i in range(0, n):
        if s_mat[i] == 0 or t_mat[i] == 0:
            continue

        d = abs(s_mat[i] - t_mat[i])
        if len(res) < 3 and not(math.isnan(d)):
            res.append({'i': i, 'd': d})
        else:
            k = -1
            min = 100000000
            l = 0
            for r in res:
                if r['d'] < min:
                    min = r['d']
                    k = l
                l = l + 1
            if k > -1 and min > d and not(math.isnan(d)):
                res[k] = {'i': i, 'd': d}

    if len(res) < 3:
        res1 = []
        m = 3 - len(res)
        for i in range(0, n):
            if s_mat[i] != 0 and t_mat[i] != 0:
                continue

            d = abs(s_mat[i] - t_mat[i])
            if len(res1) < m and not (math.isnan(d)):
                res1.append({'i': i, 'd': d})
            else:
                k = -1
                min = 100000000
                l = 0
                for r in res1:
                    if r['d'] < min:
                        min = r['d']
                        k = l
                    l = l + 1
                if k > -1 and min > d and not (math.isnan(d)):
                    res1[k] = {'i': i, 'd': d}
        for i in range(0, m):
            res.append(res1[i])
    return res

def task4(id, model, k):
    client = MongoClient('localhost', 27017)
    db = client['mwdb']
    locations = db['locations']
    loc = locations.find_one({'id': id})

    s_loc = db[loc['title']]
    s_data = s_loc.find_one({'model': model})['data']


    distances = []

    s_mat = []
    s_img = []

    for s_d in s_data:
        s_mat.append(s_d[1:])
        s_img.append(s_d[0])

    for l in locations.find({'id': {'$ne': id}}):
        t_loc = db[l['title']]
        t_data = t_loc.find_one({'model': model})['data']
        t_mat = []
        t_img = []
        for t_d in t_data:
            t_mat.append(t_d[1:])
            t_img.append(t_d[0])

        r_mat = metrics.pairwise.euclidean_distances(s_mat, t_mat)
        top_3 = top3_pairwise_matches(r_mat)
        r_avg = r_mat.mean()
        r_img = []
        for t in top_3:
            r_img.append({'src': s_img[t['i']], 'tgt': t_img[t['j']], 'd': t['d']})

        distances.append({'id':l['id'],'title':l['title'],'distance':r_avg,'top':r_img})

    x = 0

    print(str(id)+':'+str(loc['title'])+"    model - "+model+"    k - "+str(k))
    print()
    for di in sorted(distances, key=lambda k: k['distance']):
        print(str(di['id']) + ':' + str(di['title']) + " - " + str(di['distance']))
        print('Top 3 contributing images')
        for t in di['top']:
            print(str(t['src']) + ':' + str(t['tgt']) + " - " + str(t['d']))
        print()
        print()
        x = x + 1
        if x >= k:
            break

def top3_pairwise_matches(r_mat):

    res = []
    n = len(r_mat)
    m = len(r_mat[0])

    for i in range(0,n):
        for j in range(0,m):
            if len(res) < 3:
                res.append({'i': i, 'j': j, 'd': r_mat[i][j]})
            else:
                k = -1
                max = -1
                l = 0
                for r in res:
                    if r['d'] > max:
                        max = r['d']
                        k = l
                    l = l + 1
                if k > -1 and max > r_mat[i][j]:
                    res[k] = {'i': i, 'j': j, 'd': r_mat[i][j]}

    return res

def task5(id, k):
    client = MongoClient('localhost', 27017)
    db = client['mwdb']
    locations = db['locations']
    loc = locations.find_one({'id': id})

    s_loc = db[loc['title']]

    models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CN3x3', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
    first = 0
    distances = []
    for model in models:
        s_data = s_loc.find_one({'model': model})['data']

        s_mat = []
        s_img = []

        for s_d in s_data:
            s_mat.append(s_d[1:])
            s_img.append(s_d[0])


        n = 0
        for l in locations.find({'id': {'$ne': id}}):
            t_loc = db[l['title']]
            t_data = t_loc.find_one({'model': model})['data']
            t_mat = []
            t_img = []
            for t_d in t_data:
                t_mat.append(t_d[1:])
                t_img.append(t_d[0])

            r_mat = metrics.pairwise.euclidean_distances(s_mat, t_mat)
            r_avg = r_mat.mean()



            if first == 0:
                r_dist = []
                r_dist.append(r_avg)
                distances.append({'id':l['id'],'title':l['title'],'distances':r_dist})
            else:
                distances[n]['distances'].append(r_avg)

            n = n + 1
        first = 1

    for d in distances:
        avg = sum(d['distances']) / float(len(d['distances']))
        d['avg'] = avg

    x = 0
    print(str(id)+':'+str(loc['title'])+"    k - "+str(k))
    print()
    for di in sorted(distances, key=lambda k: k['avg']):
        print(str(di['id']) + ':' + str(di['title']) + " - " + str(di['avg']))
        print('Contributions')
        for i in range(0,len(models)):
            print(str(models[i]) + ' - ' + str(di['distances'][i]))
        print()
        print()
        x = x + 1
        if x >= k:
           break