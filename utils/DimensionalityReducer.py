import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_classif
from sklearn.tree import DecisionTreeClassifier

import utils.EA.config as c
from utils.EA.fitness import fitness, combined_fitness, classification_fitness, clustering_fitness
from utils.EA.crossover import *
from utils.EA.mutation import *
from utils.EA.population import phenotype
from utils.EA.algorithm import ea_for_plot

from utils import Expressions, binarize_labels

class DimensionalityReducer:
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

        return pca, X, gene_indices


    ####### FEATURE SELECTION BY STATISTICS #######

    def getFeatures(self,  data, k=20, m="chi2"):
        selector = SelectKBest(self.method_table[m], k=k)
        selector.fit(data.expressions, data.labels)
        # sort and select features
        # [::-1] reverses an 1d array in numpy
        indices = selector.scores_.argsort()[-k:][::-1]

        return indices, data.expressions[:, indices]

    def getNormalizedFeatures(self, sick, healthy, normalization, k=20, n=5000, m="chi2"):
        options = {
            'substract': self.getNormalizedFeaturesS,
            'exclude': self.getNormalizedFeaturesE,
        }
        return options[normalization](sick, healthy, k, n, m)

    def getNormalizedFeaturesS(self, sick, healthy, k, n, m):
        selector = SelectKBest(self.method_table[m], k="all")
        selector.fit(healthy.expressions, healthy.labels)
        healthy_scores = selector.scores_
        healthy_scores /= max(healthy_scores)

        selector.fit(sick.expressions, sick.labels)
        sick_scores = selector.scores_
        sick_scores /= max(sick_scores)

        # subtract healthy scores from sick scores (this is the normalization here)
        indices = (sick_scores - healthy_scores).argsort()[-k:][::-1]

        return indices, sick.expressions[:, indices], healthy.expressions[:, indices]

    def getNormalizedFeaturesE(self, sick, healthy, k, n, m):
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
        # sort selected features by score
        indices = features[selector.scores_[features].argsort()[-k:][::-1]]

        return indices, sick.expressions[:, indices], healthy.expressions[:, indices]


    ####### MULTI-VARIATE FEATURE SELECTION #######

    def getEAFeatures(self, sick, healthy, normalization="substract", true_label=""):
        # preselect features to reduce runtime
        selected_genes, sick_X, healthy_X = self.getNormalizedFeatures(sick,healthy,normalization, c.chromo_size, c.chromo_size)
        crossover = one_point_crossover
        mutation = binary_mutation
        fitness_function = fitness(Expressions(sick_X, sick.labels), Expressions(healthy_X, healthy.labels), true_label=true_label)
        best, stat, stat_aver = ea_for_plot(c, c.chromo_size, fitness_function, crossover, mutation)
        indices = selected_genes[phenotype(best)]
        return indices, sick.expressions[:, indices], healthy.expressions[:, indices]

    def getFeaturesBySFS(self, sick, healthy, k=3, n=5000, m=100, normalization="exclude", true_label=""):
        # preselect 100 genes in sick data which do not separate healthy data well
        selected_genes, _, _ = self.getNormalizedFeatures(sick,healthy,normalization, m, n)

        # first gene has highest score and will be selected first
        indices = [selected_genes[0]]
        # iteratively join the best next feature based on a fitness function until k features are found
        for idx in range(1,k):
            best_fitness = -10
            best_gene = 0
            for i in range(1,m):
                gene = selected_genes[i]
                fitness_score = combined_fitness(Expressions(sick.expressions[:,indices + [gene]], sick.labels),\
                                        Expressions(healthy.expressions[:,indices + [gene]], healthy.labels), true_label=true_label)
                if fitness_score > best_fitness:
                    best_fitness = fitness_score
                    best_gene = gene
            indices.append(best_gene)
            print("added new feature")

        return indices, sick.expressions[:, indices], healthy.expressions[:, indices]


    ####### EMBEDDED FEATURE SELECTION #######

    def getDecisionTreeFeatures(self, data, k=20):
        tree = DecisionTreeClassifier()
        tree.fit(data.expressions, data.labels)
        indices = tree.feature_importances_.argsort(
        )[-k:][::-1]  # indices of k greatest values
        return indices, data.expressions[:, indices]


    ####### 1 vs Rest #######

    def getOneAgainstRestFeatures(self, sick, healhty, k=3, method="sfs", normalization="exclude"):
        features = {}
        for label in np.unique(sick.labels):
            label = label.split("-")[0]
            s_labels = binarize_labels(sick.labels, label)
            sick_binary = Expressions(sick.expressions, s_labels)

            if healhty == "":
                indices, _ = self.getFeatures(sick_binary, k)

            else:
                h_labels = binarize_labels(healhty.labels, label)
                healhty_binary = Expressions(healhty.expressions, h_labels)

                if method == "ea":
                    indices, _, _ = self.getEAFeatures(sick, healhty, normalization, true_label=label)
                elif method == "norm":
                    indices, _, _ = self.getNormalizedFeatures(sick_binary, healhty_binary, normalization, k)
                else:
                    indices, _, _ = self.getFeaturesBySFS(sick, healhty, k, normalization=normalization, true_label=label)

            features[label] = indices

        return features
