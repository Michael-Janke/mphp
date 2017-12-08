import json
import numpy as np

from flask import Flask
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
    luad_thca = dataLoader.getData(["sick", "healthy"], ["LUAD","THCA"])
    indices, X = dimReducer.getFeatures(luad_thca, 20)

    response = {
        'data': X.tolist(),
        'labels': luad_thca.labels.tolist(),
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)

@app.route('/plot', methods=["GET"])
def getPlotData():
    healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
    sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
    indices, s_data, _ = dimReducer.getNormalizedFeatures(sick, healthy, "exclude", 3)

    data = {}
    for label in np.unique(sick.labels):
        data[label] = s_data[sick.labels==label,:].T.tolist()

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
                "name":'Feature Selection Normalization:Exclude',
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
                "name":'Feature Selection Normalization:Substract',
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
            }
        ],

    }

    return json.dumps(response)

@app.route("/runAlgorithm", methods=["POST"])
def runSpecificAlgorithm():
    return runAlgorithm(request.args.get("algorithm",""))

@app.route('/statistics', methods=["GET"])
def getStatistics():
    statistics = dataLoader.getStatistics()

    return json.dumps(statistics.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
