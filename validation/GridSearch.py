import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, f1_score
from datetime import datetime

from utils.DimensionalityReducer import DimensionalityReducer
from utils.EA.fitness import combined_fitness
from validation.Analyzer import Analyzer

class GridSearch(object):
    
    def __init__(self, sick, healthy, data):
        self.sick = sick
        self.healthy = healthy
        self.data = data

        self.table_all_at_once = None
        self.table_one_vs_rest = None

        self.dimReducer = DimensionalityReducer()
        self.analyzer = Analyzer()

        self.K_OPTIONS = [3] # , 5, 10, 20
        self.EXCLUDE_OPTIONS = [100, 500, 1000, 5000, 10000]
        self.M_OPTIONS = [10] # , 50, 100, 500
        self.S_OPTIONS = ["chi2", "f_classif"] #, "mutual_info_classif"
        self.NORM_OPTIONS = ["substract", "exclude"]
        self.F_OPTIONS = ["combined", "classification", "clustering", "distance"]

        self.BASIC_METHODS = {
            "basic": self.dimReducer.getFeatures,
            "tree" : self.dimReducer.getDecisionTreeFeatures,
        }

        self.NORMALIZED_METHODS = {
            "subt": self.dimReducer.getNormalizedFeaturesS,
            "excl": self.dimReducer.getNormalizedFeaturesE,
        }

        self.COMBINED_METHODS = {
            "ea":  self.dimReducer.getEAFeatures,
            "sfs": self.dimReducer.getFeaturesBySFS,
        }

        self.ALL_METHODS = [
            "basic", 
            "tree",
            "norm",
            "ea",
            "sfs",
        ]

    ### ALL AT ONCE ###
    def get_basic_results(self):
        results = []
        for k in self.K_OPTIONS:
            for method in self.BASIC_METHODS:
                if method == "basic":
                    # get result for each possible statistic
                    for stat in self.S_OPTIONS:
                        start = datetime.now()
                        features = self.BASIC_METHODS[method](self.data, k, stat)
                        time = round((datetime.now()-start).total_seconds(),2)

                        result = self.get_result_dict_all_at_once(method, k, features, time, statistic=stat)
                        results.append(result)

                else:
                    start = datetime.now()
                    features = self.BASIC_METHODS[method](self.data, k)
                    time = round((datetime.now()-start).total_seconds(),2)
                    
                    result = self.get_result_dict_all_at_once(method, k, features, time)
                    results.append(result)

            print("Parameter k: " + str(k) + " is done")
        print("Basic methods are done")
        return results

    def get_normalized_results(self, statistic = "chi2"):
        results = []
        for k in self.K_OPTIONS:
            for method in self.NORMALIZED_METHODS:
                if method == "excl":
                    # get result for each possible exlude parameter
                    for exclude_n in self.EXCLUDE_OPTIONS:
                        start = datetime.now()
                        features = self.NORMALIZED_METHODS[method](self.sick, self.healthy, k, exclude_n, statistic)
                        time = round((datetime.now()-start).total_seconds(),2)

                        result = self.get_result_dict_all_at_once(method, k, features, time, statistic=statistic, exclude=exclude_n, normalization="exclude")
                        results.append(result)

                else:
                    start = datetime.now()
                    features = self.NORMALIZED_METHODS[method](self.sick, self.healthy, k, 42, statistic)
                    time = round((datetime.now()-start).total_seconds(),2)
                    
                    result = self.get_result_dict_all_at_once(method, k, features, time, statistic=statistic, normalization="substract")
                    results.append(result)

        print("Normalized methods are done")
        return results

    def get_combined_results(self, statistic = "chi2", normalization = "exclude", n = 5000):
        results = []
        for k in self.K_OPTIONS:
            for method in self.COMBINED_METHODS:
                for m in self.M_OPTIONS:
                    for fit in self.F_OPTIONS:
                
                        start = datetime.now()
                        features = self.COMBINED_METHODS[method](self.sick, self.healthy, k, n, m, normalization, fit)
                        time = round((datetime.now()-start).total_seconds(),2)
                        
                        result = self.get_result_dict_all_at_once(method, k, features, time, statistic=statistic, exclude=n, normalization="exclude", preselect=m, fitness_method=fit)
                        results.append(result)

                print("Method " + method + " is done")
            print("Parameter k: " + str(k) + " is done")
        print("Combined methods are done")
        return results


    ### 1 vs Rest ###
    def get_one_against_rest_results(self):
        results = []
        id = 0
        for k in self.K_OPTIONS:
            for method in self.ALL_METHODS:
                if method in ["basic", "tree"]:
                    start = datetime.now()
                    feature_sets = self.dimReducer.getOneAgainstRestFeatures(self.data, '', k, method=method)
                    time = round((datetime.now()-start).total_seconds(),2)
                else:    
                    start = datetime.now()
                    feature_sets = self.dimReducer.getOneAgainstRestFeatures(self.sick, self.healthy, k, method=method)
                    time = round((datetime.now()-start).total_seconds(),2)

                validation = self.analyzer.computeFeatureValidationOneAgainstRest(self.sick, self.healthy, feature_sets)
                del validation["meanFitness"]

                for cancer_type, metrics in validation.items():
                    result = self.get_result_dict_one_vs_rest(id, cancer_type, method, k, metrics, time, feature_sets[cancer_type])
                    results.append(result)

                id += 1
                print("Method: " +  method + " is done")
            print("Parameter k: " + str(k) + " is done")

        return results


    ### Utils ###
    def get_table_one_vs_rest(self):
        if not self.table_one_vs_rest is None:
            return self.table_one_vs_rest

        table = []
        table.append(["ID", "Type", "Method", "K", "Fitness_score", "Sick_F1", "Time", "Features"])
        table.extend(self.get_one_against_rest_results())

        return table

    def get_table_all_at_once(self):
        if not self.table_all_at_once is None:
            return self.table_all_at_once

        table = []
        table.append(["Method", "K", "Statistic", "Normalization", "Exclude", "Preselect", "Fitness_method", "Fitness_score", "Sick_F1", "Time", "Features"])
        table.extend(self.get_basic_results())
        table.extend(self.get_normalized_results())
        table.extend(self.get_combined_results())

        self.table_all_at_once = table
        return table

    def get_result_dict_one_vs_rest(self, id, cancer_type, method, k, metrics, time, features):
        fitness = float(str(metrics["fitness"]["combinedFitness"])[0:5])
        sick_f1 = float(str(metrics["sick"]["classification"]["decisionTree"]["f1"]["mean"])[0:5])
        return [id, cancer_type, method, k, fitness, sick_f1, time, features.tolist()]

    def get_result_dict_all_at_once(self, method, k, feature_set, time, statistic="", normalization="", exclude="", preselect="", fitness_method=""):
        fitness_score = float(str(combined_fitness(self.sick, self.healthy, feature_set))[0:5])

        scoring = { 'f1': make_scorer(f1_score, average='macro') }
        clf = DecisionTreeClassifier()
        scores = cross_validate(clf, self.sick.expressions[:,feature_set], self.sick.labels, cv=5, scoring=scoring, return_train_score=False)
        f1 = scores['test_f1'].mean()

        return [method, k, statistic, normalization, exclude, preselect, fitness_method, fitness_score, f1, time, feature_set.tolist()]

    def save_table_to_disk(self, table, name="grid_table"):
        with open(name+".csv","w") as f:
            wr = csv.writer(f)
            wr.writerows(table)
