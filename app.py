import json
import numpy as np

from flask import Flask
from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer

app = Flask(__name__)
CORS(app)
dataLoader = DataLoader("dataset4")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=["GET"])
def getData():
    gene_labels = dataLoader.getGeneLabels()
    dimReducer = DimensionalityReducer()
    luad_thca = dataLoader.getData(["sick", "healthy"], ["LUAD","THCA"])
    # pca, X, pca_indices = dimensionalityReducer.getPCA(data, 3, 20)
    indices, X = dimReducer.getFeatures(luad_thca, 20)

    response = {
        'data': X.tolist(),
        'labels': luad_thca.labels.tolist(),
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)

@app.route('/plot', methods=["GET"])
def getPlotData():
    gene_labels = dataLoader.getGeneLabels()
    dimReducer = DimensionalityReducer()
    healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
    sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
    indices, s_data, _ = dimReducer.getNormalizedFeatures(sick, healthy, "exclude", 3, 5000)

    data = {}
    for label in np.unique(sick.labels):
        data[label] = s_data[sick.labels==label,:].T.tolist()

    response = {
        'data': data,
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)

@app.route('/statistics', methods=["GET"])
def getStatistics():
    statistics = dataLoader.getStatistics()

    return json.dumps(statistics.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
