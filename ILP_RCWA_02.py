import gurobipy as gp
import networkx as nx
import random

'''
SLCなし、完全単模性を保持せずに、対称性を完全に削除したRCWAモデル

    Minimize,   ∑_(ω∈W)▒〖ωβ〗^ω 

    subject to
    <流量保存制約>
    ∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(s_r)^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(s_r)^+)▒α_r^(e,ω,c) =-1,∀r∈R
    ∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(d_r)^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(d_r)^+)▒α_r^(e,ω,c) =1,∀r∈R
    ∑_(c∈C)▒∑_(e∈L_v^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(e∈L_v^+)▒α_r^(e,ω,c) =0,∀r∈R,v∈V∖{s_r,d_r },ω∈W
    <波長非重畳制約>
    ∑_(r∈R)▒α_r^(e,ω,c) ≤β^ω,∀e∈E,ω∈W,c∈C
    <γ_r^cの下限>
    ∑_(ω∈W)▒α_r^(e,ω,c) ≤γ_r^c,∀r∈R,e∈E,c∈C
    <コアの連続制約>
    ∑_(c∈C)▒γ_r^c =1,∀r∈R

    
引数の説明
1.  graph
概要：ネットワークトポロジーを表した無向グラフG=(V,E)
型：networkxのGraphオブジェクト

2.  R
概要：リクエストのインデックス番号から送信元のノード番号、宛先のノード番号を取得するための変数
型：keyがint、valueがtuple[int,int]の辞書型

3.  W
概要：波長のインデックス番号を要素とする集合
型：intのset型

4.  C
概要：コアのインデックス番号を要素とする集合
型：intのset型

'''

def ILP_RCWA_02(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], C:set[int], getPath=False):
    # parameter
    V = set(graph.nodes)
    E = set(graph.edges)   # 無向リンク集合E
    E_DIR = set()   # 有向リンク集合E_dir
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
    model = gp.Model("ILP_RCWA_02",env=env)

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


    gamma = {}
    for r in R:
        for c in C:
            gamma[r,c] = model.addVar(vtype=gp.GRB.BINARY, name=f"request {r} use core {c}")
    
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
    
    # 変数gamma[r,c]の下限
    for r in R:
        for e in E_DIR:
            for c in C:
                model.addConstr(gp.quicksum(alpha[r,e,w,c] for w in W)<=gamma[r,c])
    
    # コアの連続制約
    for r in R:
        model.addConstr(gp.quicksum(gamma[r,c] for c in C)==1)
    
    model.setObjective(gp.quicksum(w*beta[w] for w in W), gp.GRB.MINIMIZE)
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
    
    for w in W:
        if beta[w].X > EPS:
            w_max = w

    if getPath:
        return path, w_alloc
    else:
        return round(model.Runtime,2), float(w_max)
