import numpy as np
import pandas as pd
import os

def tensor_form():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(cur_dir + "\\data\\")
    #names = ['acropolisathens.csv','agrafort.csv','Albert Memorial.csv','Altes Museum.csv','amiens_cathedral.csv','angelofthenorth.csv','angkor_wat.csv','ara_pacis.csv','arc_de_triomphe.csv','aztec_ruins.csv','berlin_cathedral.csv','bigben.csv','bok_tower_gardens.csv','brandenburg_gate.csv','cabrillo.csv','casa_batllo.csv','casa_rosada.csv','Castillo de San Marcos.csv','chartres_cathedral.csv','chichen_itza.csv','Christ the Redeemer.csv','cn_tower.csv','cologne_cathedral.csv','colosseum.csv','hearst_castle.csv','la_madeleine.csv','montezuma_castle.csv','nues_museum.csv','pont_alexandre.csv','The Civic Center in San Francisco.csv']
    datafinal = []
    term = 0
    for i in files:
        data = []
        csv = pd.read_csv(cur_dir + "\\data\\" +i)
        usid = list(set(csv["_userid"]))
        imid = list(set(csv["_id"]))
        while(len(imid)<300):
            imid.append(-len(imid))
        print("Processing file : " + i)
        csv['tg_cnt'] = 0
        term = term+20
        for i in usid:
            row_vector = [0] * len(imid)
            for idx, j in enumerate(imid):
                l = csv.loc[(csv._userid == str(i)) & (csv._id == j),"_tags"].tolist()
                try:
                    if len(l)>0:
                        row_vector[idx] = len(l[0].split())
                except:
                    pass
            data.append(row_vector)
        datafinal.append(np.array(data))
    a = np.dstack(datafinal)
    return a


tensor_form()

