import pickle
import networkx as nx
import sys

G = nx.MultiDiGraph ()            
H = nx.MultiDiGraph ()            
I = nx.DiGraph ()
J = nx.Graph ()

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    f = open("at_multidigraph.pkl")
    G = pickle.load(f)
    f.close()
    f = open(sys.argv[1])
    H = pickle.load(f)
    f.close()

    for u,v,data in H.edges (data=True):
        if I.has_edge(u,v):
            I[u][v]["weight"] = I[u][v]["weight"] + 1
        else:
            I.add_edge(u,v, weight = 1, tokens = data["tokens"])
    
    for u,v, data in I.edges(data=True):
        if I.has_edge(u,v) and I.has_edge(v,u):
            J.add_edge(u,v, weight=min(I[u][v]["weight"], I[v][u]["weight"]), tokens = data["tokens"])


    dumpit(sys.argv[2], I)
    dumpit(sys.argv[3], J)
    
if __name__ == "__main__":
    main()

    

    
