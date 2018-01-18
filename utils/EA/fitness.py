import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import silhouette_samples
from utils import Expressions, binarize_labels, ignore_warnings

from utils.EA.population import phenotype

def fitness(sick, healthy):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        sick_reduced = Expressions(sick.expressions[:,pheno], sick.labels)
        healthy_reduced = Expressions(healthy.expressions[:,pheno], healthy.labels)
        return distance_evaluate(sick_reduced, healthy_reduced)
    return fitness_

@ignore_warnings
def classification_fitness(sick, healthy, alpha=0.5, true_label=""):
    if not true_label:
        clf = DecisionTreeClassifier()
        sick_score = cross_val_score(clf, sick.expressions, sick.labels, cv=5, scoring="f1_macro").mean()
        healthy_score = cross_val_score(clf, healthy.expressions, healthy.labels, cv=5, scoring="f1_macro").mean()
        return (alpha * sick_score + (1-alpha) * (1- healthy_score))
    else:
        sick_labels = binarize_labels(sick.labels, true_label)
        healthy_labels = binarize_labels(healthy.labels, true_label)
        clf = DecisionTreeClassifier()
        sick_score = cross_val_score(clf, sick.expressions, sick_labels, cv=5, scoring="f1").mean()
        healthy_score = cross_val_score(clf, healthy.expressions, healthy_labels, cv=5, scoring="f1").mean()
    return (alpha * sick_score + (1-alpha) * (1- healthy_score))

def clustering_fitness(sick, healthy, alpha=0.5, true_label=""):

    sick_silhouette_samples = (silhouette_samples(sick.expressions, sick.labels) + 1) / 2
    healthy_silhouette_samples = (silhouette_samples(healthy.expressions, healthy.labels) + 1) / 2

    if not true_label:
        sick_cluster_silhouettes = [np.mean(sick_silhouette_samples[sick.labels==label]) for label in np.unique(sick.labels)]
        healthy_cluster_silhouettes = [np.mean(healthy_silhouette_samples[healthy.labels==label]) for label in np.unique(healthy.labels)]
        return (alpha * np.mean(sick_cluster_silhouettes) + (1 - alpha) * (1 - np.mean(healthy_cluster_silhouettes)))
    else:
        silhoutte_sick = np.mean(sick_silhouette_samples[sick.labels==true_label+"-sick"])
        silhoutte_healthy = np.mean(healthy_silhouette_samples[healthy.labels==true_label+"-healthy"])
        return (alpha * silhoutte_sick + (1- alpha) * (1 - silhoutte_healthy))

def combined_fitness(sick, healthy, alpha=0.5, beta=0.5, true_label=""):
    return beta * classification_fitness(sick, healthy, alpha, true_label=true_label)\
        + (1 - beta) * clustering_fitness(sick, healthy, alpha, true_label=true_label)

#
# def evaluate(sick, healthy):
#     clf = DecisionTreeClassifier()
#
#     if sick.expressions.shape[1] > 10:
#         return -10
#     else:
#         sick_scores = cross_val_score(clf, sick.expressions, sick.labels, cv=5, scoring="f1_micro")
#         fitness_score = sick_scores.mean() - sick_scores.std()
#
#         healthy_scores = cross_val_score(clf, healthy.expressions, healthy.labels, cv=5, scoring="f1_micro")
#         fitness_score -= 2*healthy_scores.mean() - healthy_scores.std()
#
#         #fitness_score -= np.log10(sick_data.shape[1])
#
#         return fitness_score
#
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
