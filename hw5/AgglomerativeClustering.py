import math

import numpy as np
import matplotlib.pyplot as plt

# use average link
dataset = []
map = dict()
def readFile(path):
    # read data from a given txt file
    with open(path) as file:
        lines = file.readlines()
        lines = [line.split() for line in lines]
        for line in lines:
            dataset.append([(float(line[0]), float(line[1]))])
    print(len(dataset))
    return dataset


def compute_distance(data):
    # matrix = [[10000 for i in range(len(data))] for j in range(len(data))]
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
    
    A_avgX = sum([x for (x,y) in A]) / len(A)
    A_avgY = sum([y for (x,y) in A]) / len(A)
    B_avgX = sum([x for (x,y) in B]) / len(B)
    B_avgY = sum([y for (x,y) in B]) / len(B)

    dist = pow(A_avgX - B_avgX, 2) + pow(A_avgY - B_avgY, 2)
    dist = math.sqrt(dist)
    return dist

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







