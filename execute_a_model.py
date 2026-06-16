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

def execute_a_model(model_name:str, graph:nx.Graph, R:dict[int,tuple[int,int]]) -> tuple[float, int]:

    
    # 波長
    W_number = 50
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    if model_name == "ILP_RCWA_01":
        isOptimal, runtime, wavelength, data = ILP_RCWA_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_02":
        isOptimal, runtime, wavelength, data = ILP_RCWA_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_03":
        isOptimal, runtime, wavelength, data = ILP_RCWA_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_04":
        isOptimal, runtime, wavelength, data = ILP_RCWA_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_01":
        isOptimal, runtime, wavelength, data = ILP_RCWA_SLC_01(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_02":
        isOptimal, runtime, wavelength, data = ILP_RCWA_SLC_02(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_03":
        isOptimal, runtime, wavelength, data = ILP_RCWA_SLC_03(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RCWA_SLC_04":
        isOptimal, runtime, wavelength, data = ILP_RCWA_SLC_04(graph=graph, R=R, W=W, C=C)
    elif model_name == "ILP_RWA_01":
        isOptimal, runtime, wavelength, data = ILP_RWA_01(graph=graph, R=R, W=W)
    elif model_name == "ILP_RWA_02":
        isOptimal, runtime, wavelength, data = ILP_RWA_02(graph=graph, R=R, W=W)
    elif model_name == "ILP_RWA_03":
        isOptimal, runtime, wavelength, data = ILP_RWA_03(graph=graph, R=R, W=W)
    else:
        runtime = 0.0
        wavelength = 0
        isOptimal = False
    
    print(__name__)
    if __name__ == "__main__":
        if isOptimal:
            for r in data:
                print(f"リクエスト{r}:{data[r]["Request"]}")
                print(f"パス：{data[r]["Path"]}")
                print(f"波長：{data[r]["Wavelength"]}")
    
    return runtime, wavelength




if __name__ == "__main__":
    # 実験に使用するネットワークトポロジーを選択する
    graph,topology_name = get_topology(topology_number=3)
    model_name = "ILP_RWA_01"

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
        runtime, wavelength = execute_a_model(model_name=model_name, graph=graph, R=R)
    
    print(runtime,wavelength)

