import networkx as nx
from matplotlib import pyplot as plt

def getTopology(topology_number):
    graph = nx.Graph()

    # ネットワークトポロジー1（ノード6リンク9）
    if topology_number == 1:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6])
        graph.add_edges_from([(1,2), (1,4), (2,3), (2,4), (3,4), (3,5), (3,6), (4,5), (5,6)])
    
    # ネットワークトポロジー2（ノード6メッシュ型）
    if topology_number == 2:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6])
        graph.add_edges_from([(1,2), (1,3), (1,4), (1,5), (1,6), (2,3), (2,4), (2,5), (2,6), (3,4), (3,5), (3,6), (4,5), (4,6), (5,6)])
    
    # ネットワークトポロジー3(JPN12)
    if topology_number == 3:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        graph.add_edges_from([(1,2), (1,4), (2,3), (2,4), (3,4), (3,5), (4,6), (5,6), (5,7), (6,8), (6,10), (7,8), (8,9), (9,10), (9,12), (10,11), (11,12)])
    
    return graph

# Network_Topology_01のグラフを表示する。
# graph = getTopology(topology_number=1)
# pos = {1:[-1,0], 2:[-0.5,0.5], 3:[0.5,0.5], 4:[-0.5,-0.5], 5:[0.5,-0.5], 6:[1,0]}
# plt.figure(figsize=(10,10))
# nx.draw_networkx(graph, pos)
# plt.show()

# Network_Topology_02のグラフを表示する。
# graph = getTopology(topology_number=2)
# pos = {1:[-1,0], 2:[-0.5,0.866], 3:[0.5,0.866], 4:[-0.5,-0.866], 5:[0.5,-0.866], 6:[1,0]}
# plt.figure(figsize=(10,10))
# nx.draw_networkx(graph, pos)
# plt.show()

# Network_Topology_03のグラフを表示する。
# graph = getTopology(topology_number=3)
# pos = {1:[-1,-1], 2:[-0.6,0.3], 3:[-0.4,0.3], 4:[-0.4,0], 5:[-0.1,0.2], 6:[0.1,0.2], 7:[0.3,0.5], 8:[0.5,0.4], 9:[0.6,0.2], 10:[0.65,0.15], 11:[0.8,0.5], 12:[1,1]}
# plt.figure(figsize=(10,10))
# nx.draw_networkx(graph, pos)
# plt.show()
