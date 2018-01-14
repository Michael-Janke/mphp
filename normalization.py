#%%
import numpy as np
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.plot import plotScatter
print("Imported modules")

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
healthy_fs_indices = dimReducer.getFeatures(healthy, 3)
sick_fs_indices = dimReducer.getFeatures(sick, 3)
print("feature selection done")

# compare selected genes
intersection = np.intersect1d(healthy_fs_indices, sick_fs_indices)
print(intersection.size)
print(gene_labels[intersection])

#%%
plotScatter(healthy, healthy_fs_indices, gene_labels)
plotScatter(sick, sick_fs_indices, gene_labels)

plotScatter(healthy, sick_fs_indices, gene_labels)
plotScatter(sick, healthy_fs_indices, gene_labels)

print("plotting original done")




# NORMALIZING DATA BEFORE PLOTTING AGAIN
# SICK SHOULD STILL BE DISCRIMINATED
# HEALTHY SHOULD BE ALMOST UNIFORM
#%%
dataNormalizer = DataNormalizer()
sick_norm = dataNormalizer.normalizeDataWithMean(sick, healthy)

sick_fs_indices_norm = dimReducer.getFeatures(sick_norm, 3)
plotScatter(sick_norm, sick_fs_indices_norm, gene_labels)

plotScatter(sick, sick_fs_indices_norm, gene_labels)


healthy_X3 = healthy.expressions[:,sick_fs_indices_norm]
plotScatter(healthy, sick_fs_indices_norm, gene_labels)
print("plotting normalized data done")

#%%
# NORMALIZING TAKES PLACES INSIDE THE FEATURE SELECTION HERE
method = "substract"
selected_genes = dimReducer.getNormalizedFeatures(sick, healthy, method, 3, 5000)
plotScatter(healthy, selected_genes, gene_labels)
plotScatter(sick, selected_genes, gene_labels)
print("plotting with normalized features done - " + method)
