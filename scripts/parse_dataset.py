
# coding: utf-8

import os
import numpy as np
from glob import glob

def parse_dataset(name):
    print("Started to parse dataset")
    print(name)

    PATH = "data/" + name + "/"
    DATA_PATH, META_DATA_PATH = glob(PATH + "TCGA*") #eliminate TCGA?

    data_file = open(DATA_PATH, "rb")

    # will load the data file and save into files per cancer type
    # please set PATH constants

    data_file.seek(0)
    gene_labels = np.genfromtxt(data_file, delimiter=",", max_rows=1, dtype=np.unicode)[1:]
    trim_quotes = np.vectorize(lambda x: x[1:-1])
    gene_labels = trim_quotes(gene_labels)

    feature_count = gene_labels.shape[0]
    data_file.seek(0)
    row_count = sum(1 for line in data_file)

    meta_file = open(META_DATA_PATH, "rb")
    meta_data = np.genfromtxt(meta_file, delimiter=",", dtype=np.unicode)[:,1:]

    data_file.seek(0)
    data = np.empty((row_count-1, feature_count), dtype = np.float32)
    cancer_labels = np.transpose([row.replace('"', '') for row in meta_data[1]]) #meta data has same order, so we just set the meta_data column 2 as label
    sample_types = np.transpose([row.replace('"', '') for row in meta_data[2]]) #meta data has same order, so we just set the meta_data column 2 as label

    previous_cancer_label = cancer_labels[0]
    for index, cancer_label in enumerate(cancer_labels):
        if cancer_label == "NA":
            cancer_labels[index] = previous_cancer_label
        previous_cancer_label = cancer_label

    progress = progress_now = 0
    for irow, line in enumerate(data_file):
        if irow == 0:
            continue
        row = line.split(b",")
        if meta_data[0, irow-1] != row[0].decode().replace('\n', ''):
            raise ValueError("bad Metadata")
        data[irow-1, :] = row[1:]
        # show progress
        progress_now = round(irow/float(row_count)*100)
        if progress != progress_now:
            print("%s%% parsed (%d)" % (progress_now, irow), flush=True, end="\r")
        progress = progress_now
    print("---parsing finished---", flush=True)

    data_file.close()
    meta_file.close()

    # ## subsets
    SUBSET_PATH = PATH + "subsets/"

    if not os.path.exists(SUBSET_PATH):
        os.makedirs(SUBSET_PATH)

    for cancer_label in set(cancer_labels):
        indices = np.where(cancer_labels == cancer_label)[0][1:]
        np.save(SUBSET_PATH + cancer_label, data[indices])
        np.save(SUBSET_PATH + cancer_label + "_meta_data", sample_types[indices])

    np.save(SUBSET_PATH + "gene_labels", gene_labels)
