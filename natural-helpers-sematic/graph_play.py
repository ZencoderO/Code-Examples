import pickle
import networkx as nx
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tygraph", help="input: thank you graph")
    parser.add_argument("--amdgraph", help="input: @ multidigraph")
    parser.add_argument("--otydgraph", help="output: thankyou digraph")
    parser.add_argument("--otygraph", help="output: thankyou graph")

    args = parser.parse_args()
    return args

G = nx.MultiDiGraph ()            
H = nx.MultiDiGraph ()            
I = nx.DiGraph ()
J = nx.Graph ()

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    args = parse_args()
    f = open(args.amdgraph)
    G = pickle.load(f)
    f.close()

    f = open(args.tygraph)
    H = pickle.load(f)
    f.close()

    for u,v in H.edges():
        if I.has_edge(u,v):
            I[u][v]["weight"] = I[u][v]["weight"] + 1
        else:
            I.add_edge(u,v, weight = 1)
    
    for u,v in I.edges():
        if I.has_edge(u,v) and I.has_edge(v,u):
            J.add_edge(u,v, weight=min(I[u][v]["weight"], I[v][u]["weight"]))


    dumpit(args.otydgraph, I)
    dumpit(args.otygraph, J)
    
if __name__ == "__main__":
    main()

    

    
