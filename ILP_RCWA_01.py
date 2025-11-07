import gurobipy as gp
import networkx as nx
import random


# 引数：無向グラフgraph
def ILP_RCWA_01(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], C:set[int]):
    # parameter
    V = set(graph.nodes)
    E = set(graph.edges)   # 無向リンク集合E
    E_DIR = set()   # 有向リンク集合E_dir
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

    # ログを非表示にするための環境設定
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    # モデルの構築
    model = gp.Model("ILP_RCWA_01",env=env)

    # variable
    alpha = {}
    for r in R:
        for e in E_DIR:
            for w in W:
                for c in C:
                    alpha[r,e,w,c] = model.addVar(vtype=gp.GRB.BINARY, name=f"request{r} use wavelength{w} in edge{e}")
    beta = {}
    for w in W:
        beta[w] = model.addVar(vtype=gp.GRB.BINARY, name=f"wavelength{w} is used")

    w_max = model.addVar(vtype=gp.GRB.INTEGER, name="maximum of wavelength")

    gamma = {}
    for r in R:
        for c in C:
            gamma[r,c] = model.addVar(vtype=gp.GRB.BINARY, name=f"request {r} use core {c}")
    
    model.update()

    # 流量保存制約
    for r in R:
        src,dest = R[r]
        model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in E_incoming[src] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in E_outgoing[src] for w in W for c in C)==-1)
        model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in E_incoming[dest] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in E_outgoing[dest] for w in W for c in C)==1)
        for v in V-{src,dest}:
            for w in W:
                model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in E_incoming[v] for c in C)-gp.quicksum(alpha[r,e,w,c] for e in E_outgoing[v] for c in C)==0)
    
    # 波長非重畳制約
    for e in E:
        v,u = e
        e_reverse = (u,v)
        for w in W:
            for c in C:
                if v < u:
                    model.addConstr(gp.quicksum(alpha[r,e,w,c] for r in R)+gp.quicksum(alpha[r,e_reverse,w,c] for r in R)<=beta[w])
    
    # w_maxの下限
    for w in W:
        model.addConstr(w*beta[w]<=w_max)
    
    # 変数gamma[r,c]の下限
    for r in R:
        for e in E_DIR:
            for c in C:
                model.addConstr(gp.quicksum(alpha[r,e,w,c] for w in W)<=gamma[r,c])
    
    # コアの連続制約
    for r in R:
        model.addConstr(gp.quicksum(gamma[r,c] for c in C)==1)
    
    model.setObjective(w_max, gp.GRB.MINIMIZE)
    model.optimize()

    path = {r:set() for r in R}
    w_alloc = {r:0 for r in R}
    c_alloc = {r:set() for r in R}
    EPS = 1.e-6
    for r,e,w,c in alpha:
        v,u = e
        if alpha[r,e,w,c].X > EPS:
            w_alloc[r] = w
            c_alloc[r].add(c)
            if v > u:   path[r].add((u,v))
            else:   path[r].add(e)

    return round(model.Runtime,2), w_max.X
