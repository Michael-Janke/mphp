from random import random, randint, sample
from config import prob_crossover as default_prob

def one_point_crossover(indiv_1, indiv_2, prob_crossover = default_prob):
    if random() < prob_crossover:
        chromosome_1, chromosome_2 = indiv_1[0], indiv_2[0]
        cross_point = randint(0,len(chromosome_1))
        new_1 = chromosome_1[0:cross_point] + chromosome_2[cross_point:]
        new_2 = chromosome_2[0:cross_point] + chromosome_1[cross_point:]
        return ( (new_1,0) , (new_2,0) )
    else:
        return ( indiv_1, indiv_2 )
        
def two_points_crossover(indiv_1, indiv_2, prob_crossover = default_prob):
    if random() < prob_crossover:
        chromosome_1, chromosome_2 = indiv_1[0], indiv_2[0]
        cross_points = sample(range(len(chromosome_1)),2)
        cross_points.sort()
        point_1, point_2 = cross_points

        new_1 = chromosome_1[:point_1] + chromosome_2[point_1:point_2] + chromosome_1[point_2:]
        new_2 = chromosome_2[:point_1] + chromosome_1[point_1:point_2] + chromosome_2[point_2:]
        return ( (new_1, 0), (new_2, 0) )
    else:
        return ( indiv_1, indiv_2 )
        
def uniform_crossover(indiv_1, indiv_2, prob_crossover = default_prob):
    if random() < prob_crossover:
        chromosome_1, chromosome_2 = indiv_1[0], indiv_2[0]
        new_1 = new_2 = []
        for i in range(0, len(chromosome_1)):
            if random() < 0.5:
                new_1.append(chromosome_1[i])
                new_2.append(chromosome_2[i])
            else:
                new_1.append(chromosome_2[i])
                new_2.append(chromosome_1[i])
        return ( (new_1, 0), (new_2, 0) )
    else:
        return ( indiv_1, indiv_2 )