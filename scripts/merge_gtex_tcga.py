
# coding: utf-8

import os
import re
import numpy as np
from glob import glob

def merge_gtex_tcga(name):

    PATH = "data/" + name + "/subsets/"
    
    GTEX_gene_labels = np.load(PATH + 'GTEX-gene_labels.npy')
    TCGA_gene_labels = np.load(PATH + 'TCGA-gene_labels.npy')

    gene_labels_new = np.intersect1d(GTEX_gene_labels, TCGA_gene_labels, assume_unique=True)

    np.save(PATH + 'MERGED-gene_labels.npy', gene_labels_new)

    gene_labels_new_list = gene_labels_new.tolist()
    def new_index_mapper_func(x):
        try:
            return gene_labels_new_list.index(x)
        except: 
            return -1

    new_index_mapper = np.vectorize(new_index_mapper_func)

    GTEX_gene_index = new_index_mapper(GTEX_gene_labels)
    GTEX_gene_index = np.delete(GTEX_gene_index, np.nonzero(GTEX_gene_index == -1))
    TCGA_gene_index = new_index_mapper(GTEX_gene_labels)
    TCGA_gene_index = np.delete(TCGA_gene_index, np.nonzero(TCGA_gene_index == -1))


    TCGA_META_FILES = glob("data/"+name+"/subsets/TCGA*_meta_data.npy")
    GTEX_META_FILES = glob("data/"+name+"/subsets/GTEX*_meta_data.npy")
    TCGA_FILES = glob("data/"+name+"/subsets/TCGA*_count_data.npy")
    GTEX_FILES = glob("data/"+name+"/subsets/GTEX*_count_data.npy")
    cancer_types_tcga = [re.search(".*TCGA-(.*)_count_data.npy", x).group(1) for x in TCGA_FILES]
    cancer_types_gtex = [re.search(".*GTEX-(.*)_count_data.npy", x).group(1) for x in GTEX_FILES]

    if len(set(cancer_types_tcga) - set(cancer_types_gtex)) > 0: 
        raise "cancer_types cant be merged"

    for i, tcga_file in enumerate(TCGA_FILES):
        cancer_type = cancer_types_tcga[i]
        count_data_tcga = np.load(tcga_file)
        count_data_gtex = np.load(GTEX_FILES[i])
        new_count_data_tcga = count_data_tcga[:, TCGA_gene_index]
        new_count_data_gtex = count_data_gtex[:, GTEX_gene_index]
        new_count_data = np.concatenate([new_count_data_tcga, new_count_data_gtex])
        np.save(PATH+'MERGED-{}_count_data.npy'.format(cancer_type), new_count_data)
        
        new_meta_data = np.concatenate([np.load(TCGA_META_FILES[i]),np.load(GTEX_META_FILES[i])])
        np.save(PATH+'MERGED-{}_meta_data.npy'.format(cancer_type), new_meta_data)
        
        print("merged {}".format(cancer_type), flush=True)

    for i, tcga_file in enumerate(TCGA_FILES):
        os.remove(GTEX_FILES[i])
        os.remove(TCGA_FILES[i])
        os.remove(GTEX_META_FILES[i])
        os.remove(TCGA_META_FILES[i])

    os.remove(PATH + 'GTEX-gene_labels.npy')
    os.remove(PATH + 'TCGA-gene_labels.npy')