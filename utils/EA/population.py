import numpy as np
from random import randint
from .config import population_size

### POPULATION CREATION ###
def generate_population(size_cromo, size_pop = population_size):
    return [ (generate_indiv(size_cromo), 0) for i in range(size_pop)]

def generate_indiv(size_cromo):
    # random initialization
    indiv = [0 for i in range(size_cromo)]

    for i in range(10):
        indiv[randint(0,size_cromo-1)] = 1

    return indiv


### CONVERSION ###
def phenotype(indiv):
    #should return indices of ones
    selected_features = [i for i, x in enumerate(indiv[0]) if x == 1]
    return np.array(selected_features)