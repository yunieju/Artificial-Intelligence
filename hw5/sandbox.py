import numpy as np

A = np.array([(2,4)])
print(A.mean(axis=0))
B = np.array([(2,10)])
print(np.linalg.norm(A[0] - B[0]))

l1 = [[1.2242, 1.4167]]
l2 = [[1.2242, 1.4167]]
l1 = l1 + l2
print(l1)
print(l2)