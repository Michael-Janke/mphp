from random import random
from .config import prob_mutation as default_prob

def binary_mutation(indiv, prob_mutation = default_prob):
    chromosome = indiv[0][:]
    for i in range(len(chromosome)):
        chromosome[i] = binary_mutation_gene(chromosome[i], prob_mutation)
    return (chromosome, 0)

def binary_mutation_gene(gene, prob_mutation = default_prob):
    if random() < prob_mutation:
        gene ^= 1
    return gene