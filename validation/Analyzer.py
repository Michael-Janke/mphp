import numpy as np
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator
from utils.EA.fitness import classification_fitness, clustering_fitness, distance_fitness, combined_fitness
from utils import Expressions, binarize_labels
from collections import defaultdict

from numpy.core.defchararray import find
from scipy.stats import mannwhitneyu

class Analyzer:
    def __init__(self):
        pass

    def computeFeatureValidationOneAgainstRest(self, sick, healthy, selected_genes_dict):
        results = {}
        for label, genes in selected_genes_dict.items():
            s_labels = binarize_labels(sick.labels, label)
            sick_binary = Expressions(sick.expressions, s_labels)

            if healthy == "":
                results[label] = self.computeFeatureValidation(sick_binary, "", genes)
            else:
                h_labels = binarize_labels(healthy.labels, label)
                healthy_binary = Expressions(healthy.expressions, h_labels)
                results[label] = self.computeFeatureValidation(sick_binary, healthy_binary, genes)

        return results

    def computeFeatureValidation(self, sick, healthy, selected_genes):
        sick_validation = self.assembleValidationOutput(sick, selected_genes)

        if healthy == "":
            return sick_validation

        healthy_validation = self.assembleValidationOutput(healthy, selected_genes)

        class_fitness = classification_fitness(sick, healthy, selected_genes)
        clus_fitness = clustering_fitness(sick, healthy, selected_genes)
        comb_fitness = combined_fitness(sick, healthy, selected_genes)
        dist_fitness = distance_fitness(sick, healthy, selected_genes)

        return {
            "sick": sick_validation,
            "healthy": healthy_validation,
            "fitness": {
                "classificationFitness": class_fitness,
                "clusteringFitness": clus_fitness,
                "distanceFitness": dist_fitness,
                "combinedFitness": comb_fitness,
            }
        }

    def assembleValidationOutput(self, X, selected_genes):
        clusVal = ClusterValidator()
        classVal = ClassificationValidator()
        classification = classVal.evaluate(X, selected_genes, ["*"])
        clustering = clusVal.evaluate(X, selected_genes, ["*"], ["*"])
        return {"classification": classification, "clustering": clustering}


    def computeExpressionMatrixOneAgainstRest(self, sick, healthy, selected_genes_dict):
        results = {}
        for label, genes in selected_genes_dict.items():
            results[label] = self.computeExpressionMatrix(sick, healthy, genes)

        return results

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
