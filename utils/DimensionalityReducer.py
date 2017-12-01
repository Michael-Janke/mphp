import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier

class DimensionalityReducer:
    ####### PCA #######
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



    ####### FEATURE SELECTION BY STATISTICS #######
    def getFeatures(self, data, k=20):
        selector = SelectKBest(chi2, k=k)
        selector.fit(data.expressions, data.labels)
        # sort and select features
        # [::-1] reverses an 1d array in numpy
        indices = selector.scores_.argsort()[-k:][::-1]

        return indices, data.expressions[:,indices]

    def getNormalizedFeatures(self, sick, healthy, method, k=20, n=1000):
        options = {
            'subtract': self.getNormalizedFeaturesS,
            'exclude' : self.getNormalizedFeaturesE,
        }
        return options[method](sick, healthy, k, n)

    def getNormalizedFeaturesS(self, sick, healthy, k, n):
        selector = SelectKBest(chi2, k="all")
        selector.fit(healthy.expressions, healthy.labels)
        healthy_scores = selector.scores_
        healthy_scores /= max(healthy_scores)

        selector.fit(sick.expressions, sick.labels)
        sick_scores = selector.scores_
        sick_scores /= max(sick_scores)

        # subtract healthy scores from sick scores (this is the normalization here)
        indices = (sick_scores - healthy_scores).argsort()[-k:][::-1]

        return indices, sick.expressions[:,indices], healthy.expressions[:,indices]

    def getNormalizedFeaturesE(self, sick, healthy, k, n):
        selector = SelectKBest(chi2, k=n)
        selector.fit(healthy.expressions, healthy.labels)
        h_indices = selector.get_support(indices=True)

        selector = SelectKBest(chi2, k=n+k)
        selector.fit(sick.expressions, sick.labels)
        s_indices = selector.get_support(indices=True)

        # get features in sick data which do not discriminate healty data
        features = list(set(s_indices)-set(h_indices))
        print("excluded "+str(n-len(features))+" features")
        features = np.asarray(features, dtype=np.uint32)
        # sort selected features by score
        indices = features[ selector.scores_[features].argsort()[-k:][::-1] ]

        return indices, sick.expressions[:,indices], healthy.expressions[:,indices]



    ####### EMBEDDED FEATURE SELECTION #######
    def getDecisionTreeFeatures(self, data, k=20):
        tree =  DecisionTreeClassifier()
        tree.fit(data.expressions, data.labels)
        indices = tree.feature_importances_.argsort()[-k:][::-1] #indices of k greatest values
        return indices, data[:,indices]
