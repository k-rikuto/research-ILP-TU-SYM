import random
from tqdm import tqdm

from Network_Topology import getTopology
from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from ILP_RWA_01 import ILP_RWA_01
from ILP_RWA_02 import ILP_RWA_02
from ILP_RWA_03 import ILP_RWA_03
from Results_to_Excel import results_to_excel

# RCWAモデル
MODEL_RCWA = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03"]

# RWAモデル
MODEL_RWA = ["ILP_RWA_01", "ILP_RWA_02", "ILP_RWA_03"]

def main():
    # 変更場所
    R_number = 100           # リクエストの数
    number_of_running = 50   # 実験回数
    model = MODEL_RWA       # 検証で扱うモデル

    # 実行確認
    # 変更が反映されてない状態で実行してしまうのを防ぐために確認する
    print(f"リクエストの数：{R_number}")
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":  pass
    else:   return

    # 実験に使用するネットワークトポロジーを選択する
    # ネットワークトポロジー1（ノード6リンク9）
    graph,topology_name = getTopology(topology_number=1)

    # ネットワークトポロジー2（ノード6メッシュ型）
    # graph,topology_name = getTopology(topology_number=2)

    # ネットワークトポロジー3（JPN12）
    # graph,topology_name = getTopology(topology_number=3)


    # モデルごとの結果
    results = {m:[] for m in model}

    # モデルごとのruntime結果
    results_runtime = {m:[] for m in model}

    # モデルごとのwavelength結果
    results_wavelength = {m:[] for m in model}

    # ノード集合からリクエストを生成するため
    V = set(graph.nodes)

    # 波長
    W_number = 30
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    # リクエストの集合
    R = {}


    for i in tqdm(range(number_of_running), leave=False):
        # リクエストをR_numberの個数分、ランダムで生成する。
        for r in range(1,R_number+1):
            # ノードリストの中から2つをランダムで選択する
            [src, dist] = random.sample(list(V), 2)
            R[r] = (src, dist)

        for m in tqdm(model, leave=False):
            if model == MODEL_RCWA:
                runtime,wavelength = eval(m)(graph=graph, R=R, W=W, C=C)
            else:
                runtime,wavelength = eval(m)(graph=graph, R=R, W=W)
            results[m].append((runtime, wavelength))
            results_runtime[m].append(runtime)
            results_wavelength[m].append(wavelength)

    # モデルごとに平均の計算
    for m in model:
        time_total = sum(results_runtime[m])
        time_average = time_total/len(results_runtime[m])
        w_total = sum(results_wavelength[m])
        w_average = w_total/len(results_wavelength[m])
        results[m].append((time_average,w_average))
    
    if model == MODEL_RCWA:
        results_to_excel(results=results, number_of_runnning=number_of_running, topology_name=topology_name, R_number=R_number)
    else:
        results_to_excel(results=results, number_of_runnning=number_of_running, topology_name=topology_name, R_number=R_number, isRWA=True)

    return



main()