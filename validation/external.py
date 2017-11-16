import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


class ExternalValidator:

    def __init__(self, dataLoader):
        self.dataLoader = dataLoader

    def validate_external_classifier(self, lhs, rhs, genes):
        gene_labels = self.dataLoader.getGeneLabels()

        sick_expressions = self.dataLoader.getData(["sick"], lhs)[0]
        healthy_expressions = self.dataLoader.getData(["healthy"], lhs)[0]
        other_expressions = self.dataLoader.getData(["sick", "healthy"], rhs)[0]

        labels = np.array([0] * sick_expressions.shape[0] + [1] * (healthy_expressions.shape[0] + other_expressions.shape[0]))
        expressions = np.concatenate((sick_expressions, healthy_expressions, other_expressions))

        reduced = expressions.T[np.in1d(gene_labels, genes)].T

        cl = LogisticRegression(max_iter=25)

        score_complete = cross_val_score(cl, expressions, labels, cv=10)
        score_reduced = cross_val_score(cl, reduced, labels, cv=10)

        print(score_complete, score_reduced)

        return (np.mean(score_complete), np.mean(score_reduced))

class ExternalValidationResource():

    def __init__(self, dataLoader):
        self.validator = ExternalValidator(dataLoader)

    def on_get(self, req, resp):
        datasetid = req.get_param('id')
        lhs = req.get_param('lhs')
        rhs = req.get_param('rhs')
        genes = req.get_param('genes')
        sc, sr = self.validator.validate_external_classifier(lhs.split(","), rhs.split(","), genes.split(","))
        resp.body = '{"complete": ' + str(sc) +', "reduced": ' + str(sr) + '}'
