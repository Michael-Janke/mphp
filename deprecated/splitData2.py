DATA_PATH = "C:/Users/Micha/mphp/data/TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_TP_TB_HTSeq-Counts.csv"
DATA2_PATH = "C:/Users/Micha/mphp/data/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts.csv"
SUBSET_PATH = "C:/Users/Micha/mphp/data/subsets/"

import numpy
data_file = open(DATA_PATH, "rb")
data_file2 = open(DATA_PATH2, "rb")

data_file.seek(0)
gen_labels1 = numpy.genfromtxt(data_file, delimiter=",", max_rows=1, dtype=numpy.unicode)[1:]
gen_labels

feature_count = gen_labels.shape[0]
feature_count
data_file.seek(0)
row_count = sum(1 for line in data_file)
row_count

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
    if irow % 100 == 0:
        print(str(irow) + " rows parsed")

data_file.close()
meta_file.close()

cancer_data = {}
for cancer_label in set(cancer_labels):
    cancer_data[cancer_label] = data[numpy.where(cancer_labels == cancer_label)[0][1:]]
cancer_data.pop('NA', None)

import os
if not os.path.exists(SUBSET_PATH):
    os.makedirs(SUBSET_PATH)

for cancer_label, subset in cancer_data.items():
    file = open(SUBSET_PATH + cancer_label + '.npz','wb')
    numpy.save(file, subset)
    file.close()
