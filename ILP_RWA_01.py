from gurobipy import Model,GRB,quicksum
import networkx as nx
import random
import matplotlib.pyplot as plt
from Network_Topology import getTopology

# 引数：無向グラフgraph
def ILP_RWA_01(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int]):
    # parameter
    V = set(graph.nodes)
    E = set()   # 有向リンク集合E
    E_incoming = {v:set() for v in V}
    E_outgoing = {v:set() for v in V}
    for u,v in list(graph.edges):
        # 有向リンク集合Eに要素を追加する。
        E |= {(u,v),(v,u)}
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
        for e in E:
            for w in W:
                alpha[r,e,w] = model.addVar(vtype=GRB.BINARY, name=f"request{r} use wavelength{w} in edge{e}")
    beta = {}
    for w in W:
        beta[w] = model.addVar(vtype=GRB.BINARY, name=f"wavelength{w} is used")
    w_max = model.addVar(vtype=GRB.INTEGER, name="maximum of wavelength")
    model.update()

    # 流量保存制約
    for r in R:
        src,dest = R[r]
        model.addConstr(quicksum(alpha[r,e,w] for e in E_incoming[src] for w in W)-quicksum(alpha[r,e,w] for e in E_outgoing[src] for w in W)==-1)
        model.addConstr(quicksum(alpha[r,e,w] for e in E_incoming[dest] for w in W)-quicksum(alpha[r,e,w] for e in E_outgoing[dest] for w in W)==1)
        for v in V-{src,dest}:
            for w in W:
                model.addConstr(quicksum(alpha[r,e,w] for e in E_incoming[v])-quicksum(alpha[r,e,w] for e in E_outgoing[v])==0)
    
    # 波長非重畳制約
    for e in E:
        v,u = e
        e_reverse = (u,v)
        for w in W:
            if v < u:
                model.addConstr(quicksum(alpha[r,e,w] for r in R)+quicksum(alpha[r,e_reverse,w] for r in R)<=beta[w])
    
    # w_maxの下限
    for w in W:
        model.addConstr(w*beta[w]<=w_max)
    
    model.setObjective(w_max, GRB.MINIMIZE)
    model.optimize()

    path = {r:set() for r in R}
    w_alloc = {r:0 for r in R}
    EPS = 1.e-6
    for r,e,w in alpha:
        v,u = e
        if alpha[r,e,w].X > EPS:
            w_alloc[r] = w
            if v > u:   path[r].add((u,v))
            else:   path[r].add(e)

    return path, w_alloc, w_max.X



graph = nx.Graph()
graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
graph.add_edges_from([(1,12), (1,27), (2,3), (2,13), (2,28), (3,4), (3,14), (4,5), (4,17), (5,6), (5,21), (6,7), (6,16), (7,8), (8,9), (8,23), (9,10),
     (10,11), (10,15), (11,24), (12,13), (12,15), (12,26), (14,15), (14,16), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23),
     (24,25), (25,26), (27,28)])
V = set(graph.nodes)
R = {}
R_size = 100
for r in range(1,R_size+1):
    # ノードの中から2つをランダムで選択する
    [src, dist] = random.sample(list(V), 2)
    R[r] = (src, dist)
W = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}

path,w_alloc,w_max = ILP_RWA_01(graph=graph, R=R, W=W)
for r in R:
    print("----------------------------")
    print(f"リクエスト{r}")
    print(f"パス：{path[r]}")
    print(f"使用する波長：{w_alloc[r]}")
