import numpy as np
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator
from utils.EA.fitness import classification_fitness, clustering_fitness, distance_fitness, combined_fitness, sick_vs_healthy_fitness
from utils import Expressions, binarize_labels
from collections import defaultdict

from numpy.core.defchararray import find
from scipy.stats import mannwhitneyu

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
        results = {}
        for label, genes in selected_genes_dict.items():
            results[label] = self.computeFeatureValidation(sick, healthy, genes, true_label=label)

        if healthy:
            cumulated_fitness = 0
            for res in results.values():
                cumulated_fitness += res["fitness"]["combinedFitness"]

            results["meanFitness"] = cumulated_fitness / len(results.keys())

        return results

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

        sick = sick.select_genes(selected_genes)
        healthy = healthy.select_genes(selected_genes)

        class_fitness = classification_fitness(sick, healthy, true_label=true_label, cv=5)
        clus_fitness = clustering_fitness(sick, healthy, true_label=true_label)
        comb_fitness = combined_fitness(sick, healthy, true_label=true_label, cv=5)
        dist_fitness = distance_fitness(sick, healthy, true_label=true_label)
        s_vs_h_fitness = sick_vs_healthy_fitness(sick, healthy, cv=5)

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
        results = {}
        for label, genes in selected_genes_dict.items():
            results[label] = self.computeExpressionMatrix(sick, healthy, genes)

        return results

    '''
        sick and healthy should contain at least one cancer type
        selected_genes: call with result from feature selection
    '''
    def computeExpressionMatrix(self, sick, healthy, selected_genes):
        expressions = defaultdict(list)
        for label in np.unique(sick.labels):
            cancertype = label.split("-")[0]

            healthy_X = healthy.expressions[healthy.labels==cancertype+"-healthy"]
            sick_X = sick.expressions[sick.labels==cancertype+"-sick"]

            for gene in selected_genes:
                if healthy_X.shape[0] < 20:
                    U_high, p_high = mannwhitneyu(sick_X[:,gene], healthy_X[:,gene], alternative="greater")
                    U_low,  p_low  = mannwhitneyu(sick_X[:,gene], healthy_X[:,gene], alternative="less")
                    expression = "greater" if p_high < 0.01 else "less" if p_low < 0.01 else "unchanged"
                    expressions[cancertype].append("cant compute - " + expression)
                else:
                    U_high, p_high = mannwhitneyu(sick_X[:,gene], healthy_X[:,gene], alternative="greater")
                    U_low,  p_low  = mannwhitneyu(sick_X[:,gene], healthy_X[:,gene], alternative="less")
                    expressions[cancertype].append("greater" if p_high < 0.01 else "less" if p_low < 0.01 else "unchanged")
        return expressions
