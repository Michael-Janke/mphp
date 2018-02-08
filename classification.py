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

if __name__ == '__main__':
    print("Imported modules")

    dataLoader = DataLoader("dataset4")
    dimReducer = DimensionalityReducer()
    analyzer = Analyzer()

    clusVal = ClusterValidator()
    classVal = ClassificationValidator()
    sampler = Sampler()
    print("data loaded")

    healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
    #healthy = sampler.over_sample(healthy)

    sick = dataLoader.getData(["sick"], ["THCA","LUAD", "HNSC", "KIRC", "UCEC"])
    data = dataLoader.getData(["sick", "healthy"], ["THCA","LUAD", "HNSC", "KIRC", "UCEC"])
    gene_labels = dataLoader.getGeneLabels()
    print("got combined data")

    """
    features = dimReducer.getOneAgainstRestFeatures(sick,healthy)
    pprint(features)

    results = analyzer.computeFeatureValidationOneAgainstRest(sick, healthy, features)
    pprint(results)

    expressions = analyzer.computeExpressionMatrixOneAgainstRest(sick, healthy, features)
    pprint(expressions)

    # Feature Selection
    #selected_genes = dimReducer.getEAFeatures(sick,healthy,fitness="clustering")
    #selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 3, fitness="combined")
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
    """


    #start = datetime.now()
    #selected_genes = dimReducer.getFeaturesBySFS(sick, healthy, 10, m=100 ,fitness="classification", returnMultipleSets = False)
    selected_genes = dimReducer.getNormalizedFeaturesE(sick, healthy, k=3, n=10000, m="chi2", returnMultipleSets=True)
    print(selected_genes)
    #pprint(analyzer.computeFeatureValidation(sick, healthy, selected_genes)["fitness"])
    #print(datetime.now() - start)
