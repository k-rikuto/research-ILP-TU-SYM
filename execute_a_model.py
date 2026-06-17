import networkx as nx

from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_04 import ILP_RCWA_04
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from ILP_RCWA_SLC_04 import ILP_RCWA_SLC_04
from ILP_RWA_01 import ILP_RWA_01
from ILP_RWA_02 import ILP_RWA_02
from ILP_RWA_03 import ILP_RWA_03
from Network_Topology import get_topology
from check_cycle import check_cycle


def execute_a_model(model_name:str, graph:nx.Graph, R:dict[int,tuple[int,int]]) -> tuple[float, int]:

    
    # 波長
    W_number = 50
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    isRWA = False
    if model_name == "ILP_RCWA_01":
        isOptimal, runtime, w_max, data = ILP_RCWA_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_02":
        isOptimal, runtime, w_max, data = ILP_RCWA_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_03":
        isOptimal, runtime, w_max, data = ILP_RCWA_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_04":
        isOptimal, runtime, w_max, data = ILP_RCWA_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_01":
        isOptimal, runtime, w_max, data = ILP_RCWA_SLC_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_02":
        isOptimal, runtime, w_max, data = ILP_RCWA_SLC_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_03":
        isOptimal, runtime, w_max, data = ILP_RCWA_SLC_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_04":
        isOptimal, runtime, w_max, data = ILP_RCWA_SLC_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RWA_01":
        isOptimal, runtime, w_max, data = ILP_RWA_01(graph=graph, R=R, W=W)
        isRWA = True
    elif model_name == "ILP_RWA_02":
        isOptimal, runtime, w_max, data = ILP_RWA_02(graph=graph, R=R, W=W)
        isRWA = True
    elif model_name == "ILP_RWA_03":
        isOptimal, runtime, w_max, data = ILP_RWA_03(graph=graph, R=R, W=W)
        isRWA = True
    else:
        print("モデルがありません。")
        runtime = 0.0
        w_max = 0
        isOptimal = False
    
    if __name__ == "__main__":
        if isOptimal:

            for r_index in data:
                r,p,w = data[r_index]
                print("リクエスト",r_index,":",r)
                print("パス",p)
                print("波長",w)
            
            # 各リンクごとにどのリクエストが使用しているかを可視化
            empty = "--"
            cycle_num = 0
            if isRWA:
                visualize_links = {link:[empty for i in range(w_max)] for link in graph.edges}
                for r_index in data:
                    r,p,w = data[r_index]
                    if check_cycle(r=r,path=p,V=graph.nodes): cycle_num = cycle_num+1
                    if r_index < 10:
                        r_index_str = f"0{r_index}"
                    else:
                        r_index_str = f"{r_index}"
                    for  u,v,c in p:
                        if u<=v:
                            visualize_links[(u,v)][w-1] = r_index_str
                        else:
                            visualize_links[(v,u)][w-1] = r_index_str
                
                for link in visualize_links:
                    print(link,end="")
                    print("[",end="")
                    for space in visualize_links[link]:
                        print(" "+space+" ",end="")
                    print("]")
            else:
                visualize_links = {link:{c:[empty for i in range(w_max)] for c in C} for link in graph.edges}
                for r_index in data:
                    r,p,w = data[r_index]
                    if check_cycle(r=r,path=p,V=graph.nodes): cycle_num = cycle_num+1
                    if r_index < 10:
                        r_index_str = f"0{r_index}"
                    else:
                        r_index_str = f"{r_index}"
                    for  u,v,c in p:
                        if u<=v:
                            visualize_links[(u,v)][c][w-1] = r_index_str
                        else:
                            visualize_links[(v,u)][c][w-1] = r_index_str

                for link in visualize_links:
                    print(link)
                    for c in C:
                        print("コア",c,end=" ")
                        print("[",end="")
                        for space in visualize_links[link][c]:
                            print(" "+space+" ",end="")
                        print("]")
            print("閉路の数",cycle_num)

    return runtime, w_max




if __name__ == "__main__":
    # 実験に使用するネットワークトポロジーを選択する
    graph,topology_name = get_topology(topology_number=3)
    model_name = "ILP_RCWA_04"

    R_sd = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12),
        (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12),
        (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12),
        (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12),
        (7,8), (7,9), (7,10), (7,11), (7,12),(8,9), (8,10), (8,11), (8,12), (9,10), (9,11), (9,12), (10,11), (10,12), (11,12)
        ]
    r_num = [1, 1, 1, 3, 1, 4, 0, 3, 0, 2, 2, 2, 2, 1, 1, 0, 3, 2, 1, 2, 0, 0, 4, 3, 3, 0, 0, 2, 0, 1, 1, 1, 0, 1, 2, 2, 0, 0, 2, 0, 3, 1, 0, 1, 2, 0, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 2, 0, 0, 2, 0, 2, 1, 1, 1, 2]

    R:dict[int,tuple[int,int]] = {}
    num = 1
    for i in range(len(r_num)):
        for j in range(r_num[i]):
            R[num] = R_sd[i]
            num = num+1

    print(f"リクエストの数：{sum(r_num)}")
    print(f"モデル：{model_name}")
    print(f"ネットワークトポロジー：{topology_name}")
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":
        runtime, w_max = execute_a_model(model_name=model_name, graph=graph, R=R)
        print(runtime,w_max)

