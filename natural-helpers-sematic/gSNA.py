import collections
import csv
import json
import networkx as nx

def ReadCsvDiGraph(nodeCsv, edgeCsv, intId, nodeId, edgeSrc, edgeDest, edgeWeight, nodeExclude):
    G = nx.DiGraph()
    with open(nodeCsv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if intId:
                id = int(row[nodeId])
            else:
                id = row[nodeId]
            r = collections.OrderedDict()
            for key in row:
                if key not in nodeExclude:
                    r[key] = row[key]
            G.add_node(id, r)
    with open(edgeCsv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if intId:
                src = int(row[edgeSrc])
                dest = int(row[edgeDest])
            else:
                src = row[edgeSrc]
                dest = row[edgeDest]
            G.add_weighted_edges_from([(src, dest, float(row[edgeWeight]))])
    return G

def GetNodeDegreeInformation(G, csvfile):
    with open(csvfile, 'w') as file:
        data = collections.OrderedDict()
        nodes = sorted(nx.nodes(G))
        # Degrees
        d_list = list(G.degree_iter(sorted(nx.nodes(G))))
        degrees = {}
        for n in d_list:
            degrees[n[0]] = n[1]
        id_list = list(G.in_degree_iter(sorted(nx.nodes(G))))
        # Out Degrees
        in_degrees = {}
        for n in id_list:
            in_degrees[n[0]] = n[1]
        # In Degrees
        od_list = list(G.out_degree_iter(sorted(nx.nodes(G))))
        out_degrees = {}
        for n in od_list:
            out_degrees[n[0]] = n[1]
        # Build Dictionary
        for n in nodes:
            data[n] = collections.OrderedDict()
            data[n]["d"] = degrees[n]
            data[n]["id"] = in_degrees[n]
            data[n]["od"] = out_degrees[n]
        # Write CSV
        file.write("Id,Degree,In-Degree,Out-Degree\n")
        for key in data:
            file.write(str(key) + ',' + str(data[key]["d"]) + ',' + str(data[key]["id"]) + ','  + str(data[key]["od"]) + '\n')

def GetAllPairsNodeConnectivity(G, csvfile):
    with open(csvfile, 'w') as file:
        data = collections.OrderedDict()
        nodes = sorted(nx.nodes(G))
        apnc = nx.all_pairs_node_connectivity(G)
        # Write Header
        for n in nodes:
            file.write(',' + str(n))
        file.write('\n')
        # Create and Write Body
        for n in nodes:
            s = str(n)
            for k in nodes:
                s += ','
                if n != k:
                    s += str(apnc[n][k])
            file.write(s + '\n')

def GetCommunicability(G, csvfile):
    with open(csvfile, 'w') as file:
        data = collections.OrderedDict()
        nodes = sorted(nx.nodes(G))
        comm = nx.communicability(G)
        # Write Header
        for n in nodes:
            file.write(',' + str(n))
        file.write('\n')
        # Create and Write Body
        for n in nodes:
            s = str(n)
            for k in nodes:
                s += ','
                if n != k:
                    s += str(comm[n][k])
            file.write(s + '\n')

def GetGraphStatistics(G, csvfile, negWeights):
    with open(csvfile, 'w') as file:
        nodes = sorted(nx.nodes(G))
        # Stats
        file.write("Node Count," + str(len(nodes)) + '\n')
        file.write("Edge Count," + str(len(nx.edges(G))) + '\n')
        file.write("Node Connectivity," + str(nx.node_connectivity(G)) + '\n')
        file.write("Transitivity," + str(nx.transitivity(G)) + '\n')
        # Closeness Centrality
        file.write("Closeness Centrality")
        cc = nx.closeness_centrality(G)
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # Degree Centrality
        file.write("Degree Centrality")
        cc = nx.degree_centrality(G)
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # In-Degree Centrality
        file.write("In-Degree Centrality")
        cc = nx.in_degree_centrality(G)
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # Out-Degree Centrality
        file.write("Out-Degree Centrality")
        cc = nx.out_degree_centrality(G)
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # Betweenness Centrality
        file.write("Betweenness Centrality")
        cc = nx.betweenness_centrality(G, weight="weight")
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # Eigenvector Centrality
        file.write("Eigenvector Centrality")
        cc = nx.eigenvector_centrality(G, weight="weight")
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # PageRank
        file.write("PageRank")
        cc = nx.pagerank(G, weight="weight")
        for key in cc:
            file.write(',' + str(key))
        file.write('\n')
        for key in cc:
            file.write(',' + str(cc[key]))
        file.write('\n')
        # Load Centrality
        if not negWeights:
            file.write("Load Centrality")
            cc = nx.load_centrality(G, weight="weight")
            for key in cc:
                file.write(',' + str(key))
            file.write('\n')
            for key in cc:
                file.write(',' + str(cc[key]))
            file.write('\n')

def Run(folder):
    GraphPrefix = ["Activities", "CommunicationFrequency", "CompareFrequency", "Contact", "PersonalGrowth", "TypeActivities1", "TypeActivities2", "TypeActivities3", "TypeActivities4", "TypeActivities5"]
    for gp in GraphPrefix:
        G = ReadCsvDiGraph('nodes_+Master.csv', 'edges_' + gp + '.csv', True, 'Id', 'Source', 'Target', 'Weight', ['Id'])
        GetNodeDegreeInformation(G, folder + gp + "_NodeDegreeInformation.csv")
        GetAllPairsNodeConnectivity(G, folder + gp + "_AllPairsNodeConnectivity.csv")
        GetGraphStatistics(G, folder + gp + "_Statistics.csv", gp == "CompareFrequency")

Run("out/")
#G = ReadCsvDiGraph('nodes_+Master.csv', 'edges_Activities.csv', True, 'Id', 'Source', 'Target', 'Weight', ['Id'])
#GetNodeDegreeInformation(G, "activities_NodeDegreeInformation.csv")
#GetAllPairsNodeConnectivity(G, "activities_AllPairsNodeConnectivity.csv")
#GetGraphStatistics(G, "activities_Statistics.csv")
