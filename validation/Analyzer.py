import numpy as np
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator
from utils.EA.fitness import evaluate, distance_evaluate
from utils import Expressions

class Analyzer:
    def __init__(self):
        pass

    def computeFeatureValidation(self, sick, healthy, selected_genes):
        sick_reduced = Expressions(sick.expressions[:,selected_genes], sick.labels)
        healthy_reduced = Expressions(healthy.expressions[:, selected_genes], healthy.labels)

        sick = self.assembleValidationOutput(sick_reduced)
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
        levels = self.computeExpressionThresholds(healthy, selected_genes)

        expression_matrix = {}
        for label in np.unique(sick.labels):
            indices = np.where(sick.labels == label)
            # compute median for each label and gene
            medians = np.median(sick.expressions[indices,], axis=1).tolist()[0]
            expressions = []

            for index, median in enumerate(medians):
                #compare median with thresholds
                thresholds = levels[label[0:4]][selected_genes[index]]
                if median < thresholds[0]:
                    expressions.append("lower")
                elif median < thresholds[1]:
                    expressions.append("mid-lower")
                elif median < thresholds[2]:
                    expressions.append("unchanged")
                elif median < thresholds[3]:
                    expressions.append("mid-higher")
                else:
                    expressions.append("higher")

            expression_matrix[label] = expressions

        return expression_matrix

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