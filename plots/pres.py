import pandas as pd
import sklearn.cluster
import matplotlib.pyplot as plt
import numpy as np
import sys
import re
from collections import defaultdict

data = pd.read_csv("plots/pres_binary.csv", sep=",").fillna('')

basic = defaultdict(list)
subt = defaultdict(list)
excl = defaultdict(list)
sfs = defaultdict(list)
ea = defaultdict(list)
tree = defaultdict(list)
reflieff = defaultdict(list)

algorithm = {
    "basic": basic,
    "subt": subt,
    "excl": excl,
    "sfs": sfs,
    "ea": ea,
    "tree": tree,
    "relief": reflieff,
}


markers = "dso^*ph"
names = {
    "basic": "Feature Selection",
    "subt": "Subtract",
    "excl": "Exclude",
    "sfs": "Greedy",
    "ea": "Evolutionary",
    "tree": "Decision Tree",
    "relief": "ReliefF"
}

for row in data.iterrows():
    method = row[1]["Method"]
    if method:
        algorithm[method]["Fitness_score"] += [row[1]["Fitness_score"]]
        algorithm[method]["K"] += [row[1]["K"]]
        algorithm[method]["Time"] += [row[1]["Time"]]

for i, key in enumerate(algorithm):
    plt.scatter(algorithm[key]["K"],algorithm[key]["Fitness_score"], marker=markers[i], label=names[key])



plt.xlabel("Number of Features")
plt.ylabel("Fitness Score")
plt.legend(loc="best",fancybox=True, framealpha=0.5)
plt.savefig("plots/pres.png", dpi=600)
plt.show()
plt.ylim((0.4, 5))
plt.clf()

for i,key in enumerate(algorithm):
    plt.scatter(algorithm[key]["K"], algorithm[key]["Time"], marker=markers[i], label=names[key])

plt.xlabel("Number of Features")
plt.ylabel("Time (s)")
plt.yscale("log",fancybox=True, framealpha=0.5)
plt.ylim((0,1200))
plt.legend(loc="best")
plt.savefig("plots/pres_time.png", dpi=600)
plt.show()
