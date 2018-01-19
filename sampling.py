#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.Sampler import Sampler
from utils.plot import plotScatter

from utils import Expressions

from validation.Analyzer import Analyzer

print("Imported modules")

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()
analyzer = Analyzer()

print("data loaded")

#%%
healthy = dataLoader.getData(["healthy"], ["THCA","SARC","LUAD","GBM"])
#sick = dataLoader.getData(["sick"], ["THCA","GBM"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
selected_genes = dimReducer.getFeatures(healthy)
print("Unsampled")
plotScatter(healthy, selected_genes, gene_labels)


# %%
sampler = Sampler()
print("Standard Sampling")

sampled = sampler.over_sample(healthy, change_labels=True)
plotScatter(sampled, selected_genes, gene_labels)


#%%
samples = sampler.get_different_samples(healthy)
methods = sampler.get_sample_methods()
for index, sample in enumerate(samples):
    print("Method: " + methods[index])
    plotScatter(sample, selected_genes, gene_labels)
