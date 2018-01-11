import numpy as np
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator
from utils.EA.fitness import evaluate, distance_evaluate
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
        sick_reduced = Expressions(sick.expressions[:,selected_genes], sick.labels)
        sick = self.assembleValidationOutput(sick_reduced)

        if healthy == "":
            return sick

        healthy_reduced = Expressions(healthy.expressions[:, selected_genes], healthy.labels)
        healthy = self.assembleValidationOutput(healthy_reduced)

        classificationFitness = evaluate(sick_reduced, healthy_reduced)
        clusteringFitness = distance_evaluate(sick_reduced, healthy_reduced)

        return {
            "sick": sick,
            "healthy": healthy,
            "fitness": {
                "classificationFitness": classificationFitness,
                "clusteringFitness": clusteringFitness
            }
        }

    def assembleValidationOutput(self, X):
        clusVal = ClusterValidator()
        classVal = ClassificationValidator()
        classification = classVal.evaluate(X, ["*"])
        clustering = clusVal.evaluate(X, ["*"], ["*"])
        return {"classifictation": classification, "clustering": clustering}

    def computeExpressionMatrix(self, sick, healthy, selected_genes):
        expressions = defaultdict(list)
        for label in np.unique(sick.labels):
            cancertype = label.split("-")[0]
            healthy_X = healthy.expressions[healthy.labels==cancertype+"-healthy"]
            sick_X = sick.expressions[sick.labels==cancertype+"-sick"]
            for i in range(sick_X.shape[1]):
                if healthy_X.shape[0] < 20:
                    #h = np.concatenate((healthy_X[:,i],healthy_X[:,i],healthy_X[:,i],healthy_X[:,i],healthy_X[:,i],healthy_X[:,i]), axis=0)
                    #print(h.shape)
                    #U_high, p_high = mannwhitneyu(sick_X[:,i], h, alternative="greater")
                    #U_low,  p_low  = mannwhitneyu(sick_X[:,i], h, alternative="less")
                    expressions[cancertype].append("cant compute")
                else:
                    U_high, p_high = mannwhitneyu(sick_X[:,i], healthy_X[:,i], alternative="greater")
                    U_low,  p_low  = mannwhitneyu(sick_X[:,i], healthy_X[:,i], alternative="less")
                    expressions[cancertype].append("greater" if p_high < 0.01 else "less" if p_low < 0.01 else "unchanged")
                    #print(p_low, p_high)
                    #print(np.mean(sick_X[:,i]), np.mean(healthy_X[:,i]))
            #print("====")
        return expressions

    def computeExpressionThresholds(self, healthy, selected_genes):
        levels = {}
        for label in np.unique(healthy.labels):
            levels[label[0:4]] = {}
            for gene in selected_genes:
                indices = np.where(healthy.labels == label)
                reduced_data = healthy.expressions[indices,gene]
                min_thresh = np.percentile(reduced_data, 5)
                max_thresh = np.percentile(reduced_data, 95)
                lower_thresh = np.percentile(reduced_data, 33)
                upper_thresh = np.percentile(reduced_data, 66)
                levels[label[0:4]][gene] = [min_thresh, lower_thresh, upper_thresh, max_thresh]

        return levels
