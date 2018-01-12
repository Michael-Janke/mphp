import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from utils import Expressions

from utils.EA.population import phenotype

def fitness(sick, healthy):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        sick_reduced = Expressions(sick.expressions[:,pheno], sick.labels)
        healthy_reduced = Expressions(healthy.expressions[:,pheno], healthy.labels)
        return distance_evaluate(sick_reduced, healthy_reduced)
    return fitness_

def evaluate(sick, healthy):
    clf = DecisionTreeClassifier()

    if sick.expressions.shape[1] > 10:
        return -10
    else:
        sick_scores = cross_val_score(clf, sick.expressions, sick.labels, cv=5, scoring="f1_micro")
        fitness_score = sick_scores.mean() - sick_scores.std()

        healthy_scores = cross_val_score(clf, healthy.expressions, healthy.labels, cv=5, scoring="f1_micro")
        fitness_score -= 2*healthy_scores.mean() - healthy_scores.std()

        #fitness_score -= np.log10(sick_data.shape[1])

        return fitness_score

def distance_evaluate(sick, healthy):
    if sick.expressions.shape[1] > 10:
        return -10

    sick_intra_distance, sick_inner_distance = compute_cluster_distance(sick)
    healthy_intra_distance, healthy_inner_distance = compute_cluster_distance(healthy)

    fitness_sick = 5*sick_intra_distance - sick_inner_distance
    fitness_healthy = 5*healthy_intra_distance + healthy_inner_distance
    fitness = fitness_sick - fitness_healthy
    return fitness

def compute_cluster_distance(data):
    normalized_data = data.expressions / np.max(data.expressions, axis=0)

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
