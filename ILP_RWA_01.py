import gurobipy as gp
import networkx as nx

# 引数：無向グラフgraph
def ILP_RWA_01(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], getPath=False):
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
    
    # ログを非表示にするための環境設定
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    # variable
    model = gp.Model("ILP_RWA_01",env=env)
    alpha = {}
    for r in R:
        for e in E_DIR:
            for w in W:
                alpha[r,e,w] = model.addVar(vtype=gp.GRB.BINARY, name=f"request{r} use wavelength{w} in edge{e}")
    beta = {}
    for w in W:
        beta[w] = model.addVar(vtype=gp.GRB.BINARY, name=f"wavelength{w} is used")
    w_max = model.addVar(vtype=gp.GRB.INTEGER, name="maximum of wavelength")
    model.update()

    # 流量保存制約
    for r in R:
        src,dest = R[r]
        model.addConstr(gp.quicksum(alpha[r,e,w] for e in E_incoming[src] for w in W)-gp.quicksum(alpha[r,e,w] for e in E_outgoing[src] for w in W)==-1)
        model.addConstr(gp.quicksum(alpha[r,e,w] for e in E_incoming[dest] for w in W)-gp.quicksum(alpha[r,e,w] for e in E_outgoing[dest] for w in W)==1)
        for v in V-{src,dest}:
            for w in W:
                model.addConstr(gp.quicksum(alpha[r,e,w] for e in E_incoming[v])-gp.quicksum(alpha[r,e,w] for e in E_outgoing[v])==0)
    
    # # 波長非重畳制約
    # for e in E:
    #     v,u = e
    #     e_reverse = (u,v)
    #     for w in W:
    #         model.addConstr(gp.quicksum(alpha[r,e,w] for r in R)+gp.quicksum(alpha[r,e_reverse,w] for r in R)<=beta[w])
        
    # 波長非重畳制約
    for e in E:
        v,u = e
        e_reverse = (u,v)
        for w in W:
            model.addConstr(gp.quicksum(alpha[r,e,w]+alpha[r,e_reverse,w] for r in R)<=beta[w])

    # w_maxの下限
    for w in W:
        model.addConstr(w*beta[w]<=w_max)
    
    model.setObjective(w_max, gp.GRB.MINIMIZE)
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

    if getPath:
        return path, w_alloc
    else:
        return round(model.Runtime,2), w_max.X
    