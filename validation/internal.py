#%%

import pickle
import numpy as np
from collections import namedtuple

import matplotlib.pyplot as plt

import falcon

from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import sklearn.cluster as cluster
import sklearn.metrics as metrics

from utils.DataLoader import DataLoader

from scipy import stats

#%%

dataLoader = DataLoader("dataset3")

#%%

class Validator():
    def validate(self, lhs, rhs, genes):
        #ds = data[datasetid]

        #class_results = self.validate_classification(ds, lhs, rhs, genes)

        #clus_results = self.validate_clustering(ds, lhs, rhs, genes)

        #self.validate_distribution(ds, lhs, rhs, genes)
        print(self.validate_internal_classifier(lhs, rhs, genes))
        #return class_results, clus_results

    def validate_internal_classifier(self, lhs, rhs, genes):

        expression, labels, colors = dataLoader.getData(["healthy", "sick"], lhs)
        gene_labels = dataLoader.getGeneLabels()
        data = expression.T[np.in1d(gene_labels, genes)].T

        cl = LogisticRegression(max_iter=25)
        score = cross_val_score(cl, data, labels, cv=10)
        return np.mean(score)


    """def validate_discriminative_classification(self, ds, lhs, rhs, genes):
        complete = Imputer().fit_transform(ds.expressions[np.in1d(ds.labels, lhs + rhs)])

        reduced = (complete.T[np.in1d(ds.genes, genes)]).T
        labels = ds.labels[np.in1d(ds.labels, lhs + rhs)]

        rf = LogisticRegression(max_iter=25)
        scores = cross_val_score(rf, complete, labels, cv=10)

        rf = LogisticRegression(max_iter=25)
        scores2 = cross_val_score(rf, reduced, labels, cv=10)
        return (scores, scores2)

    def validate_clustering(self, ds, lhs, rhs, genes):
        complete = Imputer().fit_transform(ds.expressions[np.in1d(ds.labels, lhs + rhs)])
        reduced = (complete.T[np.in1d(ds.genes, genes)]).T
        labels = ds.labels[np.in1d(ds.labels, lhs + rhs)]

        km = cluster.KMeans(n_clusters=2)
        km.fit(reduced)

        clus0, clus0A = (0,0)
        clus1, clus1A = (0,0)
        for i in range(0, len(km.labels_)):
            if km.labels_[i]:
                clus0 +=1
                if labels[i] in lhs:
                    clus0A += 1
            else:
                clus1 += 1
                if labels[i] in lhs:
                    clus1A += 1
        print(clus0, clus0A, clus1, clus1A)
        binary_labels = [1 if label in lhs else 0 for label in labels]
        return metrics.fowlkes_mallows_score(binary_labels, km.labels_)

    def validate_distribution(self, ds, lhs, rhs, genes):
        complete = Imputer().fit_transform(ds.expressions[np.in1d(ds.labels, lhs + rhs)])

        reduced = (complete.T[np.in1d(ds.genes, genes)]).T
        labels = ds.labels[np.in1d(ds.labels, lhs + rhs)]

        lhsdata = reduced[np.in1d(labels, lhs)]

        candidates = {cancertype: reduced[np.in1d(labels, cancertype)] for cancertype in rhs}
        for c, v in candidates.items():
            print (stats.mstats.normaltest(v))
            print (stats.kstest(lhsdata, "norm", args=(np.mean(lhsdata), np.std(lhsdata))))
            print(stats.anderson(v))
            plt.hist(v)
            plt.savefig("" + c + ".png")
            plt.clf()
        plt.hist(lhsdata)
        plt.savefig("lhs.png")"""

class InternalValidationResource():

    def __init__(self):
        self.validator = Validator()

    def on_get(self, req, resp):
        datasetid = req.get_param('id')
        lhs = req.get_param('lhs')
        rhs = req.get_param('rhs')
        genes = req.get_param('genes')
        s1 = self.validator.validate_internal_classifier(lhs.split(","), rhs.split(","), genes.split(","))
        resp.body = '{"accuracy": ' + str(s1) +'}'

#%

app = falcon.API()

validator = InternalValidationResource()

app.add_route('/validate/internal', validator)

a = Validator()
a.validate(["GBM"], ["LAML"], ['"ENSG00000281910"'])
