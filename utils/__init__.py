import collections
import numpy as np
import warnings
from functools import wraps

class Expressions:
    def __init__(self, expressions, labels):
        self._expressions = expressions
        self._labels = labels
    @property
    def expressions(self):
        return self._expressions
    @property
    def labels(self):
        return self._labels

    def select_genes(self, genes):
        expressions = self.expressions[:,genes]
        return Expressions(expressions, self.labels)

def binarize_labels(labels, selected_label):
    new_labels = np.zeros(labels.shape)
    indices = np.flatnonzero(np.core.defchararray.find(labels,selected_label)!=-1)
    new_labels[indices] = 1

    return new_labels

def ignore_warnings(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("ignore")
            response = f(*args, **kwargs)
        return response
    return inner
