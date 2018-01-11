#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from validation.Analyzer import Analyzer
from utils.plot import plotScatter

from utils import Expressions
print("Imported modules")

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()
analyzer = Analyzer()
print("data loaded")

healthy = dataLoader.getData(["healthy"], ["THCA","LUAD","KIRC"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD","KIRC"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
selected_genes, sick_X, healthy_X = dimReducer.getFeaturesBySFS(sick,healthy,3)
print(selected_genes)

sick_reduced = Expressions(sick_X, sick.labels)
healthy_reduced = Expressions(healthy_X, healthy.labels)

print("SICK REDUCED")
plotScatter(sick_X, sick.labels, gene_labels[selected_genes])

print("HEALTHY REDUCED")
plotScatter(healthy_X,healthy.labels, gene_labels[selected_genes])
#%%
validation = analyzer.computeFeatureValidation(sick, healthy, selected_genes)
pprint(validation)

#%%
expression_matrix = analyzer.computeExpressionMatrix(sick_reduced, healthy, selected_genes)
pprint(expression_matrix)


#%%
########## SICK OR HEALTHY DATA ONLY ##########
features, data_reduced_X = dimReducer.getFeatures(healthy, 3)
data_reduced = Expressions(data_reduced_X, healthy.labels)
validation = analyzer.computeFeatureValidation(healthy, '', features)
pprint(validation)


# %%
features = dimReducer.getOneAgainstRestFeatures(healthy, '', 3)
pprint(features)
results = analyzer.computeFeatureValidationOneAgainstRest(healthy, '', features)
pprint(results)
