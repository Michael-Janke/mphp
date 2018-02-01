import numpy as np

from utils.DimensionalityReducer import DimensionalityReducer
from validation.Analyzer import Analyzer

dimReducer = DimensionalityReducer()
analyzer = Analyzer()

method_table = {
    "getFeatures": "features",
    "getDecisionTreeFeatures": "tree",
    "getNormalizedFeaturesE": "norm",
    "getNormalizedFeaturesS": "norm",
    "getFeaturesBySFS": "sfs",
}

normalization_table = {
    "getNormalizedFeaturesE": "exclude",
    "getNormalizedFeaturesS": "substract",
}

def execute(algorithm, dataLoader, oneAgainstRest):
    data = getData(algorithm, dataLoader)

    if oneAgainstRest:
        features = run(algorithm, data, oneAgainstRest)
        matrix = calcExpressionMatrix(algorithm, data, features, oneAgainstRest)
        evaluation = evaluate(algorithm, data, features, oneAgainstRest)

        # TODO assemble result

        return None
    else:
        response_data, gene_indices = run(
            algorithm, data)
        expression_matrix = calcExpressionMatrix(
            algorithm, data, gene_indices)
        evaluation = evaluate(
            algorithm, data, gene_indices)

        return {
            'data': {key: scores[0:3] for (key, scores) in response_data.items()},
            'genes': dataLoader.getGeneLabels()[gene_indices].tolist(),
            'expressionMatrix': expression_matrix,
            'geneNames': dataLoader.getGeneNames()[gene_indices].tolist(),
            'evaluation': evaluation,
        }

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


def run(algorithm, data, oneAgainstRest):
    key = algorithm["key"]
    n_components = algorithm["parameters"].get("n_components")
    n_f_components = algorithm["parameters"].get("n_features_per_component")
    k = algorithm["parameters"].get("k")
    n = algorithm["parameters"].get("n")

    if oneAgainstRest:
        sick = data["sick"]
        healthy = "" if not len(data["healthy"].labels) else data["healthy"]
        method = method_table[key]
        normalization = normalization_table.get(key)
        if normalization != None:
            return dimReducer.getOneAgainstRestFeatures(sick, healthy, k, method=method, normalization=normalization)
        else:
            return dimReducer.getOneAgainstRestFeatures(sick, healthy, k, method=method)
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

    X = data["combined"].expressions[:, gene_indices]

    response_data = {}
    for label in np.unique(labels):
        response_data[label] = X[labels == label, :].T.tolist()

    return response_data, gene_indices


def calcExpressionMatrix(algorithm, data, gene_indices, oneAgainstRest):
    # only calc expression matrix if doto contains sick an healthy samples
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]
    if len(sick_tissue_types) == 0 or len(healthy_tissue_types) == 0:
        return None

    X = np.vstack(
        (data["sick"].expressions[:, gene_indices], data["healthy"].expressions[:, gene_indices]))

    if oneAgainstRest:
        return analyzer.computeExpressionMatrixOneAgainstRest(data["sick"], data["healthy"], gene_indices)
    else:
        return analyzer.computeExpressionMatrix(data["sick"], data["healthy"], gene_indices)


def evaluate(algorithm, data, gene_indices, oneAgainstRest):
    cancer_types = algorithm["cancerTypes"]
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]

    if len(cancer_types) == 1 or len(sick_tissue_types) == 0 or len(healthy_tissue_types) == 0:
        sick = data["combined"]
        healthy = ""
    else:
        sick = data["sick"]
        healthy = data["healthy"]

    if oneAgainstRest:
        return analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, gene_indices)
    else:
        return analyzer.computeFeatureValidation(sick, healthy, gene_indices)
