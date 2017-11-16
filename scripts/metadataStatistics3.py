import numpy as np
import json
import os
import matplotlib.pyplot as plt


PATH = "data/dataset3/"
METADATA_PATH = PATH + "TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_HTSeq-Counts_metadata.csv"
STATISTICS_PATH = PATH + "statistics/"

metadata_file = open(METADATA_PATH, "rb")
metadata = np.genfromtxt(metadata_file, delimiter=",", dtype=np.unicode)[1:,1:]

sample_types = np.unique(metadata[1:,:])
sample_types = [x.strip('"') for x in sample_types]

counts = {}
last_cancer_type = ""
for column in metadata.T:
    cancer_type = column[0].strip('"').split('-', 1)[-1]
    sample_type = column[1].strip('"')

    if cancer_type == 'NA':
        cancer_type = last_cancer_type

    if cancer_type not in counts:
        counts[cancer_type] = {x : 0 for x in sample_types}
    else:
        counts[cancer_type][sample_type] += 1
    
    last_cancer_type = cancer_type


# write statistics files
if not os.path.exists(STATISTICS_PATH):
    os.makedirs(STATISTICS_PATH)

np.save(STATISTICS_PATH + "sample_types", sample_types)
np.save(STATISTICS_PATH + "counts", counts)

with open(STATISTICS_PATH + 'counts_human_readable.txt', 'w') as outfile:
    json.dump(counts, outfile, indent=4)


# create plot for sample types by cancer type
fig, ax = plt.subplots()
index = np.arange(len(counts))
bar_width = 0.1
colors = ["blue","red","green","yellow","orange","black","grey","magenta","cyan"]
colors = colors[:len(sample_types)]
for i in range(0, len(sample_types)):
    values = [x[sample_types[i]] for x in counts.values()]
    plt.bar(index + (i * bar_width), values, bar_width, color=colors[i], label=sample_types[i])

plt.xlabel('Cancer Type')
plt.ylabel('Counts')
plt.title('Sample types by cancer type')
plt.xticks(index + bar_width / 2, counts.keys())
plt.legend()
plt.tight_layout()
plt.savefig(STATISTICS_PATH + 'plot_sample_types_by_cancer_type.png')


# create plot for sick and healthy by cancer type
fig, ax = plt.subplots()
index = np.arange(len(counts))
bar_width = 0.2

sick = []
healthy = []
for sample_type in sample_types:
    if sample_type.startswith("T"):
        sick.append([x[sample_type] for x in counts.values()])
    elif sample_type.startswith("N"):
        healthy.append([x[sample_type] for x in counts.values()])
    else:
        print("sample type " + sample_type + " is not included")

sick = np.asarray(sick)
sick = sick.sum(axis=0)
healthy = np.asarray(healthy)
healthy = healthy.sum(axis=0)

plt.bar(index, sick, bar_width, color='r', label='sick')
plt.bar(index + bar_width, healthy, bar_width, color='b', label='healthy')

plt.xlabel('Cancer Type')
plt.ylabel('Counts')
plt.title('Sick and healthy by cancer type')
plt.xticks(index + bar_width / 2, counts.keys())
plt.legend()
plt.tight_layout()
plt.savefig(STATISTICS_PATH + 'plot_sick_and_healthy_by_cancer_type.png')