import numpy as np
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator
from utils.EA.fitness import classification_fitness, clustering_fitness, distance_fitness, combined_fitness, sick_vs_healthy_fitness
from utils import Expressions, binarize_labels
from collections import defaultdict

from numpy.core.defchararray import find
from scipy.stats import mannwhitneyu

from joblib import Parallel, delayed

class Analyzer:
    def __init__(self):
        pass

    '''
        case 1:
            sick and healthy should contain at least two cancer types
        case 2:
            healthy = ""
            no fitness function is calculated
        selected_genes_dict: call with result from getOneAgainstRestFeatures
    '''
    def computeFeatureValidationOneAgainstRest(self, sick, healthy, selected_genes_dict):
        n_jobs = len(selected_genes_dict.keys())
        items = list(selected_genes_dict.items())

        results = Parallel(n_jobs=n_jobs, backend="threading")\
            (delayed(self.computeFeatureValidationWrapper)(sick, healthy, label, genes) for label, genes in items)

        combined_results = {}
        for label, validation in results:
            combined_results[label] = validation

        if healthy:
            cumulated_fitness = 0
            for res in combined_results.values():
                cumulated_fitness += res["fitness"]["combinedFitness"]

            combined_results["meanFitness"] = cumulated_fitness / len(combined_results.keys())

        return combined_results

    def computeFeatureValidationWrapper(self, sick, healthy, label, genes):
        validation = self.computeFeatureValidation(sick, healthy, genes, true_label=label)
        return label, validation

    '''
        case 1:
            sick and healthy should contain at least two cancer types
            returns validation for sick and healthy and fitness functions
        case 2:
            healthy = ""
            only data in sick is validated
            sick should contain at least two cancer types
        selected_genes: call with result from feature selection
    '''
    def computeFeatureValidation(self, sick, healthy, selected_genes, true_label=""):
        sick_validation = self.assembleValidationOutput(sick, selected_genes, true_label=true_label)

        if not healthy:
            return sick_validation

        healthy_validation = self.assembleValidationOutput(healthy, selected_genes, true_label=true_label)

        class_fitness = classification_fitness(sick, healthy, selected_genes, true_label=true_label, cv=5)
        clus_fitness = clustering_fitness(sick, healthy, selected_genes, true_label=true_label)
        comb_fitness = combined_fitness(sick, healthy, selected_genes, true_label=true_label, cv=5)
        dist_fitness = distance_fitness(sick, healthy, selected_genes, true_label=true_label)
        s_vs_h_fitness = sick_vs_healthy_fitness(sick, healthy, selected_genes, cv=5)

        return {
            "sick": sick_validation,
            "healthy": healthy_validation,
            "fitness": {
                "classificationFitness": class_fitness,
                "clusteringFitness": clus_fitness,
                "sickVsHealthyFitness": s_vs_h_fitness,
                "distanceFitness": dist_fitness,
                "combinedFitness": comb_fitness,
            }
        }

    def assembleValidationOutput(self, X, selected_genes, true_label=""):
        classVal = ClassificationValidator()
        classification = classVal.evaluate(X, selected_genes, ["*"], true_label=true_label)
        return {"classification": classification}

    '''
        sick and healthy should contain at least one cancer type
        selected_genes_dict: call with result from getOneAgainstRestFeatures
    '''
    def computeExpressionMatrixOneAgainstRest(self, sick, healthy, selected_genes_dict):
        n_jobs = len(selected_genes_dict.keys())
        items = list(selected_genes_dict.items())

        results = Parallel(n_jobs=n_jobs, backend="threading")\
            (delayed(self.computeExpressionMatrixWrapper)(sick, healthy, label, genes) for label, genes in items)

        combined_results = {}
        for label, matrix in results:
            combined_results[label] = {label: matrix[label]}

        return combined_results

    def computeExpressionMatrixWrapper(self, sick, healthy, label, genes):
        matrix = self.computeExpressionMatrix(sick, healthy, genes)
        return label, matrix

    '''
        sick and healthy should contain at least one cancer type
        selected_genes: call with result from feature selection
    '''
    def computeExpressionMatrix(self, sick, healthy, selected_genes):
        expressions = defaultdict(list)
        for label in np.unique(sick.labels):
            cancertype = label.split("-")[0]

            sick_rows = np.flatnonzero(np.core.defchararray.find(cancertype+"-sick",sick.labels)!=-1)
            healthy_rows = np.flatnonzero(np.core.defchararray.find(cancertype+"-healthy",healthy.labels)!=-1)

            for gene in selected_genes:
                _, p_high = mannwhitneyu(sick.expressions[sick_rows,gene], healthy.expressions[healthy_rows,gene], alternative="greater")
                _, p_low  = mannwhitneyu(sick.expressions[sick_rows,gene], healthy.expressions[healthy_rows,gene], alternative="less")
                expression = "greater" if p_high < 0.01 else "less" if p_low < 0.01 else "unchanged"
                
                if healthy_rows.shape[0] < 20:
                    expressions[cancertype].append("cant compute - " + expression)
                else:
                    expressions[cancertype].append(expression)

        return expressions
