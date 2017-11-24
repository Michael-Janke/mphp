#%%
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.plot import plotScatter
print("Imported modules")

#%%
# execute me once
dataLoader = DataLoader("dataset4")
dimensionalityReducer = DimensionalityReducer()
print("data loaded")

#%%
healthy_data, healthy_labels, healthy_colors = dataLoader.getData(["healthy"],["LUAD", "KIRC"])
sick_data, sick_labels, sick_colors = dataLoader.getData(["sick"],["LUAD", "KIRC"])
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



# NORMALIZING DATA BEFORE PLOTTING AGAIN
# SICK SHOULD STILL BE DISCRIMINATED
# HEALTHY SHOULD BE ALMOST UNIFORM

#%%
healthy_luad, _, _ = dataLoader.getData(["healthy"],["LUAD"])
healthy_thca, _, _ = dataLoader.getData(["healthy"],["KIRC"])
sick_luad, _, _ = dataLoader.getData(["sick"],["LUAD"])
sick_thca, _, _ = dataLoader.getData(["sick"],["KIRC"])

sick_thca_norm = sick_thca - np.mean(healthy_thca, axis=0)
sick_thca_norm = sick_thca_norm + np.absolute(np.min(sick_thca_norm))
sick_luad_norm = sick_luad - np.mean(healthy_luad, axis=0)
sick_luad_norm = sick_luad_norm + np.absolute(np.min(sick_luad_norm))
sick_normalized = np.concatenate((sick_luad_norm, sick_thca_norm), axis=0)

sick_X_norm, sick_fs_indices_norm = dimensionalityReducer.getFeatures(sick_normalized, sick_labels, 3)
plotScatter(sick_X_norm,sick_colors,sick_labels)

sick_X3 = sick_data[:,sick_fs_indices_norm]
plotScatter(sick_X3,sick_colors,sick_labels)

healthy_X3 = healthy_data[:,sick_fs_indices_norm]
plotScatter(healthy_X3,healthy_colors,healthy_labels)

#%%
intersection = np.intersect1d(sick_fs_indices_norm, healthy_fs_indices)
print(intersection)
print(gene_labels[intersection])

#%%
np.mean(healthy_thca, axis=0).shape

#%%
gene_labels[sick_fs_indices_norm]