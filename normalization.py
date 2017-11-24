#%%
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.plot import plotScatter
print("Imported modules")

#%%
# execute me once
dataLoader = DataLoader("dataset4")
dimensionalityReducer = DimensionalityReducer()
print("data loaded")

#%%
healthy_data, healthy_labels, healthy_colors = dataLoader.getData(["healthy"],["all"],["LAML"])
sick_data, sick_labels, sick_colors = dataLoader.getData(["sick"],["all"],["LAML"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
healthy_X, healthy_fs_indices = dimensionalityReducer.getFeatures(healthy_data, healthy_labels, 3)
sick_X, sick_fs_indices = dimensionalityReducer.getFeatures(sick_data, sick_labels, 3)
print("feature selection done")

# compare selected genes
intersection = np.intersect1d(healthy_fs_indices, sick_fs_indices)
print(intersection.size)
print(gene_labels[intersection])

#%%
plotScatter(healthy_X,healthy_colors,healthy_labels)
plotScatter(sick_X,sick_colors,sick_labels)

healthy_X2 = healthy_data[:, sick_fs_indices]
sick_X2 = sick_data[:, healthy_fs_indices]

plotScatter(healthy_X2,healthy_colors,healthy_labels)
plotScatter(sick_X2,sick_colors,sick_labels)
print("plotting done")
print("")




# NORMALIZING DATA BEFORE PLOTTING AGAIN
# SICK SHOULD STILL BE DISCRIMINATED
# HEALTHY SHOULD BE ALMOST UNIFORM
#%%
dataNormalizer = DataNormalizer()
sick_norm, sick_norm_labels = dataNormalizer.normalizeDataWithMean(sick_data, healthy_data, sick_labels, healthy_labels)

sick_X_norm, sick_fs_indices_norm = dimensionalityReducer.getFeatures(sick_norm, sick_norm_labels, 3)
plotScatter(sick_X_norm,sick_colors,sick_norm_labels)

sick_X3 = sick_data[:,sick_fs_indices_norm]
plotScatter(sick_X3,sick_colors,sick_labels)

healthy_X3 = healthy_data[:,sick_fs_indices_norm]
plotScatter(healthy_X3,healthy_colors,healthy_labels)

#%%
sick_labels