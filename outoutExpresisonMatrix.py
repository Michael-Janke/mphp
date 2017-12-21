#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.Analyzer import Analyzer
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
selected_genes, sick_X, healthy_X = dimReducer.getFaturesBySFS(sick,healthy,3)
print(selected_genes)

sick_reduced = Expressions(sick_X, sick.labels)
healthy_reduced = Expressions(healthy_X, healthy.labels)

print("SICK REDUCED")
plotScatter(sick_X, sick.labels, gene_labels[selected_genes])

print("HEALTHY REDUCED")
plotScatter(healthy_X,healthy.labels, gene_labels[selected_genes])



# %%
# EXPRESSION RELATIVE ACCORDING TO SICK DATA AND TYPES
expression_levels = {
    1:   "high",
    0.8: "mid-high",
    0.6: "neutral",
    0.4: "mid-low",
    0.2: "low",
}

normalized_Data = sick_X / np.max(sick_X)
data = {"genes": gene_labels[selected_genes].tolist()}

for label in np.unique(sick.labels):
    indices = np.where(sick.labels == label)
    medians = np.median(normalized_Data[indices,:], axis=1).tolist()[0]
    expressions = []
    for median in medians:
        expressions.append(expression_levels[np.ceil(median*5)/5])
    data[label] = expressions

pprint(data)


#%%
expression_matrix = analyzer.computeExpressionMatrix(sick_reduced, healthy, selected_genes)
pprint(expression_matrix)
