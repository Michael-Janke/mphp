import numpy as np

from utils.DimensionalityReducer import DimensionalityReducer
from validation.Analyzer import Analyzer

dimReducer = DimensionalityReducer()
analyzer = Analyzer()


def getData(algorithm, dataLoader):
    cancer_types = algorithm["cancerTypes"]
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]

    sick = dataLoader.getData(sick_tissue_types, cancer_types)
    sick = dataLoader.replaceLabels(sick)
    healthy = dataLoader.getData(healthy_tissue_types, cancer_types)
    healthy = dataLoader.replaceLabels(healthy)
    combined = dataLoader.getData(
        sick_tissue_types + healthy_tissue_types, cancer_types)
    combined = dataLoader.replaceLabels(combined)

    data = {
        "sick": sick,
        "healthy": healthy,
        "combined": combined
    }
    return data


def run(algorithm, data, one_against_rest):
    key = algorithm["key"]
    n_components = algorithm["parameters"].get("n_components")
    n_f_components = algorithm["parameters"].get("n_features_per_component")
    k = algorithm["parameters"].get("k")
    n = algorithm["parameters"].get("n")

    if one_against_rest:
        healthy = "" if len(data["healthy"].expressions) == 0 else data["healthy"]
        gene_indices = dimReducer.getOneAgainstRestFeatures(data["sick"], healthy, k, key)
        labels = data["combined"].labels

    elif key == "getPCA":
        gene_indices = dimReducer.getPCA(
            data["combined"].expressions, n_components, n_f_components)
        labels = data["combined"].labels

    elif key == "getFeatures":
        gene_indices = dimReducer.getFeatures(data["combined"], k)
        labels = data["combined"].labels

    elif key == "getDecisionTreeFeatures":
        gene_indices = dimReducer.getDecisionTreeFeatures(data["combined"], k)
        labels = data["combined"].labels

    elif key == "getNormalizedFeaturesE":
        gene_indices = dimReducer.getNormalizedFeaturesE(
            data["sick"], data["healthy"], k, n, "chi2")
        labels = np.hstack((data["sick"].labels, data["healthy"].labels))

    elif key == "getNormalizedFeaturesS":
        gene_indices = dimReducer.getNormalizedFeaturesS(
            data["sick"], data["healthy"], k, n, "chi2")
        labels = np.hstack((data["sick"].labels, data["healthy"].labels))

    elif key == "getFeaturesBySFS":
        gene_indices = dimReducer.getFeaturesBySFS(
            data["sick"], data["healthy"])
        labels = np.hstack((data["sick"].labels, data["healthy"].labels))

    response_data = {}

    if one_against_rest:
        for cancer_type in gene_indices:
            response_data[cancer_type] = collect_data(data, gene_indices[cancer_type], labels)
    else:
        response_data = collect_data(data, gene_indices, labels)

    return response_data, gene_indices

def collect_data(data, gene_indices, labels):
    X = data["combined"].expressions[:, gene_indices]
    response_data = {}
    for label in np.unique(labels):
        response_data[label] = X[labels == label, :].T.tolist()
    return response_data

def calcExpressionMatrix(algorithm, data, gene_indices, one_against_rest):
    # TODO assemble the right way
    if one_against_rest:
        return None
    # only calc expression matrix if doto contains sick an healthy samples
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]
    if len(sick_tissue_types) == 0 or len(healthy_tissue_types) == 0:
        return None

    X = np.vstack(
        (data["sick"].expressions[:, gene_indices], data["healthy"].expressions[:, gene_indices]))

    return analyzer.computeExpressionMatrix(data["sick"], data["healthy"], gene_indices)


def evaluate(algorithm, data, gene_indices, one_against_rest):
    cancer_types = algorithm["cancerTypes"]
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]

    if len(cancer_types) == 1 or len(sick_tissue_types) == 0 or len(healthy_tissue_types) == 0:
        sick = data["combined"]
        healthy = ""
    else:
        sick = data["sick"]
        healthy = data["healthy"]

    if one_against_rest:
        return analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, gene_indices)
    else:
        return analyzer.computeFeatureValidation(sick, healthy, gene_indices)
