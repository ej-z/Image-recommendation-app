import pandas as pd
import numpy as np

data1 = pd.read_csv('C:\\Users\\Vasu\\Desktop\\xclara.csv')
data = pd.read_csv('C:\\Users\\Vasu\\Desktop\\audioData.csv')
dataset = data.astype(float).values.tolist()
data = data.values
centroids = {}
for k in range(2,10):
    for i in range(k):
        centroids[i] = data[i]
    for i in range(300):
        classes = {}
        for j in range(k):
            classes[j] = []

        for features in data:
            distances = [np.linalg.norm(features - centroids[centroid]) for centroid in centroids]
            classification = distances.index(min(distances))
            classes[classification].append(features)
        old_centroids = dict(centroids)
        for f in classes:
            centroids[f] = np.average(classes[f], axis=0)
        run = True
        for m in centroids:
            old = old_centroids[m]
            new = centroids[m]
            dif = new - old
            perc = dif/(old*100)
            if(((new-old)/(old*100.00))> 0.001).any():
                run = False
        if(run):
            break
    sum = 0
    for i in classes:
        for j in range(len(classes[i])):
            amount = ((classes[i][j] - centroids[i])**2)
            amount = np.sum(amount)
            sum = sum + amount
    print(sum)