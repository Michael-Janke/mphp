from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.metrics import f1_score

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
        result = []
        if "*" in classifier:
            classifier = self.classifier_table.keys()
        for c in classifier:
            if not c in self.classifier_table:
                continue
            clf = self.classifier_table[c]()
            clf.fit(data.expressions, data.labels)
            pred = clf.predict(data.expressions)
            result += [f1_score(data.labels, pred, average="micro")]
        return result
