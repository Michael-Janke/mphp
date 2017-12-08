"""
EA algorithm for binary genotypes with restart and immigrants
"""


from copy import deepcopy
from config import *
import numpy as np

def run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func,givens):
    statistics = []
    generations = []
    final_conflicts = []
    for i in range(numb_runs):
        seed(i)
        best, stat_best, stat_aver,gen = sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func,givens)
        print(best[0])
        print(best[1])
        final_conflicts.append(best[1])
        statistics.append(stat_best)
        generations.append(gen)
    stat_gener = list(zip(*statistics))
    best = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]

    best_generation = min(generations)
    aver_generation = np.mean(generations)
    numb_solution = len([x for x in generations if x < numb_generations-1])

    return best, aver_gener,final_conflicts,best_generation,aver_generation,numb_solution

# Return the best plus, best by generation, average population by generation
def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func, givens):
    # initialize population: indiv = (cromo,fit)
    population = gen_function(size_pop)
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]

    stat = [best_pop(population)[1]]
    stat_aver = [average_pop(population)]
    
    gen_without_improvement = 0
    current_best = 81
    
    for i in range(numb_generations):
        old_pop = deepcopy(population)

        if should_restart and gen_without_improvement==restart_generations:
            gen_without_improvement=0
            old_pop_size = int(len(population)*(1-immigrant_perc))
            population = population[0:old_pop_size]
            immigrants = gen_function(size_pop-old_pop_size)
            [population.append(immigrant) for immigrant in immigrants]
            population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]

        mate_pool = sel_parents(population)
        # Variation
        # ------ Crossover
        parents = []
        for j in  range(0,size_pop-1,2):
            cromo_1= mate_pool[j]
            cromo_2 = mate_pool[j+1]
            children = recombination(cromo_1,cromo_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendents = []
        for indiv,fit in parents:
            new_indiv = mutation(indiv,prob_mut, givens)
            #mutation cant swap givens, so that there is no need to fix
            if prob_cross>0:
                new_indiv = fix_func(new_indiv)
            descendents.append((new_indiv,fitness_func(new_indiv)))
        # New population
        population = sel_survivors(old_pop,descendents)
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    
        # Estatistica
        stat.append(best_pop(population)[1])
        stat_aver.append(average_pop(population))

        best_fitness = best_pop(population)[1]
        if best_fitness == 0:
            #fill stat with zeros to allow plot to show values until final generation
            while len(stat)<numb_generations:
                stat.append(0)
            #stop algorithm as it found the solution
            break

        #count generations without improvement for restart
        if best_fitness<current_best:
            gen_without_improvement = 0
            current_best=deepcopy(best_fitness)
        else:
            gen_without_improvement += 1
    
    return best_pop(population),stat, stat_aver,i



