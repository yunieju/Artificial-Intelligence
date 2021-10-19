import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

# read data from a given txt file
data = pd.read_csv('./B.txt', sep=" ", header=None)
data.rename(columns={0: 'X', 1:'Y'}, inplace=True)

print(data)

ac = AgglomerativeClustering(n_clusters=2, linkage='single')
plt.figure(figsize=(8,8))
plt.scatter(data['X'], data['Y'],
           c = ac.fit_predict(data), cmap ='rainbow')
plt.show()





