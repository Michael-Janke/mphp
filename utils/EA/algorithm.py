"""
EA algorithm for binary genotypes with restart and immigrants
"""

import numpy as np
from copy import deepcopy
from random import seed

from .population import generate_population, phenotype
from .selection import tournament, elitism
from .ea_utils import best_indiv, best_indivs, average_indiv

from heapq import heappush, heappop


def run(c, size_cromo, k, fitness_func, crossover, mutation):
    statistics = []
    for i in range(c.runs):
        seed(i)
        _, _, stat_best, _ = ea_for_plot(c, size_cromo, k, fitness_func, crossover, mutation)
        statistics.append(stat_best)

    stat_gener = list(zip(*statistics))
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]

    if c.maximization:
        best = [max(g_i) for g_i in stat_gener]
    else:
        best = [min(g_i) for g_i in stat_gener]

    return best, aver_gener

# Return the best individual, best by generations, average population by generation
def ea_for_plot(c, size_cromo, k, fitness_func, crossover, mutation):
    heap = []
    # initialize population: indiv = (cromo,fit)
    population = generate_population(size_cromo, k)
    population = [(indiv[0], fitness_func(indiv)) for indiv in population]

    for indiv in population:
        if len(phenotype(indiv)) == k:
            heappush(heap, (-1 * indiv[1], indiv[0]))

    stat = [best_indiv(population)[1]]
    stat_aver = [average_indiv(population)]

    gen_without_improvement = 0
    current_best = c.max_fitness
    for i in range(c.generations):
        old_pop = deepcopy(population)

        if c.should_restart and gen_without_improvement == c.restart_generations:
            gen_without_improvement = 0
            old_pop_size = int(len(population) * (1 - c.immigrant_perc))
            population = population[ 0 : old_pop_size ]
            immigrants = generate_population(c.population_size - old_pop_size, k)
            [population.append(immigrant) for immigrant in immigrants]
            population = [ (indiv[0], fitness_func(indiv)) for indiv in population ]

        mate_pool = tournament(population)
        # Variation
        # ------ Crossover
        parents = []
        for j in range(0, c.population_size-1, 2):
            cromo_1 = mate_pool[j]
            cromo_2 = mate_pool[j+1]
            children = crossover(cromo_1, cromo_2)
            parents.extend(children)

        # ------ Mutation
        descendents = []
        for indiv in parents:
            new_indiv = mutation(indiv)
            descendents.append( (new_indiv[0], fitness_func(new_indiv)) )

        # New population
        population = elitism(old_pop, descendents)
        population = [(indiv[0], fitness_func(indiv)) for indiv in population]

        for indiv in population:
            if len(phenotype(indiv)) == k:
                heappush(heap, (-1 * indiv[1], indiv[0]))

        # Statistics
        stat.append(best_indiv(population)[1])
        stat_aver.append(average_indiv(population))

        # Check if solution improved in this generation
        best_fitness = best_indiv(population)[1]
        print(best_fitness, flush=True)

        if best_fitness == c.max_fitness:
            #fill stat with zeros to allow plot to show values until final generation
            while len(stat) < c.generations:
                stat.append(0)
            #stop algorithm as it found the solution
            break

        #count generations without improvement for restart
        if best_fitness < current_best:
            gen_without_improvement = 0
            current_best = deepcopy(best_fitness)
        else:
            gen_without_improvement += 1

    #return best_indiv(population), best_indivs(population, 3), stat, stat_aver
    best = heappop(heap)
    second =  heappop(heap)
    third = heappop(heap)
    best_k = [best, second, third]
    return (best[1], best[0]), best_k, stat, stat_aver
