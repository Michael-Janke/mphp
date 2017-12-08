import mutation
import crossover

### General ###
maximization = True
runs = 1
generations = 10
prob_mutation = 0.1
prob_crossover = 0.9
population_size = 10
tour_size = 3
elite_percentage = 0.1


### METHODS ###
mutation = mutation.binary_mutation
crossover = crossover.one_point_crossover

### Restart ####
should_restart = False
max_fitness = 100000
immigrant_perc = 0.5
restart_generations = 1000
