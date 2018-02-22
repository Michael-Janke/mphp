import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, cross_validate, StratifiedShuffleSplit
from sklearn.metrics import silhouette_samples
from utils import ignore_warnings, binarize_labels
from time import time

from utils.EA.population import phenotype

def fitness(sick, healthy, fit='combined', k=10, true_label=""):
    fitness_func  = globals()[get_fitness_function_name(fit)]
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        # todo smarter penalty
        # if pheno.shape[0] > k:
        #    return -10
        if len(pheno) > max(20, 2 * k):
            return -10

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
def classification_fitness(sick, healthy, genes, alpha=0.5, true_label="", cv=3):
    clf = DecisionTreeClassifier(presort=True)
    if not true_label:
        sick_score = cross_validate(clf, sick.expressions[:,genes], sick.labels, cv=cv, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        healthy_score = cross_validate(clf, healthy.expressions[:,genes], healthy.labels, cv=cv, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        return (alpha * sick_score + (1-alpha) * (1- healthy_score))
    else:
        sick_labels = binarize_labels(sick.labels, true_label)
        healthy_labels = binarize_labels(healthy.labels, true_label)
        sick_score = cross_validate(clf, sick.expressions[:,genes], sick_labels, cv=cv, scoring="f1", return_train_score=False)["test_score"].mean()
        healthy_score = cross_validate(clf, healthy.expressions[:,genes], healthy_labels, cv=cv, scoring="f1", return_train_score=False)["test_score"].mean()
    return (alpha * sick_score + (1-alpha) * (1- healthy_score))

@ignore_warnings
def sick_vs_healthy_fitness(sick, healthy, genes, alpha=None, true_label=None, cv=3):
    clf = DecisionTreeClassifier(presort=True)

    if not true_label:
        scores = []
        for selected_label in np.unique(sick.labels):
            label = selected_label.split("-")[0]
            sick_indices = np.flatnonzero(np.core.defchararray.find(sick.labels, label) != -1)
            healthy_indices = np.flatnonzero(np.core.defchararray.find(healthy.labels, label) != -1)

            data = np.vstack((sick.expressions[sick_indices][:,genes], healthy.expressions[healthy_indices][:,genes]))
            labels = np.hstack((sick.labels[sick_indices], healthy.labels[healthy_indices]))

            score = cross_validate(clf, data, labels, cv=cv, scoring="f1_macro", return_train_score=False)["test_score"].mean()
            scores.append(score)

        return np.mean(scores)

    else:
        label = true_label.split("-")[0]
        sick_indices = np.flatnonzero(np.core.defchararray.find(sick.labels, label) != -1)
        healthy_indices = np.flatnonzero(np.core.defchararray.find(healthy.labels, label) != -1)

        data = np.vstack((sick.expressions[sick_indices][:,genes], healthy.expressions[healthy_indices][:,genes]))
        labels = np.hstack((sick.labels[sick_indices], healthy.labels[healthy_indices]))

        score = cross_validate(clf, data, labels, cv=cv, scoring="f1_macro", return_train_score=False)["test_score"].mean()
        return score

def clustering_fitness(sick, healthy, genes, alpha=0.5, true_label=""):
    n_cancers = np.unique(sick.labels).shape[0]
    sick_split = StratifiedShuffleSplit(n_splits=1, test_size=None, train_size=min(len(sick.labels)-n_cancers, n_cancers*100), random_state=0)
    healthy_split = StratifiedShuffleSplit(n_splits=1, test_size=None, train_size=min(len(healthy.labels)-n_cancers, n_cancers*100), random_state=0)
    sick_indices, _ = next(sick_split.split(sick.expressions, sick.labels))
    healthy_indices, _ = next(healthy_split.split(healthy.expressions, healthy.labels))

    sick_silhouette_samples = (silhouette_samples(sick.expressions[:,genes][sick_indices,:], sick.labels[sick_indices]) + 1) / 2
    healthy_silhouette_samples = (silhouette_samples(healthy.expressions[:,genes][healthy_indices,:], healthy.labels[healthy_indices]) + 1) / 2

    fitness = 0
    if not true_label:
        sick_cluster_silhouettes = [np.mean(sick_silhouette_samples[sick.labels[sick_indices]==label]) for label in np.unique(sick.labels)]
        healthy_cluster_silhouettes = [np.mean(healthy_silhouette_samples[healthy.labels[healthy_indices]==label]) for label in np.unique(healthy.labels)]
        fitness = (alpha * np.mean(sick_cluster_silhouettes) + (1 - alpha) * (1 - np.mean(healthy_cluster_silhouettes)))
    else:
        silhoutte_sick = np.mean(sick_silhouette_samples[sick.labels[sick_indices]==true_label+"-sick"])
        silhoutte_healthy = np.mean(healthy_silhouette_samples[healthy.labels[healthy_indices]==true_label+"-healthy"])
        fitness = (alpha * silhoutte_sick + (1- alpha) * (1 - silhoutte_healthy))
    return fitness

def combined_fitness(sick, healthy, genes, alpha=0.5, beta=0.5, true_label="", cv=3, return_single_scores=False):
    class_score = classification_fitness(sick, healthy, genes, alpha, true_label=true_label, cv=cv)
    clust_score = clustering_fitness(sick, healthy, genes, alpha, true_label=true_label)
    s_v_h_score = sick_vs_healthy_fitness(sick, healthy, genes, true_label=true_label, cv=cv)
    combi_score = (class_score + clust_score + s_v_h_score) / 3

    if return_single_scores:
        return (combi_score, class_score, clust_score, s_v_h_score)
    else:
        return combi_score

def distance_fitness(sick, healthy, genes, true_label=""):
    sick_intra_distance, sick_inner_distance = compute_cluster_distance(sick, genes, true_label)
    healthy_intra_distance, healthy_inner_distance = compute_cluster_distance(healthy, genes, true_label)

    fitness_sick = 5*sick_intra_distance - sick_inner_distance
    fitness_healthy = 5*healthy_intra_distance + healthy_inner_distance
    fitness = fitness_sick - fitness_healthy
    return fitness


def compute_cluster_distance(data, genes, true_label=""):
    normalized_data = np.copy(data.expressions[:,genes])
    normalized_data = normalized_data / np.max(normalized_data, axis=0)

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
            if true_label == "":
                dist += np.linalg.norm(centers[i][0] - centers[j][0])
            else:
                if true_label in unique_labels[i] or true_label in unique_labels[j]:
                    dist += np.linalg.norm(centers[i][0] - centers[j][0])

    number_types = np.unique(data.labels).shape[0]
    deviation = np.sum(deviations)/number_types
    cluster_distance = dist/(number_types * (number_types-1) * 0.5)

    return cluster_distance, deviation
