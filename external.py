from server.externalApiCalls import fullTestGenes
from utils.DataLoader import DataLoader

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import re
import ast
from collections import defaultdict

infile = open("results/fitnesses3.csv", "r")
outfile = open("results/sickf1.csv", "w")

fields = ["Method","K","Statistic","Normalization","Exclude","Preselect","Fitness_method","Class_fitness","Clus_fitness","SvH_fitness","Fitness_score","Sick_F1","External","Time","Features"]
outfile.write(";".join(fields) + "\n")

genelabels = DataLoader("dataset4").getGeneLabels()

fdata = pd.read_csv("results/fitnesses3.csv", sep=";").fillna('')

for i,row in fdata.iterrows():
    genes = [genelabels[g] for g in ast.literal_eval(row["Features"])]
    external = fullTestGenes(genes, None)
    score = np.mean([external[gene]["score"] for gene in external])
    newline = {}
    newline["External"] = score
    for key in row.keys():
        newline[key] = row[key]
    outfile.write(";".join(map(str, [newline[key] for key in fields])) + "\n")

