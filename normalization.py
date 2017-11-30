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
dimReducer = DimensionalityReducer()
print("data loaded")

#%%
healthy_data, healthy_labels = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick_data, sick_labels = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
healthy_fs_indices, healthy_X = dimReducer.getFeatures(healthy_data, healthy_labels, 3)
sick_fs_indices, sick_X = dimReducer.getFeatures(sick_data, sick_labels, 3)
print("feature selection done")

# compare selected genes
intersection = np.intersect1d(healthy_fs_indices, sick_fs_indices)
print(intersection.size)
print(gene_labels[intersection])

#%%
plotScatter(healthy_X,healthy_labels)
plotScatter(sick_X,sick_labels)

healthy_X2 = healthy_data[:, sick_fs_indices]
sick_X2 = sick_data[:, healthy_fs_indices]

plotScatter(healthy_X2,healthy_labels)
plotScatter(sick_X2,sick_labels)
print("plotting original done")




# NORMALIZING DATA BEFORE PLOTTING AGAIN
# SICK SHOULD STILL BE DISCRIMINATED
# HEALTHY SHOULD BE ALMOST UNIFORM
#%%
dataNormalizer = DataNormalizer()
sick_norm, sick_norm_labels = dataNormalizer.normalizeDataWithMean(sick_data, healthy_data, sick_labels, healthy_labels)

sick_fs_indices_norm, sick_X_norm = dimReducer.getFeatures(sick_norm, sick_norm_labels, 3)
plotScatter(sick_X_norm,sick_norm_labels)

sick_X3 = sick_data[:,sick_fs_indices_norm]
plotScatter(sick_X3,sick_labels)

healthy_X3 = healthy_data[:,sick_fs_indices_norm]
plotScatter(healthy_X3,healthy_labels)
print("plotting normalized data done")

#%%
# NORMALIZING TAKES PLACES INSIDE THE FEATURE SELECTION HERE
method = "exclude"
idx, h_data, s_data = dimReducer.getNormalizedFeatures(healthy_data, sick_data, healthy_labels, sick_labels, method, 3, 1000)
plotScatter(h_data, healthy_labels)
plotScatter(s_data, sick_labels)
print("plotting with normalized features done - "+method)
