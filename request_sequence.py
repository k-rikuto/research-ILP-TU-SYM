import random as rd
from tqdm import tqdm
import gurobipy as gp
import os

from Network_Topology import get_topology
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
from Results_to_Excel import results_to_excel
from Analyze_Request import analyze_request

# RCWAモデル
MODEL_RCWA = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03"]

# RWAモデル
MODEL_RWA = ["ILP_RWA_01", "ILP_RWA_02", "ILP_RWA_03"]

# 全てのモデル
MODEL_ALL = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03", "ILP_RWA_01", "ILP_RWA_02", "ILP_RWA_03"]

# 対称性のモデル
MODEL_SYMMETRY = ["ILP_RCWA_01", "ILP_RCWA_04", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_04"]

# model04を含めたすべてのモデル
MODEL = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_04","ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03", "ILP_RCWA_SLC_04"]

def request_sequence():
    ## 変更場所
    R_number = 100           # リクエストの数
    number_of_running = 20   # 試行回数
    model = MODEL       # 検証で扱うモデル


    # 実験に使用するネットワークトポロジーを選択する
    # ネットワークトポロジー1（ノード6リンク9）
    # graph,topology_name = get_topology(topology_number=1)

    # ネットワークトポロジー2（ノード6メッシュ型）
    # graph,topology_name = get_topology(topology_number=2)

    # ネットワークトポロジー3（JPN12）
    graph,topology_name = get_topology(topology_number=3)

    # # ネットワークトポロジー4（European Backbone Network, EBN）
    # graph,topology_name = get_topology(topology_number=4)

    # 実行確認
    # 変更が反映されてない状態で実行してしまうのを防ぐために確認する
    print(f"リクエストの数：{R_number}")
    print(f"モデル：{model}")
    print(f"実行回数：{number_of_running}")
    print(f"ネットワークトポロジー：{topology_name}")
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":  pass
    else:   return


    # モデルごとの結果
    results = {m:[] for m in model}
    results_nonseq = {m:[] for m in model}

    # ノード集合からリクエストを生成するため
    V = set(graph.nodes)

    # 波長
    W_number = 50
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    # リクエストの集合
    R = {}
    R_nonseq = {}

    # モデルごとのruntime結果
    results_runtime = {m:[] for m in model}
    results_nonseq_runtime = {m:[] for m in model}

    # モデルごとのwavelength結果
    results_wavelength = {m:[] for m in model}
    results_nonseq_wavelength = {m:[] for m in model}


    for i in tqdm(range(number_of_running), leave=False):
        # リクエストをR_numberの個数分、ランダムで生成する。
        for r in range(1,R_number+1):
            # ノードリストの中から2つをランダムで選択する
            [src, dist] = rd.sample(list(V), 2)
            R[r] = (src, dist)
            if src < dist: R_nonseq[r] = (src, dist)
            else: R_nonseq[r] = (dist, src)

        for m in tqdm(model, leave=False):
            # R
            isOptimal,runtime,wavelength = eval(m)(graph=graph, R=R, W=W, C=C)
            results[m].append((runtime, wavelength))
            results_runtime[m].append(runtime)
            results_wavelength[m].append(wavelength)
            # R_nonseq
            isOptimal,runtime,wavelength = eval(m)(graph=graph, R=R_nonseq, W=W, C=C)
            results_nonseq[m].append((runtime, wavelength))
            results_nonseq_runtime[m].append(runtime)
            results_nonseq_wavelength[m].append(wavelength)
    

    # モデルごとに平均の計算
    for m in model:
        # R
        time_total = sum(results_runtime[m])
        time_average = time_total/len(results_runtime[m])
        w_total = sum(results_wavelength[m])
        w_average = w_total/len(results_wavelength[m])
        results[m].append((time_average,w_average))

        #R_nonseq
        time_total = sum(results_nonseq_runtime[m])
        time_average = time_total/len(results_nonseq_runtime[m])
        w_total = sum(results_nonseq_wavelength[m])
        w_average = w_total/len(results_nonseq_wavelength[m])
        results_nonseq[m].append((time_average,w_average))

    
    
    # ディレクトリがない場合、生成
    dir = f"./results/{topology_name}/"
    if not os.path.exists(dir):
        if not os.path.exists("./results"):
            os.mkdir("./results")
            os.mkdir(dir)
        else:
            os.mkdir(dir)
    
    file = dir + f"results_request_{R_number}.xlsx"
    results_to_excel(results=results, number_of_runnning=number_of_running, file=file)
    file = dir + f"results_request_nonseq_{R_number}.xlsx"
    results_to_excel(results=results_nonseq, number_of_runnning=number_of_running, file=file)

    return



if __name__ == "__main__":
    request_sequence()