import numpy as np
from imblearn.over_sampling import SMOTE

from utils import Expressions

class Sampler:
    def over_sample(self, data, kind="regular", min_samples=20, change_labels=False):
        # kind: 'regular', 'borderline1', 'borderline2', 'svm'

        original_counts = self.get_label_counts(data)
        min_count = min(original_counts.values())

        desired_counts = self.get_label_counts(data, adjust=True, min_samples=min_samples)
        sampler = SMOTE(ratio = desired_counts, k_neighbors=min_count-1, kind=kind)

        X, y = sampler.fit_sample(data.expressions, data.labels)

        y = y if not change_labels else self.change_labels(y, data.labels.shape[0])

        return Expressions(X, y)

    def get_label_counts(self, data, adjust=False, min_samples=20):
        label_dict = {}
        labels = np.unique(data.labels, return_counts = True)
        for index, label in enumerate(labels[0]):
            if adjust:
                label_dict[label] = max(labels[1][index], min_samples)
            else:
                label_dict[label] = labels[1][index]

        return label_dict

    def change_labels(self, labels, original_counts):
        suffix = "-sampled"
        n_chars_label = int(str(labels.dtype).split("U")[-1]) + len(suffix)
        labels = labels.astype("<U"+str(n_chars_label))

        labels[original_counts:] = np.core.defchararray.add(labels[original_counts:], suffix)
        return labels

    def get_sample_methods(self):
        return ['regular', 'borderline1', 'borderline2'] #, 'svm'

    def get_different_samples(self, data, min_samples=20, change_labels=True):
        methods = self.get_sample_methods()
        samples = []
        for method in methods:
            sampled = self.over_sample(data, kind=method, min_samples=min_samples, change_labels=change_labels)
            samples.append(sampled)

        return samples