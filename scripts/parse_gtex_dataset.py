
# coding: utf-8

import os
import re
import numpy as np
from glob import glob

def parse_gtex_dataset(name):

    PATH = "data/" + name + "/"
    [DATA_PATH] = glob(PATH + "GTEx_expre*") 
    [META_DATA_PATH] = glob(PATH + "*GTEx_Meta*") 

    data_file = open(DATA_PATH, "rb")
    # will load the data file and save into files per cancer type
    # please set PATH constants

    data_file.seek(0)
    gene_labels = np.genfromtxt(data_file, delimiter=",", max_rows=1, dtype=np.unicode)[1:]
    regex = re.compile('ENSG\d*')
    trim_quotes = (lambda regex: lambda string: regex.search(string)[0])(regex)
    gene_labels = np.vectorize(trim_quotes)(gene_labels)

    feature_count = gene_labels.shape[0]
    data_file.seek(0)
    row_count = sum(1 for line in data_file)

    meta_file = open(META_DATA_PATH, "rb")
    meta_data = np.genfromtxt(meta_file, delimiter="\t", dtype=np.unicode)

    data_file.seek(0)
    data = np.empty((row_count-1, feature_count), dtype = np.float32)
    cancer_labels = np.empty((row_count-1), dtype = '<U4')

    cancer_labels_map = {
        "Prostate" : "PRAD",
        "Ovary" : "OV",
        "Colon - Sigmoid" : "COAD",
        "Colon - Transverse" : "COAD",
        "Breast - Mammary Tissue" : "BRCA",
        "Stomach" : "STAD",
        "Cervix - Ectocervix" : "CESC",
        "Cervix - Endocervix" : "CESC",
        "Kidney - Cortex" : "KIRC",
        "Bladder" : "BLCA",
        "Thyroid" : "THCA",
        "Esophagus - Gastrointestinal Junction" : "ESCA",
        "Esophagus - Gastroesophageal Junction" : "ESCA",
        "Esophagus - Mucosa" : "ESCA",
        "Esophagus - Muscularis" : "ESCA"
    }

    cancer_mapping = np.vectorize(cancer_labels_map.get)
    meta_data[:,1] = cancer_mapping(meta_data[:,1])
    sample_id_conversion = np.vectorize(lambda x: x.replace('-', '.'))
    meta_data[:,0] = sample_id_conversion(meta_data[:,0])

    sample_types = np.empty(len(meta_data[:,0]), dtype = '<U2')
    sample_types.fill("NT")

    progress = progress_now = 0
    for irow, line in enumerate(data_file):
        if irow == 0:
            continue
        row = line.split(b",")
        sample_id = row[0].decode().replace('\n', '').replace('"', '')
        sample_id_index = np.nonzero(meta_data[:, 0] == sample_id)[0][0]
        cancer_type = meta_data[sample_id_index, 1]
        cancer_labels[irow-1] = cancer_type
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
    SUBSET_PATH = PATH + "subsets"

    if not os.path.exists(SUBSET_PATH):
        os.makedirs(SUBSET_PATH)

    for cancer_label in set(cancer_labels):
        indices = np.where(cancer_labels == cancer_label)[0][:]
        np.save(SUBSET_PATH + '/GTEX-' + cancer_label + '_count_data', data[indices])
        np.save(SUBSET_PATH + '/GTEX-' + cancer_label + "_meta_data", sample_types[indices])

    np.save(SUBSET_PATH + '/GTEX-gene_labels', gene_labels)
