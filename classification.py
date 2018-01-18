#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.plot import plotScatter

from utils import Expressions

from validation.Analyzer import Analyzer
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator

print("Imported modules")

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()
analyzer = Analyzer()

clusVal = ClusterValidator()
classVal = ClassificationValidator()
print("data loaded")

#%%
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD","GBM"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD","GBM"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
features = dimReducer.getOneAgainstRestFeatures(sick,healthy)
pprint(features)

results = analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, features)
pprint(results)

expressions = analyzer.computeExpressionMatrixOneAgainstRest(sick, healthy, features)
pprint(expressions)



# %%
# Feature Selection
#selected_genes = dimReducer.getEAFeatures(sick,healthy,fitness="clustering")
selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 3, fitness="classification")
print(selected_genes)

print("SICK REDUCED")
pprint(classVal.evaluate(sick, selected_genes, ["DecisionTree"]))
plotScatter(sick, selected_genes, gene_labels)

print("HEALTHY REDUCED")
pprint(classVal.evaluate(healthy, selected_genes, ["DecisionTree"]))
plotScatter(healthy, selected_genes, gene_labels)

# %%
pprint(analyzer.computeFeatureValidation(sick, healthy, selected_genes)["fitness"])

# %%
#selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 3, fitness="classification", returnMultipleSets = True)
selected_genes = dimReducer.getEAFeatures(sick, healthy, fitness="distance", returnMultipleSets = True)
pprint(selected_genes)