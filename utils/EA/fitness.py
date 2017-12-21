import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

from .population import phenotype

def fitness(sick_data, sick_labels, healthy_data, healthy_labels):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate

        return distance_evaluate(sick_data[:, pheno], sick_labels, healthy_data[:, pheno], healthy_labels)
    return fitness_

def evaluate(sick_data, sick_labels, healthy_data, healthy_labels):
    clf = DecisionTreeClassifier()

    if sick_data.shape[1] > 10:
        return -10
    else:
        sick_scores = cross_val_score(clf, sick_data, sick_labels, cv=5, scoring="f1_micro")
        fitness_score = sick_scores.mean() - sick_scores.std()

        healthy_scores = cross_val_score(clf, healthy_data, healthy_labels, cv=5, scoring="f1_micro")
        fitness_score -= 2*healthy_scores.mean() - healthy_scores.std()

        #fitness_score -= np.log10(sick_data.shape[1])

        return fitness_score

def distance_evaluate(sick_data, sick_labels, healthy_data, healthy_labels):
    if sick_data.shape[1] > 10:
        return -10

    sick_intra_distance, sick_inner_distance = compute_cluster_distance(sick_data, sick_labels)
    healthy_intra_distance, healthy_inner_distance = compute_cluster_distance(healthy_data, healthy_labels)

    fitness_sick = sick_intra_distance - sick_inner_distance
    fitness_healthy = healthy_intra_distance + healthy_inner_distance
    fitness = fitness_sick - fitness_healthy
    return fitness

def compute_cluster_distance(data, labels):
    normalized_data = np.copy(data)
    for index in range(normalized_data.shape[1]):
        normalized_data[:, index] /= np.max(normalized_data[:,index])

    centers = []
    deviations = []
    for label in np.unique(labels):
        indices = np.where(label == labels)
        data = normalized_data[indices, :]
        centers.append(np.median(data, axis=1))
        deviations.append(np.std(data))

    unique_labels = np.unique(labels).T
    dist = 0
    for index, label in enumerate(unique_labels):
        unique_labels = np.delete(unique_labels, 0)
        for _ in unique_labels:
            dist += np.linalg.norm(centers[index][0] - centers[index+1][0])

    number_types = np.unique(labels).shape[0]
    deviation = np.sum(deviations)/number_types
    cluster_distance = dist/(number_types * (number_types-1) * 0.5)

    return cluster_distance, deviation
