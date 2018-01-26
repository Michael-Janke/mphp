import pandas as pd
import numpy as np
import os.path
import json
import urllib

from SPARQLWrapper import SPARQLWrapper, JSON
from xml.dom.minidom import parse, parseString


def getCancerGeneCensusData():
    csv_file = 'data/cancer_gene_census.csv'
    return pd.read_csv(csv_file)


def lookupDisgenet(gene):
    entrez_file = "data/gene_names/entrez_names.npy"
    entrez_labels_map = np.load(entrez_file).item()
    gene_url = '<http://identifiers.org/ncbigene/' + \
        entrez_labels_map[int(gene[4:])] + '>'
    file_name = 'data/disgenet/' + gene + '.json'
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
            if hasattr(var, 'items'):
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

        semantic_types = search('semanticType', json_data)
        for semantic_type in semantic_types:
            for k, v in semantic_type.items():
                if k == 'value':
                    if 'T191' in v:
                        return True
    return False


def lookupProteinAtlas(gene):
    try:
        url = 'https://www.proteinatlas.org/' + gene + '.xml'
        file_name = 'data/proteinatlas/' + gene + '.xml'
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        if not os.path.isfile(file_name):
            urllib.request.urlretrieve(url, file_name)

        f = open(file_name, 'r')
        xml = f.read()
        f.close()
        dom = parseString(xml)
        proteinClass = dom.getElementsByTagName('proteinClass')
        for c in proteinClass:
            if c.attributes['name'].value == "Cancer-related genes":
                return True
    except:
        print("Error accessing proteinatlas for gene: " + gene)
    return False


def lookupCancerGeneCensus(gene, cancer_gene_census_data):
    census_data_genes = cancer_gene_census_data['Synonyms'].tolist()
    for gene_synonyms in census_data_genes:
        # filter out NaN values
        if gene_synonyms == gene_synonyms:
            if gene in gene_synonyms:
                return True
    return False


def lookupEntrezGeneSummary(gene):
    entrez_file = "data/gene_names/entrez_names.npy"
    entrez_labels_map = np.load(entrez_file).item()
    try:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=' + \
            entrez_labels_map[int(gene[4:])]
        file_name = 'data/entrezgene/' + gene + '.xml'
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        if not os.path.isfile(file_name):
            urllib.request.urlretrieve(url, file_name)

        f = open(file_name, 'r')
        xml = f.read()
        f.close()
        dom = parseString(xml)
        summary = dom.getElementsByTagName(
            'Summary')[0].childNodes[0].nodeValue
        if "cancer" in summary:
            return True
    except:
        print("Error accessing entrez gene summary for gene: " + gene)
    return False


def testGenes(genes, cache):

    response = {}

    cancer_gene_census_data = getCancerGeneCensusData()

    for gene in genes:
        cache_key = "V1_" + gene
        if cache.isCached(cache_key):
            response[gene] = cache.getCache(cache_key)
            continue
        disgenet = lookupDisgenet(gene)
        proteinAtlas = lookupProteinAtlas(gene)
        cancerGeneCensus = lookupCancerGeneCensus(
            gene, cancer_gene_census_data)
        entrezGeneSummary = lookupEntrezGeneSummary(gene)

        score = (0.4 if cancerGeneCensus else 0) + \
            (0.2 if disgenet else 0) + (0.2 if proteinAtlas else 0) + (0.2 if entrezGeneSummary else 0)
        response[gene] = {'proteinAtlas': proteinAtlas, 'disgenet': disgenet,
                          'cancer_gene_census': cancerGeneCensus, 'entrezGeneSummary': entrezGeneSummary, 'score': score}

        cache.cache(cache_key, response[gene])

    return response
