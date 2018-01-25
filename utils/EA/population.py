import numpy as np
from random import randint
from .config import population_size

### POPULATION CREATION ###
def generate_population(size_cromo, k, size_pop = population_size):
    return [ (generate_indiv(size_cromo, k), 0) for i in range(size_pop)]

def generate_indiv(size_cromo, k):
    # random initialization
    indiv = [0 for i in range(size_cromo)]

    for i in range(k):
        indiv[randint(0,size_cromo-1)] = 1

    return indiv


### CONVERSION ###
def phenotype(indiv):
    #should return indices of ones
    selected_features = [i for i, x in enumerate(indiv[0]) if x == 1]
    if len(selected_features) == 0:
        selected_features = [ randint(0, len(indiv[0])) ]
    return np.array(selected_features)