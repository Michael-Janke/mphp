import json
import numpy as np
import base64

from flask import Flask, request
from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer

app = Flask(__name__)
CORS(app)
dataLoader = DataLoader("dataset4")
gene_labels = dataLoader.getGeneLabels()
dimReducer = DimensionalityReducer()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data', methods=["GET"])
def getData():
    luad_thca = dataLoader.getData(["sick", "healthy"], ["LUAD", "THCA"])
    indices, X = dimReducer.getFeatures(luad_thca, 20)

    response = {
        'data': X.tolist(),
        'labels': luad_thca.labels.tolist(),
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)


@app.route('/plot', methods=["GET"])
def getPlotData():
    healthy = dataLoader.getData(["healthy"], ["THCA", "LUAD"])
    sick = dataLoader.getData(["sick"], ["THCA", "LUAD"])
    indices, s_data, _ = dimReducer.getNormalizedFeatures(
        sick, healthy, "exclude", 3)

    data = {}
    for label in np.unique(sick.labels):
        data[label] = s_data[sick.labels == label, :].T.tolist()

    response = {
        'data': data,
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)


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
    key = algorithm["key"]

    sick = dataLoader.getData(
        algorithm["sickTissueTypes"], algorithm["cancerTypes"])
    healthy = dataLoader.getData(
        algorithm["healthyTissueTypes"], algorithm["cancerTypes"])
    data = dataLoader.getData(
        algorithm["healthyTissueTypes"] + algorithm["sickTissueTypes"], algorithm["cancerTypes"])

    if key == "getPCA":
        _, X, gene_indices = dimReducer.getPCA(
            data.expressions, algorithm["parameters"]["n_components"], algorithm["parameters"]["n_features_per_component"])
    elif key == "getDecisionTreeFeatures":
        gene_indices, X = dimReducer.getDecisionTreeFeatures(
            data, algorithm["parameters"]["k"])
    elif key == "getNormalizedFeaturesE":
        gene_indices, X, Y = dimReducer.getNormalizedFeaturesE(
            sick, healthy, algorithm["parameters"]["k"], algorithm["parameters"]["n"], "chi2")
        X = np.vstack((X, Y))
    elif key == "getNormalizedFeaturesS":
        gene_indices, X, Y = dimReducer.getNormalizedFeaturesS(
            sick, healthy, algorithm["parameters"]["k"], algorithm["parameters"]["n"], "chi2")
        X = np.vstack((X, Y))
    elif key == "getFeatures":
        gene_indices, X = dimReducer.getFeatures(
            data, algorithm["parameters"]["k"])
    elif key == "getFeaturesBySFS":
        gene_indices, X, Y = dimReducer.getFeaturesBySFS(
            sick, healthy)
        X = np.vstack((X, Y))


    responseData = {}
    for label in np.unique(data.labels):
        responseData[label] = X[data.labels == label, :].T.tolist()

    response = {
        'data': responseData,
        'genes': gene_labels[gene_indices].tolist(),
    }
    return json.dumps(response)


@app.route('/statistics', methods=["GET"])
def getStatistics():
    statistics = dataLoader.getStatistics()

    return json.dumps(statistics.tolist())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True, threaded=True)
