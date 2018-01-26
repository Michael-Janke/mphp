### General ###
maximization = True
runs = 1
generations = 5
population_size = 100
chromo_size = 100
prob_mutation = 1/generations
prob_crossover = 30*2/population_size
tour_size = 3
elite_percentage = 0.1


### METHODS ###
mutation = "binary_simple"
crossover = "one-point"

### Restart ####
should_restart = True
max_fitness = 100000
immigrant_perc = 0.5
restart_generations = 20
