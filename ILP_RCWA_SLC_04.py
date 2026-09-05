import gurobipy as gp
import networkx as nx
from convert_vars_to_data import convert_vars_to_data

'''
SLCあり、完全単模性を保持せずに、対称性を完全に削除したRCWAモデル

    Minimize,   W_max

    subject to
    <流量保存制約>
    ∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(s_r)^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(s_r)^+)▒α_r^(e,ω,c) =-1,∀r∈R
    ∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(d_r)^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(ω∈W)▒∑_(e∈L_(d_r)^+)▒α_r^(e,ω,c) =1,∀r∈R
    ∑_(c∈C)▒∑_(e∈L_v^-)▒α_r^(e,ω,c) -∑_(c∈C)▒∑_(e∈L_v^+)▒α_r^(e,ω,c) =0,∀r∈R,v∈V∖{s_r,d_r },ω∈W
    <波長非重畳制約>
    ∑_(r∈R)▒α_r^(e,ω,c) ≤β^ω,∀e∈E,ω∈W,c∈C
    <W_maxの下限>
    ωβ^ω≤W_max,∀ω∈W
    <γ_r^cの下限>
    ∑_(ω∈W)▒α_r^(e,ω,c) ≤γ_r^c,∀r∈R,e∈E,c∈C

    
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

def ILP_RCWA_SLC_04(graph:nx.Graph, R:dict[int,tuple[int,int]], W:set[int], C:set[int], timelimit=0, restart=False) -> tuple[bool,float,int,dict[int, tuple[tuple[int, int], set[tuple[int, int, int]], int]],int]:

    if timelimit == 0:
        # ログを非表示にするための環境設定
        env = gp.Env(empty=True)
        env.setParam('OutputFlag', 1)
        env.setParam('LogToConsole', 0)
        env.setParam('LogFile', "results/Logs/RCWA_SLC_04.log")
        env.start()
    else:
        env = gp.Env()
        env.setParam('OutputFlag', 1)
        env.start()
    
    ## parameter
    # ネットワークのノード集合V
    V = set(graph.nodes)
    # ネットワークの無向リンク集合E
    E = set(graph.edges)
    # 有向リンク集合E_dir
    E_DIR = set()
    # ノードvに入っていくリンク集合L_v^-
    L_incoming = {v:set() for v in V}
    # ノードvから出ていくリンク集合L_v^+
    L_outgoing = {v:set() for v in V}

    for u,v in list(graph.edges):
        # 有向リンク集合Eに要素を追加する。
        E_DIR |= {(u,v),(v,u)}
        # ノードu,vから出ていくリンク集合
        L_outgoing[u].add((u,v))
        L_outgoing[v].add((v,u))
        # ノードu,vに入ってくるリンク集合
        L_incoming[u].add((v,u))
        L_incoming[v].add((u,v))

    # 実行時間の初期化
    runtime = 0.0
    
    # モデルの構築
    if restart:
        print("再開")
        # 過去の記録を取り込む
        model = gp.read("./save/model.mps",env=env)
        model.read("./save/state.mst")

        alpha = {}
        for r in R:
            for e in E_DIR:
                for w in W:
                    for c in C:
                        alpha[r,e,w,c] = model.getVarByName(name=f"alpha_{r}_{u}_{v}_{w}_{c}")
        beta = {}
        for w in W:
            beta[w] = model.getVarByName(name=f"beta_{w}")


        # 過去の累積実行時間を取り出す
        with open("./save/runtime.txt",'r') as f:
            runtime = float(f.read())

    else:
        model = gp.Model("ILP_RCWA_SLC_01",env=env)

        ## variable
        alpha = {}
        for r in R:
            for e in E_DIR:
                (u,v) = e
                for w in W:
                    for c in C:
                        alpha[r,e,w,c] = model.addVar(vtype=gp.GRB.BINARY, name=f"alpha_{r}_{u}_{v}_{w}_{c}")
        beta = {}
        for w in W:
            beta[w] = model.addVar(vtype=gp.GRB.BINARY, name=f"beta_{w}")

        

        # 流量保存制約
        for r in R:
            src,dest = R[r]
            model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[src] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[src] for w in W for c in C)==-1)
            model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[dest] for w in W for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[dest] for w in W for c in C)==1)
            for v in V-{src,dest}:
                for w in W:
                    model.addConstr(gp.quicksum(alpha[r,e,w,c] for e in L_incoming[v] for c in C)-gp.quicksum(alpha[r,e,w,c] for e in L_outgoing[v] for c in C)==0)
        
        # 波長非重畳制約（betaの下限）
        for e in E:
            (v,u) = e
            e_reverse = (u,v)
            for w in W:
                for c in C:
                    if v < u:
                        model.addConstr(gp.quicksum(alpha[r,e,w,c] for r in R)+gp.quicksum(alpha[r,e_reverse,w,c] for r in R)<=beta[w])
        
        # beta_wの順序関係
        for w in W:
            if w+1 in W:
                model.addConstr(beta[w]-beta[w+1]>=0)
        
        model.setObjective(gp.quicksum(beta[w] for w in W), gp.GRB.MINIMIZE)
        model.update()
    

    # 時間制限の設定
    if timelimit != 0:
        print("時間制限あり")
        model.setParam("NodefileStart", 0.5)
        model.setParam("NodefileDir", "./save/")
        model.setParam("TimeLimit", timelimit)
        

    model.optimize()

    isOptimal = False
    runtime += float(model.Runtime)
    w_used = 0
    data = {}
    w_max = -100

    ## タイムリミットで中断した際の処理 + モデルが正常終了した時の処理 + モデルが異常終了した時の処理
    # モデルの途中解、分枝の状態、累積計算時間を保存する
    if model.Status == gp.GRB.TIME_LIMIT:
        if model.SolCount > 0:
            model.write("./save/model.mps")
            model.write("./save/state.mst")
            with open('./save/runtime.txt', 'w') as f:
                    f.write(f"{runtime}")
        else:
            print("実行可能解が見つかっていない。")
    ## 最適解を計算できた際の処理
    # runtime, w_usedを返す。getPathがTrueの時、pathとw_allocも返す
    elif model.Status == gp.GRB.OPTIMAL:
        isOptimal = True
        EPS = 0.5
        for w in W:
            if beta[w].X > EPS:
                w_used += 1
        data, w_max = convert_vars_to_data(alpha=alpha, E_DIR=E_DIR, R=R, W=W, C=C)
    ## 何かしらのエラーが発生した際の処理
    else:
        print("何かしらのエラーが発生")
        print(f"ステータスコード：{model.Status}")
    
    return isOptimal, round(runtime, 2), w_used, data, w_max