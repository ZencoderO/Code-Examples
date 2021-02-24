import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import network_analysis
import networkx as nx
import random

def permutateEdges(nodes,edges):
    newGraph = nx.Graph()
    nodes = list(nodes)
    for edge in edges:
        data = edge[2]['data_dict']
        firstNode = random.choice(nodes)
        secondNode = random.choice(nodes)
        while firstNode is secondNode:
            secondNode = random.choice(nodes)
        newGraph.add_edges_from([(firstNode, secondNode, data)])
    return newGraph


def visualize(dictMedianDiff, realDiff):
    '''
    :param dictMedianDiff:
    :return:
    '''
    for key in dictMedianDiff:
        values = np.asarray(dictMedianDiff[key])
        counts = np.unique(values,return_counts=True)
        numer= max(counts[1])
        ax = sns.distplot(values, norm_hist=False, kde=False, hist=True, bins=50)
        plt.ylabel("Frequency")
        plt.plot([realDiff[key], realDiff[key]],[0,10],'r')
        plt.xlabel("Score")
        plt.title(key)
        plt.savefig("Visualizations/" + key + "EdgePermutations.pdf")
        plt.clf()



def main():
    f = open('thank_you_no_binaries.pkl', 'rb')
    at_graph = pickle.load(f)
    edges = at_graph.edges.data()
    nodes = at_graph.nodes
    networkProperties = {}
    networkProperties['BiConnectedComponent'] = []
    networkProperties['ConnectedComponent'] =[]
    actualValues = {}
    actualValues['BiConnectedComponent'] = 0
    actualValues['ConnectedComponent'] = 0
    output = network_analysis.getSizeofConnectedComponents(at_graph)
    actualValues['BiConnectedComponent'] = output['BiConnectedComponent']
    actualValues['ConnectedComponent'] = output['ConnectedComponent']
    for i in range(1000):
        newGraph = permutateEdges(nodes,edges)
        output = network_analysis.getSizeofConnectedComponents(newGraph)
        networkProperties['BiConnectedComponent'].append(output['BiConnectedComponent'])
        networkProperties['ConnectedComponent'].append(output['ConnectedComponent'])
    visualize(networkProperties,actualValues)



if __name__ == '__main__':
    main()