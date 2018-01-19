#%%
import numpy as np
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
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

plotScatter(healthy, selected_genes, gene_labels)


# %%
from imblearn.over_sampling import SMOTE

class Sampler:
    def over_sample(self, data, kind="regular", min_samples=20, change_labels=False):
        # kind: 'regular', 'borderline1', 'borderline2', 'svm'

        original_counts = self.get_label_counts(data)
        min_count = min(original_counts.values())

        desired_counts = self.get_label_counts(data, adjust=True, min_samples=min_samples)
        sampler = SMOTE(ratio = desired_counts, k_neighbors=min_count-1, kind=kind)

        X, y = sampler.fit_sample(data.expressions, data.labels)

        y = y if not change_labels else self.change_labels(y, data.labels.shape[0])

        return Expressions(X, y)

    def get_label_counts(self, data, adjust=False, min_samples=20):
        label_dict = {}
        labels = np.unique(data.labels, return_counts = True)
        for index, label in enumerate(labels[0]):
            if adjust:
                label_dict[label] = max(labels[1][index], min_samples)
            else:
                label_dict[label] = labels[1][index]

        return label_dict

    def change_labels(self, labels, original_counts):
        suffix = "-sampled"
        n_chars_label = int(str(labels.dtype).split("U")[-1]) + len(suffix)
        labels = labels.astype("<U"+str(n_chars_label))

        labels[original_counts:] = np.core.defchararray.add(labels[original_counts:], suffix)
        return labels



sampler = Sampler()

sampled = sampler.over_sample(healthy, change_labels=True)
plotScatter(sampled, selected_genes, gene_labels)

print(sampler.get_label_counts(sampled))

print(sampled.labels)