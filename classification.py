import numpy as np
from datetime import datetime
from pprint import pprint
from utils.DataLoader import DataLoader
from utils.DimensionalityReducer import DimensionalityReducer
from utils.DataNormalizer import DataNormalizer
from utils.Sampler import Sampler
from utils.plot import plotScatter

from utils import Expressions

from validation.Analyzer import Analyzer
from validation.ClusterValidator import ClusterValidator
from validation.ClassificationValidator import ClassificationValidator

from multiprocessing import Array

if __name__ == '__main__':

    print("Imported modules")

    dataLoader = DataLoader("dataset5")
    dimReducer = DimensionalityReducer()
    analyzer = Analyzer()

    clusVal = ClusterValidator()
    classVal = ClassificationValidator()
    sampler = Sampler()
    print("data loaded")

    #healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
    #healthy = sampler.over_sample(healthy)

    sick = dataLoader.getData(["sick"], ["COAD","THCA"])
    healthy = dataLoader.getData(["healthy"], ["COAD","THCA"])
    data = dataLoader.getData(["sick", "healthy"], ["all"])


    gene_labels = dataLoader.getGeneLabels()
    print("got combined data")

    start = datetime.now()
    #selected_genes = dimReducer.getFeatures(data, 10)
    #selected_genes = dimReducer.getOneAgainstRestFeatures(data, "",5)
    
    #selected_genes = dimReducer.getNormalizedFeatures(sick, healthy, k=10)
    #selected_genes = dimReducer.getOneAgainstRestFeatures(sick, healthy, 10, "norm", "relief")
    #selected_genes = dimReducer.getOneAgainstRestFeatures(sick, healthy, 10, "norm", "exclude")

    #selected_genes = dimReducer.getDecisionTreeFeatures(data, 10)
    #selected_genes = dimReducer.getOneAgainstRestFeatures(data, "", 10, "tree")
    
    #selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 3, fitness="combined", returnMultipleSets =True)
    selected_genes = dimReducer.getOneAgainstRestFeatures(sick, healthy, 3, fitness="combined", normalization="exclude")
    pprint(selected_genes)
    print(datetime.now() - start)
    print("done")
    """
    features = dimReducer.getOneAgainstRestFeatures(sick,healthy)
    pprint(features)

    results = analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, features)
    pprint(results)

    expressions = analyzer.computeExpressionMatrixOneAgainstRest(sick, healthy, features)
    pprint(expressions)

    # Feature Selection
    #selected_genes = dimReducer.getEAFeatures(sick,healthy,fitness="clustering")
    selected_genes = dimReducer.getNormalizedFeatures(sick, healthy, k=3, normalization="relief")
    print(selected_genes)

    print("SICK REDUCED")
    pprint(classVal.evaluate(sick, selected_genes, ["decisionTree"]))
    plotScatter(sick, selected_genes, gene_labels)

    print("HEALTHY REDUCED")
    pprint(classVal.evaluate(healthy, selected_genes, ["decisionTree"]))
    plotScatter(healthy, selected_genes, gene_labels)

    pprint(analyzer.computeFeatureValidation(sick, healthy, selected_genes)["fitness"])
    from datetime import datetime
    start = datetime.now()

    selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 10, fitness="combined", returnMultipleSets = True)
    #selected_genes = dimReducer.getEAFeatures(sick, healthy, fitness="distance", returnMultipleSets = True)
    #selected_genes = dimReducer.getDecisionTreeFeatures(data, 5, returnMultipleSets = True)
    #selected_genes = dimReducer.getNormalizedFeatures(sick, healthy, k=3, returnMultipleSets = True)

    pprint(selected_genes)
    print(datetime.now()-start)


    #start = datetime.now()
    #selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 10, m=100 ,fitness="classification", returnMultipleSets = False)
    #selected_genes = dimReducer.getNormalizedFeaturesE(sick, healthy, k=3, n=10000, m="chi2", returnMultipleSets=True)
    #print(selected_genes)
    #pprint(analyzer.computeFeatureValidation(sick, healthy, selected_genes)["fitness"])
    #print(datetime.now() - start)
    """
