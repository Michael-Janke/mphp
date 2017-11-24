import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier

class DimensionalityReducer:
    def getPCA(self, data ,n_components, n_features_per_component=10):
        pca = PCA(n_components=n_components, svd_solver='full')
        pca.fit(data)
        X = pca.transform(data)

        gene_indices = []
        for i in range(n_components):
            indices = np.argsort(np.absolute(pca.components_[i]))[-n_features_per_component:]
            if len(gene_indices) == 0:
                gene_indices = indices
            else:
                gene_indices = np.concatenate((gene_indices,indices))

        gene_indices = np.unique(gene_indices)

        return pca, X, gene_indices

    def getFeatures(self, data, labels, k=20):
        selector = SelectKBest(chi2, k=k)
        selector.fit(data,labels)
        indices = selector.get_support(indices=True)

        return indices, data[:,indices]

    def getNormalizedFeatures(self, healthy_data, sick_data, healthy_labels, sick_labels, k=20):
        number_of_genes = healthy_data.shape[1]
        selector = SelectKBest(chi2, k=number_of_genes)
        selector.fit(healthy_data, healthy_labels)
        healthy_scores = selector.scores_

        selector = SelectKBest(chi2, k=number_of_genes)
        selector.fit(sick_data, sick_labels)
        sick_scores = selector.scores_

        indices = (sick_scores - healthy_scores).argsort()[-k:][::-1]

        return indices, healthy_data[:,indices], sick_data[:,indices]

    def getDecisionTreeFeatures(self, data, labels, k=20):
        tree =  DecisionTreeClassifier()
        tree.fit(data, labels)
        indices = tree.feature_importances_.argsort()[-k:][::-1] #indices of k greatest values
        return indices, data[:,indices]
