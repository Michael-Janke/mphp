#%%
%matplotlib inline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.plot import plotScatter
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
X, pca, pca_indices = dimensionalityReducer.getPCA(data, 3, 20)
print(pca.explained_variance_ratio_)
print("pca finished")

# %%
# Plotting
plotScatter(X,colors,labels)

# %%
# PCA Transform 2
reduced_data = data[:,pca_indices]
X2, pca2, pca_indices2 = dimensionalityReducer.getPCA(reduced_data, 3, 1)
# these pca_indices will be indices to the pca_indices from the pca before
pca_indices2 = pca_indices[pca_indices2]
print(pca2.explained_variance_ratio_)
print("pca finished")

#%%
plotScatter(X2,colors,labels)

# %%
# Feature Selection
X, fs_indices = dimensionalityReducer.getFeatures(data, labels, 20)
gene_labels[fs_indices]


#%%
# compare selected genes
intersection1 = np.intersect1d(fs_indices, pca_indices)
intersection2 = np.intersect1d(fs_indices, pca_indices2)

print("genes in first PCA and FS:")
print(gene_labels[intersection1])
print("genes in second PCA and FS:")
print(gene_labels[intersection2])

#%%
# correlation of selected genes
print("pairwise correlation of genes selected in first PCA:")
print(np.corrcoef(data[:,pca_indices], rowvar = False))
print("pairwise correlation of genes selected in second PCA:")
print(np.corrcoef(data[:,pca_indices2], rowvar = False))
print("pairwise correlation of genes selected in FS:")
print(np.corrcoef(data[:,fs_indices], rowvar = False))
