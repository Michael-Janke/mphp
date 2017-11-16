import numpy as np
import ntpath
from glob import glob

class DataLoader:
    def __init__(self, dataset):
        self.dataset = dataset
        self.data, self.gene_labels, self.cancer_types, self.sample_types = self.readData(dataset)

    def readData(self, dataset):
        data = {}
        cancer_types = []

        all_sample_types = np.load("data/"+dataset+"/statistics/sample_types.npy").astype("str")
        files = glob("data/"+dataset+"/subsets/TCGA*")
        meta_data_files = glob("data/"+dataset+"/subsets/TCGA*meta_data.npy")
        files = list(set(files)-set(meta_data_files))
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
        return data, gene_labels, cancer_types, all_sample_types

    def getColor(self, index):
        colors = ["blue","red","green","yellow","orange","black","grey"]

        return colors[index%len(colors)]

    def getGeneLabels(self):
        return self.gene_labels

    def getData(self, sample_types, cancer_types):
        combined_data = labels = colors = []

        if len(cancer_types) == 1 and cancer_types[0].lower() == 'all':
            cancer_types = self.cancer_types

        labels_vector = []
        new_sample_types = []
        for sample_index, sample_type in enumerate(sample_types):
            if sample_type == "healthy":
                new_sample_types.extend([type for type in self.sample_types if type.startswith("N")])
                labels_vector.extend(["healthy" for type in self.sample_types if type.startswith("T")])

            elif sample_type == "sick":
                new_sample_types.extend([type for type in self.sample_types if type.startswith("T")])
                labels_vector.extend(["sick" for type in self.sample_types if type.startswith("T")])

            else:
                labels_vector.append(sample_type)
                new_sample_types.append(sample_type)


        index = 0
        for cancer_index, cancer_type in enumerate(cancer_types):
            for sample_index, sample_type in enumerate(new_sample_types):

                label = cancer_type + "-" + labels_vector[sample_index]
                if sample_type in self.data[cancer_type]:
                    if len(combined_data) == 0:
                        combined_data = self.data[cancer_type][sample_type]
                        labels = [label] * self.data[cancer_type][sample_type].shape[0]
                        index += 1
                    else:
                        combined_data = np.concatenate((combined_data,self.data[cancer_type][sample_type]),axis=0)
                        labels = np.concatenate((labels,[label] * self.data[cancer_type][sample_type].shape[0]),axis=0)
                        index += 1

        labels = np.transpose(labels)
        _, label_counts = np.unique(labels, return_counts = True)
        colors = []
        for index, count in enumerate(label_counts):
            if index == 0:
                colors = [self.getColor(index)] * count
            else:
                colors.extend([self.getColor(index)] * count)

        return combined_data, labels, colors
