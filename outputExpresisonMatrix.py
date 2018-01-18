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


# %%
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 3)
print(selected_genes)

print("SICK REDUCED")
plotScatter(sick, selected_genes, gene_labels)

print("HEALTHY REDUCED")
plotScatter(healthy, selected_genes, gene_labels)


# %%
### ALL AT ONCE ###
validation = analyzer.computeFeatureValidation(sick, healthy, selected_genes)
pprint(validation)
expression_matrix = analyzer.computeExpressionMatrix(sick, healthy, selected_genes)
pprint(expression_matrix)



# %%
### ONE vs. REST ###
features = dimReducer.getOneAgainstRestFeatures(sick, healthy, )
pprint(features)
results = analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, features)
pprint(results)
expressions = analyzer.computeExpressionMatrixOneAgainstRest(sick, healthy, features)
pprint(expressions)



#%%
########## SICK OR HEALTHY DATA ONLY ##########
features = dimReducer.getFeatures(healthy, 3)
validation = analyzer.computeFeatureValidation(healthy, '', features)
pprint(validation)
