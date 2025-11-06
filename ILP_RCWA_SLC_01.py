from gurobipy import Model,GRB,quicksum
import networkx as nx
import random
import matplotlib.pyplot as plt
from Network_Topology import getTopology

# 引数：無向グラフgraph
def ILP_RCWA_SLC_01(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], C:set[int]):
    # parameter
    V = set(graph.nodes)
    E = set(graph.edges)
    E_DIR = set()   # 有向リンク集合E
    E_incoming = {v:set() for v in V}
    E_outgoing = {v:set() for v in V}
    for u,v in list(graph.edges):
        # 有向リンク集合Eに要素を追加する。
        E_DIR |= {(u,v),(v,u)}
        # ノードu,vから出ていくリンク集合
        E_incoming[u].add((u,v))
        E_incoming[v].add((v,u))
        # ノードu,vに入ってくるリンク集合
        E_outgoing[u].add((v,u))
        E_outgoing[v].add((u,v))

    # variable
    model = Model("ILP_RWA_01")
    alpha = {}
    for r in R:
        for e in E_DIR:
            for w in W:
                for c in C:
                    alpha[r,e,w,c] = model.addVar(vtype=GRB.BINARY, name=f"request{r} use wavelength{w} in edge{e}")
    beta = {}
    for w in W:
        beta[w] = model.addVar(vtype=GRB.BINARY, name=f"wavelength{w} is used")
    w_max = model.addVar(vtype=GRB.INTEGER, name="maximum of wavelength")
    model.update()

    # 流量保存制約
    for r in R:
        src,dest = R[r]
        model.addConstr(quicksum(alpha[r,e,w,c] for e in E_incoming[src] for w in W for c in C)-quicksum(alpha[r,e,w,c] for e in E_outgoing[src] for w in W for c in C)==-1)
        model.addConstr(quicksum(alpha[r,e,w,c] for e in E_incoming[dest] for w in W for c in C)-quicksum(alpha[r,e,w,c] for e in E_outgoing[dest] for w in W for c in C)==1)
        for v in V-{src,dest}:
            for w in W:
                model.addConstr(quicksum(alpha[r,e,w,c] for e in E_incoming[v] for c in C)-quicksum(alpha[r,e,w,c] for e in E_outgoing[v] for c in C)==0)
    
    # 波長非重畳制約
    for e in E:
        v,u = e
        e_reverse = (u,v)
        for w in W:
            for c in C:
                if v < u:
                    model.addConstr(quicksum(alpha[r,e,w,c] for r in R)+quicksum(alpha[r,e_reverse,w,c] for r in R)<=beta[w])
    
    # w_maxの下限
    for w in W:
        model.addConstr(w*beta[w]<=w_max)
    
    model.setObjective(w_max, GRB.MINIMIZE)
    model.optimize()

    path = {r:set() for r in R}
    w_alloc = {r:0 for r in R}
    EPS = 1.e-6
    for r,e,w,c in alpha:
        v,u = e
        if alpha[r,e,w,c].X > EPS:
            w_alloc[r] = w
            if v > u:   path[r].add((c,u,v))
            else:   path[r].add((c,v,u))

    return path, w_alloc, w_max.X


# ネットワークトポロジー1（ノード6リンク9）
# graph = getTopology(topology_number=1)

# ネットワークトポロジー2（ノード6メッシュ型）
graph = getTopology(topology_number=2)

# ネットワークトポロジー3（JPN12）
# graph = getTopology(topology_number=3)

# graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
# graph.add_edges_from([(1,12), (1,27), (2,3), (2,13), (2,28), (3,4), (3,14), (4,5), (4,17), (5,6), (5,21), (6,7), (6,16), (7,8), (8,9), (8,23), (9,10),
#      (10,11), (10,15), (11,24), (12,13), (12,15), (12,26), (14,15), (14,16), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23),
#      (24,25), (25,26), (27,28)])
V = set(graph.nodes)
R = {}
R_number = 100
for r in range(1,R_number+1):
    # ノードの中から2つをランダムで選択する
    [src, dist] = random.sample(list(V), 2)
    R[r] = (src, dist)
W = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
C = {1, 2, 3, 4}

path,w_alloc,w_max = ILP_RCWA_SLC_01(graph=graph, R=R, W=W, C=C)

# print(f"リクエスト集合R={R}")
# for r in R:
#     print("----------------------------")
#     print(f"リクエスト{r}")
#     print(f"パス：{path[r]}")
#     print(f"使用する波長：{w_alloc[r]}")


# G_R = nx.Graph()
# G_R.add_nodes_from(list(R.keys()))
# colorList = ['red', 'blue', 'yellow', 'green', 'purple', 'orange', 'magenta', 'lime', 'cyan', 'pink', 'navy', 'salmon']
# colorMap = {}
# for w in W:
#     color = colorList.pop(0)
#     colorMap[w] = color

# for r1 in R:
#     p1 = path[r1]
#     for r2 in R:
#         if r1 < r2:
#             p2 = path[r2]
#             if not p1.isdisjoint(p2):
#                 G_R.add_edge(r1,r2)

# nx.draw(G_R, node_color = [colorMap[w] for w in list(w_alloc.values())],with_labels=True)
# plt.show()

#. 50回実行する　← リクエストの始点と終点が変化する。
#  ネットワークトポロジー　JPN12を使っても良いが、解が得られるかどうかわからない。