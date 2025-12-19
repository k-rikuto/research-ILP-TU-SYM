from Network_Topology import get_topology
from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from ILP_RWA_01 import ILP_RWA_01
from ILP_RWA_02 import ILP_RWA_02
from ILP_RWA_03 import ILP_RWA_03
from empty_save import empty_save

import random as rd
import os
import pickle

# RCWAモデル
MODEL_RCWA = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03"]

# RWAモデル
MODEL_RWA = ["ILP_RWA_01", "ILP_RWA_02", "ILP_RWA_03"]

def timelimit():

    ## 変更場所
    R_number = 60   # リクエストの数
    model = MODEL_RCWA[0]       # 検証で扱うモデル
    timelimit = 50

    # 実験に使用するネットワークトポロジーを選択する
    # ネットワークトポロジー1（ノード6リンク9）
    graph,topology_name = get_topology(topology_number=1)

    # ネットワークトポロジー2（ノード6メッシュ型）
    # graph,topology_name = get_topology(topology_number=2)

    # ネットワークトポロジー3（JPN12）
    # graph,topology_name = get_topology(topology_number=3)

    # ネットワークトポロジー4（European Backbone Network, EBN）
    # graph,topology_name = get_topology(topology_number=4)

    if os.path.exists("./save/model_detail.txt"):
        print("モデルの再開")
        with open("./save/model_detail.txt", 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            R_number = int(lines[0])
            model = lines[1]
            topology_name = lines[2]
        print(f"リクエストの数：{R_number}")
        print(f"モデル：{model}")
        print(f"ネットワークトポロジー：{topology_name}")
        var = input("実行を続けますか？[Y/n]：")
        if var == "Y":  pass
        else:   return

        # 保存されたパラメータを取得
        with open("./save/parameter.pickle", 'rb') as f:
            data = pickle.load(f)
        graph = data["graph"]
        R = data["R"]
        W = data["W"]
        C = data["C"]
        isOptimal,runtime,wavelength = eval(model)(graph=graph, R=R, W=W, C=C, timelimit=timelimit, restart=True)

    else:
        # 実験に使用するネットワークトポロジーを選択する
        # ネットワークトポロジー4（European Backbone Network, EBN）
        graph,topology_name = get_topology(topology_number=4)

        # 実行確認
        # 変更が反映されてない状態で実行してしまうのを防ぐために確認する
        print(f"リクエストの数：{R_number}")
        print(model)
        print(f"ネットワークトポロジー：{topology_name}")
        var = input("実行を続けますか？[Y/n]：")
        if var == "Y":  pass
        else:   return
        with open("./save/model_detail.txt", 'w') as f:
            f.write(f'{R_number}\n{model}\n{topology_name}')

        # ノード集合からリクエストを生成するため
        V = set(graph.nodes)
        # 波長
        W_number = 30
        W = {i+1 for i in range(W_number)}
        # コアの集合
        C = {1, 2, 3, 4}
        # リクエストの集合
        R = {}

        # リクエストをR_numberの個数分、ランダムで生成する。
        for r in range(1,R_number+1):
            # ノードリストの中から2つをランダムで選択する
            [src, dist] = rd.sample(list(V), 2)
            R[r] = (src, dist)
        
        # パラメータを保存するためのデータ構造
        data = {"graph":graph, "R":R, "W":W, "C":C}
        with open("./save/parameter.pickle",'wb') as f:
            pickle.dump(data, f)

        isOptimal,runtime,wavelength = eval(model)(graph=graph, R=R, W=W, C=C, timelimit=timelimit)
    
    if isOptimal:
        print("実行完了")
        print(f"計算時間：{runtime}")
        print(f"波長の数：{wavelength}")
        # 保存したファイルを削除
        empty_save()
    else:
        print('タイムアウトで終了')

timelimit()
