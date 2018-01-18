import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import silhouette_samples
from utils import ignore_warnings

from utils.EA.population import phenotype

def fitness(sick, healthy, fit='combined'):
    fitness_func  = globals()[get_fitness_function_name(fit)]
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        # todo smarter penalty
        if pheno.shape[0] > 10:
            return -10

        return fitness_func(sick, healthy, pheno)
    return fitness_

def get_fitness_function_name(fit):
    options = {
        'clustering': 'clustering_fitness',
        'classification': 'classification_fitness',
        'combined': 'combined_fitness',
        'distance': 'distance_fitness',
    }
    
    return options.get(fit, 'combined_fitness')

@ignore_warnings
def classification_fitness(sick, healthy, genes, alpha=0.5):
    clf = DecisionTreeClassifier()
    sick_score = cross_val_score(clf, sick.expressions[:,genes], sick.labels, cv=5, scoring="f1_macro").mean()
    healthy_score = cross_val_score(clf, healthy.expressions[:,genes], healthy.labels, cv=5, scoring="f1_macro").mean()

    return (alpha * sick_score + (1-alpha) * (1- healthy_score))


def clustering_fitness(sick, healthy, genes, alpha=0.5):

    sick_silhouette_samples = (silhouette_samples(sick.expressions[:,genes], sick.labels) + 1) / 2
    sick_cluster_silhouettes = [np.mean(sick_silhouette_samples[sick.labels==label]) for label in np.unique(sick.labels)]

    healthy_silhouette_samples = (silhouette_samples(healthy.expressions[:,genes], healthy.labels) + 1) / 2
    healthy_cluster_silhouettes = [np.mean(healthy_silhouette_samples[healthy.labels==label]) for label in np.unique(healthy.labels)]

    return (alpha * np.mean(sick_cluster_silhouettes) + (1 - alpha) * (1 - np.mean(healthy_cluster_silhouettes)))


def combined_fitness(sick, healthy, genes, alpha=0.5, beta=0.5):
    return beta * classification_fitness(sick, healthy, genes, alpha) + (1 - beta) * clustering_fitness(sick, healthy, genes, alpha)


def distance_fitness(sick, healthy, genes):
    sick_intra_distance, sick_inner_distance = compute_cluster_distance(sick, genes)
    healthy_intra_distance, healthy_inner_distance = compute_cluster_distance(healthy, genes)

    fitness_sick = 5*sick_intra_distance - sick_inner_distance
    fitness_healthy = 5*healthy_intra_distance + healthy_inner_distance
    fitness = fitness_sick - fitness_healthy
    return fitness


def compute_cluster_distance(data, genes):
    normalized_data = data.expressions[:,genes] / np.max(data.expressions[:,genes], axis=0)

    centers = []
    deviations = []
    for label in np.unique(data.labels):
        indices = np.where(label == data.labels)
        selected_data = normalized_data[indices, :]
        centers.append(np.median(selected_data, axis=1))
        deviations.append(np.std(selected_data))

    unique_labels = np.unique(data.labels).T
    dist = 0
    for index, label in enumerate(unique_labels):
        unique_labels = np.delete(unique_labels, 0)
        for _ in unique_labels:
            dist += np.linalg.norm(centers[index][0] - centers[index+1][0])

    number_types = np.unique(data.labels).shape[0]
    deviation = np.sum(deviations)/number_types
    cluster_distance = dist/(number_types * (number_types-1) * 0.5)

    return cluster_distance, deviation
