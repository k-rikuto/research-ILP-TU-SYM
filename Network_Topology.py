import networkx as nx
from matplotlib import pyplot as plt

def get_topology(topology_number:int):
    graph = nx.Graph()
    topology_name = ''

    # ネットワークトポロジー0（データ構造を調べるための超簡易ネットワーク）
    if topology_number == 0:
        graph.add_nodes_from([1, 2, 3, 4])
        graph.add_edges_from([(1,2), (2,3), (2,4), (3,4)])
        topology_name = 'Network_Topology_00'

    # ネットワークトポロジー1（ノード6リンク9）
    if topology_number == 1:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6])
        graph.add_edges_from([(1,2), (1,4), (2,3), (2,4), (3,4), (3,5), (3,6), (4,5), (5,6)])
        topology_name = 'Network_Topology_01'
    
    # ネットワークトポロジー2（ノード6メッシュ型）
    if topology_number == 2:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6])
        graph.add_edges_from([(1,2), (1,3), (1,4), (1,5), (1,6), (2,3), (2,4), (2,5), (2,6), (3,4), (3,5), (3,6), (4,5), (4,6), (5,6)])
        topology_name = 'Network_Topology_02'
    
    # ネットワークトポロジー3(JPN12)
    if topology_number == 3:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        graph.add_edges_from([(1,2), (1,4), (2,3), (2,4), (3,4), (3,5), (4,6), (5,6), (5,7), (6,8), (6,10), (7,8), (8,9), (9,10), (9,12), (10,11), (11,12)])
        topology_name = 'Network_Topology_03'
    
    # ネットワークトポロジー4(European Backbone Network, EBN)
    if topology_number == 4:
        graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
        graph.add_edges_from([(1,12), (1,27), (2,3), (2,13), (2,28), (3,4), (3,14), (4,5), (4,17), (5,6), (5,21), (6,7), (6,16), (7,8), (8,9), (8,23), (9,10), (10,11), (10,15), (11,24), (12,13), (12,15), (12,26), (14,15), (14,16), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23), (24,25), (25,26), (27,28)])
        topology_name = 'Network_Topology_04'
    
    return graph,topology_name

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
