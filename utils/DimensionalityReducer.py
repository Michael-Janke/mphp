import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_classif
from sklearn.tree import DecisionTreeClassifier
from scipy.stats import rankdata
from random import random

import utils.EA.config as c
import utils.EA.fitness as fitness_module
from utils.EA.crossover import *
from utils.EA.mutation import *
from utils.EA.population import phenotype
from utils.EA.algorithm import ea_for_plot

from utils import Expressions, binarize_labels

class DimensionalityReducer():
    ####### PCA #######

    def __init__(self):
        self.method_table = {
            "chi2": chi2,
            "f_classif": f_classif,
            "mutual_info_classif": mutual_info_classif
        }

    def getPCA(self, data, n_components, n_features_per_component=10):
        pca = PCA(n_components=n_components, svd_solver='full')
        pca.fit(data)
        X = pca.transform(data)

        gene_indices = []
        for i in range(n_components):
            indices = np.argsort(np.absolute(
                pca.components_[i]))[-n_features_per_component:]
            if len(gene_indices) == 0:
                gene_indices = indices
            else:
                gene_indices = np.concatenate((gene_indices, indices))

        gene_indices = np.unique(gene_indices)

        return gene_indices


    ####### FEATURE SELECTION BY STATISTICS #######

    def getFeatures(self,  data, k=20, m="chi2", returnMultipleSets = False):
        selector = SelectKBest(self.method_table[m], k=k)
        selector.fit(data.expressions, data.labels)

        return self.getFeatureSets(selector.scores_, k, returnMultipleSets)

    def getNormalizedFeatures(self, sick, healthy, normalization="exclude", k=20, n=5000, m="chi2", returnMultipleSets = False):
        options = {
            'substract': self.getNormalizedFeaturesS,
            'exclude': self.getNormalizedFeaturesE,
        }

        return options[normalization](sick, healthy, k, n, m, returnMultipleSets)

    def getNormalizedFeaturesS(self, sick, healthy, k, n, m, returnMultipleSets = False):
        selector = SelectKBest(self.method_table[m], k="all")
        selector.fit(healthy.expressions, healthy.labels)
        healthy_scores = selector.scores_
        healthy_scores /= max(healthy_scores)

        selector.fit(sick.expressions, sick.labels)
        sick_scores = selector.scores_
        sick_scores /= max(sick_scores)

        # subtract healthy scores from sick scores (this is the normalization)
        scores = (sick_scores - healthy_scores)

        return self.getFeatureSets(scores, k, returnMultipleSets)

    def getNormalizedFeaturesE(self, sick, healthy, k, n, m, returnMultipleSets = False):
        selector = SelectKBest(self.method_table[m], k=n)
        selector.fit(healthy.expressions, healthy.labels)
        h_indices = selector.get_support(indices=True)

        selector = SelectKBest(self.method_table[m], k=n + k)
        selector.fit(sick.expressions, sick.labels)
        s_indices = selector.get_support(indices=True)

        # get features in sick data which do not discriminate healty data
        features = list(set(s_indices)-set(h_indices))
        print("excluded "+str(n+k-len(features))+" features")
        features = np.asarray(features, dtype=np.uint32)

        if not returnMultipleSets:
            return features[selector.scores_[features].argsort()[-k:][::-1]]

        sets = self.getFeatureSets(selector.scores_[features], k, returnMultipleSets)

        return [features[f_set] for f_set in sets]

    ####### MULTI-VARIATE FEATURE SELECTION #######

    def getEAFeatures(self, sick, healthy, k=3, n=5000, m=100, normalization="exclude", fitness="combined", returnMultipleSets = False, true_label=""):
        # preselect features to reduce runtime
        selected_genes = self.getNormalizedFeatures(sick,healthy,normalization, m, n)

        crossover = one_point_crossover
        mutation = binary_mutation

        sick_reduced = Expressions(sick.expressions[:, selected_genes], sick.labels)
        healthy_reduced = Expressions(healthy.expressions[:, selected_genes], healthy.labels)

        fitness_function = fitness_module.fitness(sick_reduced, healthy_reduced, fitness, k, true_label)

        best, sets, _, _ = ea_for_plot(c, m, k, fitness_function, crossover, mutation)

        if not returnMultipleSets:
            indices = selected_genes[phenotype(best)]
            return indices

        return [selected_genes[feature_set] for feature_set in sets]

    def getFeaturesBySFS(self, sick, healthy, k=3, n=5000, m=100, normalization="exclude", fitness="combined", returnMultipleSets = False, true_label=""):
        # preselect 100 genes in sick data which do not separate healthy data well
        selected_genes = self.getNormalizedFeatures(sick,healthy,normalization, m, n)

        best_set = self.getFeatureSetBySFS(sick, healthy, selected_genes, k, fitness, true_label=true_label)

        if not returnMultipleSets:
            return best_set

        sets = [best_set]
        for i in range(1,3):
            print("finished feature set")
            sets.append(self.getFeatureSetBySFS(sick, healthy, selected_genes[i:], k, fitness))

        return np.asarray(sets)

    def getFeatureSetBySFS(self, sick, healthy, genes, k, fitness, true_label=""):
        # first gene has highest score and will be selected first
        indices = [genes[0]]
        # iteratively join the best next feature based on a fitness function until k features are found
        for idx in range(k-1):
            best_fitness = -10
            best_gene = 0
            for i in range(1, len(genes)):
                gene = genes[i]
                if gene in indices:
                    continue

                fitness_function = fitness_module.get_fitness_function_name(fitness)
                fitness_score = getattr(fitness_module, fitness_function)(sick, healthy, indices + [gene], true_label=true_label)

                if fitness_score > best_fitness:
                    best_fitness = fitness_score
                    best_gene = gene
            indices.append(best_gene)
            print("added new feature")

        return np.asarray(indices)

    ####### EMBEDDED FEATURE SELECTION #######

    def getDecisionTreeFeatures(self, data, k=20, returnMultipleSets = False):
        tree = DecisionTreeClassifier()
        tree.fit(data.expressions, data.labels)

        return self.getFeatureSets(tree.feature_importances_, k, returnMultipleSets)


    ####### 1 vs Rest #######

    def getOneAgainstRestFeatures(self, sick, healthy, k=3, method="sfs", normalization="exclude", fitness="combined"):
        features = {}
        for label in np.unique(sick.labels):
            label = label.split("-")[0]
            s_labels = binarize_labels(sick.labels, label)
            sick_binary = Expressions(sick.expressions, s_labels)

            if healthy == "":
                if method == "tree":
                    indices = self.getDecisionTreeFeatures(sick_binary, k)
                else:
                    indices = self.getFeatures(sick_binary, k)

            else:
                h_labels = binarize_labels(healthy.labels, label)
                healthy_binary = Expressions(healthy.expressions, h_labels)

                if method == "ea":
                    indices = self.getEAFeatures(sick, healthy, k, normalization=normalization, fitness=fitness, true_label=label)
                elif method == "norm":
                    indices = self.getNormalizedFeatures(sick_binary, healthy_binary, normalization, k)
                else:
                    indices = self.getFeaturesBySFS(sick, healthy, k, normalization=normalization, fitness=fitness, true_label=label)

            features[label] = indices

        return features


    ####### UTILS #######

    def getFeatureSets(self, scores, k, returnMultipleSets):
        best_set = scores.argsort()[-k:][::-1]

        if not returnMultipleSets:
            return best_set

        sets = [best_set]
        for i in range(1,3):
            sets.append(self.getFeatureSet(scores, k))

        return sets

    def getFeatureSet(self, scores, k):
        indices = scores.argsort()[::-1]

        scores /= rankdata(scores, method='min')
        scores = sorted(scores, reverse=True)
        scores /= np.sum(scores)

        features = []

        while len(features) < k:
            feature = self.getFeature(scores)
            while feature in features:
                feature += 1

            features.append(feature)

        return indices[features]

    def getFeature(self, scores):
        cumulated_prob = 0
        i = 0
        while cumulated_prob < random():
            cumulated_prob += scores[i]
            i += 1
        return i
