#%%
import numpy as np
import csv
from pprint import pprint
from datetime import datetime

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, f1_score

from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.EA.fitness import combined_fitness

from utils import Expressions

print("Imported modules")

dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()

print("data loaded")

#%%
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD","GBM"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD","GBM"])
data = dataLoader.getData(["sick", "healthy"], ["THCA","LUAD","GBM"])
gene_labels = dataLoader.getGeneLabels()
print("got combined data")



# %%
K_OPTIONS = [3] # , 5, 10, 20
EXCLUDE_OPTIONS = [100, 500, 1000, 5000, 10000]
M_OPTIONS = [10] # , 50, 100, 500
S_OPTIONS = ["chi2", "f_classif"] #, "mutual_info_classif"
NORM_OPTIONS = ["substract", "exclude"]
F_OPTIONS = ["combined", "classification", "clustering", "distance"]

BASIC_METHODS = {
    "basic": dimReducer.getFeatures,
    #"tree" : dimReducer.getDecisionTreeFeatures,
}

NORMALIZED_METHODS = {
    "subt": dimReducer.getNormalizedFeaturesS,
    "excl": dimReducer.getNormalizedFeaturesE,
}

COMBINED_METHODS = {
    #"ea":  dimReducer.getEAFeatures,
    "sfs": dimReducer.getFeaturesBySFS,
}

ALL_METHODS = {
    "basic": dimReducer.getFeatures,
    "tree":  dimReducer.getDecisionTreeFeatures,
    "norm":  dimReducer.getNormalizedFeaturesS, # SELECT BEST
    "ea":    dimReducer.getEAFeatures,
    "sfs":   dimReducer.getFeaturesBySFS,
}

def get_result_dict(method, k, feature_set, time, statistic="-", normalization="-", exclude="-", preselect="-", fitness_method="-"):
    fitness_score = float(str(combined_fitness(sick, healthy, feature_set))[0:5])

    scoring = { 'f1': make_scorer(f1_score, average='macro') }
    clf = DecisionTreeClassifier()
    scores = cross_validate(clf, sick.expressions[:,feature_set], sick.labels, cv=5, scoring=scoring, return_train_score=False)
    f1 = scores['test_f1'].mean()

    return [method, k, statistic, normalization, exclude, preselect, fitness_method, fitness_score, f1, time, feature_set.tolist()]

def get_basic_results():
    results = []
    for k in K_OPTIONS:
        for method in BASIC_METHODS:
            if method == "basic":
                # get result for each possible statistic
                for stat in S_OPTIONS:
                    start = datetime.now()
                    features = BASIC_METHODS[method](data, k, stat)
                    time = round((datetime.now()-start).total_seconds(),2)

                    result = get_result_dict(method, k, features, time, statistic=stat)
                    results.append(result)

            else:
                start = datetime.now()
                features = BASIC_METHODS[method](data, k)
                time = round((datetime.now()-start).total_seconds(),2)
                
                result = get_result_dict(method, k, features, time)
                results.append(result)

        print("Parameter k: " + str(k) + " is done")
    print("Basic methods are done")
    return results

def get_normalized_results(statistic = "chi2"):
    results = []
    for k in K_OPTIONS:
        for method in NORMALIZED_METHODS:
            if method == "excl":
                # get result for each possible exlude parameter
                for exclude_n in EXCLUDE_OPTIONS:
                    start = datetime.now()
                    features = NORMALIZED_METHODS[method](sick, healthy, k, exclude_n, statistic)
                    time = round((datetime.now()-start).total_seconds(),2)

                    result = get_result_dict(method, k, features, time, statistic=statistic, exclude=exclude_n, normalization="exclude")
                    results.append(result)

            else:
                start = datetime.now()
                features = NORMALIZED_METHODS[method](sick, healthy, k, 42, statistic)
                time = round((datetime.now()-start).total_seconds(),2)
                
                result = get_result_dict(method, k, features, time, statistic=statistic, normalization="substract")
                results.append(result)

    print("Normalized methods are done")
    return results

def get_combined_results(statistic = "chi2", normalization = "exclude", n = 5000):
    results = []
    for k in K_OPTIONS:
        for method in COMBINED_METHODS:
            for m in M_OPTIONS:
                for fit in F_OPTIONS:
            
                    start = datetime.now()
                    features = COMBINED_METHODS[method](sick, healthy, k, n, m, normalization, fit)
                    time = round((datetime.now()-start).total_seconds(),2)
                    
                    result = get_result_dict(method, k, features, time, statistic=statistic, exclude=n, normalization="exclude", preselect=m, fitness_method=fit)
                    results.append(result)

            print("Method " + method + " is done")
        print("Parameter k: " + str(k) + " is done")
    print("Combined methods are done")
    return results


#%%
table = []
table.append(["Method", "K", "Statistic", "Normalization", "Exclude", "Preselect", "Fitness_method", "Fitness_score", "Sick_F1", "Time", "Features"])
table.extend(get_basic_results())
table.extend(get_normalized_results())
table.extend(get_combined_results())

print("table creation done")

# %%

with open("grid_table.csv","w") as f:
    wr = csv.writer(f)
    wr.writerows(table)

print("saved table to file")