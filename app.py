import json
import numpy as np

from flask import Flask
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer

app = Flask(__name__)
dataLoader = DataLoader("dataset4")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=["GET"])
def getData():
    gene_labels = dataLoader.getGeneLabels()
    dimensionalityReducer = DimensionalityReducer()
    data, labels = dataLoader.getData(["sick", "healthy"], ["LUAD","THCA"])
    # pca, X, pca_indices = dimensionalityReducer.getPCA(data, 3, 20)
    indices, X = dimensionalityReducer.getFeatures(data, labels, 20)

    response = {
        'data': X.tolist(),
        'labels': labels.tolist(),
        'genes': gene_labels[indices].tolist(),
    }

    return json.dumps(response)

@app.route('/statistics', methods=["GET"])
def getStatistics():
    dataLoader = DataLoader("dataset4")
    statistics = dataLoader.getStatistics()

    return json.dumps(statistics.tolist())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', use_reloader=True)
