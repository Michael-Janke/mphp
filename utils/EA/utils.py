import matplotlib.pyplot as plt
from operator import itemgetter

### MINIMIZATION ###
def best_pop(pop):
    pop.sort(key=itemgetter(1),reverse=False)

    return pop[0]

def average_pop(population):
    return sum([fit for cromo,fit in population])/len(population)



### Plotting ###
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def display_stat_1(best,average):
    generations = list(range(len(best)))
    plt.title('Performance over generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.show()
    
def display_stat_n(boa,average_best):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.show()