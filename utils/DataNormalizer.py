import numpy as np
import pandas as pd

import utils

class DataNormalizer:
    def normalizeDataWithMean(self, sick, healthy):
        """
            data1 = sick
            data2 = healthy
            data1 will be a matrix with data which is 'normalized' with data2
            this method subtracts the mean and adds the minimum to return values > 0
            labels1 and labels2 must match their datasets and have same amount of unique labels
        """
        # separate cancer types and combine in list of matrices
        sick_sets = self.separateTypes(sick.expressions, sick.labels)
        healthy_sets = self.separateTypes(healthy.expressions, healthy.labels)

        # normalize by mean and combine into np array
        normalized = []
        for index, data in enumerate(sick_sets):
            norm = data[0] - np.mean(healthy_sets[index][0], axis=0)
            if len(normalized) == 0:
                normalized = norm
            else:
                normalized = np.concatenate((normalized, norm), axis=0)

        normalized += np.absolute(np.min(normalized))
        labels = [label for label in sick.labels if not label.startswith("LAML")]
        return utils.Expressions(normalized, np.array(labels))


    def separateTypes(self, data, labels):
        data_sets = []
        for label in pd.unique(labels):
            if label.startswith("LAML"):
                continue
            data_indices = np.where(labels == label)
            data_sets.append(data[data_indices,:])

        return data_sets
