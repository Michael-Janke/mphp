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
dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()

clusVal = ClusterValidator()
classVal = ClassificationValidator()
print("data loaded")

healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")

# %%
# Feature Selection
#selected_genes, sick_X, healthy_X = dimReducer.getEAFeatures(sick,healthy)
selected_genes, sick_X, healthy_X = dimReducer.getFaturesBySFS(sick,healthy,3)
print(selected_genes)

#selected_genes = np.array([ 1178, 3349, 15737, 590, 10600, 232, 21125])
#sick_X = sick.expressions[:,selected_genes]
#healthy_X = healthy.expressions[:,selected_genes]


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



# %%
# GENE EXPRESSION RELATIVE TO HEALTHY DATA
levels = {}
for gene in selected_genes:
    min_thresh = np.min(healthy.expressions[:,gene])
    max_thresh = np.max(healthy.expressions[:,gene])
    lower_thresh = np.percentile(healthy.expressions[:,gene], 30)
    upper_thresh = np.percentile(healthy.expressions[:,gene], 70)
    levels[gene] = [min_thresh, lower_thresh, upper_thresh, max_thresh]

pprint(levels)

data = {"genes": gene_labels[selected_genes].tolist()}
for label in np.unique(sick.labels):
    indices = np.where(sick.labels == label)
    medians = np.median(sick_X[indices,], axis=1).tolist()[0]
    expressions = []
    for index, median in enumerate(medians):
        thresholds = levels[selected_genes[index]]
        if median < thresholds[0]:
            expressions.append("lower")
        elif median < thresholds[1]:
            expressions.append("mid-lower")
        elif median < thresholds[2]:
            expressions.append("unchanged")
        elif median < thresholds[3]:
            expressions.append("mid-higher")
        else:
            expressions.append("higher")

    data[label] = expressions

pprint(data)