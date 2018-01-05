import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from imblearn.metrics import geometric_mean_score

from utils import Expressions

class ClassificationValidator():

    def __init__(self):
        self.classifier_table = {
            "SVM": SVC,
            "LogisticRegression": LogisticRegression,
            "DecisionTree": DecisionTreeClassifier,
            "naivebayes": GaussianNB,
            "knn": KNeighborsClassifier,
            "RandomForest": RandomForestClassifier,
            "BoostedTrees": AdaBoostClassifier
        }

    def evaluate(self, data, classifier):
        result = {}
        if "*" in classifier:
            classifier = self.classifier_table.keys()
        for c in classifier:
            if not c in self.classifier_table:
                continue
            clf = self.classifier_table[c]()
            
            scoring = {
                'precision': make_scorer(precision_score, average='micro'),
                'recall': make_scorer(recall_score, average='micro'),
                'f1': make_scorer(f1_score, average='micro'),
            }
            
            le = LabelEncoder()
            labels = le.fit_transform(data.labels)
            scores = cross_validate(clf, data.expressions, labels, cv=5, scoring=scoring, return_train_score=False)
            score_dict = {
                'precision': {
                    'mean': scores['test_precision'].mean(), 
                    'std':  scores['test_precision'].std(),
                },
                'recall': {
                    'mean': scores['test_recall'].mean(), 
                    'std':  scores['test_recall'].std(),
                },
                'f1': {
                    'mean': scores['test_f1'].mean(), 
                    'std':  scores['test_f1'].std(),
                },
            }
            #print(scores['test_gmean'])
            #print(scores['test_gmean'].mean())
            result[c] = score_dict
        return result

    def evaluateOneAgainstRest(self, sick, healthy, selected_genes_dict):
        results = {}
        for label, genes in selected_genes_dict.items():
            s_labels = self.binarize_labels(sick.labels, label)
            h_labels = self.binarize_labels(healthy.labels, label)

            sick_binary = Expressions(sick.expressions[:,genes], s_labels)
            healthy_binary = Expressions(healthy.expressions[:,genes], h_labels)

            sick_results = self.evaluate(sick_binary, ["DecisionTree"])
            healthy_results = self.evaluate(healthy_binary, ["DecisionTree"])

            results[label] = {
                "sick": sick_results,
                "healthy": healthy_results,
            }

        return results

    def binarize_labels(self, labels, selected_label):
        new_labels = np.zeros_like(labels)
        indices = np.flatnonzero(np.core.defchararray.find(labels,selected_label)!=-1)
        new_labels[indices] = 1

        return new_labels
