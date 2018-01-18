import json
import numpy as np
import base64
import urllib
import xml.etree.ElementTree as ET
import rdflib
import os.path
import pandas as pd
import re

from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
from xml.dom.minidom import parse, parseString
from flask import Flask, request,abort

from flask_cors import CORS
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from validation.Analyzer import Analyzer
from utils import Expressions

datasets = {
    "dataset4" : "Dataset 4 | TCGA",
    "dataset5" : "Dataset 5 | TCGA + GTEX"
}
dataLoaders = {dataset: DataLoader(dataset) for dataset in datasets}
statistics = {dataset: dataLoader.getStatistics() for (dataset,dataLoader) in dataLoaders.items()}

app = Flask(__name__)
CORS(app)

dimReducer = DimensionalityReducer()
analyzer = Analyzer()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testGenes', methods=["POST"])
def testGene():
    data = request.get_json()["genes"]
    genes = data["genes"]
    response = {}

    # cancer gene census
    csv_file = 'data/cancer_gene_census.csv'
    cancer_gene_census_data = pd.read_csv(csv_file)
    census_data_genes = cancer_gene_census_data['Synonyms'].tolist()
    for gene in genes:

        #DisGeNet
        disgenet = False
        entrez_file = "data/gene_names/entrez_names.npy"
        entrez_labels_map = np.load(entrez_file).item()
        gene_url = '<http://identifiers.org/ncbigene/' + entrez_labels_map[int(gene[4:])] + '>'
        file_name = 'data/disgenet/'+ gene +'.json'
        results = None
        try:
            if not os.path.isfile(file_name):
                sparql = SPARQLWrapper('http://rdf.disgenet.org/sparql/')
                sparql.setQuery("""
                SELECT DISTINCT
                    ?gda
                    %s as ?gene
                    ?score
                    ?disease
                    ?diseaselabel
                    ?diseasename
                    ?semanticType
                WHERE {
                    ?gda sio:SIO_000628 %s, ?disease ;
                        sio:SIO_000253 ?source ;
                        sio:SIO_000216 ?scoreIRI .
                    ?disease sio:SIO_000008 ?semanticType .
                    ?disease a ncit:C7057 .
                    ?scoreIRI sio:SIO_000300 ?score .
                    FILTER regex(?source, "UNIPROT|CTD_human")
                    FILTER (?score >= 0.2)
                    ?disease dcterms:title ?diseasename .
                    ?disease rdfs:label ?diseaselabel
                }
                ORDER BY DESC(?score)
                """ % (gene_url, gene_url))
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                if not os.path.exists(os.path.dirname(file_name)):
                    os.makedirs(os.path.dirname(file_name))
                with open(file_name, 'w') as outfile:
                    json.dump(results, outfile)

            f = open(file_name, 'r')
            results = json.load(f)
            f.close()
        except:
            print("Error getting / reading disgenet file")

        if results is not None:

            # scan the file for a T191 --> cancer.
            json_data = results
            def search(key, var):
                if hasattr(var,'items'):
                    for k, v in var.items():
                        if k == key:
                            yield v
                        if isinstance(v, dict):
                            for result in search(key, v):
                                yield result
                        elif isinstance(v, list):
                            for d in v:
                                for result in search(key, d):
                                    yield result

            semantic_types = search('semanticType',json_data)
            for semantic_type in semantic_types:
                for k,v in semantic_type.items():
                    if k == 'value':
                        if 'T191' in v:
                            disgenet = True
        #proteinAtlas
        proteinAtlas = False
        try:
            url = 'https://www.proteinatlas.org/'+ gene +'.xml'
            file_name = 'data/proteinatlas/'+ gene +'.xml'
            if not os.path.isfile(file_name):
                urllib.request.urlretrieve(url, file_name)

            f = open(file_name, 'r')
            xml = f.read()
            f.close()
            dom = parseString(xml)
            proteinClass = dom.getElementsByTagName('proteinClass')
            for c in proteinClass:
                if c.attributes['name'].value == "Cancer-related genes":
                    proteinAtlas = True
        except:
            print("Error accessing proteinatlas for gene: " + gene)

        cancer_gene_census = False
        for gene_synonyms in census_data_genes:
            # filter out NaN values
            if gene_synonyms == gene_synonyms:
                if gene in gene_synonyms:
                    cancer_gene_census = True

        if cancer_gene_census:
            print("Found one!")

        response[gene] = {'proteinAtlas': proteinAtlas, 'disgenet': disgenet, 'cancer_gene_census': cancer_gene_census}

    return json.dumps(response)

@app.route("/context", methods=["GET"])
def context():
    response = {
        'datasets': datasets,
        'statistics': statistics,
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

    if dataset not in dataLoaders:
        return abort(400, "unknown datatset id")
    
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

    data = dataLoader.getData(
        sick_tissue_types + healthy_tissue_types, cancer_types)
    data = dataLoader.replaceLabels(data)

    calc_expression_matrix = False
    if key == "getPCA":
        gene_indices = dimReducer.getPCA(
            data.expressions, n_components, n_f_components)

    elif key == "getFeatures":
        gene_indices = dimReducer.getFeatures(data, k)

    elif key == "getDecisionTreeFeatures":
        gene_indices = dimReducer.getDecisionTreeFeatures(data, k)

    elif key == "getNormalizedFeaturesE":
        gene_indices = dimReducer.getNormalizedFeaturesE(
            sick, healthy, k, n, "chi2")
        calc_expression_matrix = True

    elif key == "getNormalizedFeaturesS":
        gene_indices = dimReducer.getNormalizedFeaturesS(
            sick, healthy, k, n, "chi2")
        calc_expression_matrix = True

    elif key == "getFeaturesBySFS":
        gene_indices = dimReducer.getFeaturesBySFS(sick, healthy)
        calc_expression_matrix = True

    X = data.expressions[:, gene_indices]
    labels = data.labels

    # calculate expression matrix
    expression_matrix = None
    if calc_expression_matrix:
        X = np.vstack(
            (sick.expressions[:, gene_indices], healthy.expressions[:, gene_indices]))
        labels = np.hstack((sick.labels, healthy.labels))
        expression_matrix = analyzer.computeExpressionMatrix(
            sick, healthy, gene_indices)

    response_data = {}
    for label in np.unique(labels):
        response_data[label] = X[labels == label, :].T.tolist()

    # evaluation
    if len(cancer_types) == 1 or len(sick_tissue_types) == 0 or len(healthy_tissue_types) == 0:
        evaluation = analyzer.computeFeatureValidation(data, "", gene_indices)
    else:
        evaluation = analyzer.computeFeatureValidation(
            sick, healthy, gene_indices)

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
