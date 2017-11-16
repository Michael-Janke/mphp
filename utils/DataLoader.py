import numpy as np
import ntpath
from glob import glob

class DataLoader:
    def __init__(self, dataset):
        self.dataset = dataset
        self.data, self.gene_labels, self.cancer_types = self.readData(dataset)

    def readData(self, dataset):
        data = {}
        cancer_types = []

        files = glob("data/"+dataset+"/subsets/TCGA*")
        meta_data_files = glob("data/"+dataset+"/subsets/TCGA*meta_data.npy")
        files = list(set(files)-set(meta_data_files))
        print(files)
        for file in files:
            cancer_type = ntpath.basename(file).split(".")[0].split("-")[1]
            cancer_types.append(cancer_type)
            gene_data = np.load(file)
            meta_data = np.load(file.replace(".npy","_meta_data.npy"))
            sample_types = np.unique(meta_data).astype('str')
            data[cancer_type] = {}
            for sample_type in sample_types:
                indices = np.where(sample_type == meta_data)
                data[cancer_type][sample_type] = gene_data[indices]

        gene_file = glob("data/"+dataset+"/subsets/gen*")[0]
        gene_labels = np.load(gene_file)
        return data, gene_labels, cancer_types

    def getColor(self, index):
        colors = ["blue","red","green","yellow","orange","black","grey","magenta","cyan"]

        return colors[index%len(colors)]

    def getGeneLabels(self):
        return self.gene_labels

    def getData(self, sample_types, cancer_types):
        combined_data = labels = colors = []

        if len(cancer_types) == 1 and cancer_types[0].lower() == 'all':
            cancer_types = self.cancer_types

        # TODO: parse sample_types for healthy and sick
        # TODO: what do we do if the requested sample type is not in the cancer_type?

        for cancer_index, cancer_type in enumerate(cancer_types):
            for sample_index, sample_type in enumerate(sample_types):
                index = cancer_index * len(sample_types) + sample_index
                label = cancer_type + "-" + sample_type
                if len(combined_data) == 0:
                    combined_data = self.data[cancer_type][sample_type]
                    labels = [label] * self.data[cancer_type][sample_type].shape[0]
                    colors = [self.getColor(index)] * self.data[cancer_type][sample_type].shape[0]
                else:
                    combined_data = np.concatenate((combined_data,self.data[cancer_type][sample_type]),axis=0)
                    labels = np.concatenate((labels,[label] * self.data[cancer_type][sample_type].shape[0]),axis=0)
                    colors = np.concatenate((colors,[self.getColor(index)] * self.data[cancer_type][sample_type].shape[0]),axis=0)

        labels = np.transpose(labels)
        colors = np.transpose(colors)

        return combined_data, labels, colors
