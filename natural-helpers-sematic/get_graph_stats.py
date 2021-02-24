from __future__ import division

import pickle
import sys
import networkx as nx
import pdb

G = nx.Graph ()            

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    global G
    f = open(sys.argv[1])
    G = pickle.load(f)
    f.close()

    print ("***** %s ******" % sys.argv[1])
    print ("|V|: \t%d" % len(G))
    print ("|E|: \t%d" % len(G.edges()))
    print ("Triangles: \t%d" % (sum(nx.triangles(G).values())/float(len(G))))
    print ("Ave clustering: \t%f" % nx.average_clustering(G))
    print ("Ave degree: \t%f" % (sum(dict(G.degree()).values())/float(len(G))))
           
if __name__ == "__main__":
    main()

