import json
import numpy as np
import re

from flask import Flask, request, abort
from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from validation.Analyzer import Analyzer
from utils import Expressions

datasets = {
    "dataset4" : "Dataset 4 | TCGA",
    "dataset5" : "Dataset 5 | TCGA + GTEX"
}

app = Flask(__name__)
CORS(app)
dataLoaders = {dataset: DataLoader(dataset) for dataset in datasets}

dimReducer = DimensionalityReducer()
analyzer = Analyzer()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/algorithms", methods=["GET"])
def algorithms():
    response = {
        'algorithms': [
            {
                "name": 'PCA',
                "parameters": [
                    {
                        "name": "#Components",
                        "key": "n_components",
                        "default": 3
                    },
                    {
                        "name": "#Features per component",
                        "key": "n_features_per_component",
                        "default": 10
                    }
                ],
                "key": "getPCA"
            },
            {
                "name": 'Decision Tree',
                "parameters": [
                    {
                        "name": "#Features",
                        "key": "k",
                        "default": 20

                    }
                ],
                "key": "getDecisionTreeFeatures"
            },
            {
                "name": 'Feature Selection Normalization:Exclude',
                "parameters": [
                    {
                        "name": "#Features",
                        "key": "k",
                        "default": 20

                    },
                    {
                        "name": "#Considered features",
                        "key": "n",
                        "default": 5000

                    }
                ],
                "key": "getNormalizedFeaturesE"
            },
            {
                "name": 'Feature Selection Normalization:Substract',
                "parameters": [
                    {
                        "name": "#Features",
                        "key": "k",
                        "default": 20

                    },
                    {
                        "name": "#Considered features",
                        "key": "n",
                        "default": 5000

                    }
                ],
                "key": "getNormalizedFeaturesS"
            },
            {
                "name": "Feature Selection",
                "parameters": [
                    {
                        "name": "#Features",
                        "key": "k",
                        "default": 20

                    }
                ],
                "key": "getFeatures"
            },
            {
                "name": "Sequential Forward Selection (normalized)",
                "key": "getFeaturesBySFS",
                "parameters": []
            }
        ],
    }

    return json.dumps(response)


@app.route("/runAlgorithm", methods=["POST"])
def runSpecificAlgorithm():
    # POST key, parameters, cancerTypes, healthyTissueTypes, sickTissueTypes
    # match to specific algorithm
    algorithm = request.get_json()["algorithm"]
    # algorithm = {
    #     "key": "getPCA",
    #     "cancerTypes": ["LUAD"],
    #     "sickTissueTypes": ["TP"],
    #     "healthyTissueTypes": ["NT"],
    #     "parameters": {
    #         "n_components": 3,
    #         "n_features_per_component": 10
    #         }
    #
    # }

    if "dataset" not in algorithm:
        return abort(400, "need dataset parameter")

    dataset = algorithm["dataset"]
    dataLoader = dataLoaders[dataset]

    key = algorithm["key"]
    cancer_types = algorithm["cancerTypes"]
    sick_tissue_types = algorithm["sickTissueTypes"]
    healthy_tissue_types = algorithm["healthyTissueTypes"]
    n_components = algorithm["parameters"].get("n_components")
    n_f_components = algorithm["parameters"].get("n_features_per_component")
    k = algorithm["parameters"].get("k")
    n = algorithm["parameters"].get("n")

    sick = dataLoader.getData(sick_tissue_types, cancer_types)
    sick = dataLoader.replaceLabels(sick)

    healthy = dataLoader.getData(healthy_tissue_types, cancer_types)
    healthy = dataLoader.replaceLabels(healthy)

    data = dataLoader.getData(sick_tissue_types + healthy_tissue_types, cancer_types)
    data = dataLoader.replaceLabels(data)

    calc_expression_matrix = False
    if key == "getPCA":
        gene_indices = dimReducer.getPCA(data.expressions, n_components, n_f_components)

    elif key == "getFeatures":
        gene_indices = dimReducer.getFeatures(data, k)
        
    elif key == "getDecisionTreeFeatures":
        gene_indices = dimReducer.getDecisionTreeFeatures(data, k)

    elif key == "getNormalizedFeaturesE":
        gene_indices = dimReducer.getNormalizedFeaturesE(sick, healthy, k, n, "chi2")
        calc_expression_matrix = True

    elif key == "getNormalizedFeaturesS":
        gene_indices = dimReducer.getNormalizedFeaturesS(sick, healthy, k, n, "chi2")
        calc_expression_matrix = True

    elif key == "getFeaturesBySFS":
        gene_indices = dimReducer.getFeaturesBySFS(sick, healthy)
        calc_expression_matrix = True

    
    X = data.expressions[:, gene_indices]
    labels = data.labels

    # calculate expression matrix
    expression_matrix = None
    if calc_expression_matrix:        
        X = np.vstack((sick.expressions[:, gene_indices], healthy.expressions[:, gene_indices]))
        labels = np.hstack((sick.labels, healthy.labels))
        expression_matrix = analyzer.computeExpressionMatrix(sick, healthy, gene_indices)

    response_data = {}
    for label in np.unique(labels):
        response_data[label] = X[labels == label, :].T.tolist()

    # evaluation
    evaluation = analyzer.computeFeatureValidation(sick, healthy, gene_indices)

    response = {
        'data': response_data,
        'genes': dataLoader.getGeneLabels[gene_indices].tolist(),
        'expressionMatrix': expression_matrix,
        'geneNames': dataLoader.getGeneNames[gene_indices].tolist(),
        'evaluation': evaluation,
    }

    # workaround to replace NaN by null
    jsonResponse = json.dumps(response)
    regex = re.compile(r'\bNaN\b')
    return re.sub(regex, 'null', jsonResponse)


@app.route('/statistics', methods=["GET"])
def getStatistics():
    dataset = request.args.get('dataset')
    if dataset not in dataLoaders:
        return abort(400, "need dataset parameter")
    statistics = dataLoaders[dataset].getStatistics()

    return json.dumps(statistics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True, threaded=True)
