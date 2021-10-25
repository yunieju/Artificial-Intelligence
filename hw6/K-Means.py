import math
import random
import numpy as np
import matplotlib.pyplot as plt

'''
1. Randomly pick k data points as our initial Centroids
2. Find the distance bt/ each points in the dataset with k centroids
3. Assign each data point to the closest centroid
4. update centroid location by taking the average of the points
5. Repeat 2-4 until the centroids don't change
'''
class KMeans:
    def __init__(self, k, num):
        self.labels = dict()
        self.k = k
        self.points = [[] for _ in range(k)]
        self.centroids = dict()
        self.num = num

    def process(self):
        data = self.readFile('./A.txt')
        self.initializeCentroids(data, self.k)

        for x in range(self.num):
            # find the distance between centroids and all the data points
            for i in range(len(data)):
                # assign a data point to its closest centroid
                distances = [self.findDistance(self.centroids[c], data[i]) for c in range(len(self.centroids))]
                minIndex = distances.index(min(distances))
                # only for the first iteration
                if x == 0:
                    self.labels[tuple(data[i])] = minIndex
                    self.points[minIndex].append(data[i])
                else:
                    prevLabel = self.labels[tuple(data[i])]
                    if minIndex != prevLabel:
                        print(self.points)
                        print(data[i])
                        self.points[prevLabel].remove(data[i])
                        self.points[minIndex].append(data[i])
                    # no need to update if minIndex == prevLabel

                # update the centroids
                self.updateCentroids()
        dVal = 0
        for c in range(self.k):
            for p in self.points[c]:
                dVal += self.findDistance(self.centroids[c], p)

        print("Distortion Value: ", dVal)
        print("Result Centroids")
        print(self.centroids)
        print(len(self.points[0])+len(self.points[1])+len(self.points[2]))

    def readFile(self, path):
        dataset = []
        # read data from a given txt file
        with open(path) as file:
            lines = file.readlines()
            lines = [line.split() for line in lines]
            for line in lines:
                dataset.append([float(line[0]), float(line[1])])
        print(len(dataset))
        return dataset

    # randomly initialize k centroids
    def initializeCentroids(self, data, k):
        for i in range(k):
            idx = random.randrange(0, len(data))
            self.centroids[i] = data[idx]
        print("Initialize centroids", self.centroids)
        return self.centroids

    # calculate Euclidean Distance from a given center to point
    def findDistance(self, center, point):
        return math.sqrt(pow(abs(center[0] - point[0]), 2) + pow(abs(center[1] - point[1]), 2))

    def updateCentroids(self):
        for i in range(len(self.points)):
            if len(self.points[i]) != 0:
                self.centroids[i] = np.mean(self.points[i], axis=0).tolist()

kmean = KMeans(k=3, num=1000)
kmean.process()
colors= ['red', 'green', 'blue', 'pink', 'orange']

for i in range(len(kmean.points)):
    for [x, y] in kmean.points[i]:
        plt.scatter(x, y, color=colors[i], s=2)
plt.show()




