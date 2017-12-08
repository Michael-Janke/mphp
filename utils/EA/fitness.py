from population import phenotype

def fitness(data, labels):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        selected_data = []
        
        return evaluate(selected_data, labels)
    return fitness_

def evaluate(data, labels):
    fitness = 0

    return fitness