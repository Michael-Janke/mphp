import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def getColor(index):
        colors = "bgrcmyk"
        return colors[index%len(colors)]

def plotScatter(data, genes, gene_labels = ["PC1","PC2","PC3"]):
    if not gene_labels[0] == "PC1":
        gene_labels = gene_labels[genes]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, label in enumerate(np.unique(data.labels)):
        indices = np.where(label == data.labels)
        x = data.expressions[indices,genes[0]]
        y = data.expressions[indices,genes[1]]
        z = data.expressions[indices,genes[2]]
        ax.scatter(x,y,z, c=getColor(i), label=label)

    ax.set_xlabel(gene_labels[0])
    ax.set_ylabel(gene_labels[1])
    ax.set_zlabel(gene_labels[2])

    plt.legend()
    plt.tight_layout()
    plt.show()