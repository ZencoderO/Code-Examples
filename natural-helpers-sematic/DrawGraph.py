import networkx as nx
import pickle
import matplotlib.pyplot as plt
import sys

B = nx.MultiDiGraph ()
f = open(sys.argv[1])
B = pickle.load(f)
f.close()

T = nx.MultiDiGraph ()
f = open(sys.argv[2])
T = pickle.load(f)
f.close()

addT = []
for node in T:
    if T.degree(node) > 0:
        addT.append(node)

addB = []
for node in B:
    if B.degree(node) > 0:
        addB.append(node)


TS = T.subgraph(addT)
BS = B.subgraph(addB)



UserT = []
for node in TS:
    UserT.append(node)

UserB = []
for node in BS:
    UserB.append(node)


nodeT = set(UserT) - set(UserB)
nodeB = set(UserB) - set(UserT)
nodeC = set(UserT) - (set(UserT) - set(UserB))
F = nx.compose(TS,BS)
plt.figure(3,figsize=(19,19)) 
pos=nx.spring_layout(F) # positions for all nodes

nx.draw_networkx_nodes(F,pos,
                       nodelist=nodeT,
                       node_color='blue',
                       node_size=180,
                   alpha=0.8)
nx.draw_networkx_nodes(F,pos,
                       nodelist=nodeB,
                       node_color='chartreuse',
                       node_size=180,
                   alpha=0.8)

nx.draw_networkx_nodes(F,pos,
                       nodelist=nodeC,
                       node_color='red',
                       node_size=180,
                   alpha=0.8)

nx.draw_networkx_edges(TS,pos,
                       edgelist=TS.edges(),
                       width=5,alpha=0.3,edge_color='black')

nx.draw_networkx_edges(BS,pos,
                       edgelist=BS.edges(),
                       width=5,alpha=0.3,edge_color='black')


#
# options = {
#     'node_color': 'black',
#     'node_size': 10,
#     'width': 1,
#     'arrowstyle': '-|>',
#     'arrowsize': 12,
# }
# nx.draw_networkx(H, arrows=True, with_labels=True, **options)
#
plt.savefig(sys.argv[3],dpi=100) # save as df

plt.show()
