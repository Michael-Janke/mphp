
# coding: utf-8

import os
import numpy

print("Started to parse dataset")

PATH = "data/dataset3/"
DATA_PATH = PATH + "TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_HTSeq-Counts.csv"
SUBSET_PATH = PATH + "subsets/"

data_file = open(DATA_PATH, "rb")

# will load the data file and save into files per cancer type
# please set PATH constants

data_file.seek(0)
gen_labels = numpy.genfromtxt(data_file, delimiter=",", max_rows=1, dtype=numpy.unicode)[1:]

feature_count = gen_labels.shape[0]
data_file.seek(0)
row_count = sum(1 for line in data_file)

meta_file = open(DATA_PATH.replace(".csv","_metadata.csv"), "rb")
meta_data = numpy.genfromtxt(meta_file, delimiter=",", dtype=numpy.unicode)[:,1:]

data_file.seek(0)
data = numpy.empty((row_count-1, feature_count), dtype = numpy.float32)
cancer_labels = numpy.transpose([row.replace('"', '') for row in meta_data[1]]) #meta data has same order, so we just set the meta_data column 2 as label
for irow, line in enumerate(data_file):
    if irow == 0:
        continue
    row = line.split(b",")
    if meta_data[0,irow-1] != row[0].decode().replace('\n', ''):
        raise ValueError("bad Metadata")
    data[irow-1, :] = row[1:]
    # show progress
    if round(irow/float(row_count)*100) % 5 == 0 and round((irow+1)/float(row_count)*100) % 5 != 0:
        print(str(irow) + " (" + str(round(irow/float(row_count)*100)) + "%) rows parsed")
print(str(irow) + " (100%) rows parsed")

data_file.close()
meta_file.close()

# ## subsets

cancer_data = {}
for cancer_label in set(cancer_labels):
    cancer_data[cancer_label] = data[numpy.where(cancer_labels == cancer_label)[0][1:]]
cancer_data.pop('NA', None)

if not os.path.exists(SUBSET_PATH):
    os.makedirs(SUBSET_PATH)

numpy.save(SUBSET_PATH + "gen_labels", gen_labels)

for cancer_label, subset in cancer_data.items():
    numpy.save(SUBSET_PATH + cancer_label, subset)
