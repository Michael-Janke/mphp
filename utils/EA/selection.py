from random import sample
from operator import itemgetter
from .config import maximization, tour_size, elite_percentage

# Parents Selection: tournament
def tournament(population):
    mate_pool = []
    for i in range(len(population)):
        winner = one_tour(population)
        mate_pool.append(winner)
    return mate_pool

def one_tour(population):
    pool = sample(population, tour_size)
    pool.sort(key=itemgetter(1), reverse=maximization)
    return pool[0]


# Survivals Selection: elitism
def elitism(parents, offspring):
    size = len(parents)
    size_elitists = int(size * elite_percentage)
    offspring.sort(key=itemgetter(1), reverse=maximization)
    parents.sort(key=itemgetter(1), reverse=maximization)
    new_population = parents[:size_elitists] + offspring[:size - size_elitists]
    return new_population