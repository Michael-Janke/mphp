import numpy as np
import ntpath
from glob import glob
import re
import utils


class DataLoader:
    def __init__(self, dataset):
        self.dataset = dataset
        self.data, self.cancer_types, self.sample_types = self.readData(
            dataset)
        self.gene_labels = self.readGeneLabels(dataset)
        self.gene_names_map = self.readGeneNamesMap()
        self.gene_names = self.mapGeneLabelsToGeneNames(self.gene_labels)
        self.statistics = self.computeStatistics()

    def readData(self, dataset):
        data = {}
        cancer_types = []

        files = glob("data/"+dataset+"/subsets/*_count_data.npy")
        meta_data_files = glob("data/"+dataset+"/subsets/*_meta_data.npy")
        for file in files:
            cancer_type = re.search(".*-(.*)_count_data.npy", file).group(1)
            cancer_types.append(cancer_type)
            gene_data = np.load(file)
            meta_data = np.load(file.replace("_count_data.npy","_meta_data.npy"))
            sample_types = np.unique(meta_data).astype('str')
            data[cancer_type] = {}
            for sample_type in sample_types:
                indices = np.where(sample_type == meta_data)
                data[cancer_type][sample_type] = gene_data[indices]

        return data, cancer_types, sample_types

    def readGeneLabels(self, dataset):
        gene_file = glob("data/"+dataset+"/subsets/*-gene_labels.npy")[0]
        return np.load(gene_file)

    def readGeneNamesMap(self):
        return np.load('data/gene_names/gene_names.npy').item()

    def mapGeneLabelsToGeneNames(self, labels):
        def mapfunc(gene): return self.gene_names_map[int(gene[4:])]
        return np.vectorize(mapfunc)(labels)

    def getGeneNamesTable(self):
        return self.gene_names

    def getGeneNames(self):
        return self.gene_names

    def getGeneLabels(self):
        return self.gene_labels

    def getStatistics(self):
        return self.statistics

    def getData(self, sample_types, cancer_types, excluded_cancer_types=[]):
        combined_data = labels = []

        if len(cancer_types) == 1 and cancer_types[0].lower() == 'all':
            cancer_types = self.cancer_types

        cancer_types = np.asarray(
            list(set(cancer_types) - set(excluded_cancer_types)))

        labels_vector = []
        new_sample_types = []
        for sample_index, sample_type in enumerate(sample_types):
            if sample_type == "healthy":
                new_sample_types.extend(
                    [type for type in self.sample_types if type.startswith("N")])
                labels_vector.extend(
                    ["healthy" for type in self.sample_types if type.startswith("N")])

            elif sample_type == "sick":
                new_sample_types.extend(
                    [type for type in self.sample_types if type.startswith("T")])
                labels_vector.extend(
                    ["sick" for type in self.sample_types if type.startswith("T")])

            else:
                labels_vector.append(sample_type)
                new_sample_types.append(sample_type)

        for cancer_type in cancer_types:
            for sample_index, sample_type in enumerate(new_sample_types):
                label = cancer_type + "-" + labels_vector[sample_index]

                if sample_type in self.data[cancer_type]:
                    if len(combined_data) == 0:
                        combined_data = self.data[cancer_type][sample_type]
                        labels = [label] * \
                            self.data[cancer_type][sample_type].shape[0]
                    else:
                        combined_data = np.concatenate(
                            (combined_data, self.data[cancer_type][sample_type]), axis=0)
                        labels = np.concatenate(
                            (labels, [label] * self.data[cancer_type][sample_type].shape[0]), axis=0)

        labels = np.transpose(labels)
        _, label_counts = np.unique(labels, return_counts=True)

        return utils.Expressions(combined_data, labels)

    def replaceLabels(self, data):
        data.labels = np.asarray(
            [re.sub(r"-N\w*", "-healthy", x) for x in data.labels])
        data.labels = np.asarray(
            [re.sub(r"-T\w*", "-sick", x) for x in data.labels])
        return data

    def computeStatistics(self): 
        stat = {}
        for ct in self.cancer_types:
            stat[ct] = {}
            for st in self.sample_types:
                if st in self.data[ct]:
                    stat[ct][st] = self.data[ct][st].shape[0]
                else:
                    stat[ct][st] = 0
        return stat

    def getStatistics(self): 
        return self.statistics