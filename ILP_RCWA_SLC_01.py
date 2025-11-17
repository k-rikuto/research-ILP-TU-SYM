import gurobipy as gp
import networkx as nx
import random

# 引数：無向グラフgraph
def ILP_RCWA_SLC_01(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], C:set[int], getPath=False):
    # parameter
    V = set(graph.nodes)
    E = set(graph.edges)
    E_DIR = set()   # 有向リンク集合E
    L_incoming = {v:set() for v in V}
    L_outgoing = {v:set() for v in V}
    for u,v in list(graph.edges):
        # 有向リンク集合Eに要素を追加する。
        E_DIR |= {(u,v),(v,u)}
        # ノードu,vから出ていくリンク集合
        L_incoming[u].add((u,v))
        L_incoming[v].add((v,u))
        # ノードu,vに入ってくるリンク集合
        L_outgoing[u].add((v,u))
        L_outgoing[v].add((u,v))

    # ログを非表示にするための環境設定
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    # モデルの構築
    model = gp.Model("ILP_RCWA_SLC_01",env=env)

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
    model.update()

    # 流量保存制約
    for r in R:
        src,dest = R[r]
        model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[src] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[src] for w in W for c in C)==-1)
        model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[dest] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[dest] for w in W for c in C)==1)
        for v in V-{src,dest}:
            for w in W:
                model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[v] for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[v] for c in C)==0)
    
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
    
    model.setObjective(w_max,gp.GRB.MINIMIZE)
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

    if getPath:
        return path, w_alloc
    else:
        return round(model.Runtime,2), w_max.X

#. 50回実行する　← リクエストの始点と終点が変化する。
#  ネットワークトポロジー　JPN12を使っても良いが、解が得られるかどうかわからない。