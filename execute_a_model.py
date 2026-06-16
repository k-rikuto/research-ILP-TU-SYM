import networkx as nx

from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_04 import ILP_RCWA_04
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from ILP_RCWA_SLC_04 import ILP_RCWA_SLC_04
from Network_Topology import get_topology

def execute_a_model(model_name:str, graph:nx.Graph, R:dict[int,tuple[int,int]]) -> tuple[float, int]:

    
    # 波長
    W_number = 50
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    if model_name == "ILP_RCWA_01":
        isOptimal, runtime, wavelength = ILP_RCWA_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_02":
        isOptimal, runtime, wavelength = ILP_RCWA_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_03":
        isOptimal, runtime, wavelength = ILP_RCWA_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_04":
        isOptimal, runtime, wavelength = ILP_RCWA_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_01":
        isOptimal, runtime, wavelength = ILP_RCWA_SLC_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_02":
        isOptimal, runtime, wavelength = ILP_RCWA_SLC_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_03":
        isOptimal, runtime, wavelength = ILP_RCWA_SLC_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_04":
        isOptimal, runtime, wavelength = ILP_RCWA_SLC_04(graph=graph, R=R, W=W, C=C)
    else:
        runtime = 0.0
        wavelength = 0
        isOptimal = False




if __name__ == "__main__":
    # 実験に使用するネットワークトポロジーを選択する
    # ネットワークトポロジー1（ノード6リンク9）
    # graph,topology_name = get_topology(topology_number=1)

    # ネットワークトポロジー2（ノード6メッシュ型）
    # graph,topology_name = get_topology(topology_number=2)

    # ネットワークトポロジー3（JPN12）
    graph,topology_name = get_topology(topology_number=3)

    # # ネットワークトポロジー4（European Backbone Network, EBN）
    # graph,topology_name = get_topology(topology_number=4)

    print(f"リクエストの数：{R_number}")
    print(f"モデル：{model_name}")
    print(f"実行回数：{number_of_running}")
    print(f"ネットワークトポロジー：{topology_name}")
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":
        g

