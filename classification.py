#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.plot import plotScatter

from utils import Expressions


from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator

print("Imported modules")

#%%

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()

clusVal = ClusterValidator()
classVal = ClassificationValidator()
print("data loaded")

#%%
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
selected_genes, sick_X, healthy_X = dimReducer.getEAFeatures(sick,healthy)
print(selected_genes)

#selected_genes = np.array([ 1178, 3349, 15737, 590, 10600, 232, 21125])
#sick_X = sick.expressions[:,selected_genes]
#healthy_X = healthy.expressions[:,selected_genes]


sick_reduced = Expressions(sick_X, sick.labels)
healthy_reduced = Expressions(healthy_X, healthy.labels)

#pprint(clusVal.evaluate(sick_reduced, ["*"], ["*"]))

#print("\n\nSICK COMPLETE")
#pprint(classVal.evaluate(sick, ["LogisticRegression"]))
#print("\n################")

print("SICK REDUCED")
pprint(classVal.evaluate(sick_reduced, ["DecisionTree"]))
plotScatter(sick_X, sick.labels, gene_labels[selected_genes])

print("HEALTHY REDUCED")
pprint(classVal.evaluate(healthy_reduced, ["DecisionTree"]))
plotScatter(healthy_X,healthy.labels, gene_labels[selected_genes])
