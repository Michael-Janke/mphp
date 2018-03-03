import numpy as np
from datetime import datetime
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.Sampler import Sampler
from utils.plot import plotScatter

from server.externalApiCalls import fullTestGenes

from utils import Expressions

from validation.Analyzer import Analyzer

def gene_score(genes):
    r = fullTestGenes(gene_labels[genes], None)
    print(np.mean([ r[key]['score'] for key in r]))

for ds in ["dataset4", "dataset5"]:
    print("####    " + ds)
    dataLoader = DataLoader(ds)
    sick = dataLoader.getData(["sick"], ["all"])
    healthy = dataLoader.getData(["healthy"], ["all"])

    gene_labels = dataLoader.getGeneLabels()

    for k in [10]:
        dimReducer = DimensionalityReducer()
        gene_score(dimReducer.getFeatures(sick, k))
        gene_score(dimReducer.getDecisionTreeFeatures(data, k))
        gene_score(dimReducer.getNormalizedFeatures(sick, healthy, k=k))
        gene_score(dimReducer.getNormalizedFeatures(sick, healthy, k=k, normalization="subtract"))
        gene_score(dimReducer.getFeaturesBySFS(sick, healthy, k, fitness="combined"))
        gene_score(getEAFeatures(sick, healthy, k, fitness="combined"))
