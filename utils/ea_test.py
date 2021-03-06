# %%
import numpy as np
from pprint import pprint

from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.EA.crossover import *
from utils.EA.mutation import *
from utils.EA.algorithm import ea_for_plot, run
from utils.EA.fitness import fitness
from utils.EA.ea_utils import display_stat_1
from utils.EA.population import phenotype
import utils.EA.config as c

from utils import Expressions

print("import successful")

# %%
dataLoader = DataLoader("dataset4")
dimReducer = DimensionalityReducer()

healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
gene_labels = dataLoader.getGeneLabels()

print("got data")

# %%
chromo_size = c.chromo_size
selected_genes = dimReducer.getNormalizedFeatures(sick,healthy,"substract", chromo_size, chromo_size)
print("preselected genes")


#%%
### PARAMS FOR EA
if c.crossover == "uniform":
    crossover = uniform_crossover
elif c.crossover == "two_points":
    crossover = two_points_crossover
else:
    crossover = one_point_crossover

mutation = binary_mutation

sick_reduced = Expressions(sick.expressions[:, selected_genes], sick.labels)
healthy_reduced = Expressions(healthy.expressions[:, selected_genes], healthy.labels)

fitness_function = fitness(sick_reduced, healthy_reduced)

best, sets, stat, stat_aver = ea_for_plot(c, chromo_size, 3, fitness_function, crossover, mutation)

display_stat_1(stat, stat_aver)
print(best[0])
print(phenotype(best), best[1])
print(sets)
features = selected_genes[phenotype(best)]
print(features)
