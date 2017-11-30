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
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
healthy_fs_indices, healthy_X = dimReducer.getFeatures(healthy, 3)
sick_fs_indices, sick_X = dimReducer.getFeatures(sick, 3)
print("feature selection done")

# compare selected genes
intersection = np.intersect1d(healthy_fs_indices, sick_fs_indices)
print(intersection.size)
print(gene_labels[intersection])

#%%
plotScatter(healthy_X,healthy.labels)
plotScatter(sick_X,sick.labels)

healthy_X2 = healthy.expressions[:, sick_fs_indices]
sick_X2 = sick.expressions[:, healthy_fs_indices]

plotScatter(healthy_X2,healthy.labels)
plotScatter(sick_X2,sick.labels)
print("plotting original done")




# NORMALIZING DATA BEFORE PLOTTING AGAIN
# SICK SHOULD STILL BE DISCRIMINATED
# HEALTHY SHOULD BE ALMOST UNIFORM
#%%
dataNormalizer = DataNormalizer()
sick_norm = dataNormalizer.normalizeDataWithMean(sick, healthy)

sick_fs_indices_norm, sick_X_norm = dimReducer.getFeatures(sick_norm, 3)
plotScatter(sick_X_norm,sick_norm.labels)

sick_X3 = sick.expressions[:,sick_fs_indices_norm]
plotScatter(sick_X3,sick.labels)

healthy_X3 = healthy.expressions[:,sick_fs_indices_norm]
plotScatter(healthy_X3,healthy.labels)
print("plotting normalized data done")

#%%
# NORMALIZING TAKES PLACES INSIDE THE FEATURE SELECTION HERE
method = "subtract"
idx, s_data, h_data = dimReducer.getNormalizedFeatures(sick, healthy, method, 3, 5000)
plotScatter(h_data, healthy.labels)
plotScatter(s_data, sick.labels)
print("plotting with normalized features done - " + method)
