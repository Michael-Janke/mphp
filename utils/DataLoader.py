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
        for file in files:
            cancer_type = ntpath.basename(file).split(".")[0].split("-")[1]
            cancer_types.append(cancer_type)
            gene_data = np.load(file)
            data[cancer_type] = gene_data

        gene_file = glob("data/"+dataset+"/subsets/gen*")[0]
        gene_labels = np.load(gene_file)

        return data, gene_labels, cancer_types

    def getColor(self, index):
        colors = ["blue","red","green","yellow","orange","black","grey","magenta","cyan"]

        return colors[index%len(colors)]

    def getGeneLabels(self):
        return self.gene_labels

    def getData(self, types):
        combined_data = labels = colors = []

        if len(types) == 1 and types[0].lower() == 'all':
            types = self.cancer_types
        
        for index, cancer_type in enumerate(types):
            if index == 0:
                combined_data = self.data[cancer_type]
                labels = [index] * self.data[cancer_type].shape[0]
                colors = [self.getColor(index)] * self.data[cancer_type].shape[0]
            else:
                combined_data = np.concatenate((combined_data,self.data[cancer_type]),axis=0)
                labels = np.concatenate((labels,[index] * self.data[cancer_type].shape[0]),axis=0)
                colors = np.concatenate((colors,[self.getColor(index)] * self.data[cancer_type].shape[0]),axis=0)

        labels = np.transpose(labels)
        colors = np.transpose(colors)

        return combined_data, labels, colors
        