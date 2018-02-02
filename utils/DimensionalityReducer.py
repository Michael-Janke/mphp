import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_classif
from sklearn.tree import DecisionTreeClassifier
from scipy.stats import rankdata
from random import random, randint
from joblib import Parallel, delayed

import utils.EA.config as c
import utils.EA.fitness as fitness_module
from utils.reliefF import reliefF
from utils.EA.crossover import *
from utils.EA.mutation import *
from utils.EA.algorithm import ea_for_plot

from utils import Expressions, binarize_labels

class DimensionalityReducer():
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

    def getNormalizedFeatures(self, sick, healthy, normalization="relief", k=20, n=5000, m="chi2", returnMultipleSets = False):
        options = {
            'substract': self.getNormalizedFeaturesS,
            'exclude': self.getNormalizedFeaturesE,
            'relief': self.getNormalizedFeaturesR,
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
        print("excluded "+str(n+k-len(features))+" features", flush=True)

        scores = selector.scores_
        scores[h_indices] = 0

        return self.getFeatureSets(scores, k, returnMultipleSets)

    def getNormalizedFeaturesR(self, sick, healthy, k, n, m, returnMultipleSets = False):
        selector = SelectKBest(self.method_table[m], k=n)
        selector.fit(healthy.expressions, healthy.labels)
        h_indices = selector.get_support(indices=True)
        mask = np.ones(selector.scores_.shape,dtype=bool)
        mask[h_indices] = False
        indices = np.where(mask == True)[0]

        X = sick.expressions[:, indices]

        scores = reliefF(X, sick.labels, k=k)

        combined_scores = np.zeros(selector.scores_.shape)
        combined_scores[indices] = scores

        return self.getFeatureSets(combined_scores, k, returnMultipleSets)

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
            indices = selected_genes[best]
            return indices

        return [selected_genes[feature_set] for feature_set in sets]

    def getFeaturesBySFS(self, sick, healthy, k=3, n=5000, m=100, normalization="exclude", fitness="combined", returnMultipleSets = False, true_label=""):
        # preselect 100 genes in sick data which do not separate healthy data well
        selected_genes = self.getNormalizedFeatures(sick,healthy,normalization, m, n)

        if not returnMultipleSets:
            return self.getFeatureSetBySFS(sick, healthy, selected_genes, k, fitness, true_label=true_label)

        results = Parallel(n_jobs=3)\
            (delayed(self.getFeatureSetBySFS)(sick, healthy, selected_genes[i:], k, fitness) for i in range(3))
        
        return np.asarray(results)

    def getFeatureSetBySFS(self, sick, healthy, genes, k, fitness, true_label=""):
        # first gene has highest score and will be selected first
        indices = [genes[0]]

        # iteratively join the best next feature based on a fitness function until k features are found
        for idx in range(k-1):
            if fitness == "combined" or fitness == "clustering":
                n_jobs = int(len(genes) / 20) # 1 process for 20 iterations
            else:
                n_jobs = int(len(genes) / 100) # 1 process for 100 iterations

            chunks = self.chunks(genes, int(len(genes) / n_jobs))
            fitness_scores = Parallel(n_jobs=n_jobs)\
                (delayed(self.call_fitness_function)(sick, healthy, indices, chunks[i], fitness, true_label) for i in range(n_jobs))

            scores = []
            for f in fitness_scores:
                scores.extend(f)
            best_genes = np.asarray(scores).argsort()[::-1]

            i = 0
            while genes[best_genes[i]] in indices:
                i += 1 

            indices.append(genes[best_genes[i]])
            print("added new feature", flush=True)

        return np.asarray(indices)

    def chunks(self, l, n):
        n = max(1, n)
        chunks = [l[i:i+n] for i in range(0, len(l), n)]
        return chunks

    def call_fitness_function(self, sick, healthy, indices, genes, fitness, true_label):
        fitness_function = fitness_module.get_fitness_function_name(fitness)
        fitness_function = getattr(fitness_module, fitness_function)

        results = []
        for gene in genes:
            results.append(fitness_function(sick, healthy, indices + [gene], true_label=true_label))

        return results

    ####### EMBEDDED FEATURE SELECTION #######

    def getDecisionTreeFeatures(self, data, k=20, returnMultipleSets = False):
        tree = DecisionTreeClassifier(presort=True)
        tree.fit(data.expressions, data.labels)

        return self.getFeatureSets(tree.feature_importances_, k, returnMultipleSets)


    ####### 1 vs Rest #######

    def getOneAgainstRestFeatures(self, sick, healthy, k=3, method="sfs", normalization="relief", fitness="combined"):
        n_labels = np.unique(sick.labels).shape[0]
        feature_sets = Parallel(n_jobs=n_labels)\
                (delayed(self.getOneAgainstRestFeaturesForLabel)(sick, healthy, k, method, normalization, fitness, label) for label in np.unique(sick.labels))
        
        features = {}
        for label, indices in feature_sets:
            features[label] = indices

        return features

    def getOneAgainstRestFeaturesForLabel(self, sick, healthy, k, method, normalization, fitness, label):
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

        return (label, indices)

    ####### UTILS #######

    def getFeatureSets(self, scores, k, returnMultipleSets):
        best_set = scores.argsort()[-k:][::-1]

        if not returnMultipleSets:
            return best_set

        indices = scores.argsort()[::-1]
        roulette_scores = self.get_roulette_scores(scores, k)
        
        sets = [best_set]
        for i in range(1,3):
            sets.append(indices[self.getFeatureSet(roulette_scores, k)])

        return np.asarray(sets)

    def get_roulette_scores(self, scores, k):
        reversed_ranks = len(scores) - rankdata(scores, method='average')
        reversed_rank_scores = 1 / (3 + reversed_ranks) # best is 1/3

        penalized_scores = scores * reversed_rank_scores

        k_highest = max(20, k*4)
        min_thresh = sorted(penalized_scores, reverse=True)[k_highest]
        penalized_scores[penalized_scores < min_thresh] = 0

        normalized_scores = penalized_scores / np.sum(penalized_scores)
        roulette_scores = np.sort(normalized_scores)[::-1]

        """
        print(np.sort(penalized_scores)[-5:][::-1])
        print(np.sort(normalized_scores)[-5:][::-1])
        print(roulette_scores[:5])
        print("==========\n")
        """
        return roulette_scores

    def getFeatureSet(self, scores, k):
        features = []

        while len(features) < k:
            feature = self.getFeature(scores)
            tries = 0
            while feature in features:
                if tries > k:
                    feature += randint(1, k*2)
                else:
                    tries += 1
                    feature = self.getFeature(scores, feature+1)

            tries = 0
            features.append(feature)

        return features

    def getFeature(self, scores, start_i=0):
        cumulated_prob = 0
        i = start_i
        rand = random()
        while cumulated_prob < rand:
            if scores[i] == 0 or i >= len(scores):
                i = 0
            cumulated_prob += scores[i]
            i += 1

        return i-1
