import networkx as nx
import matplotlib.pyplot as plt

def WP(graph:nx.Graph,colors:list):

    V = set(graph.nodes)
    V_colored = {v:None for v in V}

    # 全てのノードを次数で並べ替え
    V_uncolored = [v[0] for v in degree_sorted]

    while len(V_uncolored) > 0:
        # 次数が一番大きいノードに色を塗る
        current = V_uncolored.pop(0)
        color = colors.pop(0)
        V_colored[current] = color

        # 色を塗ったノードと隣接していないノードを次数が大きい順に塗る
        V_notAdjacent = V_uncolored.copy()
        while True:
            V_adjacent = []
            for v in V_notAdjacent:
                if current < v: e = (current,v)
                else:   e = (v,current)
                if e in E:
                    V_adjacent.append(v)
            for v in V_adjacent:
                V_notAdjacent.remove(v)
            if len(V_notAdjacent) == 0: break
            current = V_notAdjacent.pop(0)
            V_colored[current] = color
            V_uncolored.remove(current)
    
    return V_colored, color
    
    
        



# 動作確認
graph = nx.Graph([(1,12), (1,27), (2,3), (2,13), (2,28), (3,4), (3,14), (4,5), (4,17), (5,6), (5,21), (6,7), (6,16), (7,8), (8,9), (8,23), (9,10),
     (10,11), (10,15), (11,24), (12,13), (12,15), (12,26), (14,15), (14,16), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23),
     (24,25), (25,26), (27,28)])
colors = ['red', 'blue', 'yellow', 'green', 'purple', 'orange', 'brown']
V_colored, last_color = WP(graph=graph,colors=colors)
print(list(V_colored.values()))
# nx.draw(graph, node_color = list(V_colored.values()))
# plt.show()