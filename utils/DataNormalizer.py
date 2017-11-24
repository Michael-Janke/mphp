import numpy as np
import pandas as pd

class DataNormalizer:
    def normalizeDataWithMean(self, data1, data2, labels1, labels2):
        """
            data1 = sick
            data2 = healthy
            data1 will be a matrix with data which is 'normalized' with data2
            this method subtracts the mean and adds the minimum to return values > 0
            labels1 and labels2 must match their datasets and have same amount of unique labels
        """
        # separate cancer types and combine in list of matrices
        data1_sets = self.separateTypes(data1, labels1)
        data2_sets = self.separateTypes(data2, labels2)

        # normalize by mean and combine into np array
        normalized = []
        for index, data in enumerate(data1_sets):
            norm = data[0] - np.mean(data2_sets[index][0], axis=0)
            if len(normalized) == 0:
                normalized = norm
            else:
                normalized = np.concatenate((normalized, norm), axis=0)

        normalized += np.absolute(np.min(normalized))
        labels = [label for label in labels1 if not label.startswith("LAML")]
        return normalized, np.array(labels)


    def separateTypes(self, data, labels):
        data_sets = []
        for label in pd.unique(labels):
            if label.startswith("LAML"):
                continue
            data_indices = np.where(labels == label)
            data_sets.append(data[data_indices,:])
        
        return data_sets