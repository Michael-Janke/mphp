import matplotlib.pyplot as plt
from operator import itemgetter

from config import maximization

### UTILS ###
def best_indiv(population):
    population.sort(key=itemgetter(1),reverse=maximization)
    return population[0]

def average_indiv(population):
    return sum([fitness for _, fitness in population]) / len(population)



### Plotting ###
def display_stat_1(best, average):
    generations = list(range(len(best)))
    plt.title('Performance over generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations, average, label='Average')
    plt.legend(loc='best')
    plt.show()
    
def display_stat_n(best, average_best):
    generations = list(range(len(best)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best of All')
    plt.plot(generations, average_best, label='Average of Bests')
    plt.legend(loc='best')
    plt.show()