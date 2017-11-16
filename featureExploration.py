#%%
%matplotlib inline

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from utils.DataLoader import DataLoader
print("Imported modules")

#%%
# execute me once
# please only pass dataset3 for now
dataLoader = DataLoader("dataset4")
print("data loaded")

#%%
# getData(["healthy","sick"]["all"])
# getData(["TP","NT"]["GBM","LAML"])
data, labels, colors = dataLoader.getData(["sick"],["LUAD", "THCA"])
gene_labels = dataLoader.getGeneLabels()

print("got combined data")

# %%
# PCA Transform
pca = PCA(n_components=3, svd_solver='full')
pca.fit(data)
X = pca.transform(data)
print("LUAD, THCA - sick")
print(pca.explained_variance_ratio_)
print("pca finished")

# %%
# Feature Selection
selector = SelectKBest(chi2, k=3)
selector.fit(data,labels)
indices = selector.get_support(indices=True)
X = data[:,indices]
indices

#%%
pca.components_
print pd.DataFrame(pca.components_,columns=gene_labels,index = ['PC-1','PC-2','PC-3'])
maxIndex = np.argmax(pca.components_[1])
gene_labels[maxIndex]
# %%
# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = X[:,0]
y = X[:,1]
z = X[:,2]

ax.scatter(x,y,z, c=colors, marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
