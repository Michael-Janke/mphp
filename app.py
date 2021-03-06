import json
import re

from flask import Flask, request, abort, send_from_directory
from werkzeug.serving import run_simple
from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.Cache import Cache
from server import availableAlgorithms, externalApiCalls, algorithmExecution
import optparse
import os

datasets = {
    "dataset4": "TCGA",
    "dataset5": "TCGA + GTEX"
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
    genes = request.get_json()["genes"]
    return json.dumps(externalApiCalls.testGenes(genes, cache))

@app.route('/fullTestGenes', methods=["POST"])
def full_test_genes():
    genes = request.get_json()["genes"]
    return json.dumps(externalApiCalls.fullTestGenes(genes, cache))


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
    requestObject = request.get_json()
    algorithm = requestObject["algorithm"]
    oneAgainstRest = requestObject["oneAgainstRest"]
    oversampling = requestObject["oversampling"]

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
        str(oneAgainstRest),
        str(oversampling),
        "-".join([key+str(value) for key,value in algorithm["parameters"].items()]),
        "-".join(algorithm["cancerTypes"]),
        "-".join(algorithm["healthyTissueTypes"]),
        "-".join(algorithm["sickTissueTypes"])
        ))
    if cache.isCached(cache_key):
        return cache.getCache(cache_key)

    response = algorithmExecution.execute(algorithm, dataLoader, oneAgainstRest, oversampling)

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
    parser.add_option("-t", "--threaded",
                      action="store_true",
                      dest="threaded",
                      default=False,
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--processes",
                      dest="processes",
                      default=1,
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                           "[default %s]" % default_port,
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    run_simple(options.host, int(options.port), app,
        use_reloader=options.debug,
        threaded=options.threaded,
        processes=int(options.processes)
    )


if __name__ == '__main__':
    flaskrun(app)
