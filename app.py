import json
import re

from flask import Flask, request, abort
from flask_cors import CORS
from utils.DataLoader import DataLoader
from server import availableAlgorithms, externalApiCalls, algorithmExecution

datasets = {
    "dataset4": "Dataset 4 | TCGA",
    "dataset5": "Dataset 5 | TCGA + GTEX"
}
dataLoaders = {dataset: DataLoader(dataset) for dataset in datasets}
statistics = {dataset: dataLoader.getStatistics()
              for (dataset, dataLoader) in dataLoaders.items()}

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/testGenes', methods=["POST"])
def test_genes():
    return json.dumps(externalApiCalls.testGenes(request))


@app.route("/context", methods=["GET"])
def context():
    response = {
        'datasets': datasets,
        'statistics': statistics,
        'algorithms': availableAlgorithms.algorithms
    }
    return json.dumps(response)


@app.route("/runAlgorithm", methods=["POST"])
def runSpecificAlgorithm():
    algorithm = request.get_json()["algorithm"]
    if "dataset" not in algorithm:
        return abort(400, "need dataset parameter")

    dataset = algorithm["dataset"]

    if dataset not in dataLoaders:
        return abort(400, "unknown datatset id")

    dataLoader = dataLoaders[dataset]

    data = algorithmExecution.getData(algorithm, dataLoader)

    response_data, gene_indices = algorithmExecution.run(
        algorithm, data)
    expression_matrix = algorithmExecution.calcExpressionMatrix(
        algorithm, data, gene_indices)
    evaluation = algorithmExecution.evaluate(
        algorithm, data, gene_indices)

    response = {
        'data': response_data,
        'genes': dataLoader.getGeneLabels()[gene_indices].tolist(),
        'expressionMatrix': expression_matrix,
        'geneNames': dataLoader.getGeneNames()[gene_indices].tolist(),
        'evaluation': evaluation,
    }

    # workaround to replace NaN by null
    jsonResponse = json.dumps(response)
    regex = re.compile(r'\bNaN\b')
    return re.sub(regex, 'null', jsonResponse)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True, threaded=True)
