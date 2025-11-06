import networkx as nx

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
