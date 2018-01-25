#%%
from __future__ import print_function, division
import numpy as np
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA

from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()

healthy = dataLoader.getData(["healthy"], ["THCA","LUAD","GBM"])

sick = dataLoader.getData(["sick"], ["THCA","LUAD","GBM"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")


# %%
start = datetime.now()

pipe = Pipeline([
    ('reduce_dim', DimensionalityReducer(sick, healthy)),
    ('classify', LinearSVC())
])

N_FEATURES_OPTIONS = [2, 4, 8]

param_grid = [
    {
        'reduce_dim': [DimensionalityReducer(sick, healthy)]
    },
]
reducer_labels = ['KBest(chi2)']

grid = GridSearchCV(pipe, cv=3, n_jobs=3, param_grid=param_grid)
grid.fit(sick.expressions, sick.labels)
mean_scores = np.array(grid.cv_results_['mean_test_score'])

pprint(mean_scores)

print(datetime.now() - start)