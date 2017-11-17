#%%
%matplotlib inline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
print("Imported modules")

#%%
# execute me once
# please only pass dataset3|4 for now
dataLoader = DataLoader("dataset4")
dimensionalityReducer = DimensionalityReducer()
print("data loaded")

#%%
# getData(["healthy","sick"]["all"])
# getData(["TP","NT"]["GBM","LAML"])
data, labels, colors = dataLoader.getData(["sick","healthy"],["LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# PCA Transform
n_components = 3
n_features_per_component = 10
X, pca, pca_indices = dimensionalityReducer.getPCA(data, n_components, n_features_per_component)
print(pca.explained_variance_ratio_)
print("pca finished")

# %%
# Feature Selection
X, indices = dimensionalityReducer.getFeatures(data, labels, 100)
fs_indices

# %%
# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

unique_colors = np.unique(colors)
for i, label in enumerate(np.unique(labels)):
    indices = np.where(label == labels)
    x = X[indices,0]
    y = X[indices,1]
    z = X[indices,2]
    ax.scatter(x,y,z, c=unique_colors[i], label=label)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

plt.legend()
plt.tight_layout()
plt.show()


# %%
# PCA Transform 2
smallerData = data[:,pca_indices]
X2, pca2, pca_indices2 = dimensionalityReducer.getPCA(data, n_components, n_features_per_component)


#%%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

unique_colors = np.unique(colors)
for i, label in enumerate(np.unique(labels)):
    indices = np.where(label == labels)
    x = X2[indices,0]
    y = X2[indices,1]
    z = X2[indices,2]
    ax.scatter(x,y,z, c=unique_colors[i], label=label)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

plt.legend()
plt.tight_layout()
plt.show()