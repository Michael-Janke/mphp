import pandas as pd
import sklearn.cluster
import matplotlib.pyplot as plt
import numpy as np
import sys
import re
from collections import defaultdict
import ast

data = pd.read_csv("plots/experiment2.csv", sep=",").fillna('')

genes = defaultdict(int)
size = len(data)

for row in data.iterrows():
    for gene in ast.literal_eval(row[1]["Features"]):
        genes[gene] += 1

genes = {k: (v/size) for k,v in genes.items()}
genes = {k:v for k,v in genes.items() if v > 5 /size}

plt.bar(range(len(genes)), list(genes.values()), align='center')
plt.xticks(range(len(genes)), list(genes.keys()), rotation=90)
plt.savefig("plots/test.pdf")
plt.show()
