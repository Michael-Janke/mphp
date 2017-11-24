import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def getColor(index):
        colors = ["blue","red","green","yellow","orange","black","grey","purple"]

        return colors[index%len(colors)]

def plotScatter(data, colors, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, label in enumerate(np.unique(labels)):
        indices = np.where(label == labels)
        x = data[indices,0]
        y = data[indices,1]
        z = data[indices,2]
        ax.scatter(x,y,z, c=getColor(i), label=label)

    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')

    plt.legend()
    plt.tight_layout()
    plt.show()