from population import phenotype

def fitness(dimension):
    def fitness_(indiv):
        return evaluate(phenotype(indiv),dimension)
    return fitness_

def evaluate(pheno,dimension):
    conflicts = 0

    #There are no conflicts inside the sub-boxes as the algorithm is implemented to keep this constraint
    #conflicts += calculateRowConflicts(pheno,dimension)
    #conflicts += calculateColumnConflicts(pheno,dimension)
    #conflicts += calculateDiagonalConflicts(pheno,dimension)

    return conflicts