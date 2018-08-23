from datetime import datetime
import pandas as pd

from utils.DataLoader import DataLoader
from validation.GridSearch import GridSearch
from validation.Analyzer import Analyzer

import ast

start = datetime.now()


print("Imported modules", flush=True)

dataLoader = DataLoader("dataset4")

healthy = dataLoader.getData(["healthy"], ["all"], excluded_cancer_types = ["CESC"])
sick = dataLoader.getData(["sick"], ["all"], excluded_cancer_types = ["CESC"])
data = dataLoader.getData(["sick", "healthy"], ["all"], excluded_cancer_types = ["CESC"])

print(data.labels)
print(any(["CESC" in label for label in data.labels]))


ana = Analyzer()

fdata = pd.read_csv("/home/lukas/studium/masterproject/mphp/results/table4.csv", sep=";").fillna('')
outfile = open("/home/lukas/studium/masterproject/mphp/results/fitnesses.csv", "w")

fields = ["Method","K","Statistic","Normalization","Exclude","Preselect","Fitness_method","Class_fitness","Clus_fitness","SvH_fitness","Fitness_score","Sick_F1","Time","Features"]
outfile.write(";".join(fields) + "\n")

fs = {"classificationFitness": "Class_fitness", "clusteringFitness": "Clus_fitness", "sickVsHealthyFitness": "SvH_fitness"}

for i,line in fdata.iterrows():
    newline = {}
    for key in line.keys():
        newline[key] = line[key]
    features = ast.literal_eval(line["Features"])
    fitnesses = ana.computeFeatureValidation(sick, healthy, features)["fitness"]
    for f in fitnesses:
        if f in fs:
            newline[fs[f]]=fitnesses[f]
    outfile.write(";".join(map(str, [newline[key] for key in fields])) + "\n")



"""
grid_search = GridSearch(sick, healthy, data, "results/test.csv")
print("got combined data", flush=True)

grid_search.get_table_all_at_once()
print("table creation done", flush=True)

#grid_search.save_table_to_disk(table, "chi²")
print("saved table to file", flush=True)

table = grid_search.get_table_one_vs_rest()
print("table creation done", flush=True)

grid_search.save_table_to_disk(table, "grid_search_one_vs_rest_big")
print("saved table to file", flush=True)

print(datetime.now() - start)
"""
