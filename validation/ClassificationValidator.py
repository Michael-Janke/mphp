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

from utils import Expressions, binarize_labels, ignore_warnings

class ClassificationValidator():

    def __init__(self):
        self.classifier_table = {
            #"svm": SVC,
            #"logisticRegression": LogisticRegression,
            "decisionTree": DecisionTreeClassifier,
            #"naivebayes": GaussianNB,
            #"knn": KNeighborsClassifier,
            #"randomForest": RandomForestClassifier,
            #"boostedTrees": AdaBoostClassifier
        }

    @ignore_warnings
    def evaluate(self, data, genes, classifier, true_label=""):
        result = {}

        if "*" in classifier:
            classifier = self.classifier_table.keys()
        for c in classifier:
            if not c in self.classifier_table:
                continue
            clf = self.classifier_table[c]()

            labels = None
            if not true_label:
                le = LabelEncoder()
                labels = le.fit_transform(data.labels)
                scoring = {
                    'precision': make_scorer(precision_score, average='macro'),
                    'recall': make_scorer(recall_score, average='macro'),
                    'f1': make_scorer(f1_score, average='macro'),
                }
            else:
                labels = binarize_labels(data.labels, true_label)
                scoring = {
                    'precision': make_scorer(precision_score, average='binary'),
                    'recall': make_scorer(recall_score, average='binary'),
                    'f1': make_scorer(f1_score, average='binary'),
                }
            
            scores = cross_validate(clf, data.expressions[:,genes], labels, cv=5, scoring=scoring, return_train_score=False)
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
            result[c] = score_dict
        return result
    #
    # def evaluateOneAgainstRest(self, sick, healthy, selected_genes_dict):
    #     results = {}
    #     for label, genes in selected_genes_dict.items():
    #         s_labels = binarize_labels(sick.labels, label)
    #         sick_binary = Expressions(sick.expressions[:,genes], s_labels)
    #         sick_results = self.evaluate(sick_binary, ["decisionTree"])
    #
    #         if healthy == "":
    #             results[label] = sick_results
    #         else:
    #             h_labels = binarize_labels(healthy.labels, label)
    #             healthy_binary = Expressions(healthy.expressions[:,genes], h_labels)
    #             healthy_results = self.evaluate(healthy_binary, ["decisionTree"])
    #
    #             results[label] = {
    #                 "sick": sick_results,
    #                 "healthy": healthy_results,
    #             }
    #
    #     return results
