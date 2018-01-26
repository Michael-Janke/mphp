import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import silhouette_samples
from utils import ignore_warnings, binarize_labels

from utils.EA.population import phenotype

def fitness(sick, healthy, fit='combined', k=10, true_label=""):
    fitness_func  = globals()[get_fitness_function_name(fit)]
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        # todo smarter penalty
        # if pheno.shape[0] > k:
        #    return -10

        f =  fitness_func(sick, healthy, pheno, true_label=true_label)
        return f / (1 + abs(len(pheno) - k)/k)
    return fitness_

def get_fitness_function_name(fit):
    options = {
        'clustering': 'clustering_fitness',
        'classification': 'classification_fitness',
        'sick_vs_healthy': 'sick_vs_healthy_fitness',
        'combined': 'combined_fitness',
        'distance': 'distance_fitness',
    }

    return options.get(fit, 'combined_fitness')

@ignore_warnings
def classification_fitness(sick, healthy, genes, alpha=0.5, true_label=""):
    sick_expressions = sick.expressions[:,genes]
    healthy_expressions = healthy.expressions[:,genes]
    if not true_label:
        clf = DecisionTreeClassifier()
        sick_score = cross_validate(clf, sick_expressions, sick.labels, cv=5, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        healthy_score = cross_validate(clf, healthy_expressions, healthy.labels, cv=5, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        return (alpha * sick_score + (1-alpha) * (1- healthy_score))
    else:
        sick_labels = binarize_labels(sick.labels, true_label)
        healthy_labels = binarize_labels(healthy.labels, true_label)
        clf = DecisionTreeClassifier()
        sick_score = cross_validate(clf, sick_expressions, sick_labels, cv=5, scoring="f1", return_train_score=False)["test_score"].mean()
        healthy_score = cross_validate(clf, healthy_expressions, healthy_labels, cv=5, scoring="f1", return_train_score=False)["test_score"].mean()
    return (alpha * sick_score + (1-alpha) * (1- healthy_score))

@ignore_warnings
def sick_vs_healthy_fitness(sick, healthy, genes, alpha=None, true_label=None):
    sick_expressions = sick.expressions[:,genes]
    healthy_expressions = healthy.expressions[:,genes]

    scores = []
    for selected_label in np.unique(sick.labels):
        label = selected_label.split("-")[0]
        sick_indices = np.flatnonzero(np.core.defchararray.find(sick.labels, label) != -1)
        healthy_indices = np.flatnonzero(np.core.defchararray.find(healthy.labels, label) != -1)

        data = np.vstack((sick_expressions[sick_indices, :], healthy_expressions[healthy_indices, :]))
        labels = np.hstack((sick.labels[sick_indices], healthy.labels[healthy_indices]))

        clf = DecisionTreeClassifier()
        score = cross_validate(clf, data, labels, cv=5, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        scores.append(score)

    return min(scores)

def clustering_fitness(sick, healthy, genes, alpha=0.5, true_label=""):
    sick_expressions = sick.expressions[:,genes]
    healthy_expressions = healthy.expressions[:,genes]
    sick_silhouette_samples = (silhouette_samples(sick_expressions, sick.labels) + 1) / 2
    healthy_silhouette_samples = (silhouette_samples(healthy_expressions, healthy.labels) + 1) / 2

    if not true_label:
        sick_cluster_silhouettes = [np.mean(sick_silhouette_samples[sick.labels==label]) for label in np.unique(sick.labels)]
        healthy_cluster_silhouettes = [np.mean(healthy_silhouette_samples[healthy.labels==label]) for label in np.unique(healthy.labels)]
        return (alpha * np.mean(sick_cluster_silhouettes) + (1 - alpha) * (1 - np.mean(healthy_cluster_silhouettes)))
    else:
        silhoutte_sick = np.mean(sick_silhouette_samples[sick.labels==true_label+"-sick"])
        silhoutte_healthy = np.mean(healthy_silhouette_samples[healthy.labels==true_label+"-healthy"])
        return (alpha * silhoutte_sick + (1- alpha) * (1 - silhoutte_healthy))

def combined_fitness(sick, healthy, genes, alpha=0.5, beta=0.5, true_label=""):
    return 1/3 * classification_fitness(sick, healthy, genes, alpha, true_label=true_label)\
        + 1/3 * clustering_fitness(sick, healthy, genes, alpha, true_label=true_label)\
        + 1/3 * sick_vs_healthy_fitness(sick, healthy, genes)


def distance_fitness(sick, healthy, genes, true_label=""):
    sick_intra_distance, sick_inner_distance = compute_cluster_distance(sick, genes, true_label)
    healthy_intra_distance, healthy_inner_distance = compute_cluster_distance(healthy, genes, true_label)

    fitness_sick = 5*sick_intra_distance - sick_inner_distance
    fitness_healthy = 5*healthy_intra_distance + healthy_inner_distance
    fitness = fitness_sick - fitness_healthy
    return fitness


def compute_cluster_distance(data, genes, true_label=""):
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
    for i in range(len(unique_labels)-1):
        for j in range(i+1, len(unique_labels)-1):
            if true_label in unique_labels[i] or true_label in unique_labels[j] or not true_label:
                dist += np.linalg.norm(centers[i][0] - centers[j][0])
    # for index, label in enumerate(unique_labels):
    #     unique_labels = np.delete(unique_labels, 0)
    #     for _ in unique_labels:
    #         dist += np.linalg.norm(centers[index][0] - centers[index+1][0])

    number_types = np.unique(data.labels).shape[0]
    deviation = np.sum(deviations)/number_types
    cluster_distance = dist/(number_types * (number_types-1) * 0.5)

    return cluster_distance, deviation
