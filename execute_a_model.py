import networkx as nx
import os
import pandas as pd

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
from generate_request import generate_request


def execute_a_model(model_name:str, graph:nx.Graph, R:dict[int,tuple[int,int]], visualized_links:dict[tuple[int,int,int],list[str]]={}) -> tuple[float,int]:

    
    # 波長
    W_number = 35
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    isRWA = False
    if model_name == "ILP_RCWA_01":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_02":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_03":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_04":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_01":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_SLC_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_02":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_SLC_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_03":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_SLC_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_04":
        isOptimal, runtime, w_used, data, w_max = ILP_RCWA_SLC_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RWA_01":
        isOptimal, runtime, w_used, data, w_max = ILP_RWA_01(graph=graph, R=R, W=W)
        isRWA = True
    elif model_name == "ILP_RWA_02":
        isOptimal, runtime, w_used, data, w_max = ILP_RWA_02(graph=graph, R=R, W=W)
        isRWA = True
    elif model_name == "ILP_RWA_03":
        isOptimal, runtime, w_used, data, w_max = ILP_RWA_03(graph=graph, R=R, W=W)
        isRWA = True
    else:
        print("モデルがありません。")
        runtime = 0.0
        w_used = 0
        w_max = 0
        isOptimal = False
    
    if isRWA: C={1}
    
    if __name__ == "__main__":
        if isOptimal:
            # for r_index in data:
            #     r,p,w = data[r_index]
            #     print("リクエスト",r_index,":",r)
            #     print("パス",p)
            #     print("波長",w)
            
            # 各リンクごとにどのリクエストが使用しているかを可視化
            empty = "'---"
            cycle_num = 0
            for u,v in graph.edges:
                for c in C:
                    visualized_links[(u,v,c)] = [empty for i in range(w_max)]
            for r_index in data:
                r,p,w = data[r_index]
                if check_cycle(r=r,path=p,V=graph.nodes): cycle_num = cycle_num+1
                if r_index < 10:
                    r_index_str = f"'00{r_index}"
                elif r_index < 100:
                    r_index_str = f"'0{r_index}"
                else:
                    r_index_str = f"'{r_index}"
                for  u,v,c in p:
                    if u<=v:
                        visualized_links[(u,v,c)][w-1] = r_index_str
                    else:
                        visualized_links[(v,u,c)][w-1] = r_index_str

            # for u,v,c in visualize_links:
            #     print((u,v))
            #     for c in C:
            #         print("コア",c,end=" ")
            #         print("[",end="")
            #         for space in visualize_links[u,v,c]:
            #             print(" "+space+" ",end="")
            #         print("]")

            print("閉路の数",cycle_num)

    return runtime, w_used, w_max



if __name__ == "__main__":
    # 実験に使用するネットワークトポロジーを選択する
    graph,topology_name = get_topology(topology_number=3)
    models = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_04", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03", "ILP_RCWA_SLC_04"]

    # R_sd = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12),
    #     (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12),
    #     (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12),
    #     (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12),
    #     (7,8), (7,9), (7,10), (7,11), (7,12),(8,9), (8,10), (8,11), (8,12), (9,10), (9,11), (9,12), (10,11), (10,12), (11,12)
    #     ]

    R_sd = []
    for src in graph.nodes:
        for dest in graph.nodes:
            if src != dest:
                R_sd.append((src, dest))
    
    r_num =  generate_request()

    R_error = False
    R:dict[int,tuple[int,int]] = {}
    num = 1
    if len(R_sd) != len(r_num):
        R_error = True
        print("リクエストの長さが異なる。")
    else:
        for i in range(len(r_num)):
            for j in range(r_num[i]):
                R[num] = R_sd[i]
                num = num+1
    
    R_number = sum(r_num)
    print(f"リクエストの数：{R_number}")
    print(f"モデル：{models}")
    print(f"ネットワークトポロジー：{topology_name}")
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y" and not R_error:

        df_list: list[pd.DataFrame] = []
        for model_name in models:
            print("モデル名：", model_name)
            visualized_links:dict[tuple[int,int,int],list[str]] = {}
            runtime, w_used, w_max = execute_a_model(model_name=model_name, graph=graph, R=R, visualized_links=visualized_links)
            wavelength_list = [f"'{w}" for w in range(1,w_max+1)]
            df_list.append(pd.DataFrame(visualized_links.values(), index=[f"'{links}" for links in visualized_links.keys()], columns=wavelength_list))
            print("時間：", runtime)
        
        
        # ディレクトリがない場合、生成
        dir = f"./results/{topology_name}/"
        if not os.path.exists(dir):
            if not os.path.exists("./results"):
                os.mkdir("./results")
                os.mkdir(dir)
            else:
                os.mkdir(dir)
        
        file = dir + f"results_request_{R_number}_visualized_links.xlsx"
        # Excelに書き込み
        with pd.ExcelWriter(file) as writer:
            for i in range(len(df_list)):
                df_list[i].to_excel(writer, sheet_name=models[i])

