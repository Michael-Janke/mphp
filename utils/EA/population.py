from random import randint

### POPULATION CREATION ###
def gera_pop(size_pop,size_cromo):
    return [(gera_indiv(size_cromo),0) for i in range(size_pop)]

def gera_indiv(size_cromo):
    # random initialization
    indiv = [randint(0,1) for i in range(size_cromo)]
    return indiv


### CONVERSION ###
def phenotype(indiv):
    #should be the same as the genotype
    return indiv