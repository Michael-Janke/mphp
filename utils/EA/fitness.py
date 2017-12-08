import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

from .population import phenotype

def fitness(sick_data, sick_labels, healthy_data, healthy_labels):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate

        return evaluate(sick_data[:, pheno], sick_labels, healthy_data[:, pheno], healthy_labels)
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
