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

def getInvertedEntrezNamesMap():
    inverted_file = "data/gene_names/entrez_names_inverted"

    if not os.path.isfile(inverted_file + ".npy"):
        entrez_labels_map = np.load("data/gene_names/entrez_names.npy").item()
        inverted_entrez_labels_map = {v: k for k, v in entrez_labels_map.items()}
        np.save(inverted_file, inverted_entrez_labels_map)

    return np.load(inverted_file+ ".npy").item()

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
        print("Error disgenet: " + gene)

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
        print("Error protein atlas: " + gene)
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
        print("Error entrez gene summary: " + gene)
    return False


def lookupCoxpresdb(gene):
    entrez_file = "data/gene_names/entrez_names.npy"
    entrez_labels_map = np.load(entrez_file).item()

    coexpressedGenes = []
    try:
        url = 'http://coxpresdb.jp/cgi-bin/api2.cgi?gene=' + entrez_labels_map[int(gene[4:])]
        file_name = 'data/coxpresdb/' + gene + '.json'

        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        if not os.path.isfile(file_name):
            urllib.request.urlretrieve(url, file_name)


        f = open(file_name, 'r')
        response = json.load(f)
        f.close()

        results = response["results"]
        for item in results:
            if item["mutual_rank"] > 10:
                break
            coexpressedGenes.append(item["gene"])

    except:
        print("Error coxpresdb: " + gene)

    return coexpressedGenes

def testGenes(genes, cache):
    response = {}
    cancer_gene_census_data = getCancerGeneCensusData()

    for gene in genes:
        cache_key = "V3_" + gene
        if cache.isCached(cache_key):
            response[gene] = cache.getCache(cache_key)
            continue
        disgenet = gene if lookupDisgenet(gene) else None
        proteinAtlas = gene if lookupProteinAtlas(gene) else None
        cancerGeneCensus = gene if lookupCancerGeneCensus(gene, cancer_gene_census_data) else None
        entrezGeneSummary = gene if lookupEntrezGeneSummary(gene) else None

        coexpressedGenes = lookupCoxpresdb(gene)
        inverted_entrez_labels_map = getInvertedEntrezNamesMap()

        try:
            for coGene in coexpressedGenes:
                coGeneName = "ENSG" + str(inverted_entrez_labels_map[coGene]).zfill(11)
                if not disgenet:
                    disgenet = coGeneName if lookupDisgenet(coGeneName) else None
                if not proteinAtlas:
                    proteinAtlas = coGeneName if lookupProteinAtlas(coGeneName) else None
                if not cancerGeneCensus:
                    cancerGeneCensus = coGeneName if lookupCancerGeneCensus(coGeneName, cancer_gene_census_data) else None
                if not entrezGeneSummary:
                    entrezGeneSummary = coGeneName if lookupEntrezGeneSummary(coGeneName) else None
        except:
            print("Error. No Inverted Entrez Label Entry.")

        score = (0.4 if cancerGeneCensus else 0) + \
            (0.2 if disgenet else 0) + \
            (0.2 if proteinAtlas else 0) + \
            (0.2 if entrezGeneSummary else 0)
        score = round(score, 2)

        response[gene] = {
            'proteinAtlas': proteinAtlas,
            'disgenet': disgenet,
            'cancer_gene_census': cancerGeneCensus,
            'entrezGeneSummary': entrezGeneSummary,
            'score': score
        }

        cache.cache(cache_key, response[gene])

    return response
