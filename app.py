import json
import re

from flask import Flask, request, abort, send_from_directory
from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.Cache import Cache
from server import availableAlgorithms, externalApiCalls, algorithmExecution
import optparse
import os

datasets = {
    "dataset4": "Dataset 4 | TCGA",
    "dataset5": "Dataset 5 | TCGA + GTEX"
}
dataLoaders = {dataset: DataLoader(dataset) for dataset in datasets}
statistics = {dataset: dataLoader.getStatistics()
              for (dataset, dataLoader) in dataLoaders.items()}
cache = Cache()
app = Flask(__name__)
CORS(app)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    if(os.path.exists('client/build/' + path)):
        return send_from_directory('client/build/', path)
    else:
        return send_from_directory('client/build/', 'index.html')


@app.route('/static/js/<path:path>')
def servejs(path):
    return send_from_directory('client/build/static/js/', path)


@app.route('/static/media/<path:path>')
def servemedia(path):
    return send_from_directory('client/build/static/media/', path)


@app.route('/testGenes', methods=["POST"])
def test_genes():
    genes = request.get_json()["genes"]["genes"]
    return json.dumps(externalApiCalls.testGenes(genes, cache))


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

    cache_key = "_".join((
        "V2",
        dataset, 
        algorithm["key"],
        "-".join([key+str(value) for key,value in algorithm["parameters"].items()]),
        "-".join(algorithm["cancerTypes"]),
        "-".join(algorithm["healthyTissueTypes"]),
        "-".join(algorithm["sickTissueTypes"])
        ))
    if cache.isCached(cache_key):
        return cache.getCache(cache_key)

    data = algorithmExecution.getData(algorithm, dataLoader)

    response_data, gene_indices = algorithmExecution.run(algorithm, data)
    expression_matrix = algorithmExecution.calcExpressionMatrix(algorithm, data, gene_indices)
    evaluation = algorithmExecution.evaluate(algorithm, data, gene_indices)

    response = {
        'data': {key: scores[0:3] for (key, scores) in response_data.items()},
        'genes': dataLoader.getGeneLabels()[gene_indices].tolist(),
        'expressionMatrix': expression_matrix,
        'geneNames': dataLoader.getGeneNames()[gene_indices].tolist(),
        'evaluation': evaluation,
    }

    # workaround to replace NaN by null
    json_response = json.dumps(response)
    json_respone = re.sub(r'\bNaN\b', 'null', json_response)
    cache.cache(cache_key, json_respone)
    return json_respone


def flaskrun(app, default_host="0.0.0.0",
                  default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " +
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                           "[default %s]" % default_port,
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )


if __name__ == '__main__':
    flaskrun(app)
