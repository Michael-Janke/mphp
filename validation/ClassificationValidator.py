from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.model_selection import cross_val_score

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
            scores = cross_val_score(clf, data.expressions, data.labels, cv=5, scoring="f1_micro")
            result[c] = (scores.mean(), scores.std())
        return result
