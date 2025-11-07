import networkx as nx
import matplotlib.pyplot as plt

def WP(graph:nx.Graph,colors:list):

    V = set(graph.nodes)
    V_colored = {v:None for v in V}

    # 全てのノードを次数で並べ替え
    V_uncolored = sorted(list(V), key=lambda x: graph.degree[x], reverse=True)

    while len(V_uncolored) > 0:
        # 次数が一番大きいノードに色を塗る
        current = V_uncolored.pop(0)
        color = colors.pop(0)
        V_colored[current] = color

        # 色を塗ったノードと隣接していないノードを次数が大きい順に塗る
        V_notAdj = V_uncolored.copy()    # currentノードと隣接していないノードのリスト
        # 現在のノードに隣接しないノードに同じ色を塗る
        while True:
            for adj in list(graph.adj[current].keys()):
                if adj in V_notAdj: V_notAdj.remove(adj)
            if len(V_notAdj)==0:    break
            current = V_notAdj.pop(0)
            V_colored[current] = color
            V_uncolored.remove(current)

    return V_colored, color
    
    
        



# 動作確認
# graph =nx.Graph()
# graph.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
# graph.add_edges_from([(1,2), (1,7), (2,8), (2,10), (2,8), (3,4), (3,10), (4,5), (4,7), (5,6), (5,8), (6,10), (6,9), (7,8), (8,9)])
# colors = ['red', 'blue', 'yellow', 'green', 'purple', 'orange', 'brown']
# V_colored, last_color = WP(graph=graph,colors=colors)
# nx.draw(graph, node_color = list(V_colored.values()),with_labels=True)
# plt.show()