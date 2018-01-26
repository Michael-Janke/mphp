import pandas as pd
import sklearn.cluster
import matplotlib.pyplot as plt
import numpy as np
import sys
import re
from collections import defaultdict

data = pd.read_csv("plots/experiment1.csv", sep=",").fillna('')

tree = defaultdict(list)
basic_chi2 = defaultdict(list)
basic_f1 = defaultdict(list)
basic_mi = defaultdict(list)

algorithm = {
    "tree-": tree,
    "basic-chi2": basic_chi2,
    "basic-f_classif": basic_f1,
    "basic-mutual_info_classif": basic_mi,
}

for row in data.iterrows():
    used_selection = row[1]["Method"] + "-" + row[1]["Statistic"]
    print(used_selection)
    if row[1]["Normalization"]:
        continue
    if not used_selection in algorithm:
        continue
    algorithm[used_selection]["K"] += [row[1]["K"]]
    algorithm[used_selection]["Fitness_score"] += [row[1]["Fitness_score"]]
    algorithm[used_selection]["Time"] += [row[1]["Time"]]

plt.scatter(basic_chi2["K"], basic_chi2["Fitness_score"], label="chi²")
plt.scatter(basic_f1["K"], basic_f1["Fitness_score"], label="f_classif")
plt.scatter(basic_mi["K"], basic_mi["Fitness_score"], label="mutual_info_classif")
plt.scatter(tree["K"], tree["Fitness_score"], label="tree")

plt.xlabel("Number of Features")
plt.ylabel("Fitness Score")
plt.legend(loc="upper left", ncol=4)
plt.savefig("plots/basicVStree_fitness.pdf")
plt.show()

plt.clf()

plt.scatter(basic_chi2["K"], basic_chi2["Time"], label="chi²")
plt.scatter(basic_f1["K"], basic_f1["Time"], label="f_classif")
plt.scatter(basic_mi["K"], basic_mi["Time"], label="mutual_info_classif")
plt.scatter(tree["K"], tree["Time"], label="tree")

plt.xlabel("Number of Features")
plt.ylabel("Fitness Score")
plt.yscale("log")
plt.ylim((0,2000))
plt.legend(loc="upper left", ncol=4)
plt.savefig("plots/basicVStree_time.pdf")
plt.show()
