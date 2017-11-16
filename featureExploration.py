#%%
%matplotlib inline

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from utils.DataLoader import DataLoader
print("Imported modules")

#%%
# execute me once
# please only pass dataset3 for now
dataLoader = DataLoader("dataset3")
print("data loaded")

#%%
# getData(["all"])
# getData(["GBM","LAML"])
data, labels, colors = dataLoader.getData(["TP", "NT"],["GBM"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# PCA Transform
pca = PCA(n_components=3, svd_solver='full')
pca.fit(data)
X = pca.transform(data)
pca.explained_variance_ratio_
print("pca finished")

# %%
# Feature Selection
selector = SelectKBest(chi2, k=3)
selector.fit(data,labels)
indices = selector.get_support(indices=True)
X = data[:,indices]
indices

#%%
gene_labels[indices]

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
