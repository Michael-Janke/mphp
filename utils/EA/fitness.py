from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

from .population import phenotype

def fitness(sick_data, sick_labels, healthy_data, healthy_labels):
    def fitness_(indiv):
        pheno = phenotype(indiv)
        # select features and only pass this data to evaluate
        selected_data = sick_data[:, pheno]
        
        return evaluate(selected_data, sick_labels)
    return fitness_

def evaluate(data, labels):
    clf = DecisionTreeClassifier()

    if data.shape[1] > 10:
        return 0
    else:
        scores = cross_val_score(clf, data, labels, cv=5, scoring="f1_micro")
        fitness_score = scores.mean() - scores.std()

        return fitness_score
