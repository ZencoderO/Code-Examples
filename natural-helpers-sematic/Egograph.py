from __future__ import division
import networkx as nx
import pickle
import sys

graphname = nx.Graph ()

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main():
	f = open(sys.argv[1])
	graphname = pickle.load(f)
	f.close()

	corenumber = {}
	connectedcomponents = {}
	triangles = {}
	coefficient = {}
	egonetSize = {}
	for node in graphname.nodes():
		ego_graph = nx.ego_graph(graphname, node)
		# Core number
		corenumber[node] = max(nx.core_number(ego_graph).values())
		# egonetSize
		egonetSize[node] = ego_graph.size()
		# Triangle count
		triangleCount = nx.triangles(ego_graph, node)
		triangles[node] = triangleCount  # adding the count for that node in dictionary
		# Clustering co-efficients
		coeff_temp = nx.average_clustering(ego_graph)
		coefficient[node] = coeff_temp  # adding the count for that node in dictionary
		# Connected components minus ego
		ego_graph.remove_node(node)
		number = nx.number_connected_components(ego_graph)  # adding the count for that node in dictionary
		connectedcomponents[node] = number

	print ("***** %s ******" % sys.argv[1])
	print "Core Number Avg \t" + str(float(sum(corenumber.values()) / len(corenumber)))
	print "Connected Component Avg \t" + str(sum(connectedcomponents.values())/len(connectedcomponents))
	print "Triangle Avg \t" + str(sum(triangles.values())/len(triangles))
	print "Coefficient Avg \t" + str(sum(coefficient.values())/len(coefficient))
	print "Ego Net Size Avg \t" + str(sum(egonetSize.values())/len(egonetSize))

if __name__ == "__main__":
    main()