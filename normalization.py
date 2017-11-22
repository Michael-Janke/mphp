#%%
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
print("Imported modules")

#%%
# execute me once
dataLoader = DataLoader("dataset4")
dimensionalityReducer = DimensionalityReducer()
print("data loaded")

#%%
healthy_data, healthy_labels, healthy_colors = dataLoader.getData(["healthy"],["LUAD", "THCA"])
sick_data, sick_labels, sick_colors = dataLoader.getData(["sick"],["LUAD", "THCA"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
healthy_X, healthy_fs_indices = dimensionalityReducer.getFeatures(healthy_data, healthy_labels, 100)
sick_X, sick_fs_indices = dimensionalityReducer.getFeatures(sick_data, sick_labels, 100)
print("feature selection done")

# compare selected genes
intersection = np.intersect1d(healthy_fs_indices, sick_fs_indices)
print(intersection.size)
print(gene_labels[intersection])