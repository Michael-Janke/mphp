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

        return X, pca, gene_indices

    def getFeatures(self, data, labels, k=20):
        selector = SelectKBest(chi2, k=k)
        selector.fit(data,labels)
        indices = selector.get_support(indices=True)
        X = data[:,indices]

        return X, indices

    def getDecisionTreeFeatures(self, data, labels, k=20):
        tree =  DecisionTreeClassifier()
        tree.fit(data, labels)
        indices = tree.feature_importances_.argsort()[-k:][::-1] #indices of k greatest values 
        return data[:, indices], indices
