import math

import numpy as np
import matplotlib.pyplot as plt

# use single link
dataset = []
def readFile(path):
    # read data from a given txt file
    with open(path) as file:
        lines = file.readlines()
        lines = [line.split() for line in lines]
        for line in lines:
            dataset.append([(float(line[0]), float(line[1]))])
    return dataset


def compute_distance(data):
    matrix = np.zeros((len(data), len(data)))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j:
                matrix[i][j] = float(calculateDistance(data[i], data[j]))
            else:
                matrix[i][j] = 1000000
    return matrix


# calculate Euclidean distance
def calculateDistance(A, B):
    minimum = 10000
    for (ax, ay) in A:
        for (bx, by) in B:
            dist = pow(ax - bx, 2) + pow(ay - by, 2)
            dist = math.sqrt(dist)
            minimum = min(minimum, dist)

    return minimum


def findMinimumIndex(minimum, m):
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] == minimum:
                return (i, j)


def drawGraph(data):
    cluster1 = data[0]
    cluster2 = data[1]
    c1_x = [x for (x, y) in cluster1]
    c1_y = [y for (x, y) in cluster1]
    c2_x = [x for (x, y) in cluster2]
    c2_y = [y for (x, y) in cluster2]
    plt.scatter(c1_x, c1_y, c='red')
    plt.scatter(c2_x, c2_y, c='blue')
    plt.show()


def process():
    data = readFile('./B.txt')
    while len(data) > 2:
        m = compute_distance(data)

        # pick a minimum distance
        # merge into one point and remove one from data set
        minimum = min([min(r) for r in m])
        # print(minimum)
        (i, j) = findMinimumIndex(minimum, m)

        print(i,j)

        print("Merge ", data[i], " with ", data[j])
        data[i] += data[j]

        newdata = data[:j] + data[j+1:]
        data = newdata[:]

    return data


d = process()
print(d)
drawGraph(d)
print(len(d[0]) + len(d[1]))







