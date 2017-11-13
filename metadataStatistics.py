#%%
import numpy
import json
import matplotlib.pyplot as plt

print("imports done")

#%%
METADATA_PATH = "data/dataset3/TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_HTSeq-Counts_metadata.csv"
metadata_file = open(METADATA_PATH, "rb")
metadata = numpy.genfromtxt(metadata_file, delimiter=",", dtype=numpy.unicode)[1:,1:]

counts = {}
for column in metadata.T:
    cancer_type = column[0].strip('"').split('-', 1)[-1]
    sample_type = column[1].strip('"')
    if cancer_type not in counts:
        counts[cancer_type] = {'TP' : 0, 'TM' : 0, 'TR' : 0, 'NT' : 0, 'NB' : 0}
    if sample_type not in counts[cancer_type]:
        print("invalid value for " + cancer_type + ": " + sample_type)
    else:
        counts[cancer_type][sample_type] += 1

print(json.dumps(counts, indent=4))


#%%
fig, ax = plt.subplots()
index = np.arange(len(counts))
bar_width = 0.1
sample_types = ['TP', 'TM', 'TR', 'NT', 'NB']
colors = ['r', 'y', 'm', 'b', 'c']
for i in range(0, 5):
    values = [x[sample_types[i]] for x in counts.values()]
    plt.bar(index + (i * bar_width), values, bar_width, color=colors[i], label=sample_types[i])

plt.xlabel('Cancer Type')
plt.ylabel('Counts')
plt.title('Sample types by cancer type')
plt.xticks(index + bar_width / 2, counts.keys())
plt.legend()
plt.tight_layout()
plt.show()


#%%
fig, ax = plt.subplots()
index = np.arange(len(counts))
bar_width = 0.2

values = np.array([[x['TP'] for x in counts.values()], [x['TM'] for x in counts.values()], [x['TR'] for x in counts.values()]])
values = values.sum(axis=0)
plt.bar(index, values, bar_width, color='r', label='sick')

values = np.array([[x['NT'] for x in counts.values()], [x['NB'] for x in counts.values()]])
values = values.sum(axis=0)
plt.bar(index + bar_width, values, bar_width, color='b', label='healthy')

plt.xlabel('Cancer Type')
plt.ylabel('Counts')
plt.title('Sample types by cancer type')
plt.xticks(index + bar_width / 2, counts.keys())
plt.legend()
plt.tight_layout()
plt.show()