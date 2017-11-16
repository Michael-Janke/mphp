#%%
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

#%%

class InternalValidator:

    def __init__(self, dataLoader):
        self.dataLoader = dataLoader

    def validate_internal_classifier(self, lhs, rhs, genes):

        expression, labels, colors = self.dataLoader.getData(["healthy", "sick"], lhs)
        gene_labels = self.dataLoader.getGeneLabels()
        data = expression.T[np.in1d(gene_labels, genes)].T

        cl = LogisticRegression(max_iter=25)
        score = cross_val_score(cl, data, labels, cv=10)
        return np.mean(score)

class InternalValidationResource():

    def __init__(self, dataLoader):
        self.validator = InternalValidator(dataLoader)

    def on_get(self, req, resp):
        datasetid = req.get_param('id')
        lhs = req.get_param('lhs')
        rhs = req.get_param('rhs')
        genes = req.get_param('genes')
        s1 = self.validator.validate_internal_classifier(lhs.split(","), rhs.split(","), genes.split(","))
        resp.body = '{"accuracy": ' + str(s1) +'}'
